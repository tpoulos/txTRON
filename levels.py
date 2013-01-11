#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#This file contains the level information for the single player game

####################
#IMPORTS
####################
from pygame.locals import *#Required for Color class

####################
#NETWORK LEVEL
####################

NETWORKED_LEVEL = dict()#The level loaded when playing on the network

playerList = [dict(), dict(), dict(), dict()]

playerList[0]["startPos"] = (0,0)
playerList[0]["startDir"] = (0,1)
playerList[0]["color"] = Color(0, 255, 0, 1)#green

playerList[1]["startPos"] = (0,29)
playerList[1]["startDir"] = (1,0)
playerList[1]["color"] = Color(0, 0, 255, 1)#blue

playerList[2]["startPos"] = (29,29)
playerList[2]["startDir"] = (0,-1)
playerList[2]["color"] = Color(255, 0, 0, 1)#Red

playerList[3]["startPos"] = (29,0)
playerList[3]["startDir"] = (-1, 0)
playerList[3]["color"] = Color(255, 0, 255, 1)#Cyan

NETWORKED_LEVEL["name"] = "Network"
NETWORKED_LEVEL["description"] = "Basic AI skirmish with 4 cycles"
NETWORKED_LEVEL["playerList"] = playerList
NETWORKED_LEVEL["trailTurns"] = 20
NETWORKED_LEVEL["speed"] = 10
NETWORKED_LEVEL["rows"] = 30
NETWORKED_LEVEL["cols"] = 30


####################
#LEVEL LIST
####################

LEVEL_LIST = []

####################
#LEVEL 0
####################
level = 0

playerList = [dict(), dict(), dict(), dict()]
playerList[0]["startPos"] = (0,0)
playerList[0]["startDir"] = (0,1)
playerList[0]["color"] = Color(0, 255, 0, 1)#green
playerList[0]["type"] = "human"

playerList[1]["startPos"] = (0,29)
playerList[1]["startDir"] = (1,0)
playerList[1]["color"] = Color(0, 0, 255, 1)#blue
playerList[1]["type"] = "basic"

playerList[2]["startPos"] = (29,29)
playerList[2]["startDir"] = (0,-1)
playerList[2]["color"] = Color(255, 0, 0, 1)#Red
playerList[2]["type"] = "basic"

playerList[3]["startPos"] = (29,0)
playerList[3]["startDir"] = (-1, 0)
playerList[3]["color"] = Color(255, 0, 255, 1)#Cyan
playerList[3]["type"] = "basic"

LEVEL_LIST.append(dict())
LEVEL_LIST[level]["name"] = "Simple"
LEVEL_LIST[level]["description"] = "basic AI skirmish with 4 cycles"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 20
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 30
LEVEL_LIST[level]["cols"] = 30
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 1
####################

level = 1

LEVEL_LIST.append(dict())
LEVEL_LIST[level]["name"] = "Longer"
LEVEL_LIST[level]["description"] = "4 cycle AI skirmish with long tails"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 40
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 30
LEVEL_LIST[level]["cols"] = 30
LEVEL_LIST[level]["humanPlayer"] = 0


####################
#LEVEL 2
####################

level = 2

playerList = [dict(), dict()]

playerList[0]["startPos"] = (14,8)
playerList[0]["color"] = Color(255, 255, 0, 1)#yellow
playerList[0]["type"] = "human"
playerList[0]["startDir"] = (-1,0)

playerList[1]["startPos"] = (0,8)
playerList[1]["color"] = Color(0, 128, 128, 1)#teal
playerList[1]["type"] = "basic"
playerList[1]["startDir"] = (1,0)

LEVEL_LIST.append(dict())

LEVEL_LIST[level]["name"] = "Human vs AI"
LEVEL_LIST[level]["description"] = "2 cycle AI deathmatch"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 40
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 15
LEVEL_LIST[level]["cols"] = 15
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 3
####################

level = 3

playerList = [dict(), dict()]

playerList[0]["startPos"] = (19,10)
playerList[0]["color"] = Color(255, 255, 0, 1)#yellow
playerList[0]["type"] = "human"
playerList[0]["startDir"] = (-1,0)

playerList[1]["startPos"] = (0,10)
playerList[1]["color"] = Color(0, 128, 128, 1)#teal
playerList[1]["type"] = "avoider"
playerList[1]["startDir"] = (1,0)

LEVEL_LIST.append(dict())

LEVEL_LIST[level]["name"] = "Human vs AI: Round 2"
LEVEL_LIST[level]["description"] = "Longer tails. Larger board. Better AI."
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 100
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 20
LEVEL_LIST[level]["cols"] = 20
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 4
####################

level = 4

playerList = [dict(), dict()]

playerList[0]["startPos"] = (19,10)
playerList[0]["color"] = Color(255, 255, 0, 1)#yellow
playerList[0]["type"] = "human"
playerList[0]["startDir"] = (-1,0)

playerList[1]["startPos"] = (0,10)
playerList[1]["color"] = Color(0, 128, 128, 1)#teal
playerList[1]["type"] = "linelook"
playerList[1]["startDir"] = (1,0)

LEVEL_LIST.append(dict())

LEVEL_LIST[level]["name"] = "Human vs AI: Round 3"
LEVEL_LIST[level]["description"] = "Even longer tails. The best AI."
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 150
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 20
LEVEL_LIST[level]["cols"] = 20
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 5
####################
level = 5

playerList = [dict(), dict(), dict(), dict()]
playerList[0]["startPos"] = (0,0)
playerList[0]["startDir"] = (0,1)
playerList[0]["color"] = Color(0, 255, 0, 1)#green
playerList[0]["type"] = "human"

playerList[1]["startPos"] = (0,19)
playerList[1]["startDir"] = (1,0)
playerList[1]["color"] = Color(0, 0, 255, 1)#blue
playerList[1]["type"] = "basic"

playerList[2]["startPos"] = (19,19)
playerList[2]["startDir"] = (0,-1)
playerList[2]["color"] = Color(255, 0, 0, 1)#Red
playerList[2]["type"] = "basic"

playerList[3]["startPos"] = (19,0)
playerList[3]["startDir"] = (-1, 0)
playerList[3]["color"] = Color(255, 0, 255, 1)#Cyan
playerList[3]["type"] = "basic"

LEVEL_LIST.append(dict())
LEVEL_LIST[level]["name"] = "Tiny"
LEVEL_LIST[level]["description"] = "Small 4 AI skirmish with simple AI"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 15
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 20
LEVEL_LIST[level]["cols"] = 20
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 6
####################
level = 6

playerList = [dict(), dict(), dict(), dict()]
playerList[0]["startPos"] = (0,0)
playerList[0]["startDir"] = (0,1)
playerList[0]["color"] = Color(0, 255, 0, 1)#green
playerList[0]["type"] = "human"

playerList[1]["startPos"] = (0,19)
playerList[1]["startDir"] = (1,0)
playerList[1]["color"] = Color(0, 0, 255, 1)#blue
playerList[1]["type"] = "linelook"

playerList[2]["startPos"] = (19,19)
playerList[2]["startDir"] = (0,-1)
playerList[2]["color"] = Color(255, 0, 0, 1)#Red
playerList[2]["type"] = "linelook"

playerList[3]["startPos"] = (19,0)
playerList[3]["startDir"] = (-1, 0)
playerList[3]["color"] = Color(255, 0, 255, 1)#Cyan
playerList[3]["type"] = "linelook"

LEVEL_LIST.append(dict())
LEVEL_LIST[level]["name"] = "Improved Tiny"
LEVEL_LIST[level]["description"] = "Small 4 AI skirmish with better AI"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 15
LEVEL_LIST[level]["speed"] = 10
LEVEL_LIST[level]["rows"] = 20
LEVEL_LIST[level]["cols"] = 20
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 7
####################
level = 7

playerList = [dict(), dict(), dict(), dict()]
playerList[0]["startPos"] = (0,0)
playerList[0]["startDir"] = (0,1)
playerList[0]["color"] = Color(0, 255, 0, 1)#green
playerList[0]["type"] = "human"

playerList[1]["startPos"] = (0,14)
playerList[1]["startDir"] = (1,0)
playerList[1]["color"] = Color(0, 0, 255, 1)#blue
playerList[1]["type"] = "basic"

playerList[2]["startPos"] = (14,14)
playerList[2]["startDir"] = (0,-1)
playerList[2]["color"] = Color(255, 0, 0, 1)#Red
playerList[2]["type"] = "basic"

playerList[3]["startPos"] = (14,0)
playerList[3]["startDir"] = (-1, 0)
playerList[3]["color"] = Color(255, 0, 255, 1)#Cyan
playerList[3]["type"] = "basic"

LEVEL_LIST.append(dict())
LEVEL_LIST[level]["name"] = "Slow"
LEVEL_LIST[level]["description"] = "small, slow paced game with short tails"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 10
LEVEL_LIST[level]["speed"] = 5
LEVEL_LIST[level]["rows"] = 15
LEVEL_LIST[level]["cols"] = 15
LEVEL_LIST[level]["humanPlayer"] = 0

####################
#LEVEL 8
####################
level = 8

playerList = [dict(), dict(), dict(), dict()]
playerList[0]["startPos"] = (0,0)
playerList[0]["startDir"] = (0,1)
playerList[0]["color"] = Color(0, 255, 0, 1)#green
playerList[0]["type"] = "human"

playerList[1]["startPos"] = (0,29)
playerList[1]["startDir"] = (1,0)
playerList[1]["color"] = Color(0, 0, 255, 1)#blue
playerList[1]["type"] = "basic"

playerList[2]["startPos"] = (29,29)
playerList[2]["startDir"] = (0,-1)
playerList[2]["color"] = Color(255, 0, 0, 1)#Red
playerList[2]["type"] = "basic"

playerList[3]["startPos"] = (29,0)
playerList[3]["startDir"] = (-1, 0)
playerList[3]["color"] = Color(255, 0, 255, 1)#Cyan
playerList[3]["type"] = "basic"

LEVEL_LIST.append(dict())
LEVEL_LIST[level]["name"] = "Fast"
LEVEL_LIST[level]["description"] = "fast 4 player AI skirmish"
LEVEL_LIST[level]["playerList"] = playerList
LEVEL_LIST[level]["trailTurns"] = 20
LEVEL_LIST[level]["speed"] = 15
LEVEL_LIST[level]["rows"] = 30
LEVEL_LIST[level]["cols"] = 30
LEVEL_LIST[level]["humanPlayer"] = 0