#!/usr/bin/python
# -*- coding: utf-8 -*-

# NoobFunctions.py
#####################################################################
#### Don't touch this! Otherwise this client will not be executed ###
#####################################################################
from classes import *                   						  ###
																  ###
#####################################################################
##### Remember Pythons off-side-rule! Use 4-space indentation! ######
#####################################################################

# In this file you can define functions and classes, which can be called in your BattleClient


# A very rudimentary pathfinding-algorithm. Don't hesitate to improve it or build a new one!
def getDirectionForMoveToField(unit,toX,toY,Map):
    # input: Unit unit, int toX, int toY
    # output: Direction, to which unit is going to move to reach Map[X][Y]
    currentX = unit.getPosition()[0]
    currentY = unit.getPosition()[1]
    diffX = toX - currentX
    diffY = toY - currentY
    lastMoveDirection = unit.getLastMove()
   # if(lastMoveDirection == 0):
   #      lastMoveDirection = Direction.STAY;

    newDirection = Direction.STAY;
    if (diffY != 0 and lastMoveDirection != Direction.NORTH and lastMoveDirection != Direction.SOUTH):
        if (diffY > 0):
            newDirection = Direction.SOUTH
        else:
            newDirection = Direction.NORTH
    elif (diffX != 0):
        if (diffX > 0):
            newDirection = Direction.EAST
        else:
            newDirection = Direction.WEST
    elif (diffY != 0 and lastMoveDirection == Direction.NORTH):
        newDirection = Direction.NORTH
    elif (diffY != 0 and lastMoveDirection == Direction.SOUTH):
        newDirection = Direction.SOUTH
    return checkDirection(unit,currentX,currentY,newDirection,Map)

def checkDirection(unit,oldX,oldY,direction,Map):
    impossibleToMove = True
    unsuccessfulTry = 0

    while impossibleToMove and unsuccessfulTry < 5:
        if direction == Direction.NORTH:
            newY = oldY - 1
            newX = oldX
            if Map[newX][newY].isReachable(unit) and Map[newX][newY].isCrossable(unit):                
                impossibleToMove = False
            else:
                impossibleToMove = True
                unsuccessfulTry += 1
                direction = Direction.EAST
        if direction == Direction.WEST:
            newX = oldX - 1
            newY = oldY
            if Map[newX][newY].isReachable(unit) and Map[newX][newY].isCrossable(unit):
                impossibleToMove = False
            else:
                impossibleToMove = True
                unsuccessfulTry += 1
                direction = Direction.NORTH
        if direction == Direction.SOUTH:
            newY = oldY + 1;
            newX = oldX;
            if Map[newX][newY].isReachable(unit) and Map[newX][newY].isCrossable(unit):
                impossibleToMove = False
            else:
                impossibleToMove = True
                unsuccessfulTry += 1
                direction = Direction.WEST
        if direction == Direction.EAST:
            newX = oldX + 1;
            newY = oldY;
            if Map[newX][newY].isReachable(unit) and Map[newX][newY].isCrossable(unit):
                impossibleToMove = False
            else:
                impossibleToMove = True
                unsuccessfulTry += 1
                direction = Direction.SOUTH
        if direction == Direction.STAY:
            newX = oldX
            newY = oldY
            impossibleToMove = False

    if unsuccessfulTry >= 4:
        direction = Direction.STAY

    return direction

	

