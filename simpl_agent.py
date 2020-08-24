import gym
import envs
import game_evolution
import game_dynamics
import random
import collections

env = gym.make("HanabiEnv-v0")
game = game_dynamics


# env.step()


class SimpleAgent(object):

    def __init__(self):
        self.players = 2
        self.transitions = [[] for _ in range(self.players)]
        self.all_observations = []

    @staticmethod
    def select_action(legal_moves):
        available_action_list = legal_moves

        curr_action = random.choice(available_action_list)
        return curr_action


agent = SimpleAgent


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


def run_game():
    actions_unavailable = []
    initial_observations = env.reset()
    ini_current_player, _, obs_tensor, player_legal_actions = parse_observations(initial_observations)
    print('Information Tokens:', obs_tensor[1])
    print("Lives:", obs_tensor[2])
    print()

    action = agent.select_action(player_legal_actions)
    for key in ini_current_player:
        print("***", key, "took action", action, "***")

    actions_unavailable.append(action)

    is_done = False

    total_reward = 0
    step_number = 0

    while not is_done:

        observations, reward, is_done, _ = env.step(action)
        # when we run multiple episodes we can ammend tp "+= reward"
        total_reward = reward
        step_number += 1

        if is_done:
            break
        current_player, obs_dict, game_obs_tensor, player_legal_actions = parse_observations(observations)
        print('OBS DICT', obs_dict)
        print(current_player)
        print('OBS Tensor', game_obs_tensor)
        print('Information Tokens:', game_obs_tensor[1])
        print("Lives:", game_obs_tensor[2])
        print()

        player_legal_actions = game_dynamics.filter_legal_actions(player_legal_actions, actions_unavailable)
        action = agent.select_action(player_legal_actions)

        actions_unavailable.append(action)
        for key in current_player:
            print("***", key, "took action", action, "***")

        print("Game steps completed:", step_number, 'Reward:', total_reward)


run_game()

