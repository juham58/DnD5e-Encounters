from Initiative_Module import Initiative_Module
import time
import statistics as st
import matplotlib.pyplot as plt
import numpy as np

def combat_analysis(iterations):
    start_time = time.process_time()
    results = []
    player_deaths_list = []
    for _ in range(iterations):
        ini = Initiative_Module()
        ini.import_group("Goblin", 50)
        ini.import_players(["John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
        combat_end = ini.combat(verbose=False)
        results.append(combat_end[0])
        player_deaths_list.append(combat_end[1])
    succes_rate = results.count(1)/len(results)*100
    avg_player_deaths = sum(player_deaths_list)/len(player_deaths_list)
    end_time = time.process_time() - start_time
    print("Total time:", end_time, "s")
    return (succes_rate, avg_player_deaths)

def monsters_test(iterations, monster_name, number_of_monsters, list_of_players):
    total_start_time = time.process_time()
    list_of_success_rates = []
    list_of_monsters = []
    list_of_time = []
    list_of_avg_player_deaths = []
    list_of_std_player_deaths = []
    results = []
    player_deaths_list = []
    for i in range(number_of_monsters):
        start_time = time.process_time()
        for _ in range(iterations):
            ini = Initiative_Module()
            ini.import_group(monster_name, i+1)
            ini.import_players(list_of_players)
            combat_end = ini.combat(verbose=False)
            results.append(combat_end[0])
            player_deaths_list.append(combat_end[1])
        succes_rate = results.count(1)/len(results)*100
        list_of_avg_player_deaths.append(st.mean(player_deaths_list))
        list_of_std_player_deaths.append(st.stdev(player_deaths_list))
        end_time = time.process_time() - start_time
        #print("Total time:", end_time, "s")
        list_of_success_rates.append(succes_rate)
        list_of_monsters.append(i+1)
        list_of_time.append(end_time)
    total_time = time.process_time() - total_start_time
    print("Total time:", total_time)
    plt.figure()
    plt.plot(list_of_monsters, list_of_success_rates)
    plt.xlabel("Nombre de {}s".format(monster_name))
    plt.ylabel("Pourcentage de réussite (pas tous mourir)")
    plt.title("Combien de {}s est trop de {}s?".format(monster_name, monster_name))
    plt.grid()

    plt.figure()
    plt.plot(list_of_monsters, list_of_avg_player_deaths)
    plt.fill_between(np.array(list_of_monsters), np.array(list_of_std_player_deaths)+np.array(list_of_avg_player_deaths), np.array(list_of_avg_player_deaths)-np.array(list_of_std_player_deaths), color='r', alpha=0.1)
    plt.ylim((0, len(list_of_players)))
    plt.grid()

    plt.figure()
    plt.plot(list_of_monsters, list_of_time)
    plt.grid()
    plt.show()

monsters_test(100, "Core Spawn Crawler", 20, ["Core Spawn Seer", "Gorgak Gro'brah", "John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
