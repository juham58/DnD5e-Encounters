from Stats_Module import MainStats

save = MainStats()
save.set_main_stats("Goblin", ac=15, hp=7, attack_mod=4)
save.add_avg_dmg(1, 6, 2)
save.save_main_stats()

save.set_main_stats("Skeleton", ac=13, hp=13 attack_mod=4)
save.add_avg_dmg(1, 6, 2)
save.save_main_stats()

save.set_main_stats("John", ac=17, hp=83, dc=15, ini_mod=5, attack_mod=10, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 8, 8)
save.add_avg_dmg(1, 6, 0) # Rite of the dawn
save.save_main_stats()

save.set_main_stats("Faramir", ac=18, hp=77, dc=16, ini_mod=0, attack_mod=8, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 10, 4)
save.add_avg_dmg(2, 8, 0) # Si divine smite lvl 1 à chaque attaque
save.save_main_stats()

save.set_main_stats("Augustin", ac=22, hp=56, dc=17, ini_mod=2, attack_mod=10, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(1, 6, 6)
save.add_avg_dmg(0, 0, 5) # Estimation du dommage bonus pour sharpshooter
save.save_main_stats()

save.set_main_stats("Rand al'Thor", ac=16, hp=69, dc=17, ini_mod=3, attack_mod=10, number_of_attacks=2, is_monster=False)
save.add_avg_dmg(2, 6, 6)
save.add_avg_dmg(1, 10, 0) # estimation du bonus dommage pour différents spells de warlock i guess
save.save_main_stats()

save.set_main_stats("Victoriana", ac=16, hp=56, dc=17, ini_mod=8, attack_mod=10, number_of_attacks=1, is_monster=False) # avec mage armor
save.add_avg_dmg(7, 8, 0) # basé sur Chromatic orb lvl 5
save.save_main_stats()

save.set_main_stats("Dorran", ac=15, hp=107, dc=12, ini_mod=1, attack_mod=4, number_of_attacks=3, is_monster=False) # basé sur Giant Scorpion
save.add_avg_dmg(1, 8, 2)
save.add_avg_dmg(2, 10, 0) # estimation du 4d10 si la moitié du monde save le jet de con
save.save_main_stats()

save.set_main_stats("Hobgoblin Captain", ac=17, hp=39, attack_mod=6, number_of_attacks=2)
save.add_avg_dmg(2, 6, 2)
save.add_avg_dmg(2, 4, 0)
save.save_main_stats()

save.set_main_stats("Core Spawn Seer", ac=17, hp=153, ini_mod=1, attack_mod=8, number_of_attacks=2, dc=19)
save.add_avg_dmg(1, 6, 6+2) # Utilise seulement son attaque melee. +2 pour prendre en compte les debuff
save.add_avg_dmg(4, 8, 0)
save.save_main_stats()

save.set_main_stats("Core Spawn Crawler", ac=12, hp=21, ini_mod=2, attack_mod=4, number_of_attacks=4, dc=11)
save.add_avg_dmg(1, 4, 2) # Dommage moyen un peu moins bon que l'attaque Tail
save.save_main_stats()

save.set_main_stats("Gorgak Gro'brah", ac=17, hp=155, ini_mod=5, attack_mod=11, number_of_attacks=2, is_monster=False) # basé sur Giant Scorpion
save.add_avg_dmg(1, 10, 16) # Bonus de rage + dvivine fury divisée par 2
save.save_main_stats()
