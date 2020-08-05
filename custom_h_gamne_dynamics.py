"""Based on the current observation, these are the actions that can be taken """

type_of_actions = {"Hint Red": 1, "Hint Blue": 2, "Hint Green": 3,
                   "Hint Suit One": 4, "Hint Suit Two": 5, "Hint Suit Three": 6,
                   "Play Card Position1": 7, "Discard CardPosition1": 8,
                   "Play Card Position2": 9, "Discard CardPosition2": 10,
                   "Play Card Position3": 11, "Discard CardPosition3": 12}


# if hint card, information token gets used up
class DefineLegalActions(object):

    def __init__(self):

        self.legal_hint_actions = []
        self.legal_own_actions = []
        self.play_list = [7, 9, 11]
        self.discard_list = [8, 10, 12]

    # iterate through positions in hand
    def define_legal_own_actions(self, own_hand, current_player):

        positions = [1, 2, 3]
        for key, i, p in zip(own_hand.keys(), self.play_list, positions):
            if key is not "XX":
                tmp_action = str(i) + str(current_player) + str(p)
                tmp_action = int(tmp_action)
                self.legal_own_actions.append(tmp_action)

        for key, k, p in zip(own_hand.keys(), self.discard_list, positions):
            if key is not "XX":
                tmp_action = str(k) + str(current_player) + str(p)
                tmp_action = int(tmp_action)
                self.legal_own_actions.append(tmp_action)

        return self.legal_own_actions

    def define_legal_hint_actions(self, teammate_hand, obs_tensor, opposing_player):
        if obs_tensor[1] is not 0:

            positions = [1, 2, 3]
            for key, p in zip(teammate_hand.keys(), positions):
                if key is not "XX":
                    card = key
                    hint_int = str(self.colour_hint(card))
                    hint_int = int(hint_int + str(opposing_player) + str(p))
                    self.legal_hint_actions.append(hint_int)

            for key, p in zip(teammate_hand.keys(), positions):
                if key is not "XX":
                    card = key
                    hint_int = str(self.suit_hint(card))
                    hint_int = int(hint_int + str(opposing_player) + str(p))
                    self.legal_hint_actions.append(hint_int)

    def colour_hint(self, card):

        if card[0] == "R":
            return 1

        elif card[0] == "B":
            return 2

        elif card[0] == "G":
            return 3

    def suit_hint(self,card):

        if card[1] == "1":
            return 4

        elif card[1] == "2":
            return 5

        elif card[1] == "3":
            return 6





