import letstest
import torch
import torch.nn as nn
import torch.optim as optim
import collections
import numpy as np
import random
import game_evolution
import DRQNet

Records = collections.namedtuple(
    'Records', ['reward', 'policy_q_val', 'target_q_val'])


class DIALAgent(object):

    def __init__(self):

        self.model = DRQNet.CNet()
        self.players = 2
        self.gamma = 0.99
        self.transitions = [[] for _ in range(self.players)]
        self.epsilon = 0.05
        self.trailing_action = []
        self.policy_net = DRQNet.CNet()
        self.target_net = DRQNet.CNet()
        self.all_observations = None
        self.hidden_state = None
        self.target_hidden_state = None
        self.optimizer = optim.RMSprop(params=self.model.get_params(), lr=0.005, momentum=0.05)

    def begin_episode(self, current_player, legal_actions, obs_dict, obs_tensor, hidden, hidden_tar):
        prev_action = 0

        hidden_t, q_s = self.policy_net(obs_dict, obs_tensor, hidden, prev_action, current_player)
        action, policy_q_val = self.select_action(legal_actions, q_s)

        hidden_tar_t, q_tar_s = self.target_net(obs_dict, obs_tensor, hidden_tar, prev_action, current_player)
        _, target_q_val = self.select_action(legal_actions, q_tar_s)

        self.record_transition(current_player, 0, policy_q_val, target_q_val)

        return action, hidden_t, hidden_tar_t

    def step(self, reward, current_player, legal_moves, observation_dict, observation_tensor, hidden, hidden_tar):

        prev_action = self.trailing_action[0]

        hidden_t, q_s = self.policy_net(observation_dict, observation_tensor, hidden, prev_action, current_player)
        action, policy_q_val = self.select_action(legal_moves, q_s)

        hidden_tar_t, target_q_s = self.target_net(observation_dict, observation_tensor, hidden_tar, prev_action,
                                                   current_player)
        _, target_q_val = self.select_action(legal_moves, target_q_s)

        self.record_transition(current_player, reward, policy_q_val, target_q_val)
        self.trailing_action = []

        action, policy_q_val = self.select_action(legal_moves, q_s)

        self.trailing_action.append(action)
        self.hidden_state = 0
        self.target_hidden_state = 0

        return action, hidden_t, hidden_tar_t

    def hidden_states(self, hidden, hidden_t):
        self.hidden_state = hidden
        self.target_hidden_state = hidden_t

        return self.hidden_state, self.target_hidden_state

    def store_observations(self, observations):
        self.all_observations = observations

    def clear_observations(self):
        self.all_observations = 0

    def end_episode(self, episode_steps):

        loss = self.get_loss(episode_steps)

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
            action_idx = legal_action_list.index(action)
            action_value = available_qs[action_idx]

        else:
            max_q = max(available_qs)
            max_q_index = available_qs.index(max_q)
            action = legal_action_list[max_q_index]
            action_value = max_q

        return action, action_value

    def record_transition(self, current_player, reward, pol_action_val, tar_action_val):

        self.transitions[current_player].append(Records(reward, pol_action_val, tar_action_val))

    def get_loss(self):

        agents_loss = 0
        for player in range(self.players):
            total_loss = 0
            num_transitions = len(self.transitions[player])

            for index, transition in enumerate(self.transitions[player]):
                reward = self.transitions[player][index]
                pol_action_val = self.transitions[player][index].pol_action_val
                final_transition = index == num_transitions - 1
                if final_transition:
                    td_action = reward - pol_action_val
                else:
                    tar_action_value = self.transitions[player][index + 1].tar_action_value
                    td_action = reward + self.gamma * tar_action_value - pol_action_val

                loss_t = td_action ** 2
                total_loss = total_loss + loss_t

            agents_loss = agents_loss + total_loss
        loss = agents_loss / self.players

        return loss

    def end_episode(self):

        self.optimizer.zero_grad()
        loss = self.get_loss()
        loss.backward()
        self.optimizer.step()

        if self.episodes % self.opts['step_target'] == 0:
            self.model_target.load_state_dict(self.model.state_dict())
