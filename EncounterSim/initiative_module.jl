

using PyCall
using ProgressBars
using Statistics
using Random

d20 = pyimport("d20")
pickle = pyimport("pickle")

global combatants_stats = Dict()
global combatants_hp = Dict()
global combatants_names = []
global players_names = []
global monsters_names = []
global ini_order = []
global legendary_monsters = []
global legend_actions_order = Dict()
global player_deaths = 0
global verbose = true
global pythagore = false
global conditions_list = ["Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious"]
global spells_database = Dict()

function load_pickle(filename)
    r = nothing
    @pywith pybuiltin("open")(filename, "rb") as f begin
        r = pickle.load(f)
    end
    return r
end

function import_stats(name)
    stats = load_pickle(pwd()*"\\data\\stats_$name")
    #println(stats["Skeleton"])
    combatants_stats[name] = stats[name]
    combatants_hp[name] = stats[name]["max_hp"]
    push!(combatants_names, name)
    if length(combatants_stats[name]["legend_actions"]) > 0
        push!(legendary_monsters, name)
    end
    if combatants_stats[name]["is_monster"]
        push!(monsters_names, name)
    else
        push!(players_names, name)
    end
end

function import_group(base_name, quantity)
    stats = load_pickle(pwd()*"\\data\\stats_$base_name")
    for n in 1:1:quantity
        new_name = "$(base_name)_$n"
        new_dict = stats[base_name]
        combatants_stats[new_name] = new_dict
        combatants_hp[new_name] = new_dict["max_hp"]
        push!(combatants_names, new_name)
        if length(combatants_stats[new_name]["legend_actions"]) > 0
            push!(legendary_monsters, new_name)
        end
        if combatants_stats[new_name]["is_monster"]
            push!(monsters_names, new_name)
        else
            push!(players_names, new_name)
        end
    end
end

function import_players(list_of_players)
    for name in list_of_players
        import_stats(name)
    end
end

function import_monsters(list_of_monsters)
    if length(list_of_monsters) > 1
        for name in list_of_monsters
            import_stats(name)
        end
    end
end

function import_spells()
    global spells_database = load_pickle(pwd()*"\\data\\spells_database")
end

function roll_d20(; adv=false, dis=false)
    if (adv && dis) || (!adv && !dis)
        #return d20.roll("1d20").total
        roll = rand(1:20)
        println("r: ", roll)
        return roll
    elseif (adv && !dis)
        r1 = rand(1:20)
        r2 = rand(1:20)
        println("r1: ", r1, " r2: ", r2)
        if r1 >= r2
            return r1
        else
            return r2
        end
        #return d20.roll("2d20kh1").total
    elseif (!adv && dis)
        r1 = rand(1:20)
        r2 = rand(1:20)
        println("r1: ", r1, " r2: ", r2)
        if r1 <= r2
            return r1
        else
            return r2
        end
        #return d20.roll("2d20kl1").total
    end
end

function convert_dice_to_string(dice_input)
    if isa(dice_input, AbstractString)
        return dice_input
    elseif isa(dice_input, AbstractVector)
        dice_output = ""
        total_damage_modifier = 0
        for (i, dice) in enumerate(dice_input)
            if i == 1
                dice_output *= "$(dice[1])d$(dice[2])"
            else
                dice_output *= "+$(dice[1])d$(dice[2])"
            end
            total_damage_modifier += dice[3]
        end
        return dice_output
    elseif isa(dice_input, Tuple)
        return "$(dice_input[1])d$(dice_input[2])+$(dice_input[3])"
    else
        println("ERROR: dice_input must be vector, tuple or string")
    end
end

function roll_dice(dice_input)
    return d20.roll(convert_dice_to_string(dice_input)).total
end

function calculate_crit_damage(attacker_name, dice_input)
    valeurs = eachmatch(r"\d?\d?\d?\d(?=d)", dice_input)
    for (n, m) in enumerate(valeurs)
        valeur_crit = string(2*parse(Int, collect(valeurs)[n].match))
        # brutal critical
        if n == 1
            valeur_crit = string(parse(Int, valeur_crit) + combatants_stats[attacker_name]["brutal_critical"])
        end
        len_match = length(m.match)
        if m.offset > 1
            dice_input = dice_input[1:m.offset-1] * replace(dice_input[m.offset:m.offset+len_match-1], dice_input[m.offset:m.offset+len_match-1] => valeur_crit) * dice_input[m.offset+1:end]
        else
            dice_input = replace(dice_input[m.offset:m.offset+len_match-1], dice_input[m.offset:m.offset+len_match-1] => valeur_crit) * dice_input[m.offset+1:end]
        end
    end
    return d20.roll(dice_input).total
end

function roll_ini()
    temp_dict = Dict()
    for name in combatants_names
        ini_roll = roll_d20(adv=combatants_stats[name]["ini_adv"])+combatants_stats[name]["ini_mod"]
        temp_dict[ini_roll] = name
    end
    global ini_order = sort(collect(temp_dict), rev=true)
    println(ini_order)
end

function choose_inspiration_target(bard_name, target_list)
    target_choice = rand(target_list)
    if target_choice == bard_name
        if length(target_list) == 1
            return nothing
        end
        return choose_inspiration_target(bard_name, target_list)
    else
        return target_choice
    end
end

function give_bardic_inspiration(bard_name, target_name)
    if !isnothing(target_name)
        combatants_stats[target_name]["combat_stats"]["has_bardic_inspiration"] = combatants_stats[bard_name]["bardic_inspiration"]
        combatants_stats[bard_name]["combat_stats"]["bardic_inspiration_charges"] -= 1
        #logging.info("{} gave a {} bardic inspiration to {}".format(bard_name, combatants_stats[bard_name]["bardic_inspiration"][1], target_name))
    end
end

function use_bardic_inspiration(user_name)
    combatants_stats[user_name]["combat_stats"]["has_bardic_inspiration"][0] = false
    bonus = roll_dice(combatants_stats[user_name]["combat_stats"]["has_bardic_inspiration"][1])
    #logging.info("{} used a {} bardic inspiration and added {} to their roll".format(user_name, combatants_stats[user_name]["combat_stats"]["has_bardic_inspiration"][1], bonus))
    return bonus
end

function dc_check(combatant_name, dc, stat; adv=false, dis=false)
    if stat == "str" && "Petrified" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        return false
    elseif stat == "dex" && "Petrified" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        return false
    elseif stat == "str" && "Stunned" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        return false
    elseif stat == "dex" && "Stunned" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        return false
    elseif stat == "str" && "Unconscious" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        return false
    elseif stat == "dex" && "Unconscious" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        return false
    elseif stat == "dex" && "Restrained" in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        dis = true
    end
    save_bonus = combatants_stats[combatant_name]["saves"][stat]
    roll = roll_d20(adv=adv, dis=dis)+save_bonus
    if combatants_stats[combatant_name]["combat_stats"]["has_bardic_inspiration"][1]
        roll += use_bardic_inspiration(combatant_name)
    end
    if combatants_stats[combatant_name]["legend_resistances"] > 0
        roll = dc
        combatants_stats[combatant_name]["legend_resistances"] -=1
        if verbose
            println("$combatant_name uses a legendary resistance.")
        end
    end
    if roll >= dc
        return true
    else
        return false
    end
end

function reset_condition(combatant_name, condition_name, dc, stat)
    #logging.info("Condition RESET: {}, Combatant name: {}".format(condition_name, combatant_name))
    if condition_name == "Blinded"
        combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
        combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
    elseif condition_name == "Charmed"
        #pass
    elseif condition_name == "Deafened"
        #pass
    elseif condition_name == "Frightened"
        combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
    elseif condition_name == "Grappled"
        #pass
    elseif condition_name == "Incapacitated"
        #pass
    elseif condition_name == "Invisible"
        combatants_stats[combatant_name]["combat_stats"]["advantage_on_attack"] = true
        combatants_stats[combatant_name]["combat_stats"]["disadvantage_if_attacked"] = true
    elseif condition_name == "Paralyzed"
        reset_condition(combatant_name, "Incapacitated", dc, stat)
        combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
    elseif condition_name == "Petrified"
        combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
        # resistance to all damage
    elseif condition_name == "Poisoned"
        combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
    elseif condition_name == "Prone"
        # adv if attacked si attque melee et dis if attacked si attaque ranged
        #pass
    elseif condition_name == "Restrained"
        combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
        combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
    elseif condition_name == "Stunned"
        reset_condition(combatant_name, "Incapacitated", dc, stat)
        combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
    elseif condition_name == "Unconscious"
        reset_condition(combatant_name, "Incapacitated", dc, stat)
        combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
    end
end

function remove_condition(combatant_name, condition_name)
    #logging.info("Condition removed: {} Combatant name: {}".format(condition_name, combatant_name))
    #logging.info("Conditions list (remove_condition before removal): {}".format(combatants_stats[combatant_name]["combat_stats"]["conditions"]))
    if condition_name in combatants_stats[combatant_name]["combat_stats"]["conditions"]
        #combatants_stats[combatant_name]["combat_stats"]["conditions"].remove(condition_name)
        filter!(e -> e != condition_name, combatants_stats[combatant_name]["combat_stats"]["conditions"])
        #logging.info("Conditions list (remove_condition after removal): {}".format(combatants_stats[combatant_name]["combat_stats"]["conditions"]))
        for (index, condition) in enumerate(combatants_stats[combatant_name]["combat_stats"]["conditions_info"])
            #logging.info("Index: {}, Condition: {}".format(index, condition))
            if condition[1] == condition_name
                #logging.info("Condition at removed index: {}, Condition to be removed: {}".format(combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index], condition))
                #del combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index]
                deleteat!(combatants_stats[combatant_name]["combat_stats"]["conditions_info"], index)
                continue
            end
        end
        if condition_name == "Blinded"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = false
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = false
        elseif condition_name == "Charmed"
            #pass
        elseif condition_name == "Deafened"
            #pass
        elseif condition_name == "Frightened"
            #pass
        elseif condition_name == "Grappled"
            #pass
        elseif condition_name == "Incapacitated"
            #pass
        elseif condition_name == "Invisible"
            combatants_stats[combatant_name]["combat_stats"]["advantage_on_attack"] = false
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_if_attacked"] = false
        elseif condition_name == "Paralyzed"
            remove_condition(combatant_name, "Incapacitated")
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = false
        elseif condition_name == "Petrified"
            #pass
        elseif condition_name == "Poisoned"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = false
        elseif condition_name == "Prone"
            #pass
        elseif condition_name == "Restrained"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = false
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = false
        elseif condition_name == "Stunned"
            remove_condition(combatant_name, "Incapacitated")
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = false
        elseif condition_name == "Unconscious"
            remove_condition(combatant_name, "Incapacitated")
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = false
        elseif length(combatants_stats[combatant_name]["combat_stats"]["conditions"]) != 0
            for condition in combatants_stats[combatant_name]["combat_stats"]["conditions"]
                for element in combatants_stats[combatant_name]["combat_stats"]["conditions_info"]
                    if condition == element[1] && condition != condition_name
                        reset_condition(combatant_name, condition, element[2], element[3])
                    end
                end
            end
        end
    end
end

function condition_check(combatant_name, adv=false, dis=false)
    if length(combatants_stats[combatant_name]["combat_stats"]["conditions"]) != 0
        for condition in conditions_list
            if condition == "Prone"
                remove_condition(combatant_name, condition)
                continue
            end
            if condition in combatants_stats[combatant_name]["combat_stats"]["conditions"]
                #logging.info("Condition check FOUND: {}, combatant_name: {}".format(condition, combatant_name))
                #logging.info("Conditions info list: {}".format(combatants_stats[combatant_name]["combat_stats"]["conditions_info"]))
                index = findall(x->x == condition, combatants_stats[combatant_name]["combat_stats"]["conditions"])[1]
                dc = combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index][2]
                stat = combatants_stats[combatant_name]["combat_stats"]["conditions_info"][index][3]
                if dc_check(combatant_name, dc, stat, adv=adv, dis=dis) && condition != "Unconscious"
                    #logging.info("Condition save: {}, Combatant name: {}".format(condition, combatant_name))
                    remove_condition(combatant_name, condition)
                end
            end
        end
    end
end

function set_condition(combatant_name, condition_name, dc, stat)
    if !(condition_name in combatants_stats[combatant_name]["combat_stats"]["conditions"])
        #logging.info("Condition set: {}, Combatant name: {}".format(condition_name, combatant_name))
        push!(combatants_stats[combatant_name]["combat_stats"]["conditions"], condition_name)
        push!(combatants_stats[combatant_name]["combat_stats"]["conditions_info"], (condition_name, dc, stat))
        if condition_name == "Blinded"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
        elseif condition_name == "Charmed"
            #pass
        elseif condition_name == "Deafened"
            #pass
        elseif condition_name == "Frightened"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
        elseif condition_name == "Grappled"
            #pass
        elseif condition_name == "Incapacitated"
            #pass
        elseif condition_name == "Invisible"
            combatants_stats[combatant_name]["combat_stats"]["advantage_on_attack"] = true
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_if_attacked"] = true
        elseif condition_name == "Paralyzed"
            set_condition(combatant_name, "Incapacitated", dc, stat)
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
        elseif condition_name == "Petrified"
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
            # resistance to all damage
        elseif condition_name == "Poisoned"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
        elseif condition_name == "Prone"
            # adv if attacked si attque melee et dis if attacked si attaque ranged
            #pass
        elseif condition_name == "Restrained"
            combatants_stats[combatant_name]["combat_stats"]["disadvantage_on_attack"] = true
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
        elseif condition_name == "Stunned"
            set_condition(combatant_name, "Incapacitated", dc, stat)
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
        elseif condition_name == "Unconscious"
            set_condition(combatant_name, "Incapacitated", dc, stat)
            combatants_stats[combatant_name]["combat_stats"]["advantage_if_attacked"] = true
        end
    end
end

function heal(combatant_name, heal_amount)
    if heal_amount > 0
        combatants_hp[combatant_name] += heal_amount
        if combatants_stats[combatant_name]["max_hp"] <= combatants_hp[combatant_name]
            combatants_hp[combatant_name] = combatants_stats[combatant_name]["max_hp"]
        end
        if combatants_stats[combatant_name]["combat_stats"]["is_downed"]
            combatants_stats[combatant_name]["combat_stats"]["death_saves"][1] = 0
            combatants_stats[combatant_name]["combat_stats"]["death_saves"][2] = 0
            combatants_stats[combatant_name]["combat_stats"]["is_downed"] = false
            remove_condition(combatant_name, "Unconscious")
        end
    end
end

function dc_attack(attacker_name, target_name, attack_value)
    dice_rolls = attack_value["dice_rolls"]
    dc_type = attack_value["dc_type"]
    dc = combatants_stats[attacker_name]["dc"]
    dc_result = dc_check(target_name, dc, dc_type)
    if attack_value["condition"] != "" && dc_result == false
        set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
    end
    damage = 0
    damage += roll_dice(dice_rolls)

    if !dc_result
        combatants_hp[target_name] -= damage
        combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
        if attack_value["is_heal"] && attack_value["heal_type"] == "damage_dealt"
            heal(attacker_name, damage)
        end
        if combatants_stats[target_name]["combat_stats"]["is_downed"]
            combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 1
        end
        if verbose
            println(target_name, " fails to meet DC of ", dc, " and takes: ", damage, " damage!")
        end
    elseif dc_result && attack_value["if_save"] == "no_effect"
        combatants_hp[target_name] -= damage
        combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
        if attack_value["is_heal"] && attack_value["heal_type"] == "damage_dealt"
            heal(attacker_name, damage)
        end
        if combatants_stats[target_name]["combat_stats"]["is_downed"]
            combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 1
        end
        if verbose
            println(target_name, " takes: ", damage, " damage!")
        end
    elseif dc_result && attack_value["if_save"] == "half"
        combatants_hp[target_name] -= Int(floor(damage/2))
        combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += Int(floor(damage/2))
        if attack_value["is_heal"] && attack_value["heal_type"] == "damage_dealt"
            heal(attacker_name, Int(floor(damage/2)))
        end
        if combatants_stats[target_name]["combat_stats"]["is_downed"]
            combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 1
        end
        if verbose
            println(target_name, " succeeds DC of ", dc, " and takes: ", Int(floor(damage/2)), " damage! (half damage)")
        end
    end
    if dc_result && attack_value["if_save"] == "no_damage"
        if verbose
            println(target_name, " succeeds to meet DC of ", dc, " and takes no damage!")
        end
    end
    return nothing
end

function divine_smite(attacker_name, target_name)
    bonus_dice_roll = ""
    number_of_dice = 2
    level = 0
    for spell_slot_level in keys(combatants_stats[attacker_name]["combat_stats"]["spell_slots"])
        if combatants_stats[attacker_name]["combat_stats"]["spell_slots"][spell_slot_level] > 0
            level = combatants_stats[attacker_name]["combat_stats"]["spell_slots"][spell_slot_level]
        end
    end
    if level == 0
        return bonus_dice_roll
    end
    combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] -= 1
    if combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] < 0
            combatants_stats[attacker_name]["combat_stats"]["spell_slots"][level] = 0 # just to be sure
    end
    number_of_dice += level-1
    target_creature_type = combatants_stats[target_name]["creature_type"]
    if target_creature_type == "undead" || target_creature_type == "fiend"
        number_of_dice += 1
    end
    if number_of_dice > 6
        number_of_dice = 6
    end
    bonus_dice_roll = "+$(number_of_dice)d8"
    #logging.info("{} used a level {} divine smite on {} ({}) and added {} to their roll".format(attacker_name, level, target_name, target_creature_type, bonus_dice_roll))
    return bonus_dice_roll
end

function divine_smite_decision(attacker_name, target_name, straight_roll)
    if straight_roll == 20
        # je crit, je smite
        return divine_smite(attacker_name, target_name)
    end
    if combatants_stats[attacker_name]["divine_smite"] && roll_d20()>=10
        return divine_smite(attacker_name, target_name)
    else
        return ""
    end
end

function attack(attacker_name, target_name, attack_value)
    adv = false
    dis = false
    if attack_value["has_advantage"]
        adv = true
    end
    if combatants_stats[attacker_name]["combat_stats"]["advantage_on_attack"] || combatants_stats[target_name]["combat_stats"]["advantage_if_attacked"]
        adv = true
    end
    if combatants_stats[attacker_name]["combat_stats"]["disadvantage_on_attack"] || combatants_stats[target_name]["combat_stats"]["disadvantage_if_attacked"]
        dis = true
    end
    conditions = combatants_stats[target_name]["combat_stats"]["conditions"]
    if "Prone" in conditions && attack_value["action_type"] == "melee"
        adv=true
    elseif "Prone" in conditions && attack_value["action_type"] == "ranged"
        dis=true
    end
    straight_roll = roll_d20(adv=adv, dis=dis)
    attack_roll = straight_roll+combatants_stats[attacker_name]["attack_mod"]
    if combatants_stats[attacker_name]["combat_stats"]["has_bardic_inspiration"][1]
        attack_roll += use_bardic_inspiration(attacker_name)
    end
    normal_damage = 0
    crit_damage = 0
    if combatants_stats[attacker_name]["sneak_attack_dices"] != 0 && combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] == 1
        if straight_roll == 20
            sneak_attack_damage = roll_dice((2*combatants_stats[attacker_name]["sneak_attack_dices"],6,0))
            crit_damage += sneak_attack_damage
        else
            sneak_attack_damage = roll_dice((combatants_stats[attacker_name]["sneak_attack_dices"],6,0))
            normal_damage += sneak_attack_damage
        end
        if verbose
            println("Sneak attack damage ", sneak_attack_damage)
        end
        combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] = 0
    end
    dice_roll = attack_value["dice_rolls"]
    if combatants_stats[attacker_name]["divine_smite"]
        divine_smite_choice = divine_smite_decision(attacker_name, target_name, straight_roll)
        if divine_smite_choice != ""
            if !isa(attack_value["dice_rolls"], String)
                dice_roll = convert_dice_to_string(dice_roll)
            end
            dice_roll = dice_roll*divine_smite(attacker_name, target_name)
        end
    end
    normal_damage = roll_dice(dice_roll)
    if attack_value["damage_type"] in combatants_stats[target_name]["resistances"]
        normal_damage = Int(floor(normal_damage/2))
    end
    if attack_value["damage_type"] in combatants_stats[target_name]["immunities"]
        normal_damage = 0
    end
    crit_damage += calculate_crit_damage(attacker_name, convert_dice_to_string(dice_roll))
    if attack_value["damage_type"] in combatants_stats[target_name]["resistances"]
        crit_damage = Int(floor(crit_damage/2))
    end
    if attack_value["damage_type"] in combatants_stats[target_name]["immunities"]
        crit_damage = 0
    end
    if straight_roll == 20
        combatants_hp[target_name] -= crit_damage
        combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += crit_damage
        if attack_value["condition"] != ""
            if attack_value["auto_success"]
                dc = combatants_stats[attacker_name]["dc"]
                set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
            else
                dc = combatants_stats[attacker_name]["dc"]
                if !dc_check(target_name, dc, attack_value["dc_type"])
                    if attack_value["has_dc_effect_on_hit"]
                        crit_damage += roll_dice(attack_value["dc_effect_on_hit"])
                    end
                    set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
                end
            end
        end
        if verbose
            println(attacker_name, " CRITS with ", attack_roll, " and does: ", crit_damage, " damage!")
        end
        if combatants_stats[target_name]["combat_stats"]["is_downed"]
            combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 2
        end

    elseif attack_roll >= combatants_stats[target_name]["ac"]
        if !("Paralyzed" in conditions) && !("Unconscious" in conditions)
            combatants_hp[target_name] -= normal_damage
            combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += normal_damage
            if attack_value["condition"] != ""
                if attack_value["auto_success"]
                    dc = combatants_stats[attacker_name]["dc"]
                    set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
                else
                    dc = combatants_stats[attacker_name]["dc"]
                    if !dc_check(target_name, dc, attack_value["dc_type"])
                        if attack_value["has_dc_effect_on_hit"]
                            normal_damage += roll_dice(attack_value["dc_effect_on_hit"])
                        end
                        set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
                    end
                end
            end
            if verbose
                println(attacker_name, " hits with ", attack_roll, " and does: ", normal_damage, " damage!")
            end
            if combatants_stats[target_name]["combat_stats"]["is_downed"]
                combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 1
            end
        elseif "Paralyzed" in conditions || "Unconscious" in conditions
            combatants_hp[target_name] -= crit_damage
            combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += crit_damage
            if attack_value["condition"] != ""
                if attack_value["auto_success"]
                    dc = combatants_stats[attacker_name]["dc"]
                    set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
                else
                    dc = combatants_stats[attacker_name]["dc"]
                    if !dc_check(target_name, dc, attack_value["dc_type"])
                        if attack_value["has_dc_effect_on_hit"]
                            crit_damage += roll_dice(attack_value["dc_effect_on_hit"])
                        end
                        set_condition(target_name, attack_value["condition"], dc, attack_value["dc_type"])
                    end
                end
            end
            if verbose
                println(attacker_name, " CRITS on downed target with ", attack_roll, " and does: ", crit_damage, " damage!")
            end
            if combatants_stats[target_name]["combat_stats"]["is_downed"]
                combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 2
            end
        end
    elseif verbose
        println(attacker_name, " misses.")
    end
    return nothing
end

function gauss_circle_problem(rayon)
    resultat = 1
    for i in range(80)
        resultat += 4*(((rayon^2)÷(4*i+1))-((rayon^2)÷(4*i+3)))
    end
    return resultat
end

function calculate_aoe_number_of_targets(attacker_name, aoe_size, aoe_shape, pythagore)
    maximum_number_of_squares = 1
    if aoe_shape == "sphere"
        if pythagore
            maximum_number_of_squares = gauss_circle_problem(aoe_size÷5)
        else
            maximum_number_of_squares = ((2*aoe_size+1)÷5)^2
        end
    elseif aoe_shape == "cylinder"
        if pythagore
            maximum_number_of_squares = gauss_circle_problem(aoe_size÷5)
        else
            maximum_number_of_squares = ((2*aoe_size+1)÷5)^2
        end
    elseif aoe_shape == "square"
        maximum_number_of_squares = (aoe_size÷5)^2
    elseif aoe_shape == "cone"
        if pythagore
            maximum_number_of_squares = gauss_circle_problem(aoe_size÷5)÷4
        else
            maximum_number_of_squares = (((2*aoe_size+1)÷5)^2)÷4
        end
    elseif aoe_shape == "line"
        maximum_number_of_squares = aoe_shape[1]*aoe_shape[2]÷2
    end
    if combatants_stats[attacker_name]["is_monster"]
        number_of_targets = length(players_names)
    else
        number_of_targets = length(monsters_names)
    end
    if number_of_targets <= maximum_number_of_squares
        maximum_number_of_squares = number_of_targets
    end
    return rand(maximum_number_of_squares÷3:maximum_number_of_squares)
end

function set_target(attacker_name)
    if combatants_stats[attacker_name]["is_monster"]
        return rand(players_names)
    else
        choice = rand(monsters_names)
        # choix du plus gros damage dealer
        for monster_name in monsters_names
            if combatants_stats[monster_name]["combat_stats"]["damage_dealt"] > combatants_stats[choice]["combat_stats"]["damage_dealt"]
                choice = monster_name
            end
        end
        return choice
    end
end

function set_multiple_targets(attacker_name, number_of_targets)
    targets_list = []
    if combatants_stats[attacker_name]["is_monster"]
        players_list_copy = deepcopy(players_names)
        if number_of_targets > length(players_list_copy)
            number_of_targets = length(players_list_copy)
        end
        if number_of_targets == 0
            return nothing
        end
        for _ in 1:1:number_of_targets
            chosen_element = rand(players_list_copy)
            push!(targets_list, chosen_element)
            filter!(e -> e != chosen_element, players_list_copy)
        end
        return targets_list
    else
        monsters_list_copy = deepcopy(monsters_names)
        if number_of_targets > length(monsters_list_copy)
            number_of_targets = length(monsters_list_copy)
        end
        if number_of_targets == 0
            return nothing
        end
        for _ in 1:1:number_of_targets
            chosen_element = rand(monsters_list_copy)
            push!(targets_list, chosen_element)
            filter!(e -> e != chosen_element, monsters_list_copy)
        end
        return targets_list
    end
end

function aoe_attack(attacker_name, attack_value; attack_name="")
    aoe_size = attack_value["aoe_size"]
    aoe_shape = attack_value["aoe_shape"]
    number_of_targets = calculate_aoe_number_of_targets(attacker_name, aoe_size, aoe_shape, pythagore)
    list_of_targets = set_multiple_targets(attacker_name, number_of_targets)
    dc_type = attack_value["dc_type"]
    dc = combatants_stats[attacker_name]["dc"]
    damage = 0
    dice_rolls = attack_value["dice_rolls"]
    damage += roll_dice(dice_rolls)
    for target_name in list_of_targets
        if attack_value["damage_type"] in combatants_stats[target_name]["resistances"]
            damage = Int(floor(damage/2))
        end
        if attack_value["damage_type"] in combatants_stats[target_name]["immunities"]
            damage = 0
        end
        dc_result = dc_check(target_name, dc, dc_type)
        if !dc_result || attack_value["if_save"] == "no_effect"
            combatants_hp[target_name] -= damage
            combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += damage
            if attack_value["is_heal"] && attack_value["heal_type"] == "damage_dealt"
                heal(attacker_name, damage)
            end
            if combatants_stats[target_name]["combat_stats"]["is_downed"]
                combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 1
            end
            if verbose
                println(target_name, " fails to meet DC of ", dc, " and takes: ", damage, " damage!")
            end
        elseif dc_result && attack_value["if_save"] == "half"
            combatants_hp[target_name] -= Int(floor(damage/2))
            combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] += Int(floor(damage/2))
            if attack_value["is_heal"] && attack_value["heal_type"] == "damage_dealt"
                heal(attacker_name, Int(floor(damage/2)))
            end
            if combatants_stats[target_name]["combat_stats"]["is_downed"]
                combatants_stats[target_name]["combat_stats"]["death_saves"][1] += 1
            end
            if verbose
                println(target_name, " succeeds DC of ", dc, " and takes: ", Int(floor(damage/2)), " damage! (half damage)")
            end
        elseif dc_result && attack_value["if_save"] == "no_damage" && verbose
            println(target_name, " succeeds to meet DC of ", dc, " and takes no damage!")
        end
    end
end

function remove_from_ini(name)
    for i in 1:1:length(ini_order)
        if ini_order[i].second == name
            filter!(e -> e != name, ini_order)
            break
        end
    end
end

function death(name)
    if combatants_stats[name]["is_monster"]
        if combatants_stats[name]["is_mythic"] && combatants_stats[name]["combat_stats"]["mythic_state"]
            filter!(e -> e != name, monsters_names)
            remove_from_ini(name)
        elseif combatants_stats[name]["is_mythic"] && !combatants_stats[name]["combat_stats"]["mythic_state"]
            combatants_hp[name] = combatants_stats[name]["mythic_hp"]
            if verbose
                println("$name enters its mythic stage and gains $(combatants_stats[name]["mythic_hp"]) HP!")
            end
        else
            filter!(e -> e != name, monsters_names)
            remove_from_ini(name)
        end
    else
        combatants_hp[name] = 0
        set_condition(name, "Unconscious", 45, "con")
        combatants_stats[name]["combat_stats"]["is_downed"] = true
    end
end

function check_for_death()
    bring_out_your_dead = []
    for (name, hp_value) in combatants_hp
        if hp_value <= 0 && !combatants_stats[name]["combat_stats"]["is_downed"]
            death(name)
            if combatants_stats[name]["is_monster"]
                if combatants_stats[name]["is_mythic"] && !combatants_stats[name]["combat_stats"]["mythic_state"]
                    combatants_stats[name]["combat_stats"]["mythic_state"] = true
                else
                    push!(bring_out_your_dead, name)
                end
            elseif combatants_stats[name]["combat_stats"]["death_saves"][1] >= 3
                push!(bring_out_your_dead, name)
            end
        elseif combatants_stats[name]["combat_stats"]["death_saves"][1] >= 3
            push!(bring_out_your_dead, name)
            filter!(e -> e != name, players_names)
            remove_from_ini(name)
        end
    end
    for name in bring_out_your_dead
        if verbose
            println("$name dies.")
        end
        delete!(combatants_hp, name)
    end
end

function general_attack(attacker_name, attack_value)
    if attack_value["action_type"] == "spell"
        cast_spell(attacker_name)
        check_for_death()
    elseif attack_value["has_attack_mod"]
        target = set_target(attacker_name)
        attack(attacker_name, target, attack_value)
        check_for_death()
    elseif attack_value["has_dc"] && !attack_value["is_aoe"]
        target = set_target(attacker_name)
        dc_attack(attacker_name, target, attack_value)
        check_for_death()
    elseif attack_value["is_aoe"]
        aoe_attack(attacker_name, attack_value)
        check_for_death()
    end
end

function death_saves(player_name; mod=0, adv=false)
    combatants_hp[player_name] = 0
    straight_roll = roll_d20(adv=adv)
    roll = straight_roll + mod
    if straight_roll == 20
        heal(player_name, 1)
    elseif roll >= 10
        combatants_stats[player_name]["combat_stats"]["death_saves"][2] += 1
        if combatants_stats[player_name]["combat_stats"]["death_saves"][2] >= 3
            combatants_stats[player_name]["combat_stats"]["death_saves"][1] = 0
            combatants_stats[player_name]["combat_stats"]["death_saves"][2] = 0
            combatants_stats[player_name]["combat_stats"]["is_stable"] = true
        end
    elseif straight_roll == 1
        combatants_stats[player_name]["combat_stats"]["death_saves"][1] += 2
        if combatants_stats[player_name]["combat_stats"]["death_saves"][1] >= 3
            check_for_death()
        end
    elseif  roll < 10 && straight_roll != 1
        combatants_stats[player_name]["combat_stats"]["death_saves"][1] += 1
        if combatants_stats[player_name]["combat_stats"]["death_saves"][1] >= 3
            check_for_death()
        end
    end
end

function set_legend_actions_order()
    if length(players_names) > 0
        for monster_name in legendary_monsters
            initiative_order_copy = deepcopy(ini_order)
            legendary_actions_pos = []
            for possible_charge_use in 1:1:combatants_stats[monster_name]["legend_actions_charges"]
                if length(initiative_order_copy) <= 0
                    break
                end
                charge_use = rand(initiative_order_copy)
                filter!(e -> e != charge_use, initiative_order_copy)
                push!(legendary_actions_pos, charge_use.second)
            end
            legend_actions_order[monster_name] = legendary_actions_pos
        end
    end
end

function execute_legend_action(monster_name)
    attack_value = rand(combatants_stats[monster_name]["legend_actions"])
    if attack_value["charge_cost"] > combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"]
        for l_ac in combatants_stats[monster_name]["legend_actions"]
            if l_ac["charge_cost"] <= combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"]
                attack_value = l_ac
            end
        end
    end
    if attack_value["charge_cost"] <= combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"]
        combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"] -= attack_value["charge_cost"]
        #logging.info("{}'s legendary action: {}".format(monster_name, attack_value["name"]))
        check_for_death()
        if length(players_names) == 0 || length(monsters_names) == 0
            return nothing
        end
        general_attack(monster_name, attack_value)
        if length(players_names) == 0 || length(monsters_names) == 0
            return nothing
        end
    end
end

function reset_legendary_actions_charges()
    for monster_name in legendary_monsters
        combatants_stats[monster_name]["combat_stats"]["legend_actions_charges"] = combatants_stats[monster_name]["legend_actions_charges"]
    end
end

function execute_multiattack(attacker_name, attack_value)
    multiattack_list = attack_value["multiattack_list"]
    for attack_value in multiattack_list
        general_attack(attacker_name, attack_value)
    end
end

function choose_attack(attacker_name)
    recharge_seen = true
    multiattack_seen = true
    attack_not_chosen = true
    arsenal = combatants_stats[attacker_name]["action_arsenal"]
    for (attack_name, value) in arsenal
        attack_value = value
        if attack_value["has_recharge"]
            recharge_seen = false
        elseif attack_value["is_multiattack"]
            multiattack_seen = false
        end
    end
    while attack_not_chosen
        for (attack_name, value) in arsenal
            attack_value = value
            if attack_value["has_recharge"] && attack_value["recharge_ready"]
                return attack_value
            elseif attack_value["has_recharge"] && !attack["recharge_ready"]
                recharge_roll = roll_dice("1d6")
                if recharge_roll >= attack_value["recharge"]
                    return attack_value
                else
                    recharge_seen = true
                end
            elseif !attack["has_recharge"] && attack_value["is_multiattack"]
                return attack_value
            elseif !attack["has_recharge"] && !attack["is_multiattack"]
                if recharge_seen && multiattack_seen
                    return attack_value
                end
            end
        end
    end
end

function choose_aoe_or_single(attacker_name)
    enemy_hps = []
    attack_type_decision = ""
    for (name, hp_value) in combatants_hp
        if combatants_stats[attacker_name]["is_monster"]
            if combatants_stats[name]["is_monster"]
                continue
            else
                push!(enemy_hps, hp_value)
            end
        else
            if combatants_stats[name]["is_monster"]
                push!(enemy_hps, hp_value)
            else
                continue
            end
        end
    end
    average_enemy_hp = mean(enemy_hps)
    enemy_hps_std = std(enemy_hps)
    outlier_count = 0
    for (name, hp_value) in combatants_hp
        if combatants_stats[attacker_name]["is_monster"]
            if combatants_stats[name]["is_monster"]
                continue
            else
                if combatants_hp[name] > average_enemy_hp+enemy_hps_std
                    outlier_count += 1
                end
            end
        else
            if combatants_stats[name]["is_monster"]
                if combatants_hp[name] > average_enemy_hp+enemy_hps_std
                    outlier_count += 1
                end
            else
                continue
            end
        end
    end
    if combatants_stats[attacker_name]["is_monster"]
        if outlier_count >= length(players_names)/8 || outlier_count == 0
            if length(players_names) > 3
                attack_type_decision = "is_aoe"
            else
                attack_type_decision = "single"
            end
        else
            attack_type_decision = "single"
        end
    else
        if outlier_count >= length(monsters_names)/4  || outlier_count == 0
            if length(monsters_names) > 3
                attack_type_decision = "is_aoe"
            else
                attack_type_decision = "single"
            end
        else
            attack_type_decision = "single"
        end
    end
    return attack_type_decision
end

function spell_decision(caster_name)
    spellbook = combatants_stats[caster_name]["spellbook"]
    spell_slots = combatants_stats[caster_name]["combat_stats"]["spell_slots"]
    spell_level_to_use = 0
    spell_type_decision = choose_aoe_or_single(caster_name)
    chosen_spell = Dict()
    spell_name = ""

    # Détermine le niveau le plus élevé disponible
    for spell_level in sort(collect(spell_slots), rev=true)
        if spell_slots[spell_level.first] > 0
            spell_level_to_use = spell_level.first
            break
        else
            continue
        end
    end

    # Détermine si single target ou is_aoe
    if spell_type_decision == "is_aoe"
        for spell_known in spellbook
            if isa(spell_known, String)
                if spells_database[spell_known]["is_aoe"] && spells_database[spell_known]["level"] <= spell_level_to_use
                    chosen_spell = spell_known
                    break
                end
            else
                if spells_database[spell_known[1]]["is_aoe"] && spells_database[spell_known[1]]["level"] <= spell_level_to_use
                    chosen_spell = spell_known
                    break
                end
            end
        end
    else
        for spell_known in spellbook
            if isa(spell_known, String)
                if !spells_database[spell_known]["is_aoe"] && spells_database[spell_known]["level"] <= spell_level_to_use
                    chosen_spell = spell_known
                    break
                end
            else
                if !spells_database[spell_known[1]]["is_aoe"] && spells_database[spell_known[1]]["level"] <= spell_level_to_use
                    chosen_spell = spell_known
                    break
                end
            end
        end
    end
    if isa(chosen_spell, String)
        spell_name = chosen_spell
        chosen_spell = deepcopy(spells_database[chosen_spell])
    elseif isa(chosen_spell, Tuple)
        spell_name = chosen_spell[1]
        spell = deepcopy(spells_database[chosen_spell[1]])
        spell["dice_rolls"] = chosen_spell[2]
        chosen_spell = spell
    else
        chosen_spell = spellbook[end]
        spell_name = chosen_spell[1]
        spell = deepcopy(spells_database[chosen_spell[1]])
        spell["dice_rolls"] = chosen_spell[2]
        chosen_spell = spell
    end
    if chosen_spell["level"] < spell_level_to_use && chosen_spell["is_upcastable"]
        for _ in 1:1:spell_level_to_use-chosen_spell["level"]
            chosen_spell["dice_rolls"] *= "+"*chosen_spell["upcast_effect"]
        end
    else
        spell_level_to_use = chosen_spell["level"]
    end
    #logging.info("Chose {} at level {}.".format(spell_name, spell_level_to_use))
    return chosen_spell, spell_name, spell_level_to_use
end

function cast_spell(caster_name)
    spell, spell_name, spell_level = spell_decision(caster_name)
    if spell_level > 0
        combatants_stats[caster_name]["combat_stats"]["spell_slots"][spell_level] -= 1
        if combatants_stats[caster_name]["combat_stats"]["spell_slots"][spell_level] < 0
            combatants_stats[caster_name]["combat_stats"]["spell_slots"][spell_level] = 0 # just to be sure
        end
    end
    if verbose
        println("$caster_name casts $spell_name at level $(spell_level)!")
    end
    if spell["has_attack_mod"]
        attack(caster_name, set_target(caster_name), spell)
    elseif spell["has_dc"] && !spell["is_aoe"]
        dc_attack(caster_name, set_target(caster_name), spell)
    elseif spell["is_aoe"]
        aoe_attack(caster_name, spell, attack_name=spell_name)
    end
end

function combat(monsters_list, players_list; monster_name="", number_of_monsters=0, verb=false)
    global combatants_stats = Dict()
    global combatants_hp = Dict()
    global combatants_names = []
    global players_names = []
    global monsters_names = []
    global ini_order = []
    global legendary_monsters = []
    global legend_actions_order = Dict()
    global player_deaths = 0
    global verbose = true
    global pythagore = false
    global conditions_list = ["Blinded", "Charmed", "Deafened", "Frightened", "Grappled", "Incapacitated", "Invisible", "Paralyzed", "Petrified", "Poisoned", "Prone", "Restrained", "Stunned", "Unconscious"]
    global spells_database = Dict()
    if verb
        global verbose = true
    end
    players_damage = Dict()
    rounds = 1
    import_players(players_list)
    import_monsters(monsters_list)
    if number_of_monsters > 0
        import_group(monster_name, number_of_monsters)
    end
    roll_ini()
    import_spells()
    for player in players_names
        players_damage[player] = 0
    end
    while length(players_names) != 0 && length(monsters_names) != 0
        if verbose
            println("\n --- Round $rounds ---\n")
        end
        set_legend_actions_order()
        reset_legendary_actions_charges()
        for attacker in ini_order
            attacker_name = attacker.second
            if !combatants_stats[attacker_name]["is_monster"]
                combatants_stats[attacker_name]["combat_stats"]["damage_dealt"] = 0
            end
            if verbose
                println("$attacker_name's turn.")
            end
            combatants_stats[attacker_name]["combat_stats"]["sneak_attack_charge"] = 1
            if "Incapacitated" in combatants_stats[attacker_name]["combat_stats"]["conditions"]
                if combatants_stats[attacker_name]["combat_stats"]["is_downed"]
                    death_saves(attacker_name)
                end
            else
                if !isempty(combatants_stats[attacker_name]["action_arsenal"])
                    check_for_death()
                    if length(players_names) == 0
                        continue
                    end
                    attack_choice = choose_attack(attacker_name)
                    if attack_choice["is_multiattack"]
                        execute_multiattack(attacker_name, attack_choice)
                    else
                        general_attack(attacker_name, attack_choice)
                    end
                    if combatants_stats[attacker_name]["bardic_inspiration"][1] && combatants_stats[attacker_name]["combat_stats"]["bardic_inspiration_charges"] > 0
                        if combatants_stats[attacker_name]["is_monster"]
                            target_choice = choose_inspiration_target(attacker_name, monsters_names)
                        else
                            target_choice = choose_inspiration_target(attacker_name, players_names)
                        end
                        give_bardic_inspiration(attacker_name, target_choice)
                    end
                else
                    for attack_value in combatants_stats[attacker_name]["actions"]
                        check_for_death()
                        if length(players_names) == 0 || length(monsters_names) == 0
                            break
                        end
                        if attack_value["action_type"] == "spell"
                            cast_spell(attacker_name)
                            check_for_death()
                        elseif attack_value["has_attack_mod"]
                            target = set_target(attacker_name)
                            attack(attacker_name, target, attack_value)
                            check_for_death()
                        elseif attack_value["has_dc"] && !attack["is_aoe"]
                            target = set_target(attacker_name)
                            dc_attack(attacker_name, target, attack_value)
                            check_for_death()
                        elseif attack_value["is_aoe"]
                            aoe_attack(attacker_name, attack_value)
                            check_for_death()
                        end
                    end
                    if combatants_stats[attacker_name]["bardic_inspiration"][1] && combatants_stats[attacker_name]["combat_stats"]["bardic_inspiration_charges"] > 0
                        if combatants_stats[attacker_name]["is_monster"]
                            target_choice = choose_inspiration_target(attacker_name, monsters_names)
                        else
                            target_choice = choose_inspiration_target(attacker_name, players_names)
                        end
                        give_bardic_inspiration(attacker_name, target_choice)
                    end
                end
                if !combatants_stats[attacker_name]["is_monster"]
                    players_damage[attacker_name] += combatants_stats[attacker_name]["combat_stats"]["damage_dealt"]
                end
            end
            condition_check(attacker_name)
            heal(attacker_name, combatants_stats[attacker_name]["combat_stats"]["regeneration"])
            for monster_name in legendary_monsters
                for name in legend_actions_order[monster_name]
                    if name == attacker_name
                        execute_legend_action(monster_name)
                    end
                end
            end
        end
        rounds += 1
    end
    if verbose
        println("Combat ended.")
    end
    if length(players_names) == 0
        if verbose
            println("The players were killed.")
        end
        return (0, player_deaths, rounds, players_damage)
    else
        if verbose
            println("The monsters were killed.")
        end
        return (1, player_deaths, rounds, players_damage)
    end
end