import dill as pickle
from pathlib import Path


class EncounterBuilder:
    def __init__(self):
        self.players = []
        self.monsters = []
        self.party_thresholds = []
        self.total_monsters_xp = 0
        self.party_threshold = []
        self.xp_thresholds = pickle.load(open(Path.cwd()/"data"/"xp_thresholds", "rb"))
        self.xp_monsters = pickle.load(open(Path.cwd()/"data"/"xp_monsters", "rb"))

    def add_player(self, player_lvl):
        self.players.append(player_lvl)

    def remove_player(self, player_lvl):
        self.players.remove(player_lvl)

    def add_party(self, players_lvl, players_number):
        for _ in range(players_number):
            self.add_player(players_lvl)

    def add_monster(self, monster_cr):
        self.monsters.append(monster_cr)

    def remove_monster(self, monster_cr):
        self.monsters.remove(monster_cr)

    def add_monsters_group(self, monster_cr, monsters_number):
        for _ in range(monsters_number):
            self.add_monster(monster_cr)

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
