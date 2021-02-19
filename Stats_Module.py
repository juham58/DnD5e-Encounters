import pickle
from pathlib import Path

class MainStats():
    def __init__(self):
        self.avg_attack_dmg = 0
        self.name = ""
        self.ac = 10
        self.dc = 10
        self.hp = 25
        self.ini_mod = 0
        self.attack_mod = 0
        self.is_monster = True
        self.is_frontliner = True

    def add_avg_dmg(self, x, y, z):
        self.avg_attack_dmg += round(x*((y+1)/2)+z)

    def set_main_stats(self, name, ac=10, hp=25, dc=10, ini_mod=0, attack_mod=0, is_monster=True, is_frontliner=True):
        self.name = name
        self.ac = ac
        self.hp = hp
        self.dc = dc
        self.ini_mod = ini_mod
        self.attack_mod = attack_mod
        self.is_monster = is_monster
        self.is_frontliner = is_frontliner
    
    def save_main_stats(self):
        dict = {self.name: {
                "avg_attack_dmg": self.avg_attack_dmg, 
                "ac": self.ac, 
                "dc": self.dc, 
                "hp": self.hp,
                "ini_mod": self.ini_mod,
                "attack_mod": self.attack_mod,
                "is_monster": self.is_monster,
                "is_frontliner": self.is_frontliner}}
        pickle.dump(dict, open(Path.cwd()/"data"/"{}_{}".format("stats", self.name), "w+b"))

test = MainStats()
test.set_main_stats("Goblin", ac=15, hp=7, attack_mod=4)
test.add_avg_dmg(1, 6, 2)
test.save_main_stats()