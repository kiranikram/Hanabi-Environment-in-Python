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
        self.oc_1_lookup = nn.Embedding(60, 128)
        self.oc_2_lookup = nn.Embedding(60, 128)
        self.oc_3_lookup = nn.Embedding(60, 128)
        self.os_1_lookup = nn.Embedding(60, 128)
        self.os_2_lookup = nn.Embedding(60, 128)
        self.os_3_lookup = nn.Embedding(60, 128)
        self.f_1_lookup = nn.Embedding(48, 128)
        self.f_2_lookup = nn.Embedding(48, 128)
        self.f_3_lookup = nn.Embedding(48, 128)

        # self.state_tensor_lookup = nn.Embedding(48, 128)
        self.i_t_lookup = nn.Embedding(24, 128)
        self.lives_lookup = nn.Embedding(10, 128)

        self.prev_action_lookup = nn.Embedding(48, 128)

        # RNN to approximate the agent’s action-observation history.
        self.rnn = nn.GRU(input_size=128, hidden_size=128, num_layers=2)

        # 2 layer MLP with batch normalization, for producing output from RNN top layer.
        self.output = nn.Sequential(
            nn.Linear(128, 128),
            # nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 48)
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

        self.oc_1_lookup.reset.parameters()
        self.oc_2_lookup.reset_parameters()
        self.oc_3_lookup.reset_parameters()
        self.os_1_lookup.reset.parameters()
        self.os_2_lookup.reset_parameters()
        self.os_3_lookup.reset_parameters()
        self.f_1_lookup.reset.parameters()
        self.f_2_lookup.reset_parameters()
        self.f_3_lookup.reset_parameters()

        self.i_t_lookup.reset_parameters()
        self.lives_lookup.reset_parameters()

        self.prev_action_lookup.reset_parameters()
        # self.message.apply(weight_reset)
        self.output.apply(weight_reset)
        for p in self.rnn.parameters():
            p.data.uniform_(*self.init_param_range)

    def forward(self, oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, i_t, lives, hidden, prev_action, agent):
        """
        Returns the q-values and hidden state for the given step parameters
        """

        # state_dict = Variable(torch.LongTensor(state_dict))
        oc_1 = Variable(torch.LongTensor(oc_1))
        oc_2 = Variable(torch.LongTensor(oc_2))
        oc_3 = Variable(torch.LongTensor(oc_3))
        os_1 = Variable(torch.LongTensor(os_1))
        os_2 = Variable(torch.LongTensor(os_2))
        os_3 = Variable(torch.LongTensor(os_3))
        f_1 = Variable(torch.LongTensor(f_1))
        f_2 = Variable(torch.LongTensor(f_2))
        f_3 = Variable(torch.LongTensor(f_3))

        i_t = Variable(torch.LongTensor(i_t))
        lives = Variable(torch.LongTensor(lives))
        hidden = Variable(torch.FloatTensor(hidden))
        prev_action = Variable(torch.LongTensor(prev_action))
        agent = Variable(torch.LongTensor(agent))

        """Produce embeddings for rnn from input parameters"""
        z_a = self.action_lookup(agent)

        # z_o_d = self.state_dict_lookup(state_dict)

        z_oc_1 = self.oc_1_lookup(oc_1)
        z_oc_2 = self.oc_2_lookup(oc_2)
        z_oc_3 = self.oc_3_lookup(oc_3)
        z_os_1 = self.oc_1_lookup(os_1)
        z_os_2 = self.oc_2_lookup(os_2)
        z_os_3 = self.oc_3_lookup(os_3)
        z_f_1 = self.f_1_lookup(f_1)
        z_f_2 = self.f_2_lookup(f_2)
        z_f_3 = self.f_3_lookup(f_3)
        z_i_t = self.i_t_lookup(i_t)
        z_lives = self.lives_lookup(lives)
        z_u = self.prev_action_lookup(prev_action)
        # z_m = self.message(messages.view(-1, self.comm_size))

        # Add the input embeddings to calculate final RNN input.

        z_o_d = z_oc_1 + z_oc_2 + z_oc_3 + z_os_1 + z_os_2 + z_os_3 + z_f_1 + z_f_2 + z_f_3
        z_o_t = z_i_t + z_lives
        z = z_a + z_o_d + z_o_t + z_u

        z = z.unsqueeze(1)

        rnn_out, h = self.rnn(z, hidden)

        # Produce final CNet output q-values from GRU output.
        out = self.output(rnn_out[:, -1, :].squeeze())


        return h, out
