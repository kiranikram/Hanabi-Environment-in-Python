import gym
from gym import spaces
import random
import torch
import game_evolution
import game_dynamics


class HanabiEnv(gym.Env):

    def __init__(self):
        # print('Env initialized')
        self.full_deck = {"R11": 0, "G11": 1, "B11": 2, "R12": 3, "G12": 4, "B12": 5, "R13": 6, "G13": 7, "B13": 8,
                          "R21": 9, "G21": 10, "B21": 11, "R22": 12, "G22": 13, "B22": 14, "R31": 15, "G31": 16,
                          "B31": 17}
        self.players = {"Player_One": 98, "Player_Two": 99}
        self.information_tokens = 6
        self.lives = 3
        self.discard_pile = 0
        self.hand_player_one = None
        self.hand_player_two = None

        self.player_one_own_perspective_colours = {"XC1": 23, "XC2": 24, "XC3": 25}
        self.player_one_own_perspective_suits = {"SX1": 26, "SX2": 27, "SX3": 28}
        self.player_two_own_perspective_colours = {"YC1": 29, "YC2": 30, "YC3": 31}
        self.player_two_own_perspective_suits = {"SY1": 32, "SY2": 33, "SY3": 34}

        self.current_player = None
        self.initial_fireworks = {"F1": 35, "F2": 36, "F3": 37}
        self.trailing_obs = []

        """Observation space will consist of:
        -Number of cards in deck
        -Number of players
        -For Player1: color and idx of each card in hand ; #hand size:3
        -For Player2: color and idx of each card in hand ; #hand size:3
        -Color and idx of each card in Fireworks ; #3 colors and thus 3 piles
        -Information tokens available; 6
        -Life Tokens; 4"""

    """ The step function also changes from the current player to the offset player"""

    def step(self, action):
        # print('Step success!')
        # action = self.get_action_id()

        observations = self.apply_action_to_state(action)
        self.store_observations(observations)

        # observations[5], observations[6], observations[7], observations[8] = self.update_perspectives(observations)

        self.deal_hands_during_game(observations)

        observations[5], observations[6], observations[7], observations[8] = self.update_perspectives(observations)

        reward = game_evolution.get_reward(observations)

        done = game_evolution.is_terminal(observations, reward)

        info = {}
        return observations, reward, done, info

    def reset(self):
        # print('Env reset!')

        # obs will need to go into parse observations in run experiment
        # what is the shape type of the obs -- just need to match the type
        hand_p1, hand_p2, _, deck = self.deal_initial_hands()
        opening_obs_tensor = self.concat_opening_tensors()
        current_player = self.get_starting_player()
        p1_opc = self.player_one_own_perspective_colours
        p1_ops = self.player_one_own_perspective_suits
        p2_opc = self.player_two_own_perspective_colours
        p2_ops = self.player_two_own_perspective_suits
        fireworks = self.initial_fireworks

        observations = [hand_p1, hand_p2, deck, opening_obs_tensor, current_player,
                        p1_opc, p1_ops, p2_opc, p2_ops, fireworks]

        self.store_observations(observations)

        return observations

    def deal_initial_hands(self):
        hand_player_one = dict(random.sample(self.full_deck.items(), 3))

        deck = {k: v for k, v in self.full_deck.items() if k not in hand_player_one}

        hand_player_two = dict(random.sample(deck.items(), 3))

        deck = {k: v for k, v in deck.items() if k not in hand_player_two}

        deck_size = len(deck)

        return hand_player_one, hand_player_two, deck_size, deck

    def concat_opening_tensors(self):
        _, _, deck_size, _ = self.deal_initial_hands()
        information_tokens = self.information_tokens
        lives = self.lives
        discard_pile = self.discard_pile

        opening_list = []
        opening_list.extend((deck_size, information_tokens, lives, discard_pile))
        opening_tensor = opening_list

        return opening_tensor

    def get_starting_player(self):
        current_player = dict(random.sample(self.players.items(), 1))

        return current_player

    def store_observations(self, trailing_obs):
        self.trailing_obs.append(trailing_obs)
        return trailing_obs

    def apply_action_to_state(self, action):
        records = self.trailing_obs

        updated_observations = game_evolution.apply_action(records, action)

        self.trailing_obs = []

        return updated_observations

    @staticmethod
    def deal_hands_during_game(observations):

        current_player = observations[4]

        deck = observations[2]
        if len(deck) > 0:
            rand_card = dict(random.sample(deck.items(), 1))
            for key in current_player:
                if key == "Player_One":

                    if len(observations[0]) < 3:
                        observations[0].update(rand_card)
                        for key in rand_card:
                            deck.pop(key)


                elif key == "Player_Two":

                    if len(observations[1]) < 3:
                        observations[1].update(rand_card)
                        for key in rand_card:
                            deck.pop(key)

        # if card = XX:
        # game_dynamics.actions_unavailable.pop(card)

    @staticmethod
    def update_perspectives(observations):
        # print('OBS GOING IN', observations)
        # print('PRE UPD',observations[5], observations[6], observations[7], observations[8] )

        if len(observations[5]) < 3:
            player = 1
            observations[5] = game_evolution.check_and_deal_col(observations[5], player)
        if len(observations[6]) < 3:
            player = 1
            observations[6] = game_evolution.check_and_deal_suit(observations[6], player)
        if len(observations[7]) < 3:
            player = 2
            observations[7] = game_evolution.check_and_deal_col(observations[7], player)
        if len(observations[8]) < 3:
            player = 2
            observations[8] = game_evolution.check_and_deal_suit(observations[8], player)

        # print('POST UPD', observations[5], observations[6], observations[7], observations[8])

        return observations[5], observations[6], observations[7], observations[8]
