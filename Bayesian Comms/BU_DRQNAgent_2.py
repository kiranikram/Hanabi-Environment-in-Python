# import letstest
import torch
import torch.nn as nn
import torch.optim as optim
import collections
import numpy as np
import random
import game_evolution
import BU_DRQNet
import BU_game_dynamics
from torch.autograd import Variable
from torch.nn.utils import clip_grad_norm_

game = BU_game_dynamics

Records = collections.namedtuple(
    'Records', ['reward', 'policy_q_val', 'target_q_val'])


class Agent(object):

    def __init__(self):
        self.players = 2
        self.gamma = 0.99
        self.transitions = [[] for _ in range(self.players)]
        self.epsilon = 0.05
        self.trailing_action = []
        self.policy_net = BU_DRQNet.CNet()
        self.target_net = BU_DRQNet.CNet()
        self.all_observations = None
        self.hidden_state = None
        self.target_hidden_state = None
        self.optimizer = optim.RMSprop(params=self.policy_net.get_params(), lr=0.001, momentum=0.05)

    def begin_episode(self, current_player, legal_actions, obs_dict, obs_tensor, hidden, hidden_tar):
        prev_action = 0
        b_u = [0]

        oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, i_t, lives, act, cp = game.transform_inputs(obs_dict,
                                                                                                       obs_tensor,
                                                                                                       prev_action,
                                                                                                       current_player)

        hidden_t, q_s = self.policy_net(oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, b_u, i_t, lives, hidden, act,
                                        cp)
        action, policy_q_val = self.select_action(legal_actions, q_s)
        policy_q_val = Variable(torch.tensor(policy_q_val), requires_grad=True)

        hidden_tar_t, q_tar_s = self.target_net(oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, b_u, i_t, lives,
                                                hidden_tar, act, cp)
        _, target_q_val = self.select_action(legal_actions, q_tar_s)
        target_q_val = Variable(torch.tensor(target_q_val), requires_grad=True)

        curr_player = cp[0]

        # self.transitions = self.record_transition(cp[0], 0, policy_q_val, target_q_val)

        return action, hidden_t, hidden_tar_t, curr_player, policy_q_val, target_q_val

    def get_q_vals_tmp(self, oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, i_t, lives, hidden, action,
                       current_player):
        hidden_t, q_s = self.policy_net(oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, i_t, lives, hidden, action,
                                        current_player)

        return hidden_t, q_s

    def select_action(self, legal_action_arr, qs):

        """Args: legal_action_arr which is a list
         Returns: action in the form of a str"""

        legal_action_list = list(game_evolution.all_legal_actions)
        qs_list = qs.tolist()
        available_qs = []
        for j, k in zip(qs_list, legal_action_list):
            if int(k) in legal_action_arr:
                available_qs.append(j)
            else:
                available_qs.append(0.0)

        if random.random() <= self.epsilon:

            action = random.choice(legal_action_arr)
            action_idx = legal_action_list.index(str(action))
            action_value = available_qs[action_idx]

        else:

            max_q = max(available_qs)
            max_q_index = available_qs.index(max_q)
            action = legal_action_list[max_q_index]
            action_value = max_q

        return action, action_value

    def record_transition(self, current_player, reward, pol_action_val, tar_action_val):

        self.transitions[current_player].append(Records(reward, pol_action_val, tar_action_val))
        return self.transitions

    def hidden_states(self, hidden, hidden_t):
        self.hidden_state = hidden
        self.target_hidden_state = hidden_t

        return self.hidden_state, self.target_hidden_state

    ### WE ARE IN AGENT CLASS
    def step(self, current_player, legal_moves, observation_dict, observation_tensor, prev_action, hidden,
             hidden_tar, bu_msg):

        oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, i_t, lives, act, cp = game.transform_inputs(observation_dict,
                                                                                                       observation_tensor,
                                                                                                       prev_action,
                                                                                                       current_player)

        hidden_t, q_s = self.policy_net(oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, bu_msg, i_t, lives, hidden,
                                        act, cp)
        action, policy_q_val = self.select_action(legal_moves, q_s)
        policy_q_val = Variable(torch.tensor(policy_q_val), requires_grad=True)

        # for param in self.target_net.parameters():
        # print(param.data)

        hidden_tar_t, target_q_s = self.target_net(oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, bu_msg, i_t,
                                                   lives,
                                                   hidden_tar, act, cp)
        _, target_q_val = self.select_action(legal_moves, target_q_s)
        target_q_val = Variable(torch.tensor(target_q_val), requires_grad=True)

        # self.transitions = self.record_transition(cp[0], reward, policy_q_val, target_q_val)
        curr_player = cp[0]

        # action, policy_q_val = self.select_action(legal_moves, q_s)

        # self.trailing_action.append(action)
        self.hidden_state = 0
        self.target_hidden_state = 0

        return action, hidden_t, hidden_tar_t, curr_player, policy_q_val, target_q_val

    def store_observations(self, observations):
        self.all_observations = observations

    def clear_observations(self):
        self.all_observations = 0

    def get_loss(self, transitions):

        agents_loss = 0
        for player in range(self.players):
            total_loss = 0
            num_transitions = len(transitions[player])

            for index, transition in enumerate(transitions[player]):
                reward = transitions[player][index].reward  # double check

                pol_action_val = transitions[player][index].policy_q_val

                final_transition = index == num_transitions - 1
                if final_transition:
                    td_action = reward - pol_action_val
                else:
                    tar_action_value = transitions[player][index + 1].target_q_val
                    td_action = reward + self.gamma * tar_action_value - pol_action_val

                loss_t = td_action ** 2
                total_loss = total_loss + loss_t

            agents_loss = agents_loss + total_loss
        loss = agents_loss / self.players
        print('loos', loss)

        return loss

    def end_episode(self, transitions, steps, update_period):

        self.optimizer.zero_grad()
        loss = self.get_loss(transitions)
        print('loss from epi', loss)

        loss.backward()
        clip_grad_norm_(parameters=self.policy_net.get_params(), max_norm=10)
        self.optimizer.step()

        if steps % update_period == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        return loss

    def compute_prior_probs(self, teammate_hand, observations, action):

        all_playable_scores = []
        firework_values = []

        fireworks = observations[9]


        for key in fireworks:

            if key[0] == 'F':
                val = 0
            else:
                val = key[1]
            firework_values.append(int(val))
        if len(firework_values) <3:
            firework_values.append(0)

        if len(teammate_hand) > 2:

            for key in teammate_hand:
                p1 = int(key[1]) - firework_values[0]

                p2 = int(key[1]) - firework_values[1]

                if firework_values[2]:
                    p3 = int(key[1]) - firework_values[2]
                else:
                    p3 = int(key[1]) - 0

                pos_score = p1 + p2 + p3

                all_playable_scores.append(pos_score)

        elif len(teammate_hand) < 3:

            for key in teammate_hand:
                p1 = int(key[1]) - firework_values[0]
                p2 = int(key[1]) - firework_values[1]
                p3 = 0 - firework_values[2]

                pos_score = p1 + p2 + p3

                all_playable_scores.append(pos_score)
                all_playable_scores.append(0)

        if len(teammate_hand) < 2:
            all_playable_scores = [1, 0, 0]

        to_norm = min(all_playable_scores) * -1
        for i in range(len(all_playable_scores)):
            # print('playables pre norm', all_playable_scores)
            all_playable_scores[i] = all_playable_scores[i] + to_norm
            # print('post norm', all_playable_scores)

        total = sum(all_playable_scores)
        for i in range(len(all_playable_scores)):
            if total == 0:

                all_playable_scores[i] = 1.0
            else:
                all_playable_scores[i] = all_playable_scores[i] / total

        prior_prob_pos_1 = all_playable_scores[0]
        prior_prob_pos_2 = all_playable_scores[1]
        prior_prob_pos_3 = all_playable_scores[2]

        mpo, spo, tpo, mph, sph, tph = self.get_mle_data(all_playable_scores, action)

        return prior_prob_pos_1, prior_prob_pos_2, prior_prob_pos_3, mpo, spo, tpo, mph, sph, tph

    def get_mle_data(self, hand_rankings, action):

        max_pos_hint = 0
        sec_pos_hint = 0
        thr_pos_hint = 0
        max_pos_own = 0
        sec_pos_own = 0
        thr_pos_own = 0
        play_disc_singles = [7, 8, 9]
        play_disc_doubles = [10, 11, 12]
        hints = [1, 2, 3, 4, 5, 6]

        pos_played = str(action)[-1]

        pos_played = int(pos_played) - 1

        if len(str(action)) == 4:

            if int(str(action)[0]) in play_disc_singles:
                max_pos = hand_rankings.index(max(hand_rankings))
                sec_max_pos = hand_rankings.index(max(hand_rankings))
                if pos_played == max_pos:
                    max_pos_own = 1
                    hand_rankings.pop(max_pos)
                elif pos_played == sec_max_pos:
                    sec_pos_own = 1
                else:
                    thr_pos_own = 1

            elif int(str(action)[0]) in hints:

                max_pos = hand_rankings.index(max(hand_rankings))
                sec_max_pos = hand_rankings.index(max(hand_rankings))
                if pos_played == max_pos:
                    max_pos_hint = 1
                    hand_rankings.pop(max_pos)
                elif pos_played == sec_max_pos:
                    sec_pos_hint = 1
                else:
                    thr_pos_hint = 1

        elif len(str(action)) == 5:
            if int(str(action)[0:2]) in play_disc_doubles:

                max_pos = hand_rankings.index(max(hand_rankings))
                sec_max_pos = hand_rankings.index(max(hand_rankings))
                if pos_played == max_pos:
                    max_pos_own = 1
                    hand_rankings.pop(max_pos)
                elif pos_played == sec_max_pos:
                    sec_pos_own = 1
                else:
                    thr_pos_own = 1

        return max_pos_own, sec_pos_own, thr_pos_own, max_pos_hint, sec_pos_hint, thr_pos_hint
