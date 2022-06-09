from Stats_Module import MainStats
import random

### WILDEMOUNT
save = MainStats()
save.set_main_stats("John", ac=17, hp=92, dc=15, ini_mod=5, attack_mod=10, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 8, 8)
save.add_avg_dmg(1, 6, 0) # Rite of the dawn
save.set_abilities(0, 5, 1, 3, 0, -1)
save.set_saves(0, 9, 1, 7, 0, -1)
save.set_action(action_type="melee", name="Rapier, +1", dice_rolls=[(1,8,8), (1,6,0)], damage_type="magical")
save.set_action(action_type="melee", name="Rapier, +1", dice_rolls=[(1,8,8), (1,6,0)], damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Faramir", ac=19, hp=98, dc=17, ini_mod=0, attack_mod=10, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 10, 4)
save.add_avg_dmg(2, 8, 0) # Si divine smite lvl 1 à chaque attaque
save.set_abilities(4, 0, 2, 0, -1, 5)
save.set_saves(9, 5, 7, 5, 8, 14)
save.set_action(action_type="melee", name="Meteor Core Halberd", dice_rolls=[(1,10,6), (2,8,0)], damage_type="magical")
save.set_action(action_type="melee", name="Meteor Core Halberd", dice_rolls=[(1,10,6), (2,8,0)], damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Augustin", ac=24, hp=71, dc=17, ini_mod=2, attack_mod=10, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 6, 6)
save.add_avg_dmg(0, 0, 5) # Estimation du dommage bonus pour sharpshooter
save.set_abilities(0, 2, 1, 5, 0, 1)
save.set_saves(1, 3, 6, 10, 1, 2)
save.set_action(action_type="melee", name="Lightning Launcher", dice_rolls=[(1,6,12)], damage_type="lightning")
save.set_action(action_type="melee", name="Lightning Launcher", dice_rolls=[(1,6,12)], damage_type="lightning")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Rand al'Thor", ac=16, hp=89, dc=17, ini_mod=3, attack_mod=11, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(2, 6, 6)
save.add_avg_dmg(1, 10, 0) # estimation du bonus dommage pour différents spells de warlock i guess
save.set_abilities(-1, 3, 2, -1, 1, 5)
save.set_saves(-1, 3, 2, -1, 5, 9)
save.set_action(action_type="melee", name="Wrath of the Seasons", dice_rolls="2d6+2d8+12", damage_type="magical")
save.set_action(action_type="melee", name="Wrath of the Seasons", dice_rolls="2d6+2d8+12", damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Victoriana", ac=16, hp=72, dc=17, ini_mod=8, attack_mod=10, number_of_attacks=1, is_monster=False) # avec mage armor
save.add_avg_dmg(7, 8, 0) # basé sur Chromatic orb lvl 5
save.set_abilities(-1, 3, 1, 5, 1, 0)
save.set_saves(-1, 3, 1, 9, 5, 0)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 3, 3, 2, 1, 0, 0, 0)
save.set_spellbook(["Disintegrate", "Fireball", "Chromatic Orb", ("Toll the Dead", "3d12")])
#save.set_action(action_type="melee", name="Rapier", dice_rolls="1d8+3", damage_type="piercing")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Dorran", ac=15, hp=52, dc=12, ini_mod=1, attack_mod=4, number_of_attacks=3, is_monster=False)
save.add_avg_dmg(1, 8, 2)
save.add_avg_dmg(2, 10, 0) # estimation du 4d10 si la moitié du monde save le jet de con
save.set_abilities(-1, 2, 2, 3, 5, -1)
save.set_saves(-1, 2, 2, 7, 9, -1)
save.set_action(name="Spellcasting", action_type="spell")
save.set_spell_slots(4, 3, 3, 3, 2, 1, 0, 0, 0)
save.set_spellbook(["Ice Storm", "Blight", "Thunderwave", ("Thorn Whip", "3d6")])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gaspard Maupassant", ac=19, hp=87, ini_mod=8, attack_mod=9, number_of_attacks=2, is_monster=False, sneak_attack_dices=6)
save.set_abilities(-1, 5, 1, 0, 0, 3)
save.set_saves(0, 10, 2, 5, 1, 4)
save.set_action(action_type="melee", name="Frost Brand Rapier", dice_rolls="1d8+1d6+5", damage_type="magical")
save.set_action(action_type="melee", name="Hand Crossbow", dice_rolls=[(1,6,5)])
save.save_main_stats()

### DND WITH THE BOYZ

save = MainStats()
save.set_main_stats("Ewyn", ac=20, hp=59, ini_mod=-1, ini_adv=True, attack_mod=6, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 12, 3)
save.set_abilities(3, -1, 4, 0, 0, 2)
save.set_saves(3, -1, 4, 0, 2, 4)
save.set_action(action_type="melee", name="Battleaxe", dice_rolls=[(1,8,3), (2,8,0)])
save.set_action(action_type="melee", name="Battleaxe", dice_rolls=[(1,8,3), (2,8,0)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gowon", ac=13, hp=43, ini_mod=2, attack_mod=8, number_of_attacks=2, is_monster=False, dc=14)
save.add_avg_dmg(1, 10, 0)
save.set_abilities(0, 2, 3, -1, 1, 4)
save.set_saves(0, 2, 3, -1, 3, 6)
save.set_action(action_type="range", name="Eldritch Blast", dice_rolls=[(1,10,4)], damage_type="force") # Eyldritch Bleeaaaassssttt
save.set_action(action_type="range", name="Eldritch Blast", dice_rolls=[(1,10,4)], damage_type="force")
save.save_main_stats()

save = MainStats() # on considère qu'il est toujours en rage, donc resistance et +2 sur damage
save.set_main_stats("Iaachus", ac=16, hp=44, ini_mod=2, attack_mod=5, number_of_attacks=1, is_monster=False, resistances=["nonmagical"])
save.add_avg_dmg(2, 6, 3)
save.set_abilities(3, 2, 4, -1, -1, 1)
save.set_saves(5, 2, 4, -1, -1, 1)
save.set_action(action_type="melee", name="Greatsword", dice_rolls=[(2,6,5)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Melvin", ac=15, hp=45, ini_mod=0, attack_mod=7, number_of_attacks=1, is_monster=False)
save.add_avg_dmg(4, 6, 0)
save.set_abilities(-1, 0, 1, 3, 4, 1)
save.set_saves(-1, 0, 1, 3, 6, 3)
save.set_action(action_type="ranged", name="Guiding Bolt", dice_rolls=[(5,6,0)], damage_type="radiant")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Reaghan", ac=13, hp=46, ini_mod=2, attack_mod=5, number_of_attacks=1, is_monster=False, dc=15)
save.add_avg_dmg(3, 6, 0)
save.set_abilities(0, 1, 3, 0, -1, 3)
save.set_saves(0, 3, 3, 0, -1, 5)
save.set_action(action_type="ranged", name="Dissonant Whispers", dice_rolls=[(3,6,0)], has_dc=True, dc_type="wis", has_attack_mod=False, damage_type="psychic")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vilgefortz", ac=16, hp=30, ini_mod=4, attack_mod=7, number_of_attacks=2, is_monster=False, sneak_attack_dices=3)
save.add_avg_dmg(1, 8, 3)
save.add_avg_dmg(1, 6, 0)
save.set_abilities(-1, 4, 0, 2, 0, 3)
save.set_saves(-1, 7, 0, 5, 0, 3)
save.set_action(action_type="melee", name="Psychic Blade", dice_rolls=[(1,6,4)], damage_type="psychic")
save.set_action(action_type="melee", name="Psychic Blade", dice_rolls=[(1,4,4)], damage_type="psychic")
save.save_main_stats()


save = MainStats()
save.set_main_stats("Ardorius", ac=16, hp=46, ini_mod=4, attack_mod=8, number_of_attacks=2, is_monster=False)
save.set_abilities(0, 4, 2, 2, 0, 1)
save.set_saves(0, 7, 2, 5, 0, 1)
save.set_action(action_type="melee", name="Rapier +1", dice_rolls="1d8+1d6", damage_type="magical")
save.set_action(action_type="melee", name="Rapier +1", dice_rolls="1d8+1d6", damage_type="magical")
save.save_main_stats()

