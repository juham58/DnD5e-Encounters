import dill as pickle
from pathlib import Path

class MainStats():
    def __init__(self):
        self.custom_stats = []
        self.avg_attack_dmg = 0
        self.name = ""
        self.ac = 10
        self.dc = 10
        self.speed = 30
        self.max_hp = 25
        self.ini_mod = 0
        self.ini_adv = False
        self.attack_mod = 0
        self.spellcasting_ability = ""
        self.spellcasting_mod = 0
        self.number_of_attacks = 1
        self.creature_type = "humanoid"
        self.resistances = []
        self.vulnerabilities = []
        self.immunities = []
        self.is_monster = True
        self.is_frontliner = True
        self.sneak_attack_dices = 0
        self.brutal_critical = 0
        self.divine_smite = False
        self.eldritch_smite = False
        self.crits_on = 20
        self.bardic_inspiration = [False, "1d6"]
        self.magic_resistance = False
        self.is_mythic = False
        self.mythic_hp = 0
        self.legend_actions_charges = 0
        self.legend_resistances = 0
        self.evasion = False
        self.move_behavior = "Frontliner"
        self.has_bonus_action_dash = False
        self.combat_stats = {"is_downed": False,
                            "is_stable": False,
                            "position": 0,
                            "desired_position": 0,
                            "longest_attack_range": 0,
                            "focus_type": "random",
                            "focused_target": "",
                            "conditions": [],
                            "conditions_info": [],
                            "lingering_damage": [], 
                            "death_saves": [0, 0],
                            "regeneration": 0,
                            "advantage_on_attack": False,
                            "advantage_if_attacked": False,
                            "disadvantage_on_attack": False,
                            "disadvantage_if_attacked": False,
                            "sneak_attack_charge": 1,
                            "damage_dealt": 0,
                            "damage_received_in_turn": 0,
                            "mythic_state": False,
                            "legend_actions_charges": self.legend_actions_charges,
                            "casted_smite_spell": False,
                            "has_bardic_inspiration": [False, "1d6"],
                            "bardic_inspiration_charges": 0,
                            "spell_slots": {1: 0, 
                                            2: 0, 
                                            3: 0, 
                                            4: 0, 
                                            5: 0, 
                                            6: 0, 
                                            7: 0, 
                                            8: 0, 
                                            9: 0}}
        self.abilities = {"str": 0,
                          "dex": 0,
                          "con": 0,
                          "wis": 0,
                          "int": 0,
                          "cha": 0}
        self.saves = {"str": 0,
                      "dex": 0,
                      "con": 0,
                      "wis": 0,
                      "int": 0,
                      "cha": 0}
        self.spellbook = []
        self.actions = []
        self.action_arsenal = {}
        self.legend_actions = []
        self.mythic_actions = []
        self.regeneration = 0

    def add_avg_dmg(self, x, y, z):
        self.avg_attack_dmg += round(x*((y+1)/2)+z)

    def set_spellcasting_mod(self):
        if self.spellcasting_ability != "" and self.spellcasting_ability.lower in ["str", "dex", "con", "int", "wis", "cha"]:
            self.spellcasting_mod = self.abilities[self.spellcasting_ability.lower]

    def set_main_stats(self, name, ac=10, hp=25, dc=10, speed=30, ini_mod=None, ini_adv=False, attack_mod=0, number_of_attacks=1, resistances=[], immunities=[], vulnerabilities=[], creature_type="humanoid", legend_actions_charges=0, legend_resistances=0, regeneration=0, is_monster=True, is_frontliner=True, sneak_attack_dices=0, brutal_critical=0, divine_smite=False, eldritch_smite=False, bardic_inspiration=[False, "1d6"], advantage_if_attacked=False, disadvantage_if_attacked=False, magic_resistance=False, is_mythic=False, mythic_hp=0, max_ki_points=0, focus_type="random", evasion=False, crits_on=20, move_behavior="Frontliner", has_bonus_action_dash=False, spellcasting_ability=""):
        self.name = name
        self.ac = ac
        self.max_hp = hp
        self.dc = dc
        self.ini_mod = ini_mod
        self.ini_adv = ini_adv
        self.attack_mod = attack_mod
        self.spellcasting_ability = spellcasting_ability
        self.number_of_attacks = number_of_attacks
        self.resistances = resistances
        self.immunities = immunities
        self.vulnerabilities = vulnerabilities
        self.creature_type = creature_type
        self.legend_actions_charges = legend_actions_charges
        self.legend_resistances = legend_resistances
        self.regeneration = regeneration
        self.is_monster = is_monster
        self.is_frontliner = is_frontliner
        self.sneak_attack_dices = sneak_attack_dices
        self.brutal_critical = brutal_critical
        self.divine_smite = divine_smite
        self.eldritch_smite = eldritch_smite
        self.crits_on = crits_on
        self.bardic_inspiration = bardic_inspiration
        self.magic_resistance = magic_resistance
        self.is_mythic = is_mythic
        self.mythic_hp = mythic_hp
        self.evasion = evasion
        self.move_behavior = move_behavior
        self.speed = speed
        self.has_bonus_action_dash = has_bonus_action_dash
        if move_behavior == "Frontliner":
            self.combat_stats["position"] = 0
            self.combat_stats["desired_position"] = 0
        elif move_behavior == "HitAndRun":
            if self.speed <= 30:
                self.combat_stats["position"] = 1
                self.combat_stats["desired_position"] = 1
            elif self.speed <= 60:
                self.combat_stats["position"] = 2
                self.combat_stats["desired_position"] = 2
            else:
                self.combat_stats["position"] = 3
                self.combat_stats["desired_position"] = 3
        elif move_behavior == "Ranged":
            self.combat_stats["position"] = 3
            self.combat_stats["desired_position"] = 3
        elif move_behavior == "Support":
            self.combat_stats["position"] = 2
            self.combat_stats["desired_position"] = 2
        else:
            # if unknown, assume Frontliner
            self.combat_stats["position"] = 0
            move_behavior = "Frontliner"
        self.combat_stats["advantage_if_attacked"] = advantage_if_attacked
        self.combat_stats["disadvantage_if_attacked"] = disadvantage_if_attacked
        self.combat_stats["focus_type"] = focus_type
        self.combat_stats["ki_points"] = max_ki_points

    def set_abilities(self, str_bonus, dex_bonus, con_bonus, int_bonus, wis_bonus, cha_bonus):
        self.abilities = {"str": str_bonus,
                          "dex": dex_bonus,
                          "con": con_bonus,
                          "int": int_bonus,
                          "wis": wis_bonus,
                          "cha": cha_bonus}
        if self.ini_mod == None:
            self.ini_mod = dex_bonus

    def set_saves(self, str_bonus, dex_bonus, con_bonus, int_bonus, wis_bonus, cha_bonus):
        self.saves = {"str": str_bonus,
                      "dex": dex_bonus,
                      "con": con_bonus,
                      "int": int_bonus,
                      "wis": wis_bonus,
                      "cha": cha_bonus}

    def set_spell_slots(self, lvl_1, lvl_2, lvl_3, lvl_4, lvl_5, lvl_6, lvl_7, lvl_8, lvl_9):
        self.combat_stats["spell_slots"] = {1: lvl_1, 
                            2: lvl_2, 
                            3: lvl_3, 
                            4: lvl_4, 
                            5: lvl_5, 
                            6: lvl_6, 
                            7: lvl_7, 
                            8: lvl_8, 
                            9: lvl_9}

    def set_action(self, action_type="melee", attack_mod=-99, name="", range=0, has_attack_mod=True, has_dc=False, dc_type="", dice_rolls=[], condition="", is_aoe=False, aoe_size=30, aoe_shape="sphere", damage_type="nonmagical", if_save="half", auto_success=False, has_dc_effect_on_hit=False, dc_effect_on_hit=[], has_advantage=False, is_heal=False, heal_type="damage_dealt", return_dict=False, lingering_damage=""):
        act_dict = {}
        act_dict["action_type"] = action_type
        act_dict["name"] = name
        act_dict["range"] = range
        if attack_mod == -99:
            act_dict["attack_mod"] = self.attack_mod
        else:
            act_dict["attack_mod"] = attack_mod
        act_dict["has_attack_mod"] = has_attack_mod
        act_dict["has_dc"] = has_dc
        act_dict["dc_type"] = dc_type
        act_dict["dice_rolls"] = dice_rolls
        act_dict["condition"] = condition
        act_dict["is_aoe"] = is_aoe
        act_dict["aoe_size"] = aoe_size
        act_dict["aoe_shape"] = aoe_shape
        act_dict["damage_type"] = damage_type
        act_dict["if_save"] = if_save
        act_dict["auto_success"] = auto_success
        act_dict["has_dc_effect_on_hit"] = has_dc_effect_on_hit
        act_dict["dc_effect_on_hit"] = dc_effect_on_hit
        act_dict["lingering_damage"] = lingering_damage
        act_dict["has_advantage"] = has_advantage
        act_dict["is_heal"] = is_heal
        act_dict["heal_type"] = heal_type
        act_dict["is_custom_action"] = False
        self.actions.append(act_dict)
        if return_dict:
            return act_dict

    def add_custom_action(self, action_python_function, name="", range=0):
        act_dict = {}
        act_dict["name"] = name
        act_dict["range"] = range
        act_dict["is_custom_action"] = True
        act_dict["action_python_function"] = action_python_function
        self.actions.append(act_dict)

    def set_action_in_arsenal(self, action_type="melee", name="", attack_mod=-99, range=0, has_attack_mod=True, has_dc=False, dc_type="", dice_rolls=[], condition="", is_aoe=False, aoe_size=30, aoe_shape="sphere", damage_type="nonmagical", if_save="half", auto_success=False, has_dc_effect_on_hit=False, dc_effect_on_hit=[], has_advantage=False, is_heal=False, heal_type="damage_dealt", has_recharge=False, recharge=6, recharge_ready=True, is_multiattack=False, multiattack_list=[], lingering_damage=""):
        act_dict = {}
        act_dict["action_type"] = action_type
        act_dict["name"] = name
        act_dict["range"] = range
        if attack_mod == -99:
            act_dict["attack_mod"] = self.attack_mod
        else:
            act_dict["attack_mod"] = attack_mod
        act_dict["has_attack_mod"] = has_attack_mod
        act_dict["has_dc"] = has_dc
        act_dict["dc_type"] = dc_type
        act_dict["dice_rolls"] = dice_rolls
        act_dict["condition"] = condition
        act_dict["is_aoe"] = is_aoe
        if action_type == "aoe":
            act_dict["is_aoe"] = True
        act_dict["aoe_size"] = aoe_size
        act_dict["aoe_shape"] = aoe_shape
        act_dict["damage_type"] = damage_type
        act_dict["if_save"] = if_save
        act_dict["auto_success"] = auto_success
        act_dict["has_dc_effect_on_hit"] = has_dc_effect_on_hit
        act_dict["dc_effect_on_hit"] = dc_effect_on_hit
        act_dict["lingering_damage"] = lingering_damage
        act_dict["has_advantage"] = has_advantage
        act_dict["is_heal"] = is_heal
        act_dict["heal_type"] = heal_type
        act_dict["has_recharge"] = has_recharge
        act_dict["recharge_ready"] = recharge_ready
        act_dict["recharge"] = recharge
        act_dict["is_multiattack"] = is_multiattack
        if action_type == "multiattack":
            act_dict["is_multiattack"] = True
        act_dict["multiattack_list"] = multiattack_list
        self.action_arsenal[name] = act_dict

    def set_legend_action(self, action_type="melee", name="", attack_mod=-99, range=0, charge_cost=1, has_attack_mod=True, has_dc=False, dc_type="", dice_rolls=[], condition="", is_aoe=False, aoe_size=30, aoe_shape="sphere", damage_type="nonmagical", if_save="half", auto_success=False, has_dc_effect_on_hit=False, dc_effect_on_hit=[], has_advantage=False, is_heal=False, lingering_damage=""):
        act_dict = {}
        act_dict["action_type"] = action_type
        act_dict["name"] = name
        act_dict["range"] = range
        act_dict["charge_cost"] = charge_cost
        if attack_mod == -99:
            act_dict["attack_mod"] = self.attack_mod
        else:
            act_dict["attack_mod"] = attack_mod
        act_dict["has_attack_mod"] = has_attack_mod
        act_dict["has_dc"] = has_dc
        act_dict["dc_type"] = dc_type
        act_dict["dice_rolls"] = dice_rolls
        act_dict["condition"] = condition
        act_dict["is_aoe"] = is_aoe
        act_dict["aoe_size"] = aoe_size
        act_dict["aoe_shape"] = aoe_shape
        act_dict["damage_type"] = damage_type
        act_dict["if_save"] = if_save
        act_dict["auto_success"] = auto_success
        act_dict["has_dc_effect_on_hit"] = has_dc_effect_on_hit
        act_dict["dc_effect_on_hit"] = dc_effect_on_hit
        act_dict["lingering_damage"] = lingering_damage
        act_dict["has_advantage"] = has_advantage
        act_dict["is_heal"] = is_heal
        self.legend_actions.append(act_dict)

    def set_mythic_action(self, action_type="melee", name="", range=0, charge_cost=1, attack_mod=-99, has_attack_mod=True, has_dc=False, dc_type="", dice_rolls=[], condition="", is_aoe=False, aoe_size=30, aoe_shape="sphere", damage_type="nonmagical", if_save="half", auto_success=False, has_dc_effect_on_hit=False, dc_effect_on_hit=[], has_advantage=False, lingering_damage=""):
        act_dict = {}
        act_dict["action_type"] = action_type
        act_dict["name"] = name
        act_dict["range"] = range
        act_dict["charge_cost"] = charge_cost
        if attack_mod == -99:
            act_dict["attack_mod"] = self.attack_mod
        else:
            act_dict["attack_mod"] = attack_mod
        act_dict["has_attack_mod"] = has_attack_mod
        act_dict["has_dc"] = has_dc
        act_dict["dc_type"] = dc_type
        act_dict["dice_rolls"] = dice_rolls
        act_dict["condition"] = condition
        act_dict["is_aoe"] = is_aoe
        act_dict["aoe_size"] = aoe_size
        act_dict["aoe_shape"] = aoe_shape
        act_dict["damage_type"] = damage_type
        act_dict["if_save"] = if_save
        act_dict["auto_success"] = auto_success
        act_dict["has_dc_effect_on_hit"] = has_dc_effect_on_hit
        act_dict["dc_effect_on_hit"] = dc_effect_on_hit
        act_dict["lingering_damage"] = lingering_damage
        act_dict["has_advantage"] = has_advantage
        self.legend_actions.append(act_dict)

    def set_spellbook(self, list_of_available_spells):
        self.spellbook = list_of_available_spells

    def add_custom_combat_stat(self, key, value):
        self.combat_stats[key] = value

    def add_custom_stat(self, key, value):
        self.custom_stats.append((key, value))
    
    def save_main_stats(self):
        self.set_spellcasting_mod()
        act_dict = {self.name: {
                "name": self.name,
                "avg_attack_dmg": self.avg_attack_dmg, 
                "ac": self.ac, 
                "dc": self.dc, 
                "speed": self.speed,
                "max_hp": self.max_hp,
                "ini_mod": self.ini_mod,
                "ini_adv": self.ini_adv,
                "attack_mod": self.attack_mod,
                "spellcasting_mod": self.spellcasting_mod,
                "number_of_attacks": self.number_of_attacks,
                "resistances": self.resistances,
                "immunities": self.immunities,
                "vulnerabilities": self.vulnerabilities,
                "creature_type": self.creature_type,
                "is_monster": self.is_monster,
                "is_frontliner": self.is_frontliner,
                "sneak_attack_dices": self.sneak_attack_dices,
                "brutal_critical": self.brutal_critical,
                "divine_smite": self.divine_smite,
                "eldritch_smite": self.eldritch_smite,
                "crits_on": self.crits_on,
                "bardic_inspiration": self.bardic_inspiration,
                "magic_resistance": self.magic_resistance,
                "is_mythic": self.is_mythic,
                "mythic_hp": self.mythic_hp,
                "evasion": self.evasion,
                "move_behavior": self.move_behavior,
                "has_bonus_action_dash": self.has_bonus_action_dash,
                "combat_stats": self.combat_stats,
                "abilities": self.abilities,
                "saves": self.saves,
                "spellbook": self.spellbook,
                "actions": self.actions,
                "action_arsenal": self.action_arsenal,
                "legend_actions": self.legend_actions,
                "mythic_actions": self.mythic_actions,
                "legend_actions_charges": self.legend_actions_charges,
                "legend_resistances": self.legend_resistances}}
        if len(self.custom_stats) != 0:
            for custom_stat in self.custom_stats:
                act_dict[self.name][custom_stat[0]] = custom_stat[1]

        if act_dict[self.name]["bardic_inspiration"][0]:
            act_dict[self.name]["combat_stats"]["bardic_inspiration_charges"] = act_dict[self.name]["abilities"]["cha"]
        self.actions = []
        longest_action_range = 0
        for action in act_dict[self.name]["actions"]:
            if action["range"] > longest_action_range:
                longest_action_range = action["range"]
        if len(self.spellbook) != 0:
            spells_database = pickle.load(open(Path.cwd()/"data"/"spells_database", "rb"))
            for spell in self.spellbook:
                if type(spell) == tuple:
                    spell = spell[0]
                if spells_database[spell]["range"] > longest_action_range:
                    longest_action_range = spells_database[spell]["range"]
        act_dict[self.name]["combat_stats"]["longest_action_range"] = longest_action_range
        pickle.dump(act_dict, open(Path.cwd()/"data"/"{}_{}".format("stats", self.name), "w+b"))
