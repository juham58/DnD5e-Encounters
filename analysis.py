from Initiative_Module import Initiative_Module

def combat_analysis(iterations):
    results = []
    for _ in range(iterations):
        test = Initiative_Module()
        test.import_group("Goblin", 8)
        test.import_stats("John")
        results.append(test.combat(verbose=False))
    succes_rate = results.count(1)/len(results)*100
    return succes_rate

print(combat_analysis(10000))
