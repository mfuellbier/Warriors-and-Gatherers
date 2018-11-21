# Warriors-and-Gatherers

A game for coder. Improve your AI to defeat the enemy.

## Dependencies
* Python3
* TKinter

## Instructions
### Init
`python createGameDat.py`
### Play
`python gui.py`
### Cheat
To unlock all challenges and maps, do
`python createGameDat.py cheat`

## Instructions
Modify following files to improve your AI:
* yourAI.py
* yourFunctions.py

## Files
Short description of the files
### AIs
#### Players AI
`YourAI.py`
`YourFunctions.py`
#### Enemies AI
`Noob.py`
`NoobFunctions.py`
`Intermediate.py`
`IntermediateFunctions.py`
`Expert.py`
`ExpertFunctions.py`
#### Dummy AI
`Dummy.py`
### createGameDat.py
Creates game.dat.
This file contains the challanges and saves the players progress
### gui.py
GUI of the game.
`python3 gui.py`

starts the game.
### classesGUI.py
Classes of GUI, the game data and game stats
### classes.py
Classes of the games objects (units,base,fields,..). Contains basically games logic.
### main.py
Sets conditions of game such as distribution of resources and strength and costs of units.  
Also contains the logic of the game.


## Disclosure
This is the entire code of the game. To sell this as a "real" game, one would have to obfuscate and compile it, such that the player would not be able to see the code of the enemies AI.

This is one of my very first coding projects.
