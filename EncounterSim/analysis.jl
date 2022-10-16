using Plots
using ProgressBars
using Statistics
using DataFrames


include(pwd()*"\\EncounterSim\\initiative_module.jl")

#combat(["Goblin"], ["Gaspard Maupassant", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"], monster_name="Skeleton", number_of_monsters=10, verb=true)
function pre_import_stats(list_of_names)
    list_of_stats = []
    for name in list_of_names
        push!(list_of_stats, load_pickle(pwd()*"\\data\\stats_$name"))
    end
    return list_of_stats
end

function combat_analysis(n_iterations, monsters_list, players_list; verb=false)
    results = []
    player_deaths_list = []
    rounds = []
    players_damage = Dict()
    total_damage = 0
    monsters_stats = pre_import_stats(monsters_list)
    players_stats = pre_import_stats(players_list)
    spells = import_spells()
    for player in players_list
        players_damage[player] = 0
    end
    for _ in tqdm(1:1:n_iterations)
        combat_end = combat(deepcopy(monsters_stats), deepcopy(players_stats), verb=verb, spells=spells)
        push!(results, combat_end[1])
        push!(rounds, combat_end[3])
        if combat_end[1] == 1
            push!(player_deaths_list, combat_end[2])
        end
        if isempty(player_deaths_list)
            push!(player_deaths_list, length(players_list))
        end
        for player in players_list
            total_damage += combat_end[4][player]
            players_damage[player] += combat_end[4][player]
        end
    end
    dataframe_damage = DataFrame(Joueur=String[], pc_damage=Float64[], total_damage=Float64[])
    for player in players_list
        push!(dataframe_damage, [player, round(players_damage[player]*100/total_damage, digits=1), round(players_damage[player]/n_iterations)])
        #players_damage[player] = ["$(round(players_damage[player]*100/total_damage, digits=1))%", round(players_damage[player]/n_iterations)]
    end
    sort!(dataframe_damage, [:total_damage], rev=true)
    success_rate = round(mean(results)*100, digits=1)
    avg_player_deaths = round(mean(player_deaths_list), digits=1)
    avg_rounds = round(mean(rounds), digits=1)
    println("----\n")
    println("Success rate: ", success_rate, "%")
    println("Average players deaths: ", avg_player_deaths, " ± ", round(std(player_deaths_list), digits=1))
    println("Average number of rounds: ", avg_rounds, " ± ", round(std(rounds), digits=1))
    println("Average damage dealt by player:\n", dataframe_damage)
end

combat_analysis(1000, ["Caldriel"], ["Gaspard Maupassant", "Augustin", "Rand al'Thor", "Victoriana", "Dorran"], verb=false)