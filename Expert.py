#!/usr/bin/python
# -*- coding: utf-8 -*-

# Expert.py
#####################################################################
### Don't touch this! Otherwise this client will not be executed! ###
#####################################################################
from classes import *           								  ###
from ExpertFunctions import *							          ###
																  ###
def BattleClient(roundState, gameConfiguration):				  ###
#####################################################################
##### Remember Pythons off-side-rule! Use 4-space indentation! ######
#####################################################################

    turnOnWaiting = True

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
    warriorOnMap = False
    warriorsAreHunting = False
    for x in range(len(Map)):
        for y in range(len(Map[x])):
            if Map[x][y].getUnitOnField() != None and Map[x][y].getFieldType() != FieldType.BASE and Map[x][y].getUnitOnField().getOwner() != myName:
                counterEnemy += 1
                if str(Map[x][y].getUnitOnField().getUnitType()) == UnitType.GATHERER:
                    gathererOnMap = True
                if str(Map[x][y].getUnitOnField().getUnitType()) == UnitType.WARRIOR:
                    warriorOnMap = True
                    
    # ==== Rank Maps ====    
    
    
    dummyRankMap = createDummyRankMap(Map)
            
    # Resources
      
    # Create RankMapResources
    (rankMapResources,rankMapResourcesEmpty) = getRankMapResources(Map,myName,base.getHiddenUnits(),warriorsAreHunting,gameConfiguration,roundState)
    
    rankMapEnemyGatherer = rankMapResources
    rankMapEnemyWarrior = rankMapResources
    
    # Enemy
    
    if counterEnemy > 0:
        if gathererOnMap:
            rankMapEnemyGatherer = getRankMapUnit(Map,myName,base.getHiddenUnits(),UnitType.GATHERER, gameConfiguration, roundState)
        if warriorOnMap:
            rankMapEnemyWarrior = getRankMapUnit(Map,myName,base.getHiddenUnits(),UnitType.WARRIOR, gameConfiguration, roundState)        

    
    
    # === Create Units ===
    
    # Create units
    while resources >= gathererCost and counterGatherer<len(Map)/5 and roundState.getRoundNumber() <= gameConfiguration.getRounds()*3/4 and (rankMapResources[base.getPosition()[0]][base.getPosition()[1]] != None and 2*rankMapResources[base.getPosition()[0]][base.getPosition()[1]] + 10 < roundsToGo):
        roundState.getBase().createUnitGatherer()
        resources -= gathererCost
        counterGatherer += 1

    while resources >= warriorCost and counterEnemy > 0 and counterWarrior < min((len(Map)/3)+1,3*counterEnemy) and roundState.getRoundNumber() <= gameConfiguration.getRounds()*3/4 and ((type(rankMapEnemyGatherer[base.getPosition()[0]][base.getPosition()[1]]) == int and 2*rankMapEnemyGatherer[base.getPosition()[0]][base.getPosition()[1]]+counterEnemy < roundsToGo) or (type(rankMapEnemyWarrior[base.getPosition()[0]][base.getPosition()[1]]) == int and 2*rankMapEnemyWarrior[base.getPosition()[0]][base.getPosition()[1]]+counterEnemy < roundsToGo)): 
        roundState.getBase().createUnitWarrior()
        resources -= warriorCost
        counterWarrior += 1
    
    if counterEnemy > 0 and counterWarrior > 0 and counterGatherer > 0:
        warriorsAreHunting = True
    
    if not warriorsAreHunting and rankMapResources != dummyRankMap:
        rankMapEnemyGatherer = rankMapResources
        rankMapEnemyWarrior = rankMapResources

    # === Rank Map ===

    # Base
    
    # Create RankMapBase
    if roundsToGo < gameConfiguration.getRounds()/4:
        rankMapBase = getRankMapBase(Map,myName,False)
    else:
        rankMapBase = getRankMapBase(Map,myName,warriorsAreHunting)
                
    
    # === Move Units ===
    
    # Move units
    for unit in units:        
        if unit.getUnitType().getString() == UnitType.GATHERER or not warriorsAreHunting:   
            if unit.getLastMove() == Direction.STAY:
                # check if it stucks in a traffic jam
                inTrafficJam = checkForTrafficJam(Map,unit,myName)
                if inTrafficJam and (roundNumber % 3 == 1 or roundNumber % 3 == 2):
                    direction = getRandomDirection(Map,unit)
                    unit.moveUnit(direction) 
                    continue                    
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
            if type(rankMapBase[unit.getPosition()[0]][unit.getPosition()[1]]) == int and rankMapBase[unit.getPosition()[0]][unit.getPosition()[1]] < roundsToGo+20 and rankMapBase[unit.getPosition()[0]][unit.getPosition()[1]] > roundsToGo-10 and unit.getResources() == unit.getUnitType().getMaxResources():
                # lateGame
                direction = getDirectionOnRankMap(rankMapBase,Map,unit)
            else:
                # Go on Hunt
                [direction,enemyInMedio,enemyInCorto,looseTrafficJam] = checkIfEnemyInMedioWarrior(unit,Map,myName)
                if enemyInCorto:
                    unit.moveUnit(direction)
                    continue
                elif enemyInMedio and not looseTrafficJam and turnOnWaiting:
                    unit.moveUnit(Direction.STAY)
                    continue
                else:
                    # Chase enemy
                    distanceToWarrior = len(Map)*len(Map[0])
                    distanceToGatherer = len(Map)*len(Map[0])
                    if warriorOnMap and type(rankMapEnemyWarrior[unit.getPosition()[0]][unit.getPosition()[1]]) == int:
                        # distanceToWarrior
                        distanceToWarrior = rankMapEnemyWarrior[unit.getPosition()[0]][unit.getPosition()[1]]
                    if gathererOnMap and type(rankMapEnemyGatherer[unit.getPosition()[0]][unit.getPosition()[1]]) == int:
                        # distanceToGatherer
                        distanceToGatherer = rankMapEnemyGatherer[unit.getPosition()[0]][unit.getPosition()[1]]
                    if distanceToWarrior < distanceToGatherer/3:
                        direction = getDirectionOnRankMap(rankMapEnemyWarrior,Map,unit)
                    else:
                        direction = getDirectionOnRankMap(rankMapEnemyGatherer,Map,unit)
            unit.moveUnit(direction)
        
    

