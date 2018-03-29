#!/usr/bin/python
# -*- coding: utf-8 -*-

# How to compile:
#
# 1. execute createGameDat.py
# 2. ~/bin/compileWag

# TODO: field.getUnitOnField() nur Kopie => Ja! Units auf der Karte können nicht bewegt werden! Das selbe für Basis => In Dokumentation!

from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from classes import *
from classesGui import *
from copy import *
from functions import *
from tkinter import messagebox
import pickle
import platform, sys, shutil
import time, datetime, random
import Noob, Intermediate, Advanced, Expert, Dummy
import traceback

# Program Version
version = 1.2

# Default game-title
gameTitle = 'Warriors & Gatherers'

# Load the game, incl. challenges and rewards
try:
    gameStats = pickle.load(open('game.dat','rb'))
except OSError:
    messagebox.showerror('Error!','Could not find "game.dat"!')
    sys.exit()
except EOFError:
    messagebox.showerror('Error!','The file "game.dat" is corrupted!')
    sys.exit()
class Player():
    
    def __init__(self,gameData,ranAgain,gameTitle,lastRounds,lastAIs,lastMap,lastSpeeder):
        
        self.gameData = gameData
        self.ranAgain = ranAgain
        self.gameTitle = gameTitle
        self.lastRounds = lastRounds
        self.lastAIs = lastAIs
        self.lastMap = lastMap
        self.lastSpeeder = lastSpeeder
    
        self.roundOfCurrentGame = lastRounds
        self.noGameRan = True
        
        self.updateBoardForce = False   # Needed for searching with scale
        
        # Game Settings
        self.startResource = 200
        self.resourceOnField = 100
        self.probabilityForResourceOnField = 0.025  # For probability distribution see functions.computeProbabilityForResourceOnField()
        self.unitMaxResourcesWarrior = 30
        self.unitStrengthWarrior = 0.75             # For probability distribution see functions.fight()
        self.unitCostWarrior = 60
        self.unitMaxResourcesGatherer = 100
        self.unitStrengthGatherer = 0.5
        self.unitCostGatherer = 50
        
        # Window
        self.root = Tk()
        self.root.focus_set()
        self.root.title(self.gameTitle)
        self.root.geometry('268x328')       
        
        self.frameSettingsAndProgressbar = Frame(self.root, width=400, height=600)
        self.frameSettingsAndProgressbar.grid(row=0, column=1)
        
        self.frameSettings = Frame(self.frameSettingsAndProgressbar, width=400, height=600)
        self.frameSettings.grid(row=0, column=0)
        
        self.frameRadiobuttons = Frame(self.frameSettingsAndProgressbar, width=400, height=600)
        self.frameRadiobuttons.grid(padx = 10, row=1, column=0,sticky = (W))
        
        self.frameRunLoad = Frame(self.frameSettingsAndProgressbar, width=400, height=600)
        self.frameRunLoad.grid(padx = 10, row=2, column=0,sticky = (W))
        
        self.frameProgressbar = Frame(self.frameSettingsAndProgressbar, width=400, height=600)
        self.frameProgressbar.grid(row=3, column=0)
        
        self.frameVersion = Frame(self.frameProgressbar, width=400, height=600)
        self.frameVersion.grid(row=1, column=0)
        
        # Settings (Rounds, Map, AI)
         
        # Rounds
        Label(self.frameSettings, text='Rounds').grid(row = 0, column = 0)
        self.rounds = IntVar()
        self.spinbox = Spinbox(self.frameSettings,values=[x*100 for x in range(1,11)], width = 5, textvariable = self.rounds)
        self.spinbox.grid(row = 0, column = 1)
        self.rounds.set(self.lastRounds)
        Label(self.frameSettings, text='Up/Down').grid(row = 0, column = 2)
        
        # Map
        Label(self.frameSettings, text='Map').grid(row = 1, column = 0)
        self.MapName = StringVar()
        self.mapEntry = Entry(self.frameSettings, width = 15, textvariable = self.MapName)
        self.mapEntry.grid(row = 1, column = 1)
        self.MapName.set(self.lastMap)
        Button(self.frameSettings, text='Open file', command=self.chooseMap).grid(row = 1, column = 2)
        
        # AI
        for k in range(4):
            exec("Label(self.frameSettings, text='AI "+str(k+1)+"').grid(row = "+str(k+2)+", column = 0)")
            exec("self.Ai"+str(k+1)+" = StringVar()")
            exec("self.mapEntry = Entry(self.frameSettings, width = 15, textvariable = self.Ai"+str(k+1)+")")
            exec("self.mapEntry.grid(row = "+str(k+2)+", column = 1)")
            exec("self.Ai"+str(k+1)+".set(self.lastAIs["+str(k)+"])") 
        Button(self.frameSettings, text='Open file', command= lambda: self.chooseAi(1)).grid(row = 2, column = 2) # lambda seems not to work in for-loop
        Button(self.frameSettings, text='Open file', command= lambda: self.chooseAi(2)).grid(row = 3, column = 2)
        Button(self.frameSettings, text='Open file', command= lambda: self.chooseAi(3)).grid(row = 4, column = 2)
        Button(self.frameSettings, text='Open file', command= lambda: self.chooseAi(4)).grid(row = 5, column = 2)
        
        self.root.bind('<KeyPress-Return>', self.executeKey)
        self.root.bind('<KeyPress-Up>', self.roundsUp)
        self.root.bind('<KeyPress-Down>', self.roundsDown)
        
        # Run/Load Button
        self.buttonExecute = Button(self.frameRunLoad, text="Run", command = self.execute).grid(row = 0, column = 0,sticky = (W))
        self.buttonLoad = Button(self.frameRunLoad, text="Load game", command=self.load).grid(row = 0, column = 1,sticky = (W))
        Label(self.frameRunLoad, text="Return").grid(row = 0, column = 2)
        
        # Radiobuttons
        self.radioButtonVar = StringVar()

        challengesList = ['Noob','Intermediate','Advanced','Expert']
        n = 0
        k = 4
        for challenge in challengesList:
            if gameStats.getChallenge() in challengesList[::-1][:k]:
                Radiobutton(self.frameRadiobuttons, 
                    text=challenge+' - '+str(gameStats.getCounter(challenge))+' of '+str(gameStats.getMatches(challenge)),
                    variable=self.radioButtonVar, 
                    value=challenge).grid(row=n,column = 0,sticky = (W))
            else:
                Radiobutton(self.frameRadiobuttons, 
                    text=challenge,
                    state=DISABLED,
                    variable=self.radioButtonVar, 
                    value=challenge).grid(row=n,column = 0,sticky = (W))
            n+=1
            k-=1
        Radiobutton(self.frameRadiobuttons, 
                    text='Custom',
                    variable=self.radioButtonVar, 
                    value='Custom').grid(row=4,column = 0,sticky = (W))
        
        radioPick = self.initializeRadiobuttons(gameStats,self.rounds.get(),self.MapName.get(),[self.Ai1.get(),self.Ai2.get(),self.Ai3.get(),self.Ai4.get()])
        self.radioButtonVar.set(radioPick)
        self.saveButton = self.radioButtonVar.get()
        self.saveRounds = self.rounds.get()
        self.saveMap = self.MapName.get()
        self.saveAi1 = self.Ai1.get()
        self.saveAi2 = self.Ai2.get()
        self.saveAi3 = self.Ai3.get()
        self.saveAi4 = self.Ai4.get()
        
        # ProgressBar
        self.progressbar = ttk.Progressbar(self.frameProgressbar, length=250, mode='determinate')
        self.progressbar.grid(row=0, column=0, padx = 10)       
        
        # Version
        Label(self.frameVersion, text = 'Version '+str(version)).grid(row = 0, column = 1)
        
        # set Rounds, Map, Ai in dependance of radiobuttons
        if self.radioButtonVar.get() != 'Custom':
            self.rounds.set(gameStats.getRounds(self.radioButtonVar.get()))
            self.MapName.set(gameStats.getMap(self.radioButtonVar.get()))
            self.Ai1.set('yourAI')
            for k in range(1,4):
                exec("self.Ai"+str(k+1)+".set(self.radioButtonVar.get())") 
        
        self.speed = IntVar()
        self.field = []
        
        self.backward = False
        self.gameLoaded = False
        self.paused = True
        self.finished = False
      
        self.round = StringVar()
        self.resourcePlayer = []
        self.unitsPlayer = []
        self.HiddenUnitsPlayer = []
        self.unitsOnMapPlayer = []
               
        if self.gameData != None:
            self.gui(self.gameData)
        else:
            self.idle()
        
        self.root.mainloop()

    def save(self):
        self.paused = True
        try:
            if platform.system() == 'Windows':
                game = filedialog.asksaveasfilename(initialdir = "./saves",title = "choose your file",filetypes = (("all files","*.*"),("p files","*.p")))
            else:
                game = filedialog.asksaveasfilename(initialdir = "./saves",title = "choose your file",filetypes = (("p files","*.p"),("all files","*.*")))
            self.root.title('Warriors & Gatherers - '+shortString(game))
            # Copy logs
            for string in self.playerNames:
                shutil.copyfile(string+'.log',game[:-2]+'_'+string+'.log')
            pickle.dump(self.data, open(game, "wb" ) )
        except:
            return None

    def load(self):
        self.paused = True
        if not self.ranAgain:
            messagebox.showwarning('Warning', 'Not saved data will be lost.')
        try:
            if platform.system() == 'Windows':
                game = filedialog.askopenfilename(initialdir = "./saves",title = "choose your file",filetypes = (("all files","*.*"),("p files","*.p")))
            else:
                game = filedialog.askopenfilename(initialdir = "./saves",title = "choose your file",filetypes = (("p files","*.p"),("all files","*.*")))
            self.gameTitle = 'Warriors & Gatherers - '+shortString(game)
            self.root.title(self.gameTitle)
            self.gameData = pickle.load(open(game,"rb"))
        
            self.ranAgain = True 
            self.noGameRan = False
            self.root.destroy()
        except:
            print("hier")
            return None
        
    def executeKey(self,event):
        self.execute()

    def execute(self):
        self.paused = True
        
        if self.rounds.get() > 1000 or self.rounds.get() < 1:
            messagebox.showwarning('Error!','"Rounds" must be between 1 and 1000!')
            return None
            
        if not self.ranAgain:
            if not messagebox.askyesno('Verify', 'Not saved data will be lost.\nDo you want to run a new game?'):
                return None
                            
        Ai = [self.Ai1.get(),self.Ai2.get(),self.Ai3.get(),self.Ai4.get()]
        listAI = [None]*4
        for k in range(4):
            listAI[k] = shortString(Ai[k])
                    
        mapName = self.MapName.get()
        
        
        # import AIs
        try:
            for k in range(4):
                exec('import '+str(listAI[k]))
        except ImportError:
            messagebox.showerror('Error!','File not found!\n'+str(sys.exc_info()[1])+'.')
            #self.root.destroy()
            return None
        except Exception:
            sys.stdout = open(str(self.playerNames[k])+'.log','a')
            formatted_lines = traceback.format_exc().splitlines()
            print(formatted_lines[-4])
            print(formatted_lines[-3])
            print(formatted_lines[-2])
            print(formatted_lines[-1])
            print()
            messagebox.showerror('Error!','An Error occured! Check '+self.playerNames[k]+'.log!')
            sys.stdout = save_stdout
            #self.root.destroy()
            return None

        # check for not activated challenges
        if AiIsNotActivatedYet(gameStats,[listAI[k] for k in range(4)]):
            messagebox.showerror('Error!','Challenge is not activated yet!')
            #self.root.destroy()
            return None
        
        try:
            for ai in listAI:
                if ai != 'Noob' and ai != 'Intermediate' and ai != 'Advanced' and ai != 'Expert' and False:
                    if UserImportedAi(ai):
                        messagebox.showerror('Cheater!','You imported an preprogrammed Ai. Do it yourself!')
                        #self.root.destroy()
                        return None
        except OSError:
            messagebox.showerror('Error!',str(sys.exc_info()[1])[10:]+'.')
            #self.root.destroy()
            return None
        (self.gameData , winnerStats) = self.Run(listAI,mapName,self.rounds.get())  # Running the game
        self.gameTitle = 'Warriors & Gatherers'
        self.ranAgain = True
        self.noGameRan = False

        
       # After running check for challenge:
        winner = winnerStats[1]
        if challengeMatchWon(winner,gameStats,findChallenge(gameStats,listAI,self.rounds.get(),mapName)):
            # update ChallengeCounter
            gameStats.updateCounter(gameStats.getChallenge())
            if gameStats.getCurrentMatches()-gameStats.getCurrentCounter() == 1:
                messagebox.showinfo('Congratulations!','You won!\n'+str(gameStats.getCurrentMatches()-gameStats.getCurrentCounter())+' match left.')
            elif gameStats.getCurrentMatches()-gameStats.getCurrentCounter() > 1:
                messagebox.showinfo('Congratulations!','You won!\n'+str(gameStats.getCurrentMatches()-gameStats.getCurrentCounter())+' matches left.')
            
        if challengeDone(winner,gameStats,findChallenge(gameStats,listAI,self.rounds.get(),mapName)):
            if gameStats.getChallenge() == 'Expert':
                messagebox.showinfo('Congratulations!','Wow! You mastered the challenge "'+gameStats.getChallenge()+'"!\nYou truly are a rockstar programmer!')
            else:
                messagebox.showinfo('Congratulations!','You mastered the challenge "'+gameStats.getChallenge()+'"!\nThe next challenge is available.\nYour reward is in the programs direction. Also check out the new Maps!')
            reward(gameStats)
            self.radioButtonVar.set(gameStats.getChallenge())
        
        self.root.destroy()

# Actual process of computing a game      
    def Run(self,listAI,mapNameLong,rounds):

        startTimeGame = time.time()
        
        mapName = shortString(mapNameLong)+'.map'
        
        pathToMap = 'maps/'+mapName

        # Check if some Names are the same
        self.playerNames = checkForMultipleNames(checkForMultipleNames([listAI[k] for k in range(4)]))
        
        self.unitTypesStrings = { self.unitMaxResourcesGatherer : 'GATHERER' , self.unitMaxResourcesWarrior : 'WARRIOR'}
        self.unitTypes = {'WARRIOR' : UnitType(self.unitMaxResourcesWarrior,self.unitStrengthWarrior,self.unitCostWarrior,self.unitTypesStrings) , 'GATHERER' : UnitType(self.unitMaxResourcesGatherer,self.unitStrengthGatherer,self.unitCostGatherer,self.unitTypesStrings)}

        # Gathering Informations for very first round
        self.gameConfiguration = GameConfiguration(self.unitCostWarrior,self.unitCostGatherer,self.unitStrengthWarrior,self.unitStrengthGatherer,self.unitMaxResourcesWarrior,self.unitMaxResourcesGatherer,rounds)
        
        try:
            (Map,Base) = createMapBeginning(pathToMap,self.startResource,self.resourceOnField,self.gameConfiguration,self.unitTypes,deepcopy(self.playerNames),self.probabilityForResourceOnField)
        except IndexError:
            messagebox.showerror('Error!',self.MapName.get()+' is not a valid map!')
            return [None,[0,[]]]
        except OSError:
            k=0
            char = str(sys.exc_info()[1])[k]
            while char != '/':
                k+=1
                char = str(sys.exc_info()[1])[k]
            # char = "/"
            nameFail = str(sys.exc_info()[1])[k+1:-1]
            messagebox.showerror('Error!','Map not found!\n"'+nameFail+'" is not in direction "maps".')
            return [None,[0,[]]]

        # Open new log
        self.userLog = [None,None,None,None]
        for k in range(4):
            self.userLog[k] = open(str(self.playerNames[k])+'.log','w')

        # game process; Returns data,Base,Map
        gameData = self.gameProcess(rounds,Base,Map,listAI)

        # Play
        print('The game took',round(time.time() - startTimeGame,4),'seconds.')
        
        [maxRes,winnerList] = findWinner(Base,self.playerNames) #is needed for statistics
        
        return [gameData,[maxRes,winnerList]]

    def gameProcess(self,rounds,Base,Map,listAI):
        
        # set dummys resources to 0:
        for k in range(4):
            if listAI[k] == 'Dummy':
                Base[k].resources = 0
        
        # data-list to save the game
        gameData = []
        playerNamesDeepCopy = deepcopy(self.playerNames)    # Needed for Data, so that Player can't manipulate the names
        gameData.append(prepareDataForPlayer(0,playerNamesDeepCopy,Map,Base))
        
        self.progressbar.start()
        for Round in range(1,rounds+1):
            
            # running the round
            (Map,Base,ErrorOccured) = self.roundProcess(Base,Map,Round,listAI,playerNamesDeepCopy,rounds)
            
            # save the data
            gameData.append(prepareDataForPlayer(Round,playerNamesDeepCopy,Map,Base))
            
            # control progressbar
            self.progressbar.step(100/(rounds*1.01))
            self.progressbar.update_idletasks()
            if ErrorOccured:
                break
                
        self.progressbar.stop()
        
        return gameData    
        
    def roundProcess(self,Base,Map,Round,listAI,playerNamesDeepCopy,rounds):
        startTimeRound = time.time()
        save_stdout = sys.stdout

        # import AIs
        try:
            for k in range(4):
                exec('import '+str(listAI[k]))
        except ImportError:
            messagebox.showerror('Error!','File not found!\n'+str(sys.exc_info()[1])+'.')
            self.root.destroy()
            return (Map,Base,False)
        except Exception:
            sys.stdout = open(str(self.playerNames[k])+'.log','a')
            formatted_lines = traceback.format_exc().splitlines()
            print(formatted_lines[-4])
            print(formatted_lines[-3])
            print(formatted_lines[-2])
            print(formatted_lines[-1])
            print()
            messagebox.showerror('Error!','An Error occured! Check '+self.playerNames[k]+'.log!')
            sys.stdout = save_stdout
            self.root.destroy()
            return (Map,Base,False)
            
        for k in range(4):
            
            playerCanMove = False
            # Check if player can move:
            if Base[k].resources >= min(self.unitCostWarrior,self.unitCostGatherer) or (Base[k].units != [] and Base[k].units != None):
                playerCanMove = True
            
            # safe Data for preventing cheating
            if playerCanMove:
                safe = safeData(Base,playerNamesDeepCopy,self.gameConfiguration,self.unitTypes,k)            
                
            
            # Set stdout to log
            sys.stdout = open(str(self.playerNames[k])+'.log','a')
            print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Start process round',Round,'\n')
            startTimeAi = time.time()
            
            # Execute AI only, if player can move
            if playerCanMove:
                try:
                    exec(listAI[k]+'.BattleClient(RoundState(Base[k],deepCopyMap(Map,self.gameConfiguration,self.unitTypes),Round),self.gameConfiguration)')
                    #exec(listAI[k]+'.BattleClient(RoundState(Base[k],Map,Round),self.gameConfiguration)')
                    #exec(listAI[k]+'.BattleClient(RoundState(Base[k],deepcopy(Map),Round),self.gameConfiguration)') # Needed to prevent Cheating in final Version!
                except (Exception, KeyboardInterrupt):#, IndexError, TypeError, NameError, SyntaxError):
                    formatted_lines = traceback.format_exc().splitlines()
                    print(formatted_lines[-5])
                    print(formatted_lines[-4])
                    print(formatted_lines[-3])
                    print(formatted_lines[-2])
                    print(formatted_lines[-1])
                    print()
                    messagebox.showerror('Error!','An Error occured! Check '+self.playerNames[k]+'.log!')
                    print('Processed round',Round,'in',round((time.time()-startTimeAi)*1000,4),'ms.\n')
                    print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Finished process round',Round,'\n')
                    self.userLog[k].close()
                    sys.stdout = save_stdout
                    
                    return (Map,Base,True)            
            if not playerCanMove:
                print('Game Over! No units and not enough resources to move!\n')
            print('Processed round',Round,'in',round((time.time()-startTimeAi)*1000,4),'ms.\n')
            print('[EXECUTION SERVER] '+time.strftime("%H:%M:%S.", time.localtime())+str(datetime.datetime.now().microsecond)+' Finished process round',Round,'\n')
            print('\n')
            
            # Set stdout back to default
            sys.stdout = save_stdout
            
            # process move
            if playerCanMove:
                
                # Reinitilize gameConfiguration and unitTypes in case of illegal manipulation
                self.gameConfiguration = GameConfiguration(self.unitCostWarrior,self.unitCostGatherer,self.unitStrengthWarrior,self.unitStrengthGatherer,self.unitMaxResourcesWarrior,self.unitMaxResourcesGatherer,rounds)
                self.unitTypes = {'WARRIOR' : UnitType(self.unitMaxResourcesWarrior,self.unitStrengthWarrior,self.unitCostWarrior,self.unitTypesStrings) , 'GATHERER' : UnitType(self.unitMaxResourcesGatherer,self.unitStrengthGatherer,self.unitCostGatherer,self.unitTypesStrings)}
                
                # check if player number k cheated
                cheater = preventCheating(Base,safe,playerNamesDeepCopy,k,self.gameConfiguration,Map)  
                 
                # betweenTurns: Move units, perform fights, compute new resources and so on     
                if cheater == False:
                    cheater = betweenTurns(Base,Map,self.resourceOnField,self.gameConfiguration,k,self.probabilityForResourceOnField)
                
                # if cheated set cheaters resources to 0    
                if cheater == True:
                    print('Player '+str(k+1)+': Cheater! Resources will be set to 0.')
                    Base[k].resources = 0
                    
        if platform.system() == 'Windows':
            print('Round',Round)
        else:
            print('Round',Round,'took',round((time.time()-startTimeRound)*1000,4),'ms.')
        
        return (Map,Base,False)

# Gui
    def gui(self,data):
        self.data = data
        self.roundOfCurrentGame = len(self.gameData)-1
        self.timer = 0
        self.mapLength = max(len(self.data[0].getMap()),len(self.data[0].getMap()[0]))
        self.scale = int(self.mapLength/5)
        self.root.geometry(str(int(100*self.mapLength/self.scale)+268)+'x750')
                
        self.frameInfo = Frame(self.root, width=550, height = 200)
        self.frameInfo.grid(row=1, column=0)
        
        self.frameSpeederRounder = Frame(self.root, width=550, height = 300)
        self.frameSpeederRounder.grid(row=2, column=0, sticky=(W), padx = 105)
        self.frameSpeeder = Frame(self.frameSpeederRounder, width=30, height = 300)
        self.frameSpeeder.grid(row=0, column=5, sticky=(W))
        self.frameRounder = Frame(self.frameSpeederRounder, width=183, height = 300)
        self.frameRounder.grid(row=0, column=0, columnspan = 4 ,sticky=(E))
        
        self.frameButton = Frame(self.root, width=550, height = 400)
        self.frameButton.grid(row=3, column=0) 
        
        # Canvas
        self.canvas = Canvas(self.root, width=int(100*self.mapLength/self.scale), height = int(100*self.mapLength/self.scale))
        self.canvas.grid(row=0, column=0)
        self.playerNames = self.data[0].getPlayerNames()
        
        self.land = PhotoImage(file="./img/land.gif").subsample(self.scale,self.scale)
        self.water = PhotoImage(file="./img/water.gif").subsample(self.scale,self.scale)
        self.wall = PhotoImage(file="./img/wall.gif").subsample(self.scale,self.scale)
        self.resource = PhotoImage(file="./img/resource.gif").subsample(self.scale,self.scale)
        self.base1 = PhotoImage(file="./img/player1_base.gif").subsample(self.scale,self.scale)
        self.base2 = PhotoImage(file="./img/player2_base.gif").subsample(self.scale,self.scale)
        self.base3 = PhotoImage(file="./img/player3_base.gif").subsample(self.scale,self.scale)
        self.base4 = PhotoImage(file="./img/player4_base.gif").subsample(self.scale,self.scale)
        self.gath1 = PhotoImage(file="./img/player1_gath.gif").subsample(self.scale,self.scale)
        self.gath2 = PhotoImage(file="./img/player2_gath.gif").subsample(self.scale,self.scale)
        self.gath3 = PhotoImage(file="./img/player3_gath.gif").subsample(self.scale,self.scale)
        self.gath4 = PhotoImage(file="./img/player4_gath.gif").subsample(self.scale,self.scale)
        self.warr1 = PhotoImage(file="./img/player1_warr.gif").subsample(self.scale,self.scale)
        self.warr2 = PhotoImage(file="./img/player2_warr.gif").subsample(self.scale,self.scale)
        self.warr3 = PhotoImage(file="./img/player3_warr.gif").subsample(self.scale,self.scale)
        self.warr4 = PhotoImage(file="./img/player4_warr.gif").subsample(self.scale,self.scale)

        
        # Player Names
        color = ["#FC4444", "#50E352", "#4563FF", "#FFF554"]
        w = 11
        for k in range(4):
            # Player Name
            Label(self.frameInfo, text=str(self.playerNames[k]), width = w, bg=color[k]).grid(row = k+1, column = 0)    
            self.resourcePlayer.append(StringVar())
            # Resources
            Label(self.frameInfo, textvariable=self.resourcePlayer[k], width = w, bg=color[k]).grid(row = k+1, column = 1)
            self.resourcePlayer[k].set(str(self.data[0].getResource(self.playerNames[k])))
            self.unitsPlayer.append(StringVar())
            # Total Units
            Label(self.frameInfo, textvariable=self.unitsPlayer[k], width = w, bg=color[k]).grid(row = k+1, column = 2)
            self.unitsPlayer[k].set(str(self.data[0].getUnits(self.playerNames[k])[0]+self.data[0].getUnits(self.playerNames[k])[1]))
            self.HiddenUnitsPlayer.append(StringVar())
            # Hidden Units
            Label(self.frameInfo, textvariable=self.HiddenUnitsPlayer[k], width = w, bg=color[k]).grid(row = k+1, column = 3)
            self.HiddenUnitsPlayer[k].set(str(self.data[0].getUnits(self.playerNames[k])[1]))
            self.unitsOnMapPlayer.append(StringVar())
            # Units On Map
            Label(self.frameInfo, textvariable=self.unitsOnMapPlayer[k], width = w, bg=color[k]).grid(row = k+1, column = 4)
            self.unitsOnMapPlayer[k].set(str(self.data[0].getUnits(self.playerNames[k])[0]))
                
        #Info Box
        Label(self.frameInfo, text='Player', width = w+1).grid(row = 0, column = 0)
        Label(self.frameInfo, text='Resources', width = w+1).grid(row = 0, column = 1)
        Label(self.frameInfo, text='Total Units', width = w+1).grid(row = 0, column = 2)
        Label(self.frameInfo, text='Hidden Units', width = w+1).grid(row = 0, column = 3)
        Label(self.frameInfo, text='Units on Map', width = w+1).grid(row = 0, column = 4)
        
        #Buttons
        self.buttonPlay = Button(self.frameButton, text="Play/Pause", command=self.changePauseStatus).grid(row = 1, column = 1)
        self.buttonBackward = Button(self.frameButton, text="<<", command=self.updateBoardBackward).grid(row = 1, column = 2)
        self.buttonForeward = Button(self.frameButton, text=">>", command=self.updateBoardForeward).grid(row = 1, column = 3)
        self.buttonForeward = Button(self.frameButton, text="Save game", command=self.save).grid(row = 1, column = 4)
        Label(self.frameButton, text='Space').grid(row = 2, column = 1)
        Label(self.frameButton, text='Left').grid(row = 2, column = 2)
        Label(self.frameButton, text='Right').grid(row = 2, column = 3)
        
        #Rounder
        Label(self.frameRounder, text='Round').grid(row = 1, column = 0)
        self.timer = Scale(self.frameRounder, from_=0, to=len(self.data)-1, length = 183 , orient=HORIZONTAL)
        self.timer.bind("<Button-1>", self.scalePause)
        self.timer.bind("<ButtonRelease-1>", self.scaleUpdateBoard)
        self.timer.set(0)
        self.timer.grid(row=0, column=0, sticky = (E))
        
        #Speeder
        Label(self.frameSpeeder, text='Speed').grid(row = 1, column = 0)
        self.speeder = Scale(self.frameSpeeder, from_=0.1, digits=2, to=4, resolution=0.1, orient=HORIZONTAL)
        self.speeder.set(self.lastSpeeder)
        self.speeder.grid(row=0, column=0, sticky = (W))
        
        #Keys
        self.root.bind('<KeyPress-Right>', self.updateBoardForewardKey)
        self.root.bind('<KeyPress-Left>', self.updateBoardBackwardKey)
        self.root.bind('<KeyPress-space>', self.changePauseStatusKey)
        
        # force focus
        self.root.focus_force()
        
        self.drawNewGrid()
        self.paused = True
        self.finished = False
        self.playTheGame()
    
    def scalePause(self,event):
        self.paused = True
        return None
        
    def scaleUpdateBoard(self,event):
        self.drawNewGrid()
        self.updateBoardForce = True
        self.updateBoard()
        self.updateBoardForce = False
        return
    
    def roundsUp(self,event):
        rounds = self.rounds.get()
        if 0 <= rounds or rounds < 1000:
            for k in range(10):
                if 0<=rounds-k*100 and rounds-k*100<100:
                    self.rounds.set((k+1)*100)       
        return None
            
    def roundsDown(self,event):
        rounds = self.rounds.get()
        if 100 < rounds or rounds <= 1000:
            for k in range(1,11):
                if 0<rounds-k*100 and rounds-k*100<=100:
                    self.rounds.set(k*100)       
        return None
    
    def chooseMap(self):
        name = filedialog.askopenfilename(initialdir = "./maps",title = "choose a *.map-file",filetypes = (("map files","*.map"),("all files","*.*")))[::-1] # inverse Name
        if name != () and name != "":
            mapName = ''
            for char in name:
                if char == '/':
                    break
                mapName += char
            self.MapName.set(mapName[::-1])

    def chooseAi(self,k):
        name = filedialog.askopenfilename(initialdir = "./",title = "choose your file",filetypes = (("python files","*.py"),("all files","*.*")))[::-1] # inverse Name
        if name != () and name != "":
            Ai = ''
            for char in name:
                if char == '/':
                    break
                Ai += char
            exec('self.Ai'+str(k)+'.set(Ai[::-1])')   
    
    def changePauseStatus(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True
    
    def changePauseStatusKey(self,event):
        if self.paused:
            self.paused = False
        else:
            self.paused = True
    
    def updateBoardForeward(self):
        if self.timer.get()<self.roundOfCurrentGame:    
            self.timer.set(self.timer.get()+1)
            self.updateBoard()
    
    def updateBoardBackward(self):
        if self.timer.get()>0:
            self.timer.set(self.timer.get()-1)
            self.backward = True
            self.updateBoard()

    def updateBoardForewardKey(self,event):
        if self.timer.get()<self.roundOfCurrentGame:
            self.timer.set(self.timer.get()+1)
            self.updateBoard()

    def updateBoardBackwardKey(self,event):
        if self.timer.get()>0:
            self.timer.set(self.timer.get()-1)
            self.backward = True
            self.finished = False
            self.updateBoard()
       
    def initializeRadiobuttons(self,gameStats,rounds,mapName,Ai):
        
        # Ai = [AI1,AI2,AI3,AI4]
        radioPick = 'Custom'
        challengesList = ['Noob','Intermediate','Advanced','Expert']
        for challenge in challengesList:
            if gameStats.getRounds(challenge) == rounds and gameStats.getMap(challenge) == mapName and shortString(Ai[0]) == 'yourAI' and shortString(Ai[1]) == challenge and Ai[2] == challenge and shortString(Ai[3]) == challenge:
                radioPick = challenge
        return radioPick
     
    def updateRadioButton(self):
        # set Rounds, Map, Ai in dependance of radiobuttons
        selectedChallenge = findChallenge(gameStats,[self.Ai1.get(),self.Ai2.get(),self.Ai3.get(),self.Ai4.get()],self.rounds.get(),self.MapName.get()) # which challeng is selected
        
        # save Custom inputs, if Button did not change
        if self.radioButtonVar.get() == 'Custom' and self.saveButton == self.radioButtonVar.get():
            self.saveRounds = self.rounds.get()
            self.saveMap = self.MapName.get()
            self.saveAi1 = self.Ai1.get()
            self.saveAi2 = self.Ai2.get()
            self.saveAi3 = self.Ai3.get()
            self.saveAi4 = self.Ai4.get()
        
        if self.saveButton != self.radioButtonVar.get():
            # radiobutton changed
            if self.radioButtonVar.get() != 'Custom':                    
                self.rounds.set(gameStats.getRounds(self.radioButtonVar.get()))
                self.MapName.set(gameStats.getMap(self.radioButtonVar.get()))
                self.Ai1.set('yourAI')
                # Here set AIs for Challenge; also see functions.findChallenge()
                if self.radioButtonVar.get() == 'Noob' or self.radioButtonVar.get() == 'Intermediate':
                    for k in [2,3,4]:
                        exec("self.Ai"+str(k)+".set(self.radioButtonVar.get())")
                elif self.radioButtonVar.get() == 'Advanced':
                    for k in [2,3]:
                        exec("self.Ai"+str(k)+".set('Dummy')")
                    exec("self.Ai"+str(4)+".set(self.radioButtonVar.get())")
                elif self.radioButtonVar.get() == 'Expert':
                    exec("self.Ai"+str(2)+".set('Intermediate')")
                    exec("self.Ai"+str(3)+".set('Advanced')")
                    exec("self.Ai"+str(4)+".set('Expert')")
            else:
                self.rounds.set(self.saveRounds)
                self.MapName.set(self.saveMap)
                for k in range(4):
                    exec("self.Ai"+str(k+1)+".set(self.saveAi"+str(k+1)+")")
        else:
            # either nothing changed or input
            if selectedChallenge != self.radioButtonVar.get():
                 self.radioButtonVar.set(selectedChallenge)
        self.saveButton = self.radioButtonVar.get()
    
    def idle(self):
        self.updateRadioButton()
        updateConfig(self.rounds.get(),self.MapName.get(),[self.Ai1.get(),self.Ai2.get(),self.Ai3.get(),self.Ai4.get()],speedConfig)
        self.root.after(50, self.idle)
        return None
        
    def playTheGame(self):        
        # also idle
        
        self.updateRadioButton()
        updateConfig(self.rounds.get(),self.MapName.get(),[self.Ai1.get(),self.Ai2.get(),self.Ai3.get(),self.Ai4.get()],self.speeder.get())
        
        # playTheGame
        if not self.paused:
            if self.finished and self.timer.get() >= self.roundOfCurrentGame:
                self.timer.set(0)
            if self.timer.get() == 0:
                self.drawNewGrid()
                self.finished = False
            if self.timer.get() < self.roundOfCurrentGame:
                self.timer.set(self.timer.get() + 1)
                self.speed.set(int(100*1/self.speeder.get()))
                self.finished = False
                self.updateBoard()
            else:
                self.paused = True
                self.finished = True
            self.canvas.after(self.speed.get(), self.playTheGame)
        else:
            self.canvas.after(50, self.playTheGame) # 50
            
    def updateBoard(self):

        if self.backward:
            MapOld = self.data[self.timer.get()+1].getMap()
            self.backward = False
        else:
            MapOld = self.data[self.timer.get()-1].getMap()
        Map = self.data[self.timer.get()].getMap()
        
        for X in range(len(Map)):
            for Y in range(len(Map[X])):
                if Map[X][Y] == MapOld[X][Y] and not self.updateBoardForce:   # nothing changed => don't change widget
                    continue
                else:   # field has changed => find new image
                    if Map[X][Y] == FieldType.WALL:
                        fieldImage = self.wall       
                    elif Map[X][Y] == FieldType.WATER:  
                        fieldImage = self.water
                    elif Map[X][Y] == str(1)+FieldType.BASE:   
                        fieldImage = self.base1
                    elif Map[X][Y] == str(2)+FieldType.BASE:   
                        fieldImage = self.base2
                    elif Map[X][Y] == str(3)+FieldType.BASE:   
                        fieldImage = self.base3
                    elif Map[X][Y] == str(4)+FieldType.BASE:   
                        fieldImage = self.base4
                    elif Map[X][Y] == str(1)+UnitType.WARRIOR:
                        fieldImage = self.warr1
                    elif Map[X][Y] == str(1)+UnitType.GATHERER:
                        fieldImage = self.gath1
                    elif Map[X][Y] == str(2)+UnitType.WARRIOR:
                        fieldImage = self.warr2
                    elif Map[X][Y] == str(2)+UnitType.GATHERER:
                        fieldImage = self.gath2
                    elif Map[X][Y] == str(3)+UnitType.WARRIOR:
                        fieldImage = self.warr3
                    elif Map[X][Y] == str(3)+UnitType.GATHERER:
                        fieldImage = self.gath3
                    elif Map[X][Y] == str(4)+UnitType.WARRIOR:
                        fieldImage = self.warr4
                    elif Map[X][Y] == str(4)+UnitType.GATHERER:
                        fieldImage = self.gath4
                    elif Map[X][Y] == FieldType.RESOURCE:
                        fieldImage = self.resource
                    elif Map[X][Y] == FieldType.LAND:
                        fieldImage = self.land
                    self.canvas.delete(self.field[X][Y])
                    self.field[X][Y] = self.canvas.create_image(X*int(100/self.scale),Y*int(100/self.scale), anchor=NW, image=fieldImage)
                    
        
        # InfoBox: Resources and Round
        for k in range(4):
            self.resourcePlayer[k].set(str(self.data[self.timer.get()].getResource(self.playerNames[k])))
            self.unitsPlayer[k].set(str(self.data[self.timer.get()].getUnits(self.playerNames[k])[0]+self.data[self.timer.get()].getUnits(self.playerNames[k])[1]))
            self.HiddenUnitsPlayer[k].set(str(self.data[self.timer.get()].getUnits(self.playerNames[k])[1]))
            self.unitsOnMapPlayer[k].set(str(self.data[self.timer.get()].getUnits(self.playerNames[k])[0]))
        self.round.set('Round '+str(self.timer.get()))
    
    def drawNewGrid(self):
        Map = self.data[0].getMap()
        for X in range(len(Map)):
            self.field.append([])
            for Y in range(len(Map[X])):
                if Map[X][Y] == FieldType.WALL:
                    fieldImage = self.wall       
                elif Map[X][Y] == FieldType.WATER:  
                    fieldImage = self.water
                elif Map[X][Y] == str(1)+FieldType.BASE:   
                    fieldImage = self.base1
                elif Map[X][Y] == str(2)+FieldType.BASE:   
                    fieldImage = self.base2
                elif Map[X][Y] == str(3)+FieldType.BASE:   
                    fieldImage = self.base3
                elif Map[X][Y] == str(4)+FieldType.BASE:   
                    fieldImage = self.base4
                elif Map[X][Y] == str(1)+UnitType.WARRIOR:
                    fieldImage = self.warr1
                elif Map[X][Y] == str(1)+UnitType.GATHERER:
                    fieldImage = self.gath1
                elif Map[X][Y] == str(2)+UnitType.WARRIOR:
                    fieldImage = self.warr2
                elif Map[X][Y] == str(2)+UnitType.GATHERER:
                    fieldImage = self.gath2
                elif Map[X][Y] == str(3)+UnitType.WARRIOR:
                    fieldImage = self.warr3
                elif Map[X][Y] == str(3)+UnitType.GATHERER:
                    fieldImage = self.gath3
                elif Map[X][Y] == str(4)+UnitType.WARRIOR:
                    fieldImage = self.warr4
                elif Map[X][Y] == str(4)+UnitType.GATHERER:
                    fieldImage = self.gath4
                elif Map[X][Y] == FieldType.RESOURCE:
                    fieldImage = self.resource
                elif Map[X][Y] == FieldType.LAND:
                    fieldImage = self.land
                self.field[X].append(self.canvas.create_image(X*int(100/self.scale),Y*int(100/self.scale), anchor=NW, image=fieldImage))
    
    def returnData(self):
        return (self.gameData,self.ranAgain,self.gameTitle,self.noGameRan)

programIsRunning = True
ranAgain = False
data = None
noGameRan = True

while programIsRunning:
    # Initilize default settings
    try:
        config = open('config.ini','r')
    except OSError:
        updateConfig(str(gameStats.getRounds(gameStats.getChallenge())),gameStats.getMap(gameStats.getChallenge()),['yourAI',gameStats.getChallenge(),gameStats.getChallenge(),gameStats.getChallenge()],1)
        config = open('config.ini','r')
    listAIconfig=[None,None,None,None]
    for line in config:
        if line[:6] == 'Rounds':
            roundsConfig = findValue(line)
        if line[:3] == 'Map':
            mapNameConfig = findValue(line)
        for k in range(4):
            if line[:4] == 'AI_'+str(k+1):
                listAIconfig[k] = findValue(line)
        if line[:5] == 'Speed':
            speedConfig = findValue(line)
            
    (data,ranAgain,gameTitle,noGameRan) = Player(data,not ranAgain,gameTitle,roundsConfig,listAIconfig,mapNameConfig,speedConfig).returnData()
    
    if not ranAgain or noGameRan:
        programIsRunning = False

