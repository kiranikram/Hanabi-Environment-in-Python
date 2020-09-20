all_hint_actions = ['1991', '1992', '1993', '3991', '3992', '3993', '2991', '2992', '2993',
                    '1981', '1982', '1983', '3981', '3982', '3983', '2981', '2982', '2983',
                    '4991', '4992', '4993', '5991', '5992', '5993', '6991', '6992', '6993', '4981', '4982',
                    '4983', '5981', '5982', '5983', '6981', '6982', '6983', '7981', '9982', '11983', '7991', '9992',
                    '11993', '8981', '10982', '12983', '8991', '10992', '12993', '13991', '13992', '13993',
                    '13981','13982', '13983', '14991', '14992', '14993', '14981', '14982', '14983','1971', '1972',
                    '1973', '3971','3972', '3973', '2971', '2972', '2973','4971', '4972','4973', '5971', '5972',
                    '5973', '6971', '6972','6973','7971', '9972','11973','8971', '10972', '12973', '13971', '13972',
                    '13973','14971', '14972', '14973']

unique_perms_cols = {'RGW': 1, "RGB": 2, "RGC": 3, "RWG": 4, "RWB": 5, "RWC": 6, "RBG": 7, "RBW": 8, "RBC": 9,
                     "RCG": 10, "RCW": 11, "RCB": 12, "GBW": 13, "GRB": 14, "GRC": 15, "GWR": 16,
                     "GWB": 17, "GWC": 18, "GBR": 19, "WWC": 20, "GBC": 21, "GCR": 22, "GCW": 23, "GCB": 24, "WRG": 25,
                     "WRB": 26,
                     "WRC": 27, "WGR": 28, "WGB": 29, "WGC": 30,
                     "WBR": 31, "WBG": 32, "WBC": 33, "WCR": 34, "WCG": 35, "WCB": 36, "BRG": 37, "BRW": 38, "BRC": 39,
                     "BGR": 40, "BGW": 41, "BGC": 42, "BWR": 43, "BWG": 44, "BWC": 45,
                     "BCR": 46, "BCG": 47, "BCW": 48, "CRG": 49, "CRW": 50, "CRB": 51,
                     "CGR": 52, "CGW": 53, "CGB": 54, "CWR": 55, "CWG": 56, "CWB": 57, "CBR": 58, "CBG": 59, "CBW": 60,
                     "RRW": 61, "RWR": 62, "WRR": 63, "RRG": 64, "RGR": 65, "GRR": 66, "RRB": 67, "RBR": 68, "BRR": 69,
                     "RRC": 70, "RCR": 71, "CRR": 72, "GGW": 73, "GWG": 74, "WGG": 75, "GGR": 76, "GRG": 77, "RGG": 78,
                     "GGB": 79,
                     "GBG": 80, "BGG": 81, "GGC": 82, "GCG": 83, "CGG": 84, "WWG": 85, "WGW": 86, "GWW": 87, "WWR": 88,
                     "WRW": 89, "RWW": 90, "WWB": 91,
                     "WBW": 92, "BWW": 93, "WCW": 95, "CWW": 96, "BBW": 97, "BWB": 98, "WBB": 99, "BBR": 100,
                     "BRB": 101, "RBB": 102,
                     "BBG": 103, "BGB": 104, "GBB": 105, "BBC": 106, "BCB": 107, "CBB": 108, "CCW": 109, "CWC": 110,
                     "WCC": 111, "CCR": 112, "CRC": 113,
                     "RCC": 114, "CCG": 115, "CGC": 116, "GCC": 117, "CCB": 118, "CBC": 119, "BCC": 120, "RRR": 121,
                     "WWW": 122, "BBB": 123, "GGG": 124, "CCC": 125}

cols_keys = list(unique_perms_cols.keys())

unique_perms_suits = {'134': 1, "132": 2, "13S": 3, "143": 4, "142": 5, "14S": 6, "123": 7, "124": 8, "12S": 9,
                      "153": 10, "1S4": 11, "1S2": 12, "324": 13, "312": 14, "31S": 15, "341": 16,
                      "342": 17, "34S": 18, "321": 19, "1S3": 20, "32S": 21, "3S1": 22, "3S4": 23, "3S2": 24, "413": 25,
                      "412": 26,
                      "41S": 27, "431": 28, "432": 29, "43S": 30,
                      "421": 31, "423": 32, "42S": 33, "4S1": 34, "4S3": 35, "4S2": 36, "213": 37, "214": 38, "21S": 39,
                      "231": 40, "234": 41, "23S": 42, "241": 43, "243": 44, "24S": 45,
                      "2S1": 46, "2S3": 47, "2S4": 48, "S13": 49, "S14": 50, "S12": 51,
                      "S31": 52, "S34": 53, "S32": 54, "S41": 55, "S43": 56, "S42": 57, "S21": 58, "S23": 59, "S24": 60,
                      "114": 61, "141": 62, "411": 63, "113": 64, "131": 65, "311": 66, "112": 67, "121": 68, "211": 69,
                      "11S": 70, "1S1": 71, "S11": 72, "334": 73, "343": 74, "433": 75, "331": 76, "313": 77, "133": 78,
                      "332": 79,
                      "323": 80, "233": 81, "33S": 82, "3S3": 83, "S33": 84, "443": 85, "434": 86, "344": 87, "441": 88,
                      "414": 89, "144": 90, "442": 91,
                      "424": 92, "244": 93, "4S4": 95, "S44": 96, "224": 97, "242": 98, "422": 99, "221": 100,
                      "212": 101, "122": 102,
                      "223": 103, "232": 104, "322": 105, "22S": 106, "2S2": 107, "S22": 108, "SS4": 109, "S4S": 110,
                      "4SS": 111, "SS1": 112, "S1S": 113,
                      "1SS": 114, "SS3": 115, "S3S": 116, "3SS": 117, "SS2": 118, "S2S": 119, "2SS": 120, "111": 121,
                      "444": 122, "222": 123, "333": 124, "SSS": 125, "44S": 126, "314": 127}

suits_keys = list(unique_perms_suits.keys())


def transform_inputs(obs_dict, obs_tensor, prev_action, current_player):
    obs_keys = list(obs_dict.keys())

    own_cols = []
    own_suits = []
    col_str = ""
    suit_str = ""
    own_cols.append(obs_keys[0])
    own_cols.append(obs_keys[1])
    own_cols.append(obs_keys[2])
    own_suits.append(obs_keys[3])
    own_suits.append(obs_keys[4])
    own_suits.append(obs_keys[5])

    for i in own_cols:
        col_str += i[1]

    for j in own_suits:
        suit_str += j[0]



    if col_str not in cols_keys:
        own_c = [0]
    else:
        own_c = unique_perms_cols.get(col_str)
        own_c = [own_c]

    if suit_str not in suits_keys:
        own_s = [0]
    else:
        own_s = unique_perms_suits.get(suit_str)
        own_s = [own_s]

    obs_dict_list = list(obs_dict.values())
    th_1 = [0]
    th_2 = [0]
    th_3 = [0]
    f_1 = [0]
    f_2 = [0]
    f_3 = [0]
    f_4 = [0]

    if len(obs_dict_list) == 9:
        f_1 = [obs_dict_list[5]]
        f_2 = [obs_dict_list[6]]
        f_3 = [obs_dict_list[7]]
        f_4 = [0]

        th_1 = [0]
        th_2 = [0]
        th_3 = [0]

    elif len(obs_dict_list) == 10:
        f_1 = [obs_dict_list[6]]
        f_2 = [obs_dict_list[7]]
        f_3 = [obs_dict_list[8]]
        f_4 = [obs_dict_list[9]]
        th_1 = [0]
        th_2 = [0]
        th_3 = [0]

    elif len(obs_dict_list) == 11:
        f_1 = [obs_dict_list[7]]
        f_2 = [obs_dict_list[8]]
        f_3 = [obs_dict_list[9]]
        f_4 = [obs_dict_list[10]]
        th_1 = [obs_dict_list[6]]
        th_2 = [0]
        th_3 = [0]

    elif len(obs_dict_list) == 12:
        f_1 = [obs_dict_list[8]]
        f_2 = [obs_dict_list[9]]
        f_3 = [obs_dict_list[10]]
        f_4 = [obs_dict_list[11]]
        th_1 = [obs_dict_list[6]]
        th_2 = [obs_dict_list[7]]
        th_3 = [0]

    elif len(obs_dict_list) == 13:
        f_1 = [obs_dict_list[9]]
        f_2 = [obs_dict_list[10]]
        f_3 = [obs_dict_list[11]]
        f_4 = [obs_dict_list[12]]
        th_1 = [obs_dict_list[6]]
        th_2 = [obs_dict_list[7]]
        th_3 = [obs_dict_list[8]]

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

    return own_c, own_s, th_1, th_2, th_3, f_1, f_2, f_3, f_4, i_t, lives, act, cp
