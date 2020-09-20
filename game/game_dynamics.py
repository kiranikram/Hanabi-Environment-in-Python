"""Based on the current observation, these are the actions that can be taken """

type_of_actions = {"Hint Red": 1, "Hint Blue": 2, "Hint Green": 3,
                   "Hint Suit One": 4, "Hint Suit Two": 5, "Hint Suit Three": 6,
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
                    '11993', '8981', '10982', '12983', '8991', '10992', '12993', ]


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
    print('teammate hand', teammate_hand)
    print('opposing', opposing_player)
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


def suit_hint(card):
    if card[1] == "1":
        return 4
    elif card[1] == "2":
        return 5
    elif card[1] == "3":
        return 6


def filter_legal_actions(player_legal_actions, actions_unavailable, obs_tensor):
    for act in player_legal_actions:

        if str(act) in actions_unavailable:
            player_legal_actions.remove(act)

    player_legal_actions = remove_hint_actions(obs_tensor, player_legal_actions)

    return player_legal_actions


def transform_inputs(obs_dict, obs_tensor, prev_action, current_player):
    obs_dict_list = list(obs_dict.values())

    oc_1 = [obs_dict_list[0]]
    oc_2 = [obs_dict_list[1]]
    oc_3 = [obs_dict_list[2]]
    os_1 = [obs_dict_list[3]]
    os_2 = [obs_dict_list[4]]
    os_3 = [obs_dict_list[5]]
    f_1 = [obs_dict_list[6]]
    f_2 = [obs_dict_list[7]]
    if len(obs_dict_list) == 9:
        f_3 = [obs_dict_list[8]]

    else:
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

    return oc_1, oc_2, oc_3, os_1, os_2, os_3, f_1, f_2, f_3, i_t, lives, act, cp


def remove_hint_actions(obs_tensor, legal_actions):
    hint_actions_list = [1991, 1992, 1993, 3991, 3992, 3993, 2991, 2992, 2993, 1981,
                         1982, 1983, 3981, 3982, 3983, 2981, 2982, 2983, 4991, 4992,
                         4993, 5991, 5992, 5993, 6991, 6992, 6993, 4981, 4982, 4983,
                         5981, 5982, 5983, 6981, 6982, 6983]
    if obs_tensor[1] <= 0:

        for act in legal_actions:
            if act in hint_actions_list:
                legal_actions.pop(act)

    return legal_actions
