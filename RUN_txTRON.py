#txTRON by Taylor Poulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012


####################
#IMPORTS
####################
import pygame
from pygame.locals import *
import config
import random
import sys
import tron_game
import tron_client
import gui

####################
#Tron Class
####################
#creates and runs a tron menu system
class Tron(object):
	def run(self):
		pygame.init()
		pygame.mixer.init()
		self.window = gui.GameWindow()
		self.background = pygame.Surface(config.SCREEN_SIZE)
		self.init()
		self.menu = IntroAnimation(self.background, self.newMenu, self.window)
		self.menu = MainMenu(self.background, self.newMenu, self.window)
		while(True):
			self.listenForMenuEvents()
			self.redrawAll()
        	self.window.mainClock.tick(config.MENU_FRAMERATE)

	def redrawAll(self):
		pygame.display.flip()
		self.background.fill(config.BACKGROUND_COLOR)
		self.menu.draw()
		self.window.display.blit(self.background, (0,0))

	def newMenu(self, MenuType):
		self.menu = MenuType(self.background, self.newMenu, self.window)

	def init(self):
		pass

	def listenForMenuEvents(self):
		for event in pygame.event.get():#Runs through and mouse events
			if event.type == QUIT:#Quits the game
				pygame.quit()
				sys.exit()
			if(event.type == KEYDOWN):
  				if event.key == 27:#The escape key
					pygame.quit()
					sys.exit()  
				if event.key == K_UP:
					self.menu.scrollUp()
				if event.key == K_DOWN:
					self.menu.scrollDown()
				if (event.key == K_SPACE):
					#Interacting is sometimes different than selecting, 
					#but often the same, so they are sepparate, but sometimes
					#Interact just calls select
					self.menu.interact()
				if (event.key == K_RETURN):
					self.menu.select()
				if (event.key == K_BACKSPACE):
					self.menu.newMenu(MainMenu)
####################
#Menu Class
####################
#A general class the creates a menu
class Menu(object):
	def __init__(self, surface, newMenu, window):
		self.window = window
		self.newMenu = newMenu
		self.surface = surface
		self.width = config.WINDOW_WIDTH
		self.height = config.WINDOW_HEIGHT
		self.menuItems = [None]
		self.cursorPosition = 0
		pygame.font.init()
		self.minDimension = min(config.WINDOW_HEIGHT, config.WINDOW_WIDTH)

		self.screenBlink = 0 #Screen blink is a way of adding some animation to the menus
		#When the blink is zero, all of the menu items are displayed
		#When something on the interface moves, the items are displayed only after
		#A certain number of frames

		self.title = pygame.font.Font("fonts/cour.ttf", int(float(self.minDimension)/config.TITLE_RATIO))
		self.headding = pygame.font.Font("fonts/cour.ttf", int(float(self.minDimension)/config.HEADDING_RATIO))
		self.text = pygame.font.Font("fonts/cour.ttf", int(float(self.minDimension)/config.TEXT_RATIO))

		self.init()

	def init(self):#Overwritten by the menu classes
		pass

	def scrollUp(self):#Move the currently selected menu item up by one
		self.cursorPosition -= 1
		if(self.cursorPosition < 0):
			self.cursorPosition = len(self.menuItems) - 1
			self.playUpSound()

	def scrollDown(self):#Move the currently selected menu item down by one
		self.cursorPosition += 1
		if(self.cursorPosition > len(self.menuItems) - 1):
			self.cursorPosition = 0
			self.playDownSound()

	def select(self):#Run whatever behavior is bound to the menu item
		self.menuItems[self.cursorPosition]["activate"]()
		self.playSelectSound()

	def draw(self):#This function is overwritten by the menu specific layout
		pass

	def interact(self):#Interact is often the same as select, however the option is left to different menus to use a different behavior
		self.select()

	def menuItem(self, text, type, centerLine, selected):
		#Renders a title in the supplied font, on the supplied center line
		#Contains a flag for making the text the current selected menu item
		if(selected == True):
			text = "-" + text + "-"
		title = type.render(text, True, config.MENU_COLOR)
		self.surface.blit(title, ( (self.width - title.get_width())/2.0, 
						           self.height*centerLine - title.get_height()/2.0))

	def startCountDown(self, afterCount):
		background = pygame.Surface(config.SCREEN_SIZE)
		for i in ["3", "2", "1", "GO"]:
			background.fill(config.BACKGROUND_COLOR)
			title = self.title.render(str(i), True, config.MENU_COLOR)#Renders the current number of seconds remaining
			background.blit(title, ((self.width - title.get_width())/2, self.height/2 - title.get_height()/2))#Places the number in the middle of the screen
			self.window.display.blit(background, (0,0))
			self.window.mainClock.tick(1)#Waits 1 second
			pygame.display.flip()
		afterCount()

	def randomizeText(self, text, targetText = None):
		if(targetText == None):
			targetText = len(text)*"a"
		for i in xrange(len(targetText)):
			if(text[i] != targetText[i]):
				text = text[:i] + random.choice(config.HORIZONTAL_CHARACTERS + config.VERTICAL_CHARACTERS + targetText[i]) + text[i+1:]
		return text

	def playMenuMusic(self):
		self.window.mixer.music.stop()
		self.window.mixer.music.load("sounds/music_menu.ogg")
		self.window.mixer.music.play(-1)

	def playGameMusic(self):
		self.window.mixer.music.stop()
		self.window.mixer.music.load("sounds/music_game.ogg")
		self.window.mixer.music.play(-1)

	def fadeOutMusic(self, time):
		pygame.mixer.music.fadeout(time)

	def playDownSound(self):
		self.window.downSound.play()

	def playUpSound(self):
		self.window.upSound.play()

	def playSelectSound(self):
		self.window.selectSound.play()

####################
#Intro Class
####################
#Creates an intro animation
class IntroAnimation(Menu):

	def init(self):
		self.playMenuMusic()
		self.startIntro()

	def startIntro(self):
		text = "ASDFGH"
		targetText = "txTRON"
		while(text != targetText):
			self.surface.fill(config.BACKGROUND_COLOR)
			for i in xrange(2):
				text = self.randomizeText(text, targetText = targetText)
				self.menuItem(text, self.title, 1.0/3.0, False)
			self.window.display.blit(self.surface, (0,0))
			pygame.display.flip()
			self.window.mainClock.tick(config.MENU_FRAMERATE)



####################
#MainMenu Class
####################
#Specifically creates the Main Menu
class MainMenu(Menu):
	def init(self):#Initializes the menu options
		self.cursorPosition = 0
		self.menuItems = [dict(), dict(), dict()]
		self.menuItems[0]["activate"] = self.displayInstructions
		self.menuItems[1]["activate"] = self.runLevel
		self.menuItems[2]["activate"] = self.runMultiplayer

	def displayInstructions(self):
		self.newMenu(Instructions)

	def runLevel(self):
		self.newMenu(LevelSelect)

	def runMultiplayer(self):
		self.newMenu(MultiplayerMenu)

	def draw(self):
		if(self.screenBlink > 0):
			self.screenBlink -= 1
		self.drawMainMenu(self.cursorPosition)


	def drawMainMenu(self, selected):
		self.menuItem("txTRON", self.title, 1.0/3.0, False)
		if(self.screenBlink > 3*config.BLINKFRAMES/4.0):#Draw only the selected item
			if(selected == 0):
				self.menuItem("Instructions", self.headding, 7.0/12.0, 0 == selected)
			if(selected == 1):
				self.menuItem("Level Selection", self.headding, 8.0/12.0, 1 == selected)
			if(selected == 2):
				self.menuItem("Multiplayer", self.headding, 9.0/12.0, 2 == selected)
		elif(self.screenBlink > 0):#Draw the selected item, with the others scrambled
			if(selected == 0):
				self.menuItem("Instructions", self.headding, 7.0/12.0, 0 == selected)
			else:
				self.menuItem(self.randomizeText("Instructions"), self.headding, 7.0/12.0, 0 == selected)
			if(selected == 1):
				self.menuItem("Level Selection", self.headding, 8.0/12.0, 1 == selected)
			else:
				self.menuItem(self.randomizeText("Level Selection"), self.headding, 8.0/12.0, 1 == selected)
			if(selected == 2):
				self.menuItem("Multiplayer", self.headding, 9.0/12.0, 2 == selected)
			else:
				self.menuItem(self.randomizeText("Multiplayer"), self.headding, 9.0/12.0, 2 == selected)
		else:
			self.menuItem("Instructions", self.headding, 7.0/12.0, 0 == selected)
			self.menuItem("Level Selection", self.headding, 8.0/12.0, 1 == selected)
			self.menuItem("Multiplayer", self.headding, 9.0/12.0, 2 == selected)


	def scrollUp(self):#Move the currently selected menu item up by one
		self.playUpSound()
		self.screenBlink = config.BLINKFRAMES
		self.cursorPosition -= 1
		if(self.cursorPosition < 0):
			self.cursorPosition = len(self.menuItems) - 1

	def scrollDown(self):#Move the currently selected menu item down by one
		self.playDownSound()
		self.screenBlink = 100
		self.cursorPosition += 1
		if(self.cursorPosition > len(self.menuItems) - 1):
			self.cursorPosition = 0

####################
#LevelSelect Class
####################
#Specifically creates the Level selection screen
class LevelSelect(Menu):
	def init(self):
		self.scrollDirection = "up"
		self.levels = config.LEVEL_LIST

	def scrollUp(self):
		self.playUpSound()
		self.screenBlink = config.BLINKFRAMES
		self.scrollDirection = "up"
		self.cursorPosition -= 1
		if(self.cursorPosition < 0):
			self.cursorPosition = len(self.levels) - 1

	def scrollDown(self):
		self.playDownSound()
		self.screenBlink = config.BLINKFRAMES
		self.scrollDirection = "down"
		self.cursorPosition += 1
		if(self.cursorPosition >= len(self.levels)):
			self.cursorPosition = 0

	def select(self):
		self.playSelectSound()
		self.playGameMusic()
		self.startCountDown(self.launchLevel)

	def launchLevel(self):#Launches the actual game level inside a surface
		level = self.levels[self.cursorPosition]
		sideLength = 9*config.WINDOW_HEIGHT/10
		#The board is 9/10ths of the size of the screen,
		# so almost filling the screen top to bottom
		top = 1*config.WINDOW_HEIGHT/20
		#The board is lowered so that it is equally bordered on 
		#the top and bottom
		left = (config.WINDOW_WIDTH - sideLength)/2
		#The same is done for the left offset
		surface = gui.GameSurface(self.window, left, top, sideLength)
		rows = level["rows"]
		cols = level["cols"]
		speed = level["speed"]
		window = self.window
		trailTurns = level["trailTurns"]
		playerList = level["playerList"]
		player = level["humanPlayer"]
		game = tron_game.TronGame(rows, cols, speed, window, surface, 
			trailTurns, playerList, humanPlayer = player)
		self.winScreen(game.winner, player)

	def winScreen(self, winner, player):
	#Flashes a screen to tell the player who won
		if(winner.playerNumber == player):
			text =  "Win: Human Player"
		else:
			text = "Win: AI"
		background = pygame.Surface(config.SCREEN_SIZE)
		background.fill(config.BACKGROUND_COLOR)
		title = self.headding.render(text, True, config.MENU_COLOR)
		background.blit(title, ((self.width - title.get_width())/2, 
			self.height*0.5 - title.get_height()/2))
		self.window.display.blit(background, (0,0))
		pygame.display.flip()
		self.fadeOutMusic(1)
		self.window.mainClock.tick(1)#Waits 1 second
		pygame.event.get()
		self.playMenuMusic()

	def draw(self):
		self.screenBlink -= 1
		self.menuItem("select the level from the list below", self.text, 1.0/5.0, False)
		self.menuItem(self.levels[self.cursorPosition]["name"], self.headding, 1.0/2.0, True)#The current level's name, selected
		if(self.screenBlink > 3.0*config.BLINKFRAMES/4.0):
			pass#Draw nothing
		elif(self.screenBlink > 0):
			self.menuItem(self.randomizeText(self.levels[self.cursorPosition]["description"]), self.headding, 4.0/5.0, False)#A description of the currently selected level
			if(self.scrollDirection == "down"):
				self.menuItem(self.randomizeText(self.levels[self.cursorPosition - 1]["name"]), self.text, 2.0/5.0, False)#The previous level's name
			if(self.scrollDirection == "up"):
				tempCursorPosition = (self.cursorPosition + 1) % len(self.levels) #The next level's name
				self.menuItem(self.randomizeText(self.levels[tempCursorPosition]["name"]), self.text, 3.0/5.0, False)
		else:
			self.menuItem(self.levels[self.cursorPosition]["description"], self.headding, 4.0/5.0, False)#A description of the currently selected level
			self.menuItem(self.levels[self.cursorPosition - 1]["name"], self.text, 2.0/5.0, False)#The previous level's name
			tempCursorPosition = (self.cursorPosition + 1) % len(self.levels) #The next level's name
			self.menuItem(self.levels[tempCursorPosition]["name"], self.text, 3.0/5.0, False)


####################
#Multiplayer Menu Class
####################
#Specifically creates the multiplayer screen
class MultiplayerMenu(Menu):
	def init(self):#Assigns multiplayer specific information
		self.client = tron_client.TronClient(config.SERVER_IP, int(800))

		self.aiPlayer = dict()
		self.aiPlayer["name"] = "AI"
		self.aiPlayer["type"] = "ai"

		self.otherPlayer = dict()
		self.otherPlayer["name"] = "foreign"
		self.otherPlayer["type"] = "other"

		self.localPlayer = dict()
		self.localPlayer["name"] = "player"
		self.localPlayer["type"] = "local"

		self.nonePlayer = dict()
		self.nonePlayer["name"] = "empty"
		self.nonePlayer["type"] = "empty"

		self.players = [self.nonePlayer, self.nonePlayer, self.nonePlayer, self.nonePlayer]

		self.emptySlot = 0
		self.slot = None

	def draw(self):
		self.handleNetworkEvents()

		self.menuItem("add an AI with space", self.headding, 1.0/5.0, False)
		self.menuItem(self.players[0]["name"], self.text, 3.0/10.0, False)
		self.menuItem(self.players[1]["name"], self.text, 4.0/10.0, False)
		self.menuItem(self.players[2]["name"], self.text, 5.0/10.0, False)
		self.menuItem(self.players[3]["name"], self.text, 6.0/10.0, False)
		self.menuItem("enter to start game", self.headding, 4.0/5.0, False)

	def select(self):#On pressing enter, start the game
		self.playSelectSound()
		self.startGame()

	def interact(self):#On pressing space, add an ai to the list of players
		self.playSelectSound()
		if(self.emptySlot >= config.MAX_PLAYERS):
			print "server full"
		elif(self.players[self.emptySlot]["type"] == "empty"):
			self.addAI()

	def startGame(self):#Send a message to start the game
		#Don't actually start the game, we will do that 
		#when we recieve the message from the server to start it
		self.client.gameStart()

	def addAI(self):#Add an AI to the list of players
		self.players[self.emptySlot] = self.aiPlayer
		self.emptySlot += 1
		self.client.addAI()

	def understandGameState(self, event):
	#Translate server events into menu events
		if(event["action"] == "playerAdded"):
			if(self.players[event["slotNumber"]]["type"] == "other"):
			#This means the slot is already filled
				print "problem"
			elif(self.players[event["slotNumber"]]["type"] == "empty"):
			#If the slot is empty, fill it
				self.players[event["slotNumber"]] = self.localPlayer
				self.slot = event["slotNumber"]
				if(self.slot != 0):#If we are not in the first slot, 
				#then other people have claimed the other ones already]
					for slot in xrange(self.slot):
						self.players[slot] = self.otherPlayer
				self.emptySlot = self.slot + 1#Increment the current slot

		if(event["action"] == "slotTaken"):
			if(self.players[event["slotNumber"]]["type"] == "ai"):
				pass
			#This means the slot is filled with an AI
			elif(self.players[event["slotNumber"]]["type"] == "other"):
			#This means the slot is already filled
				print "problem"
			elif(self.players[event["slotNumber"]]["type"] == "empty"):
			#If the slot is empty, fill it
				self.players[event["slotNumber"]] = self.otherPlayer
				self.emptySlot += 1#Increment the current empty slot

		if(event["action"] == "gameEvent"):
			if(event["gameEvent"] == "gameStart"):
				self.startCountDown(self.launchLevel)

	def launchLevel(self):
		self.playGameMusic()
		level = config.NETWORKED_LEVEL
		sideLength = 9*config.WINDOW_HEIGHT/10#The board is 9/10ths of the 
		#size of the screen, so almost filling the screen top to bottom
		top = 1*config.WINDOW_HEIGHT/20#The board is lowered so that it is 
		#equally bordered on the top and bottom
		left = (config.WINDOW_WIDTH - sideLength)/2
		#The same is done for the left offset
		surface = gui.GameSurface(self.window, left, top, sideLength)
		rows = level["rows"]
		cols = level["cols"]
		speed = level["speed"]
		window = self.window
		trailTurns = level["trailTurns"]
		playerList = level["playerList"]
		for i in xrange(len(playerList)):
			if((self.players[i]["type"] == "empty") or 
				(self.players[i]["type"] == "local") or 
				(self.players[i]["type"] == "other")):
				playerList[i]["type"] = "local"#This type of cycle will only 
				#respond to networked events, not create any networked events
				#Therefore, if no player or AI is supplied, this type works 
				#well, because it will just travel straight into a wall
				#It also works well for a human player, because a human 
				#player's turns are sent from the keylistener
			elif(self.players[i]["type"] == "ai"):
				playerList[i]["type"] = "networked ai"
				#network is short for networked AI
		game = tron_game.NetworkedTronGame(rows, cols, speed, window, 
			surface, trailTurns, playerList, self.client, 
			humanPlayer = self.slot)
		self.newMenu(MainMenu)

	def handleNetworkEvents(self):
		self.client.pump()#Handle the client's events
		events = self.client.callGameEvents()
		for event in events:
			self.understandGameState(event);

####################
#Instructions Class
####################
#Displays and interacts with the instructions
class Instructions(Menu):
	def init(self):
		self.instructions = config.INSTRUCTIONS
		self.pages = len(self.instructions)

	def draw(self):
		if(self.screenBlink > 0):
			self.screenBlink -= 1
		if(self.screenBlink < config.BLINKFRAMES/4.0):
			self.menuItem(self.instructions[self.cursorPosition], self.text, 1.0/2.0, False)
		elif(self.screenBlink < 3.0*config.BLINKFRAMES/4.0):
			text = self.randomizeText(self.instructions[self.cursorPosition])
			self.menuItem(text, self.text, 1.0/2.0, False)

	def backToMain(self):
		self.newMenu(MainMenu)

	def scrollUp(self):
		self.screenBlink = config.BLINKFRAMES
		self.playUpSound()
		self.cursorPosition -= 1
		if(self.cursorPosition < 0):
			self.backToMain()

	def scrollDown(self):
		self.screenBlink = config.BLINKFRAMES
		self.playDownSound()
		self.cursorPosition += 1
		if(self.cursorPosition == self.pages):
			self.backToMain()

	def select(self):
		self.scrollDown()

#Runs the game when selected
if __name__ == '__main__':
    app = Tron()
    app.run()