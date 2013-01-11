#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#These functions create the cycles on the board

####################
#IMPORTS
####################
import random
import config

####################
#Cycle Creator
####################
#This function creates cycles of different types
def newCycle(window, board, rows, cols, row, col, color, drow, dcol, 
            playerNumber, type = "none", name = None, connection = None):
    playerName = name
    if(name == None):
        #If no name has been supplied, then just name it after its type
        name = type
    if(type == "basic"):
        return BasicAICycle(window, board, rows, cols, row, col, color, 
                            drow, dcol, playerNumber, name = playerName, 
                            connection = None)
    elif(type == "linelook"):
        return LineLookCycle(window, board, rows, cols, row, col, 
                                color, drow, dcol, playerNumber, 
                                connection = connection, name = playerName)
    elif(type == "avoider"):
        return AvoiderCycle(window, board, rows, cols, row, col, 
                                color, drow, dcol, playerNumber, 
                                connection = None, name = playerName)
    elif(type == "local"):
        if(connection == None):#If there is no network connection, crash
            raise Exception("Networked cycle without a connection")
        return LocalCycle(window, board, rows, cols, row, col, color, 
                            drow, dcol, playerNumber, 
                            connection = connection, name = playerName)
    elif(type == "networked ai"):
        if(connection == None):#If there is no network connection, crash
            raise Exception("Networked cycle without a connection")
        return NetworkedAICycle(window, board, rows, cols, row, col, 
                                color, drow, dcol, playerNumber, 
                                connection = connection, name = playerName)
    else:#Just to be safe, return a simple cycle
        return Cycle(window, board, rows, cols, row, col, color, drow, dcol, 
            playerNumber, connection = None, name = playerName)

####################
#Cycle Class
####################
class Cycle(object):#A basic cycle class
    isAI = False
    def __init__(self, window, board, rows, cols, row, col, color, drow, 
                    dcol, playerNumber, name, connection):
        self.rows, self.cols = rows, cols
        self.playerNumber = playerNumber
        self.name = name
        self.window = window
        self.isLive = True
        self.connection = connection
        self.row, self.col = row, col
        self.color = color
        self.board = board
        self.drow, self.dcol = drow, dcol
        self.setCell()
        
    def move(self):#Moves the cycle in the direction it is pointed in
        self.row += self.drow
        self.col += self.dcol
        if(not self.testMove(self.row, self.col)):#Tests if the move is legal
            self.crash()
        else:
            self.setCell()

    def testMove(self, row, col):#Tests if a move is legal
        if((row < 0) or (col < 0) or 
           (row >= self.rows) or (col >= self.cols ) or 
           (self.board[row][col].color != config.BLANK_COLOR)):
            return False
        else:
            return True

    def turn(self, drow, dcol):#Resets drow, dcol
    #This function can be overwritten by networked classes
        if((self.drow != -drow) or (self.dcol != -dcol)):
            #So that running into yourself is not a valid move
            self.drow, self.dcol = drow, dcol


    def setDirection(self, drow, dcol):#Same as turn, but should not 
    #be overwritten by a networked class
    #This function should not be overwritten by networked classes
        if((self.drow != -drow) or (self.dcol != -dcol)):
            #So that running into yourself is not a valid move
            self.drow, self.dcol = drow, dcol

    def crash(self):#Crash the cycle
        self.isLive = False
    
    def networkCrash(self):#Should not be overwritten by networked classes
        self.isLive = False


    def setCell(self):#Set a certain cell to the cycle's color
        self.board[self.row][self.col].setOwner(self.color, 
                                                (self.drow, self.dcol))

    def findLegalDistance(self, move):#Finds the distance the cycle can travel in a given direction without dying
        tempRow = self.row + move[0]
        tempCol = self.col + move[1]
        numSpaces = 0
        while(self.testMove(tempRow, tempCol) == True):
            numSpaces += 1
            tempRow +=  move[0]
            tempCol +=  move[1]
        return numSpaces

####################
#LocalCycle Class
####################
#A cycle that is controlled by outside influence in a networked game
class LocalCycle(Cycle):
    def turn(self, drow, dcol):
        self.connection.turn(self.playerNumber, drow, dcol)

    def crash(self):
        self.connection.crash(self.playerNumber)

####################
#BasicAICycle Class
####################
#A cycle that is controlled by a simple AI
class BasicAICycle(Cycle):
    isAI = True

    def computeMove(self):#The AI class
        move = self.pickRandomMove()#Every so often, pick a random move
        tempRow = self.row + move[0]
        tempCol = self.col + move[1]
        if(self.testMove(tempRow, tempCol) == False):
            move = self.safeMove()#Repicks if the move is unsafe
            if(move != None):
                return self.turn(move[0], move[1])
            else:#If there is no safe move, crash
                return self.crash()
        return self.turn(move[0], move[1])

    def pickRandomMove(self):#Randomizes the AI's movement
        if(random.random() > config.RANDOM_PERCENT):
            #Picks a random move a set percentage of the time
            return random.choice(config.POSSIBLE_MOVES)
        else:
            return (self.drow, self.dcol)

    def safeMove(self):#Makes sure that the move picked is safe
        for move in config.POSSIBLE_MOVES:
                if(self.testMove(self.row + move[0], 
                                self.col + move[1]) == True):
                    return move
        return None


####################
#NetworkedAICycle Class
####################
#A cycle that is controlled by a simple AI and is networked
class NetworkedAICycle(BasicAICycle):
    def turn(self, drow, dcol):
        self.connection.turn(self.playerNumber, drow, dcol)

    def crash(self):#Crashes the cycle if it is in an illegal place
        Cycle.crash(self)


####################
#LineLookCycle Class
####################
#A slightly more advanced AI, which looks is all legal directions when it
#Is about to crash, and chooses the one in which it can travel the furthest
#Without crashing.
class LineLookCycle(Cycle):
    isAI = True

    def computeMove(self):#The AI class
        move = self.pickRandomMove()#Every so often, pick a random move
        tempRow = self.row + move[0]
        tempCol = self.col + move[1]
        if(self.testMove(tempRow, tempCol) == False):
            move = self.findBest()#Repicks if the move is unsafe
            if(move == None):#If there is no safe move, crash
                print self.color, "crashing"
                return self.crash()
            else:
                print self.color, "turning", move
                return self.turn(move[0], move[1])
        return self.turn(move[0], move[1])

    def pickRandomMove(self):#Randomizes the AI's movement
        if(random.random() > config.RANDOM_PERCENT):
            #Picks a random move a set percentage of the time
            print self.color, "picking a random move"
            return random.choice(config.POSSIBLE_MOVES)
        else:
            return (self.drow, self.dcol)

    def findBest(self):#Finds the best possible move from the list of possible moves
        print "finding the best move for", self.color, 
        highestLegalDistance = 0
        bestMove = None
        for move in config.POSSIBLE_MOVES:
                print "\ttrying move ", move
                legalDistance = self.findLegalDistance(move)
                print "\t\tlegal distance of", legalDistance
                if(legalDistance > highestLegalDistance):
                    highestLegalDistance = legalDistance
                    bestMove = move
        print "returning the best move:", move
        return bestMove

####################
#AvoiderCycle Class
####################
#Another advanced AI
#Always chooses the path with the longest distance before hitting anything.
class AvoiderCycle(Cycle):
    isAI = True

    def computeMove(self):#The AI class
        move = self.findBest()#Repicks if the move is unsafe
        if(move == None):#If there is no safe move, crash
            print self.color, "crashing"
            return self.crash()
        else:
            print self.color, "turning", move
            return self.turn(move[0], move[1])
        return self.turn(move[0], move[1])

    def findBest(self):#Finds the best possible move from the list of possible moves
        print "finding the best move for", self.color, 
        highestLegalDistance = 0
        bestMove = None
        for move in config.POSSIBLE_MOVES:
                print "\ttrying move ", move
                legalDistance = self.findLegalDistance(move)
                print "\t\tlegal distance of", legalDistance
                if(legalDistance > highestLegalDistance):
                    highestLegalDistance = legalDistance
                    bestMove = move
        print "returning the best move:", move
        return bestMove
