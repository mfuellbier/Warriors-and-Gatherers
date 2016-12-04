#!/usr/bin/python
# -*- coding: utf-8 -*-

# IntermediateFunctions.py
#####################################################################
#### Don't touch this! Otherwise this client will not be executed ###
#####################################################################
from classes import *                   						  ###
import random   												  ###
#####################################################################
##### Remember Pythons off-side-rule! Use 4-space indentation! ######
#####################################################################

# In this file you can define functions and classes, which can be called in your BattleClient

dictionaryDirection = {str([0,0]):Direction.STAY, str([-1,0]):Direction.WEST, str([1,0]):Direction.EAST, str([0,1]):Direction.SOUTH, str([0,-1]):Direction.NORTH}

# TODO: Sometimes floods all

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

def rankFieldsAround(position,rankMap,Map,myName,destination):

    # ranks the fields around rankMap[position[0]][position[1]]
    # if destination = Base 'b', then fields with own units will be ranked
    # if destination = Resource 'r', then fields with own units won't be ranked => no traffic jam
    xPos = position[0]
    yPos = position[1]
    rank = rankMap[xPos][yPos]+1
    #raiseNumberOfImportandFieldsRanked = False
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
                            if Map[X][Y].getFieldType() != FieldType.BASE and Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() == myName and destination == 'b':
                                if rankMap[X][Y] == 'b':
                                    numberOfImportandFieldsAround += 1
                                rankMap[X][Y] = None
                            else:
                                if rankMap[X][Y] == None:
                                    rankMap[X][Y] = rank
                                else:
                                    rankMap[X][Y] = min(rank,rankMap[X][Y])
    return numberOfImportandFieldsAround             

def rankFieldsAround(position,rankMap,Map,myName,destination):

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
                            if Map[X][Y].getFieldType() != FieldType.BASE and Map[X][Y].getUnitOnField() != None and Map[X][Y].getUnitOnField().getOwner() == myName and destination != rankMap[X][Y]:
                                # no Base, own unit and unit has another job than rankMap
                                if destination == 'r':
                                    if type(rankMap[X][Y]) == int:
                                        rankMap[X][Y] = min(rank,rankMap[X][Y])
                                    else:
                                        rankMap[X][Y] = rank
                                elif destination == 'b':
                                    if Map[X][Y].getUnitOnField().getResources() != Map[X][Y].getUnitOnField().getUnitType().getMaxResources():
                                        # Gatherer for resource
                                        rankMap[X][Y] = 'bRanked'   # has finally to be None
                                    else:
                                        if type(rankMap[X][Y]) == int:
                                            rankMap[X][Y] = min(rank,rankMap[X][Y])
                                        else:
                                            rankMap[X][Y] = rank
                            else:
                                # Rank the field
                                if rankMap[X][Y] == 'r' or rankMap[X][Y] == 'b':
                                    numberOfImportandFieldsAround += 1
                                    rankMap[X][Y] = rank
                                elif type(rankMap[X][Y]) == int:
                                        rankMap[X][Y] = min(rank,rankMap[X][Y])
                                elif type(rankMap[X][Y]) != str:
                                    rankMap[X][Y] = rank
    return numberOfImportandFieldsAround   

def flood(rankMap,Map,myName,numberOfImportandFields,destination):
    # Input: rankMap[][] is 0 on destination (resource, own base, enemy unit,...), None elsewhere), Map is reference
    # Floods the rankMap with ranks. Every rank gives the distance to the destination
    fieldsToRank = True
    rank = 0
    numberOfImportandFieldsRanked = 0
    #print('Number of importand Fields:',numberOfImportandFields)
    while fieldsToRank and numberOfImportandFieldsRanked < numberOfImportandFields:
        fieldsToRank = False
        rank += 1
        for x in range(len(rankMap)):
            for y in range(len(rankMap[x])):
                field = rankMap[x][y]
                if field == rank-1:
                    numberOfImportandFieldsAround = rankFieldsAround([x,y],rankMap,Map,myName,destination)
                    fieldsToRank = True
                    numberOfImportandFieldsRanked += numberOfImportandFieldsAround
        #print(rank,' number of Fields:',numberOfImportandFieldsRanked)
    rank += 1
    for x in range(len(rankMap)):
        for y in range(len(rankMap[x])):
            field = rankMap[x][y]
            if field == rank-1:
                raiseNumberOfImportandFieldsRanked = rankFieldsAround([x,y],rankMap,Map,myName,destination)
                fieldsToRank = True
                if destination == 'r':
                    if Map[x][y].getUnitOnField() != None and Map[x][y].getFieldType() != FieldType.BASE and Map[x][y].getUnitOnField().getOwner() == myName:
                        numberOfImportandFieldsRanked +=1
                    elif Map[x][y].getFieldType() == FieldType.BASE and Map[x][y].getBase().getOwner() == myName and len(Map[x][y].getBase().getHiddenUnits()) > 0:
                        numberOfImportandFieldsRanked +=1
                elif raiseNumberOfImportandFieldsRanked:
                    numberOfImportandFieldsRanked +=1      
    return None

def getRankMapResources(Map,myName,hiddenUnits):    
    
    rankMap = createDummyRankMap(Map)
    numberOfImportantFields = 0
    #print('Resources')
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if field.getResources() > 0:
                rankMap[x][y] = 0
            elif field.getBase() != None and field.getBase().getOwner() == myName and hiddenUnits != []:
                # own base, if units in base
                rankMap[x][y] = 'r'
                numberOfImportantFields += 1
            elif field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() == myName:
                # own unit
                rankMap[x][y] = 'r'
                numberOfImportantFields += 1
            else:
                rankMap[x][y] = None
    # Flood the map
    #printRankMap(rankMap)
    flood(rankMap,Map,myName,numberOfImportantFields,'r')
    #printRankMap(rankMap)
    return rankMap
    
def getRankMapBase(Map,myName):
    
    rankMap = createDummyRankMap(Map)
    numberOfImportantFields = 0
    #print('Base')
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            field = Map[x][y]
            if field.getBase() != None and field.getBase().getOwner() == myName:
                rankMap[x][y] = 0
            elif field.getBase() == None and field.getUnitOnField() != None and field.getUnitOnField().getOwner() == myName and field.getUnitOnField().getResources() == field.getUnitOnField().getUnitType().getMaxResources():
                rankMap[x][y] = 'b'
                numberOfImportantFields += 1
            else:
                rankMap[x][y] = None
    # Flood the map
    #printRankMap(rankMap)
    flood(rankMap,Map,myName,numberOfImportantFields,'b')
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            if rankMap[x][y] == 'b' or rankMap[x][y] == 'bRanked':
                rankMap[x][y] = None
    #printRankMap(rankMap)
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

def isGathererWorth(rankMapResources,base,roundsToGo):
    
    if rankMapResources == None:
        return False
    
    distanceResource = rankMapResources[base.getPosition()[0]][base.getPosition()[1]]
    if distanceResource == None:
        # No Resource on Map
        return False
    if roundsToGo > 2*distanceResource:
        return True
    else:
        return False
