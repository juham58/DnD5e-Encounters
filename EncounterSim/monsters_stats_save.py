from Stats_Module import MainStats
import random

save = MainStats()
save.set_main_stats("Goblin", ac=15, hp=7, attack_mod=4)
save.add_avg_dmg(1, 6, 2)
save.set_abilities(-1, 2, 0, 0, -1, -1)
save.set_saves(-1, 2, 0, 0, -1, -1)
save.set_action(action_type="melee", name="Scimitar", dice_rolls=[(1,6,2)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Skeleton", ac=13, hp=13, attack_mod=4)
save.add_avg_dmg(1, 6, 2)
save.set_abilities(0, 2, 2, -2, -1, -3)
save.set_saves(0, 2, 2, -2, -1, -3)
save.set_action(action_type="melee", name="Shortsword", dice_rolls=[(1,6,2)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Hobgoblin Captain", ac=17, hp=39, attack_mod=6, number_of_attacks=2)
save.add_avg_dmg(2, 6, 2)
save.add_avg_dmg(2, 4, 0)
save.set_abilities(2, 2, 2, 1, 0, 1)
save.set_saves(2, 2, 2, 1, 0, 1)
save.set_action(action_type="melee", name="Greatsword", dice_rolls=[(2,6,2), (3,6,0)])
save.set_action(action_type="melee", name="Greatsword", dice_rolls=[(2,6,2)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Core Spawn Seer", ac=17, hp=153, ini_mod=1, attack_mod=8, number_of_attacks=2, dc=19)
save.add_avg_dmg(1, 6, 6+2) # Utilise seulement son attaque melee. +2 pour prendre en compte les debuff
save.add_avg_dmg(4, 8, 0)
save.set_abilities(2, 1, 4, 6, 4, 3)
save.set_saves(2, 6, 2, 11, 9, 8)
save.set_action(action_type="melee", name="Fission Staff", dice_rolls=[(1,6,6), (4,8,0), (1,6,0)], condition="Prone", auto_success=True)
save.set_action(action_type="ranged", name="Psychedelic Orb", dice_rolls=[(5,10,0)], has_dc=True, has_attack_mod=False, dc_type="wis", condition=random.choice(["Blinded", "Frightened", "Stunned"]), if_save="no_damage")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Core Spawn Crawler", ac=12, hp=21, ini_mod=2, attack_mod=4, number_of_attacks=4, dc=11)
save.add_avg_dmg(1, 4, 2) # Dommage moyen un peu moins bon que l'attaque Tail
save.set_abilities(-2, 2, 0, -1, 1, -2)
save.set_saves(-2, 2, 0, -1, 1, -2)
save.set_action(action_type="melee", name="Bite", dice_rolls=[(1,4,2)], has_dc_effect_on_hit=True, dc_effect_on_hit=[(0,0,0)], condition="Frightened", dc_type="wis", has_advantage=True)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,4,2)], has_advantage=True)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,4,2)], has_advantage=True)
save.set_action(action_type="melee", name="Tail", dice_rolls=[(1,6,2)], has_advantage=True)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Core Spawn Worm", ac=18, hp=279, ini_mod=-3, attack_mod=13, number_of_attacks=2, dc=18)
save.set_abilities(8, -3, 5, -2, -1, -3)
save.set_saves(8, -3, 10, -2, 4, -3)
save.set_action(action_type="melee", name="Barbed Tentacles", dice_rolls="5d6+8", has_dc_effect_on_hit=True, dc_effect_on_hit=[(0,0,0)], condition="Restrained", dc_type="dex")
save.set_action(action_type="melee", name="Bite", dice_rolls="5d8+4d6+8", has_dc=True, dc_effect_on_hit=["0"], condition="Blinded", dc_type="dex")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gorgak Gro'brah", ac=17, hp=155, ini_mod=5, attack_mod=11, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 10, 16) # Bonus de rage + dvivine fury divisée par 2
save.set_abilities(5, 2, 5, 1, 1, 2)
save.set_saves(9, 2, 9, 1, 1, 2)
save.set_action(action_type="melee", name="Meteor Core Halberd", dice_rolls=[(1,10,10), (1,6,4)])
save.set_action(action_type="melee", name="Meteor Core Halberd", dice_rolls=[(1,10,10)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Thug", ac=11, hp=32, attack_mod=4)
save.add_avg_dmg(1, 6, 2)
save.set_abilities(2, 0, 2, 0, 0, 0)
save.set_saves(2, 0, 2, 0, 0, 0)
save.set_action(action_type="melee", name="Mace", dice_rolls=[(1,6,2)], has_advantage=True) # approx que Pack Tactics est toujours vrai
save.save_main_stats()

save = MainStats()
save.set_main_stats("Stone Golem", ac=17, hp=178, attack_mod=10, number_of_attacks=2)
save.add_avg_dmg(3, 8, 6)
save.set_abilities(6, -1, 5, -4, 0, -5)
save.set_saves(6, -1, 5, -4, 0, -5)
save.set_action(action_type="melee", name="Slam", dice_rolls=["3d8+6"]) # on oublie l'abilité Slow
save.set_action(action_type="melee", name="Slam", dice_rolls=["3d8+6"])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Iron Golem", ac=20, hp=210, attack_mod=13, number_of_attacks=2)
save.add_avg_dmg(3, 8, 7)
save.set_abilities(6, -1, 5, -4, 0, -5)
save.set_saves(6, -1, 5, -4, 0, -5)
save.set_action(action_type="melee", name="Slam", dice_rolls=[(3,8,7)]) # on oublie l'abilité Poison Breath
save.set_action(action_type="melee", name="Sword", dice_rolls=[(3,10,7)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gold-Forged Sentinel", ac=16, hp=76, attack_mod=7, number_of_attacks=2)
save.add_avg_dmg(3, 8, 7)
save.set_abilities(4, 1, 4, -4, 3, 0)
save.set_saves(4, 1, 4, -4, 3, 0)
save.set_action(action_type="melee", name="Ram", dice_rolls=[(2,8,4)]) # on oublie l'abilité Fire Breath, Charge et Spell Turning
save.set_action(action_type="melee", name="Ram", dice_rolls=[(2,8,4)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Shadow Rand", ac=16, hp=38, dc=17, ini_mod=3, attack_mod=10, number_of_attacks=2)
save.add_avg_dmg(2, 6, 6)
save.add_avg_dmg(1, 10, 0) # estimation du bonus dommage pour différents spells de warlock i guess
save.set_abilities(-1, 5, -1, -1, 0, 5)
save.set_saves(-1, 5, -1, -1, 4, 9)
save.set_action(action_type="melee", name="Ruin's Wake", dice_rolls=[(3,8,9)]) # 3d8 sur chaque attaque pour approximer l'attaque en réaction
save.set_action(action_type="melee", name="Ruin's Wake", dice_rolls=[(3,8,9)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Demetriu", ac=18, hp=40, dc=15, ini_mod=5, attack_mod=9, number_of_attacks=4)
save.add_avg_dmg(2, 6, 6)
save.set_abilities(-1, 5, 3, 0, 3, 2)
save.set_saves(3, 9, 3, 0, 3, 2)
save.set_action(action_type="melee", name="Mace", dice_rolls=[(1,6,3)], has_advantage=True)
save.set_action(action_type="melee", name="Mace", dice_rolls=[(1,6,3)])
save.set_action(action_type="melee", name="Unarmed Strike", dice_rolls=[(1,6,3)])
save.set_action(action_type="melee", name="Unarmed Strike", dice_rolls=[(1,6,3)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Loup Garou", ac=16, hp=170, dc=17, ini_mod=4, attack_mod=9, number_of_attacks=2, regeneration=10, legend_actions_charges=3)
save.add_avg_dmg(2, 6, 6)
save.set_abilities(4, 4, 4, 2, 3, 3)
save.set_saves(4, 9, 9, 2, 3, 8)
save.set_action(action_type="melee", name="Bite", dice_rolls=[(2,8,4), (4,6,0)], has_advantage=True)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(2,6,4)], has_advantage=True, has_dc_effect_on_hit=True, condition="Prone", dc_type="str")
save.set_legend_action(action_type="melee", charge_cost=1, name="Swipe", dice_rolls=[(2,6,4)], has_advantage=True, has_dc_effect_on_hit=True, condition="Prone", dc_type="str")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Werewolf", ac=12, hp=58, dc=12, ini_mod=1, attack_mod=5, number_of_attacks=2)
save.add_avg_dmg(2, 6, 6)
save.set_abilities(2, 1, 2, 0, 0, 0)
save.set_saves(2, 1, 2, 0, 0, 0)
save.set_action(action_type="melee", name="Bite", dice_rolls=[(1,8,2)])
save.set_action(action_type="melee", name="Claws", dice_rolls=[(2,4,2)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Jiangshi", ac=16, hp=119, dc=16, ini_mod=1, attack_mod=8, number_of_attacks=4)
save.set_abilities(4, -4, 4, 3, 2, 1)
save.set_saves(4, -4, 8, 3, 6, 5)
save.set_action(action_type="melee", name="Slam", dice_rolls=[(2,8,4)])
save.set_action(action_type="melee", name="Slam", dice_rolls=[(2,8,4)])
save.set_action(action_type="melee", name="Slam", dice_rolls=[(2,8,4)])
save.set_action(action_type="melee", name="Consume Energy", dice_rolls=[(4,8,0)], has_attack_mod=False, has_dc=True, dc_type="con", is_heal=True, heal_type="damage_dealt")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Cultist", ac=12, hp=9, attack_mod=3)
save.set_abilities(0, 1, 0, 0, 0, 0)
save.set_saves(0, 1, 0, 0, 0, 0)
save.set_action(action_type="melee", name="Scimitar", dice_rolls=[(1,6,1)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Cult Fanatic", ac=13, hp=33, attack_mod=3)
save.set_abilities(0, 2, 1, 0, 1, 2)
save.set_saves(0, 2, 1, 0, 1, 2)
save.set_action(action_type="melee", name="Inflict Wounds", dice_rolls=[(4,10,0)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Imp", ac=13, hp=10, attack_mod=5, resistances=["cold", "nonmagical"], immunities=["fire", "poison"], dc=11)
save.set_abilities(-2, 3, 1, 0, 1, 2)
save.set_saves(-2, 3, 1, 0, 1, 2)
save.set_action(action_type="melee", name="Sting", dice_rolls=[(1,4,3)], has_dc_effect_on_hit=True, dc_type="con", dc_effect_on_hit=[(3,6,0)], damage_type="poison")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Barbed Devil", ac=15, hp=110, attack_mod=6, resistances=["cold", "nonmagical"], immunities=["fire", "poison"])
save.set_abilities(3, 3, 4, 1, 2, 2)
save.set_saves(6, 3, 7, 1, 5, 5)
save.set_action(action_type="melee", name="Claw", dice_rolls=[(1,6,3)])
save.set_action(action_type="melee", name="Claw", dice_rolls=[(1,6,3)])
save.set_action(action_type="melee", name="Tail", dice_rolls=[(2,6,3)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Spined Devil", ac=13, hp=22, attack_mod=2, resistances=["cold", "nonmagical"], immunities=["fire", "poison"])
save.set_abilities(0, 2, 1, 0, 2, -1)
save.set_saves(0, 2, 1, 0, 2, -1)
save.set_action(action_type="melee", name="Bite", dice_rolls=[(2,4,0)])
save.set_action(action_type="melee", name="Fork", dice_rolls=[(1,6,0)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Zyn Daev'yana", ac=19, hp=125, attack_mod=9, number_of_attacks=3, ini_mod=5)
save.set_abilities(0, 5, 5, 1, 3, 3)
save.set_saves(4, 5, 9, 1, 7, 3)
save.set_action(action_type="melee", name="Frost Brand Rapier", dice_rolls=[(1,8,7), (1,6,0)], has_advantage=True, damage_type="magical")
save.set_action(action_type="melee", name="Frost Brand Rapier", dice_rolls=[(1,8,7), (1,6,0)], has_advantage=True, damage_type="magical")
save.set_action(action_type="melee", name="Frost Brand Rapier", dice_rolls=[(1,8,7), (1,6,0)], damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Urmelena Mirimm", ac=18, hp=163, attack_mod=12, number_of_attacks=1, ini_mod=5, sneak_attack_dices=8)
save.set_abilities(1, 5, 3, 2, 2, 5)
save.set_saves(1, 10, 3, 7, 7, 5)
save.set_action(action_type="melee", name="Silken Spite", dice_rolls=[(1,8,7)], damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Ereldra Icoszrin", ac=22, hp=72, attack_mod=9, number_of_attacks=2, ini_mod=5)
save.set_abilities(-1, 5, 3, 5, 0, 0)
save.set_saves(-1, 5, 3, 9, 4, 0)
save.set_action(action_type="melee", name="Scimitar of Sharpness", dice_rolls=[(6,1,6)], damage_type="magical") # maximise le dommage et +1 pour dommage moyen de plus sur les crits
save.save_main_stats()

save = MainStats()
save.set_main_stats("Higher Vampire", ac=19, hp=250, dc=20, ini_mod=8, attack_mod=13, number_of_attacks=4, regeneration=50, legend_actions_charges=3, resistances=["nonmagical", "necrotic", "magical", "fire", "poison", "lightning", "force"], advantage_if_attacked=True)
save.set_abilities(4, 8, 5, 5, 2, 5)
save.set_saves(4, 13, 5, 5, 7, 10)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,10,8)], has_advantage=True)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,10,8)], has_advantage=True)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,10,8)], has_advantage=True)
save.set_action(action_type="melee", name="Bite", dice_rolls=[(1,6,8), (4,6,0)], has_advantage=True)
save.set_legend_action(action_type="melee", charge_cost=1, name="Claws", dice_rolls=[(1,10,8)], has_advantage=True)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Friendly Higher Vampire", ac=19, hp=250, dc=20, ini_mod=8, attack_mod=13, number_of_attacks=4, regeneration=50, legend_actions_charges=3, is_monster=False)
save.set_abilities(4, 8, 5, 5, 2, 5)
save.set_saves(4, 13, 5, 5, 7, 10)
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,10,8)])
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,10,8)])
save.set_action(action_type="melee", name="Claws", dice_rolls=[(1,10,8)])
save.set_action(action_type="melee", name="Bite", dice_rolls=[(1,6,8), (4,6,0)])
save.set_legend_action(action_type="melee", charge_cost=1, name="Claws", dice_rolls=[(1,10,8)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Tommy", ac=18, hp=148, dc=14, ini_mod=2, attack_mod=11, number_of_attacks=2)
save.set_abilities(5, 2, 4, 2, 0, 0)
save.set_saves(7, 8, 6, 6, 0, 0)
save.set_action(action_type="melee", name="Pike", dice_rolls=[(1,10,7), (1,8,0)])
save.set_action(action_type="melee", name="Pike", dice_rolls=[(1,10,7), (1,8,0)])
#save.set_action(action_type="melee", name="Pike", dice_rolls=[(1,4,6), (1,8,0)])
#save.set_legend_action(action_type="melee", charge_cost=1, name="Pike", dice_rolls=[(1,10,6), (1,8,0)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Tony", ac=20, hp=148, dc=14, ini_mod=2, attack_mod=11, number_of_attacks=2)
save.set_abilities(5, 2, 4, 2, 0, 0)
save.set_saves(7, 8, 6, 6, 0, 0)
save.set_action(action_type="melee", name="Morningstar", dice_rolls=[(1,10,9), (1,8,0)])
save.set_action(action_type="melee", name="Morningstar", dice_rolls=[(1,10,9), (1,8,0)])
#save.set_legend_action(action_type="melee", charge_cost=1, name="Morningstar", dice_rolls=[(1,10,8), (1,8,0)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Troglodyte", ac=11, hp=13, attack_mod=4, number_of_attacks=3)
save.set_abilities(2, 0, 2, -2, 0, -2)
save.set_saves(2, 0, 2, -2, 0, -2)
save.set_action(action_type="melee", name="Bite", dice_rolls=["1d4+2"])
save.set_action(action_type="melee", name="Claw", dice_rolls=["1d4+2"])
save.set_action(action_type="melee", name="Claw", dice_rolls=["1d4+2"])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Hobgoblin Devastator", ac=13, hp=45, attack_mod=5, dc=13, number_of_attacks=1)
save.set_abilities(1, 1, 2, 3, 1, 0)
save.set_saves(1, 1, 2, 3, 1, 0)
save.set_action(action_type="spell", name="Spellcasting")
save.set_spell_slots(4, 3, 3, 1, 0, 0, 0, 0, 0)
save.set_spellbook(["Ice Storm", "Fireball", "Thunderwave", ("Fire Bolt", "2d10")])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Hobgoblin Warlord", ac=20, hp=97, attack_mod=9, number_of_attacks=3)
save.set_abilities(3, 2, 3, 2, 0, 2)
save.set_saves(3, 2, 3, 5, 3, 5)
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d8+4d6+3")
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d8+3")
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d8+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vampire", ac=16, hp=144, dc=20, ini_mod=4, attack_mod=9, number_of_attacks=2, regeneration=20, legend_actions_charges=3, resistances=["nonmagical", "necrotic"])
save.set_abilities(4, 4, 4, 3, 2, 4)
save.set_saves(4, 9, 4, 3, 7, 9)
save.set_action(action_type="melee", name="Claws", dice_rolls="1d8+4")
save.set_action(action_type="melee", name="Bite", dice_rolls="1d6+3d6+4")
save.set_legend_action(action_type="melee", charge_cost=1, name="Claws", dice_rolls=[(1,8,4)])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vampire Spawn", ac=15, hp=82, dc=13, ini_mod=8, attack_mod=6, number_of_attacks=2, regeneration=10, resistances=["nonmagical", "necrotic"])
save.set_abilities(3, 3, 3, 0, 0, 1)
save.set_saves(3, 6, 3, 0, 3, 1)
save.set_action(action_type="melee", name="Claws", dice_rolls="2d4+3")
save.set_action(action_type="melee", name="Bite", dice_rolls="1d6+2d6+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vampire Spawn", ac=15, hp=82, attack_mod=6, number_of_attacks=2, resistances=["nonmagical", "necrotic"], regeneration=10)
save.set_abilities(6, 2, 4, 0, 0, 2)
save.set_saves(11, 2, 9, 0, 0, 2)
save.set_action(action_type="melee", name="Claws", dice_rolls="2d4+3")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d4+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vampire Spawn", ac=15, hp=82, attack_mod=6, number_of_attacks=2, creature_type="undead", resistances=["nonmagical", "necrotic"], regeneration=10)
save.set_abilities(6, 2, 4, 0, 0, 2)
save.set_saves(11, 2, 9, 0, 0, 2)
save.set_action(action_type="melee", name="Claws", dice_rolls="2d4+3")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d4+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Vampire", ac=16, hp=144, dc=18, ini_mod=4, attack_mod=9, number_of_attacks=2, legend_actions_charges=3, creature_type="undead", resistances=["necrotic", "nonmagical"], legend_resistances=3, regeneration=20)
save.set_abilities(4, 4, 4, 3, 2, 4)
save.set_saves(4, 9, 4, 3, 7, 9)
save.set_action(action_type="melee", name="Unarmed Strike", dice_rolls="1d8+4", damage_type="nonmagical")
save.set_action(action_type="melee", name="Bite", dice_rolls="3d6", damage_type="necrotic")
save.set_legend_action(action_type="melee", charge_cost=1, name="Unarmed Strike", dice_rolls="1d8+4", damage_type="nonmagical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Gnoll Pack Lord", ac=15, hp=49, attack_mod=5, number_of_attacks=3)
save.set_abilities(3, 2, 1, -1, 0, -1)
save.set_saves(3, 2, 1, -1, 0, -1)
save.set_action(action_type="melee", name="Glaive", dice_rolls="1d8+3")
save.set_action(action_type="melee", name="Glaive", dice_rolls="1d8+3")
save.set_action(action_type="melee", name="Bite", dice_rolls="1d8+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Purple Worm", ac=18, hp=350, dc=19, attack_mod=14, number_of_attacks=2)
save.set_abilities(9, -2, 6, -5, -1, -3)
save.set_saves(9, -2, 11, -5, 4, -3)
save.set_action(action_type="melee", name="Bite", dice_rolls="3d8+9", has_dc_effect_on_hit=True, condition="Blinded", dc_effect_on_hit="6d6", dc_type="dex")
save.set_action(action_type="melee", name="Tail Stinger", dice_rolls="3d6+9", has_dc_effect_on_hit=True, dc_effect_on_hit="12d6", dc_type="con")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Pestilence", ac=18, hp=350, dc=18, ini_mod=3, attack_mod=13, number_of_attacks=3, legend_actions_charges=3)
save.set_abilities(5, 3, 4, 2, 5, 4)
save.set_saves(10, 3, 9, 2, 10, 9)
save.set_action(action_type="melee", name="Bow of Sickness", dice_rolls="5d10+5")
save.set_action(action_type="melee", name="Bow of Sickness", dice_rolls="5d10+5")
save.set_action(action_type="melee", name="Bow of Sickness", dice_rolls="5d10+5")
save.set_legend_action(action_type="melee", charge_cost=1, name="Bow of Sickness", dice_rolls="5d10+5")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Ancient Blue Dragon", ac=22, hp=481, dc=23, ini_mod=0, attack_mod=16, number_of_attacks=3, legend_actions_charges=3, legend_resistances=3)
save.set_abilities(9, 0, 8, 4, 3, 5)
save.set_saves(9, 7, 15, 4, 10, 5)
save.set_action(action_type="melee", name="Bite", dice_rolls="2d10+9")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+9")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+9")
save.set_legend_action(action_type="melee", charge_cost=1, name="Tail Attack", dice_rolls="2d8+9")
save.set_action_in_arsenal(action_type="melee", name="Bite", dice_rolls="2d10+9")
save.set_action_in_arsenal(action_type="melee", name="Claws", dice_rolls="2d6+9")
save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Bite", "Claws", "Claws"])
save.set_action_in_arsenal(action_type="aoe", name="Lightning Breath", has_attack_mod=False, has_dc=True, dc_type="dex", dice_rolls="16d10", aoe_size=(120, 10), aoe_shape="line", damage_type="lightning", has_recharge=True, recharge=5)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Ancient Red Dragon", ac=22, hp=546, dc=24, ini_mod=0, attack_mod=17, number_of_attacks=3, legend_actions_charges=3, legend_resistances=3)
save.set_abilities(10, 0, 9, 4, 2, 6)
save.set_saves(10, 7, 16, 4, 9, 13)
save.set_action(action_type="melee", name="Bite", dice_rolls="2d10+10")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+10")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+10")
save.set_legend_action(action_type="melee", charge_cost=1, name="Tail Attack", dice_rolls="2d8+9")
save.set_action_in_arsenal(action_type="melee", name="Bite", dice_rolls="2d10+10")
save.set_action_in_arsenal(action_type="melee", name="Claws", dice_rolls="2d6+10")
save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Bite", "Claws", "Claws"])
save.set_action_in_arsenal(action_type="aoe", name="Fire Breath", has_attack_mod=False, has_dc=True, dc_type="dex", dice_rolls="26d6", aoe_size=90, aoe_shape="cone", damage_type="fire", has_recharge=True, recharge=5)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Ancient White Dragon", ac=20, hp=400, dc=22, ini_mod=0, attack_mod=15, number_of_attacks=3, legend_actions_charges=3, legend_resistances=3)
save.set_abilities(10, 0, 8, 0, 1, 2)
save.set_saves(10, 6, 14, 0, 7, 8)
save.set_action(action_type="melee", name="Bite", dice_rolls="2d10+8")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+8")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+8")
save.set_legend_action(action_type="melee", charge_cost=1, name="Tail Attack", dice_rolls="2d8+8")
save.set_action_in_arsenal(action_type="melee", name="Bite", dice_rolls="2d10+8+1d8")
save.set_action_in_arsenal(action_type="melee", name="Claws", dice_rolls="2d6+8")
save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Bite", "Claws", "Claws"])
save.set_action_in_arsenal(action_type="aoe", name="Cold Breath", has_attack_mod=False, has_dc=True, dc_type="dex", dice_rolls="16d8", aoe_size=90, aoe_shape="cone", damage_type="cold", has_recharge=True, recharge=5)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Young White Dragon", ac=17, hp=100, dc=15, ini_mod=0, attack_mod=7, number_of_attacks=3)
save.set_abilities(4, 0, 4, -2, 0, 1)
save.set_saves(4, 3, 7, -2, 3, 4)
save.set_action(action_type="melee", name="Bite", dice_rolls="2d10+4+1d8")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+4")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+4")
save.set_action_in_arsenal(action_type="melee", name="Bite", dice_rolls="2d10+4+1d8")
save.set_action_in_arsenal(action_type="melee", name="Claws", dice_rolls="2d6+4")
save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Bite", "Claws", "Claws"])
save.set_action_in_arsenal(action_type="aoe", name="Cold Breath", has_attack_mod=False, has_dc=True, dc_type="dex", dice_rolls="10d8", aoe_size=30, aoe_shape="cone", damage_type="cold", has_recharge=True, recharge=5)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Battleforce Angel", ac=14, hp=45, ini_mod=1, attack_mod=6, number_of_attacks=2)
save.set_abilities(3, 1, 1, 0, 3, 4)
save.set_saves(3, 1, 1, 0, 6, 7)
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d10+4d8+1d4+3")
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d10+4d8+1d4+3")
save.set_action_in_arsenal(action_type="melee", name="Longsword", dice_rolls="1d10+4d8+1d4+3")
save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Longsword", "Longsword"])
save.save_main_stats()

save = MainStats()
save.set_main_stats("Caldriel", ac=21, hp=400, dc=26, ini_mod=7, attack_mod=16, number_of_attacks=3, legend_actions_charges=0, legend_resistances=3, regeneration=0, is_mythic=True, mythic_hp=300, magic_resistance=True, resistances=["cold", "radiant"], immunities=["necrotic", "poison"], focus_type="focused")
save.set_abilities(8, 7, 9, 8, 8, 10)
save.set_saves(8, 7, 9, 16, 16, 18)
save.set_action(action_type="melee", name="Flail", dice_rolls="2d8+8d8+8", damage_type="force")
save.set_action(action_type="melee", name="Flail", dice_rolls="2d8+8d8+8", damage_type="force")
save.set_action(action_type="melee", name="Longsword", dice_rolls="2d8+8d8+8", damage_type="radiant")
#save.set_legend_action(action_type="melee", charge_cost=3, name="Flail", dice_rolls="2d8+8d8+8", damage_type="force")
save.set_action_in_arsenal(action_type="melee", name="Flail", dice_rolls="2d8+8d8+8", damage_type="force")
save.set_action_in_arsenal(action_type="melee", name="Longsword", dice_rolls="2d8+8d8+8", damage_type="radiant")
save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Flail", "Longsword", "Flail"])
#save.set_action_in_arsenal(action_type="melee", name="Horrid Touch", has_attack_mod=False, has_dc=True, dc_type="con", dice_rolls="8d10", damage_type="necrotic", has_recharge=True, recharge=5, condition="poisoned")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Leitmotif", ac=20, hp=223, ini_mod=5, attack_mod=14, number_of_attacks=2, sneak_attack_dices=10, disadvantage_if_attacked=True, legend_resistances=3, legend_actions_charges=3)
save.set_abilities(-1, 5, 5, 1, 0, 5)
save.set_saves(-1, 11, 5, 7, 6, 5)
save.set_action(action_type="melee", name="Silken Spite", dice_rolls="1d8+8", damage_type="magical")
save.set_action(action_type="ranged", name="Hand Crossbow", dice_rolls="1d6+8", damage_type="magical")
save.set_legend_action(action_type="ranged", charge_cost=1, name="Hand Crossbow", dice_rolls="1d6+4d6+8", damage_type="magical")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Thanatos", ac=20, hp=150, dc=20, ini_mod=3, attack_mod=12, number_of_attacks=1, regeneration=0, legend_actions_charges=3, legend_resistances=3, resistances=["cold", "lightning", "necrotic"])
save.set_abilities(0, 3, 3, 5, 2, 3)
save.set_saves(0, 3, 10, 12, 9, 3)
save.set_action(action_type="spell", name="Spellcasting")
save.set_spell_slots(4, 3, 3, 3, 3, 2, 1, 1, 1)
save.set_spellbook(["Horrid Wilting", "Finger of Death", "Disintegrate", "Blight", "Fireball", ("Ray of Frost", "4d8")])
save.set_legend_action(action_type="ranged", charge_cost=1, name="Ray of Frost", dice_rolls="4d8", damage_type="cold")
#save.set_action_in_arsenal(action_type="melee", name="Flail", dice_rolls="2d8+8d8+8", damage_type="force")
#save.set_action_in_arsenal(action_type="melee", name="Longsword", dice_rolls="2d8+8d8+8", damage_type="radiant")
#save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Flail", "Flail", "Flail"])
#save.set_action_in_arsenal(action_type="melee", name="Horrid Touch", has_attack_mod=False, has_dc=True, dc_type="con", dice_rolls="8d10", damage_type="necrotic", has_recharge=True, recharge=5, condition="poisoned")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Pool of Souls", ac=15, hp=200, dc=20, ini_mod=0, attack_mod=0, number_of_attacks=1, regeneration=20, legend_actions_charges=0, legend_resistances=0, immunities=["nonmagical", "psychic"])
save.set_abilities(0, 3, 3, 5, 2, 3)
save.set_saves(40, -5, 40, 90, 90, 90)
save.set_action(action_type="ranged", name="Souls of the Dead", has_attack_mod=False, has_dc=True, dc_type="con", dice_rolls="15d6", damage_type="necrotic")
#save.set_spell_slots(4, 3, 3, 3, 3, 1, 1, 1, 1)
#save.set_spellbook(["Thunderwave", "Fireball", "Blight", "Disintegrate", "Finger of Death", ("Ray of Frost", "4d8")])
#save.set_legend_action(action_type="ranged", charge_cost=1, name="Ray of Frost", dice_rolls="4d8", damage_type="cold")
#save.set_action_in_arsenal(action_type="melee", name="Flail", dice_rolls="2d8+8d8+8", damage_type="force")
#save.set_action_in_arsenal(action_type="melee", name="Longsword", dice_rolls="2d8+8d8+8", damage_type="radiant")
#save.set_action_in_arsenal(action_type="multiattack", name="Multiattack", multiattack_list=["Flail", "Flail", "Flail"])
#save.set_action_in_arsenal(action_type="melee", name="Horrid Touch", has_attack_mod=False, has_dc=True, dc_type="con", dice_rolls="8d10", damage_type="necrotic", has_recharge=True, recharge=5, condition="poisoned")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Bandit", ac=12, hp=11, attack_mod=3)
save.set_abilities(0, 1, 1, 0, 0, 0)
save.set_saves(0, 1, 1, 0, 0, 0)
save.set_action(action_type="melee", name="Scimitar", dice_rolls="1d6+1")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Bandit Captain", ac=15, hp=65, attack_mod=5, number_of_attacks=2)
save.set_abilities(2, 3, 2, 2, 0, 2)
save.set_saves(4, 5, 2, 2, 2, 2)
save.set_action(action_type="melee", name="Scimitar", dice_rolls="1d6+3")
save.set_action(action_type="melee", name="Scimitar", dice_rolls="1d6+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Dragours vert", ac=12, hp=120, attack_mod=7, number_of_attacks=4)
save.set_abilities(5, 0, 3, -4, 1, -2)
save.set_saves(5, 0, 3, -4, 1, -2)
save.set_action(action_type="melee", name="Bite", dice_rolls="3d8+5")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+5")
save.set_action(action_type="melee", name="Claws", dice_rolls="2d6+5")
save.set_action(action_type="aoe", name="Exhale Poison", has_attack_mod=False, has_dc=True, is_aoe=True, dc_type="con", dice_rolls="3d6", aoe_shape="square", aoe_size=15, damage_type="poison")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Necrichor", ac=12, hp=250, attack_mod=6, number_of_attacks=4, legend_resistances=2, focus_type="focused")
save.set_abilities(-1, 2, 3, 3, 1, 0)
save.set_saves(-1, 2, 6, 6, 4, 0)
save.set_action(action_type="melee", name="Pseudopod", dice_rolls="2d6+3", has_dc_effect_on_hit=True, condition="Paralyzed", dc_type="con")
save.set_action(action_type="ranged", name="Necrotic Bolt", dice_rolls="3d8+3")
save.set_action(action_type="ranged", name="Necrotic Bolt", dice_rolls="3d8+3")
save.set_action(action_type="ranged", name="Necrotic Bolt", dice_rolls="3d8+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Zombtrouille", ac=8, hp=1, attack_mod=3, number_of_attacks=1)
save.set_abilities(1, -2, 3, -4, -2, -3)
save.set_saves(1, -2, 3, -4, 0, -3)
save.set_action(action_type="melee", name="Slam", dice_rolls="1d6+1")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Veteran", ac=17, hp=58, attack_mod=5, number_of_attacks=2)
save.set_abilities(3, 1, 2, 0, 0, 0)
save.set_saves(3, 1, 2, 0, 0, 0)
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d10+3")
save.set_action(action_type="melee", name="Longsword", dice_rolls="1d10+3")
save.save_main_stats()

save = MainStats()
save.set_main_stats("Cerbère-Hydre", ac=17, hp=200, attack_mod=10, number_of_attacks=5, focus_type="focused")
save.set_abilities(6, 0, 6, -4, 0, -2)
save.set_saves(6, 0, 6, -4, 0, -2)
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.set_action(action_type="melee", name="Bite", dice_rolls="2d6+6")
save.add_custom_combat_stat("number_of_heads", 5)
save.add_custom_stat("hp_threshold_for_head_removal", 40)
save.save_main_stats()

save = MainStats()
save.set_main_stats("Assassin", ac=15, hp=78, attack_mod=6, number_of_attacks=2, ini_mod=4, sneak_attack_dices=4, dc=15)
save.set_abilities(1, 3, 2, 1, 0, 0)
save.set_saves(1, 6, 2, 4, 0, 0)
save.set_action(action_type="melee", name="Shortsword", dice_rolls="1d6+3", dc_type="con", has_dc_effect_on_hit=True, dc_effect_on_hit="7d6", condition="Poison Damage")
save.set_action(action_type="melee", name="Shortsword", dice_rolls="1d6+3", dc_type="con", has_dc_effect_on_hit=True, dc_effect_on_hit="7d6", condition="Poison Damage")
save.save_main_stats()


save = MainStats()
save.set_main_stats("Master Assassin", ac=18, hp=300, attack_mod=8, number_of_attacks=2, ini_mod=4, sneak_attack_dices=8, dc=15)
save.set_abilities(1, 5, 2, 1, 0, 0)
save.set_saves(1, 8, 2, 4, 0, 0)
save.set_action(action_type="melee", name="Shortsword", dice_rolls="1d6+5", dc_type="con", has_dc_effect_on_hit=True, dc_effect_on_hit="12d6", condition="Poison Damage")
save.set_action(action_type="melee", name="Shortsword", dice_rolls="1d6+5", dc_type="con", has_dc_effect_on_hit=True, dc_effect_on_hit="12d6", condition="Poison Damage")
save.save_main_stats()
