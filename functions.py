#!/usr/bin/python
# -*- coding: utf-8 -*-

# Functions

from classes import *
from classesGui import *
from tkinter import *
import random
import time
import pickle

def computeProbabilityForResourceOnField(numberResources,numberResourceFields,probabilityForResourceOnField):
    return probabilityForResourceOnField*10**(-4*numberResources/numberResourceFields)

def randomResourceOnField(resourceOnField, probability):
	if random.random() < probability:
		return resourceOnField
	else:
		return 0

def createDummyMap(Map):
    dummyMap = [None]*len(Map[0])
    for k in range(len(Map[0])):
        dummyMap[k] = [None]*len(Map)
    
    return dummyMap

def inverseDirection(direction):
    if direction == Direction.SOUTH:
        return Direction.NORTH
    elif direction == Direction.NORTH:
        return Direction.SOUTH
    elif direction == Direction.EAST:
        return Direction.WEST
    elif direction == Direction.WEST:
        return Direction.EAST
    elif direction == Direction.STAY:
        return Direction.STAY
    return 1
        
def createMapBeginning(pathToMap,startResource,resourceOnField,gameConfiguration,unitTypes,playerNames,probabilityForResourceOnField):
	# Input: 'maps/name.map', int
	# Output: [Field[][],base,base,base,base]
	
    txt = open(pathToMap,'r')
    
	# Inverse the map
    i=0
    temp=[]
    Map=[]
    for line in txt:
        i=i+1
        if i>4:
            temp.append([])
            Map.append([])
            for char in line:
                if char != '\n':
                    temp[i-5].append(char)
	# Create Map
    # Find Bases
    for y in range(0, len(temp)):
        for x in range(0, len(temp[y])):
            char = temp[y][x]
            if char == '1':
                Base1 = Base(startResource,[x,y],[],playerNames[0],gameConfiguration,unitTypes)
            elif char == '2':
                Base2 = Base(startResource,[x,y],[],playerNames[1],gameConfiguration,unitTypes)
            elif char == '3':
                Base3 = Base(startResource,[x,y],[],playerNames[2],gameConfiguration,unitTypes)
            elif char == '4':
                Base4 = Base(startResource,[x,y],[],playerNames[3],gameConfiguration,unitTypes)    
    
    bases = [Base1,Base2,Base3,Base4]
	
    for y in range(0, len(temp)):
        for x in range(0, len(temp[y])):
            char = temp[y][x]
            if char == 'Y':
                Map[x].append(Field([x,y],FieldType.WALL, None, 0, None))#, bases))
            elif char == 'X':
                Map[x].append(Field([x,y],FieldType.WATER, None, 0, None))#, bases))
            elif char == 'R':
                Map[x].append(Field([x,y],FieldType.RESOURCE, None , randomResourceOnField(resourceOnField,probabilityForResourceOnField*4), None))#, bases))
            elif char == '1':
                Map[x].append(Field([x,y],FieldType.BASE, [], 0, Base1))#, bases))
            elif char == '2':
                Map[x].append(Field([x,y],FieldType.BASE, [], 0, Base2))#, bases))
            elif char == '3':
                Map[x].append(Field([x,y],FieldType.BASE, [], 0, Base3))#, bases))
            elif char == '4':
                Map[x].append(Field([x,y],FieldType.BASE, [], 0, Base4))#, bases))
            else:
                Map[x].append(Field([x,y],FieldType.LAND, None, 0, None))#, bases))#
                
    #print('Map created:',time.time()-startTime)	
    return [Map,[Base1,Base2,Base3,Base4]]

def createMapBeginningData(pathToMap):
	# Input: 'maps/name.map', int
	# Output: [Field[][],base,base,base,base]
	
    txt = open(pathToMap,'r')

	
	# Inverse the map
    startTime = time.time()
    i=0
    temp=[]
    Map=[]
    for line in txt:
        i=i+1
        if i>4:
            temp.append([])
            Map.append([])
            for char in line:
                temp[i-5].append(char)
    
	# Create Map	
    for y in range(0, len(temp)):
        for x in range(0, len(temp[y])-1):
            char = temp[y][x]
            if char == 'Y':
                Map[x].append('WALL')
            elif char == 'X':
                Map[x].append('WATER')
            elif char == '1':
                Map[x].append('1BASE')
            elif char == '2':
                Map[x].append('2BASE')
            elif char == '3':
                Map[x].append('3BASE')
            elif char == '4':
                Map[x].append('4BASE')
            else:
                Map[x].append('LAND')
                
    #print('Map created:',time.time()-startTime)	
    return Data(0,[1,2,3,4],[200,200,200,200],Map,[[0,0],[0,0],[0,0],[0,0]])

def fight(attacker,defender,field,bases):
    if attacker.getUnitType().getStrength() == defender.getUnitType().getStrength(): # same Strength == same Types
        if random.random() < 2/3:
            winner = attacker
            looser = defender
        else:
            winner = defender
            looser = attacker
    else:	# different Strength == different Types
        if random.random() < attacker.getUnitType().getStrength():
            # attacker (WARRIOR) wins or attacker (GATHERER) wins
            winner = attacker
            looser = defender
        else:
            winner = defender
            looser = attacker
    # looser drops resources
    if looser.getResources() > 0: # If looser had resources
        field.resources+=looser.getResources()
    # looser dies
    for base in bases:
        if looser.getOwner() == base.getOwner():
            base.units.remove(looser)
    # winner stays on field
    return winner
    
def updateUnit(unit,Map,bases,lastPlayer):
    for k in range(4):
        if Map[bases[k].getPosition()[0]][bases[k].getPosition()[1]].unit == None:
            Map[bases[k].getPosition()[0]][bases[k].getPosition()[1]].unit = []
            
    dictionaryDirection = {Direction.STAY:[0,0], Direction.WEST:[-1,0], Direction.EAST:[1,0], Direction.SOUTH:[0,1], Direction.NORTH:[0,-1]}
    unitMoved = False
    X = unit.getPosition()[0]
    Y = unit.getPosition()[1]
    Xold = X-dictionaryDirection[unit.getLastMove()][0]
    Yold = Y-dictionaryDirection[unit.getLastMove()][1]
    if Map[X][Y].getFieldType() == FieldType.WATER or Map[X][Y].getFieldType() == FieldType.WALL:
        # unit enters Wall or Water => should not happen
        #print('ERROR: unit enters Wall or Water. Unit stays.')
        unit.moved = False
        unit.moveUnitBack()
        unit.moved = False
        unitMoved = True
    elif Map[X][Y].getFieldType() == FieldType.BASE: # unit enters base
        if Map[X][Y].base.getOwner() == unit.getOwner():
            bases[lastPlayer].resources += unit.getResources()	# unit transfers resources to base
            unit.resources = 0
            Map[X][Y].unit.append(unit)
            unitMoved = True
            if Map[Xold][Yold].getFieldType() == FieldType.BASE and unit in Map[Xold][Yold].unit:
                Map[Xold][Yold].unit.remove(unit)
            else:
                Map[Xold][Yold].unit = None
        else:   # unit enters enemys base; should not happen
            #print('ERROR: Unit enters enemys base! unit stays')
            unit.moved = False
            unit.moveUnitBack()
            unit.moved = False
            unitMoved = True
    else:
        # unit enters Land or Resource; either empty, enemy unit, same unit (Direction.STAY) or own other unit (last should not happen)
        if Map[X][Y].getUnitOnField() == None:
            # empty field => unit enters it
            Map[X][Y].unit = unit	# updating Map[][].unit
            unitMoved = True
            unit.moved = False
            if Map[Xold][Yold].getFieldType() == FieldType.BASE and unit in Map[Xold][Yold].unit:
                Map[Xold][Yold].unit.remove(unit)
            else:
                Map[Xold][Yold].unit = None
        elif Map[X][Y].getUnitOnField().getOwner() == unit.getOwner():
            # own unit on field
            if Map[X][Y].getUnitOnField().getUnitId() == unit.getUnitId():
                # unit stayed
                unitMoved = True
                unit.moved = False
                unit.lastMove = Direction.STAY
        else:
            # enemy unit => fight
            Map[X][Y].unit = fight(unit,Map[X][Y].getUnitOnField(),Map[X][Y],bases)
            unitMoved = True
            if Map[Xold][Yold].getFieldType() == FieldType.BASE and unit in Map[Xold][Yold].unit:
                Map[Xold][Yold].unit.remove(unit)
            else:
                Map[Xold][Yold].unit = None
    return unitMoved
    
def betweenTurns(bases,Map,resourceOnField,gameConfiguration,lastPlayer,probabilityForResourceOnField):
	# Input: (Base[],Field[][],GameConfiguration,int(0..3))
	# Output: [Base[],Field[][]]
	
	# This happens between turns:
	#	Fights
	#	updating base.units (deleting dead units, setting unit.moved to False)
	#	updating Map[][].unit
	#	updating base.resource
	#	Gathering of resources
	#	new resources
	#	Fights
    
    lastPlayersName = bases[lastPlayer].getOwner()
        
    #	Update Map; Position of units and update base.resources
    numberResources = 0     # Needed for computing new resources
    numberResourceFields = 0
    
    cheater = False
    for X in range(len(Map)):
        for Y in range(len(Map)):
            # Check if units on Map moved in illegal manner
            if Map[X][Y].getFieldType() != FieldType.BASE:
                if Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() == bases[lastPlayer].getOwner():
                    unit = Map[X][Y].getUnitOnField()
                    if not Map[X][Y].isReachable(unit):
                        unit.position[0] = X
                        unit.position[1] = Y
                        cheater = True
            # Needed for computing new resources
            if Map[X][Y].getFieldType() == FieldType.RESOURCE:
                if Map[X][Y].getResources() > 0:
                    numberResources += 1
                numberResourceFields += 1
    
    # Check if hidden units moved in illegal manner
    for unit in bases[lastPlayer].getHiddenUnits():
        if not Map[bases[lastPlayer].getPosition()[0]][bases[lastPlayer].getPosition()[1]].isReachable(unit):
            unit.position[0] = bases[lastPlayer].getPosition()[0]
            unit.position[1] = bases[lastPlayer].getPosition()[1]
            cheater = True
    
    if bases[lastPlayer].units != []:
        temp = [None] * len(bases[lastPlayer].units)
        for k in range(len(bases[lastPlayer].units)):
            unit = bases[lastPlayer].units[k]
            temp[k] = unit
            bases[lastPlayer].units[k].moved = False
        
        allUnitsMoved = True
        while temp != [] and allUnitsMoved:
            allUnitsMoved = False
            for unit in temp:
                unitMoved = updateUnit(unit,Map,bases,lastPlayer)
                if unitMoved:
                    temp.remove(unit)
                    allUnitsMoved = True
                    Map[unit.getPosition()[0]][unit.getPosition()[1]].gatherResource()
        # temp is list of units, which could not move because of 
        for unit in temp:
            unit.moved = False
            unit.moveUnitBack()
            unit.moved = False
            unit.lastMove = Direction.STAY
            Map[unit.getPosition()[0]][unit.getPosition()[1]].gatherResource()
	
    						
	#   new Resources
    #   Compute Probability    
    probabilityForResource = computeProbabilityForResourceOnField(numberResources,numberResourceFields,probabilityForResourceOnField)
    
    for column in Map:
        for field in column:
            if field.getFieldType() == FieldType.RESOURCE and field.getResources() == 0 and field.getUnitOnField() == None:
                field.resources = randomResourceOnField(resourceOnField,probabilityForResource)
    
    for k in range(4):
        if Map[bases[k].getPosition()[0]][bases[k].getPosition()[1]].unit == None:
            Map[bases[k].getPosition()[0]][bases[k].getPosition()[1]].unit = []
    
    return cheater

def prepareDataForPlayer(round,playerNames,Map,Base):
    
    playerMap = createDummyMap(Map)    
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if field.getFieldType() == FieldType.BASE:
                for k in range(4):
                    if playerNames[k] == field.base.getOwner():
                        playerMap[x][y] = str(k+1)+'BASE'
            elif field.getUnitOnField() != None:
                for k in range(4):
                    if playerNames[k] == field.getUnitOnField().getOwner():
                        playerMap[x][y] = str(k+1)+field.getUnitOnField().getUnitType().getString()
            elif field.getResources() > 0:
                playerMap[x][y] = FieldType.RESOURCE
            elif field.getFieldType() == FieldType.RESOURCE:
                playerMap[x][y] = 'LAND'
            else:
                playerMap[x][y] = field.getFieldType()
    resources = [None] * 4
    units = [[0,0],[0,0],[0,0],[0,0]]
    for k in range(4):
        resources[k] = Base[k].getResources()
        units[k] = [len(Base[k].units)-len(Base[k].getHiddenUnits()),len(Base[k].getHiddenUnits())]
    
    return Data(round,playerNames,resources,playerMap,units)
  
    
def safeData(base,playerNames,gameConfiguration,unitTypes,lastPlayer):
    # safes some Data: Resources and Position of Base, Number, Position and Resources of Units
    # Refreshes gameConfiguration and unitTypes

    k = lastPlayer
    
    # units
    tempW = 0
    tempG = 0
    resourcesUnits = {}
    
    # resources:
    resourcesBases = base[k].getResources()
    
    base[k].gameConfiguration = gameConfiguration
    base[k].unitTypes = unitTypes
    if base[k].owner != playerNames[k]:
        base[k].owner = playerNames[k]
    for unit in base[k].units:
        if unit.getUnitType().getString() == UnitType.WARRIOR:
            tempW += 1
        elif unit.getUnitType().getString() == UnitType.GATHERER:
            tempG += 1
        resourcesUnits[unit.getUnitId()] = unit.getResources()
    warriorsGatherers = (tempW,tempG)
    
    return (resourcesBases,warriorsGatherers,resourcesUnits)
    				
def preventCheating(base,safe,playerNames,lastPlayer,gameConfiguration,Map):
    # safe = (resourcesBases,warriorsGatherers,resourcesUnits)
    
    k = lastPlayer    
    # if cheated => Last players turn will be skipped and all changed stats will be set back
    lastPlayer = playerNames[k]
    cheater = False
    
    # base owner
    if base[k].getOwner() != playerNames[k]:
        base[k].owner = playerNames[k]
        cheater = True
    
    # Last Player => Resources
    # units
    unitDictionary = {}
    warriorsCount = 0
    gatherersCount = 0
    for unit in base[k].units:
        unitDictionary[unit.getUnitId()] = unit
        if unit.getUnitType().getString() == UnitType.WARRIOR:
            warriorsCount += 1
        if unit.getUnitType().getString() == UnitType.GATHERER:
            gatherersCount += 1
    # number of warriors:
    if warriorsCount < safe[1][0]:
        cheater = True
    if gatherersCount < safe[1][1]:        
        cheater = True
    for Id in unitDictionary:
        if Id in safe[2]:
        # Old units
            # Resources
            if unitDictionary[Id].getResources() != safe[2][Id]:
                cheater = True
                unitDictionary[Id].resources = safe[2][Id]
        else:
        # New units
            # Resources
            if unitDictionary[Id].getResources() != 0:
                cheater = True
                unitDictionary[Id].resources = 0
    # Resources: ResourcesSafe = Resources + #Gatherers * GathererCost + #Warriors * WarriorsCost
    if safe[0] != base[k].getResources() + (gatherersCount-safe[1][1]) * gameConfiguration.getUnitCostGatherer() + (warriorsCount-safe[1][0]) * gameConfiguration.getUnitCostWarrior():
        cheater = True
    return cheater

def deepCopyMap(Map,gameConfiguration,unitTypes):
    
    startTime = time.time()

    Copy = createDummyMap(Map)
    for X in range(len(Map)):
        for Y in range(len(Map[X])):
            field = Map[X][Y]
            # find attributes
            fieldType = field.getFieldType()
            if field.getFieldType() == FieldType.BASE:
                # get units on field
                unitList = []
                for unit in field.getUnitOnField():
                    unitList.append(Unit(unit.getUnitId(),unitTypes[unit.getUnitType().getString()],unit.getOwner(),unit.getResources(),[X,Y],False,unit.getLastMove()))
                baseCopy = Base(field.getBase().getResources(),[X,Y],unitList,field.getBase().getOwner(),gameConfiguration,unitTypes)
            else:
                baseCopy = None
                if field.getUnitOnField() == None:
                    unitList = None
                else:
                    unitList = Unit(field.getUnitOnField().getUnitId(),unitTypes[field.getUnitOnField().getUnitType().getString()],field.getUnitOnField().getOwner(),field.getUnitOnField().getResources(),[X,Y],False,field.getUnitOnField().getLastMove())
            Copy[X][Y] = Field([X,Y],fieldType,unitList,field.getResources(),baseCopy)
    return Copy

def findWinner(Base,playerNames):
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
    return [maxRes,winnerList]

    
def checkForMultipleNames(playerNames):
    doppelganger = []
    setOfAddings = []
    for k in range(3,-1,-1):
        adding = 0
        playerName = playerNames[k]
        listWithoutPlayerName = [None,None,None]
        for l in range(4):
            if l != k:
                if l>k:
                    m = l-1
                else:
                    m=l
                listWithoutPlayerName[m] = playerNames[l]
        numberOfDoppelganger = 0
        for j in range(3):
            if playerName == listWithoutPlayerName[j]:
                numberOfDoppelganger += 1
        while playerName in listWithoutPlayerName:
            playerName = playerNames[k]+str(numberOfDoppelganger-adding+1)
            adding += 1
        playerNames[k]=playerName
        setOfAddings.append(playerName[-1:])
        if numberOfDoppelganger > 0 and playerName[:-1] not in doppelganger:
            # remember Doppelganger
            doppelganger.append(playerName[:-1])
            
    # add 1 to doppelganger in playerNames
    for k in range(4):
        for l in range(len(doppelganger)):
            if playerNames[k] == doppelganger[l]:
                playerNames[k] = playerNames[k]+str(1)
    return playerNames

def shortString(string):
    # Input: string/with/slashes/and/maybe/dot/with.suffix
    # Output: with
    k = 0
    char = ""
    while k<len(string) and char != "." and char != "/":
        char = string[::-1][k]
        k+=1
    # char == "/" or "."
    
    newString = string
    if char == ".":
        # remove ".suffix"
        newString = string[:-k]
    elif char == "/":
        # remove "string/with/slashes/and/maybe/dot/"
        newString = string[len(string)-k+1:]
    
    # repeat as often as necessary
    if newString != string:
        newString = shortString(newString)
    return newString

# following functions are needed for the gui

def findValue(line):

    k = 0
    while line[k] != '=':
        k+=1
    # k+1 is first char after '='
    
    k+=1
    while line[k] == ' ':
        k+=1
    # line[k] is first char in value

    value = ''
    while k<len(line) and line[k] != ' ' and line[k] != '\n':
        value += line[k]
        k+=1
    return value
    
def AiIsNotActivatedYet(gameStats,Ai):
    
    challenges = ('Noob','Intermediate','Advanced','Expert')
    
    if gameStats.getChallenge() == challenges[0]:
        # first challenge => no 'Intermediate' , 'Advanced' or 'Expert'
        if challenges[1] in Ai or challenges[2] in Ai or challenges[3] in Ai:
            return True
    
    if gameStats.getChallenge() == challenges[1]:
        # second challenge => no 'Advanced' or 'Expert'
        if challenges[2] in Ai or challenges[3] in Ai:
            return True
    
    if gameStats.getChallenge() == challenges[2]:
        # third challenge => no 'Expert'
        if challenges[3] in Ai:
            return True
    
    return False
    
def findChallenge(gameStats,Ai,rounds,Map):
    # Here the AIs for the challenges are defined
    # For Radiobuttons see gui.player().updateRadiobutton()
    
    for k in range(len(Ai)):
        Ai[k]=shortString(Ai[k])
        
    challengesList = ['Noob','Intermediate','Advanced','Expert']  
    for challenge in challengesList:
        if challenge == 'Noob' or challenge == 'Intermediate':
            numberOfChallengedAIs = 0  
            for name in Ai:
                if name == challenge:
                    numberOfChallengedAIs += 1
            if numberOfChallengedAIs == 3 and 'yourAI' == Ai[0] and rounds == gameStats.getRounds(challenge) and Map == gameStats.getMap(challenge):
                return challenge
        elif challenge == 'Advanced':
            if Ai[0] == 'yourAI' and Ai[1] == 'Dummy' and Ai[2] == 'Dummy' and Ai[3] == 'Advanced' and rounds == gameStats.getRounds(challenge) and Map == gameStats.getMap(challenge):
                return 'Advanced'
        elif challenge == 'Expert':
            if Ai[0] == 'yourAI' and Ai[1] == 'Intermediate' and Ai[2] == 'Advanced' and Ai[3] == 'Expert' and rounds == gameStats.getRounds(challenge) and Map == gameStats.getMap(challenge):
                return 'Expert'
    return 'Custom'
    
def challengeMatchWon(winner,gameStats,challenge):
    
    if gameStats.getChallenge() == challenge and len(winner) == 1 and winner[0] == 'yourAI':
        # Challenge done
        return True
    return False
    
def challengeDone(winner,gameStats,challenge):
    
    if gameStats.getChallenge() == challenge and len(winner) == 1 and winner[0] == 'yourAI' and gameStats.getCurrentMatches()== gameStats.getCurrentCounter():
        # Challenge done
        return True
    return False

def updateConfig(rounds,mapName,Ai,speed):
    
    config = open('config.ini','w')
    config.write('[Default Rounds]\nRounds = '+str(rounds)+'\n\n[Default Map]\nMap = '+mapName+'\n\n[Default AIs]\nAI_1 = '+Ai[0]+'\nAI_2 = '+Ai[1]+'\nAI_3 = '+Ai[2]+'\nAI_4 = '+Ai[3]+'\n\n[Default Speed]\nSpeed = '+str(speed))
    config.close()
    
    return None

def reward(gameStats):
    
    if True:       
         
        # Maps
        if gameStats.getChallenge() == 'Noob':
            MapFile = open('maps/circle.map','w')
            MapFile.write(gameStats.getRewardMap('circle'))
            MapFile.close()
            MapFile = open('maps/source.map','w')
            MapFile.write(gameStats.getRewardMap('circle'))
            MapFile.close()
        elif gameStats.getChallenge() == 'Intermediate':
            MapFile = open('maps/labyrinth.map','w')
            MapFile.write(gameStats.getRewardMap('labyrinth'))
            MapFile.close()
            MapFile = open('maps/backyard.map','w')
            MapFile.write(gameStats.getRewardMap('backyard'))
            MapFile.close()
        elif gameStats.getChallenge() == 'Advanced':
            MapFile = open('maps/central.map','w')
            MapFile.write(gameStats.getRewardMap('central'))
            MapFile.close()
            MapFile = open('maps/tight_corridors.map','w')
            MapFile.write(gameStats.getRewardMap('tight_corridors'))
            MapFile.close()
        elif gameStats.getChallenge() == 'Expert':
            MapFile = open('maps/garden.map','w')
            MapFile.write(gameStats.getRewardMap('garden'))
            MapFile.close()
        
        # Source-Code
        AiFile = open(gameStats.getChallenge()+'.py','w')
        AiFile.write(gameStats.getCodeAi(gameStats.getChallenge()))
        AiFile.close()
        
        FunctionsFile = open(gameStats.getChallenge()+'Functions.py','w')
        FunctionsFile.write(gameStats.getCodeFunctions(gameStats.getChallenge()))
        FunctionsFile.close()
    
    # update Challenge
    gameStats.updateChallenge()  

    # Save gameStats
    pickle.dump(gameStats,open('game.dat','wb'))
    
    return None
    
def UserImportedAi(ai):
    
    txt = open(ai+'.py','r')
    
    AiImported = False
    for line in txt:
        if ("Expert" in line or "Advanced" in line or "Intermediate" in line or "Noob" in line) and "import" in line:
            AiImported = True
    
    return AiImported

def cheat():
    gameStats = pickle.load(open('game.dat','wb'))
    for i in range(4):
        reward(gameStats)
    return None
