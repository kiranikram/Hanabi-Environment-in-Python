import gym
import envs
import torch
from game import full_game_dynamics, full_game_evolution_3p, full_game_dynamics_3p, fullBU_game_dynamics_3p
import collections
from agents import DRQNAgent_wtest, full_DRQNAgent_wtest
from torch.autograd import Variable
import numpy as np
import pandas as pd

# env = gym.make("HanabiEnv-v0")
game = fullBU_game_dynamics_3p
agent = full_DRQNAgent_wtest


class Hidden(object):

    def __init__(self):
        self.hidden_tar = torch.zeros(2, 1, 128)
        self.hidden = torch.zeros(2, 1, 128)
        self.player_one_records = []
        self.player_two_records = []
        self.player_three_records = []

    def initialize_hidden(self):
        return self.hidden, self.hidden_tar

    def update_game_records(self, p1_records, p2_records, p3_records, current_player, action, hidden_st, hidden_tar_st):
        step_dict = dict(player=current_player, action=action, hidden_st=hidden_st, hidden_tar_st=hidden_tar_st)
        for key in current_player:
            if key == "Player_One":
                p1_records.append(step_dict)
            elif key == "Player_Two":
                p2_records.append(step_dict)
            else:
                p3_records.append(step_dict)

        return p1_records, p2_records, p3_records

    def get_game_records(self, current_player, p1_records, p2_records,p3_records):
        for key in current_player:
            if key == "Player_One":
                if len(p1_records) == 0:
                    action = 0
                    hidden_st, hidden_tar_st = self.initialize_hidden()
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

                    # if hidden_tar_st.size == (0,):
                    # prev_step = len(p1_records) - 3
                    # hidden_tar_st = prev_step['hidden_tar_st']


            elif key == "Player_Two":
                if len(p2_records) == 0:
                    action = 0
                    hidden_st, hidden_tar_st = self.initialize_hidden()
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

                    # if hidden_tar_st.size == (0,):
                    # prev_step = len(p2_records) - 3
                    # hidden_tar_st = prev_step['hidden_tar_st']

            elif key == "Player_Three":
                if len(p3_records) == 0:
                    action = 0
                    hidden_st, hidden_tar_st = self.initialize_hidden()
                elif len(p3_records) == 1:

                    prev_step = p3_records[0]
                    action = prev_step['action']
                    hidden_st = prev_step['hidden_st']
                    hidden_tar_st = prev_step['hidden_tar_st']

                elif len(p3_records) >= 1:

                    prev_time = len(p3_records) - 2
                    prev_step = p3_records[prev_time]
                    action = prev_step['action']
                    hidden_st = prev_step['hidden_st']
                    hidden_tar_st = prev_step['hidden_tar_st']

                    # if hidden_tar_st.size == (0,):
                    # prev_step = len(p2_records) - 3
                    # hidden_tar_st = prev_step['hidden_tar_st']

        # print('p1 LEN', len(p1_records), 'P1 HIDDEN', hidden_st, 'P1 TAR', hidden_tar_st)
        # print('p2 LEN', len(p2_records),  'P1 HIDDEN', hidden_st, 'P1 TAR',hidden_tar_st)
        return action, hidden_st, hidden_tar_st


def parse_observations(observations):

    unique_player_obs_set = {}
    legal_own_actions = []
    legal_hint_actions = []
    full_obs_tensor = observations[4]
    player_legal_actions = []
    current_player = observations[5]

    for key in observations[5]:

        if key == "Player_One":
            # offsetting player will be Player 2

            x = "Player_One"

            teammate = 99
            teammate_hand = observations[1]
            own_hand = observations[0]
            current_player = observations[5]

            legal_own_actions = game.define_legal_own_actions(own_hand, current_player[x])

            legal_hint_actions = game.define_legal_hint_actions(teammate_hand, full_obs_tensor, teammate)
            unique_player_obs_set.update(observations[6])
            unique_player_obs_set.update(observations[7])

            unique_player_obs_set.update(teammate_hand)

        elif key == "Player_Two":
            # offsetting player will be  Player 3
            x = "Player_Two"

            teammate = 98
            teammate_hand = observations[2]
            own_hand = observations[1]

            current_player = observations[5]

            legal_own_actions = game.define_legal_own_actions(own_hand, current_player[x])

            legal_hint_actions = game.define_legal_hint_actions(teammate_hand, full_obs_tensor, teammate)

            unique_player_obs_set.update(observations[8])
            unique_player_obs_set.update(observations[9])

            unique_player_obs_set.update(teammate_hand)

        elif key == "Player_Three":
            #offsetting player will be Player 1
            x = "Player_Three"

            teammate = 97
            teammate_hand = observations[0]
            own_hand = observations[2]

            current_player = observations[5]

            legal_own_actions = game.define_legal_own_actions(own_hand, current_player[x])

            legal_hint_actions = game.define_legal_hint_actions(teammate_hand, full_obs_tensor, teammate)

            unique_player_obs_set.update(observations[10])
            unique_player_obs_set.update(observations[11])

            unique_player_obs_set.update(teammate_hand)

    player_legal_actions.extend(legal_hint_actions)
    player_legal_actions.extend(legal_own_actions)
    unique_player_obs_set.update(observations[12])

    return current_player, unique_player_obs_set, full_obs_tensor, player_legal_actions


def record_transition(transitions, current_player, reward, pol_action_val, tar_action_val, Records):
    transitions[current_player].append(Records(reward, pol_action_val, tar_action_val))
    return transitions





def run_game(step_count, target_update, train_mode):
    stacker = Hidden()
    env = gym.make("HanabiEnv-v0")

    loss = 0
    Records = collections.namedtuple(
        'Records', ['reward', 'policy_q_val', 'target_q_val'])
    actions_unavailable = []

    transitions = [[] for _ in range(3)]  # no of players

    initial_observations = env.reset()

    ini_current_player, ini_obs_dict, obs_tensor, player_legal_actions = parse_observations(initial_observations)

    hidden, hidden_tar = stacker.initialize_hidden()

    action, hidden_opn, hidden_tar_opn, cp_record, pol_val, tar_val = agent.Agent().begin_episode(ini_current_player,
                                                                                                  player_legal_actions,
                                                                                                  ini_obs_dict,
                                                                                                  obs_tensor,
                                                                                                  hidden, hidden_tar)

    transitions = record_transition(transitions, cp_record, 0, pol_val, tar_val, Records)

    actions_unavailable.append(action)

    stacker.player_one_records, stacker.player_two_records, stacker.player_three_records = stacker.update_game_records(stacker.player_one_records,
                                                                                         stacker.player_two_records,
                                                                                         stacker.player_three_records,
                                                                                         ini_current_player, action,
                                                                                         hidden_opn, hidden_tar_opn)

    is_done = False

    total_reward = 0
    step_number = 0
    while not is_done:

        observations, reward, is_done, info = env.step(action)
        evolved_deck = observations[3]
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

        prev_action, prev_hidden, prev_hidden_tar = stacker.get_game_records(current_player, stacker.player_one_records,
                                                                             stacker.player_two_records, stacker.player_three_records)

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

        stacker.player_one_records, stacker.player_two_records , stacker.player_three_records = stacker.update_game_records(stacker.player_one_records,
                                                                                             stacker.player_two_records,
                                                                                             stacker.player_three_records,
                                                                                             current_player,
                                                                                             action, hidden_tr,
                                                                                             tar_hidden_tr)

        actions_unavailable = game.make_reavailable(actions_unavailable, allowed_actions)
        actions_unavailable.append(action)

        # agent.hidden_states(hidden_tr,tar_hidden_tr)

    if train_mode:
        loss = agent.Agent().end_episode(transitions, step_count, target_update)

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

        if step_count % 10 == 0:
            print('TRAINING; Avg Return:', sum_returns / num_episodes)
            print('TRAINING; Avg Steps:', step_count / num_episodes)
            avg_reward.append(sum_returns / num_episodes)
            avg_steps.append(step_count / num_episodes)

        if step_count % eval_every_n == 0:
            print('EVALUATING NOW')
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


run_one_phase(20000000, 10, 50)
