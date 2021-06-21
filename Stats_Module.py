import pickle
from pathlib import Path

class MainStats():
    def __init__(self):
        self.avg_attack_dmg = 0
        self.name = ""
        self.ac = 10
        self.dc = 10
        self.max_hp = 25
        self.ini_mod = 0
        self.attack_mod = 0
        self.number_of_attacks = 1
        self.is_monster = True
        self.is_frontliner = True
        self.combat_stats = {"is_downed": False,
                            "is_stable": False,
                            "conditions": [],
                            "conditions_info": [],
                            "death_saves": [0, 0],
                            "regeneration": 0,
                            "advantage_on_attack": False,
                            "advantage_if_attacked": False,
                            "disadvantage_on_attack": False,
                            "disadvantage_if_attacked": False}
        self.abilities = {"str": 10,
                          "dex": 10,
                          "con": 10,
                          "wis": 10,
                          "int": 10,
                          "cha": 10}
        self.saves = {"str": 10,
                      "dex": 10,
                      "con": 10,
                      "wis": 10,
                      "int": 10,
                      "cha": 10}
        self.actions = []
        self.legend_actions = []
        self.legend_actions_charges = 0
        self.legend_resistances = 0

    def add_avg_dmg(self, x, y, z):
        self.avg_attack_dmg += round(x*((y+1)/2)+z)

    def set_main_stats(self, name, ac=10, hp=25, dc=10, ini_mod=0, attack_mod=0, number_of_attacks=1, legend_resistances=0, is_monster=True, is_frontliner=True):
        self.name = name
        self.ac = ac
        self.max_hp = hp
        self.dc = dc
        self.ini_mod = ini_mod
        self.attack_mod = attack_mod
        self.number_of_attacks = number_of_attacks
        self.legend_resistances = legend_resistances
        self.is_monster = is_monster
        self.is_frontliner = is_frontliner

    def set_abilities(self, str_bonus, dex_bonus, con_bonus, int_bonus, wis_bonus, cha_bonus):
        self.abilities = {"str": str_bonus,
                          "dex": dex_bonus,
                          "con": con_bonus,
                          "int": int_bonus,
                          "wis": wis_bonus,
                          "cha": cha_bonus}

    def set_saves(self, str_bonus, dex_bonus, con_bonus, int_bonus, wis_bonus, cha_bonus):
        self.saves = {"str": str_bonus,
                      "dex": dex_bonus,
                      "con": con_bonus,
                      "int": int_bonus,
                      "wis": wis_bonus,
                      "cha": cha_bonus}

    def set_action(self, action_type="melee", name="", has_attack_mod=True, has_dc=False, dc_type="", dice_rolls=[], condition="", aoe=False, damage_type="nonmagical", if_save="half", auto_success=False, has_dc_effect_on_hit=False, dc_effect_on_hit=[], has_advantage=False):
        dict = {}
        dict["action_type"] = action_type
        dict["name"] = name
        dict["has_attack_mod"] = has_attack_mod
        dict["has_dc"] = has_dc
        dict["dc_type"] = dc_type
        dict["dice_rolls"] = dice_rolls
        dict["condition"] = condition
        dict["aoe"] = aoe
        dict["damage_type"] = damage_type
        dict["if_save"] = if_save
        dict["auto_success"] = auto_success
        dict["has_dc_effect_on_hit"] = has_dc_effect_on_hit
        dict["dc_effect_on_hit"] = dc_effect_on_hit
        dict["has_advantage"] = has_advantage
        self.actions.append(dict)
    
    def save_main_stats(self):
        dict = {self.name: {
                "avg_attack_dmg": self.avg_attack_dmg, 
                "ac": self.ac, 
                "dc": self.dc, 
                "max_hp": self.max_hp,
                "ini_mod": self.ini_mod,
                "attack_mod": self.attack_mod,
                "number_of_attacks": self.number_of_attacks,
                "is_monster": self.is_monster,
                "is_frontliner": self.is_frontliner,
                "combat_stats": self.combat_stats,
                "abilities": self.abilities,
                "saves": self.saves,
                "actions": self.actions}}
        self.actions = []
        pickle.dump(dict, open(Path.cwd()/"data"/"{}_{}".format("stats", self.name), "w+b"))
