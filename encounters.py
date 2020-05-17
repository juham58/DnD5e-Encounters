import numpy as np
import pickle


class EncounterBuilder:
    def __init__(self):
        self.players = []
        self.monsters = []
        self.party_thresholds = []
        self.xp_thresholds = pickle.load(open("xp_thresholds", "rb"))
        self.xp_monsters = pickle.load(open("xp_monsters", "rb"))
        print("init")

    def add_player(self, player_lvl):
        self.players.append(player_lvl)

    def add_monster(self, monster_cr):
        self.monsters.append(monster_cr)

    def set_party_thresholds(self):
        easy, medium, hard, deadly = 0, 0, 0, 0
        for i in self.players:
                easy += self.xp_thresholds[str(i)][0]
                medium += self.xp_thresholds[str(i)][1]
                hard += self.xp_thresholds[str(i)][2]
                deadly += self.xp_thresholds[str(i)][3]
        self.party_threshold = [easy, medium, hard, deadly]

    def set_monsters_xp:
        pass

    def get_difficulty(self):
        pass

test = EncounterBuilder()
test.add_player(1)
test.add_player(1)
test.set_party_threshold("D")
print(test.party_threshold)
print(test.players)
