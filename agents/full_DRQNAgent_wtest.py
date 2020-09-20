# import letstest
import torch
import torch.optim as optim
import collections
import random
from nets import DRQNet, DRQNet_3p, full_DRQNet
from game import full_game_dynamics_3p, full_game_evolution_3p, full_game_dynamics,full_game_evolution,\
    BU_game_dynamics, BU_game_evolution, fullBU_game_dynamics_3p
from game import permutations
from torch.autograd import Variable
from torch.nn.utils import clip_grad_norm_

"""Need to set these for game configuration"""
game = fullBU_game_dynamics_3p
evolution = full_game_evolution_3p

Records = collections.namedtuple(
    'Records', ['reward', 'policy_q_val', 'target_q_val'])


class Agent(object):

    def __init__(self):
        self.players = 2
        self.gamma = 0.99
        self.transitions = [[] for _ in range(self.players)]
        self.epsilon = 0.05
        self.trailing_action = []
        self.policy_net = full_DRQNet.CNet()
        self.target_net = full_DRQNet.CNet()
        self.all_observations = None
        self.hidden_state = None
        self.target_hidden_state = None
        self.optimizer = optim.RMSprop(params=self.policy_net.get_params(), lr=0.001, momentum=0.05)

    def begin_episode(self, current_player, legal_actions, obs_dict, obs_tensor, hidden, hidden_tar):

        prev_action = 0

        own_c, own_s, th_1, th_2, th_3, f_1, f_2, f_3,f_4, i_t, lives, act, cp = permutations.transform_inputs(
            obs_dict,
            obs_tensor,
            prev_action,
            current_player)


        hidden_t, q_s = self.policy_net(own_c,own_s, th_1, th_2, th_3, f_1, f_2, f_3,f_4, i_t, lives,
                                        hidden, act, cp)
        action, policy_q_val = self.select_action(legal_actions, q_s,train_mode=True)
        policy_q_val = Variable(torch.tensor(policy_q_val), requires_grad=True)

        hidden_tar_t, q_tar_s = self.target_net(own_c, own_s, th_1, th_2, th_3, f_1, f_2, f_3,f_4,
                                                i_t, lives,
                                                hidden_tar, act, cp)
        _, target_q_val = self.select_action(legal_actions, q_tar_s, train_mode=True)
        target_q_val = Variable(torch.tensor(target_q_val), requires_grad=True)

        curr_player = cp[0]

        # self.transitions = self.record_transition(cp[0], 0, policy_q_val, target_q_val)

        return action, hidden_t, hidden_tar_t, curr_player, policy_q_val, target_q_val



    def select_action(self, legal_action_arr, qs,  train_mode):


        """Args: legal_action_arr which is a list
         Returns: action in the form of a str"""

        if train_mode:
            self.epsilon = self.epsilon
        else:
            self.epsilon = 0
        legal_action_list = list(evolution.all_legal_actions)


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
             hidden_tar, train_mode=True):

        hidden_tar_t = 0
        target_q_val = 0


        own_c,own_s, th_1, th_2, th_3, f_1, f_2, f_3,f_4, i_t, lives, act, cp = permutations.transform_inputs(
            observation_dict,
            observation_tensor,
            prev_action,
            current_player)


        hidden_t, q_s = self.policy_net(own_c,own_s, th_1, th_2, th_3, f_1, f_2, f_3,f_4, i_t, lives,
                                        hidden, act, cp)
        action, policy_q_val = self.select_action(legal_moves, q_s,  train_mode)
        policy_q_val = Variable(torch.tensor(policy_q_val), requires_grad=True)

        # for param in self.target_net.parameters():
        # print(param.data)

        if train_mode:
            hidden_tar_t, target_q_s = self.target_net(own_c,own_s, th_1, th_2, th_3, f_1, f_2,
                                                       f_3,f_4, i_t, lives,
                                                       hidden_tar, act, cp)
            _, target_q_val = self.select_action(legal_moves, target_q_s,  train_mode)
            target_q_val = Variable(torch.tensor(target_q_val), requires_grad=True)

        else:
            hidden_tar_t = torch.zeros(2, 1, 128)

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

        return loss

    def end_episode(self, transitions, steps, update_period):

        self.optimizer.zero_grad()
        loss = self.get_loss(transitions)

        loss.backward()
        clip_grad_norm_(parameters=self.policy_net.get_params(), max_norm=10)
        self.optimizer.step()

        if steps % update_period == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        return loss
