"""This is where we run the experiment"""

import gym
import torch
import envs
import base_agent
import letstest
import game_dynamics
import itertools
import game_evolution

env = gym.make("HanabiEnv-v0")
agent = base_agent.DIALAgent
game = game_dynamics.DefineLegalActions


def initialize_records():
    hidden = torch.zeros(2, 128)
    hidden_tar = torch.zeros(2, 128)

    return hidden, hidden_tar






def store_records_during():
    _, hidden_t, hidden_tar = agent.step()
    return hidden_t, hidden_tar


def parse_observations(observations, total_moves):
    unique_player_obs_set = {}
    legal_own_actions = []
    legal_hint_actions = []
    full_obs_tensor = observations[3]

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

    player_legal_actions = legal_hint_actions + legal_own_actions
    unique_player_obs_set.update(observations[9])
    legal_action_arr = available_legal_moves(player_legal_actions)

    return current_player, unique_player_obs_set, full_obs_tensor, legal_action_arr


# These are given to agent obs for action selection

def available_legal_moves(legal_actions):
    legal_moves = []
    all_moves = game_evolution.all_legal_actions.values()
    for k in all_moves:
        if k in legal_actions:
            legal_moves.append(0.0)
        else:
            legal_moves.append(-float('inf'))

    return legal_moves


def run_one_episode(agent, env, min_steps):
    observations = env.reset()
    agent.store_observations()

    current_player, legal_moves, observation_vector, observation_tensor = parse_observations(observations)
    hidden, hidden_tar = initialize_records()

    action,hidden_opn,hidden_tar_opn = agent.begin_episode(current_player, legal_moves, observation_vector, observation_tensor, hidden,
                                 hidden_tar)

    is_done = False

    total_reward = 0
    step_number = 0

    while not is_done:

        observations, reward, is_done, _ = env.step(action)
        agent.store_observations(observations)

        total_reward += reward
        step_number += 1
        if is_done:
            break

        if step_number == 0:

            hidden = hidden_opn , hidden_tar = hidden_tar_opn
        else:
            hidden, hidden_tar = agent.hidden_states()

        current_player, legal_moves, observation_vector, observation_tensor = parse_observations(observations)

        action, hidden_tr , tar_hidden_tr = agent.step(reward, current_player, legal_moves, observation_vector, observation_tensor, hidden,
                                  hidden_tar)
        agent.hidden_states(hidden_tr,tar_hidden_tr)

    agent.end_episode(min_steps)
    return step_number, total_reward


def run_one_phase(agent, env, min_steps):
    step_count = 0
    num_episodes = 0
    sum_returns = 0

    while step_count < min_steps:
        episode_length, episode_return = run_one_episode(agent, env)
        if step_count % 100 == 0:
            print('Episode length', episode_length)
            print('Episode returns', episode_return)

        step_count += episode_length
        sum_returns += episode_return
        num_episodes += 1

    return step_count , sum_returns , num_episodes


