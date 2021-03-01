import random
import pickle
from pathlib import Path
import logging

logging.basicConfig(filename='Infinite loop debug.log', level=logging.INFO)

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
        self.conditions_list = ["Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious"]

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

    def import_monsters(self, list_of_monsters):
        for name in list_of_monsters:
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

    def roll_dice(self, tuple):
        result = 0
        for _ in range(tuple[0]):
            result += random.randint(1, tuple[1])
        result += tuple[2]
        return result

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

    def dc_attack(self, attacker_name, target_name, attack):
        dice_rolls = attack["dice_rolls"]
        dc_type = attack["dc_type"]
        dc = self.combatants_stats[attacker_name]["dc"]
        dc_result = self.dc_check(target_name, dc, dc_type)
        if attack["condition"] != "":
            if dc_result is False:
                self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
        damage = 0
        for dice_roll in dice_rolls:
            damage += self.roll_dice(dice_roll)
        if dc_result is False:
            self.combatants_hp[target_name] -= damage
            if self.verbose is True:
                print(target_name, "fails to meet DC of", dc, "and takes:", damage, " damage!")
        if dc_result is True and attack["if_save"] == "half":
            self.combatants_hp[target_name] -= round(damage/2)
            if self.verbose is True:
                print(target_name, "succeeds DC of", dc, "and takes:", round(damage/2), " damage! (half damage)")
        if dc_result is True and attack["if_save"] == "no_damage":
            if self.verbose is True:
                print(target_name, "succeeds to meet DC of", dc, "and takes no damage!")

    def attack(self, attacker_name, target_name, attack, adv=False, dis=False):
        if self.combatants_stats[attacker_name]["combat_stats"]["advantage_on_attack"] is True or self.combatants_stats[target_name]["combat_stats"]["advantage_if_attacked"] is True:
            adv = True
        if self.combatants_stats[attacker_name]["combat_stats"]["disadvantage_on_attack"] is True or self.combatants_stats[target_name]["combat_stats"]["disadvantage_if_attacked"] is True:
            dis = True
        attack_roll = self.d20(adv=adv, dis=dis)+self.combatants_stats[attacker_name]["attack_mod"]
        straight_roll = attack_roll-self.combatants_stats[attacker_name]["attack_mod"]
        conditions = self.combatants_stats[target_name]["combat_stats"]["conditions"]
        normal_damage = 0
        for dice_roll in attack["dice_rolls"]:
            normal_damage += self.roll_dice(dice_roll)
        crit_damage = 0
        for dice_roll in attack["dice_rolls"]:
            dice_roll = (2*dice_roll[0], dice_roll[1], dice_roll[2])
            crit_damage += self.roll_dice(dice_roll)
        #if target_name is None:
            #if self.verbose is True:
                #print("There is no one to attack.")
        if straight_roll == 20:
            if "Paralyzed" not in conditions and "Unconscious" not in conditions:
                self.combatants_hp[target_name] -= crit_damage
                if attack["condition"] != "":
                    if attack["auto_success"] is True:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                    else:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        if self.dc_check(target_name, dc, attack["dc_type"]) is False:
                            if attack["has_dc_effect_on_hit"] is True:
                                for dice_roll in attack["dc_effect_on_hit"]:
                                    crit_damage += self.roll_dice(dice_roll)
                            self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                if self.verbose is True:
                    print(attacker_name, "CRITS with", attack_roll, "and does:", crit_damage, " damage!")

        if attack_roll >= self.combatants_stats[target_name]["ac"] and straight_roll != 20:
            if "Paralyzed" not in conditions and "Unconscious" not in conditions:
                self.combatants_hp[target_name] -= normal_damage
                if attack["condition"] != "":
                    if attack["auto_success"] is True:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                    else:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        if self.dc_check(target_name, dc, attack["dc_type"]) is False:
                            if attack["has_dc_effect_on_hit"] is True:
                                for dice_roll in attack["dc_effect_on_hit"]:
                                    normal_damage += self.roll_dice(dice_roll)
                            self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                if self.verbose is True:
                    print(attacker_name, "hits with", attack_roll, "and does:", normal_damage, " damage!")

        if attack_roll >= self.combatants_stats[target_name]["ac"]:
            if "Paralyzed" in conditions or "Unconscious" in conditions:
                print(conditions)
                self.combatants_hp[target_name] -= crit_damage
                if attack["condition"] != "":
                    if attack["auto_success"] is True:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                    else:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        if self.dc_check(target_name, dc, attack["dc_type"]) is False:
                            if attack["has_dc_effect_on_hit"] is True:
                                for dice_roll in attack["dc_effect_on_hit"]:
                                    crit_damage += self.roll_dice(dice_roll)
                            self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                if self.verbose is True:
                    print(attacker_name, "CRITS on paralyzed or unconscious", target_name, "with", attack_roll, "and does:", crit_damage, " damage!")
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

    def dc_check(self, combatant_name, dc, stat, adv=False, dis=False):
        if stat == "str" and "Petrified" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            return False
        if stat == "dex" and "Petrified" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            return False
        if stat == "str" and "Stunned" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            return False
        if stat == "dex" and "Stunned" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            return False
        if stat == "str" and "Unconscious" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            return False
        if stat == "dex" and "Unconscious" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            return False
        if stat == "dex" and "Restrained" in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            dis=True
        save_bonus = self.combatants_stats[combatant_name]["saves"][stat]
        roll = self.d20(adv=adv, dis=dis)+save_bonus
        if roll >= dc:
            return True
        else:
            return False

    def condition_check(self, combatant_name, adv=False, dis=False):
        if len(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]) != 0:
            for condition in self.conditions_list:
                print("Condition:", condition)
                logging.info("Condition check: {}, combatant_name: {}".format(condition, combatant_name))
                if condition == "Prone":
                    self.remove_condition(combatant_name, condition)
                    continue
                if condition in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
                    logging.info("Condition check FOUND: {}, combatant_name: {}".format(condition, combatant_name))
                    print("conditions on {}:".format(combatant_name), self.combatants_stats[combatant_name]["combat_stats"]["conditions"])
                    logging.info("Conditions info list: {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"]))
                    index = self.combatants_stats[combatant_name]["combat_stats"]["conditions"].index(condition)
                    dc = self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index][1]
                    stat = self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index][2]
                    if self.dc_check(combatant_name, dc, stat, adv=adv, dis=dis) is True:
                        print("Condition save", condition, "Combatant name:", combatant_name)
                        logging.info("Condition save: {}, Combatant name: {}".format(condition, combatant_name))
                        self.remove_condition(combatant_name, condition)

    def remove_condition(self, combatant_name, condition_name):
        print("Condition removed:", condition_name, "comabatant name:", combatant_name)
        logging.info("Condition removed: {} Combatant name: {}".format(condition_name, combatant_name))
        logging.info("Conditions list (remove_condition before removal): {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]))
        if condition_name in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            self.combatants_stats[combatant_name]["combat_stats"]["conditions"].remove(condition_name)
            logging.info("Conditions list (remove_condition after removal): {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]))
            for index, condition in enumerate(self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"]):
                print(index, condition)
                logging.info("Index: {}, Condition: {}".format(index, condition))
                if condition[0] == condition_name:
                    print("condition at removed index:", self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index])
                    logging.info("Condition at removed index: {}, Condition to be removed: {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index], condition))
                    del self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index]
                    continue
            if condition_name == "Blinded":
                self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = False
                self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = False
            if condition_name == "Charmed":
                pass
            if condition_name == "Deafened":
                pass
            if condition_name == "Frightened":
                pass
            if condition_name == "Grappled":
                pass
            if condition_name == "Incapacitated":
                pass
            if condition_name == "Invisible":
                self.combatants_stats[combatant_name]["combat_stats"]["advantage_on_attack"] = False
                self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_if_attacked"] = False
            if condition_name == "Paralyzed":
                self.remove_condition(combatant_name, "Incapacitated")
                self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = False
            if condition_name == "Petrified":
                pass
            if condition_name == "Poisoned":
                self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = False
            if condition_name == "Prone":
                pass
            if condition_name == "Restrained":
                self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = False
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = False
            if condition_name == "Stunned":
                self.remove_condition(combatant_name, "Incapacitated")
                self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = False
            if condition_name == "Unconscious":
                self.remove_condition(combatant_name, "Incapacitated")
                self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = False
            if len(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]) != 0:
                for condition in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
                    for element in self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"]:
                        if condition == element[0] and condition != condition_name:
                            self.reset_condition(combatant_name, condition, element[1], element[2])

    def reset_condition(self, combatant_name, condition_name, dc, stat):
        print("Condition RESET:", condition_name, "comabatant name:", combatant_name, "dc:", dc, "stat:", stat)
        logging.info("Condition RESET: {}, Combatant name: {}".format(condition_name, combatant_name))
        if condition_name == "Blinded":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Charmed":
            pass
        if condition_name == "Deafened":
            pass
        if condition_name == "Frightened":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
        if condition_name == "Grappled":
            pass
        if condition_name == "Incapacitated":
            pass
        if condition_name == "Invisible":
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_on_attack"] = True
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_if_attacked"] = True
        if condition_name == "Paralyzed":
            self.reset_condition(combatant_name, "Incapacitated", dc, stat)
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Petrified":
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
            # resistance to all damage
        if condition_name == "Poisoned":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
        if condition_name == "Prone":
            # adv if attacked si attque melee et dis if attacked si attaque ranged
            pass
        if condition_name == "Restrained":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Stunned":
            self.reset_condition(combatant_name, "Incapacitated", dc, stat)
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Unconscious":
            self.reset_condition(combatant_name, "Incapacitated", dc, stat)
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True

    def set_condition(self, combatant_name, condition_name, dc, stat):
        print("Condition set:", condition_name, "comabatant name:", combatant_name, "dc:", dc, "stat:", stat)
        logging.info("Condition set: {}, Combatant name: {}".format(condition_name, combatant_name))
        self.combatants_stats[combatant_name]["combat_stats"]["conditions"].append(condition_name)
        self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"].append((condition_name, dc, stat))
        if condition_name == "Blinded":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Charmed":
            pass
        if condition_name == "Deafened":
            pass
        if condition_name == "Frightened":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
        if condition_name == "Grappled":
            pass
        if condition_name == "Incapacitated":
            pass
        if condition_name == "Invisible":
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_on_attack"] = True
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_if_attacked"] = True
        if condition_name == "Paralyzed":
            self.set_condition(combatant_name, "Incapacitated", dc, stat)
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Petrified":
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
            # resistance to all damage
        if condition_name == "Poisoned":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
        if condition_name == "Prone":
            # adv if attacked si attque melee et dis if attacked si attaque ranged
            pass
        if condition_name == "Restrained":
            self.combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = True
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Stunned":
            self.set_condition(combatant_name, "Incapacitated", dc, stat)
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True
        if condition_name == "Unconscious":
            self.set_condition(combatant_name, "Incapacitated", dc, stat)
            self.combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = True


    def combat(self, verbose=True):
        rounds = 1
        self.roll_ini()
        self.separate_players_vs_monsters()
        self.verbose = verbose
        while len(self.players_names) != 0 and len(self.monsters_names) != 0:
            if self.verbose is True:
                print("\n --- Round {} ---\n".format(rounds))
                logging.info("\n --- Round {} ---\n".format(rounds))
            for attacker_name in self.ini_order:
                for attack in self.combatants_stats[attacker_name]["actions"]:
                    print(attacker_name, attack["name"])
                    logging.info("{}, with {}".format(attacker_name, attack["name"]))
                    self.check_for_death()
                    if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                        break
                    if attack["has_attack_mod"] is True:
                        target = self.set_target(attacker_name)
                        #print("\nAttacker:", attacker_name, "Target:", target, "Attack name:", attack["name"])
                        self.attack(attacker_name, target, attack)
                        self.check_for_death()
                    if attack["has_dc"] is True:
                        target = self.set_target(attacker_name)
                        self.dc_attack(attacker_name, target, attack)
                        self.check_for_death()
                    if attack["aoe"] is True:
                        pass
                    #print("\n Combatants HP:", self.combatants_hp)
                    if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                        break
                self.condition_check(attacker_name)
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
                

# fix incapacitated et doublons de conditions

# À FAIRE:
# Gérer les debuffs (conditions)
# Actually rouler les dés (enregistrer des tuples dans le dictionnaire)
# Implémenter les aoe et les attaques différentes

# Besoin d'une manière de décider qui est attaqué (Check: random pour l'instant)
# Besoin d'une manière de distinguer les frontliners (facultatif)
# Gérer les death saves
# Gérer le healing
# Simuler des stratégies
