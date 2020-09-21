imprt rl_env
import itertools
all_legal_actions= {"1991":1 , "2991":2, "3991":3 , "1992":4 , "2992":5 , "3992":6, "1993":7,
                    "2993":8, "3993":9 , "4991":10 , "5991":11 ,"6991":12 , "4992":13, "5992":14,
                    "6992":15 , "4993":16 , "5993":17, "6993":18 , "7981":19 , "9982":20 ,
                    "11983":21 , "8981":22 , "10982":23 , "12983":24 , "1981":25 , "2981":26,
                    "3981":27, "1982":28 , "2982":29 , "3982":30 , "1983":31 , "2983":32,
                    "3983":33 , "4981":34 , "5981":35, "6981":36 , "4982":37 , "5982":38,
                    "6982":39 , "4983":40 , "5983":41 , "6983":42, "7991":43 , "9992":44,
                    "11993":45 , "8991":46 , "10992":47 ,"12993":48}


def apply_action(hand_p1,hand_p2,own_colour_p1,own_colour_p2,own_suit_p1,own_suit_p2,obs_tensor,fireworks, action):

    # REVEAL COLOURS
    # from player 1 to player to 2, which means that player 2's card knowledge needs to change
    # player 2's cards w/o hints are listed as 'YC'
    if action == "1991":
        own_colour_p2['YR1'] = own_colour_p2.pop('YC1')
    if action == "1992":
        own_colour_p2['YR2'] = own_colour_p2.pop('YC2')
    if action == "1993":
        own_colour_p2['YR3'] = own_colour_p2.pop('YC3')
    if action == "3991":
        own_colour_p2['YG1'] = own_colour_p2.pop('YC1')
    if action == "3992":
        own_colour_p2['YG2'] = own_colour_p2.pop('YC2')
    if action == "3993":
        own_colour_p2['YG3'] = own_colour_p2.pop('YC3')
    if action == "2991":
        own_colour_p2['YB1'] = own_colour_p2.pop('YC1')
    if action == "2992":
        own_colour_p2['YB2'] = own_colour_p2.pop('YC2')
    if action == "2993":
        own_colour_p2['YB3'] = own_colour_p2.pop('YC3')

    # from player 2 to player 1 , which means that player 1's cards need to change
    # player 1's cards w/o hints are listed as 'XC'
    if action == "1981":
        own_colour_p1['XR1'] = own_colour_p1.pop('XC1')
    if action == "1982":
        own_colour_p1['XR2'] = own_colour_p1.pop('XC2')
    if action == "1983":
        own_colour_p1['XR3'] = own_colour_p1.pop('XC3')
    if action == "3981":
        own_colour_p1['XG1'] = own_colour_p1.pop('XC1')
    if action == "3982":
        own_colour_p1['XG2'] = own_colour_p1.pop('XC2')
    if action == "3983":
        own_colour_p1['XG3'] = own_colour_p1.pop('XC3')
    if action == "2981":
        own_colour_p1['XB1'] = own_colour_p1.pop('XC1')
    if action == "2982":
        own_colour_p1['XB2'] = own_colour_p1.pop('XC2')
    if action == "2983":
        own_colour_p1['XB3'] = own_colour_p1.pop('XC3')

    # REVEAL SUITS
    # from player 1 to player to , which means that player 2's card knowledge needs to change
    # player 2's cards w/o hints are listed as 'SY'
    if action == "4991":
        own_suit_p2['1Y1'] = own_suit_p2.pop('SY1')
    if action == "4992":
        own_suit_p2['1Y2'] = own_suit_p2.pop('SY2')
    if action == "4993":
        own_suit_p2['1Y3'] = own_suit_p2.pop('SY3')
    if action == "5991":
        own_suit_p2['2Y1'] = own_suit_p2.pop('SY1')
    if action == "5992":
        own_suit_p2['2Y2'] = own_suit_p2.pop('SY2')
    if action == "5993":
        own_suit_p2['2Y3'] = own_suit_p2.pop('SY3')
    if action == "6991":
        own_suit_p2['3Y1'] = own_suit_p2.pop('SY1')
    if action == "6992":
        own_suit_p2['3Y2'] = own_suit_p2.pop('SY2')
    if action == "6993":
        own_suit_p2['3Y3'] = own_suit_p2.pop('SY3')

    # from player 2 to player 1 , which means that player 1's cards need to change
    # player 1's cards w/o hints are listed as 'SX'
    if action == "4981":
        own_suit_p1['1X1'] = own_suit_p1.pop('SX1')
    if action == "4982":
        own_suit_p1['1X2'] = own_suit_p1.pop('SX2')
    if action == "4983":
        own_suit_p1['1X3'] = own_suit_p1.pop('SX3')
    if action == "5981":
        own_suit_p1['2X1'] = own_suit_p1.pop('SX1')
    if action == "5982":
        own_suit_p1['2X2'] = own_suit_p1.pop('SX2')
    if action == "5983":
        own_suit_p1['2X3'] = own_suit_p1.pop('SX3')
    if action == "6981":
        own_suit_p1['3X1'] = own_suit_p1.pop('SX1')
    if action == "6982":
        own_suit_p1['3X2'] = own_suit_p1.pop('SX2')
    if action == "6983":
        own_suit_p1['3X3'] = own_suit_p1.pop('SX3')

    # PLAY A CARD
    # playability of card can be a sep function
    # when a card is played, the card needs to be replaced by a card dealt from the deck
    #Player 1 playing card
    if action == "7981":
        hand_dict = dict(itertools.islice(hand_p1.items(),0,1))
        for key in hand_dict.keys():
            card_playability(key,hand_p1,fireworks,obs_tensor)

    if action == "9982":
        hand_dict = dict(itertools.islice(hand_p1.items(),1,2))
        for key in hand_dict.keys():
            card_playability(key,hand_p1,fireworks,obs_tensor)

    if action == "11983":
        hand_dict = dict(itertools.islice(hand_p1.items(),2,3))
        for key in hand_dict.keys():
            card_playability(key,hand_p1,fireworks,obs_tensor)

    #Player 2 playing card
    if action == "7991":
        hand_dict = dict(itertools.islice(hand_p2.items(), 0, 1))
        for key in hand_dict.keys():
            card_playability(key, hand_p2, fireworks, obs_tensor)

    if action == "9992":
        hand_dict = dict(itertools.islice(hand_p2.items(), 1, 2))
        for key in hand_dict.keys():
            card_playability(key, hand_p2, fireworks, obs_tensor)

    if action == "11993":
        hand_dict = dict(itertools.islice(hand_p2.items(), 2, 3))
        for key in hand_dict.keys():
            card_playability(key, hand_p2, fireworks, obs_tensor)

    # Player 1 Discards card
    if action == "8981":
        hand_dict = dict(itertools.islice(hand_p1.items(), 0, 1))
        for key in hand_dict.keys():
            hand_p1.pop(key)
            obs_tensor[1] += 1

    if action == "10982":
        hand_dict = dict(itertools.islice(hand_p1.items(), 1, 2))
        for key in hand_dict.keys():
            hand_p1.pop(key)
            obs_tensor[1] += 1

    if action == "12983":
        hand_dict = dict(itertools.islice(hand_p1.items(), 2, 3))
        for key in hand_dict.keys():
            hand_p1.pop(key)
            obs_tensor[1] += 1

    # Player 2 Discards Card
    if action == "8991":
        hand_dict = dict(itertools.islice(hand_p2.items(), 0, 1))
        for key in hand_dict.keys():
            hand_p1.pop(key)
            obs_tensor[1] += 1

    if action == "10992":
        hand_dict = dict(itertools.islice(hand_p2.items(), 1, 2))
        for key in hand_dict.keys():
            hand_p1.pop(key)
            obs_tensor[1] += 1

    if action == "12993":
        hand_dict = dict(itertools.islice(hand_p2.items(), 2, 3))
        for key in hand_dict.keys():
            hand_p1.pop(key)
            obs_tensor[1] += 1

    return hand_p1, hand_p2, own_colour_p1, own_colour_p2, own_suit_p1, own_suit_p2, obs_tensor, fireworks


### IMP: if the card is indeed playable, and the stack is updated, it is removed from obs dict automatically ;
### This does not need to be a sep exercise -- be sure to DEAL new card!

# Need to keep track of what is in hands and what is not!
def card_playability(card,player_hand,firework_stack, obs_tensor):

    if card == "R11":
        if "F1" in firework_stack:
            firework_stack['R11'] = firework_stack.pop('F1')
            player_hand.pop("R11")
        else:
            obs_tensor[2] -= 1

    elif card == "R12":
        if "F1" in firework_stack:
            firework_stack['R12'] = firework_stack.pop('F1')
            player_hand.pop("R12")
        else:
            obs_tensor[2] -= 1

    elif card == "R13":
        if "F1" in firework_stack:
            firework_stack['R13'] = firework_stack.pop('F1')
            player_hand.pop("R13")
        else:
            obs_tensor[2] -= 1

    elif card == "B11":
        if "F2" in firework_stack:
            firework_stack['B11'] = firework_stack.pop('F2')
            player_hand.pop("B11")
        else:
            obs_tensor[2] -= 1

    elif card == "B12":
        if "F2" in firework_stack:
            firework_stack['B12'] = firework_stack.pop('F2')
            player_hand.pop("B12")
        else:
            obs_tensor[2] -= 1

    elif card == "B13":
        if "F2" in firework_stack:
            firework_stack['B13'] = firework_stack.pop('F2')
            player_hand.pop("B13")
        else:
            obs_tensor[2] -= 1

    elif card == "G11":
        if "F3" in firework_stack:
            firework_stack['G11'] = firework_stack.pop('F3')
            player_hand.pop("G11")
        else:
            obs_tensor[2] -= 1

    elif card == "G12":
        if "F3" in firework_stack:
            firework_stack['G12'] = firework_stack.pop('F3')
            player_hand.pop("G12")
        else:
            obs_tensor[2] -= 1

    elif card == "G13":
        if "F3" in firework_stack:
            firework_stack['G13'] = firework_stack.pop('F3')
            player_hand.pop("G13")
        else:
            obs_tensor[2] -= 1

    elif card == "R21":
        proceeding_viable_cards = ["R11", "R12" , "R13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["R21"] = firework_stack.pop(x)
                player_hand.pop("R21")
            else:
                obs_tensor[2] -= 1

    elif card == "R22":
        proceeding_viable_cards = ["R11", "R12", "R13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["R22"] = firework_stack.pop(x)
                player_hand.pop("R22")
            else:
                obs_tensor[2] -= 1

    elif card == "B21":
        proceeding_viable_cards = ["B11", "B12", "B13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["B21"] = firework_stack.pop(x)
                player_hand.pop("B21")
            else:
                obs_tensor[2] -= 1

    elif card == "B22":
        proceeding_viable_cards = ["B11", "B12", "R13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["B22"] = firework_stack.pop(x)
                player_hand.pop("B22")
            else:
                obs_tensor[2] -= 1

    elif card == "G21":
        proceeding_viable_cards = ["G11", "G12", "G13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["G21"] = firework_stack.pop(x)
                player_hand.pop("G21")
            else:
                obs_tensor[2] -= 1

    elif card == "G22":
        proceeding_viable_cards = ["G11", "G12", "G13"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["R21"] = firework_stack.pop(x)
                player_hand.pop("B22")
            else:
                obs_tensor[2] -= 1

    elif card == "R31":
        proceeding_viable_cards = ["R21", "R22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["R31"] = firework_stack.pop(x)
                player_hand.pop("R31")
            else:
                obs_tensor[2] -= 1

    elif card == "B31":
        proceeding_viable_cards = ["B21", "B22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["B31"] = firework_stack.pop(x)
                player_hand.pop("B31")
            else:
                obs_tensor[2] -= 1

    elif card == "G31":
        proceeding_viable_cards = ["G21", "G22"]
        for x in proceeding_viable_cards:
            if x in firework_stack:
                firework_stack["G31"] = firework_stack.pop(x)
                player_hand.pop("G31")
            else:
                obs_tensor[2] -= 1




