import itertools

all_legal_actions = {"1991": 1, "2991": 2, "3991": 3, "13991": 4, "1992": 5, "2992": 6, "3992": 7, "13992": 8,
                     "1993": 9,
                     "2993": 10, "3993": 11, "13993": 12, "4991": 13, "5991": 14, "6991": 15, "14991": 16, "4992": 17,
                     "5992": 18,
                     "6992": 19, "14992": 20, "4993": 21, "5993": 22, "6993": 23, "14993": 24, "7981": 25, "9982": 26,
                     "11983": 27, "8981": 28, "10982": 29, "12983": 30, "1981": 31, "2981": 32,
                     "3981": 33, "13981": 34, "1982": 35, "2982": 36, "3982": 37, "13982": 38, "1983": 39, "2983": 40,
                     "3983": 41, "13983": 42, "4981": 43, "5981": 44, "6981": 45, "14981": 46, "4982": 47, "5982": 48,
                     "6982": 49, "14982": 50, "4983": 51, "5983": 52, "6983": 53, "14983": 54, "7991": 55, "9992": 56,
                     "11993": 57, "8991": 58, "10992": 59, "12993": 60,"1971": 61, "2971": 62, "3971": 63, "13971": 64,
                     "1972": 65, "2972": 66, "3972": 67, "13972": 68, "1973": 69, "2973": 70, "3973": 71, "13973": 72,
                     "4971": 73, "5971": 74, "6971": 75, "14971": 76, "4972": 77,
                     "5972": 78,"6972": 79, "14972": 80, "4973": 81, "5973": 82, "6973": 83, "14973": 84,
                     "7971": 85, "9972": 86,
                     "11973": 87, "8971": 88, "10972": 89, "12973": 90}

game_moves = len(all_legal_actions)


def apply_action(records, action):
    action = str(action)


    curr_records = records[0]

    hand_p1 = curr_records[0]
    hand_p2 = curr_records[1]
    hand_p3 = curr_records[2]

    deck = curr_records[3]
    obs_tensor = curr_records[4]

    current_player = curr_records[5]
    own_colour_p1 = curr_records[6]
    own_suit_p1 = curr_records[7]
    own_colour_p2 = curr_records[8]
    own_suit_p2 = curr_records[9]
    own_colour_p3 = curr_records[10]
    own_suit_p3 = curr_records[11]

    fireworks = curr_records[12]

    for key in current_player:
        if key == "Player_One":
            current_player = {"Player_Two": 99}
        elif key == "Player_Two":
            current_player = {"Player_One": 98}
        elif key == "Player_Three":
            current_player = {"Player_Three": 97}

    # REVEAL COLOURS
    # from player 1 to player to 2, which means that player 2's card knowledge needs to change
    # player 2's cards w/o hints are listed as 'YC'
    ### imp! need to reduce for each, an information token upon giving hints

    # Reveal Red
    if action == "1991":
        tmp_col = {'YR1': 13}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YR1'] = own_colour_p2.pop('YC1')
    if action == "1992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YR2': 14})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YR2'] = own_colour_p2.pop('YC2')
    if action == "1993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YR3': 15})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    # Reveal Green
    if action == "3991":
        tmp_col = {'YG1': 16}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        obs_tensor[1] -= 1

        # own_colour_p2['YG1'] = own_colour_p2.pop('YC1')
    if action == "3992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YG2': 17})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YG2'] = own_colour_p2.pop('YC2')
    if action == "3993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YG3': 18})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    # Reveal Blue
    if action == "2991":
        tmp_col = {'YB1': 19}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YB1'] = own_colour_p2.pop('YC1')
    if action == "2992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YB2': 20})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YB2'] = own_colour_p2.pop('YC2')
    if action == "2993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YB3': 21})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    # Reveal White
    if action == "13991":
        tmp_col = {'YW1': 22}
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 1, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    if action == "13992":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 1))
        tmp_col.update({'YW2': 35})
        tmp_col.update(dict(itertools.islice(own_colour_p2.items(), 2, 3)))
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    if action == "13993":
        tmp_col = dict(itertools.islice(own_colour_p2.items(), 0, 2))
        tmp_col.update({'YW3': 36})
        own_colour_p2 = tmp_col
        obs_tensor[1] -= 1

    # from player 2 to player 1 , which means that player 1's cards need to change
    # player 1's cards w/o hints are listed as 'XC'
    if action == "1981":
        tmp_col = {'XR1': 37}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XR1'] = own_colour_p1.pop('XC1')
    if action == "1982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XR2': 38})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XR2'] = own_colour_p1.pop('XC2')
    if action == "1983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XR3': 39})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    if action == "3981":
        tmp_col = {'XG1': 40}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XG1'] = own_colour_p1.pop('XC1')
    if action == "3982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XG2': 41})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XG2'] = own_colour_p1.pop('XC2')
    if action == "3983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XG3': 42})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    if action == "2981":
        tmp_col = {'XB1': 43}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XB1'] = own_colour_p1.pop('XC1')
    if action == "2982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XB2': 44})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XB2'] = own_colour_p1.pop('XC2')
    if action == "2983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XB3': 45})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    # Reveal White
    if action == "13981":
        tmp_col = {'XW1': 65}
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 1, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XR1'] = own_colour_p1.pop('XC1')
    if action == "13982":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 1))
        tmp_col.update({'XW2': 66})
        tmp_col.update(dict(itertools.islice(own_colour_p1.items(), 2, 3)))
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p1['XR2'] = own_colour_p1.pop('XC2')
    if action == "13983":
        tmp_col = dict(itertools.islice(own_colour_p1.items(), 0, 2))
        tmp_col.update({'XW3': 67})
        own_colour_p1 = tmp_col
        obs_tensor[1] -= 1

    # action directed at player 3
    # Reveal Red
    if action == "1971":
        tmp_col = {'ZR1': 81}
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 1, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YR1'] = own_colour_p2.pop('YC1')
    if action == "1972":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 1))
        tmp_col.update({'ZR2': 82})
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 2, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YR2'] = own_colour_p2.pop('YC2')
    if action == "1973":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 2))
        tmp_col.update({'ZR3': 83})
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

    # Reveal Green
    if action == "3971":
        tmp_col = {'ZG1': 84}
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 1, 3)))
        obs_tensor[1] -= 1

        # own_colour_p2['YG1'] = own_colour_p2.pop('YC1')
    if action == "3972":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 1))
        tmp_col.update({'ZG2': 85})
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 2, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YG2'] = own_colour_p2.pop('YC2')
    if action == "3973":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 2))
        tmp_col.update({'ZG3': 86})
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

    # Reveal Blue
    if action == "2971":
        tmp_col = {'ZB1': 87}
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 1, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YB1'] = own_colour_p2.pop('YC1')
    if action == "2972":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 1))
        tmp_col.update({'ZB2': 88})
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 2, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

        # own_colour_p2['YB2'] = own_colour_p2.pop('YC2')
    if action == "2973":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 2))
        tmp_col.update({'ZB3': 89})
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

    # Reveal White
    if action == "13971":
        tmp_col = {'ZW1': 90}
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 1, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

    if action == "13972":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 1))
        tmp_col.update({'ZW2': 91})
        tmp_col.update(dict(itertools.islice(own_colour_p3.items(), 2, 3)))
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

    if action == "13973":
        tmp_col = dict(itertools.islice(own_colour_p3.items(), 0, 2))
        tmp_col.update({'ZW3': 92})
        own_colour_p3 = tmp_col
        obs_tensor[1] -= 1

    # REVEAL SUITS
    # from player 1 to player to pl 2 , which means that player 2's card knowledge needs to change
    # player 2's cards w/o hints are listed as 'SY'
    if action == "4991":
        tmp_suit = {'1Y1': 46}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y1'] = own_suit_p2.pop('SY1')
    if action == "4992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'1Y2': 47})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y2'] = own_suit_p2.pop('SY2')
    if action == "4993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'1Y3': 48})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    if action == "5991":
        tmp_suit = {'2Y1': 49}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['2Y1'] = own_suit_p2.pop('SY1')
    if action == "5992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'2Y2': 50})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['2Y2'] = own_suit_p2.pop('SY2')
    if action == "5993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'2Y3': 51})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    if action == "6991":
        tmp_suit = {'3Y1': 52}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['3Y1'] = own_suit_p2.pop('SY1')
    if action == "6992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'3Y2': 53})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['3Y2'] = own_suit_p2.pop('SY2')
    if action == "6993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'3Y3': 54})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    # revealing suit 4
    if action == "14991":
        tmp_suit = {'4Y1': 68}
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 1, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y1'] = own_suit_p2.pop('SY1')
    if action == "14992":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 1))
        tmp_suit.update({'4Y2': 69})
        tmp_suit.update(dict(itertools.islice(own_suit_p2.items(), 2, 3)))
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y2'] = own_suit_p2.pop('SY2')
    if action == "14993":
        tmp_suit = dict(itertools.islice(own_suit_p2.items(), 0, 2))
        tmp_suit.update({'4Y3': 70})
        own_suit_p2 = tmp_suit
        obs_tensor[1] -= 1

    # from player 2 to player 1 , which means that player 1's cards need to change
    # player 1's cards w/o hints are listed as 'SX'
    if action == "4981":
        tmp_suit = {'1X1': 55}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['1X1'] = own_suit_p1.pop('SX1')
    if action == "4982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'1X2': 56})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['1X2'] = own_suit_p1.pop('SX2')
    if action == "4983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'1X3': 57})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    if action == "5981":
        tmp_suit = {'2X1': 58}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['2X1'] = own_suit_p1.pop('SX1')
    if action == "5982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'2X2': 59})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['2X2'] = own_suit_p1.pop('SX2')
    if action == "5983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'2X3': 60})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    if action == "6981":
        tmp_suit = {'3X1': 61}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['3X1'] = own_suit_p1.pop('SX1')
    if action == "6982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'3X2': 62})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['3X2'] = own_suit_p1.pop('SX2')
    if action == "6983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'3X3': 63})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    # Reveal Suit 4
    if action == "14981":
        tmp_suit = {'4X1': 71}
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 1, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['1X1'] = own_suit_p1.pop('SX1')
    if action == "14982":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 1))
        tmp_suit.update({'4X2': 72})
        tmp_suit.update(dict(itertools.islice(own_suit_p1.items(), 2, 3)))
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p1['1X2'] = own_suit_p1.pop('SX2')
    if action == "14983":
        tmp_suit = dict(itertools.islice(own_suit_p1.items(), 0, 2))
        tmp_suit.update({'4X3': 73})
        own_suit_p1 = tmp_suit
        obs_tensor[1] -= 1

    # REVEAL SUITS TO PLAYER 3
    if action == "4971":
        tmp_suit = {'1Z1': 93}
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 1, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y1'] = own_suit_p2.pop('SY1')
    if action == "4972":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 1))
        tmp_suit.update({'1Z2': 94})
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 2, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y2'] = own_suit_p2.pop('SY2')
    if action == "4973":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 2))
        tmp_suit.update({'1Z3': 95})
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

    if action == "5971":
        tmp_suit = {'2Z1': 96}
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 1, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['2Y1'] = own_suit_p2.pop('SY1')
    if action == "5972":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 1))
        tmp_suit.update({'2Z2': 97})
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 2, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['2Y2'] = own_suit_p2.pop('SY2')
    if action == "5973":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 2))
        tmp_suit.update({'2Z3': 98})
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

    if action == "6971":
        tmp_suit = {'3Z1': 99}
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 1, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['3Y1'] = own_suit_p2.pop('SY1')
    if action == "6972":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 1))
        tmp_suit.update({'3Z2': 100})
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 2, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['3Y2'] = own_suit_p2.pop('SY2')
    if action == "6973":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 2))
        tmp_suit.update({'3Z3': 101})
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

    # Reveal Suit 4
    if action == "14971":
        tmp_suit = {'4Z1': 102}
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 1, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y1'] = own_suit_p2.pop('SY1')
    if action == "14972":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 1))
        tmp_suit.update({'4Z2': 103})
        tmp_suit.update(dict(itertools.islice(own_suit_p3.items(), 2, 3)))
        own_suit_p3 = tmp_suit
        obs_tensor[1] -= 1

        # own_suit_p2['1Y2'] = own_suit_p2.pop('SY2')
    if action == "14973":
        tmp_suit = dict(itertools.islice(own_suit_p3.items(), 0, 2))
        tmp_suit.update({'4Z3': 104})
        own_suit_p3 = tmp_suit
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

    # Player 3 playing card
    if action == "7971":

        hand_dict = dict(itertools.islice(hand_p3.items(), 0, 1))
        for key in hand_dict.keys():
            card_playability(key, hand_p3, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p3.items(), 0, 1))
        for key in col_dict.keys():
            own_colour_p3.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p3.items(), 0, 1))
        for key in suit_dict.keys():
            own_suit_p3.pop(key)

    if action == "9972":

        hand_dict = dict(itertools.islice(hand_p3.items(), 1, 2))
        for key in hand_dict.keys():
            card_playability(key, hand_p3, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p3.items(), 1, 2))
        for key in col_dict.keys():
            own_colour_p3.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p3.items(), 1, 2))
        for key in suit_dict.keys():
            own_suit_p3.pop(key)

    if action == "11973":

        hand_dict = dict(itertools.islice(hand_p3.items(), 2, 3))
        for key in hand_dict.keys():
            card_playability(key, hand_p3, fireworks, obs_tensor)
        col_dict = dict(itertools.islice(own_colour_p3.items(), 2, 3))
        for key in col_dict.keys():
            own_colour_p3.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p3.items(), 2, 3))
        for key in suit_dict.keys():
            own_suit_p3.pop(key)

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

    # Player 3 Discards card
    if action == "8971":

        hand_dict = dict(itertools.islice(hand_p3.items(), 0, 1))
        for key in hand_dict.keys():
            hand_p3.pop(key)
        col_dict = dict(itertools.islice(own_colour_p3.items(), 0, 1))
        for key in col_dict.keys():
            own_colour_p3.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p3.items(), 0, 1))
        for key in suit_dict.keys():
            own_suit_p3.pop(key)
            obs_tensor[1] += 1

    if action == "10972":

        hand_dict = dict(itertools.islice(hand_p3.items(), 1, 2))
        for key in hand_dict.keys():
            hand_p3.pop(key)
        col_dict = dict(itertools.islice(own_colour_p3.items(), 1, 2))
        for key in col_dict.keys():
            own_colour_p3.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p3.items(), 1, 2))
        for key in suit_dict.keys():
            own_suit_p3.pop(key)
            obs_tensor[1] += 1

    if action == "12983":

        hand_dict = dict(itertools.islice(hand_p3.items(), 2, 3))
        for key in hand_dict.keys():
            hand_p3.pop(key)
        col_dict = dict(itertools.islice(own_colour_p3.items(), 2, 3))
        for key in col_dict.keys():
            own_colour_p3.pop(key)
        suit_dict = dict(itertools.islice(own_suit_p3.items(), 2, 3))
        for key in suit_dict.keys():
            own_suit_p3.pop(key)
            obs_tensor[1] += 1

    updated_records = [hand_p1, hand_p2,hand_p3, deck, obs_tensor, current_player, own_colour_p1, own_suit_p1, own_colour_p2,
                       own_suit_p2,own_colour_p3,own_suit_p3, fireworks]
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

    elif card == "W11":
        if "F4" in firework_stack:
            firework_stack.pop('F4')
            firework_stack.update({"W11": 3})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("W11")

    elif card == "W12":
        if "F4" in firework_stack:
            firework_stack.pop('F4')
            firework_stack.update({"W12": 7})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("W12")

    elif card == "W13":
        if "F4" in firework_stack:
            firework_stack.pop('F4')
            firework_stack.update({"W13": 11})
        else:
            obs_tensor[2] -= 1
        player_hand.pop("W13")

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

    elif card == "W21":
        check = False
        proceeding_viable_cards = ["W11", "W12", "W13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"W21": 15})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("W21")

    elif card == "W22":
        check = False
        proceeding_viable_cards = ["W11", "W12", "W13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"W22": 19})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("W22")

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

    elif card == "W31":
        check = False
        proceeding_viable_cards = ["W21", "W22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"W31": 23})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("W31")

    elif card == "R32":
        check = False
        proceeding_viable_cards = ["R21", "R22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"R32": 24})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("R32")

    elif card == "B32":
        check = False
        proceeding_viable_cards = ["B21", "B22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"B32": 26})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("B32")

    elif card == "G32":
        check = False
        proceeding_viable_cards = ["G21", "G22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"G32": 25})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("G32")

    elif card == "W32":
        check = False
        proceeding_viable_cards = ["W21", "W22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"W32": 27})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("W32")

    elif card == "R41":
        check = False
        proceeding_viable_cards = ["R31", "R32"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"R41": 28})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("R41")

    elif card == "B41":
        check = False
        proceeding_viable_cards = ["B31", "B32"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"B41": 30})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("B41")

    elif card == "G41":
        check = False
        proceeding_viable_cards = ["G31", "G32"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"G41": 30})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("G41")

    elif card == "W41":
        check = False
        proceeding_viable_cards = ["W31", "W32"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack.pop(x)
                firework_stack.update({"W41": 31})
                check = True
        if check is False:
            obs_tensor[2] -= 1
        player_hand.pop("W41")


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
    elif player == 3:
        if '1' not in positions:
            new_obs = {'ZC1': 105}
            new_obs.update(obs)
        elif '2' not in positions:
            new_obs = dict(itertools.islice(obs.items(), 0, 1))
            new_obs.update({'ZC2': 106})
            new_obs.update(dict(itertools.islice(obs.items(), 1, 2)))
        elif '3' not in positions:
            new_obs = obs
            new_obs.update({'ZC3': 107})


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
    elif player == 3:
        if '1' not in positions:
            new_obs = {'SZ1': 108}
            new_obs.update(obs)
        elif '2' not in positions:
            new_obs = dict(itertools.islice(obs.items(), 0, 1))
            new_obs.update({'SZ2': 109})
            new_obs.update(dict(itertools.islice(obs.items(), 1, 2)))
        elif '3' not in positions:
            new_obs = obs
            new_obs.update({'SZ3': 110})

    return new_obs


def get_reward(observations):


    reward = 0
    fireworks_count = []

    fireworks = observations[12]

    for key in fireworks:
        fireworks_count.append(key)

    for i, k in zip(range(len(fireworks_count)), fireworks_count):
        if fireworks_count[i][0] is not 'F':
            reward += int(k[1:2])

    return reward


def is_terminal(observations, reward):

    if len(observations[3]) == 1:
        return True

    if observations[4][2] == 0:
        return True

    if reward == 12:
        return True

    if observations[0] == {} and observations[1] == {} and observations[2] == {}:

        return True

    else:
        return False
