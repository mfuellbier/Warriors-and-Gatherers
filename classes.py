#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import add

class AlreadyMovedError(Exception): pass

class CreatingUnitError(Exception): pass

class WrongDirectionError(Exception): pass

class UnitType:
    WARRIOR = 'WARRIOR'
    GATHERER = 'GATHERER'
    
    def __init__(self, maxResource, strength, cost, unitTypesStrings):
        self.maxResource = maxResource
        self.strength = strength
        self.cost = cost
        self.unitTypesStrings = unitTypesStrings
    
    def __str__(self):
        return self.unitTypesStrings[self.maxResource]
    
    def getMaxResources(self):
        return self.maxResource
        
    def getStrength(self):
        return self.strength
        
    def getCost(self):
        return self.cost
    
    def getString(self):
        return self.unitTypesStrings[self.maxResource]
    
class FieldType:
	WATER = 'WATER'
	WALL = 'WALL'
	LAND = 'LAND'
	RESOURCE = 'RESOURCE'
	BASE = 'BASE'
    
class Direction:
	NORTH= 'NORTH'
	SOUTH = 'SOUTH'
	WEST = 'WEST'
	EAST = 'EAST'
	STAY = 'STAY'

class Unit:

    def __init__(self, unitId, unitType, owner, resources, position, moved, lastMove):
        self.unitId = unitId		# int
        self.unitType = unitType	# GATHERER / WARRIOR
        self.owner = owner			# Name of Owner
        self.resources = resources	# int
        self.position = position	# [int,int]
        self.moved = moved 			# True / False
        self.lastMove = lastMove    # Direction
    
    def getUnitId(self):
        return self.unitId
		
    def getUnitType(self):
        return self.unitType
		
    def getOwner(self):
        return self.owner
		
    def getResources(self):
        return self.resources
    
    def getPosition(self):
        return self.position
		
    def moveUnit(self, direction):
        try:
            if self.moved:
                raise AlreadyMovedError
            if direction == Direction.EAST:
                self.position[0]+=1
            elif direction == Direction.WEST:
                self.position[0]-=1
            elif direction == Direction.NORTH:
                self.position[1]-=1
            elif direction == Direction.SOUTH:
                self.position[1]+=1
            elif direction != Direction.STAY:
                raise WrongDirectionError
            self.moved = True
            self.lastMove = direction
            return
        except AlreadyMovedError:
            print("Unit can't move more than once a round!")
            return False
        except WrongDirectionError:
            print('Wrong Direction!')
            return False

    def getLastMove(self):
        return self.lastMove
    
    def moveUnitBack(self):
        self.moved = False
        if self.lastMove == Direction.SOUTH:
            direction = Direction.NORTH
        elif self.lastMove == Direction.NORTH:
            direction = Direction.SOUTH
        elif self.lastMove == Direction.EAST:
            direction = Direction.WEST
        elif self.lastMove == Direction.WEST:
            direction = Direction.EAST
        elif self.lastMove == Direction.STAY:
            direction = Direction.STAY
        self.moveUnit(direction)
        

class Base:

    def __init__(self, resources, position, units, owner, gameConfiguration,unitTypes):
        self.resources = resources	# int
        self.position = position	# [int,int]
        self.units = units	# Unit[]
        self.owner = owner
        self.gameConfiguration = gameConfiguration
        self.unitTypes = unitTypes
        self.unitId = 0

    def getResources(self):
        return self.resources

    def getHiddenUnits(self):
        hiddenUnits = []
        for unit in self.units:
            if unit.position == self.position:
                hiddenUnits.append(unit)
        return hiddenUnits
    
    def getUnits(self):
        return self.units
    
    def getPosition(self):
        return self.position
		
    def getOwner(self):
        return self.owner
		
    def createUnitWarrior(self):
        try:
            costWarrior = self.gameConfiguration.getUnitCostWarrior()
            if costWarrior > self.resources:
                raise CreatingUnitError
            else:
                self.resources=self.resources-costWarrior
                self.units.append(Unit(self.unitId,self.unitTypes['WARRIOR'],self.owner,0,[self.position[0],self.position[1]],False,Direction.STAY))	# In this place you need "[self.position[0],self.position[1]]" instead of "self.position", because variables of type "list" are mutable unlike variables of type "int", which are immutable.
                self.unitId += 1
            return																		            									# There would be be a problem in moving the units. In this case you wouldn't only change the position of one unit, but all the positions of all units and the base. All of the "variables" are pointing to the same value. see Pass by reference!
        except CreatingUnitError:
            print('Not enough resources for warrior!')
            return False
        
    def createUnitGatherer(self):
        try:
            costGatherer = self.gameConfiguration.getUnitCostGatherer()
            if costGatherer > self.resources:
                raise CreatingUnitError
            else:
                self.resources=self.resources-costGatherer
                self.units.append(Unit(self.unitId,self.unitTypes['GATHERER'],self.owner,0,[self.position[0],self.position[1]],False,Direction.STAY))
                self.unitId += 1
            return None
        except CreatingUnitError:
            print('Not enough resources for gatherer!')
            return False
	
class Field:

    def __init__(self, position, fieldType, unit, resources, base):
        self.position = position	# [int,int]
        self.fieldType = fieldType	# FieldType
        self.unit = unit			# Unit[] / Unit / None
        self.resources = resources	# int
        self.base = base			# None if fieldType != BASE

    def getFieldType(self):
        return self.fieldType
    
    def getPosition(self):
        return self.position
		
    def getUnitOnField(self):
        if self.fieldType == FieldType.BASE:
            return self.base.getHiddenUnits()
        return self.unit		# 0 if no unit on field, Unit[] if field = base
		
    def getResources(self):
        return self.resources
    
    def getResourcesOnField(self):
        return self.resources
	
    def getBase(self):
        return self.base
    	
    def isCrossable(self,unit):
        # if field is base
        if self.fieldType == FieldType.BASE:
            if unit.getOwner() != self.base.getOwner():
                return False    # field is not own base
            else:
                return True # field is own base
        
        #if field is WALL or WATER
        if self.fieldType == FieldType.WALL or self.fieldType == FieldType.WATER:
            return False
                
        # Check if the field (which is of Type LAND or RESOURCE) is occupied by own unit
        if self.unit == None:
            return True
        elif self.unit.getOwner() != unit.getOwner():
            return True
        else:
            if self.unit.getUnitId() == unit.getUnitId():
                return True
            else:
                return False
        
    def isReachable(self,unit):
        # Check, if field is reachable by allowed move (NORTH, EAST, SOUTH, WEST, STAY)
        if (abs(unit.getPosition()[0]-self.position[0]) == 1 and unit.getPosition()[1]-self.position[1] == 0) or (abs(unit.getPosition()[1]-self.position[1]) == 1 and unit.getPosition()[0]-self.position[0] == 0) or (unit.getPosition() == self.position):
            return True
        else:
            return False
                
    def gatherResource(self):
        if self.unit == None:
            return 1
        unit = self.unit
        if self.resources == 0 or unit.getUnitType().getMaxResources() == unit.getResources():
            # No resources or unit is full
            return None
        elif unit.getResources() + self.resources < unit.getUnitType().getMaxResources():
            # all resources can be picked up
            unit.resources+=self.resources
            self.resources = 0
        else:
            # resources on field, but unit can't pick up all of them
            self.resources = self.resources - unit.getUnitType().getMaxResources() + unit.getResources()
            unit.resources = unit.getUnitType().getMaxResources()
        return None
		
class GameConfiguration:

	def __init__(self, unitCostWarrior, unitCostGatherer, unitStrengthWarrior, unitStrengthGatherer, unitMaxResourcesWarrior, unitMaxResourcesGatherer,rounds):
		self.unitCostWarrior = unitCostWarrior
		self.unitCostGatherer = unitCostGatherer
		self.unitStrengthWarrior = unitStrengthWarrior
		self.unitStrengthGatherer = unitStrengthGatherer
		self.unitMaxResourcesWarrior = unitMaxResourcesWarrior
		self.unitMaxResourcesGatherer = unitMaxResourcesGatherer
		self.rounds = rounds;
	
	def getUnitCostWarrior(self):
		return self.unitCostWarrior
		
	def getUnitCostGatherer(self):
		return self.unitCostGatherer
		
	def getUnitStrengthWarrior(self):
		return self.unitStrengthWarrior
		
	def getUnitStrengthGatherer(self):
		return self.unitStrengthGatherer
		
	def getUnitMaxResourcesWarrior(self):
		return self.unitMaxResourcesWarrior
		
	def getUnitMaxResourcesGatherer(self):
		return self.unitMaxResourcesGatherer
		
	def getRounds(self):
		return self.rounds

class RoundState:

    def __init__(self, base, map, roundNumber):
        self.base = base	# Base
        self.map = map		# Field[][]
        self.unitList = self.base.units	# Unit[]
        self.roundNumber = roundNumber	# int
		
    def getBase(self):
        return self.base
        
    def getOwnBase(self):
        return self.base
	
    def getMap(self):
        return self.map
	
    def getUnits(self):
        return self.unitList
    	
    def getOwnUnits(self):
        return self.unitList
		
    def getRoundNumber(self):
        return self.roundNumber
        
    def getOwnName(self):
        return self.base.getOwner()
        
    def getOwnResources(self):
        return self.base.getResources()
