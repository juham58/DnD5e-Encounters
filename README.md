# Encounters

This repo is a 2 parts project which gives me tools to balance encounters for 5e Dungeons and Dragons. This is mostly for personal use so it is not well documented for now.

## NOTE À MES JOUEURS: Allez pas voir dans le dossier "data" si vous voulez pas vous faire spoil des encounters futurs :)

## CRFinder

The section CRFinder is a simple implementation of the rules given in the Dungeon Master's Guide to get the Challenge Rating from creatures' stats. The tools can be accessed through the file UI.py

## EncounterSim

The section EncounterSim is used to simulate encounters from the stats. To use it, add stats using monsters_stats_save.py or players_stats_save.py to add stats for a player or a monster. Then use analysis.py to run a simulation and get plots for data analysis.

Right now, it takes into account:
* HP
* Multiattack
* Ranged or melee attacks
* DC attacks
* Attacks with a DC effect
* Conditions that dosen't involve movement
* Death saves for players
* Legendary Actions
* Legendary Resistances
* Area of Effect
* Damage spells
* Simple decision system to choose spells to use
* Bardic Inspiration
* Divine Smite

As of now, it doesn't take into account:
* Any strategy
* Movement
* Non-damage spells
* Specific class features
