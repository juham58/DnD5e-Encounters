import dill as pickle
from pathlib import Path
import numpy as np


xp_thresholds = {"1": np.array([25, 50, 75, 100]),
                 "2": np.array([50, 100, 150, 200]),
                 "3": np.array([75, 150, 225, 400]),
                 "4": np.array([125, 250, 375, 500]),
                 "5": np.array([250, 500, 750, 1100]),
                 "6": np.array([300, 600, 900, 1400]),
                 "7": np.array([350, 750, 1100, 1700]),
                 "8": np.array([450, 900, 1400, 2100]),
                 "9": np.array([550, 1100, 1600, 2400]),
                 "10": np.array([600, 1200, 1900, 2800]),
                 "11": np.array([800, 1600, 2400, 3600]),
                 "12": np.array([1000, 2000, 3000, 4500]),
                 "13": np.array([1100, 2200, 3400, 5100]),
                 "14": np.array([1250, 2500, 3800, 5700]),
                 "15": np.array([1400, 2800, 4300, 6400]),
                 "16": np.array([1600, 3200, 4800, 7200]),
                 "17": np.array([2000, 3900, 5900, 8800]),
                 "18": np.array([2100, 4200, 6300, 9500]),
                 "19": np.array([2400, 4900, 7300, 10900]),
                 "20": np.array([2800, 5700, 8500, 12700])}


xp_monsters = {"0": 10, str(1/8): 25, str(1/4): 50, str(1/2): 100, "1": 200, "2": 450,
               "3": 700, "4": 1100, "5": 1800, "6": 2300, "7": 2900, "8": 3900,
               "9": 5000, "10": 5900, "11": 7200, "12": 8400, "13": 10000,
               "14": 11500, "15": 13000, "16": 15000, "17": 18000, "18": 20000,
               "19": 22000, "20": 25000, "21": 33000, "22": 41000, "23": 50000,
               "24": 62000, "25": 75000, "26": 90000, "27": 105000, "28": 120000,
               "29": 135000, "30": 155000}


def cr_hp():
    cr_hp_list = []
    for i in range(850):
        if 1 <= i+1 <= 6:
            cr_hp_list.append(0)
        if 7 <= i+1 <= 35:
            cr_hp_list.append(1/8)
        if 36 <= i+1 <= 49:
            cr_hp_list.append(1/4)
        if 50 <= i+1 <= 70:
            cr_hp_list.append(1/2)
        if 71 <= i+1 <= 85:
            cr_hp_list.append(1)
        if 86 <= i+1 <= 100:
            cr_hp_list.append(2)
        if 101 <= i+1 <= 115:
            cr_hp_list.append(3)
        if 116 <= i+1 <= 130:
            cr_hp_list.append(4)
        if 131 <= i+1 <= 145:
            cr_hp_list.append(5)
        if 146 <= i+1 <= 160:
            cr_hp_list.append(6)
        if 161 <= i+1 <= 175:
            cr_hp_list.append(7)
        if 176 <= i+1 <= 190:
            cr_hp_list.append(8)
        if 191 <= i+1 <= 205:
            cr_hp_list.append(9)
        if 206 <= i+1 <= 220:
            cr_hp_list.append(10)
        if 221 <= i+1 <= 235:
            cr_hp_list.append(11)
        if 236 <= i+1 <= 250:
            cr_hp_list.append(12)
        if 251 <= i+1 <= 265:
            cr_hp_list.append(13)
        if 266 <= i+1 <= 280:
            cr_hp_list.append(14)
        if 281 <= i+1 <= 295:
            cr_hp_list.append(15)
        if 296 <= i+1 <= 310:
            cr_hp_list.append(16)
        if 311 <= i+1 <= 325:
            cr_hp_list.append(17)
        if 326 <= i+1 <= 340:
            cr_hp_list.append(18)
        if 341 <= i+1 <= 355:
            cr_hp_list.append(19)
        if 356 <= i+1 <= 400:
            cr_hp_list.append(20)
        if 401 <= i+1 <= 445:
            cr_hp_list.append(21)
        if 446 <= i+1 <= 490:
            cr_hp_list.append(22)
        if 491 <= i+1 <= 535:
            cr_hp_list.append(23)
        if 536 <= i+1 <= 580:
            cr_hp_list.append(24)
        if 581 <= i+1 <= 625:
            cr_hp_list.append(25)
        if 626 <= i+1 <= 670:
            cr_hp_list.append(26)
        if 671 <= i+1 <= 715:
            cr_hp_list.append(27)
        if 716 <= i+1 <= 760:
            cr_hp_list.append(28)
        if 761 <= i+1 <= 805:
            cr_hp_list.append(29)
        if 806 <= i+1 <= 850:
            cr_hp_list.append(30)
    return cr_hp_list


def dmg_per_round():
    dmg_per_round_list = []
    for i in range(320):
        if 0 <= i+1 <= 1:
            dmg_per_round_list.append(0)
        if 2 <= i+1 <= 3:
            dmg_per_round_list.append(1/8)
        if 4 <= i+1 <= 5:
            dmg_per_round_list.append(1/4)
        if 6 <= i+1 <= 8:
            dmg_per_round_list.append(1/2)
        if 9 <= i+1 <= 14:
            dmg_per_round_list.append(1)
        if 15 <= i+1 <= 20:
            dmg_per_round_list.append(2)
        if 21 <= i+1 <= 26:
            dmg_per_round_list.append(3)
        if 27 <= i+1 <= 32:
            dmg_per_round_list.append(4)
        if 33 <= i+1 <= 38:
            dmg_per_round_list.append(5)
        if 39 <= i+1 <= 44:
            dmg_per_round_list.append(6)
        if 45 <= i+1 <= 50:
            dmg_per_round_list.append(7)
        if 51 <= i+1 <= 56:
            dmg_per_round_list.append(8)
        if 57 <= i+1 <= 62:
            dmg_per_round_list.append(9)
        if 63 <= i+1 <= 68:
            dmg_per_round_list.append(10)
        if 69 <= i+1 <= 74:
            dmg_per_round_list.append(11)
        if 75 <= i+1 <= 80:
            dmg_per_round_list.append(12)
        if 81 <= i+1 <= 86:
            dmg_per_round_list.append(13)
        if 87 <= i+1 <= 92:
            dmg_per_round_list.append(14)
        if 93 <= i+1 <= 98:
            dmg_per_round_list.append(15)
        if 99 <= i+1 <= 104:
            dmg_per_round_list.append(16)
        if 105 <= i+1 <= 110:
            dmg_per_round_list.append(17)
        if 111 <= i+1 <= 116:
            dmg_per_round_list.append(18)
        if 117 <= i+1 <= 122:
            dmg_per_round_list.append(19)
        if 123 <= i+1 <= 140:
            dmg_per_round_list.append(20)
        if 141 <= i+1 <= 158:
            dmg_per_round_list.append(21)
        if 159 <= i+1 <= 176:
            dmg_per_round_list.append(22)
        if 177 <= i+1 <= 194:
            dmg_per_round_list.append(23)
        if 195 <= i+1 <= 212:
            dmg_per_round_list.append(24)
        if 213 <= i+1 <= 230:
            dmg_per_round_list.append(25)
        if 231 <= i+1 <= 248:
            dmg_per_round_list.append(26)
        if 249 <= i+1 <= 266:
            dmg_per_round_list.append(27)
        if 267 <= i+1 <= 284:
            dmg_per_round_list.append(28)
        if 285 <= i+1 <= 302:
            dmg_per_round_list.append(29)
        if 303 <= i+1 <= 320:
            dmg_per_round_list.append(30)
    return dmg_per_round_list


def cr_list():
    cr_liste = [0, 1/8, 1/4, 1/2]
    for i in range(30):
        cr_liste.append(i+1)
    print(cr_liste)
    return cr_liste


monster_stats_by_cr = {str(0): [13, 3, 13], str(1/8): [13, 3, 13], str(1/4): [13, 3, 13],
                       str(1/2): [13, 3, 13], str(1): [13, 3, 13], str(2): [13, 3, 13],
                       str(3): [13, 4, 13], str(4): [14, 5, 14], str(5): [15, 6, 15],
                       str(6): [15, 6, 15], str(7): [15, 6, 15], str(8): [16, 7, 16],
                       str(9): [16, 7, 16], str(10): [17, 7, 16], str(11): [17, 8, 17],
                       str(12): [17, 8, 17], str(13): [18, 8, 18], str(14): [18, 8, 18],
                       str(15): [18, 8, 18], str(16): [18, 9, 18], str(17): [19, 10, 19],
                       str(18): [19, 10, 19], str(19): [19, 10, 19], str(20): [19, 10, 19],
                       str(21): [19, 11, 20], str(22): [19, 11, 20], str(23): [19, 11, 20],
                       str(24): [19, 12, 21], str(25): [19, 12, 21], str(26): [19, 12, 21],
                       str(27): [19, 13, 22], str(28): [19, 13, 22], str(29): [19, 13, 22],
                       str(30): [19, 14, 23]}


pickle.dump(xp_thresholds, open(Path.cwd()/"data"/"xp_thresholds", "w+b"))
pickle.dump(xp_monsters, open(Path.cwd()/"data"/"xp_monsters", "w+b"))
pickle.dump(cr_hp(), open(Path.cwd()/"data"/"cr_hp", "w+b"))
pickle.dump(dmg_per_round(), open(Path.cwd()/"data"/"dmg_per_round", "w+b"))
pickle.dump(monster_stats_by_cr, open(Path.cwd()/"data"/"monster_stats_by_cr", "w+b"))
pickle.dump(cr_list(), open(Path.cwd()/"data"/"cr_list", "w+b"))
