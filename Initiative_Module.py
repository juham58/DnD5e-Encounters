import random
import pickle
from pathlib import Path

class Initiative_Module():
    def __init__(self):
        self.combatants_stats = {}
        self.combatants_hp = {}
        self.combatants_names = []
        self.players_names = []
        self.monsters_names = []
        self.ini_order = {}
        self.player_deaths = 0
        self.verbose = True

    def import_stats(self, name):
        stats = pickle.load(open(Path.cwd()/"data"/"stats_{}".format(name), "rb"))
        self.combatants_stats[name] = stats[name]
        self.combatants_hp[name] = stats[name]["hp"]
        self.combatants_names.append(name)

    def import_group(self, base_name, quantity):
        stats = pickle.load(open(Path.cwd()/"data"/"stats_{}".format(base_name), "rb"))
        for n in range(quantity):
            new_name = "{}_{}".format(base_name, n+1)
            new_dict = stats[base_name]
            self.combatants_stats[new_name] = new_dict
            self.combatants_hp[new_name] = new_dict["hp"]
            self.combatants_names.append(new_name)

    def import_players(self, list_of_players):
        for name in list_of_players:
            self.import_stats(name)

    def d20(self, adv=False, dis=False):
        if adv is False and dis is False:
            return random.randint(1, 20)

        if adv is True and dis is True:
            return random.randint(1, 20)
        
        if adv is True and dis is False:
            roll_1 = random.randint(1, 20)
            roll_2 = random.randint(1, 20)
            if roll_1 >= roll_2:
                return roll_1
            if roll_1 < roll_2:
                return roll_2
        
        if adv is False and dis is True:
            roll_1 = random.randint(1, 20)
            roll_2 = random.randint(1, 20)
            if roll_1 >= roll_2:
                return roll_2
            if roll_1 < roll_2:
                return roll_1

    def roll_ini(self):
        temp_dict = {}
        for name in self.combatants_names:
            temp_dict[name] = self.d20()+self.combatants_stats[name]["ini_mod"]
        self.ini_order = list(dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)).keys())

    def separate_players_vs_monsters(self):
        for name in self.combatants_names:
            if self.combatants_stats[name]["is_monster"] is True:
                self.monsters_names.append(name)
            else:
                self.players_names.append(name)

    def attack(self, attacker_name, target_name, adv=False, dis=False):
        if self.combatants_stats[attacker_name]["combat_stats"]["advantage_on_attack"] is True or self.combatants_stats[target_name]["combat_stats"]["advantage_if_attacked"] is True:
            adv = True
        if self.combatants_stats[attacker_name]["combat_stats"]["disadvantage_on_attack"] is True or self.combatants_stats[target_name]["combat_stats"]["disadvantage_if_attacked"] is True:
            dis = True
        attack_roll = self.d20(adv=adv, dis=dis)+self.combatants_stats[attacker_name]["attack_mod"]
        straight_roll = attack_roll-self.combatants_stats[attacker_name]["attack_mod"]
        if target_name is None:
            if self.verbose is True:
                print("There is no one to attack.")
        else:
            if straight_roll == 20:
                self.combatants_hp[target_name] -= 2*self.combatants_stats[attacker_name]["avg_attack_dmg"]
                if self.verbose is True:
                    print(attacker_name, "CRITS with", attack_roll, "and does:", 2*self.combatants_stats[attacker_name]["avg_attack_dmg"], " damage!")

            if attack_roll >= self.combatants_stats[target_name]["ac"] and straight_roll != 20:
                self.combatants_hp[target_name] -= self.combatants_stats[attacker_name]["avg_attack_dmg"]
                if self.verbose is True:
                    print(attacker_name, "hits with", attack_roll, "and does:", self.combatants_stats[attacker_name]["avg_attack_dmg"], " damage!")
            else:
                if self.verbose is True:
                    print(attacker_name, "misses.")

    def heal(self):
        pass

    def set_target(self, attacker_name):
        try:
            if self.combatants_stats[attacker_name]["is_monster"] is True:
                return random.choice(self.players_names)

            else:
                return random.choice(self.monsters_names)
        except IndexError:
            return None

    def death(self, name):
        if self.combatants_stats[name]["is_monster"] is True:
            self.monsters_names.remove(name)
            self.ini_order.remove(name)

        else:
            self.players_names.remove(name)
            self.ini_order.remove(name)
            self.player_deaths += 1

    def check_for_death(self):
        if any(v <= 0 for v in self.combatants_hp.values()):
            dead_list = []
            for name in self.combatants_hp:
                if self.combatants_hp[name] <= 0:
                    self.death(name)
                    dead_list.append(name)
            for name in dead_list:
                if self.verbose is True:
                    print(name, " dies.")
                del self.combatants_hp[name]

    def player_downed(self):
        pass

    def dc_check(self, dc, stat, combatant_name):
        pass

    def set_condition(self, combatant_name, condition_name):
        if condition_name == "Blinded":
            pass
        if condition_name == "Charmed":
            pass
        if condition_name == "Deafened":
            pass
        if condition_name == "Frightened":
            pass
        if condition_name == "Grappled":
            pass
        if condition_name == "Incapacited":
            pass
        if condition_name == "Invisible":
            pass
        if condition_name == "Paralyzed":
            pass
        if condition_name == "Petrified":
            pass
        if condition_name == "Poisoned":
            pass
        if condition_name == "Prone":
            pass
        if condition_name == "Restrained":
            pass
        if condition_name == "Stunned":
            pass
        if condition_name == "Unconscious":
            pass


    def combat(self, verbose=True):
        rounds = 1
        self.roll_ini()
        self.separate_players_vs_monsters()
        self.verbose = verbose
        while len(self.players_names) != 0 and len(self.monsters_names) != 0:
            for attacker_name in self.ini_order:
                for _ in range(self.combatants_stats[attacker_name]["number_of_attacks"]):
                    target = self.set_target(attacker_name)
                    self.attack(attacker_name, target)
                    self.check_for_death()
                    #print("\n Combatants HP:", self.combatants_hp)
                    if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                        break
            rounds += 1
        if self.verbose is True:
            print("Combat ended")
        if len(self.players_names) == 0:
            if self.verbose is True:
                print("The players were killed.")
            return (0, self.player_deaths)
        else:
            if self.verbose is True:
                print("The monsters were killed.")
            return (1, self.player_deaths)
                



# À FAIRE:
# Besoin d'une manière de décider qui est attaqué (Check: random pour l'instant)
# Besoin d'une manière de distinguer les frontliners (facultatif)
# Faire l'algorithme de simulation de combat (check)
# Gérer les death saves
# Gérer le healing
# Gérer les debuffs
# Simuler des stratégies
# Retirer les combatants morts (check)
# Actually rouler les dés (enregistrer des tuples dans le dictionnaire)
