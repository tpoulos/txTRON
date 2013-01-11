#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#Config file, contains game constants and level information

####################
#IMPORTS
####################
from pygame.locals import *#Needed for color class
import levels

####################
#Level Information
####################
LEVEL_LIST = levels.LEVEL_LIST#Makes the information from the level file
NETWORKED_LEVEL = levels.NETWORKED_LEVEL#A little more accessable

####################
#Instructions
####################
INSTRUCTIONS = [#The instructions from the tutorial
				"space to continue",
				"arrows to steer",
				"esc to exit",
				"don't run into the walls",
				"don't run into each other",
				"<---end instructions--->"
				]

####################
#Screen Resolution
####################
#The game will display in any resolution that is wider than long
#But for Fullscreen to work propperly, your screen's pixel count 
#must be enterd. The windowed version is the safer option

import Tkinter
root = Tkinter.Tk()
FULLSCREEN = True
WINDOW_WIDTH = root.winfo_screenwidth()
WINDOW_HEIGHT = root.winfo_screenheight()
SCREEN_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

####################
#Menu Options
####################
BLINKFRAMES = 70
MENU_FRAMERATE = 20
MENU_COLOR = Color(255,255,255,1)#White

TITLE_RATIO = 4#The ratio of the window height to the text height
HEADDING_RATIO = 20#the same ratio as above, this time for headdings
TEXT_RATIO = 26#The same, but for text

####################
#Game Display
####################
BACKGROUND_COLOR = Color(0, 0, 0, 1)#Black
BLANK_COLOR = Color(0, 0, 0, 1)#Black
MARGIN_COLOR = Color(50, 50, 50, 1)#grey

OUTLINE_RATIO = 0.005#The ratio of the screen width to the outline
CELL_SCALE = 1.6#The size the text is in relation to the cell containing it
CYCLE_SCALE = 3#The number of times the cycles are bigger than the tails

#The cycle sprites, up, down, left, right, and dead respectivly
CYCLE_CHARACTERS = "AV<>O"
#Vaugly horizontal characters for the horizontal lines
HORIZONTAL_CHARACTERS = "-~^@*=+tw'xz#xzq#"
#Vaugly vertical characters for the vertical lines
VERTICAL_CHARACTERS = "!$()|[]{}IiT/\17tjLl;:?"

####################
#Server
####################
#The server can support an arbitrarally large number of players
#But for the convenience of creating a usable menu
#I decided to limit the server size to four
MAX_PLAYERS = 4
SERVER_IP = "localhost"

####################
#Game Constants
####################
#The possible moves a cycle can go in at any time
POSSIBLE_MOVES = [(1,0), (0,1), (-1,0), (0,-1)]
RANDOM_PERCENT = 0.75#The percentage of the time the AI makes a random move