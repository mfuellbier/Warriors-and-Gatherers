#!/usr/bin/python
# -*- coding: utf-8 -*-

# Intermediate.py
#####################################################################
### Don't touch this! Otherwise this client will not be executed! ###
#####################################################################
from classes import *           								  ###
from IntermediateFunctions import *						          ###
                            									  ###
def BattleClient(roundState, gameConfiguration):				  ###
#####################################################################
##### Remember Pythons off-side-rule! Use 4-space indentation! ######
#####################################################################

    base = roundState.getBase()
    resources = base.getResources() # = 200 in the beginning
    myName = base.getOwner()
    """
    base contains information:
    base.getPosition() = [x,y]
    base.getHiddenUnits() # List of units in the Base
    base.createUnitWarrior() # Creates a Warrior in the Base, if there are enough resources
    base.createUnitGatherer() # Creates a Gatherer in the Base, if there are enough resources
    """
    Map = roundState.getMap()
    """
    Map contains information:
    Map is a list of lists of Fields, i.e.
    Map[x][y] is a Field with Position [x,y], where [0,0] is the top left corner, [0,19] is the bottom left corner, [19,0] is the top right corner and [19,19] is the bottom right corner
    Field.getFieldType() is either 'WALL', 'WATER', 'RESOURCE', 'BASE' or 'LAND'
    WALL and WATER are not crossable. BASE is only crossable, if it's your own. RESOURCE is a field, where resources appear
    Field.getResources() is the amount of Resources, which are on the field. If the Field is BASE or if a unit is on it, then it's 0.
    Field.getUnitOnField() is of class Unit, if there is one unit on Field. 0 if Field is empty, [Unit] if Field.getFieldType() == FieldType.BASE
    Unit.getOwner() is the owner of the unit
    Unit.getUnitId() is the Unit-ID. Each players units have unique Unit-IDs. i.e. Player 1 and Player 2 might have units with ID x, but Player 1 only can have up to one unit with ID x.
    Unit.getUnitType() is of class UnitType. str(Unit.getUnitType()) gives a string, either 'WARRIOR' or 'GATHERER'
    Unit.getResources() is the amount of resources the unit is carrying
    Unit.getPosition() = [x,y]
    """
    rounds = gameConfiguration.getRounds()	# Number of Rounds for the match = duration of the match
    roundNumber = roundState.getRoundNumber() # Current round number
    roundsToGo = rounds-roundNumber
    units = roundState.getOwnUnits() # List of own Units, in the beginning [], it's going to be manipulated during execution of the script
    warriorCost = gameConfiguration.getUnitCostWarrior()
    gathererCost = gameConfiguration.getUnitCostGatherer()
    maxResourceWarrior = gameConfiguration.getUnitMaxResourcesWarrior()	# Maximum amount of resources a Warrior can carry
    maxResourceGatherer = gameConfiguration.getUnitMaxResourcesGatherer()	# Maximum amount of resources a Gatherer can carry
          
          
    # Count units:
    counterGatherer = 0
    counterWarrior = 0
    for unit in units:
        if str(unit.getUnitType()) == UnitType.GATHERER:
            counterGatherer += 1
        else:
            counterWarrior += 1
            
    # Count enemies:
    counterEnemy = 0
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            if Map[x][y].getUnitOnField() != None and Map[x][y].getFieldType() != FieldType.BASE and Map[x][y].getUnitOnField().getOwner() != myName:
                counterEnemy += 1
    
    
    # Create units
    while resources >= gathererCost and counterGatherer<5:
        roundState.getBase().createUnitGatherer()
        resources -= gathererCost
        counterGatherer += 1
    
    while resources >= warriorCost and counterWarrior<len(Map)/3:
        roundState.getBase().createUnitWarrior()
        resources -= warriorCost
        counterWarrior += 1
    
    # Search fo resource
    counterFieldsWithResources = 0
    for X in range(len(Map)):
        for Y in range(len(Map)):
            if Map[X][Y].getResources() > 0:
                counterFieldsWithResources += 1
    
    # Create rankMapResources
    resourceOnField = False
    if counterFieldsWithResources > 0:
        resourceOnField = True 
    
    if resourceOnField:
        rankMapResources = getRankMapResources(Map,myName,base.getHiddenUnits())
    else:
        rankMapResources = None

    
    # Create rankMapBase
    rankMapBaseNeeded = False
    for unit in units:
        if unit.getResources() == unit.getUnitType().getMaxResources():
            rankMapBaseNeeded = True

    if rankMapBaseNeeded:
        rankMapBase = getRankMapBase(Map,myName)
    else:
        rankMapBase = None

    # Move units    
    for unit in units:
        if unit.getResources() == unit.getUnitType().getMaxResources():
            direction = getDirectionOnRankMap(rankMapBase,Map,unit)
            unit.moveUnit(direction)
        else:
            if resourceOnField:
                direction = getDirectionOnRankMap(rankMapResources,Map,unit)
            else:
                direction = Direction.STAY
            unit.moveUnit(direction)
    

