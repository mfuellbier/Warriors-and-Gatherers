#!/usr/bin/python
# -*- coding: utf-8 -*-

from classes import *
from classesGui import *
from copy import *
import pickle
import shutil
import platform
import sys
import functions

gameDat = open('game.dat','wb')

gameStats = GameStats('Noob',{'Noob':0,'Intermediate':0,'Advanced':0,'Expert':0},None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)

# Set source-codes for the AI as reward
listOfCode = ('Noob','NoobFunctions','Intermediate','IntermediateFunctions','Advanced','AdvancedFunctions','Expert','ExpertFunctions')
CodeStrings = []
for code in listOfCode:
    source = open(code+'.py','r').read()
    exec("gameStats.set"+code+"(source)")

# Set challenges
gameStats.setChallengeNoob(1000,'newbie.map',10)
gameStats.setChallengeIntermediate(1000,'circle.map',5)
gameStats.setChallengeAdvanced(1000,'newbie.map',3)
gameStats.setChallengeExpert(1000,'central.map',1)

# Set rewardMaps
listOfMaps = ('backyard','central','circle','garden','labyrinth','newbie','source','tight_corridors')
MapStrings = []
for mapName in listOfMaps:
    stringOfMap = open('maps/'+mapName+'.map','r').read()
    exec("gameStats.set"+mapName+"(stringOfMap)")

# dump the file
pickle.dump(gameStats,gameDat)

if len(sys.argv) > 1 and sys.argv[1] == "cheat":
    functions.cheat()
