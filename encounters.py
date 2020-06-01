import pickle


class EncounterBuilder:
    def __init__(self):
        self.players = []
        self.monsters = []
        self.party_thresholds = []
        self.total_monsters_xp = 0
        self.party_threshold = []
        self.xp_thresholds = pickle.load(open("xp_thresholds", "rb"))
        self.xp_monsters = pickle.load(open("xp_monsters", "rb"))

    def add_player(self, player_lvl):
        self.players.append(player_lvl)

    def remove_player(self, player_lvl):
        self.players.remove(player_lvl)

    def add_party(self, players_lvl, players_number):
        for i in range(players_number):
            self.add_player(players_lvl)

    def add_monster(self, monster_cr):
        self.monsters.append(monster_cr)

    def remove_monster(self, monster_cr):
        self.monsters.remove(monster_cr)

    def set_party_thresholds(self):
        easy, medium, hard, deadly = 0, 0, 0, 0
        for i in self.players:
            easy += self.xp_thresholds[str(i)][0]
            medium += self.xp_thresholds[str(i)][1]
            hard += self.xp_thresholds[str(i)][2]
            deadly += self.xp_thresholds[str(i)][3]
        self.party_threshold = [easy, medium, hard, deadly]

    def set_monsters_xp(self):
        self.total_monsters_xp = 0
        for i in self.monsters:
            self.total_monsters_xp += self.xp_monsters[str(i)]

        if len(self.players) < 3:
            if len(self.monsters) == 0:
                print("Error: add monster before setting monsters xp")
            if len(self.monsters) == 1:
                self.total_monsters_xp = self.total_monsters_xp*1.5
            if len(self.monsters) == 2:
                self.total_monsters_xp = self.total_monsters_xp*2
            if 3 <= len(self.monsters) <= 6:
                self.total_monsters_xp = self.total_monsters_xp*2.5
            if 7 <= len(self.monsters) <= 10:
                self.total_monsters_xp = self.total_monsters_xp*3
            if 11 <= len(self.monsters) <= 14:
                self.total_monsters_xp = self.total_monsters_xp*4
            if len(self.monsters) >= 15:
                self.total_monsters_xp = self.total_monsters_xp*5

        if 3 <= len(self.players) <= 5:
            if len(self.monsters) == 0:
                print("Error: add monster before setting monsters xp")
            if len(self.monsters) == 1:
                self.total_monsters_xp = self.total_monsters_xp*1
            if len(self.monsters) == 2:
                self.total_monsters_xp = self.total_monsters_xp*1.5
            if 3 <= len(self.monsters) <= 6:
                self.total_monsters_xp = self.total_monsters_xp*2
            if 7 <= len(self.monsters) <= 10:
                self.total_monsters_xp = self.total_monsters_xp*2.5
            if 11 <= len(self.monsters) <= 14:
                self.total_monsters_xp = self.total_monsters_xp*3
            if len(self.monsters) >= 15:
                self.total_monsters_xp = self.total_monsters_xp*4

        if len(self.players) >= 6:
            if len(self.monsters) == 0:
                print("Error: add monster before setting monsters xp")
            if len(self.monsters) == 1:
                self.total_monsters_xp = self.total_monsters_xp*0.5
            if len(self.monsters) == 2:
                self.total_monsters_xp = self.total_monsters_xp*1
            if 3 <= len(self.monsters) <= 6:
                self.total_monsters_xp = self.total_monsters_xp*1.5
            if 7 <= len(self.monsters) <= 10:
                self.total_monsters_xp = self.total_monsters_xp*2
            if 11 <= len(self.monsters) <= 14:
                self.total_monsters_xp = self.total_monsters_xp*2.5
            if len(self.monsters) >= 15:
                self.total_monsters_xp = self.total_monsters_xp*3

    def get_difficulty(self):
        self.set_party_thresholds()
        self.set_monsters_xp()
        if 0 < self.total_monsters_xp < self.party_threshold[0]:
            print("Encounter difficulty: Very Easy")
        if self.party_threshold[0] <= self.total_monsters_xp < self.party_threshold[1]:
            print("Encounter difficulty: Easy")
        if self.party_threshold[1] <= self.total_monsters_xp < self.party_threshold[2]:
            print("Encounter difficulty: Medium")
        if self.party_threshold[2] <= self.total_monsters_xp < self.party_threshold[3]:
            print("Encounter difficulty: Hard")
        if self.party_threshold[3] <= self.total_monsters_xp:
            print("Encounter difficulty: Deadly")


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
        self.cr_hp = pickle.load(open("cr_hp", "rb"))
        self.dmg_per_round = pickle.load(open("dmg_per_round", "rb"))
        self.monster_stats_by_cr = pickle.load(open("monster_stats_by_cr", "rb"))
        self.cr_list = pickle.load(open("cr_list", "rb"))

    def avg_dice_collector(self):
        if len(self.avg_dice_list) == 0:
            self.dmg = 0
            return self.dmg
        self.dmg = round(sum(self.avg_dice_list)/len(self.avg_dice_list))

    def avg_dice(self, x, y, z):
        return self.avg_dice_list.append(x*((y+1)/2)+z)

    def cr_from_hp(self, hp):
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
            print("off_cr from atk bonus:", self.off_cr)
            return self.off_cr

        adj_index = cr_index - (sugg_dc - save_dc)//2
        if adj_index <= 0:
            adj_index = 0
        self.off_cr = self.cr_list[adj_index]
        print("off_cr from save dc:", self.off_cr)
        return self.off_cr

    def get_final_cr(self):
        print("\n-------", "\nDefensive challenge rating:", self.def_cr, "\nOffensive challenge rating:", self.off_cr,"\nAdjusted challenge rating:", round((self.off_cr+self.def_cr)/2), "\n-------\n")
        return round((self.off_cr+self.def_cr)/2)



def find_cr_atk_bonus(ac=10, hp=10, atk_bonus=3):
    finder = CR_Finder()
    finder.avg_dice(3, 6, 2)
    finder.avg_dice_collector()
    finder.cr_from_hp(hp)
    finder.cr_from_ac(ac)
    finder.cr_from_dmg()
    finder.cr_from_atk_bonus(atk_bonus)
    return finder.get_final_cr()


def find_cr_save_dc(ac=10, hp=10, save_dc=10):
    finder = CR_Finder()
    finder.avg_dice(3, 6, 2)
    finder.avg_dice_collector()
    finder.cr_from_hp(hp)
    finder.cr_from_ac(ac)
    finder.cr_from_dmg()
    finder.cr_from_atk_bonus(save_dc)
    return finder.get_final_cr()



test = EncounterBuilder()
test.add_party(1, 6)
test.add_monster(find_cr_atk_bonus(ac=18, hp=100, atk_bonus=4))
test.get_difficulty()
