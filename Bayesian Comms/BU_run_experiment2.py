import gym
import torch
import envs
import game_evolution
import BU_game_dynamics
import random
import collections
import BU_DRQNAgent_2
from torch.autograd import Variable
import matplotlib.pyplot as plt

# env = gym.make("HanabiEnv-v0")
game = BU_game_dynamics
agent = BU_DRQNAgent_2


class MLE_stacker(object):

    def __init__(self):
        self.max_pos_own = 1
        self.sec_pos_own = 1
        self.thr_pos_own = 1
        self.max_pos_hint = 1
        self.sec_pos_hint = 1
        self.thr_pos_hint = 1

    def add_mle_data(self, mpo, spo, tpo, mph, sph, tph):
        self.max_pos_own += mpo
        self.sec_pos_own += spo
        self.thr_pos_own += tpo
        self.max_pos_hint += mph
        self.sec_pos_hint += sph
        self.thr_pos_hint += tph

    def get_curr_data(self):
        return self.max_pos_own, self.sec_pos_own, self.thr_pos_own, self.max_pos_hint, \
               self.sec_pos_hint, self.thr_pos_hint

    def get_likelihoods(self):
        p1_mle = self.max_pos_hint / (self.max_pos_own * 2)
        p2_mle = self.sec_pos_hint / (self.sec_pos_own * 2)
        p3_mle = self.thr_pos_hint / (self.thr_pos_own * 2)

        return p1_mle, p2_mle, p3_mle


def initialize_hidden():
    hidden = torch.zeros(2, 1, 128)
    hidden_tar = torch.zeros(2, 1, 128)

    return hidden, hidden_tar


def update_game_records(p1_records, p2_records, current_player, action, hidden_st, hidden_tar_st):
    step_dict = dict(player=current_player, action=action, hidden_st=hidden_st, hidden_tar_st=hidden_tar_st)
    for key in current_player:
        if key == "Player_One":
            p1_records.append(step_dict)
        elif key == "Player_Two":
            p2_records.append(step_dict)

    return p1_records, p2_records


def update_msg_records(p1_msg_records, p2_msg_records, current_player, bu):
    for key in current_player:
        if key == "Player_One":
            p2_msg_records.append(bu)

        elif key == "Player_Two":
            p1_msg_records.append(bu)

    return p1_msg_records, p2_msg_records


def get_msg_records(current_player, p1_msg_records, p2_msg_records):
    for key in current_player:
        if key == "Player_One":
            if len(p1_msg_records) == 0:
                bu_msg = [0]
            else:
                bu_msg = p1_msg_records[0]
        elif key == "Player_Two":
            if len(p2_msg_records) == 0:
                bu_msg = [0]
            else:
                bu_msg = p2_msg_records[0]

    return bu_msg


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

    return current_player, unique_player_obs_set, full_obs_tensor, player_legal_actions, teammate_hand


def record_transition(transitions, current_player, reward, pol_action_val, tar_action_val, Records):
    transitions[current_player].append(Records(reward, pol_action_val, tar_action_val))
    return transitions


mle_stacker = MLE_stacker()

"""The position with the highest posterior probability  -- that needs to be matched to the hand it represents
to indicate a signal as to which card is most playable """


def compute_bayesian_update(p1_prior, p2_prior, p3_prior):

    p1_mle, p2_mle, p3_mle = mle_stacker.get_likelihoods()
    p_d = p1_mle * p1_prior + p2_mle * p2_prior + p3_mle * p3_prior

    p1_posterior = (p1_mle * p1_prior) / p_d
    p2_posterior = (p2_mle * p2_prior) / p_d
    p3_posterior = (p3_mle * p3_prior) / p_d

    all_posteriors = [p1_posterior,p2_posterior,p3_posterior]
    if all_posteriors.index((max(all_posteriors))) == 0:
        bu_msg = [1]
    elif all_posteriors.index((max(all_posteriors))) == 1:
        bu_msg = [2]
    elif all_posteriors.index((max(all_posteriors))) == 2:
        bu_msg = [3]

    return bu_msg


def run_game(step_count, target_update):
    env = gym.make("HanabiEnv-v0")
    Records = collections.namedtuple(
        'Records', ['reward', 'policy_q_val', 'target_q_val'])
    actions_unavailable = []
    player1_records = []
    player2_records = []
    p1_msg_records = []
    p2_msg_records = []
    transitions = [[] for _ in range(2)]  # no of players

    initial_observations = env.reset()

    ini_current_player, ini_obs_dict, obs_tensor, player_legal_actions, teammate_hand = parse_observations(
        initial_observations)

    hidden, hidden_tar = initialize_hidden()

    action, hidden_opn, hidden_tar_opn, cp_record, pol_val, tar_val = agent.Agent().begin_episode(ini_current_player,
                                                                                                  player_legal_actions,
                                                                                                  ini_obs_dict,
                                                                                                  obs_tensor,
                                                                                                  hidden, hidden_tar)

    priors1, priors2, priors3, mpo, spo, tpo, mph, sph, tph = agent.Agent().compute_prior_probs(teammate_hand,
                                                                                                initial_observations,
                                                                                                action)
    mle_stacker.add_mle_data(mpo, spo, tpo, mph, sph, tph)
    bu = compute_bayesian_update(priors1, priors2, priors3)
    p1_msg_records, p2_msg_records = update_msg_records(p1_msg_records, p2_msg_records, ini_current_player, bu)

    transitions = record_transition(transitions, cp_record, 0, pol_val, tar_val, Records)

    actions_unavailable.append(action)

    player1_records, player2_records = update_game_records(player1_records, player2_records, ini_current_player, action,
                                                           hidden_opn, hidden_tar_opn)

    is_done = False

    total_reward = 0
    step_number = 0
    while not is_done:

        observations, reward, is_done, _ = env.step(action)
        agent.Agent().store_observations(observations)

        # when we run multiple episodes we can ammend tp "+= reward"
        total_reward = reward
        step_number += 1
        if is_done:
            break

        current_player, observation_vector, observation_tensor, legal_moves, teammate_hand = parse_observations(
            observations)

        player_legal_actions = game.filter_legal_actions(legal_moves, actions_unavailable, observation_tensor)
        if not player_legal_actions:
            break

        prev_action, prev_hidden, prev_hidden_tar = get_game_records(current_player, player1_records, player2_records)

        bu_msg = get_msg_records(current_player, p1_msg_records, p2_msg_records)


        action, hidden_tr, tar_hidden_tr, cp_record, pol_val, tar_val = agent.Agent().step(current_player,
                                                                                           player_legal_actions,
                                                                                           observation_vector,
                                                                                           observation_tensor,
                                                                                           prev_action,
                                                                                           prev_hidden,
                                                                                           prev_hidden_tar,
                                                                                           bu_msg)
        # step_count,
        # target_update)
        priors1, priors2, priors3, mpo, spo, tpo, mph, sph, tph = agent.Agent().compute_prior_probs(teammate_hand,
                                                                                                    observations,
                                                                                                    action)
        mle_stacker.add_mle_data(mpo, spo, tpo, mph, sph, tph)
        bu = compute_bayesian_update(priors1,priors2,priors3)
        p1_msg_records, p2_msg_records = update_msg_records(p1_msg_records, p2_msg_records, ini_current_player, bu)



        if step_number % 100 == 0:
            print('action selected at step ', step_number, 'is', action)

        reward = Variable(torch.tensor(reward))
        transitions = record_transition(transitions, cp_record, reward, pol_val, tar_val, Records)

        player1_records, player2_records = update_game_records(player1_records, player2_records, current_player,
                                                               action,
                                                               hidden_tr, tar_hidden_tr)

        p1_msg_records, p2_msg_records = update_msg_records(p1_msg_records, p2_msg_records, ini_current_player, bu)

        actions_unavailable.append(action)

        # agent.hidden_states(hidden_tr,tar_hidden_tr)

    loss = agent.Agent().end_episode(transitions, step_count, target_update)

    print('Game reward is ', total_reward)
    return step_number, total_reward, loss


def run_one_phase(min_steps, target_update):
    print('****TRAINING NOW****')
    step_count = 0
    num_episodes = 0
    sum_returns = 0

    avg_reward = []
    avg_steps = []
    loss_list = []

    while step_count < min_steps:
        episode_length, episode_return, episode_loss = run_game(step_count, target_update)

        step_count += episode_length
        sum_returns += episode_return
        num_episodes += 1
        loss_list.append(episode_loss.item())

        if step_count % 50 == 0:
            print('TRAINING; Avg Return:', sum_returns / num_episodes)
            print('TRAINING; Avg Steps:', step_count / num_episodes)
            avg_reward.append(sum_returns / num_episodes)

            avg_steps.append(step_count / num_episodes)




    print('END; Avg Return:', sum_returns / num_episodes)
    print('END; Avg Steps:', step_count / num_episodes)
    print(loss_list)

    plt.plot(avg_reward, avg_steps)
    plt.show()

    return step_count, sum_returns, num_episodes


run_one_phase(10000, 10)
