from Initiative_Module import Initiative_Module
import time
import statistics as st
import matplotlib.pyplot as plt
import numpy as np

def combat_analysis(iterations, monsters_list, list_of_players):
    start_time = time.process_time()
    results = []
    player_deaths_list = []
    rounds = []
    players_damage = {}
    for player in list_of_players:
        players_damage[player] = 0
    for _ in range(iterations):
        ini = Initiative_Module()
        ini.import_monsters(monsters_list)
        ini.import_players(list_of_players)
        combat_end = ini.combat(verbose=False)
        results.append(combat_end[0])
        player_deaths_list.append(combat_end[1])
        rounds.append(combat_end[2])
        for player in list_of_players:
            players_damage[player] += combat_end[3][player]
    for player in list_of_players:
        players_damage[player] = players_damage[player]/iterations
    succes_rate = results.count(1)/len(results)*100
    avg_player_deaths = sum(player_deaths_list)/len(player_deaths_list)
    avg_rounds = sum(rounds)/len(rounds)
    end_time = time.process_time() - start_time
    print("Total time:", end_time, "s")
    print("----\nSuccess rate:", succes_rate, "%", "\nAverage players deaths:", avg_player_deaths, "\nAverage number of rounds: ", avg_rounds, "\nAverage damage dealt by player:", players_damage, "\n----")

#combat_analysis(200, ["Tommy", "Tony"], ["Ewyn", "Gowon", "Melvin", "Reaghan", "Vilgefortz"])
combat_analysis(2000, ["Higher Vampire"], ["Gaspard Maupassant", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])

def monsters_test(iterations, monster_name, number_of_monsters, list_of_players, list_of_monsters_to_import=[], verbose=False):
    total_start_time = time.process_time()
    list_of_success_rates = []
    list_of_monsters = []
    list_of_time = []
    list_of_avg_player_deaths = []
    list_of_std_player_deaths = []
    list_of_avg_rounds = []
    list_of_std_rounds = []
    results = []
    player_deaths_list = []
    number_of_rounds = []
    players_damage = {}
    for player in list_of_players:
        players_damage[player] = 0
    for i in range(number_of_monsters):
        start_time = time.process_time()
        for _ in range(iterations):
            ini = Initiative_Module()
            ini.import_group(monster_name, i+1)
            ini.import_monsters(list_of_monsters_to_import)
            ini.import_players(list_of_players)
            combat_end = ini.combat(verbose=verbose)
            results.append(combat_end[0])
            player_deaths_list.append(combat_end[1])
            number_of_rounds.append(combat_end[2])
            for player in list_of_players:
                players_damage[player] += combat_end[3][player]
        succes_rate = results.count(1)/len(results)*100
        list_of_avg_player_deaths.append(st.mean(player_deaths_list))
        list_of_std_player_deaths.append(st.stdev(player_deaths_list))
        list_of_avg_rounds.append(st.mean(number_of_rounds))
        list_of_std_rounds.append(st.stdev(number_of_rounds))
        end_time = time.process_time() - start_time
        #print("Total time:", end_time, "s")
        list_of_success_rates.append(succes_rate)
        list_of_monsters.append(i+1)
        list_of_time.append(end_time)
    total_damage = 0
    for player in list_of_players:
        total_damage += players_damage[player]
    for player in list_of_players:
        players_damage[player] = 100*players_damage[player]/total_damage
    total_time = time.process_time() - total_start_time
    print("Total time:", total_time)
    plt.figure()
    plt.plot(list_of_monsters, list_of_success_rates)
    plt.xlim(left=1)
    plt.xlabel("Nombre de {}s".format(monster_name))
    plt.ylabel("Pourcentage de réussite (pas tous mourir)")
    plt.title("Combien de {}s est trop de {}s?".format(monster_name, monster_name))
    plt.grid()
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.figure()
    plt.plot(list_of_monsters, list_of_avg_player_deaths, label="Moyenne de morts de personnages")
    plt.fill_between(np.array(list_of_monsters), np.array(list_of_std_player_deaths)+np.array(list_of_avg_player_deaths), np.array(list_of_avg_player_deaths)-np.array(list_of_std_player_deaths), color='r', alpha=0.1, label="Écart type")
    plt.ylim((0, len(list_of_players)))
    plt.xlim(left=1)
    plt.xlabel("Nombre de {}s".format(monster_name))
    plt.ylabel("Nombre de morts de joueurs")
    plt.title("Nombre moyen et écart type de morts de joueurs en fonction du nombre de {}s".format(monster_name))
    plt.grid()
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.figure()
    plt.plot(list_of_monsters, list_of_avg_rounds, label="Nombre de rounds de combat")
    plt.fill_between(np.array(list_of_monsters), np.array(list_of_std_rounds)+np.array(list_of_avg_rounds), np.array(list_of_avg_rounds)-np.array(list_of_std_rounds), color='r', alpha=0.1, label="Écart type")
    plt.xlim(left=1)
    plt.xlabel("Nombre de {}s".format(monster_name))
    plt.ylabel("Nombre de rounds de combat")
    plt.title("Nombre moyen et écart type de rounds de combat en fonction du nombre de {}s".format(monster_name))
    plt.grid()
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.figure()
    plt.bar(players_damage.keys(), players_damage.values())
    plt.xlabel("Nom du joueur")
    plt.ylabel("Pourcentage de dommage fait en combat")
    plt.title("Pourcentage du dommage fait en combat parmis les joueurs sur toutes les itérations")
    plt.grid()
    
    plt.figure()
    plt.plot(list_of_monsters, list_of_time)
    plt.grid()
    plt.xlabel("Nombre de {}s".format(monster_name))
    plt.ylabel("Temps par itération [s]")
    plt.show()

#monsters_test(5, "Skeleton", 200, ["Gaspard Maupassant", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
#monsters_test(5, "Skeleton", 200, ["Gaspard Maupassant", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
#monsters_test(5, "Skeleton", 25, ["Victoriana"], verbose=True)
#monsters_test(100, "Skeleton", 25, ["Ewyn", "Gowon", "Iaachus", "Reaghan", "Vilgefortz", "Sartin"])







#monsters_test(50, "Skeleton", 150, ["John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
#monsters_test(300, "Thug", 10, ["Ewyn", "Gowon", "Iaachus", "Melvin", "Reaghan", "Vilgefortz"])
#monsters_test(100, "Werewolf", 10, ["John", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"], list_of_monsters_to_import=["Loup Garou"])
#monsters_test(50, "Jiangshi", 10, ["John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
#monsters_test(300, "Spined Devil", 10, ["Gowon", "Iaachus", "Reaghan", "Vilgefortz"], list_of_monsters_to_import=["Imp"])

#ini = Initiative_Module()
#ini.import_group("Core Spawn Crawler", 4)
#ini.import_players(["Core Spawn Seer", "Gorgak Gro'brah", "John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
#ini.combat(verbose=True)
