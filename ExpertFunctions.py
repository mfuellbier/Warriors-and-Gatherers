#!/usr/bin/python
# -*- coding: utf-8 -*-

# ExpertFunctions.py
#####################################################################
#### Don't touch this! Otherwise this client will not be executed ###
#####################################################################
from classes import *         
import random                             						  ###
																  ###
#####################################################################
##### Remember Pythons off-side-rule! Use 4-space indentation! ######
#####################################################################

# In this file you can define functions and classes, which can be called in your BattleClient

dictionaryDirection = {str([0,0]):Direction.STAY, str([-1,0]):Direction.WEST, str([1,0]):Direction.EAST, str([0,1]):Direction.SOUTH, str([0,-1]):Direction.NORTH}
    
def createDummyRankMap(Map):
    rankMap = [None]*len(Map[0])
    for k in range(len(Map[0])):
        rankMap[k] = [None]*len(Map)
    
    return rankMap

def printRankMap(rankMap):
    if rankMap == None:
        return None
    for k in range(len(rankMap)):
        print(rankMap[k])
    return None

def rankFieldsAround(position,rankMap,Map,myName,destination,warriorsAreHunting):

    # ranks the fields around rankMap[position[0]][position[1]]
    # if destination = Base 'b', then fields with own units will be ranked
    # if destination = Resource 'r', then fields with own units won't be ranked => no traffic jam
    xPos = position[0]
    yPos = position[1]
    rank = rankMap[xPos][yPos]+1
    numberOfImportandFieldsAround = 0
    for x in [-1,0,1]:
        X=x+xPos
        for y in [-1,0,1]:
            Y=y+yPos
            if ((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1)):
                if min(Y,X) >=0 and max(Y,X)<len(rankMap):
                    if Map[X][Y].getFieldType() == FieldType.RESOURCE or Map[X][Y].getFieldType() == FieldType.LAND or Map[X][Y].getFieldType() == FieldType.BASE:
                        if Map[X][Y].getFieldType() != FieldType.BASE or Map[X][Y].getBase().getOwner() == myName:
                            # field is either of type land or resource or own base
                            # evasion
                            if Map[X][Y].getFieldType() != FieldType.BASE and Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() == myName and rankMap[X][Y] != destination:
                                # no Base, own unit and unit has another job than rankMap
                                if destination == 'e':
                                    rankMap[X][Y] == 'eRanked'   # has finally to be None
                                elif destination == 'r':
                                    if type(rankMap[X][Y]) == int:
                                        rankMap[X][Y] = min(rank,rankMap[X][Y])
                                    else:
                                        rankMap[X][Y] = rank
                                elif destination == 'b':
                                    if Map[X][Y].getUnitOnField().getResources() != Map[X][Y].getUnitOnField().getUnitType().getMaxResources() and (str(Map[X][Y].getUnitOnField().getUnitType()) == UnitType.GATHERER or not warriorsAreHunting):
                                        # Gatherer for resource
                                        rankMap[X][Y] = 'bRanked'   # has finally to be None
                                    else:
                                        if type(rankMap[X][Y]) == int:
                                            rankMap[X][Y] = min(rank,rankMap[X][Y])
                                        else:
                                            rankMap[X][Y] = rank
                            else:
                                # Rank the field
                                if rankMap[X][Y] == 'r' or rankMap[X][Y] == 'b' or rankMap[X][Y] == 'e':
                                    numberOfImportandFieldsAround += 1
                                    rankMap[X][Y] = rank
                                elif type(rankMap[X][Y]) == int:
                                        rankMap[X][Y] = min(rank,rankMap[X][Y])
                                elif type(rankMap[X][Y]) != str:
                                    rankMap[X][Y] = rank
    return numberOfImportandFieldsAround            

def flood(rankMap,Map,myName,numberOfImportandFields,destination,warriorsAreHunting):
    # Input: rankMap[][] is 0 on destination (resource, own base, enemy unit,...), None elsewhere), Map is reference
    # Floods the rankMap with ranks. Every rank gives the distance to the destination
    fieldsToRank = True
    rank = 0
    numberOfImportandFieldsRanked = 0
    while fieldsToRank and numberOfImportandFieldsRanked < numberOfImportandFields:
        fieldsToRank = False
        rank += 1
        for x in range(len(rankMap)):
            for y in range(len(rankMap[x])):
                field = rankMap[x][y]
                if field == rank-1:
                    numberOfImportandFieldsAround = rankFieldsAround([x,y],rankMap,Map,myName,destination,warriorsAreHunting)
                    fieldsToRank = True
                    numberOfImportandFieldsRanked += numberOfImportandFieldsAround
    rank += 1
    for x in range(len(rankMap)):
        for y in range(len(rankMap[x])):
            field = rankMap[x][y]
            if field == rank-1:
                rankFieldsAround([x,y],rankMap,Map,myName,destination,warriorsAreHunting)
    return None

def getRankMapResources(Map,myName,hiddenUnits,warriorsAreHunting,gameConfiguration,roundState):    
    rankMap = createDummyRankMap(Map)

    counterUnitsForResources = 0
    destinationOnMap = False
    
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if field.getResources() > 0 and (field.getUnitOnField() == None or field.getUnitOnField().getOwner() != myName or (str(field.getUnitOnField().getUnitType()) == UnitType.WARRIOR and warriorsAreHunting)):
                rankMap[x][y] = 0
                destinationOnMap = True
            elif field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() == myName and field.getUnitOnField().getResources() != field.getUnitOnField().getUnitType().getMaxResources() and (str(field.getUnitOnField().getUnitType()) == UnitType.GATHERER or not warriorsAreHunting):
                rankMap[x][y] = 'r'
                counterUnitsForResources += 1
            elif field.getBase() != None and field.getBase().getOwner() == myName and (hiddenUnits != [] or gameConfiguration.getUnitCostGatherer() <= roundState.getBase().getResources()):
                hiddenUnitForResources = False
                rankMap[x][y] = None
                if hiddenUnits != []:
                    for unit in hiddenUnits:
                        if str(unit.getUnitType()) == UnitType.GATHERER or not warriorsAreHunting:
                            hiddenUnitForResources = True
                    if hiddenUnitForResources:
                        counterUnitsForResources += 1
                        rankMap[x][y] = 'r'
                # check if it could be worth to create gatherers
                if hiddenUnitForResources == False and roundState.getRoundNumber() <= gameConfiguration.getRounds()/2:
                    counterUnitsForResources += 1
                    rankMap[x][y] = 'r'
            else:
                rankMap[x][y] = None
    # Flood the map
    if destinationOnMap:
        flood(rankMap,Map,myName,counterUnitsForResources,'r',warriorsAreHunting)
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if rankMap[x][y] == 'r' or rankMap[x][y] == 'rRanked':
                rankMap[x][y] = None
    return (rankMap,not destinationOnMap)
    
def getRankMapBase(Map,myName,warriorsAreHunting):
    rankMap = createDummyRankMap(Map)
    
    counterUnitsBackToBase = 0
    unitsWantToGetBack = False  
        
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if field.getBase() != None and field.getBase().getOwner() == myName:
                rankMap[x][y] = 0
            elif field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() == myName and field.getUnitOnField().getResources() == field.getUnitOnField().getUnitType().getMaxResources() and (str(field.getUnitOnField().getUnitType()) == UnitType.GATHERER or not warriorsAreHunting):
                rankMap[x][y] = 'b'
                counterUnitsBackToBase += 1
                unitsWantToGetBack = True
            else:
                rankMap[x][y] = None
    # Flood the map
    if unitsWantToGetBack:
        flood(rankMap,Map,myName,counterUnitsBackToBase,'b',warriorsAreHunting)
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            if rankMap[x][y] == 'bRanked' or rankMap[x][y] == 'b':
                rankMap[x][y] = None
    return rankMap
    
def getRankMapUnit(Map,myName,hiddenUnits,unitType,gameConfiguration,roundState):
    rankMap = createDummyRankMap(Map)
    
    counterWarriors = 0
    destinationOnMap = False
    
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() != myName and str(field.getUnitOnField().getUnitType()) == unitType:
                rankMap[x][y] = 0
                destinationOnMap = True
            elif field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() == myName and str(field.getUnitOnField().getUnitType()) == UnitType.WARRIOR:
                rankMap[x][y] = 'e'
                counterWarriors += 1
            elif field.getBase() != None and field.getBase().getOwner() == myName and (hiddenUnits != [] or gameConfiguration.getUnitCostWarrior() <= roundState.getBase().getResources()):
                rankMap[x][y] = None
                hiddenUnitForEnemy = False
                if hiddenUnits != []:
                    for unit in hiddenUnits:
                        if str(unit.getUnitType()) == UnitType.WARRIOR:
                            hiddenUnitForEnemy = True
                    if hiddenUnitForEnemy:
                        counterWarriors += 1 
                        rankMap[x][y] = 'e'  
                # check if it could be worth to create warriors
                if hiddenUnitForEnemy == False and roundState.getRoundNumber() <= 2*gameConfiguration.getRounds()/3:
                    counterWarriors += 1
                    rankMap[x][y] = 'e'
            else:
                rankMap[x][y] = None
    # Flood the map
    if destinationOnMap:
        flood(rankMap,Map,myName,counterWarriors,'e',True)
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            if rankMap[x][y] == 'eRanked' or rankMap[x][y] == 'e':
                rankMap[x][y] = None
    return rankMap
    
def pickRandomFromList(listOfDirections):
    if len(listOfDirections) == 1:
        return listOfDirections[0]
    elif len(listOfDirections) == 2:
        if random.random() < 0.5:
            return listOfDirections[0]
        else:
            return listOfDirections[1]
    elif len(listOfDirections) == 3:
        if random.random() < 1/3:
            return listOfDirections[0]
        elif random.random() < 2/3:
            return listOfDirections[1]
        else:
            return listOfDirections[2]
    else:
        if random.random() < 1/4:
            return listOfDirections[0]
        elif random.random() < 1/2:
            return listOfDirections[1]
        elif random.random() < 3/4:
            return listOfDirections[2]
        else:
            return listOfDirections[3]
    
def getDirectionOnRankMap(rankMap,Map,unit):
    xPos = unit.getPosition()[0]
    yPos = unit.getPosition()[1]
    rank = rankMap[xPos][yPos]
    direction = Direction.STAY
    
    minRank = len(rankMap)*len(rankMap)
    for x in [-1,0,1]:
        X=x+xPos
        for y in [-1,0,1]:
            Y=y+yPos
            if (((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1))) and rankMap[X][Y] != None:
                if rankMap[X][Y] < rank:
                    minRank = rankMap[X][Y]
    
    possibleDirection = []
    for x in [-1,0,1]:
        X=x+xPos
        for y in [-1,0,1]:
            Y=y+yPos
            if (((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1))) and rankMap[X][Y] != None:
                if rankMap[X][Y] == minRank:
                    possibleDirection.append(dictionaryDirection[str([x,y])])
    
    if possibleDirection == []:
        return direction
    else:
        return pickRandomFromList(possibleDirection)

def checkIfEnemyInCorto(unit,Map,myName):
    # returns direction to next enemy to fight
    xPos = unit.getPosition()[0]
    yPos = unit.getPosition()[1]
    nextToGatherer = False
    nextToWarrior = False
    direction = Direction.STAY
    for x in [-1,0,1]:
        X=x+xPos
        for y in [-1,0,1]:
            Y=y+yPos
            if ((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1)):
                field = Map[X][Y]
                if field.getFieldType() != FieldType.BASE and field.getUnitOnField() != None and field.getUnitOnField().getOwner() != myName:
                    if str(field.getUnitOnField().getUnitType()) == UnitType.GATHERER:
                        nextToGatherer = True
                        direction = dictionaryDirection[str([x,y])]
                    elif not nextToGatherer:
                        direction = dictionaryDirection[str([x,y])]
                        nextToWarrior = True
    return [direction,nextToWarrior,nextToGatherer]

def checkIfEnemyInMedio(unit,rankMap,Map,myName):
    unitIsFleeing = False
    enemyInCorto = False
    xPos = unit.getPosition()[0]
    yPos = unit.getPosition()[1]
    direction = Direction.STAY
    possibleDirectionsDict = {Direction.NORTH:[xPos,yPos-1],Direction.EAST:[xPos+1,yPos],Direction.SOUTH:[xPos,yPos+1],Direction.WEST:[xPos-1,yPos]}
    
    # Corto
    possibleDirections = {Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST}
    for x in [-1,0,1]:
        X=x+xPos
        if X < 0 or X >= len(Map):
            continue
        for y in [-1,0,1]:
            Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
            if ((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1)):
                # Cross-Pattern
                field = Map[X][Y]
                if field.getFieldType() != FieldType.BASE and field.getUnitOnField() != None and field.getUnitOnField().getOwner() != myName:
                    unitIsFleeing = True
                    enemyInCorto = True
                    if y > 0:
                        if Direction.SOUTH in possibleDirections:
                            possibleDirections.remove(Direction.SOUTH)
                    if y < 0:
                        if Direction.NORTH in possibleDirections:
                            possibleDirections.remove(Direction.NORTH)
                    if x > 0:
                        if Direction.EAST in possibleDirections:
                            possibleDirections.remove(Direction.EAST)
                    if x < 0:
                        if Direction.WEST in possibleDirections:
                            possibleDirections.remove(Direction.WEST)
    if unitIsFleeing and possibleDirections == {}:
        return [direction,False]                   
 
    PossibleDirectionFound = False
    for x in [-2,-1,0,1,2]:
        X=x+xPos
        if X < 0 or X >= len(Map):
            continue
        for y in [-2,-1,0,1,2]:
            Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
            if ((x == -2 or x == 2) and y == 0) or (x == 0 and (y == -2 or y == 2)) or ((x == 1 or x == -1) and (y == 1 or y == -1)):
                # Diamond-Pattern
                if Map[X][Y].getFieldType() != FieldType.BASE and Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() != myName:
                    unitIsFleeing = True
                    if y > 0:
                        if Direction.SOUTH in possibleDirections:
                            possibleDirections.remove(Direction.SOUTH)
                    if y < 0:
                        if Direction.NORTH in possibleDirections:
                            possibleDirections.remove(Direction.NORTH)
                    if x > 0:
                        if Direction.EAST in possibleDirections:
                            possibleDirections.remove(Direction.EAST)
                    if x < 0:
                        if Direction.WEST in possibleDirections:
                            possibleDirections.remove(Direction.WEST)
        
    rank = len(rankMap)*len(rankMap)
    for x in [-1,0,1]:
        X=x+xPos
        if X < 0 or X >= len(Map):
            continue
        for y in [-1,0,1]:
            Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
            if (((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1))) and rankMap[X][Y] != None:
                # Cross-Pattern
                if rankMap[X][Y] < rank and dictionaryDirection[str([x,y])] in possibleDirections:
                    PossibleDirectionFound = True
                    rank = rankMap[X][Y]
                    direction = dictionaryDirection[str([x,y])]
    
    if enemyInCorto and not PossibleDirectionFound:
        # Attack enemyInCorto
        for x in [-1,0,1]:
            X=x+xPos
            if X < 0 or X >= len(Map):
                continue
            for y in [-1,0,1]:
                Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
                if (((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1))) and rankMap[X][Y] != None:
                    # Cross-Pattern
                    if rankMap[X][Y] < rank and Map[X][Y].getUnitOnField() != None and Map[X][Y].getFieldType() == FieldType.BASE and Map[X][Y].getUnitOnField().getOwner() != myName:
                        rank = rankMap[X][Y]
                        direction = dictionaryDirection[str([x,y])]
    return [direction,unitIsFleeing]
                        
def checkIfEnemyInMedioWarrior(unit,Map,myName):
    enemyInCorto = False
    gathererInCorto = False
    warriorInCorto = False
    enemyInMedio = False
    
    xPos = unit.getPosition()[0]
    yPos = unit.getPosition()[1]
    
    directionGat = Direction.STAY
    directionWar = Direction.STAY
    direction = Direction.STAY
    possibleDirectionsDict = {Direction.NORTH:[xPos,yPos-1],Direction.EAST:[xPos+1,yPos],Direction.SOUTH:[xPos,yPos+1],Direction.WEST:[xPos-1,yPos]}
    
    # Corto
    for x in [-1,0,1]:
        X=x+xPos
        if X < 0 or X >= len(Map):
            continue
        for y in [-1,0,1]:
            Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
            if ((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1)):
                # Cross-Pattern
                field = Map[X][Y]
                if field.getFieldType() != FieldType.BASE and field.getUnitOnField() != None and field.getUnitOnField().getOwner() != myName and str(field.getUnitOnField().getUnitType()) == UnitType.GATHERER:
                    gathererInCorto = True
                    enemyInCorto = True
                    if y > 0:
                        directionGat = Direction.SOUTH
                    if y < 0:
                        directionGat = Direction.NORTH
                    if x > 0:
                        directionGat = Direction.EAST
                    if x < 0:
                        directionGat = Direction.WEST
                if field.getFieldType() != FieldType.BASE and field.getUnitOnField() != None and field.getUnitOnField().getOwner() != myName and str(field.getUnitOnField().getUnitType()) == UnitType.WARRIOR:
                    warriorInCorto = True
                    enemyInCorto = True
                    if y > 0:
                        directionWar = Direction.SOUTH
                    if y < 0:
                        directionWar = Direction.NORTH
                    if x > 0:
                        directionWar = Direction.EAST
                    if x < 0:
                        directionWar = Direction.WEST
    if gathererInCorto:
        direction = directionGat
    elif warriorInCorto:
        direction = directionWar
    
    friendCounter = 0
    for x in [-2,-1,0,1,2]:
        X=x+xPos
        if X < 0 or X >= len(Map):
            continue
        for y in [-2,-1,0,1,2]:
            Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
            if ((x == -2 or x == 2) and y == 0 and Map[xPos + int(x/abs(x))][Y].getFieldType() != FieldType.WALL and Map[xPos + int(x/abs(x))][Y].getFieldType() != FieldType.WATER) or (x == 0 and (y == -2 or y == 2) and Map[X][yPos + int(y/abs(y))].getFieldType() != FieldType.WALL and Map[X][yPos + int(y/abs(y))].getFieldType() != FieldType.WATER) or ((x == 1 or x == -1) and (y == 1 or y == -1)):
                # Diamond-Pattern
                if Map[X][Y].getFieldType() != FieldType.BASE and Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() != myName:
                    # there is enemy in medio
                    enemyInMedio = True
            if Map[X][Y].getFieldType() != FieldType.BASE and Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() == myName and str(Map[X][Y].getUnitOnField().getUnitType()) == UnitType.WARRIOR:
                friendCounter += 1
                    
    print(friendCounter)
    
    looseTrafficJam = False
    if enemyInMedio and friendCounter >= 3:
        looseTrafficJam = True        
                        
    return [direction,enemyInMedio,enemyInCorto,looseTrafficJam]

def checkForTrafficJam(Map,unit,myName):
    trafficJam = False
    xPos = unit.getPosition()[0]
    yPos = unit.getPosition()[1]
    
    for x in [-1,0,1]:
        X=x+xPos
        if X < 0 or X >= len(Map):
            continue
        for y in [-1,0,1]:
            Y=y+yPos
            if Y < 0 or Y >= len(Map):
                continue
            if ((x == -1 or x == 1) and y == 0) or (x == 0 and (y == -1 or y == 1)):
                # Cross-Pattern
                field = Map[X][Y]
                if field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() == myName and field.getUnitOnField().getLastMove() == Direction.STAY:
                    trafficJam = True
    return trafficJam

def getRandomDirection(Map,unit):
    xPos = unit.getPosition()[0]
    yPos = unit.getPosition()[1]
    possibleDirectionsDict = {Direction.NORTH:[xPos,yPos-1],Direction.EAST:[xPos+1,yPos],Direction.SOUTH:[xPos,yPos+1],Direction.WEST:[xPos-1,yPos]}
    
    X=0
    Y=0
    k=0
    direction = Direction.STAY
    while not Map[X][Y].isCrossable(unit) and k<9:
        k+=1
        if random.random() < 0.25:
            directionTemp = Direction.NORTH
        elif random.random() < 0.5:
            directionTemp = Direction.EAST
        elif random.random() < 0.75:
            directionTemp = Direction.SOUTH
        else:
            directionTemp = Direction.WEST
        X = possibleDirectionsDict[directionTemp][0]
        Y = possibleDirectionsDict[directionTemp][1]
        if Map[X][Y].isCrossable(unit):
            direction = directionTemp
    return direction
