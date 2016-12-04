#!/usr/bin/python
# -*- coding: utf-8 -*-

# Advanced.py
#####################################################################
### Don't touch this! Otherwise this client will not be executed! ###
#####################################################################
from classes import *           								  ###
from AdvancedFunctions import *							          ###
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
    
    dictionaryDirection = {str([0,0]):Direction.STAY, str([-1,0]):Direction.WEST, str([1,0]):Direction.EAST, str([0,1]):Direction.SOUTH, str([0,-1]):Direction.NORTH}
    
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
    gathererOnMap = False
    warriorsAreHunting = False
    
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            if Map[x][y].getUnitOnField() != None and Map[x][y].getFieldType() != FieldType.BASE and Map[x][y].getUnitOnField().getOwner() != myName:
                counterEnemy += 1
                if str(Map[x][y].getUnitOnField().getUnitType()) == UnitType.GATHERER:
                    gathererOnMap = True
    
    # Create units
    while resources >= gathererCost and counterGatherer<len(Map)/4:
        roundState.getBase().createUnitGatherer()
        resources -= gathererCost
        counterGatherer += 1
    
    while resources >= warriorCost and counterWarrior<counterEnemy:
        roundState.getBase().createUnitWarrior()
        resources -= warriorCost
        counterWarrior += 1
    
    if counterEnemy > 0 and counterWarrior > 0 and counterGatherer > 0:
        warriorsAreHunting = True
    
    
    # ==== Rank Maps ====    
    
    # Enemy
    
    if warriorsAreHunting:
        if gathererOnMap:
            rankMapEnemy = getRankMapUnit(Map,myName,base.getHiddenUnits(),UnitType.GATHERER)
        else:
            rankMapEnemy = getRankMapUnit(Map,myName,base.getHiddenUnits(),UnitType.WARRIOR)
    
    # Resources
      
    # Create RankMapResources
    (rankMapResources,rankMapResourcesEmpty) = getRankMapResources(Map,myName,base.getHiddenUnits(),warriorsAreHunting)
    
    if not warriorsAreHunting:
        rankMapEnemy = rankMapResources

    # Base
    
    # Create RankMapBase
    rankMapBase = getRankMapBase(Map,myName,warriorsAreHunting)
                
    # Move units
    for unit in units:
        if unit.getUnitType().getString() == UnitType.GATHERER or not warriorsAreHunting:            
            if unit.getResources() == unit.getUnitType().getMaxResources():
                # back to base
                [direction,unitIsFleeing] = checkIfEnemyInMedio(unit,rankMapBase,Map,myName)
                if not unitIsFleeing:
                    direction = getDirectionOnRankMap(rankMapBase,Map,unit)
                unit.moveUnit(direction)
            else:
                if rankMapResourcesEmpty:
                    [direction,unitIsFleeing] = checkIfEnemyInMedio(unit,rankMapBase,Map,myName)
                    if not unitIsFleeing:
                        direction = Direction.STAY
                else:
                    [direction,unitIsFleeing] = checkIfEnemyInMedio(unit,rankMapResources,Map,myName)
                    if not unitIsFleeing:
                        direction = getDirectionOnRankMap(rankMapResources,Map,unit)

                unit.moveUnit(direction)
        else:
            # unit is Warrior and there are Enemies on the map
            # Check, if unit is next to an enemy
            [direction,nextToWarrior,nextToGatherer] = checkIfEnemyInCorto(unit,Map,myName)
            if not nextToWarrior and not nextToGatherer:
                direction = getDirectionOnRankMap(rankMapEnemy,Map,unit)
            unit.moveUnit(direction)
    
    

