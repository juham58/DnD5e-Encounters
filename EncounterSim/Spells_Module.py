import dill as pickle
import json
import re
from pathlib import Path

class Spells_Database():
    def __init__(self):
        self.database = pickle.load(open(Path.cwd()/"data"/"spells_database", "rb"))

    def save_spells(self):
        pickle.dump(self.database, open(Path.cwd()/"data"/"spells_database", "w+b"))
    
    def check_if_aoe(self, spell):
        if len(re.findall("line", spell["range"])) > 0:
            if len(re.findall("(\d+)-foot\Dlong", spell["description"])) > 0:
                return True, int(re.findall("(\d+)-foot\Dlong", spell["description"])[0]), "line"
            elif len(re.findall("(\d+) feet long", spell["description"])) > 0:
                return True, int(re.findall("(\d+) feet long", spell["description"])[0]), "line"
            else:
                print(spell["name"], "Line size unknown")
                return False, 0, "line"
        if len(re.findall("cone", spell["description"])) > 0:
            return True, int(re.findall("(\d+)-foot\Dcone", spell["description"])[0]), "cone"
        if len(re.findall("cube", spell["description"])) > 0:
            if len(re.findall("(\d+)-foot\Dcube", spell["description"])) > 0:
                return True, int(re.findall("(\d+)-foot\Dcube", spell["description"])[0]), "cube"
            elif len(re.findall("cube (\d+) feet", spell["description"])) > 0:
                return True, int(re.findall("cube (\d+) feet", spell["description"])[0]), "cube"
            else:
                print(spell["name"], "Cube size unknown")
                return True, 0, "cube"
        if len(re.findall("sphere", spell["description"])) > 0:
            if len(re.findall("(\d+)-foot\Dradius", spell["description"])) > 0:
                size = re.findall("(\d+)-foot\Dradius", spell["description"])[0]
            elif len(re.findall("(\d+)-foot\Ddiameter", spell["description"])) > 0:
                size = re.findall("(\d+)-foot\Ddiameter", spell["description"])[0]
            else:
                print(spell["name"], "Sphere size unknown")
                size = 0
                return False, int(size), "sphere"
            return True, int(size), "sphere"
        if len(re.findall("cylinder", spell["description"])) > 0:
            if len(re.findall("(\d+)-foot\Dradius", spell["description"])) > 0:
                size = re.findall("(\d+)-foot\Dradius", spell["description"])[0]
            elif len(re.findall("(\d+)-foot\Ddiameter", spell["description"])) > 0:
                size = re.findall("(\d+)-foot\Ddiameter", spell["description"])[0]
            else:
                print(spell["name"], "Cylinder size unknown")
                size = 0
                return False, 0, "cylinder"
            return True, int(size), "cylinder"
        else:
            return False, 0, ""

    def find_conditions(self, spell):
        conditions_found = []
        conditions = ["blinded", "charmed", "deafened", "frightened", "grappled", "incapacitated", "invisible", "paralyzed", "petrified", "poisoned", "prone", "restrained", "stunned", "unconscious"]
        for condition in conditions:
            if len(re.findall(condition, spell["description"].lower())) > 0:
                conditions_found.append(condition)
        return conditions_found


    def add_spell(self, name, level, spell_type="damage", dice_rolls="8d6", range=120, has_attack_mod=False, has_dc=False, is_aoe=False, dc_type="", condition="", aoe_size=20, aoe_shape="sphere", damage_type="", if_save="", has_dc_effect_on_hit=False, dc_effect_on_hit="", is_heal=False, heal_type="damage_dealt", is_upcastable=False, upcast_effect="", concentration=False, is_bonus_action=False, n_targets=1, can_add_spellcasting_mod=False):
        spell_dict = {}
        spell_dict["level"] = level
        spell_dict["range"] = range
        spell_dict["attack_mod"] = -99
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
        spell_dict["has_advantage"] = False
        spell_dict["concentration"] = concentration
        spell_dict["is_bonus_action"] = is_bonus_action
        spell_dict["n_targets"] = n_targets
        spell_dict["can_add_spellcasting_mod"] = can_add_spellcasting_mod
        self.database[name] = spell_dict
    
    def edit_spell(self, spell_name, elements_to_edit=[], edits=[]):
        for i, element in enumerate(elements_to_edit):
            self.database[spell_name][element] = edits[i]

    def print_spell(self, spell_name):
        print(self.database[spell_name])

    def convert_ability_type(self, ability_string):
        if ability_string == "Strength":
            return "str"
        elif ability_string == "Dexterity":
            return "dex"
        elif ability_string == "Constitution":
            return "con"
        elif ability_string == "Intelligence":
            return "int"
        elif ability_string == "Wisdom":
            return "wis"
        elif ability_string == "Charisma":
            return "cha"

    def parse_spells_json(self):
        with open(Path.cwd()/"data"/"spells.json", encoding='utf-8') as fichier:
            file = json.load(fichier)
            for spell in file:
                print(spell["name"])
                name = spell["name"]
                if spell["level"] == "cantrip":
                    level = 0
                else:
                    level = int(spell["level"])
                if "bonus action" in spell["casting_time"]:
                    is_bonus_action = True
                else:
                    is_bonus_action = False
                if len(re.findall("\d+", spell["range"])) > 0:
                    range = int(re.findall("\d+", spell["range"])[0])
                if len(re.findall("spell attack", spell["description"])) > 0 and len(re.findall("make \w+\s(\w+)\ssaving throw", spell["description"])) > 0:
                    has_attack_mod = True
                    has_dc_effect_on_hit = True
                elif len(re.findall("spell attack", spell["description"])) > 0:
                    has_attack_mod = True
                    has_dc_effect_on_hit = False
                else:
                    has_dc_effect_on_hit = False
                    has_attack_mod = False
                if has_attack_mod is False and len(re.findall("make \w+\s(\w+)\ssaving throw", spell["description"])) > 0:
                    has_dc = True
                    dc_type = self.convert_ability_type(re.findall("make \w+\s(\w+)\ssaving throw", spell["description"])[0])
                else:
                    has_dc = False
                    dc_type = ""
                if len(re.findall("\d+d\d+\s(\w+)\sdamage", spell["description"])) > 0:
                    dice_rolls = re.findall("(\d+d\d+)\s\w+\sdamage", spell["description"])[0]
                else:
                    dice_rolls = ""
                is_aoe, aoe_size, aoe_shape = self.check_if_aoe(spell)
                found_conditions = self.find_conditions(spell)

                # TODO permettre plus qu'une condition
                if len(found_conditions) > 0:
                    condition = found_conditions[0]
                else:
                    condition = ""
                
                if len(re.findall("\d+d\d+\s(\w+)\sdamage", spell["description"])) > 0:
                    damage_type = re.findall("\d+d\d+\s(\w+)\sdamage", spell["description"])[0]
                else:
                    damage_type = ""

                if len(re.findall("or half", spell["description"])) > 0:
                    if_save = "half"
                elif len(re.findall("takes half", spell["description"])) > 0:
                    if_save = "half"
                else:
                    if_save = "no_damage"

                if len(re.findall("regai\w+\shit points", spell["description"])) > 0 and len(re.findall("can't regain hit points", spell["description"])) == 0:
                    is_heal = True
                    heal_type = "roll"
                else:
                    is_heal = False
                    heal_type = ""
                try:
                    is_upcastable = True
                    if len(re.findall("\d+d\d+", spell["higher_levels"])) > 0:
                        upcast_effect = re.findall("\d+d\d+", spell["higher_levels"])[0]
                    else:
                        upcast_effect = ""
                except KeyError:
                    is_upcastable = False
                    upcast_effect = ""
                if len(re.findall("concentration", spell["duration"].lower())) > 0:
                    concentration = True
                else:
                    concentration = False
                dc_effect_on_hit = ""
                self.add_spell(name, level, dice_rolls=dice_rolls, range=int(range), 
                            has_attack_mod=has_attack_mod, has_dc=has_dc, 
                            is_aoe=is_aoe, dc_type=dc_type, condition=condition, 
                            aoe_size=aoe_size, aoe_shape=aoe_shape, damage_type=damage_type, 
                            if_save=if_save, has_dc_effect_on_hit=has_dc_effect_on_hit, dc_effect_on_hit=dc_effect_on_hit, 
                            is_heal=is_heal, heal_type=heal_type, is_upcastable=is_upcastable, upcast_effect=upcast_effect,
                            concentration=concentration, is_bonus_action=is_bonus_action)

sd = Spells_Database()
#sd.parse_spells_json()
sd.add_spell("Toll the Dead", 0, dice_rolls="1d12", range=60, has_attack_mod=False, has_dc=True, is_aoe=False, dc_type="wis", condition="", damage_type="necrotic", if_save="no_damage")
sd.add_spell("Toll the Dead", 0, dice_rolls="1d12", range=60, has_attack_mod=False, has_dc=True, is_aoe=False, dc_type="wis", condition="", damage_type="necrotic", if_save="no_damage")
sd.add_spell("Mind Sliver", 0, dice_rolls="1d6", range=60, has_attack_mod=False, has_dc=True, is_aoe=False, dc_type="int", condition="", damage_type="psychic", if_save="no_damage")
sd.add_spell("Disintegrate", 6, dice_rolls="10d6+40", range=60, has_attack_mod=False, has_dc=True, is_aoe=False, dc_type="dex", condition="", damage_type="force", if_save="no_damage", is_upcastable=True, upcast_effect="3d6")
sd.add_spell("Chromatic Orb", 1, dice_rolls="3d8", range=90, has_attack_mod=True, has_dc=False, is_aoe=False, damage_type="acid", is_upcastable=True, upcast_effect="1d8")
sd.add_spell("Sorcerous Burst", 0, dice_rolls="1d8", range=120, has_attack_mod=True, has_dc=False, is_aoe=False, damage_type="magical")
sd.add_spell("Call Lightning", 3, dice_rolls="3d10", range=120, has_attack_mod=False, has_dc=True, is_aoe=True, aoe_size=5, aoe_shape="cylinder", dc_type="dex", is_upcastable=True, upcast_effect="1d10", damage_type="lightning", if_save="half")
sd.add_spell("Cloud of Daggers", 2, dice_rolls="4d4", range=60, has_attack_mod=False, has_dc=True, is_aoe=True, aoe_size=5, aoe_shape="square", dc_type="dex", if_save="no_effect", is_upcastable=True, upcast_effect="2d4")
sd.add_spell("Horrid Wilting", 8, dice_rolls="12d8", range=150, has_attack_mod=False, has_dc=True, is_aoe=True, aoe_size=30, aoe_shape="square", dc_type="con", if_save="half")
sd.add_spell("Chaos Bolt", 1, dice_rolls="2d8+1d6", range=120, has_attack_mod=True)
sd.edit_spell("Ice Storm", ["dice_rolls"], ["2d8+4d6"])
sd.edit_spell("Meteor Swarm", ["dice_rolls", "range"], ["40d6", 5280])
sd.edit_spell("Finger of Death", ["dice_rolls"], ["7d8+30"])
sd.edit_spell("Sacred Flame", ["has_dc", "dc_type"], [True, "dex"])
sd.edit_spell("Hypnotic Pattern", ["condition"], ["Incapacitated"])
sd.edit_spell("Healing Word", ["dice_rolls", "can_add_spellcasting_mod"], ["2d4", True])
sd.edit_spell("Mass Healing Word", ["dice_rolls", "n_targets", "can_add_spellcasting_mod"], ["2d4", 6, True])
sd.edit_spell("Cure Wounds", ["dice_rolls", "upcast_effect", "can_add_spellcasting_mod"], ["2d8", "2d8", True])
sd.edit_spell("Mass Cure Wounds", ["dice_rolls", "n_targets", "can_add_spellcasting_mod"], ["5d8", 6, True])
sd.edit_spell("Heal", ["dice_rolls"], ["70"])
#sd.add_spell("Firebolt", 0, dice_rolls="1d10", range=120, has_attack_mod=True, has_dc=False, is_aoe=False, damage_type="fire")
#sd.print_spell("Cloud of Daggers")
#sd.print_spell("Bless")
#sd.print_spell("Magic Missile")
#sd.print_spell("Mind Sliver")
sd.print_spell("Magic Missile")
sd.print_spell("Scorching Ray")
sd.print_spell("Hypnotic Pattern")
sd.print_spell("Mass Healing Word")
sd.save_spells()


# TODO implémenter Magic Missile et Scorching Ray