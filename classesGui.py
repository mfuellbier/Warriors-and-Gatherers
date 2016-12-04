#!/usr/bin/python
# -*- coding: utf-8 -*-

class Harddata:
    
    def __init__(self, round, playerNames,Map,Base):
        self.round = round
        self.playerNames = playerNames
        self.Map = Map
        self.Base = Base

class Data:

    def __init__(self, round, playerNames, resources, map, units):
        self.round = round	# Zahl
        self.playerNames = playerNames	# []
        self.resources = resources
        self.map = map	# String[][]
        self.units = units  # [unitsPlayer1,unitsPlayer2,unitsPlayer3,unitsPlayer4]
                            #  unitsPlayerx = [unitsOnMap,hiddenUnits]
        '''
        'LAND' = Land
        'RESOURCE' = Resource
        '1WARRIOR' = Warrior of Player1
        '1GATHERER' = Gatherer of Player1
        '1BASE' = Base of Player1
        'WALL' = Wall
        'WATER' = Water
        '''
    
    def getRound(self):
        return self.round
        
    def getMap(self):
        return self.map
        
    def getPlayerNames(self):
        return self.playerNames
        
    def getResource(self,player):
        k = 0
        for name in self.playerNames:
            if name == player:
                return self.resources[k]
            k += 1
            
    def getUnits(self,player):
        k = 0
        for name in self.playerNames:
            if name == player:
                return self.units[k]
            k += 1

class GameStats:

    def __init__(self, challenge, counterDictionary, backyard, central, circle, garden, labyrinth, newbie, source, tight_corridors, Noob, NoobFunctions, Intermediate, IntermediateFunctions, Advanced, AdvancedFunctions, Expert, ExpertFunctions, challengeNoob, challengeIntermediate, challengeAdvanced, challengeExpert):
    
        self.challenge = challenge # 'Noob','Intermediate','Advanced','Expert' or None
        self.counterDictionary = counterDictionary
        
        # rewardMaps
        self.backyard = backyard
        self.central = central
        self.circle = circle
        self.garden = garden
        self.newbie = newbie
        self.source = source
        self.tight_corridors = tight_corridors
        
        # Noob, Intermediate, Advanced and Expert (+ Functions) are source codes of the AIs
        self.Noob = Noob
        self.NoobFunctions = NoobFunctions
        self.Intermediate = Intermediate
        self.IntermediateFunctions = IntermediateFunctions
        self.Advanced = Advanced
        self.AdvancedFunctions = AdvancedFunctions
        self.Expert = Expert
        self.ExpertFuntions = ExpertFunctions
        
        # Challenges: (rounds,map)
        self.challengeNoob = challengeNoob
        self.challengeIntermediate = challengeIntermediate
        self.challengeAdvanced = challengeAdvanced
        self.challengeExpert = challengeExpert
    
    def setCounter(self,challenge,number):
        self.counterDictionary[challenge] = number
        return None
        
    def getCounter(self,challenge):
        return self.counterDictionary[challenge]
    
    def getRewardMap(self,string):
        if string == 'backyard':
            return self.backyard
        elif string == 'central':
            return self.central
        elif string == 'circle':
            return self.circle
        elif string == 'garden':
            return self.garden
        elif string == 'labyrinth':
            return self.labyrinth
        elif string == 'newbie':
            return self.newbie
        elif string == 'source':
            return self.source
        elif string == 'tight_corridors':
            return self.tight_corridors
        else:
            return None
    
    def setbackyard(self,Map):
        self.backyard = Map
        return None
    
    def setcentral(self,Map):
        self.central = Map
        return None
        
    def setcircle(self,Map):
        self.circle = Map
        return None
        
    def setgarden(self,Map):
        self.garden = Map
        return None
        
    def setlabyrinth(self,Map):
        self.labyrinth = Map
        return None
        
    def setnewbie(self,Map):
        self.newbie = Map
        return None
        
    def setsource(self,Map):
        self.backyard = Map
        return None
        
    def setsource(self,Map):
        self.backyard = Map
        return None
        
    def settight_corridors(self,Map):
        self.tight_corridors = Map
        return None
    
    def setChallenge(self,challenge):
        self.challenge = challenge
        return None
    
    def setNoob(self,string):
        self.Noob = string
        return None
    
    def setNoobFunctions(self,string):
        self.NoobFunctions = string
        return None
        
    def setIntermediate(self,string):
        self.Intermediate = string
        return None
    
    def setIntermediateFunctions(self,string):
        self.IntermediateFunctions = string
        return None
        
    def setAdvanced(self,string):
        self.Advanced = string
        return None
    
    def setAdvancedFunctions(self,string):
        self.AdvancedFunctions = string
        return None
        
    def setExpert(self,string):
        self.Expert = string
        return None
    
    def setExpertFunctions(self,string):
        self.ExpertFunctions = string
        return None
    
    def setChallengeNoob(self,rounds,Map,matches):
        self.challengeNoob = [rounds,Map,matches]
        return None
        
    def setChallengeIntermediate(self,rounds,Map,matches):
        self.challengeIntermediate = [rounds,Map,matches]
        return None
    
    def setChallengeAdvanced(self,rounds,Map,matches):
        self.challengeAdvanced = [rounds,Map,matches]
        return None
    
    def setChallengeExpert(self,rounds,Map,matches):
        self.challengeExpert = [rounds,Map,matches]
        return None
    
    def getChallenge(self):
        return self.challenge
    
    def getCodeAi(self,string):
        if string == 'Noob':
            return self.Noob
        elif string == 'Intermediate':
            return self.Intermediate
        elif string == 'Advanced':
            return self.Advanced
        elif string == 'Expert':
            return self.Expert
        else:
            return None
    
    def getCodeFunctions(self,string):
        if string == 'Noob':
            return self.NoobFunctions
        elif string == 'Intermediate':
            return self.IntermediateFunctions
        elif string == 'Advanced':
            return self.AdvancedFunctions
        elif string == 'Expert':
            return self.ExpertFunctions
        else:
            return None
    
    def updateChallenge(self):
        self.counter = 0
        if self.challenge == 'Noob':
            self.setChallenge('Intermediate')
        elif self.challenge == 'Intermediate':
            self.setChallenge('Advanced')
        elif self.challenge == 'Advanced':
            self.setChallenge('Expert')
        #elif self.challenge == 'Expert':
        #    self.setChallenge(None)
        else:
            return None
        return None
    def getRounds(self,challenge):
        if challenge == 'Noob':
            return self.challengeNoob[0]
        elif challenge == 'Intermediate':
            return self.challengeIntermediate[0]
        elif challenge == 'Advanced':
            return self.challengeAdvanced[0]
        elif challenge == 'Expert':
            return self.challengeExpert[0]
        else:
            return None
            
    def getMap(self,challenge):
        if challenge == 'Noob':
            return self.challengeNoob[1]
        elif challenge == 'Intermediate':
            return self.challengeIntermediate[1]
        elif challenge == 'Advanced':
            return self.challengeAdvanced[1]
        elif challenge == 'Expert':
            return self.challengeExpert[1]
        else:
            return None
            
    def getMatches(self,challenge):
        if challenge == 'Noob':
            return self.challengeNoob[2]
        elif challenge == 'Intermediate':
            return self.challengeIntermediate[2]
        elif challenge == 'Advanced':
            return self.challengeAdvanced[2]
        elif challenge == 'Expert':
            return self.challengeExpert[2]
        else:
            return None
    
    def getCurrentMatches(self):
        return self.getMatches(self.getChallenge())
    
    def getCurrentRounds(self):
        return self.getRounds(self.getChallenge())
        
    def getCurrentMap(self):
        return self.getMap(self.getChallenge())
        
    def getCurrentCounter(self):
        return self.getCounter(self.getChallenge())
    
    def updateCounter(self,challenge):
        self.counterDictionary[challenge] += 1
        return None
