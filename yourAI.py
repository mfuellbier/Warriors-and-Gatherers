#!/usr/bin/python
# -*- coding: utf-8 -*-

# yourAI.py
#####################################################################
#### Don't touch this! Otherwise this client will not be executed ###
#####################################################################
from classes import *           								  ###
from yourFunctions import *			    				    	  ###
																  ###
def BattleClient(roundState, gameConfiguration):				  ###
#####################################################################
##### Remember Pythons off-side-rule! Use 4-space indentation! ######
#####################################################################

    base = roundState.getBase()
    resources = base.getResources() # = 200 in the beginning
    """
    base contains information:
    base.getPosition() = [x,y]
    base.getOwner() = Players Name
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
    units = roundState.getOwnUnits() # List of own Units, in the beginning []
    warriorCost = gameConfiguration.getUnitCostWarrior()
    gathererCost = gameConfiguration.getUnitCostGatherer()
    maxResourceWarrior = gameConfiguration.getUnitMaxResourcesWarrior()	# Maximum amount of resources a Warrior can carry
    maxResourceGatherer = gameConfiguration.getUnitMaxResourcesGatherer()	# Maximum amount of resources a Gatherer can carry

    
    # Build new units
    while resources >= gathererCost and len(units)<5:
        roundState.getBase().createUnitGatherer()
        resources -= gathererCost
        
        
    # Search fo resource
    resourcePosition = []
    for X in range(len(Map)):
        for Y in range(len(Map)):
            if Map[X][Y].getResources() > 0:
                resourcePosition = [X,Y]
     
    # Move units
    for unit in units:
        if unit.getResources() == unit.getUnitType().getMaxResources():
            # if unit is full => go back to base
            direction = getDirectionForMoveToField(unit,base.getPosition()[0],base.getPosition()[1],Map)
        else:
            # go for resources
            if resourcePosition == []:
                direction = Direction.STAY
            else:
                direction = getDirectionForMoveToField(unit,resourcePosition[0],resourcePosition[1],Map)
        unit.moveUnit(direction)
	
    return None		
    

