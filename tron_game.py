#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#This is the code that creates and maintains the board

####################
#IMPORTS
####################

import pygame
import config
import cycle
from pygame.locals import *
import sys

####################
#Cell Class
####################
#The basic unit of the game, each cell is either neutral or owned by a player
#If a cycle passes over a non-neutral cell, it crashes
class Cell(object):

    def __init__(self, row, col, window, 
                 trailTurns, color = config.BLANK_COLOR):
        self.trailTurns = trailTurns
        self.color = color
        self.turns = 0 #the number of turns that the cell will remain 
        #a player's color before changing back to the blank color
        self.row, self.col = row, col
        self.direction = "no direction"#Direction is used when drawing
        
    def setOwner(self, color, direction):
        #Sets the cells's owner to a player's color
        self.color = color
        self.turns = self.trailTurns
        if(direction[0] != 0):#Gives the cell a direction to be drawn
            self.direction = "vertical"
        elif(direction[1] != 0):
            self.direction = "horizontal"
        else:
            self.direction = "no direction"
        
    def incrementTurns(self):
        #Decreases the number of turns the cell will remain a player's color
        self.turns -= 1
        if(self.turns < 0):#When the cell is out of turns, just return to
            #The blank color
            self.color = config.BLANK_COLOR
        return self.turns
        
####################
#Board Class
####################    
#A board composed of cells which the cycles race on
class Board(object):
    def __init__(self, rows, cols, trailTurns, window):
        self.window = window
        self.rows, self.cols = rows, cols
        self.board = []
        for row in xrange(rows):#Creates the board as a 2d list of cells
            tempRow = []
            for col in xrange(cols):
                tempRow.append(Cell(row, col, window, trailTurns, 
                               color = config.BLANK_COLOR))
            self.board.append(tempRow)

####################
#TronGame Class
#################### 
#Starts an instance of a tron game inside of a supplied surface
class TronGame(object): 
    def __init__(self, rows, cols, frameRate, window, surface, trailTurns, 
                 playerList, humanPlayer = None):
        self.trailTurns = trailTurns
        self.humanPlayer = humanPlayer
        self.rows, self.cols = rows, cols
        self.window, self.surface = window, surface
        self.frameRate = frameRate
        self.gameInit(playerList)#Initializes the board and places the players
        self.winner = None
        while (self.gameOver == False):#Game loop
            self.update()
        self.redrawAll
        pause = trailTurns
        while(pause > 0):#Waits until the tails have emptied
            pause -= 1
            self.window.mainClock.tick(self.frameRate*2)#Waits
            self.redrawAll()
            self.getHumanEvents()

    def gameInit(self,startPlayer):#Initializes the board and sets the players
        self.board = Board(self.rows, self.cols, self.trailTurns, self.window)
        self.gameOver = False
        #Playerlist contains a list of the cycles for this game
        self.playerList = []
        for i in xrange(len(startPlayer)):
            self.playerList.append(self.placeCycle(startPlayer[i],i))
        self.surface.setBoard(self.board)

    def redrawAll(self):#Redraws the board
        for player in self.playerList:
            self.surface.drawCycle(player)
        self.surface.redrawAll()
        self.surface.updateDisplay()

    def update(self):#Runs every game loop
        self.computeAIMove()#Computes the AI's next move
        self.pump()
        self.window.mainClock.tick(self.frameRate)#Waits
        self.getHumanEvents()#Processes key presses
        self.getNetworkedEvents()#Get networked events for a networked game
        self.moveCycles()#Moves all of the cycles at once
        self.checkGameOver()#Checks if the game is over
        self.redrawAll()#Displays a new screen

    def pump(self):#Pumps the client's connection to the server. 
        #Pumped twice each turn, once when the AI's move is called, 
        #and once after we have waited
        #Should be overwritten by a networked class
        pass

    def getNetworkedEvents(self):#Calls the events that have happened 
        #since we last called the client connection
        pass#Should be overwritten by a networked class

    def moveCycles(self):#Moves all of the cycles at once
        if(self.gameOver == False):
            for player in self.playerList:#Moves the players
                if(player.isLive == True):
                    player.move()

    def getHumanEvents(self):#Checks if the human player has pressed any keys
        for event in pygame.event.get():#Runs through the keyboard events
            if event.type == QUIT:#Quits the game
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == 27:#The escape key
                    pygame.quit()
                    sys.exit()  
                #If there is a human player, respond to mouse events
                if(self.humanPlayer != None) and (self.gameOver == False):
                    if event.key == K_UP:
                        self.playerList[self.humanPlayer].turn(-1, 0)
                    if event.key == K_LEFT:
                        self.playerList[self.humanPlayer].turn(0, -1)
                    if event.key == K_RIGHT:
                        self.playerList[self.humanPlayer].turn(0, 1)
                    if event.key == K_DOWN:
                        self.playerList[self.humanPlayer].turn(1, 0)

    def computeAIMove(self):#Figures out what the AI's next move is. 
        #Does not actually move the AI
        for player in self.playerList:
            if((player.isLive == True) and (player.isAI == True)):
                player.computeMove()

    def checkGameOver(self):#Checks if the game is over. A wrapper for the 
        #isGameOver class that can be overwritten by a networked class
        self.gameOver = self.isGameOver()
        return self.gameOver

    def isGameOver(self):#determines how many cycles are still alive
        playersLive = 0
        for player in self.playerList:
            if(player.isLive == True):
                #If there is only one cycle alive, self.winner will be it
                self.winner = player
                playersLive += 1
        if(playersLive == 1):
            return True
        if(playersLive == 0):#If no cycles have survived, there is no winner
            self.winner = None
            return True
        return False
    
    def placeCycle(self, player, playerNumber):
        #Create a cycle based on a passed dictionary
        newcycle = cycle.newCycle(self.window, self.board.board, 
                                    self.rows, self.cols, 
                                    player["startPos"][0], 
                                    player["startPos"][1], 
                                    player["color"], 
                                    player["startDir"][0], 
                                    player["startDir"][1], 
                                    playerNumber, 
                                    type = player["type"])
        return newcycle

####################
#Networked Tron Game Class
####################
#Extends the tron game with networking
#A game class with some added networking-specific requirements
class NetworkedTronGame(TronGame):
    def __init__(self, rows, cols, speed, window, surface, trailTurns, 
                 playerList, client, humanPlayer = None):
        self.connection = client
        TronGame.__init__(self, rows, cols, speed, window, surface, 
                        trailTurns, playerList, humanPlayer = humanPlayer)

    def placeCycle(self, player, playerNumber):#Places a networking cycle
        newcycle = cycle.newCycle(self.window, self.board.board, self.rows, 
                                    self.cols, player["startPos"][0], 
                                    player["startPos"][1], player["color"], 
                                    player["startDir"][0], 
                                    player["startDir"][1], 
                                    playerNumber, type = player["type"], 
                                    connection = self.connection)
        return newcycle

    def checkGameOver(self):#When the game is over, this sends out a message 
        #to all clients that the game is over
        TronGame.checkGameOver(self)
        if(self.gameOver == True):
            self.connection.gameOver()

    def networkChanges(self, events):
        ##Eacts the changes sent with this networking moment
        for event in events:
            if(event["gameEvent"] == "cycleTurn"):
                self.playerList[event["cycleNum"]].setDirection(event["drow"],
                                                                event["dcol"])
            if(event["gameEvent"] == "cycleCrash"):
                self.playerList[event["cycleNum"]].networkCrash()
            if(event["gameEvent"] == "gameOver"):
                self.gameOver = True

    def pump(self):#Pumps the client's connection to the server. 
        #Pumped twice each turn, once when the AI's move is called, 
        #and once after we have waited
        self.connection.pump()

    def getNetworkedEvents(self):#Overwrites the empty class 
        #getNetworkedEvents with something that actually 
        #fetches the networked events. Also calls the events that have 
        #happened since we last called the client connection
        self.pump()
        self.networkChanges(self.connection.callGameEvents())
        