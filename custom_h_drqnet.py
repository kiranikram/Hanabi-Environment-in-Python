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
        self.action_lookup = nn.Embedding(100, 128)
        self.state_dict_lookup = nn.Embedding(100, 128)
        self.state_tensor_lookup = nn.Embedding(48, 128)
        # self.prev_action_lookup = nn.Embedding(opts['game_action_space_total'], opts['rnn_size'])

        # RNN to approximate the agent’s action-observation history.
        self.rnn = nn.GRU(input_size=128, hidden_size=128, num_layers=2)

        # 2 layer MLP with batch normalization, for producing output from RNN top layer.
        self.output = nn.Sequential(
            nn.Linear(128, 128),
            nn.BatchNorm1d(128),
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
        self.state_dict_lookup.reset_parameters()
        self.state_tensor_lookup.reset_parameters()
        #self.prev_action_lookup.reset_parameters()
        #self.message.apply(weight_reset)
        self.output.apply(weight_reset)
        for p in self.rnn.parameters():
            p.data.uniform_(*self.init_param_range)

    def forward(self, state_dict,state_tensor, hidden, agent):
        """
        Returns the q-values and hidden state for the given step parameters
        """

        state_dict = Variable(torch.LongTensor(state_dict))
        state_tensor = Variable(torch.LongTensor(state_dict))
        hidden = Variable(torch.FloatTensor(hidden))
        prev_action = Variable(torch.LongTensor(prev_action))
        agent = Variable(torch.LongTensor(agent))

        # Produce embeddings for rnn from input parameters
        z_a = self.action_lookup(agent)
        z_o_d = self.state_dict_lookup(state_dict)
        z_o_t = self.state_tensor_lookup(state_tensor)
        z_u = self.prev_action_lookup(prev_action)
        #z_m = self.message(messages.view(-1, self.comm_size))

        # Add the input embeddings to calculate final RNN input.
        z = z_a + z_o_d + z_o_t + z_m
        z = z.unsqueeze(1)

        rnn_out, h = self.rnn(z, hidden)
        # Produce final CNet output q-values from GRU output.
        out = self.output(rnn_out[:, -1, :].squeeze())

        return h, out
