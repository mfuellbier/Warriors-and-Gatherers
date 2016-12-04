#!/usr/bin/python
# -*- coding: utf-8 -*-

from classes import *
from functions import *
import sys
import time
import datetime
import run
import os

# sys.argv[1] = number of rounds
# sys.argv[2] = mapName
# sys.argv[3] = number of games

############### Variables #########################

Rounds = int(sys.argv[1])
Map = sys.argv[2]
numberOfGames = int(sys.argv[3])

AIlist = ["AI2.py","AI2.py","AI2.py","AI2.py"]

multiplicatorOfBreak = 1
timeBetweenGames = 15

###################################################

for AIlist in [["AI2.py","AI2.py","AI2.py","AI2.py"],["Intermediate.py","Intermediate.py","Intermediate.py","Intermediate.py"]]:
    overallWinnerList = []
    listOfResources = []
    listOfDurations = []
    playerNames = checkForMultipleNames([AIlist[k][:-3] for k in range(4)])
    save_stdout = sys.stdout
    print('Compute',numberOfGames,'games.')
    for k in range(numberOfGames):
        start_time = time.time()
        sys.stdout = open(os.devnull, 'w')
        game = run.Run(AIlist,Map,Rounds)[1]
        sys.stdout = save_stdout
        
        duration = time.time() - start_time
        print('Game',k+1,'took',round(duration,4),'seconds')
        overallWinnerList.append(game[1])
        listOfResources.append(game[0])
        listOfDurations.append(duration)
        if k < numberOfGames:#-1:
            # Break between games
            #time.sleep(multiplicatorOfBreak*duration) 
            time.sleep(multiplicatorOfBreak*timeBetweenGames)   
        

    timesPlayerWon = [0,0,0,0] # [20,40,40,20] means Player 1 won 20 times, player 2 40 times and so on

    for game in overallWinnerList:
        for winner in game:
            for k in range(4):
                if winner == playerNames[k]:
                    timesPlayerWon[k] += 1

    #Statistics for maxRes
    listOfResources.sort()
    listOfDurations.sort()
    
    sys.stdout = open('statistics.log','a')
    print('Times players won ',playerNames,':',timesPlayerWon)
    print('Each game went for',str(Rounds),'Rounds.')
    print('Maximal resources of winner:',max(listOfResources))
    print('Minimal resources of winner:',min(listOfResources))
    print('Arithmetic mean of resources of winner:',sum(listOfResources)/len(listOfResources))
    if numberOfGames%2 == 0:
        # numberOfGames even
        median = (listOfResources[int(numberOfGames/2)-1]+listOfResources[int(numberOfGames/2)])/2
    else:
        median = listOfResources[int((numberOfGames-1)/2)]
    print('Median of resources of winner:',median)
    print('Maximal duration:',round(max(listOfDurations),4))
    print('Minimal duration:',round(min(listOfDurations),4))
    print('Arithmetic mean of duration:',round(sum(listOfDurations)/len(listOfDurations),4))
    if numberOfGames%2 == 0:
        # numberOfGames even
        median = round((listOfDurations[int(numberOfGames/2)-1]+listOfDurations[int(numberOfGames/2)])/2,4)
    else:
        median = round(listOfDurations[int((numberOfGames-1)/2)],4)
    print('Median of duration:',median)
    print("\n")
    sys.stdout=save_stdout
