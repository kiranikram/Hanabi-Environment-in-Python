import gym
import torch
from game import full_game_dynamics
import collections
import DRQNAgent_wtest
from torch.autograd import Variable
import numpy as np
import pandas as pd

# env = gym.make("HanabiEnv-v0")
game = full_game_dynamics
agent = DRQNAgent_wtest




def initialize_hidden():
    hidden = torch.zeros(2, 1, 128)
    hidden_tar = torch.zeros(2, 1, 128)

    return hidden, hidden_tar


def update_game_records(p1_records, p2_records, current_player, action, hidden_st, hidden_tar_st):
    step_dict = dict(player=current_player, action=action, hidden_st=hidden_st, hidden_tar_st=hidden_tar_st)
    for key in current_player:
        if key == "Player_One":
            p1_records.append(step_dict)
        else:
            p2_records.append(step_dict)

    return p1_records, p2_records


def get_game_records(current_player, p1_records, p2_records):
    for key in current_player:
        if key == "Player_One":
            if len(p1_records) == 0:
                action = 0
                hidden_st, hidden_tar_st = initialize_hidden()
            elif len(p1_records) == 1:
                prev_step = p1_records[0]
                action = prev_step['action']
                hidden_st = prev_step['hidden_st']
                hidden_tar_st = prev_step['hidden_tar_st']

            elif len(p1_records) >= 1:
                prev_time = len(p1_records) - 2
                prev_step = p1_records[prev_time]
                action = prev_step['action']
                hidden_st = prev_step['hidden_st']
                hidden_tar_st = prev_step['hidden_tar_st']


        elif key == "Player_Two":
            if len(p2_records) == 0:
                action = 0
                hidden_st, hidden_tar_st = initialize_hidden()
            elif len(p2_records) == 1:

                prev_step = p2_records[0]
                action = prev_step['action']
                hidden_st = prev_step['hidden_st']
                hidden_tar_st = prev_step['hidden_tar_st']

            elif len(p2_records) >= 1:

                prev_time = len(p2_records) - 2
                prev_step = p2_records[prev_time]
                action = prev_step['action']
                hidden_st = prev_step['hidden_st']
                hidden_tar_st = prev_step['hidden_tar_st']

        return action, hidden_st, hidden_tar_st


def parse_observations(observations):
    unique_player_obs_set = {}
    legal_own_actions = []
    legal_hint_actions = []
    full_obs_tensor = observations[3]
    player_legal_actions = []

    for key in observations[4]:

        if key == "Player_One":

            x = "Player_One"

            teammate = 99
            teammate_hand = observations[1]
            own_hand = observations[0]
            current_player = observations[4]

            legal_own_actions = game.define_legal_own_actions(own_hand, current_player[x])

            legal_hint_actions = game.define_legal_hint_actions(teammate_hand, full_obs_tensor, teammate)
            unique_player_obs_set.update(observations[5])
            unique_player_obs_set.update(observations[6])

        elif key == "Player_Two":
            x = "Player_Two"

            teammate = 98
            teammate_hand = observations[0]
            own_hand = observations[1]

            current_player = observations[4]

            legal_own_actions = game.define_legal_own_actions(own_hand, current_player[x])

            legal_hint_actions = game.define_legal_hint_actions(teammate_hand, full_obs_tensor, teammate)

            unique_player_obs_set.update(observations[7])
            unique_player_obs_set.update(observations[8])

    player_legal_actions.extend(legal_hint_actions)
    player_legal_actions.extend(legal_own_actions)
    unique_player_obs_set.update(observations[9])

    return current_player, unique_player_obs_set, full_obs_tensor, player_legal_actions


def record_transition(transitions, current_player, reward, pol_action_val, tar_action_val, Records):
    transitions[current_player].append(Records(reward, pol_action_val, tar_action_val))
    return transitions


def run_game(step_count, target_update, train_mode):
    env = gym.make("HanabiEnv-v0")

    loss = 0
    Records = collections.namedtuple(
        'Records', ['reward', 'policy_q_val', 'target_q_val'])
    actions_unavailable = []
    player1_records = []
    player2_records = []
    transitions = [[] for _ in range(2)]  # no of players

    initial_observations = env.reset()



    ini_current_player, ini_obs_dict, obs_tensor, player_legal_actions = parse_observations(initial_observations)

    hidden, hidden_tar = initialize_hidden()

    action, hidden_opn, hidden_tar_opn, cp_record, pol_val, tar_val = agent.Agent().begin_episode(ini_current_player,
                                                                                                  player_legal_actions,
                                                                                                  ini_obs_dict,
                                                                                                  obs_tensor,
                                                                                                  hidden, hidden_tar)

    transitions = record_transition(transitions, cp_record, 0, pol_val, tar_val, Records)

    actions_unavailable.append(action)

    player1_records, player2_records = update_game_records(player1_records, player2_records, ini_current_player, action,
                                                           hidden_opn, hidden_tar_opn)

    is_done = False

    total_reward = 0
    step_number = 0
    while not is_done:

        observations, reward, is_done, info = env.step(action)
        evolved_deck = observations[2]
        allowed_actions = game.add_actions_back(evolved_deck, step_number)


        agent.Agent().store_observations(observations)

        # when we run multiple episodes we can ammend tp "+= reward"
        total_reward = reward

        step_number += 1
        if is_done:
            break

        current_player, observation_vector, observation_tensor, legal_moves = parse_observations(observations)

        player_legal_actions = game.filter_legal_actions(legal_moves, actions_unavailable, observation_tensor)
        if not player_legal_actions:
            break

        prev_action, prev_hidden, prev_hidden_tar = get_game_records(current_player, player1_records, player2_records)

        action, hidden_tr, tar_hidden_tr, cp_record, pol_val, tar_val = agent.Agent().step(current_player,
                                                                                           player_legal_actions,
                                                                                           observation_vector,
                                                                                           observation_tensor,
                                                                                           prev_action,
                                                                                           prev_hidden,
                                                                                           prev_hidden_tar,
                                                                                           train_mode)
        # step_count,
        # target_update)
        if step_number % 100 == 0:
            print('action selected at step ', step_number, 'is', action)

        reward = Variable(torch.tensor(reward))
        transitions = record_transition(transitions, cp_record, reward, pol_val, tar_val, Records)

        player1_records, player2_records = update_game_records(player1_records, player2_records, current_player,
                                                               action,
                                                               hidden_tr, tar_hidden_tr)

        actions_unavailable = game.make_reavailable(actions_unavailable, allowed_actions)
        actions_unavailable.append(action)



        # agent.hidden_states(hidden_tr,tar_hidden_tr)

    if train_mode:
        loss = agent.Agent().end_episode(transitions, step_count, target_update)


    if step_number % 1000 == 0:
        print('Game reward is ', total_reward)
    return step_number, total_reward, loss


def run_one_phase(min_steps, target_update, eval_every_n):
    print('****TRAINING NOW****')
    step_count = 0
    eval_step_count = 0
    num_episodes = 0
    eval_num_episodes = 0
    sum_returns = 0
    eval_sum_returns = 0

    avg_reward = []
    avg_steps = []
    eval_avg_reward = []
    eval_avg_steps = []
    loss_list = []

    while step_count < min_steps:
        episode_length, episode_return, episode_loss = run_game(step_count, target_update, train_mode=True)

        step_count += episode_length
        sum_returns += episode_return

        num_episodes += 1
        loss_list.append(episode_loss.item())

        if step_count % 100 == 0:
            print('TRAINING; Avg Return:', sum_returns / num_episodes)
            print('TRAINING; Avg Steps:', step_count / num_episodes)
            avg_reward.append(sum_returns / num_episodes)
            avg_steps.append(step_count / num_episodes)

        if step_count % eval_every_n == 0:

            eval_episode_length, eval_episode_return, _ = run_game(step_count, target_update, train_mode=False)
            eval_step_count += eval_episode_length
            eval_sum_returns += eval_episode_return
            eval_num_episodes += 1
            eval_avg_reward.append(sum_returns / num_episodes)
            eval_avg_steps.append(step_count / num_episodes)

    print('END; Avg Return:', sum_returns / num_episodes)
    print('END; Avg Steps:', step_count / num_episodes)

    avg_reward = np.array(avg_reward)
    avg_steps = np.array(avg_steps)
    loss_list = np.array(loss_list)

    eval_avg_reward = np.array(eval_avg_reward)
    eval_avg_steps = np.array(eval_avg_steps)

    training_df = pd.DataFrame(avg_reward, columns=['Avg Reward'])
    training_df['Avg Steps'] = avg_steps

    eval_df = pd.DataFrame(eval_avg_reward, columns=['Eval Avg Reward'])
    eval_df['Eval Avg Steps'] = eval_avg_steps

    loss_df = pd.DataFrame(loss_list, columns=['Running Loss'])

    print('\n', training_df.head())
    print('\n', eval_df.head())
    training_df.to_csv("Training Scores.csv")
    eval_df.to_csv("Eval Scores.csv")
    loss_df.to_csv("Running Loss.csv")

    return step_count, sum_returns, num_episodes


run_one_phase(10000000, 10, 1000)
