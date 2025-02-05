from Stats_Module import MainStats
import random

### WILDEMOUNT
save = MainStats()
save.set_main_stats("John", ac=17, hp=92, dc=15, ini_mod=5, attack_mod=10, number_of_attacks=2, is_monster=False)
save.set_abilities(0, 5, 1, 3, 0, -1)
save.set_saves(0, 9, 1, 7, 0, -1)
save.set_action(action_type="melee", name="Rapier, +1", dice_rolls=[(1,8,8), (1,6,0)], damage_type="magical")
save.set_action(action_type="melee", name="Rapier, +1", dice_rolls=[(1,8,8), (1,6,0)], damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Faramir", ac=19, hp=98, dc=17, ini_mod=0, attack_mod=10, number_of_attacks=2, is_monster=False, divine_smite=True)
save.set_abilities(4, 0, 2, 0, -1, 5)
save.set_saves(9, 5, 7, 5, 8, 14)
save.set_spell_slots(4, 3, 3, 0, 0, 0, 0, 0, 0)
save.set_action(action_type="melee", name="Meteor Core Halberd", dice_rolls=[(1,10,6), (2,8,0)], damage_type="magical")
save.set_action(action_type="melee", name="Meteor Core Halberd", dice_rolls=[(1,10,6), (2,8,0)], damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Augustin", ac=25, hp=216, dc=22, ini_mod=7, attack_mod=15, number_of_attacks=2, is_monster=False, resistances=["necrotic", "force", "radiant"])
save.set_abilities(7, 2, 4, 6, 0, 1)
save.set_saves(13, 8, 16, 18, 6, 7)
save.set_action(action_type="melee", name="Thunder Gauntlets", dice_rolls="1d8+9", damage_type="thunder")
save.set_action(action_type="melee", name="Thunder Gauntlets", dice_rolls="1d8+9", damage_type="thunder")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Rand al'Thor", ac=17, hp=170, dc=20, ini_mod=3, attack_mod=16, number_of_attacks=2, is_monster=False, eldritch_smite=True, resistances=["necrotic", "force", "radiant"])
save.set_abilities(-1, 3, 2, -1, 2, 6)
save.set_saves(-1, 3, 2, -1, 8, 12)
save.set_spell_slots(0, 0, 0, 0, 4, 0, 0, 0, 0)
save.set_action(action_type="melee", name="Wrath of the Seasons", dice_rolls="2d6+2d4+11", damage_type="magical")
save.set_action(action_type="melee", name="Wrath of the Seasons", dice_rolls="2d6+2d4+11", damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Rand al'Thor 2", ac=16, hp=89, dc=17, ini_mod=3, attack_mod=11, number_of_attacks=2, is_monster=False)
save.set_abilities(-1, 3, 2, -1, 1, 5)
save.set_saves(-1, 3, 2, -1, 5, 9)
save.set_action(action_type="melee", name="Wrath of the Seasons", dice_rolls="2d6+2d8+12", damage_type="magical")
save.set_action(action_type="melee", name="Wrath of the Seasons", dice_rolls="2d6+2d8+12", damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Victoriana", ac=16, hp=109, dc=21, ini_mod=9, attack_mod=15, number_of_attacks=1, is_monster=False, resistances=["necrotic", "force", "radiant"]) # avec mage armor
save.set_abilities(-1, 3, 1, 6, 2, 0)
save.set_saves(-1, 3, 1, 12, 8, 0)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 3, 3, 3, 2, 2, 1, 1)
save.set_spellbook(["Meteor Swarm", "Disintegrate", "Fireball", "Chromatic Orb", ("Mind Sliver", "4d6")])
#save.set_action(action_type="melee", name="Rapier", dice_rolls="1d8+3", damage_type="piercing")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Dorran", ac=18, hp=152, dc=18, ini_mod=2, attack_mod=10, number_of_attacks=1, is_monster=False, resistances=["necrotic", "force", "radiant"])
save.set_abilities(6, 2, 3, 3, 6, -1)
save.set_saves(6, 2, 3, 9, 12, -1)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 3, 3, 2, 1, 1, 0, 0)
save.set_spellbook(["Ice Storm", "Blight", "Thunderwave", ("Thorn Whip", "3d6")])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gaspard Maupassant", ac=19, hp=163, ini_mod=9, attack_mod=12, number_of_attacks=2, is_monster=False, sneak_attack_dices=10, resistances=["fire", "necrotic", "force", "radiant"])
save.set_abilities(-1, 6, 1, 0, 0, 3)
save.set_saves(-1, 12, 1, 6, 6, 3)
save.set_action(action_type="melee", name="Rapier, +3", dice_rolls="1d8+9", damage_type="magical")
save.set_action(action_type="melee", name="Hand Crossbow, +3", dice_rolls="1d6+9", damage_type="magical")
save.save_main_stats()

### DND WITH THE BOYZ

save = MainStats()
save.set_main_stats("Ewyn", ac=21, hp=71, ini_mod=-1, ini_adv=True, attack_mod=7, number_of_attacks=2, is_monster=False, divine_smite=True)
save.set_abilities(3, -1, 4, 0, 0, 2)
save.set_saves(3, -1, 4, 0, 2, 4)
save.set_spell_slots(4, 2, 0, 0, 0, 0, 0, 0, 0)
save.set_action(action_type="melee", name="Battleaxe +1", dice_rolls="1d8+4", damage_type="magical")
save.set_action(action_type="melee", name="Battleaxe +1", dice_rolls="1d8+4", damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gowon", ac=13, hp=46, ini_mod=2, attack_mod=8, number_of_attacks=2, is_monster=False, dc=16)
save.set_abilities(0, 2, 3, -1, 1, 4)
save.set_saves(0, 2, 3, -1, 3, 6)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(0, 0, 2, 0, 0, 0, 0, 0, 0)
save.set_spellbook(["Burning Hands", ("Eldritch Blast", "1d10+4")])
save.save_main_stats()

save = MainStats() # on considère qu'il est toujours en rage, donc resistance et +2 sur damage
save.set_main_stats("Iaachus", ac=16, hp=44, ini_mod=2, attack_mod=5, number_of_attacks=1, is_monster=False, resistances=["nonmagical"])
save.set_abilities(3, 2, 4, -1, -1, 1)
save.set_saves(5, 2, 4, -1, -1, 1)
save.set_action(action_type="melee", name="Greatsword", dice_rolls=[(2,6,5)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Melvin", ac=15, hp=45, ini_mod=0, attack_mod=7, number_of_attacks=1, is_monster=False)
save.set_abilities(-1, 0, 1, 3, 4, 1)
save.set_saves(-1, 0, 1, 3, 6, 3)
save.set_action(action_type="ranged", name="Guiding Bolt", dice_rolls=[(5,6,0)], damage_type="radiant")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Reaghan", ac=13, hp=54, ini_mod=2, attack_mod=5, number_of_attacks=1, is_monster=False, dc=15, bardic_inspiration=[True, "1d8"])
save.set_abilities(0, 1, 3, 0, -1, 3)
save.set_saves(0, 3, 3, 0, -1, 5)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 3, 0, 0, 0, 0, 0, 0)
save.set_spellbook(["Hypnotic Pattern", "Cloud of Daggers", "Dissonant Whispers", ("Vicious Mockery", "2d4")])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vilgefortz", ac=16, hp=34, ini_mod=4, attack_mod=7, number_of_attacks=2, is_monster=False, sneak_attack_dices=3)
save.set_abilities(-1, 4, 0, 2, 0, 3)
save.set_saves(-1, 7, 0, 5, 0, 3)
save.set_action(action_type="melee", name="Psychic Blade", dice_rolls=[(1,6,4)], damage_type="psychic")
save.set_action(action_type="melee", name="Psychic Blade", dice_rolls=[(1,4,4)], damage_type="psychic")
save.save_main_stats()


save = MainStats()
save.set_main_stats("Ardorius", ac=16, hp=46, ini_mod=4, attack_mod=8, number_of_attacks=2, is_monster=False)
save.set_abilities(0, 4, 2, 2, 0, 1)
save.set_saves(0, 7, 2, 5, 0, 1)
save.set_action(action_type="melee", name="Rapier +1", dice_rolls="1d8+2d6", damage_type="magical")
save.set_action(action_type="melee", name="Rapier +1", dice_rolls="1d8+2d6", damage_type="magical")
save.save_main_stats()

###########
## VALASSI
###########

save = MainStats()
save.set_main_stats("Gwenyth", ac=16, hp=93, dc=14, ini_mod=7, attack_mod=10, number_of_attacks=2, is_monster=False, focus_type="focused", move_behavior="Ranged")
save.set_abilities(-1, 4, 1, 1, 3, 0)
save.set_saves(-1, 7, 1, 4, 3, 0)
save.set_action(action_type="ranged", name="Longbow", action_range=150, dice_rolls="1d8+2d6+7", damage_type="magical") # avec Hunter's Mark+Sneak Attack+Favored Foe
save.set_action(action_type="ranged", name="Longbow", action_range=150, dice_rolls="1d8+1d6+7", damage_type="magical") # avec Hunter's Mark
save.save_main_stats()

save = MainStats()
save.set_main_stats("Kal", ac=16, hp=95, dc=10, ini_mod=2, ini_adv=True, attack_mod=8, number_of_attacks=3, is_monster=False, resistances=["nonmagical", "magical", "acid", "cold", "fire", "force", "lightning", "necrotic", "poison", "radiant", "thunder"]) # totem of the bear+rage
save.set_abilities(4, 2, 3, 0, 1, -1)
save.set_saves(7, 2, 6, 0, 1, -1)
save.set_action(action_type="melee", name="Longsword, +1", dice_rolls="1d8+7", damage_type="magical") # avec rage
save.set_action(action_type="melee", name="Longsword, +1", dice_rolls="1d8+7", damage_type="magical") # avec rage
save.set_action(action_type="melee", name="Longsword, +1", dice_rolls="1d8+7", damage_type="magical") # two-weapon fighting avec rage
save.save_main_stats()

save = MainStats()
save.set_main_stats("Kara", ac=17, hp=64, dc=13, ini_mod=4, attack_mod=8, number_of_attacks=3, is_monster=False, max_ki_points=8, evasion=True)
save.set_abilities(0, 4, 2, 1, 3, 0)
save.set_saves(3, 7, 2, 1, 3, 0)
save.set_action(action_type="melee", name="Quarterstaff", dice_rolls="1d8+5", damage_type="magical")
save.set_action(action_type="melee", name="Quarterstaff", dice_rolls="1d8+5", damage_type="magical")
save.set_action(action_type="melee", name="Flurry of Blows", dice_rolls="1d8+5", damage_type="magical")
save.set_action(action_type="melee", name="Flurry of Blows", dice_rolls="1d8+5", damage_type="magical")
save.save_main_stats()

save = MainStats()
#save.set_main_stats("Denis", ac=14, hp=42, dc=14, ini_mod=1, attack_mod=8, number_of_attacks=2, is_monster=False, divine_smite=True, focus_type="focused", crits_on=19) # 59 max hp
save.set_main_stats("Denis", ac=16, hp=79, dc=14, ini_mod=1, attack_mod=9, number_of_attacks=2, is_monster=False, divine_smite=True, focus_type="focused", crits_on=19) # 59 max hp
save.set_abilities(1, 1, 2, 0, -1, 4)
save.set_saves(6, 6, 7, 5, 7, 12)
save.set_action(action_type="melee", name="Halberd, +1", dice_rolls="1d10+9", damage_type="magical") # + hexblade's curse (accurate si focused)
save.set_action(action_type="melee", name="Halberd, +1", dice_rolls="1d10+9", damage_type="magical") # + hexblade's curse (accurate si focused)
save.set_spell_slots(6, 2, 0, 0, 0, 0, 0, 0, 0)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Ghaz", ac=21, hp=57, dc=15, ini_mod=-1, attack_mod=7, number_of_attacks=1, is_monster=False, move_behavior="Support")
save.set_abilities(3, -1, 1, -1, 4, 2)
save.set_saves(3, 2, 1, -1, 4, 5)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 3, 2, 0, 0, 0, 0, 0)
save.set_spellbook(["Guiding Bolt", ("Sacred Flame", "2d8")])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Illian", ac=12, hp=42, dc=15, ini_mod=2, attack_mod=5, number_of_attacks=1, is_monster=False)
save.set_abilities(-1, 2, 2, 0, 1, 4)
save.set_saves(-1, 2, 4, 0, 1, 7)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 2, 0, 0, 0, 0, 0, 0)
save.set_spellbook(["Fireball", "Scorching Ray", "Magic Missile", ("Fire Bolt", "1d10")])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Cornelia", ac=18, hp=51, ini_mod=5, attack_mod=8, number_of_attacks=1, is_monster=False, sneak_attack_dices=4, is_frontliner=False)
save.set_abilities(-1, 5, 1, 4, 2, 0)
save.set_saves(-1, 8, 1, 7, 2, 0)
save.set_action(action_type="ranged", name="Heavy Crossbow, +1", dice_rolls="1d10+6", damage_type="magical", has_advantage=True)
save.save_main_stats()
