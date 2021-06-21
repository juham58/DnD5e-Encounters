# Encounters

This repo is a 2 parts project which gives me tools to balance encounters for 5e Dungeons and Dragons

## NOTE À MES JOUEURS: Allez pas voir dans le dossier "data" si vous voulez pas vous faire spoil des encounters futurs :)

## CRFinder

The section CRFinder is a simple implementation of the rules given in the Dungeon Master's Guide to get the Challenge Rating from creatures' stats. The tools can be accessed through the file UI.py

## EncounterSim

The section EncounterSim is used to simulate encounters from the stats.

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

As of now, it doesn't take into account:
* Any strategy
* Area of effect abilities
* Movement
* Spells for players
