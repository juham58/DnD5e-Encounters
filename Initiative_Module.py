import random
import pickle
from pathlib import Path

class Initiative_Module():
    def __init__(self):
        self.combatants_stats = {}
        self.combatants_names = []
        self.ini_order = {}

    def import_stats(self, name):
        stats = pickle.load(open(Path.cwd()/"data"/"stats_{}".format(name), "rb"))
        self.combatants_stats[name] = stats[name]
        self.combatants_names.append(name)

    def import_group(self, base_name, quantity):
        stats = pickle.load(open(Path.cwd()/"data"/"stats_{}".format(base_name), "rb"))
        for n in range(quantity):
            new_name = "{}_{}".format(base_name, n+1)
            new_dict = stats[base_name]
            self.combatants_stats[new_name] = new_dict
            self.combatants_names.append(new_name)

    def roll_ini(self):
        temp_dict = {}
        for name in self.combatants_names:
            temp_dict[name] = random.randint(1, 20)+self.combatants_stats[name]["ini_mod"]
        self.ini_order = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True))
        print(self.ini_order)

    def attack(self, attacker_name, target_name)


# À FAIRE:
# Besoin d'une manière de séparer les monstres des joueurs et les frontliners
# Besoin d'une manière de décider qui est attaqué
# Faire l'algorithme de simulation de combat



    
test = Initiative_Module()
test.import_group("Goblin", 8)
test.roll_ini()
