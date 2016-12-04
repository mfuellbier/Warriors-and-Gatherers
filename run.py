#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
from classes import *
from classesGui import *
from functions import *
import sys
import random
import time
import datetime
import Noob, Intermediate, Advanced, Expert

def Run(AIlistWithPy,mapName,rounds):

    startTimeGame = time.time()

    # Starting Conditions

    startResource = 200
    resourceOnField = 100
    probabilityForResourceOnField = 0.025

    unitMaxResourcesWarrior = 30
    unitStrengthWarrior = 0.75
    unitCostWarrior = 60
    unitMaxResourcesGatherer = 100
    unitStrengthGatherer = 0.5
    unitCostGatherer = 50
    
    pathToMap = 'maps/'+mapName
    listAI=[None]*4
    for k in range(4):
        listAI[k] = shortString(AIlistWithPy[k])
        exec('import '+str(listAI[k]))

    playerNames = [listAI[k] for k in range(4)]
    
    # Check if some Names are the same
    playerNames = checkForMultipleNames(playerNames)
    
    unitTypesStrings = { unitMaxResourcesGatherer : 'GATHERER' , unitMaxResourcesWarrior : 'WARRIOR'}
    unitTypes = {'WARRIOR' : UnitType(unitMaxResourcesWarrior,unitStrengthWarrior,unitCostWarrior,unitTypesStrings) , 'GATHERER' : UnitType(unitMaxResourcesGatherer,unitStrengthGatherer,unitCostGatherer,unitTypesStrings)}

    # Gathering Informations for very first round
    gameConfiguration = GameConfiguration(unitCostWarrior,unitCostGatherer,unitStrengthWarrior,unitStrengthGatherer,unitMaxResourcesWarrior,unitMaxResourcesGatherer,rounds)
    (Map,Base) = createMapBeginning(pathToMap,startResource,resourceOnField,gameConfiguration,unitTypes,deepcopy(playerNames),probabilityForResourceOnField) # save the data temporarily
    playerNamesData = deepcopy(playerNames)
    
    # data-list to save the game
    data = []
    
    # Save stdout
    save_stdout = sys.stdout

    # Open new log
    for k in range(4):
        open(str(playerNames[k])+'.log','w')

    data.append(prepareDataForPlayer(0,playerNamesData,Map,Base))

    for Round in range(1,rounds+1):
        startTimeRound = time.time()
        for k in range(4):
            
            playerCanMove = False
            # Check if player can move:
            if Base[k].resources >= min(unitCostWarrior,unitCostGatherer) or (Base[k].units != [] and Base[k].units != None):
                playerCanMove = True
            
            # safe Data
            if playerCanMove:
                safe = safeData(Base,playerNamesData,gameConfiguration,unitTypes,k)            
                
            # Set stdout to log
            sys.stdout = open(str(playerNames[k])+'.log','a')
            print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Start process round',Round,'\n')
            startTimeAi = time.time()
            
            # Execute AI only, if player can move
            if playerCanMove:
                #exec(listAI[k]+'.BattleClient(RoundState(Base[k],deepcopy(Map),Round),gameConfiguration)') # Needed to prevent Cheating in final Version!
                exec(listAI[k]+'.BattleClient(RoundState(Base[k],deepCopyMap(Map,gameConfiguration,unitTypes),Round),gameConfiguration)') # Needed to prevent Cheating in final Version!
                #exec(listAI[k]+'.BattleClient(RoundState(Base[k],Map,Round),gameConfiguration)')
            else:
                print('Game Over! No units and not enough resources to move!\n')
            print('Processed round',Round,'in',round((time.time()-startTimeAi)*1000,4),'ms.\n')
            print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Finished process round',Round,'\n')
            print()
            
            # Set stdout back to default
            sys.stdout = save_stdout
            
            # process move
            if playerCanMove:
                gameConfiguration = GameConfiguration(unitCostWarrior,unitCostGatherer,unitStrengthWarrior,unitStrengthGatherer,unitMaxResourcesWarrior,unitMaxResourcesGatherer,rounds)
                unitTypes = {'WARRIOR' : UnitType(unitMaxResourcesWarrior,unitStrengthWarrior,unitCostWarrior,unitTypesStrings) , 'GATHERER' : UnitType(unitMaxResourcesGatherer,unitStrengthGatherer,unitCostGatherer,unitTypesStrings)}
                cheater = preventCheating(Base,safe,playerNamesData,k,gameConfiguration,Map)        
                if cheater == False:
                    cheater = betweenTurns(Base,Map,resourceOnField,gameConfiguration,k,probabilityForResourceOnField)
                if cheater == True:
                    print('Player '+str(k+1)+': Cheater! Resources will be set to 0.')
                    Base[k].resources = 0                
        print('Round',Round,'took',round((time.time()-startTimeRound)*1000,4),'ms.')
        
        
        # Sleeps between rounds
        #time.sleep(time.time()-startTimeRound)
        
        data.append(prepareDataForPlayer(Round,playerNamesData,Map,Base))

    # Play
    print('The game took',round(time.time() - startTimeGame,4),'seconds.')
    
    [maxRes,winnerList] = findWinner(Base,playerNames) #is needed for statistics
    
    return [data,[maxRes,winnerList]]
