#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#These functions create the cycles on the board

####################
#IMPORTS
####################
import pygame
from pygame.locals import *
import config
import random

####################
#GameWindow Class
####################
#A GameWindow is the basic PyGame window the game sits in
class GameWindow(object):
	def __init__(self):
		self.mainClock = pygame.time.Clock()
		self.display = pygame.display.set_mode(config.SCREEN_SIZE)
		pygame.display.set_caption('Tron')
		pygame.mouse.set_visible(False)
		if(config.FULLSCREEN == True):
			#Makes the game fullscreen
			pygame.display.set_mode((config.WINDOW_WIDTH, 
									config.WINDOW_HEIGHT), 
									pygame.DOUBLEBUF | pygame.FULLSCREEN)
		self.initSounds()

	def initSounds(self):
		self.background = pygame.Surface(config.SCREEN_SIZE)
		self.mixer = pygame.mixer
		self.upSound = pygame.mixer.Sound("sounds/menu_up.ogg")
		self.upSound.set_volume(0.3)
		self.downSound = pygame.mixer.Sound("sounds/menu_down.ogg")
		self.downSound.set_volume(0.3)
		self.selectSound = pygame.mixer.Sound("sounds/menu_select.ogg")

####################
#GameSurface Class
####################
#A GameSurface is a surface the actual game is rendered on
class GameSurface(object):
	def __init__(self, window, top, left, pixelLength):
		#Marks the upper left of the game window
		self.top, self.left = top, left
		self.surface = pygame.Surface((pixelLength, pixelLength))
		self.sideLength = pixelLength
		self.margin = int(round(self.sideLength * config.OUTLINE_RATIO))
		self.window = window
		self.board = None

	def setBoard(self, board):#Sets the board to the game board
		#Because the game board is created slightly after the game surface
		self.board = board
		self.rows = board.rows
		self.cols = board.cols
		self.cellLength = self.sideLength / float(board.rows)
		cellFontSize =float(self.sideLength)/self.board.rows/config.CELL_SCALE
		self.cellFont = pygame.font.Font("fonts/cour.ttf", int(cellFontSize))
		cycleFontSize = cellFontSize*config.CYCLE_SCALE
		self.cycleFont = pygame.font.Font("fonts/cour.ttf",int(cycleFontSize))

	def redrawAll(self):#Redraws the board and all the cycles to the background
		self.window.background.fill(config.BACKGROUND_COLOR)
		self.drawMargin()
		for row in xrange(self.board.rows):#Draws the board
			for col in xrange(self.board.cols):
				self.drawCell(self.board.board[row][col])
		self.window.background.blit(self.surface, (self.top,self.left))
		self.window.display.blit(self.window.background, (0,0))
		pygame.display.flip()
		self.surface.fill(config.BACKGROUND_COLOR)#Fill the background color 
		#last, because the cycles draw before this function and if we fill it
		#at the beginning of the function the cycles are drawn over

	def drawMargin(self):#Draw an outline for the board
		pygame.draw.rect(self.surface, config.MARGIN_COLOR, 
			(0, 0, self.margin, self.sideLength))
		pygame.draw.rect(self.surface, config.MARGIN_COLOR, 
			(0, 0, self.sideLength, self.margin))
		pygame.draw.rect(self.surface, config.MARGIN_COLOR, 
			(0, self.sideLength - self.margin, 
				self.sideLength, self.sideLength))
		pygame.draw.rect(self.surface, config.MARGIN_COLOR, 
			(self.sideLength - self.margin, 0, 
				self.sideLength, self.sideLength))

	def updateDisplay(self):#A wrapper for the pygame update display class
		pygame.display.update()

	def drawCell(self, cell):#Draw each cel
		if(cell.turns > -1):
			cell.incrementTurns()
			x = int(round(cell.col*self.cellLength + 
				float(self.cellLength)/config.CELL_SCALE/2))
			y = int(round(cell.row*self.cellLength + 
				float(self.cellLength)/config.CELL_SCALE/2))
			for i in xrange(2):#Stacks 2 chars on top of eachother for looks
				trail = self.cellFont.render(
					self.randomCharacter(cell.direction), True, cell.color)
				self.surface.blit(trail, (x,y))

	#Give a random character based on what is being drawn
	def randomCharacter(self, type):
		if(type == "vertical"):
			return random.choice(config.VERTICAL_CHARACTERS)
		elif(type == "cycleUp"):
			return config.CYCLE_CHARACTERS[0]
		elif(type == "cycleDown"):
			return config.CYCLE_CHARACTERS[1]
		elif(type == "cycleLeft"):
			return config.CYCLE_CHARACTERS[2]
		elif(type == "cycleRight"):
			return config.CYCLE_CHARACTERS[3]
		elif(type == "cycleDead"):
			return config.CYCLE_CHARACTERS[4]
		else:
			return random.choice(config.HORIZONTAL_CHARACTERS)

	def drawCycle(self, cycle):#Draw the cycle
		cellPadding = float(self.cellLength)/config.CELL_SCALE/2
		cycleOffset = cellPadding*(config.CYCLE_SCALE/2)
		x = int(round(cycle.col*self.cellLength + cellPadding - cycleOffset))
		y = int(round(cycle.row*self.cellLength + cellPadding - cycleOffset))
		y -=  int(float(self.sideLength)/self.board.rows/
			config.CELL_SCALE*config.CYCLE_SCALE/8)
		if(cycle.isLive == True):
			if(cycle.drow == -1):#The cycle is moving up
				cycleImage = self.cycleFont.render(
					self.randomCharacter("cycleUp"), True, cycle.color)
			elif(cycle.drow == 1):#The cycle is moving down
				cycleImage = self.cycleFont.render(
					self.randomCharacter("cycleDown"), True, cycle.color)
			elif(cycle.dcol == -1):#The cycle is moving left
				#The characters we're using for left and right are a little 
				#shorter than the other characters therefore, we need to move
				#them up a little to compensate
				cycleImage = self.cycleFont.render(
					self.randomCharacter("cycleLeft"), True, cycle.color)
			elif(cycle.dcol == 1):#The cycle is moving right
				cycleImage = self.cycleFont.render(
					self.randomCharacter("cycleRight"), True, cycle.color)
		else:
			cycleImage = self.cycleFont.render(
				self.randomCharacter("cycleDead"), True, cycle.color)
		self.surface.blit(cycleImage, (x,y))