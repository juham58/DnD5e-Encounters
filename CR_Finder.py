import pickle
from pathlib import Path


class CR_Finder:
    def __init__(self):
        self.ac = 10
        self.hp = 10
        self.atk_bonus = 3
        self.dmg = 0
        self.save_dc = 13
        self.def_cr = 0
        self.off_cr = 0
        self.avg_dice_list = []
        self.resistances = False
        self.immunities = False
        self.tier = 1
        self.cr_hp = pickle.load(open(Path.cwd()/"data"/"cr_hp", "rb"))
        self.dmg_per_round = pickle.load(open(Path.cwd()/"data"/"dmg_per_round", "rb"))
        self.monster_stats_by_cr = pickle.load(open(Path.cwd()/"data"/"monster_stats_by_cr", "rb"))
        self.cr_list = pickle.load(open(Path.cwd()/"data"/"cr_list", "rb"))

    def avg_dice_collector(self):
        if len(self.avg_dice_list) == 0:
            self.dmg = 0
            return self.dmg
        self.dmg = round(sum(self.avg_dice_list))
        print("Monster's average damage per round with 100% hit rate:", self.dmg)

    def avg_dice(self, x, y, z):
        return self.avg_dice_list.append(x*((y+1)/2)+z)

    def set_tier(self, tier):
        self.tier = tier

    def set_resistances(self, resistances):
        self.resistances = resistances

    def set_immunities(self, immunities):
        self.immunities = immunities

    def cr_from_hp(self, hp):
        if self.resistances is True:
            if self.tier == 1:
                hp = round(2*hp)
            if self.tier == 2:
                hp = round(1.5*hp)
            if self.tier == 3:
                hp = round(1.25*hp)
            if self.tier == 4:
                pass

        if self.immunities is True and self.resistances is False:
            if self.tier == 1:
                hp = round(2*hp)
            if self.tier == 2:
                hp = round(2*hp)
            if self.tier == 3:
                hp = round(1.5*hp)
            if self.tier == 4:
                hp = round(1.25*hp)

        self.def_cr = self.cr_hp[hp]
        print("def_cr from hp:", self.def_cr)
        return self.def_cr

    def cr_from_ac(self, ac):
        sugg_ac = self.monster_stats_by_cr[str(self.def_cr)][0]
        cr_index = self.cr_list.index(self.def_cr)
        if abs(sugg_ac - ac) == 0 or abs(sugg_ac - ac) == 1:
            return self.def_cr

        adj_index = cr_index - (sugg_ac - ac)//2
        if adj_index <= 0:
            adj_index = 0
        self.def_cr = self.cr_list[adj_index]
        print("def_cr from ac:", self.def_cr)
        return self.def_cr

    def cr_from_dmg(self):
        self.off_cr = self.dmg_per_round[self.dmg]
        print("off_cr from dmg:", self.off_cr)
        return self.off_cr

    def cr_from_atk_bonus(self, atk_bonus):
        sugg_atk = self.monster_stats_by_cr[str(self.off_cr)][1]
        cr_index = self.cr_list.index(self.off_cr)
        if abs(sugg_atk - atk_bonus) == 0 or abs(sugg_atk - atk_bonus) == 1:
            print("off_cr from atk bonus:", self.off_cr)
            return self.off_cr

        adj_index = cr_index - (sugg_atk - atk_bonus)//2
        if adj_index <= 0:
            adj_index = 0
        self.off_cr = self.cr_list[adj_index]
        print("off_cr from atk bonus:", self.off_cr)
        return self.off_cr

    def cr_from_save_dc(self, save_dc):
        sugg_dc = self.monster_stats_by_cr[str(self.off_cr)][2]
        cr_index = self.cr_list.index(self.off_cr)
        if abs(sugg_dc - save_dc) == 0 or abs(sugg_dc - save_dc) == 1:
            print("off_cr from save dc:", self.off_cr)
            return self.off_cr

        adj_index = cr_index - (sugg_dc - save_dc)//2
        if adj_index <= 0:
            adj_index = 0
        self.off_cr = self.cr_list[adj_index]
        print("off_cr from save dc:", self.off_cr)
        return self.off_cr

    def get_final_cr(self):
        print("\n-------", "\nDefensive challenge rating:", self.def_cr, "\nOffensive challenge rating:", self.off_cr, "\nAdjusted challenge rating:", round((self.off_cr+self.def_cr)/2), "\n-------\n")
        return round((self.off_cr+self.def_cr)/2)
