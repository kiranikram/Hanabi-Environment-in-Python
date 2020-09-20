import gym
import random
from game import full_game_dynamics, full_game_evolution, full_game_evolution_3p, full_game_dynamics_3p, \
    BU_game_dynamics, BU_game_evolution, fullBU_game_dynamics_3p

evolution = full_game_evolution
game = full_game_dynamics

"""Instructions:
Running 
Need to decide between: full_deck and small_deck
                         players and three_players
                         deal_initial_hands and deal_initial_hands_3p
                         Need to amend reset
                         deal_hands vs deal_hands_3p
                         update_perspectives vs update_perspectives_3p"""


class HanabiEnv(gym.Env):

    def __init__(self):
        # print('Env initialized')
        self.unuse_full_deck = {"R11": 0, "G11": 1, "B11": 2, "W11": 3, "R12": 4, "G12": 5, "B12": 6, "W12": 7,
                          "R13": 8,
                          "G13": 9, "B13": 10, "W13": 11, "R21": 12, "G21": 13, "B21": 14, "W21": 15, "R22": 16,
                          "G22": 17,
                          "B22": 18, "W22": 19, "R31": 20, "G31": 21, "B31": 22, "W31": 23, "R32": 24, "G32": 25,
                          "B32": 26, "W32": 27, "R41": 28, "G41": 29, "B41": 30, "W41": 31}

        self.full_deck = {"R11": 0, "G11": 1, "B11": 2, "R12": 4, "G12": 5, "B12": 6, "R13": 8,
                           "G13": 9, "B13": 10, "R21": 12, "G21": 13, "B21": 14, "R22": 16, "G22": 17,
                           "B22": 18, "R31": 20, "G31": 21, "B31": 22}

        self.players = {"Player_One": 98, "Player_Two": 99}
        self.unuse_players = {"Player_One": 98, "Player_Two": 99, "Player_Three": 97}
        self.information_tokens = 12
        self.lives = 6
        self.discard_pile = 0
        self.hand_player_one = None
        self.hand_player_two = None
        self.hand_player_three = None

        self.player_one_own_perspective_colours = {"XC1": 1, "XC2": 2, "XC3": 3}
        self.player_one_own_perspective_suits = {"SX1": 4, "SX2": 5, "SX3": 6}
        self.player_two_own_perspective_colours = {"YC1": 7, "YC2": 8, "YC3": 9}
        self.player_two_own_perspective_suits = {"SY1": 10, "SY2": 11, "SY3": 12}
        self.player_three_own_perspective_colours = {"ZC1": 75, "ZC2": 76, "ZC3": 77}
        self.player_three_own_perspective_suits = {"SZ1": 78, "SZ2": 79, "SZ3": 80}

        self.current_player = None
        self.unuse_initial_fireworks = {"F1": 35, "F2": 36, "F3": 37}
        self.initial_fireworks = {"F1": 35, "F2": 36, "F3": 37, "F4": 38}
        self.trailing_obs = []

        self.bu_msg = {"play_p1": 1, "play_p2": 2, "play_p3": 3, "eval_mode": 0}

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
        print('Step success!')
        # action = self.get_action_id()

        observations = self.apply_action_to_state(action)
        self.store_observations(observations)

        # observations[5], observations[6], observations[7], observations[8] = self.update_perspectives(observations)

        observations = self.deal_hands_during_game(observations)

        #observations[6], observations[7], observations[8], observations[9], \
        #observations[10], observations[11] = self.update_perspectives_3p(observations)

        observations[5], observations[6],observations[7],observations[8] = self.update_perspectives(observations)

        reward = evolution.get_reward(observations)

        done = evolution.is_terminal(observations, reward)

        info = {}
        return observations, reward, done, info

    def reset(self):
        print('Env reset!')

        # obs will need to go into parse observations in run experiment
        # what is the shape type of the obs -- just need to match the type
        hand_p1, hand_p2,  _, deck = self.deal_initial_hands()

        opening_obs_tensor = self.concat_opening_tensors()
        current_player = self.get_starting_player()
        p1_opc = self.player_one_own_perspective_colours
        p1_ops = self.player_one_own_perspective_suits
        p2_opc = self.player_two_own_perspective_colours
        p2_ops = self.player_two_own_perspective_suits
        p3_opc = self.player_three_own_perspective_colours
        p3_ops = self.player_three_own_perspective_suits
        fireworks = self.initial_fireworks

        observations = [hand_p1, hand_p2,  deck, opening_obs_tensor, current_player,
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

    def deal_initial_hands_3p(self):

        hand_player_one = dict(random.sample(self.full_deck.items(), 3))

        deck = {k: v for k, v in self.full_deck.items() if k not in hand_player_one}

        hand_player_two = dict(random.sample(deck.items(), 3))

        deck = {k: v for k, v in deck.items() if k not in hand_player_two}

        hand_player_three = dict(random.sample(deck.items(), 3))

        deck = {k: v for k, v in deck.items() if k not in hand_player_three}

        deck_size = len(deck)

        return hand_player_one, hand_player_two, hand_player_three, deck_size, deck

    def concat_opening_tensors(self):
        _, _, _, deck_size, _ = self.deal_initial_hands_3p()
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

        updated_observations = evolution.apply_action(records, action)

        self.trailing_obs = []

        return updated_observations

    @staticmethod
    def deal_hands_during_game(observations):

        deck = observations[2]
        if len(deck) > 0:
            rand_card = dict(random.sample(deck.items(), 1))

            if len(observations[0]) < 3:

                observations[0].update(rand_card)

                for key in rand_card:
                    deck.pop(key)

            if len(observations[1]) < 3:

                observations[1].update(rand_card)

                for key in rand_card:
                    deck.pop(key)
            if len(observations[2]) < 3:

                observations[2].update(rand_card)

                for key in rand_card:
                    deck.pop(key)

        return observations

        # if card = XX:
        # game_dynamics.actions_unavailable.pop(card)

    @staticmethod
    def deal_hands_during_game_3p(observations):

        deck = observations[3]
        if len(deck) > 0:
            rand_card = dict(random.sample(deck.items(), 1))

            if len(observations[0]) < 3:

                observations[0].update(rand_card)

                for key in rand_card:
                    deck.pop(key)

                    rand_card = dict(random.sample(deck.items(), 1))

            if len(observations[1]) < 3:

                observations[1].update(rand_card)

                for key in rand_card:
                    deck.pop(key)

                    rand_card = dict(random.sample(deck.items(), 1))

            if len(observations[2]) < 3:

                observations[2].update(rand_card)

                for key in rand_card:
                    deck.pop(key)

        return observations

        # if card = XX:
        # game_dynamics.actions_unavailable.pop(card) #nee #need

    # need to check where deck is

    @staticmethod
    def update_perspectives(observations):

        # print('OBS GOING IN', observations)
        # print('PRE UPD',observations[5], observations[6], observations[7], observations[8] )

        if len(observations[5]) < 3:
            player = 1
            observations[5] = evolution.check_and_deal_col(observations[5], player)
        if len(observations[6]) < 3:
            player = 1
            observations[6] = evolution.check_and_deal_suit(observations[6], player)
        if len(observations[7]) < 3:
            player = 2
            observations[7] = evolution.check_and_deal_col(observations[7], player)
        if len(observations[8]) < 3:
            player = 2
            observations[8] = evolution.check_and_deal_suit(observations[8], player)

        # print('POST UPD', observations[5], observations[6], observations[7], observations[8])

        return observations[5], observations[6], observations[7], observations[8]

    @staticmethod
    def update_perspectives_3p(observations):

        # print('OBS GOING IN', observations)
        # print('PRE UPD',observations[5], observations[6], observations[7], observations[8] )

        if len(observations[6]) < 3:
            player = 1
            observations[6] = evolution.check_and_deal_col(observations[6], player)
        if len(observations[7]) < 3:
            player = 1
            observations[7] = evolution.check_and_deal_suit(observations[7], player)
        if len(observations[8]) < 3:
            player = 2
            observations[8] = evolution.check_and_deal_col(observations[8], player)
        if len(observations[9]) < 3:
            player = 2
            observations[9] = evolution.check_and_deal_suit(observations[9], player)
        if len(observations[10]) < 3:
            player = 3
            observations[10] = evolution.check_and_deal_col(observations[10], player)
        if len(observations[11]) < 3:
            player = 3
            observations[11] = evolution.check_and_deal_suit(observations[11], player)

        # print('POST UPD', observations[5], observations[6], observations[7], observations[8])

        return observations[6], observations[7], observations[8], observations[9], observations[10], observations[11]
