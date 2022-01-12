import random
import re
import pickle
import copy
from pathlib import Path
import logging
import d20
from d20 import dice

logging.basicConfig(filename='Debug.log', level=logging.INFO)

class Initiative_Module():
    def __init__(self, pythagore=False):
        self.combatants_stats = {}
        self.combatants_hp = {}
        self.combatants_names = []
        self.players_names = []
        self.monsters_names = []
        self.ini_order = {}
        self.legendary_monsters = []
        self.legend_actions_order = {}
        self.player_deaths = 0
        self.verbose = False
        self.conditions_list = ["Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious"]
        self.pythagore = pythagore

    def import_stats(self, name):
        stats = pickle.load(open(Path.cwd()/"data"/"stats_{}".format(name), "rb"))
        self.combatants_stats[name] = stats[name]
        self.combatants_hp[name] = stats[name]["max_hp"]
        self.combatants_names.append(name)
        if self.combatants_stats[name]["legend_actions"] != []:
            self.legendary_monsters.append(name)

    def import_group(self, base_name, quantity):
        stats = pickle.load(open(Path.cwd()/"data"/"stats_{}".format(base_name), "rb"))
        for n in range(quantity):
            new_name = "{}_{}".format(base_name, n+1)
            new_dict = stats[base_name]
            self.combatants_stats[new_name] = new_dict
            self.combatants_hp[new_name] = new_dict["max_hp"]
            self.combatants_names.append(new_name)
            if self.combatants_stats[new_name]["legend_actions"] != []:
                self.legendary_monsters.append(new_name)

    def import_players(self, list_of_players):
        for name in list_of_players:
            self.import_stats(name)

    def import_monsters(self, list_of_monsters):
        if len(list_of_monsters) > 0:
            for name in list_of_monsters:
                self.import_stats(name)

    def roll_d20(self, adv=False, dis=False):
        if adv is False and dis is False:
            return d20.roll("1d20").total

        if adv is True and dis is True:
            return d20.roll("1d20").total
        
        if adv is True and dis is False:
            return d20.roll("2d20kh1").total
        
        if adv is False and dis is True:
            return d20.roll("2d20kl1").total

    def roll_dice(self, dice_input):
        if type(dice_input) == tuple:
            string_input = "{}d{}+{}".format(dice_input[0], dice_input[1], dice_input[2])
            return d20.roll(string_input).total

        if type(dice_input) == str:
            return d20.roll(dice_input).total

        else:
            print("dice_input should be a tuple or a string")
    
    def calculate_crit_damage(self, dice_input):
        valeurs = re.findall(r"\d?\d?\d?\d(?=d)", dice_input)
        for n, membre in enumerate([(m.start(0), m.end(0)) for m in re.finditer(r"\d?\d?\d?\d(?=d)", dice_input)]):
            valeur_crit = str(2*int(valeurs[n]))
            dice_input = dice_input[:membre[0]] + dice_input[membre[0]:membre[1]].replace(valeurs[n], valeur_crit) + dice_input[membre[1]:]
        return d20.roll(dice_input).total

    def roll_ini(self):
        temp_dict = {}
        for name in self.combatants_names:
            temp_dict[name] = self.roll_d20(adv=self.combatants_stats[name]["ini_adv"])+self.combatants_stats[name]["ini_mod"]
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
            if attack["heal"] is True and attack["heal_type"] == "damage_dealt":
                self.heal(attacker_name, damage)
            if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
            if self.verbose is True:
                print(target_name, "fails to meet DC of", dc, "and takes:", damage, " damage!")
        if dc_result is True and attack["if_save"] == "half":
            self.combatants_hp[target_name] -= round(damage/2)
            if attack["heal"] is True and attack["heal_type"] == "damage_dealt":
                self.heal(attacker_name, round(damage/2))
            if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
            if self.verbose is True:
                print(target_name, "succeeds DC of", dc, "and takes:", round(damage/2), " damage! (half damage)")
        if dc_result is True and attack["if_save"] == "no_damage":
            if self.verbose is True:
                print(target_name, "succeeds to meet DC of", dc, "and takes no damage!")

    def attack(self, attacker_name, target_name, attack, adv=False, dis=False):
        if attack["has_advantage"] is True:
            adv = True
        if self.combatants_stats[attacker_name]["combat_stats"]["advantage_on_attack"] is True or self.combatants_stats[target_name]["combat_stats"]["advantage_if_attacked"] is True:
            adv = True
        if self.combatants_stats[attacker_name]["combat_stats"]["disadvantage_on_attack"] is True or self.combatants_stats[target_name]["combat_stats"]["disadvantage_if_attacked"] is True:
            dis = True
        conditions = self.combatants_stats[target_name]["combat_stats"]["conditions"]
        if "Prone" in conditions and attack["action_type"] == "melee":
            adv=True
        if "Prone" in conditions and attack["action_type"] == "ranged":
            dis=True
        attack_roll = self.roll_d20(adv=adv, dis=dis)+self.combatants_stats[attacker_name]["attack_mod"]
        straight_roll = attack_roll-self.combatants_stats[attacker_name]["attack_mod"]
        normal_damage = 0
        crit_damage = 0
        if self.combatants_stats[attacker_name]["sneak_attack_dices"] != 0 and self.combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] == 1:
            if straight_roll == 20:
                sneak_attack_damage = self.roll_dice((2*self.combatants_stats[attacker_name]["sneak_attack_dices"],6,0))
                crit_damage += sneak_attack_damage
            else:
                sneak_attack_damage = self.roll_dice((self.combatants_stats[attacker_name]["sneak_attack_dices"],6,0))
                normal_damage += sneak_attack_damage
            if self.verbose:
                print("Sneak attack damage", sneak_attack_damage)
            self.combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] = 0
        for dice_roll in attack["dice_rolls"]:
            normal_damage += self.roll_dice(dice_roll)
            if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                normal_damage = int(normal_damage/2)
            if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                normal_damage = 0
        for dice_roll in attack["dice_rolls"]:
            if type(dice_roll) == tuple:
                dice_roll = (2*dice_roll[0], dice_roll[1], dice_roll[2])
                crit_damage += self.roll_dice(dice_roll)
            else:
                crit_damage += self.calculate_crit_damage(dice_roll)
            if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                crit_damage = int(crit_damage/2)
            if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                crit_damage = 0
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
        if attack_roll >= self.combatants_stats[target_name]["ac"] and self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
            self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
        if straight_roll == 20 and self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
            self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 2
        else:
            if self.verbose is True:
                print(attacker_name, "misses.")

    def heal(self, combatant_name, heal_amount):
        self.combatants_hp[combatant_name] += heal_amount
        if self.combatants_stats[combatant_name]["max_hp"] <= self.combatants_hp[combatant_name]:
            self.combatants_hp[combatant_name] = self.combatants_stats[combatant_name]["max_hp"]
        if self.combatants_stats[combatant_name]["combat_stats"]["is_downed"]:
            self.combatants_stats[combatant_name]["combat_stats"]["death_saves"][0] = 0
            self.combatants_stats[combatant_name]["combat_stats"]["death_saves"][1] = 0
            self.combatants_stats[combatant_name]["combat_stats"]["is_downed"] = False
            self.remove_condition(combatant_name, "Unconscious")

    def gauss_circle_problem(self, rayon):
        resultat = 1
        for i in range(20):
            resultat += 4*(((rayon**2)//(4*i+1))-((rayon**2)//(4*i+3)))
        return resultat

    def calculate_aoe_number_of_targets(self, attacker_name, aoe_size, aoe_shape, pythagore):
        maximum_number_of_squares = 1
        if aoe_shape == "sphere":
            if pythagore:
                maximum_number_of_squares = self.gauss_circle_problem(aoe_size//5)
            else:
                maximum_number_of_squares = ((2*aoe_size+1)//5)**2
        if aoe_shape == "cylinder":
            if pythagore:
                maximum_number_of_squares = self.gauss_circle_problem(aoe_size//5)
            else:
                maximum_number_of_squares = ((2*aoe_size+1)//5)**2
        if aoe_shape == "square":
            maximum_number_of_squares = (aoe_size//5)**2
        if self.combatants_stats[attacker_name]["is_monster"]:
            number_of_targets = len(self.players_names)
        if self.combatants_stats[attacker_name]["is_monster"] is False:
            number_of_targets = len(self.monsters_names)
        if number_of_targets <= maximum_number_of_squares:
            maximum_number_of_squares = number_of_targets
        return random.randint(maximum_number_of_squares//2, maximum_number_of_squares)

    def set_target(self, attacker_name):
        try:
            if self.combatants_stats[attacker_name]["is_monster"] is True:
                return random.choice(self.players_names)

            else:
                return random.choice(self.monsters_names)
        except IndexError:
            return None

    def set_multiple_targets(self, attacker_name, number_of_targets):
        try:
            targets_list = []
            if self.combatants_stats[attacker_name]["is_monster"] is True:
                players_list_copy = copy.deepcopy(self.players_names)
                for _ in range(number_of_targets):
                    chosen_element = random.choice(players_list_copy)
                    players_list_copy.remove(chosen_element)
                    targets_list.append(chosen_element)
                return targets_list

            else:
                monsters_list_copy = copy.deepcopy(self.monsters_names)
                for _ in range(number_of_targets):
                    chosen_element = random.choice(monsters_list_copy)
                    monsters_list_copy.remove(chosen_element)
                    targets_list.append(chosen_element)
                return targets_list
        except IndexError:
            return None

    def aoe_attack(self, attacker_name, attack):
        aoe_size = attack["aoe_size"]
        aoe_shape = attack["aoe_shape"]
        number_of_targets = self.calculate_aoe_number_of_targets(attacker_name, aoe_size, aoe_shape, self.pythagore)
        list_of_targets = self.set_multiple_targets(attacker_name, number_of_targets)

        if self.verbose:
            print("{} casts {} on {} targets.".format(attacker_name, attack["name"], number_of_targets))

        dc_type = attack["dc_type"]
        dc = self.combatants_stats[attacker_name]["dc"]
        damage = 0
        dice_rolls = attack["dice_rolls"]
        for dice_roll in dice_rolls:
            damage += self.roll_dice(dice_roll)

        for target_name in list_of_targets:
            if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                damage = int(damage/2)
            if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                damage = 0
            dc_result = self.dc_check(target_name, dc, dc_type)
            if attack["condition"] != "":
                if dc_result is False:
                    self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
            if dc_result is False:
                self.combatants_hp[target_name] -= damage
                if attack["heal"] is True and attack["heal_type"] == "damage_dealt":
                    self.heal(attacker_name, damage)
                if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                    self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
                if self.verbose is True:
                    print(target_name, "fails to meet DC of", dc, "and takes:", damage, " damage!")
            if dc_result is True and attack["if_save"] == "half":
                self.combatants_hp[target_name] -= round(damage/2)
                if attack["heal"] is True and attack["heal_type"] == "damage_dealt":
                    self.heal(attacker_name, round(damage/2))
                if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                    self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
                if self.verbose is True:
                    print(target_name, "succeeds DC of", dc, "and takes:", round(damage/2), " damage! (half damage)")
            if dc_result is True and attack["if_save"] == "no_damage":
                if self.verbose is True:
                    print(target_name, "succeeds to meet DC of", dc, "and takes no damage!")


    def death(self, name):
        if self.combatants_stats[name]["is_monster"] is True:
            self.monsters_names.remove(name)
            self.ini_order.remove(name)

        else:
            self.combatants_hp[name] = 0
            self.set_condition(name, "Unconscious", 20, "con")
            self.combatants_stats[name]["combat_stats"]["is_downed"] = True

    def check_for_death(self):
        if any(v <= 0 for v in self.combatants_hp.values()):
            dead_list = []
            for name in self.combatants_hp:
                if self.combatants_hp[name] <= 0 and self.combatants_stats[name]["combat_stats"]["is_downed"] is False:
                    self.death(name)
                    if self.combatants_stats[name]["is_monster"]:
                        dead_list.append(name)
                    elif self.combatants_stats[name]["combat_stats"]["death_saves"][0] >= 3:
                        dead_list.append(name)
                elif self.combatants_stats[name]["combat_stats"]["death_saves"][0] >= 3:
                        dead_list.append(name)
                        self.players_names.remove(name)
                        self.ini_order.remove(name)
                        self.player_deaths += 1
            for name in dead_list:
                if self.verbose is True:
                    print(name, " dies.")
                del self.combatants_hp[name]

    def death_saves(self, player_name, mod=0, adv=False):
        self.combatants_hp[player_name] = 0
        straight_roll = self.roll_d20(adv=adv)
        roll = straight_roll + mod
        if straight_roll == 20:
            self.heal(player_name, 1)
            if self.verbose is True:
                print("{} CRITS on their death save and comes back to 1 HP!".format(player_name), "Death saves:", self.combatants_stats[player_name]["combat_stats"]["death_saves"])
            return
        if roll >= 10:
            self.combatants_stats[player_name]["combat_stats"]["death_saves"][1] += 1
            if self.combatants_stats[player_name]["combat_stats"]["death_saves"][1] >= 3:
                self.combatants_stats[player_name]["combat_stats"]["death_saves"][0] = 0
                self.combatants_stats[player_name]["combat_stats"]["death_saves"][1] = 0
                self.combatants_stats[player_name]["combat_stats"]["is_stable"] = True
            if self.verbose is True:
                print("{} succeeds on their death save.".format(player_name), "Death saves:", self.combatants_stats[player_name]["combat_stats"]["death_saves"])
        if straight_roll == 1:
            self.combatants_stats[player_name]["combat_stats"]["death_saves"][0] += 2
            if self.verbose is True:
                print("{} CRIT FAILS on their death save and and takes 2 death fails!".format(player_name), "Death saves:", self.combatants_stats[player_name]["combat_stats"]["death_saves"])
            self.check_for_death()
            return
        if roll < 10:
            self.combatants_stats[player_name]["combat_stats"]["death_saves"][0] += 1
            if self.verbose is True:
                print("{} fails on their death save.".format(player_name), "Death saves:", self.combatants_stats[player_name]["combat_stats"]["death_saves"])
            self.check_for_death()

        

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
        roll = self.roll_d20(adv=adv, dis=dis)+save_bonus
        if self.combatants_stats[combatant_name]["legend_resistances"] > 0:
            roll = dc
            self.combatants_stats[combatant_name]["legend_resistances"] -=1
            if self.verbose is True:
                print("{} uses a legendary resistance.".format(combatant_name))
        if roll >= dc:
            return True
        else:
            return False

    def condition_check(self, combatant_name, adv=False, dis=False):
        if len(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]) != 0:
            for condition in self.conditions_list:
                if condition == "Prone":
                    self.remove_condition(combatant_name, condition)
                    continue
                if condition in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
                    logging.info("Condition check FOUND: {}, combatant_name: {}".format(condition, combatant_name))
                    logging.info("Conditions info list: {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"]))
                    index = self.combatants_stats[combatant_name]["combat_stats"]["conditions"].index(condition)
                    dc = self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index][1]
                    stat = self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index][2]
                    if self.dc_check(combatant_name, dc, stat, adv=adv, dis=dis) is True and condition != "Unconscious":
                        logging.info("Condition save: {}, Combatant name: {}".format(condition, combatant_name))
                        self.remove_condition(combatant_name, condition)

    def remove_condition(self, combatant_name, condition_name):
        logging.info("Condition removed: {} Combatant name: {}".format(condition_name, combatant_name))
        logging.info("Conditions list (remove_condition before removal): {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]))
        if condition_name in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
            self.combatants_stats[combatant_name]["combat_stats"]["conditions"].remove(condition_name)
            logging.info("Conditions list (remove_condition after removal): {}".format(self.combatants_stats[combatant_name]["combat_stats"]["conditions"]))
            for index, condition in enumerate(self.combatants_stats[combatant_name]["combat_stats"]["conditions_info"]):
                logging.info("Index: {}, Condition: {}".format(index, condition))
                if condition[0] == condition_name:
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
        if condition_name not in self.combatants_stats[combatant_name]["combat_stats"]["conditions"]:
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

    def set_legend_actions_order(self):
        if self.players_names != []:
            for monster_name in self.legendary_monsters:
                initiative_order = copy.deepcopy(self.players_names)
                legendary_actions_order = []
                for possible_charge_use in range(self.combatants_stats[monster_name]["legend_actions_charges"]):
                    if initiative_order == []:
                        break
                    charge_use = random.choice(initiative_order)
                    initiative_order.remove(charge_use)
                    legendary_actions_order.append(charge_use)
                self.legend_actions_order[monster_name] = legendary_actions_order
    
    def execute_legend_action(self, monster_name):
        attack = random.choice(self.combatants_stats[monster_name]["legend_actions"])
        if attack["charge_cost"] > self.combatants_stats[monster_name]["legend_actions_charges"]:
            while attack["charge_cost"] > self.combatants_stats[monster_name]["legend_actions_charges"]:
                attack = random.choice(self.combatants_stats[monster_name]["legend_actions"])
        logging.info("{}'s legendary action: {}".format(monster_name, attack["name"]))
        self.check_for_death()
        if len(self.players_names) == 0 or len(self.monsters_names) == 0:
            return
        if attack["has_attack_mod"] is True:
            target = self.set_target(monster_name)
            self.attack(monster_name, target, attack)
            self.check_for_death()
        if attack["has_dc"] is True:
            target = self.set_target(monster_name)
            self.dc_attack(monster_name, target, attack)
            self.check_for_death()
        if attack["aoe"] is True:
            pass
        if len(self.players_names) == 0 or len(self.monsters_names) == 0:
            return

    def combat(self, verbose=True):
        rounds = 1
        self.roll_ini()
        self.separate_players_vs_monsters()
        self.verbose = verbose
        while len(self.players_names) != 0 and len(self.monsters_names) != 0:
            if self.verbose is True:
                print("\n --- Round {} ---\n".format(rounds))
                logging.info("\n --- Round {} ---\n".format(rounds))
            self.set_legend_actions_order()
            for attacker_name in self.ini_order:
                self.combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] = 1
                if "Incapacitated" in self.combatants_stats[attacker_name]["combat_stats"]["conditions"]:
                    logging.info("{} incapacitated".format(attacker_name))
                    if self.combatants_stats[attacker_name]["combat_stats"]["is_downed"]:
                        self.death_saves(attacker_name)
                else:
                    for attack in self.combatants_stats[attacker_name]["actions"]:
                        logging.info("{}, with {}".format(attacker_name, attack["name"]))
                        self.check_for_death()
                        if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                            break
                        if attack["has_attack_mod"] is True:
                            target = self.set_target(attacker_name)
                            self.attack(attacker_name, target, attack)
                            self.check_for_death()
                        if attack["has_dc"] is True and attack["aoe"] is False:
                            target = self.set_target(attacker_name)
                            self.dc_attack(attacker_name, target, attack)
                            self.check_for_death()
                        if attack["aoe"] is True:
                            self.aoe_attack(attacker_name, attack)
                            self.check_for_death()
                        if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                            break
                    self.condition_check(attacker_name)
                    self.heal(attacker_name, self.combatants_stats[attacker_name]["combat_stats"]["regeneration"])
                    for monster_name in self.legendary_monsters:
                        if attacker_name in self.legend_actions_order[monster_name]:
                            self.execute_legend_action(monster_name)
            rounds += 1
            for monster_name in self.legendary_monsters:
                self.combatants_stats[monster_name]["legendary_actions_charges"] = 3
        if self.verbose is True:
            print("Combat ended")
        if len(self.players_names) == 0:
            if self.verbose is True:
                print("The players were killed.")
            return (0, self.player_deaths, rounds)
        else:
            if self.verbose is True:
                print("The monsters were killed.")
            return (1, self.player_deaths, rounds)
                

# fix incapacitated et doublons de conditions

# À FAIRE:
# Gérer les debuffs (conditions) (Majoritairement done)
# Implémenter les aoe et les attaques différentes

# Besoin d'une manière de décider qui est attaqué (Check: random pour l'instant)
# Besoin d'une manière de distinguer les frontliners
# Simuler des stratégies
