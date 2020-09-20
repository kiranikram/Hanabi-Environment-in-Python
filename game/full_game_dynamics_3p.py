"""Based on the current observation, these are the actions that can be taken """

type_of_actions = {"Hint Red": 1, "Hint Blue": 2, "Hint Green": 3, "Hint White": 13,
                   "Hint Suit One": 4, "Hint Suit Two": 5,
                   "Hint Suit Three": 6, "Hint Suit Four": 14,
                   "Play Card Position1": 7, "Discard CardPosition1": 8,
                   "Play Card Position2": 9, "Discard CardPosition2": 10,
                   "Play Card Position3": 11, "Discard CardPosition3": 12}

# if hint card, information token gets used up


play_list = [7, 9, 11]
discard_list = [8, 10, 12]

all_hint_actions = ['1991', '1992', '1993', '3991', '3992', '3993', '2991', '2992', '2993',
                    '1981', '1982', '1983', '3981', '3982', '3983', '2981', '2982', '2983',
                    '4991', '4992', '4993', '5991', '5992', '5993', '6991', '6992', '6993', '4981', '4982',
                    '4983', '5981', '5982', '5983', '6981', '6982', '6983', '7981', '9982', '11983', '7991', '9992',
                    '11993', '8981', '10982', '12983', '8991', '10992', '12993', '13991', '13992', '13993',
                    '13981','13982', '13983', '14991', '14992', '14993', '14981', '14982', '14983','1971', '1972',
                    '1973', '3971','3972', '3973', '2971', '2972', '2973','4971', '4972','4973', '5971', '5972',
                    '5973', '6971', '6972','6973','7971', '9972','11973','8971', '10972', '12973', '13971', '13972',
                    '13973','14971', '14972', '14973']




# iterate through positions in hand
def define_legal_own_actions(own_hand, current_player):
    legal_own_actions = []
    positions = [1, 2, 3]
    for key, i, p in zip(own_hand.keys(), play_list, positions):
        if key is not "XX":
            tmp_action = str(i) + str(current_player) + str(p)
            tmp_action = int(tmp_action)
            legal_own_actions.append(tmp_action)

    for key, k, p in zip(own_hand.keys(), discard_list, positions):
        if key is not "XX":
            tmp_action = str(k) + str(current_player) + str(p)
            tmp_action = int(tmp_action)
            legal_own_actions.append(tmp_action)

    return legal_own_actions


def define_legal_hint_actions(teammate_hand, obs_tensor, opposing_player):
    legal_hint_actions = []
    if obs_tensor[1] > 0:
        positions = [1, 2, 3]
        for key, p in zip(teammate_hand.keys(), positions):
            if key is not "XX":
                card = key

                col_hint_int = str(colour_hint(card))

                col_hint_int = int(col_hint_int + str(opposing_player) + str(p))
                legal_hint_actions.append(col_hint_int)

        for key, p in zip(teammate_hand.keys(), positions):
            if key is not "XX":
                card = key
                suit_hint_int = str(suit_hint(card))

                suit_hint_int = int(suit_hint_int + str(opposing_player) + str(p))
                legal_hint_actions.append(suit_hint_int)

    return legal_hint_actions


def colour_hint(card):
    if card[0] == "R":
        return 1

    elif card[0] == "B":
        return 2

    elif card[0] == "G":
        return 3

    elif card[0] == "W":
        return 13


def suit_hint(card):
    if card[1] == "1":
        return 4
    elif card[1] == "2":
        return 5
    elif card[1] == "3":
        return 6
    elif card[1] == "4":
        return 14


def filter_legal_actions(player_legal_actions, actions_unavailable, obs_tensor):
    for act in player_legal_actions:

        if str(act) in actions_unavailable:
            player_legal_actions.remove(act)

    player_legal_actions = remove_hint_actions(obs_tensor, player_legal_actions)

    return player_legal_actions


def add_actions_back(evolved, step):
    cards_dealt = []
    allowed_actions = []
    full_deck = ['R11', 'G11', 'B11', 'W11', 'R12', 'G12', 'B12', 'W12', 'R13', 'G13', 'B13', 'W13', 'R21', 'G21',
                 'B21', 'W21',
                 'R22', 'G22', 'B22', 'W22', 'R31', 'G31', 'B31', 'W31', 'R32', 'G32', 'B32', 'W32', 'R41', 'G41',
                 'B41', 'W41']
    ongoing_deck = list(evolved.keys())

    for i in full_deck:
        if i not in ongoing_deck:
            cards_dealt.append(i)

    for card in cards_dealt:
        actions_list = add_hints_back(card)
        for i in actions_list:
            allowed_actions.append(i)

    for card in cards_dealt:
        suit_actions_list = add_suit_hints_back(card)
        for i in suit_actions_list:
            allowed_actions.append(i)

    return allowed_actions


def make_reavailable(filter_list, allowed_actions):
    for i in allowed_actions:
        if i in filter_list:
            filter_list.remove(i)

    return filter_list


def add_hints_back(card):
    reds = ['R11', 'R12', 'R13', 'R21', 'R22', 'R31', 'R32', 'R41']
    blues = ['B11', 'B12', 'B13', 'B21', 'B22', 'B31', 'B32', 'B41']
    greens = ['G11', 'G12', 'G13', 'G21', 'G22', 'G31', 'G32', 'G41']
    whites = ['W11', 'W12', 'W13', 'W21', 'W22', 'W31', 'W32', 'W41']
    if card in reds:
        actions = ['1991', '1992', '1993', '1981', '1982', '1983','1971', '1972', '1973']
        return actions
    if card in blues:
        actions = ['2991', '2992', '2993', '2981', '2982', '2983','2971', '2972', '2973']
        return actions
    if card in greens:
        actions = ['3991', '3992', '3993', '3981', '3982', '3983','3971', '3972', '3973']
        return actions
    if card in whites:
        actions = ['13991', '13992', '13993', '13981', '13982', '13983','13971', '13972', '13973',]
        return actions


def add_suit_hints_back(card):
    ones = ['R11', 'R12', 'R13', 'B11', 'B12', 'B13', 'G11', 'G12', 'G13', 'W11', 'W12', 'W13']
    twos = ['R21', 'R22', 'B21', 'B22', 'G21', 'G22', 'W21', 'W22']
    threes = ['R31', 'R32', 'B31', 'B32', 'G31', 'G32', 'W31', 'W32']
    fours = ['R41', 'B41', 'G41', 'W41']
    if card in ones:
        actions = ['4991', '4992', '4993', '4981', '4982', '4983','4971', '4972', '4973']
        return actions
    if card in twos:
        actions = ['5991', '5992', '5993', '5981', '5982', '5983','5971', '5972', '5973']
        return actions
    if card in threes:
        actions = ['6991', '6992', '6993', '6981', '6982', '6983','6971', '6972', '6973']
        return actions
    if card in fours:
        actions = ['14991', '14992', '14993', '14981', '14982', '14983','14971', '14972', '14973']
        return actions


def transform_inputs(obs_dict, obs_tensor, prev_action, current_player):

    obs_dict_list = list(obs_dict.values())

    oc_1 = [obs_dict_list[0]]
    oc_2 = [obs_dict_list[1]]
    oc_3 = [obs_dict_list[2]]
    os_1 = [obs_dict_list[3]]
    os_2 = [obs_dict_list[4]]
    os_3 = [obs_dict_list[5]]
    th_1 = [obs_dict_list[6]]
    th_2 = [obs_dict_list[7]]
    th_3 = [obs_dict_list[8]]
    f_1 = [obs_dict_list[9]]
    if len(obs_dict_list) == 11:
        f_2 = [obs_dict_list[10]]
        if len(obs_dict_list) == 12:
            f_3 = [obs_dict_list[11]]
        else:
            f_3 = [0]
    else:
        f_2 = [0]
        f_3 = [0]

    i_t = [obs_tensor[1]]
    for i in range(len(i_t)):
        if i_t[i] < 0:
            i_t[i] = 0

    lives = [obs_tensor[2]]

    if prev_action == 0:
        act = [0]
    else:
        prev_action_vals = all_hint_actions.index(str(prev_action))
        act = [prev_action_vals]

    for key in current_player:
        if key == "Player_One":
            player = 0
        else:
            player = 1

    cp = [player]

    return oc_1, oc_2, oc_3, os_1, os_2, os_3, th_1, th_2, th_3, f_1, f_2, f_3, i_t, lives, act, cp


def remove_hint_actions(obs_tensor, legal_actions):
    hint_actions_list = [1991, 1992, 1993, 3991, 3992, 3993, 2991, 2992, 2993, 1981,
                         1982, 1983, 3981, 3982, 3983, 2981, 2982, 2983, 4991, 4992,
                         4993, 5991, 5992, 5993, 6991, 6992, 6993, 4981, 4982, 4983,
                         5981, 5982, 5983, 6981, 6982, 6983,1971, 1972, 1973, 3971, 3972,
                         3973, 2971, 2972, 2973,4971, 4972,
                         4973, 5971, 5972, 5973, 6971, 6972, 6973]
    if obs_tensor[1] <= 0:

        for act in legal_actions:
            if act in hint_actions_list:
                legal_actions.pop(act)

    return legal_actions
