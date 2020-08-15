import itertools

all_legal_actions = {"1991": 1, "2991": 2, "3991": 3, "1992": 4, "2992": 5, "3992": 6, "1993": 7,
                     "2993": 8, "3993": 9, "4991": 10, "5991": 11, "6991": 12, "4992": 13, "5992": 14,
                     "6992": 15, "4993": 16, "5993": 17, "6993": 18, "7981": 19, "9982": 20,
                     "11983": 21, "8981": 22, "10982": 23, "12983": 24, "1981": 25, "2981": 26,
                     "3981": 27, "1982": 28, "2982": 29, "3982": 30, "1983": 31, "2983": 32,
                     "3983": 33, "4981": 34, "5981": 35, "6981": 36, "4982": 37, "5982": 38,
                     "6982": 39, "4983": 40, "5983": 41, "6983": 42, "7991": 43, "9992": 44,
                     "11993": 45, "8991": 46, "10992": 47, "12993": 48}

game_moves = len(all_legal_actions)


def apply_action(records, action):
    action = str(action)

    curr_records = records[0]

    hand_p1 = curr_records[0]
    hand_p2 = curr_records[1]

    deck = curr_records[2]
    obs_tensor = curr_records[3]

    current_player = curr_records[4]
    own_colour_p1 = curr_records[5]
    own_suit_p1 = curr_records[6]
    own_colour_p2 = curr_records[7]
    own_suit_p2 = curr_records[8]

    fireworks = curr_records[9]

    for key in current_player:
        if key == "Player_One":
            current_player = {"Player_Two": 99}
        elif key == "Player_Two":
            current_player = {"Player_One": 98}

    # REVEAL COLOURS
    # from player 1 to player to 2, which means that player 2's card knowledge needs to change
    # player 2's cards w/o hints are listed as 'YC'
    ### imp! need to reduce for each, an information token upon giving hints
    if action == "1991":
        tmp_col = {'YR1': 38}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YR1'] = own_colour_p2.pop('YC1')
    if action == "1992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YR2': 39})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YR2'] = own_colour_p2.pop('YC2')
    if action == "1993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YR3': 40})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    if action == "3991":
        tmp_col = {'YG1': 41}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        obs_tensor[1] -= 1

        # own_colour_p2['YG1'] = own_colour_p2.pop('YC1')
    if action == "3992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YG2': 42})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YG2'] = own_colour_p2.pop('YC2')
    if action == "3993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YG3': 43})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    if action == "2991":
        tmp_col = {'YB1': 44}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YB1'] = own_colour_p2.pop('YC1')
    if action == "2992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YB2': 45})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YB2'] = own_colour_p2.pop('YC2')
    if action == "2993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YB3': 46})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    # from player 2 to player 1 , which means that player 1's cards need to change
    # player 1's cards w/o hints are listed as 'XC'
    if action == "1981":
        tmp_col = {'XR1': 47}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XR1'] = own_colour_p1.pop('XC1')
    if action == "1982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XR2': 48})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XR2'] = own_colour_p1.pop('XC2')
    if action == "1983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XR3': 49})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    if action == "3981":
        tmp_col = {'XG1': 50}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XG1'] = own_colour_p1.pop('XC1')
    if action == "3982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XG2': 51})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XG2'] = own_colour_p1.pop('XC2')
    if action == "3983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XG3': 52})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    if action == "2981":
        tmp_col = {'XB1': 53}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XB1'] = own_colour_p1.pop('XC1')
    if action == "2982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XB2': 54})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XB2'] = own_colour_p1.pop('XC2')
    if action == "2983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XB3': 55})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    # REVEAL SUITS
    # from player 1 to player to pl 2 , which means that player 2's card knowledge needs to change
    # player 2's cards w/o hints are listed as 'SY'
    if action == "4991":
        tmp_suit = {'1Y1': 56}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y1'] = own_suit_p2.pop('SY1')
    if action == "4992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'1Y2': 57})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y2'] = own_suit_p2.pop('SY2')
    if action == "4993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'1Y3': 58})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    if action == "5991":
        tmp_suit = {'2Y1': 32}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['2Y1'] = own_suit_p2.pop('SY1')
    if action == "5992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'2Y2': 33})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['2Y2'] = own_suit_p2.pop('SY2')
    if action == "5993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'2Y3': 31})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    if action == "6991":
        tmp_suit = {'3Y1': 32}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['3Y1'] = own_suit_p2.pop('SY1')
    if action == "6992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'3Y2': 33})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['3Y2'] = own_suit_p2.pop('SY2')
    if action == "6993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'3Y3': 31})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    # from player 2 to player 1 , which means that player 1's cards need to change
    # player 1's cards w/o hints are listed as 'SX'
    if action == "4981":
        tmp_suit = {'1X1': 26}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['1X1'] = own_suit_p1.pop('SX1')
    if action == "4982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'1X2': 27})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['1X2'] = own_suit_p1.pop('SX2')
    if action == "4983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'1X3': 31})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    if action == "5981":
        tmp_suit = {'2X1': 26}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['2X1'] = own_suit_p1.pop('SX1')
    if action == "5982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'2X2': 27})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['2X2'] = own_suit_p1.pop('SX2')
    if action == "5983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'2X3': 31})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    if action == "6981":
        tmp_suit = {'3X1': 26}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['3X1'] = own_suit_p1.pop('SX1')
    if action == "6982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'3X2': 27})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['3X2'] = own_suit_p1.pop('SX2')
    if action == "6983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'3X3': 31})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    # PLAY A CARD
    # playability of card can be a sep function
    # when a card is played, the card needs to be replaced by a card dealt from the deck
    # Player 1 playing card
    if action == "7981":

        hand_dict = dict(itertools.islice(hand_p1.items(), 0, 1))
        for key in hand_dict.keys():
            card_playability(key, hand_p1, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        for key in col_dict.keys():
            own_colour_p1.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        for key in suit_dict.keys():
            own_suit_p1.pop(key)

    if action == "9982":

        hand_dict = dict(itertools.islice(hand_p1.items(), 1, 2))
        for key in hand_dict.keys():
            card_playability(key, hand_p1, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p1.items(), 1, 2))
        for key in col_dict.keys():
            own_colour_p1.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p1.items(), 1, 2))
        for key in suit_dict.keys():
            own_suit_p1.pop(key)

    if action == "11983":

        hand_dict = dict(itertools.islice(hand_p1.items(), 2, 3))
        for key in hand_dict.keys():
            card_playability(key, hand_p1, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p1.items(), 2, 3))
        for key in col_dict.keys():
            own_colour_p1.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p1.items(), 2, 3))
        for key in suit_dict.keys():
            own_suit_p1.pop(key)

    # Player 2 playing card
    if action == "7991":

        hand_dict = dict(itertools.islice(hand_p2.items(), 0, 1))
        for key in hand_dict.keys():
            card_playability(key, hand_p2, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        for key in col_dict.keys():
            own_colour_p2.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        for key in suit_dict.keys():
            own_suit_p2.pop(key)

    if action == "9992":

        hand_dict = dict(itertools.islice(hand_p2.items(), 1, 2))
        for key in hand_dict.keys():
            card_playability(key, hand_p2, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p2.items(), 1, 2))
        for key in col_dict.keys():
            own_colour_p2.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p2.items(), 1, 2))
        for key in suit_dict.keys():
            own_suit_p2.pop(key)

    if action == "11993":

        hand_dict = dict(itertools.islice(hand_p2.items(), 2, 3))
        for key in hand_dict.keys():
            card_playability(key, hand_p2, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p2.items(), 2, 3))
        for key in col_dict.keys():
            own_colour_p2.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p2.items(), 2, 3))
        for key in suit_dict.keys():
            own_suit_p2.pop(key)

    # Player 1 Discards card
    if action == "8981":

        hand_dict = dict(itertools.islice(hand_p1.items(), 0, 1))
        for key in hand_dict.keys():
            hand_p1.pop(key)
        col_dict = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        for key in col_dict.keys():
            own_colour_p1.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        for key in suit_dict.keys():
            own_suit_p1.pop(key)
            obs_tensor[1] += 1

    if action == "10982":

        hand_dict = dict(itertools.islice(hand_p1.items(), 1, 2))
        for key in hand_dict.keys():
            hand_p1.pop(key)
        col_dict = dict(itertools.islice(own_colour_p1.items(), 1, 2))
        for key in col_dict.keys():
            own_colour_p1.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p1.items(), 1, 2))
        for key in suit_dict.keys():
            own_suit_p1.pop(key)
            obs_tensor[1] += 1

    if action == "12983":

        hand_dict = dict(itertools.islice(hand_p1.items(), 2, 3))
        for key in hand_dict.keys():
            hand_p1.pop(key)
        col_dict = dict(itertools.islice(own_colour_p1.items(), 2, 3))
        for key in col_dict.keys():
            own_colour_p1.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p1.items(), 2, 3))
        for key in suit_dict.keys():
            own_suit_p1.pop(key)
            obs_tensor[1] += 1

    # Player 2 Discards Card
    if action == "8991":

        hand_dict = dict(itertools.islice(hand_p2.items(), 0, 1))
        for key in hand_dict.keys():
            hand_p2.pop(key)
        col_dict = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        for key in col_dict.keys():
            own_colour_p2.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        for key in suit_dict.keys():
            own_suit_p2.pop(key)
            obs_tensor[1] += 1

    if action == "10992":

        hand_dict = dict(itertools.islice(hand_p2.items(), 1, 2))
        for key in hand_dict.keys():
            hand_p2.pop(key)
        col_dict = dict(itertools.islice(own_colour_p2.items(), 1, 2))
        for key in col_dict.keys():
            own_colour_p2.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p2.items(), 1, 2))
        for key in suit_dict.keys():
            own_suit_p2.pop(key)
            obs_tensor[1] += 1

    if action == "12993":

        hand_dict = dict(itertools.islice(hand_p2.items(), 2, 3))
        for key in hand_dict.keys():
            hand_p2.pop(key)
        col_dict = dict(itertools.islice(own_colour_p2.items(), 2, 3))
        for key in col_dict.keys():
            own_colour_p2.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p2.items(), 2, 3))
        for key in suit_dict.keys():
            own_suit_p2.pop(key)
            obs_tensor[1] += 1

    updated_records = [hand_p1, hand_p2, deck, obs_tensor, current_player, own_colour_p1, own_suit_p1, own_colour_p2,
                       own_suit_p2, fireworks]
    return updated_records


### IMP: if the card is indeed playable, and the stack is updated, it is removed from obs dict automatically ;
### This does not need to be a sep exercise -- be sure to DEAL new card!

# Need to keep track of what is in hands and what is not!
def card_playability(card, player_hand, firework_stack, obs_tensor):
    if card == "R11":
        if "F1" in firework_stack:
            firework_stack.pop('F1')
            firework_stack.update({"R11": 0})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("R11")

    elif card == "R12":
        if "F1" in firework_stack:
            firework_stack.pop('F1')
            firework_stack.update({"R12": 3})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("R12")

    elif card == "R13":
        if "F1" in firework_stack:
            firework_stack.pop('F1')
            firework_stack.update({"R13": 6})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("R13")

    elif card == "B11":
        if "F2" in firework_stack:
            firework_stack.pop('F2')
            firework_stack.update({"B11": 2})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("B11")

    elif card == "B12":
        if "F2" in firework_stack:
            firework_stack.pop('F2')
            firework_stack.update({"B12": 5})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("B12")

    elif card == "B13":
        if "F2" in firework_stack:
            firework_stack.pop('F2')
            firework_stack.update({"B13": 8})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("B13")

    elif card == "G11":
        if "F3" in firework_stack:
            firework_stack.pop('F3')
            firework_stack.update({"G11": 1})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("G11")

    elif card == "G12":
        if "F3" in firework_stack:
            firework_stack.pop('F3')
            firework_stack.update({"G12": 4})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("G12")

    elif card == "G13":
        if "F3" in firework_stack:
            firework_stack.pop('F3')
            firework_stack.update({"G13": 7})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("G13")

    elif card == "R21":
        check = False
        proceeding_viable_cards = ["R11", "R12", "R13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"R21": 9})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("R21")

    elif card == "R22":
        check = False
        proceeding_viable_cards = ["R11", "R12", "R13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"R22": 12})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("R22")

    elif card == "B21":
        check = False
        proceeding_viable_cards = ["B11", "B12", "B13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"B21": 11})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("B21")

    elif card == "B22":
        check = False
        proceeding_viable_cards = ["B11", "B12", "R13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"B22": 14})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("B22")

    elif card == "G21":
        check = False
        proceeding_viable_cards = ["G11", "G12", "G13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"G21": 10})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("G21")

    elif card == "G22":
        check = False
        proceeding_viable_cards = ["G11", "G12", "G13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"G22": 13})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("G22")

    elif card == "R31":
        check = False
        proceeding_viable_cards = ["R21", "R22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"R31": 15})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("R31")

    elif card == "B31":
        check = False
        proceeding_viable_cards = ["B21", "B22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"B31": 17})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("B31")

    elif card == "G31":
        check = False
        proceeding_viable_cards = ["G21", "G22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"G31": 16})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("G31")


def check_and_deal_col(obs, player):
    positions = []

    for key in obs:
        card = str(key)
        positions.append(card[-1])
    if player == 1:
        if '1' not in positions:
            new_obs = {'XC1': 23}
            new_obs.update(obs)
        elif '2' not in positions:
            new_obs = dict(itertools.islice(obs.items(), 0, 1))
            new_obs.update({'XC2': 24})
            new_obs.update(dict(itertools.islice(obs.items(), 1, 2)))
        elif '3' not in positions:
            new_obs = obs
            new_obs.update({'XC3': 25})
    elif player == 2:
        if '1' not in positions:
            new_obs = {'YC1': 29}
            new_obs.update(obs)
        elif '2' not in positions:
            new_obs = dict(itertools.islice(obs.items(), 0, 1))
            new_obs.update({'YC2': 30})
            new_obs.update(dict(itertools.islice(obs.items(), 1, 2)))
        elif '3' not in positions:
            new_obs = obs
            new_obs.update({'YC3': 31})

    return new_obs


def check_and_deal_suit(obs, player):
    positions = []

    for key in obs:
        card = str(key)
        positions.append(card[-1])
    if player == 1:

        if '1' not in positions:
            new_obs = {'SX1': 26}
            new_obs.update(obs)
        elif '2' not in positions:
            new_obs = dict(itertools.islice(obs.items(), 0, 1))
            new_obs.update({'SX2': 27})
            new_obs.update(dict(itertools.islice(obs.items(), 1, 2)))
        elif '3' not in positions:
            new_obs = obs
            new_obs.update({'SX3': 28})
    elif player == 2:

        if '1' not in positions:
            new_obs = {'SY1': 32}
            new_obs.update(obs)
        elif '2' not in positions:
            new_obs = dict(itertools.islice(obs.items(), 0, 1))
            new_obs.update({'SY2': 33})
            new_obs.update(dict(itertools.islice(obs.items(), 1, 2)))
        elif '3' not in positions:
            new_obs = obs
            new_obs.update({'SY3': 34})

    return new_obs


def get_reward(observations):
    reward = 0
    fireworks_count = []

    fireworks = observations[9]

    for key in fireworks:
        fireworks_count.append(key)

    for i, k in zip(range(len(fireworks_count)), fireworks_count):
        if fireworks_count[i][0] is not 'F':
            reward += int(k[1:2])

    return reward


def is_terminal(observations, reward):
    if observations[3][2] == 0:
        return True

    if reward == 9:
        return True

    if observations[0] == {} and observations[1] == {} and observations[2] == {}:
        return True

    else:
        return False
