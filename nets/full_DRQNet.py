import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import copy

import torch.optim as optim

from torch.nn.utils import clip_grad_norm_


def weight_reset(m):
    if isinstance(m, nn.BatchNorm1d) or isinstance(m, nn.Linear):
        m.reset_parameters()


class CNet(nn.Module):
    def __init__(self):
        """
        Initializes the CNet model
        """
        super(CNet, self).__init__()

        self.init_param_range = (-0.08, 0.08)

        ## Lookup tables for the state, action and previous action.
        self.action_lookup = nn.Embedding(3, 128)

        # self.state_dict_lookup = nn.Embedding(48, 128)
        self.own_c_lookup = nn.Embedding(129, 128)
        self.own_s_lookup = nn.Embedding(129, 128)

        self.th_1_lookup = nn.Embedding(115,128)
        self.th_2_lookup = nn.Embedding(115, 128)
        self.th_3_lookup = nn.Embedding(115, 128)

        self.f_1_lookup = nn.Embedding(96, 128)
        self.f_2_lookup = nn.Embedding(96, 128)
        self.f_3_lookup = nn.Embedding(96, 128)
        self.f_4_lookup = nn.Embedding(96, 128)

        # self.state_tensor_lookup = nn.Embedding(48, 128)
        self.i_t_lookup = nn.Embedding(24, 128)
        self.lives_lookup = nn.Embedding(10, 128)

        self.prev_action_lookup = nn.Embedding(91, 128)

        # RNN to approximate the agent’s action-observation history.
        self.rnn = nn.GRU(input_size=128, hidden_size=128, num_layers=2)

        # 2 layer MLP with batch normalization, for producing output from RNN top layer.
        self.output = nn.Sequential(
            nn.Linear(128, 128),
            # nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 90)
        )

    def get_params(self):
        return list(self.parameters())

    def reset_parameters(self):
        """
        Reset all model parameters
        """
        self.rnn.reset_parameters()
        self.action_lookup.reset_parameters()

        # self.state_dict_lookup.reset_parameters()

        self.own_c_lookup.reset.parameters()
        self.own_s_lookup.reset_parameters()

        self.th_1_lookup.reset_parameters()
        self.th_2_lookup.reset_parameters()
        self.th_3_lookup.reset_parameters()
        self.f_1_lookup.reset.parameters()
        self.f_2_lookup.reset_parameters()
        self.f_3_lookup.reset_parameters()
        self.f_4_lookup.reset_parameters()

        self.i_t_lookup.reset_parameters()
        self.lives_lookup.reset_parameters()

        self.prev_action_lookup.reset_parameters()
        # self.message.apply(weight_reset)
        self.output.apply(weight_reset)
        for p in self.rnn.parameters():
            p.data.uniform_(*self.init_param_range)

    def forward(self, own_c, own_s,th_1,th_2,th_3, f_1, f_2, f_3,f_4, i_t, lives, hidden, prev_action, agent):
        """
        Returns the q-values and hidden state for the given step parameters
        """

        # state_dict = Variable(torch.LongTensor(state_dict))
        own_c = Variable(torch.LongTensor(own_c))
        own_s = Variable(torch.LongTensor(own_s))

        th_1 = Variable(torch.LongTensor(th_1))
        th_2 = Variable(torch.LongTensor(th_2))
        th_3 = Variable(torch.LongTensor(th_3))

        f_1 = Variable(torch.LongTensor(f_1))
        f_2 = Variable(torch.LongTensor(f_2))
        f_3 = Variable(torch.LongTensor(f_3))
        f_4 = Variable(torch.LongTensor(f_4))

        i_t = Variable(torch.LongTensor(i_t))
        lives = Variable(torch.LongTensor(lives))
        hidden = Variable(torch.FloatTensor(hidden))
        prev_action = Variable(torch.LongTensor(prev_action))
        agent = Variable(torch.LongTensor(agent))

        """Produce embeddings for rnn from input parameters"""
        z_a = self.action_lookup(agent)

        # z_o_d = self.state_dict_lookup(state_dict)

        z_own_c = self.own_c_lookup(own_c)
        z_own_s = self.own_s_lookup(own_s)

        z_th_1 = self.th_1_lookup(th_1)
        z_th_2 = self.th_2_lookup(th_2)
        z_th_3 = self.th_3_lookup(th_3)
        z_f_1 = self.f_1_lookup(f_1)
        z_f_2 = self.f_2_lookup(f_2)
        z_f_3 = self.f_3_lookup(f_3)
        z_f_4 = self.f_4_lookup(f_4)
        z_i_t = self.i_t_lookup(i_t)
        z_lives = self.lives_lookup(lives)
        z_u = self.prev_action_lookup(prev_action)
        # z_m = self.message(messages.view(-1, self.comm_size))

        # Add the input embeddings to calculate final RNN input.

        z_o_d = z_own_c + z_own_s + z_th_1 + z_th_2 + z_th_3 + z_f_1 + z_f_2 + z_f_3 + z_f_4
        z_o_t = z_i_t + z_lives
        z = z_a + z_o_d + z_o_t + z_u

        z = z.unsqueeze(1)

        rnn_out, h = self.rnn(z, hidden)

        # Produce final CNet output q-values from GRU output.
        out = self.output(rnn_out[:, -1, :].squeeze())


        return h, out
