import random
import re
import pickle
import copy
import statistics
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
        self.spells_database = {}

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

    def import_spells(self):
        self.spells_database = pickle.load(open(Path.cwd()/"data"/"spells_database", "rb"))

    def roll_d20(self, adv=False, dis=False):
        if adv is False and dis is False:
            return d20.roll("1d20").total

        if adv is True and dis is True:
            return d20.roll("1d20").total
        
        if adv is True and dis is False:
            return d20.roll("2d20kh1").total
        
        if adv is False and dis is True:
            return d20.roll("2d20kl1").total

    def dice_tuple_to_string(self, dice_input):
        dice_output = ""
        total_damage_modifier = 0
        for i, dice in enumerate(dice_input):
            if i == 0:
                dice_output += "{}d{}".format(dice[0], dice[1])
            else:
                dice_output += "+{}d{}".format(dice[0], dice[1])
            total_damage_modifier += dice[2]
        return dice_output

    def roll_dice(self, dice_input):
        if dice_input == "":
            return 0

        if type(dice_input) == list:
            total = 0
            for dice in dice_input:
                total += self.roll_dice(dice)
            return total

        if type(dice_input) == tuple:
            string_input = "{}d{}+{}".format(dice_input[0], dice_input[1], dice_input[2])
            return d20.roll(string_input).total

        if type(dice_input) == str:
            logging.info("Dice input (string): {}".format(dice_input))
            return d20.roll(dice_input).total

        else:
            print("dice_input should be a tuple or a string")
    
    def calculate_crit_damage(self, attacker_name, dice_input):
        valeurs = re.findall(r"\d?\d?\d?\d(?=d)", dice_input)
        for n, membre in enumerate([(m.start(0), m.end(0)) for m in re.finditer(r"\d?\d?\d?\d(?=d)", dice_input)]):
            valeur_crit = str(2*int(valeurs[n]))
            if n == 0:
                valeur_crit = str(int(valeur_crit) + self.combatants_stats[attacker_name]["brutal_critical"])
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

    def dc_attack(self, attacker_name, target_name, attack, adv=False, dis=False):
        if self.combatants_stats[target_name]["magic_resistance"]:
            adv = True
        dice_rolls = attack["dice_rolls"]
        dc_type = attack["dc_type"]
        dc = self.combatants_stats[attacker_name]["dc"]
        dc_result = self.dc_check(target_name, dc, dc_type, adv=adv, dis=dis)
        if attack["condition"] != "":
            if dc_result is False:
                self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
        damage = 0
        if type(dice_rolls) == str:
            damage += self.roll_dice(dice_rolls)
        else:
            for dice_roll in dice_rolls:
                damage += self.roll_dice(dice_roll)
        if dc_result is False:
            self.combatants_hp[target_name] -= damage
            self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
            if attack["is_heal"] is True and attack["heal_type"] == "damage_dealt":
                self.heal(attacker_name, damage)
            if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
            if self.verbose is True:
                print(target_name, "fails to meet DC of", dc, "and takes:", damage, " damage!")

        if dc_result is True and attack["if_save"] == "no_effect":
            self.combatants_hp[target_name] -= damage
            self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
            if attack["is_heal"] is True and attack["heal_type"] == "damage_dealt":
                self.heal(attacker_name, damage)
            if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
            if self.verbose is True:
                print(target_name, "takes:", damage, " damage!")

        if dc_result is True and attack["if_save"] == "half":
            self.combatants_hp[target_name] -= round(damage/2)
            self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += round(damage/2)
            if attack["is_heal"] is True and attack["heal_type"] == "damage_dealt":
                self.heal(attacker_name, round(damage/2))
            if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
            if self.verbose is True:
                print(target_name, "succeeds DC of", dc, "and takes:", round(damage/2), " damage! (half damage)")
        if dc_result is True and attack["if_save"] == "no_damage":
            if self.verbose is True:
                print(target_name, "succeeds to meet DC of", dc, "and takes no damage!")

    def general_attack(self, attacker_name, attack):
        if attack["action_type"] == "spell":
            self.cast_spell(attacker_name)
            self.check_for_death()
        elif attack["has_attack_mod"] is True:
            target = self.set_target(attacker_name)
            self.attack(attacker_name, target, attack)
            self.check_for_death()
        elif attack["has_dc"] is True and attack["is_aoe"] is False:
            target = self.set_target(attacker_name)
            self.dc_attack(attacker_name, target, attack)
            self.check_for_death()
        elif attack["is_aoe"] is True:
            self.aoe_attack(attacker_name, attack)
            self.check_for_death()

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
        straight_roll = self.roll_d20(adv=adv, dis=dis)
        attack_roll = straight_roll+self.combatants_stats[attacker_name]["attack_mod"]
        if self.combatants_stats[attacker_name]["combat_stats"]["has_bardic_inspiration"][0]:
            attack_roll += self.use_bardic_inspiration(attacker_name)
        normal_damage = 0
        crit_damage = 0
        if self.combatants_stats[attacker_name]["sneak_attack_dices"] != 0 and self.combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] == 1:
            sneak_attack_dice_type = 6
            if attacker_name == "Gaspard Maupassant":
                sneak_attack_dice_type = 10
            if straight_roll == 20:
                sneak_attack_damage = self.roll_dice((2*self.combatants_stats[attacker_name]["sneak_attack_dices"],sneak_attack_dice_type,0))
                crit_damage += sneak_attack_damage
            else:
                sneak_attack_damage = self.roll_dice((self.combatants_stats[attacker_name]["sneak_attack_dices"],sneak_attack_dice_type,0))
                normal_damage += sneak_attack_damage
            if self.verbose:
                print("Sneak attack damage", sneak_attack_damage)
            self.combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] = 0
        dice_roll = attack["dice_rolls"]
        if self.combatants_stats[attacker_name]["divine_smite"]:
            divine_smite_choice = self.divine_smite_decision(attacker_name, target_name, straight_roll)
            if divine_smite_choice != "":
                if type(attack["dice_rolls"]) != str:
                    dice_roll = self.dice_tuple_to_string(dice_roll)
                dice_roll = dice_roll+self.divine_smite(attacker_name, target_name)
        elif self.combatants_stats[attacker_name]["eldritch_smite"]:
            eldritch_smite_choice = self.eldritch_smite_decision(attacker_name, target_name, straight_roll)
            if eldritch_smite_choice != "":
                if type(attack["dice_rolls"]) != str:
                    dice_roll = self.dice_tuple_to_string(dice_roll)
                dice_roll = dice_roll+self.eldritch_smite(attacker_name, target_name)
        if type(attack["dice_rolls"]) == str:
            normal_damage += self.roll_dice(dice_roll)
            if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                normal_damage = int(normal_damage/2)
            if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                normal_damage = 0
        else:
            for dice_roll in attack["dice_rolls"]:
                normal_damage += self.roll_dice(dice_roll)
                if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                    normal_damage = int(normal_damage/2)
                if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                    normal_damage = 0
        if type(attack["dice_rolls"]) == str:
            crit_damage += self.calculate_crit_damage(attacker_name, dice_roll)
            if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                crit_damage = int(crit_damage/2)
            if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                crit_damage = 0
        else:
            dice_roll = (2*dice_roll[0], dice_roll[1], dice_roll[2])
            crit_damage += self.roll_dice(dice_roll)
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
                self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += crit_damage
                if attack["condition"] != "":
                    if attack["auto_success"] is True:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                    else:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        if self.dc_check(target_name, dc, attack["dc_type"]) is False:
                            if attack["has_dc_effect_on_hit"] is True:
                                crit_damage += self.roll_dice(attack["dc_effect_on_hit"])
                            self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                if self.verbose is True:
                    print(attacker_name, "CRITS with", attack_roll, "and does:", crit_damage, " damage!")

        elif attack_roll >= self.combatants_stats[target_name]["ac"] and straight_roll != 20:
            if "Paralyzed" not in conditions and "Unconscious" not in conditions:
                self.combatants_hp[target_name] -= normal_damage
                self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += normal_damage
                if attack["condition"] != "":
                    if attack["auto_success"] is True:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                    else:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        if self.dc_check(target_name, dc, attack["dc_type"]) is False:
                            if attack["has_dc_effect_on_hit"] is True:
                                normal_damage += self.roll_dice(attack["dc_effect_on_hit"])
                            self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                if self.verbose is True:
                    print(attacker_name, "hits with", attack_roll, "and does:", normal_damage, " damage!")

        elif attack_roll >= self.combatants_stats[target_name]["ac"]:
            if "Paralyzed" in conditions or "Unconscious" in conditions:
                self.combatants_hp[target_name] -= crit_damage
                self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += crit_damage
                if attack["condition"] != "":
                    if attack["auto_success"] is True:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                    else:
                        dc = self.combatants_stats[attacker_name]["dc"]
                        if self.dc_check(target_name, dc, attack["dc_type"]) is False:
                            if attack["has_dc_effect_on_hit"] is True:
                                crit_damage += self.roll_dice(attack["dc_effect_on_hit"])
                            self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
                if self.verbose is True:
                    print(attacker_name, "CRITS on paralyzed or unconscious", target_name, "with", attack_roll, "and does:", crit_damage, " damage!")
        else:
            if self.verbose is True:
                print(attacker_name, "misses.")
        if attack_roll >= self.combatants_stats[target_name]["ac"] and self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
            self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
        elif straight_roll == 20 and self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
            self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 2

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
        if aoe_shape == "square" or aoe_shape == "cube":
            maximum_number_of_squares = (aoe_size//5)**2
        if aoe_shape == "cone":
            if pythagore:
                maximum_number_of_squares = self.gauss_circle_problem(aoe_size//5)//4
            else:
                maximum_number_of_squares = (((2*aoe_size+1)//5)**2)//4
        if aoe_shape == "line":
            maximum_number_of_squares = aoe_shape[1]*aoe_shape[2]//2
        if self.combatants_stats[attacker_name]["is_monster"]:
            number_of_targets = len(self.players_names)
        if self.combatants_stats[attacker_name]["is_monster"] is False:
            number_of_targets = len(self.monsters_names)
        if number_of_targets <= maximum_number_of_squares:
            maximum_number_of_squares = number_of_targets
        return random.randint(maximum_number_of_squares//3, maximum_number_of_squares)

    def set_target(self, attacker_name):
        if self.combatants_stats[attacker_name]["is_monster"]:
            if self.combatants_stats[attacker_name]["combat_stats"]["focus_type"] == "random":
                choice = random.choice(self.players_names)
                return choice
            elif self.combatants_stats[attacker_name]["combat_stats"]["focus_type"] == "focused":
                if self.combatants_stats[attacker_name]["combat_stats"]["focused_target"] == "":
                    choice = random.choice(self.players_names)
                    self.combatants_stats[attacker_name]["combat_stats"]["focused_target"] = choice
                    if self.verbose:
                        print("{} picked new target: {} who has {} HP".format(attacker_name, choice, self.combatants_hp[choice]))
                else:
                    choice = self.combatants_stats[attacker_name]["combat_stats"]["focused_target"]
                    if self.verbose:
                        print("{} kept the same target: {} who has {} HP".format(attacker_name, choice, self.combatants_hp[choice]))
                return choice

        else:
            choice = random.choice(self.monsters_names)
            for name in self.monsters_names:
                # choix du plus gros damage dealer
                if self.combatants_stats[name]["combat_stats"]["damage_dealt"] > self.combatants_stats[choice]["combat_stats"]["damage_dealt"]:
                    choice = name
            return choice

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

    def aoe_attack(self, attacker_name, attack, attack_name=""):
        aoe_size = attack["aoe_size"]
        aoe_shape = attack["aoe_shape"]
        number_of_targets = self.calculate_aoe_number_of_targets(attacker_name, aoe_size, aoe_shape, self.pythagore)
        list_of_targets = self.set_multiple_targets(attacker_name, number_of_targets)

        if self.verbose:
            try:
                print("{} casts {} on {} targets.".format(attacker_name, attack["name"], number_of_targets))
            except KeyError:
                print("{} casts {} on {} targets.".format(attacker_name, attack_name, number_of_targets))

        dc_type = attack["dc_type"]
        dc = self.combatants_stats[attacker_name]["dc"]
        damage = 0
        dice_rolls = attack["dice_rolls"]
        if type(dice_rolls) == str:
            damage += self.roll_dice(dice_rolls)
        else:
            for dice_roll in dice_rolls:
                damage += self.roll_dice(dice_roll)

        for target_name in list_of_targets:
            if attack["damage_type"] in self.combatants_stats[target_name]["resistances"]:
                damage = int(damage/2)
            if attack["damage_type"] in self.combatants_stats[target_name]["immunities"]:
                damage = 0
            if self.combatants_stats[target_name]["magic_resistance"]:
                adv = True
            else:
                adv = False
            dc_result = self.dc_check(target_name, dc, dc_type, adv=adv)
            if attack["condition"] != "":
                if dc_result is False:
                    self.set_condition(target_name, attack["condition"], dc, attack["dc_type"])
            if dc_result is False:
                self.combatants_hp[target_name] -= damage
                self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
                if attack["is_heal"] is True and attack["heal_type"] == "damage_dealt":
                    self.heal(attacker_name, damage)
                if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                    self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
                if self.verbose is True:
                    print(target_name, "fails to meet DC of", dc, "and takes:", damage, " damage!")
            if dc_result is True and attack["if_save"] == "no_effect":
                self.combatants_hp[target_name] -= damage
                self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
                if attack["is_heal"] is True and attack["heal_type"] == "damage_dealt":
                    self.heal(attacker_name, damage)
                if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                    self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
                if self.verbose is True:
                    print(target_name, "takes:", damage, " damage!")
            if dc_result is True and attack["if_save"] == "half":
                self.combatants_hp[target_name] -= round(damage/2)
                self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += round(damage/2)
                if attack["is_heal"] is True and attack["heal_type"] == "damage_dealt":
                    self.heal(attacker_name, round(damage/2))
                if self.combatants_stats[target_name]["combat_stats"]["is_downed"] is True:
                    self.combatants_stats[target_name]["combat_stats"]["death_saves"][0] += 1
                if self.verbose is True:
                    print(target_name, "succeeds DC of", dc, "and takes:", round(damage/2), " damage! (half damage)")
            if dc_result is True and attack["if_save"] == "no_damage":
                if self.verbose is True:
                    print(target_name, "succeeds to meet DC of", dc, "and takes no damage!")


    def death(self, name):
        if self.combatants_stats[name]["is_monster"]:
            if self.combatants_stats[name]["is_mythic"] and self.combatants_stats[name]["combat_stats"]["mythic_state"]:
                self.monsters_names.remove(name)
                self.ini_order.remove(name)
            elif self.combatants_stats[name]["is_mythic"] and self.combatants_stats[name]["combat_stats"]["mythic_state"] is False:
                self.combatants_hp[name] = self.combatants_stats[name]["mythic_hp"]
                logging.info("{} enters its mythic stage and gains {} HP!".format(name, self.combatants_stats[name]["mythic_hp"]))
                if self.verbose:
                    print("{} enters its mythic stage and gains {} HP!".format(name, self.combatants_stats[name]["mythic_hp"]))
            else:
                self.monsters_names.remove(name)
                self.ini_order.remove(name)

        else:
            self.combatants_hp[name] = 0
            self.set_condition(name, "Unconscious", 20, "con")
            self.combatants_stats[name]["combat_stats"]["is_downed"] = True
            for monster in self.monsters_names:
                if self.combatants_stats[monster]["combat_stats"]["focused_target"] == name:
                    self.combatants_stats[monster]["combat_stats"]["focused_target"] = ""
            if self.verbose:
                print("{} is downed.".format(name))


    def check_for_death(self):
        if any(v <= 0 for v in self.combatants_hp.values()):
            dead_list = []
            for name in self.combatants_hp:
                if self.combatants_hp[name] <= 0 and self.combatants_stats[name]["combat_stats"]["is_downed"] is False:
                    self.death(name)
                    if self.combatants_stats[name]["is_monster"]:
                        if self.combatants_stats[name]["is_mythic"] and self.combatants_stats[name]["combat_stats"]["mythic_state"] is False:
                            self.combatants_stats[name]["combat_stats"]["mythic_state"] = True
                        else:
                            dead_list.append(name)
                    elif self.combatants_stats[name]["combat_stats"]["death_saves"][0] >= 3:
                        dead_list.append(name)
                elif self.combatants_stats[name]["combat_stats"]["death_saves"][0] >= 3:
                        dead_list.append(name)
                        self.players_names.remove(name)
                        self.ini_order.remove(name)
                        self.player_deaths += 1
                        for monster in self.monsters_names:
                            if self.combatants_stats[monster]["combat_stats"]["focused_target"] == name:
                                self.combatants_stats[monster]["combat_stats"]["focused_target"] = ""
            for name in dead_list:
                logging.info("{} dies.".format(name))
                if self.verbose is True:
                    print(name, " dies.")
                del self.combatants_hp[name]
                if name in self.legendary_monsters:
                    self.legendary_monsters.remove(name)

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
        if self.combatants_stats[combatant_name]["combat_stats"]["has_bardic_inspiration"][0]:
            roll += self.use_bardic_inspiration(combatant_name)
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
        if attack["charge_cost"] > self.combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"]:
            for l_ac in self.combatants_stats[monster_name]["legend_actions"]:
                if l_ac["charge_cost"] <= self.combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"]:
                    attack = l_ac
        if attack["charge_cost"] <= self.combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"]:
            self.combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"] -= attack["charge_cost"]
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
            if attack["is_aoe"] is True:
                pass
            if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                return

    def reset_legendary_actions_charges(self):
        for monster_name in self.legendary_monsters:
            self.combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"] = self.combatants_stats[monster_name]["legend_actions_charges"]


    def execute_multiattack(self, attacker_name, attack):
        multiattack_list = attack["multiattack_list"]
        for attack in multiattack_list:
            self.general_attack(attacker_name, self.combatants_stats[attacker_name]["action_arsenal"][attack])
            if len(self.players_names) == 0:
                self.check_for_death()
                break

    def choose_attack(self, attacker_name):
        recharge_seen = True
        multiattack_seen = True
        attack_not_chosen = True
        arsenal = self.combatants_stats[attacker_name]["action_arsenal"]
        for attack_name in arsenal.keys():
            attack = arsenal[attack_name]
            if attack["has_recharge"]:
                recharge_seen = False
            elif attack["is_multiattack"]:
                multiattack_seen = False
        while attack_not_chosen:
            for attack_name in arsenal.keys():
                attack = arsenal[attack_name]
                if attack["has_recharge"] and attack["recharge_ready"]:
                    return attack
                elif attack["has_recharge"] and attack["recharge_ready"] is False:
                    recharge_roll = self.roll_dice("1d6")
                    if recharge_roll >= attack["recharge"]:
                        return attack
                    else:
                        recharge_seen = True
                elif attack["has_recharge"] is False and attack["is_multiattack"]:
                    return attack
                elif attack["has_recharge"] is False and attack["is_multiattack"] is False:
                    if recharge_seen and multiattack_seen:
                        return attack

    def choose_aoe_or_single(self, attacker_name):
        enemy_hps = []
        attack_type_decision = ""
        for name in self.combatants_hp.keys():
            if self.combatants_stats[attacker_name]["is_monster"]:
                if self.combatants_stats[name]["is_monster"]:
                    continue
                else:
                    enemy_hps.append(self.combatants_hp[name])
            else:
                if self.combatants_stats[name]["is_monster"]:
                    enemy_hps.append(self.combatants_hp[name])
                else:
                    continue
        average_enemy_hp = statistics.mean(enemy_hps)
        try:
            enemy_hps_std = statistics.stdev(enemy_hps)
        except statistics.StatisticsError:
            enemy_hps_std = 0
        outlier_count = 0
        for name in self.combatants_hp.keys():
            if self.combatants_stats[attacker_name]["is_monster"]:
                if self.combatants_stats[name]["is_monster"]:
                    continue
                else:
                    if self.combatants_hp[name] > average_enemy_hp+enemy_hps_std:
                        outlier_count += 1
            else:
                if self.combatants_stats[name]["is_monster"]:
                    if self.combatants_hp[name] > average_enemy_hp+enemy_hps_std:
                        outlier_count += 1
                else:
                    continue
        if self.combatants_stats[attacker_name]["is_monster"]:
            if outlier_count >= len(self.players_names)/8 or outlier_count == 0:
                if len(self.players_names) > 3:
                    attack_type_decision = "is_aoe"
                else:
                    attack_type_decision = "single"
            else:
                attack_type_decision = "single"
        else:
            if outlier_count >= len(self.monsters_names)/4  or outlier_count == 0:
                if len(self.monsters_names) > 3:
                    attack_type_decision = "is_aoe"
                else:
                    attack_type_decision = "single"
            else:
                attack_type_decision = "single"
        return attack_type_decision

    def spell_decision(self, caster_name):
        spellbook = self.combatants_stats[caster_name]["spellbook"]
        spell_slots = self.combatants_stats[caster_name]["combat_stats"]["spell_slots"]
        spell_level_to_use = 0
        spell_type_decision = self.choose_aoe_or_single(caster_name)
        chosen_spell = {}
        spell_name = ""

        # Détermine le niveau le plus élevé disponible
        for spell_level in reversed(spell_slots.keys()):
            if spell_slots[spell_level] > 0:
                spell_level_to_use = spell_level
                break
            else:
                continue
        
        # Détermine si single target ou is_aoe
        if spell_type_decision == "is_aoe":
            for spell_known in spellbook:
                if type(spell_known) == str:
                    if self.spells_database[spell_known]["is_aoe"] and self.spells_database[spell_known]["level"] <= spell_level_to_use:
                        chosen_spell = spell_known
                        break
                else:
                    if self.spells_database[spell_known[0]]["is_aoe"] and self.spells_database[spell_known[0]]["level"] <= spell_level_to_use:
                        chosen_spell = spell_known
                        break
        else:
            for spell_known in spellbook:
                if type(spell_known) == str:
                    if self.spells_database[spell_known]["is_aoe"] is False and self.spells_database[spell_known]["level"] <= spell_level_to_use:
                        chosen_spell = spell_known
                        break
                else:
                    if self.spells_database[spell_known[0]]["is_aoe"] is False and self.spells_database[spell_known[0]]["level"] <= spell_level_to_use:
                        chosen_spell = spell_known
                        break

        if type(chosen_spell) == str:
            spell_name = chosen_spell
            chosen_spell = copy.deepcopy(self.spells_database[chosen_spell])
        elif type(chosen_spell) == tuple:
            spell_name = chosen_spell[0]
            spell = copy.deepcopy(self.spells_database[chosen_spell[0]])
            spell["dice_rolls"] = chosen_spell[1]
            chosen_spell = spell
        else:
            chosen_spell = spellbook[-1]
            spell_name = chosen_spell[0]
            spell = copy.deepcopy(self.spells_database[chosen_spell[0]])
            spell["dice_rolls"] = chosen_spell[1]
            chosen_spell = spell
        if chosen_spell["level"] < spell_level_to_use and chosen_spell["is_upcastable"]:
            for _ in range(spell_level_to_use-chosen_spell["level"]):
                chosen_spell["dice_rolls"] += "+"+chosen_spell["upcast_effect"]
        else:
            spell_level_to_use = chosen_spell["level"]
        logging.info("Chose {} at level {}.".format(spell_name, spell_level_to_use))
        return chosen_spell, spell_name, spell_level_to_use

    def cast_spell(self, caster_name):
        spell, spell_name, spell_level = self.spell_decision(caster_name)
        if spell_level > 0:
            self.combatants_stats[caster_name]["combat_stats"]["spell_slots"][spell_level] -= 1
            if self.combatants_stats[caster_name]["combat_stats"]["spell_slots"][spell_level] < 0:
                self.combatants_stats[caster_name]["combat_stats"]["spell_slots"][spell_level] = 0 # just to be sure
        if self.verbose:
            print("{} casts {} at level {}!".format(caster_name, spell_name, spell_level))
        if spell["has_attack_mod"]:
            self.attack(caster_name, self.set_target(caster_name), spell)
        elif spell["has_dc"] is True and spell["is_aoe"] is False:
            self.dc_attack(caster_name, self.set_target(caster_name), spell)
        elif spell["is_aoe"]:
            self.aoe_attack(caster_name, spell, attack_name=spell_name)

    
    def divine_smite_decision(self, attacker_name, target_name, straight_roll):
        if straight_roll == 20:
            # je crit, je smite
            return self.divine_smite(attacker_name, target_name)
        if self.combatants_stats[attacker_name]["divine_smite"] and self.roll_d20()>=10:
            return self.divine_smite(attacker_name, target_name)
        else:
            return ""
        
    def eldritch_smite_decision(self, attacker_name, target_name, straight_roll):
        if straight_roll == 20:
            # je crit, je smite
            return self.eldritch_smite(attacker_name, target_name)
        if self.combatants_stats[attacker_name]["eldritch_smite"] and self.roll_d20()>=10:
            return self.eldritch_smite(attacker_name, target_name)
        else:
            return ""

    def divine_smite(self, attacker_name, target_name):
        bonus_dice_roll = ""
        number_of_dice = 2
        level = 0
        for spell_slot_level in self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"].keys():
            if self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][spell_slot_level] > 0:
                level = self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][spell_slot_level]
        if level == 0:
            return bonus_dice_roll
        self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] -= 1
        if self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] < 0:
                self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] = 0 # just to be sure
        number_of_dice += level-1
        target_creature_type = self.combatants_stats[target_name]["creature_type"]
        if target_creature_type == "undead" or target_creature_type == "fiend":
            number_of_dice += 1
        if number_of_dice > 6:
            number_of_dice = 6
        bonus_dice_roll = "+{}d8".format(number_of_dice)
        logging.info("{} used a level {} divine smite on {} ({}) and added {} to their roll".format(attacker_name, level, target_name, target_creature_type, bonus_dice_roll))
        return bonus_dice_roll
    
    def eldritch_smite(self, attacker_name, target_name):
        bonus_dice_roll = ""
        number_of_dice = 2
        level = 0
        for spell_slot_level in self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"].keys():
            if self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][spell_slot_level] > 0:
                level = spell_slot_level
        if level == 0:
            return bonus_dice_roll
        self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] -= 1
        if self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] < 0:
                self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] = 0 # just to be sure
        number_of_dice += level-1
        target_creature_type = self.combatants_stats[target_name]["creature_type"]
        if number_of_dice > 6:
            number_of_dice = 6
        bonus_dice_roll = "+{}d8".format(number_of_dice)
        logging.info("{} used a level {} eldritch smite on {} ({}) and added {} to their roll".format(attacker_name, level, target_name, target_creature_type, bonus_dice_roll))
        #print("{} used a level {} eldritch smite on {} ({}) and added {} to their roll".format(attacker_name, level, target_name, target_creature_type, bonus_dice_roll))
        #print(self.combatants_stats[attacker_name]["combat_stats"]["spell_slots"])
        return bonus_dice_roll
    
    def choose_inspiration_target(self, bard_name, target_list):
        target_choice = random.choice(target_list)
        if target_choice == bard_name:
            if len(target_list) == 1:
                return None
            return self.choose_inspiration_target(self, bard_name, target_list)
        else:
            return target_choice

    def give_bardic_inspiration(self, bard_name, target_name):
        if target_name == None:
            pass
        else:
            self.combatants_stats[target_name]["combat_stats"]["has_bardic_inspiration"] = self.combatants_stats[bard_name]["bardic_inspiration"]
            self.combatants_stats[bard_name]["combat_stats"]["bardic_inspiration_charges"] -= 1
            logging.info("{} gave a {} bardic inspiration to {}".format(bard_name, self.combatants_stats[bard_name]["bardic_inspiration"][1], target_name))

    def use_bardic_inspiration(self, user_name):
        self.combatants_stats[user_name]["combat_stats"]["has_bardic_inspiration"][0] = False
        bonus = self.roll_dice(self.combatants_stats[user_name]["combat_stats"]["has_bardic_inspiration"][1])
        logging.info("{} used a {} bardic inspiration and added {} to their roll".format(user_name, self.combatants_stats[user_name]["combat_stats"]["has_bardic_inspiration"][1], bonus))
        return bonus
        
        
    def combat(self, verbose=True):
        rounds = 1
        players_damage = {}
        self.roll_ini()
        self.separate_players_vs_monsters()
        self.import_spells()
        self.verbose = verbose
        for player in self.players_names:
            players_damage[player] = 0
        while len(self.players_names) != 0 and len(self.monsters_names) != 0:
            if self.verbose is True:
                print("\n --- Round {} ---\n".format(rounds))
                logging.info("\n --- Round {} ---\n".format(rounds))
            self.set_legend_actions_order()
            self.reset_legendary_actions_charges()
            for attacker_name in self.ini_order:
                if self.verbose:
                    print("{}'s turn.".format(attacker_name))
                if self.combatants_stats[attacker_name]["is_monster"] is False:
                        self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] = 0
                self.combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] = 1
                if "Incapacitated" in self.combatants_stats[attacker_name]["combat_stats"]["conditions"]:
                    logging.info("{} incapacitated".format(attacker_name))
                    if self.combatants_stats[attacker_name]["combat_stats"]["is_downed"]:
                        self.death_saves(attacker_name)
                else:
                    if self.combatants_stats[attacker_name]["action_arsenal"] != {}:
                        self.check_for_death()
                        if len(self.players_names) == 0:
                            continue
                        attack_choice = self.choose_attack(attacker_name)
                        if attack_choice["is_multiattack"]:
                            self.execute_multiattack(attacker_name, attack_choice)
                        else:
                            self.general_attack(attacker_name, attack_choice)
                    else:
                        for attack in self.combatants_stats[attacker_name]["actions"]:
                            logging.info("{}, with {}".format(attacker_name, attack["name"]))
                            self.check_for_death()
                            if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                                break

                            # TODO déterminer si les spells nécessitent de voir!
                            #if attack["action_type"] == "spell" and "Blinded" not in self.combatants_stats[attacker_name]["combat_stats"]["conditions"]:
                            if attack["action_type"] == "spell":
                                self.cast_spell(attacker_name)
                                self.check_for_death()
                            elif attack["has_attack_mod"] is True:
                                target = self.set_target(attacker_name)
                                self.attack(attacker_name, target, attack)
                                self.check_for_death()
                            elif attack["has_dc"] is True and attack["is_aoe"] is False:
                                target = self.set_target(attacker_name)
                                self.dc_attack(attacker_name, target, attack)
                                self.check_for_death()
                            elif attack["is_aoe"] is True:
                                self.aoe_attack(attacker_name, attack)
                                self.check_for_death()
                            if self.combatants_stats[attacker_name]["bardic_inspiration"][0] and self.combatants_stats[attacker_name]["combat_stats"]["bardic_inspiration_charges"] > 0:
                                if self.combatants_stats[attacker_name]["is_monster"]:
                                    target_choice = self.choose_inspiration_target(attacker_name, self.monsters_names)
                                else:
                                    target_choice = self.choose_inspiration_target(attacker_name, self.players_names)
                                self.give_bardic_inspiration(attacker_name, target_choice)
                            if self.combatants_stats[attacker_name]["is_monster"] is False:
                                players_damage[attacker_name] += self.combatants_stats[attacker_name]["combat_stats"]["damage_dealt"]
                            if len(self.players_names) == 0 or len(self.monsters_names) == 0:
                                break
                    self.condition_check(attacker_name)
                    self.heal(attacker_name, self.combatants_stats[attacker_name]["combat_stats"]["regeneration"])
                    for monster_name in self.legendary_monsters:
                        if attacker_name in self.legend_actions_order[monster_name]:
                            self.execute_legend_action(monster_name)
            rounds += 1
        if self.verbose is True:
            print("Combat ended")
        if len(self.players_names) == 0:
            if self.verbose is True:
                print("The players were killed.")
            return (0, self.player_deaths, rounds, players_damage)
        else:
            if self.verbose is True:
                print("The monsters were killed.")
            return (1, self.player_deaths, rounds, players_damage)
                

# fix incapacitated et doublons de conditions

# À FAIRE:
# Gérer les debuffs (conditions) (Majoritairement done)
# Implémenter les aoe et les attaques différentes

# Besoin d'une manière de décider qui est attaqué (Check: random pour l'instant)
# Besoin d'une manière de distinguer les frontliners
# Simuler des stratégies
