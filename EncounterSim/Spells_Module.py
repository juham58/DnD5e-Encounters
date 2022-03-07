import pickle
import json
import re
from pathlib import Path

class Spells_Database():
    def __init__(self):
        self.database = pickle.load(open(Path.cwd()/"data"/"spells_database", "rb"))

    def save_spells(self):
        pickle.dump(self.database, open(Path.cwd()/"data"/"spells_database", "w+b"))

    def add_spell(self, name, level, dice_rolls="8d6", range=120, has_attack_mod=False, has_dc=False, is_aoe=False, dc_type="", condition="", aoe_size=20, aoe_shape="sphere", damage_type="fire", if_save="half", has_dc_effect_on_hit=False, dc_effect_on_hit=[], is_heal=False, heal_type="damage_dealt", is_upcastable=False, upcast_effect="1d6"):
        spell_dict = {}
        spell_dict["level"] = level
        spell_dict["range"] = range
        spell_dict["has_attack_mod"] = has_attack_mod
        spell_dict["has_dc"] = has_dc
        spell_dict["dc_type"] = dc_type
        spell_dict["dice_rolls"] = dice_rolls
        spell_dict["condition"] = condition
        spell_dict["is_aoe"] = is_aoe
        spell_dict["aoe_size"] = aoe_size
        spell_dict["aoe_shape"] = aoe_shape
        spell_dict["damage_type"] = damage_type
        spell_dict["if_save"] = if_save
        spell_dict["has_dc_effect_on_hit"] = has_dc_effect_on_hit
        spell_dict["dc_effect_on_hit"] = dc_effect_on_hit
        spell_dict["is_heal"] = is_heal
        spell_dict["heal_type"] = heal_type
        spell_dict["is_upcastable"] = is_upcastable
        spell_dict["upcast_effect"] = upcast_effect
        self.database[name] = spell_dict

    def parse_spells_json(self):
        with open(Path.cwd()/"data"/"spells.json", encoding='utf-8') as fichier:
            file = json.load(fichier)
            for k in file:
                print(k["name"])

sd = Spells_Database()
sd.parse_spells_json()