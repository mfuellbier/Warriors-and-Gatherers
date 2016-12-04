#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
from classes import *
from functions import *
#from gui import Player
from player import Player
import sys
import random
import AI1, AI2, AI3, AI4
import time
import datetime
import pickle
import copy


startTimeGame = time.time()


'''
mapName = sys.argv[1]
pathToMap = 'maps/'+mapName+'.map'
'''
pathToMap = 'maps/newbie.map'
#'''

# Starting Conditions

startResource = 200
resourceOnField = 100
probabilityForResourceOnField = 0.1
rounds = 15
playerNames = [1,2,3,4]
AI = ['AI3','AI1','AI1','AI1']

unitMaxResourcesWarrior = 30
unitStrengthWarrior = 0.75
unitCostWarrior = 60
unitMaxResourcesGatherer = 100
unitStrengthGatherer = 0.5
unitCostGatherer = 50



unitTypesStrings = { unitMaxResourcesGatherer : 'GATHERER' , unitMaxResourcesWarrior : 'WARRIOR'}
unitTypes = {'WARRIOR' : UnitType(unitMaxResourcesWarrior,unitStrengthWarrior,unitCostWarrior,unitTypesStrings) , 'GATHERER' : UnitType(unitMaxResourcesGatherer,unitStrengthGatherer,unitCostGatherer,unitTypesStrings)}

# Gathering Informations for very first round
gameConfiguration = GameConfiguration(unitCostWarrior,unitCostGatherer,unitStrengthWarrior,unitStrengthGatherer,unitMaxResourcesWarrior,unitMaxResourcesGatherer,rounds)
[Map,Base] = createMapBeginning(pathToMap,startResource,resourceOnField,gameConfiguration,unitTypes,deepcopy(playerNames),probabilityForResourceOnField) # save the data temporarily
MapSafe = deepcopy(Map)
playerNamesData = deepcopy(playerNames)
data = []
softdata = []
# Save stdout
save_stdout = sys.stdout


# Open new log1.txt
for k in range(4):
    open(AI[k]+'.log','w')

data.append(deepcopy(Harddata(0,playerNamesData,Map,Base)))
softdata.append(prepareDataForPlayer(0,playerNamesData,Map,Base))


for Round in range(1,rounds+1):
    for k in range(4):
        
        #safe Data
        #safe = safeData(Base,playerNamesData,gameConfiguration,unitTypes)
        
        # Stdout + AI
        sys.stdout = open(AI[k]+'.log','a')
        if k == 0:
            sys.stdout = save_stdout
        #print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Start process round',Round)
        startTimeAi = time.time()
        for unit in Base[0].units:
            print('Unit 1 position before turn:',unit.getPosition())
        exec(AI[k]+'.BattleClient(RoundState(Base[k],Map,Round),gameConfiguration)')
        print('Processed round',Round,'in',round((time.time()-startTimeAi)*1000,4),'ms.')
        #print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Finished process round',Round)
        for unit in Base[0].units:
            print('Unit 1 position after turn:',unit.getPosition())
        sys.stdout = save_stdout
        
        gameConfiguration = GameConfiguration(unitCostWarrior,unitCostGatherer,unitStrengthWarrior,unitStrengthGatherer,unitMaxResourcesWarrior,unitMaxResourcesGatherer,rounds)
        unitTypes = {'WARRIOR' : UnitType(unitMaxResourcesWarrior,unitStrengthWarrior,unitCostWarrior,unitTypesStrings) , 'GATHERER' : UnitType(unitMaxResourcesGatherer,unitStrengthGatherer,unitCostGatherer,unitTypesStrings)}

        #[Map,Base,cheater] = preventCheating(Base,safe,playerNamesData,k,gameConfiguration,Map,MapSafe)        
        #if cheater == False:
        betweenTurns(Base,Map,resourceOnField,gameConfiguration,k,probabilityForResourceOnField)
        for unit in Base[0].units:
            print('Unit 1 position after betweenTurns:',unit.getPosition())
    data.append(deepcopy(Harddata(Round,playerNamesData,Map,Base)))
    softdata.append(prepareDataForPlayer(Round,playerNamesData,Map,Base))
'''
# Find Winner
resourcesEnd = []
for k in range(4):
    #resourcesEnd.append(data[rounds].getResource(data[rounds].getPlayerNames()[k]))
    resourcesEnd.append(Base[k].getResources())
    
winner = 0
winnerList = []
for j in range(1,4):
    if resourcesEnd[j] > resourcesEnd[winner]:
        winner = j
maxRes = resourcesEnd[winner]
oneWinner = True
for l in range(1,4):
    if resourcesEnd[l] == maxRes and l != winner:
        oneWinner = False
        winnerList.append(playerNames[l])
if oneWinner == True:
    winnerList.append(playerNames[winner])
else:
    winnerList.append(playerNames[winner])

# return [maxRes,winnerList]
'''
# Play
print('The game took',time.time() - startTimeGame,'seconds')


pickle.dump(softdata, open("debug.p", "wb" ) )
