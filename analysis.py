from Initiative_Module import Initiative_Module
import time
import matplotlib.pyplot as plt

def combat_analysis(iterations):
    start_time = time.process_time()
    results = []
    for _ in range(iterations):
        ini = Initiative_Module()
        ini.import_group("Goblin", 50)
        ini.import_players(["John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
        results.append(ini.combat(verbose=False))
    succes_rate = results.count(1)/len(results)*100
    end_time = time.process_time() - start_time
    print("Total time:", end_time, "s")
    return succes_rate

def monsters_test(iterations, monster_name, number_of_goblins, list_of_players):
    total_start_time = time.process_time()
    list_of_success_rates = []
    list_of_goblins = []
    list_of_time = []
    results = []
    for i in range(number_of_goblins):
        start_time = time.process_time()
        for _ in range(iterations):
            ini = Initiative_Module()
            ini.import_group(monster_name, i+1)
            ini.import_players(list_of_players)
            results.append(ini.combat(verbose=False))
        succes_rate = results.count(1)/len(results)*100
        end_time = time.process_time() - start_time
        #print("Total time:", end_time, "s")
        list_of_success_rates.append(succes_rate)
        list_of_goblins.append(i+1)
        list_of_time.append(end_time)
    total_time = time.process_time() - total_start_time
    print("Total time:", total_time)
    plt.figure()
    plt.plot(list_of_goblins, list_of_success_rates)
    plt.xlabel("Nombre de {}".format(monster_name))
    plt.ylabel("Pourcentage de réussite (pas tous mourir)")
    plt.title("Combien de {} est trop de {}?".format(monster_name, monster_name))
    plt.grid()
    plt.figure()
    plt.plot(list_of_goblins, list_of_time)
    plt.grid()
    plt.show()

monsters_test(500, "Hobgoblin Captain", 100, ["John", "Faramir", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"])
