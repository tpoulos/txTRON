#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#Code to run a tron client
#Based on PodSixNet library by Chris McCormick
#URL: http://mccormick.cx/projects/PodSixNet/

####################
#IMPORTS
####################
import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener


####################
#Client
####################
class TronClient(ConnectionListener):

	def __init__(self, host, port):
		self.Connect((host, port))
		self.gameEvents = []#A Queue of the events since the last game cycle
	
	####################
	#Game Events
	####################
	#A general class of events that pertain to changed game information
	def Network_gameEvent(self, data):
		try:
			self.gameEvents.append(data)
		except:
			print "Error when appending data"
			print data

	def callGameEvents(self):#Returns the game events which have been taking
		#Place since the last time this function was called
		recentGameEvents = self.gameEvents
		self.gameEvents = []
		return recentGameEvents

	def turn(self, cycleNum, drow, dcol):
		connection.Send({"action": "cycleTurn", "cycleNum": cycleNum,
					     "drow": drow, "dcol": dcol})

	def crash(self, cycleNum):
		connection.Send({"action": "cycleCrash", "cycleNum": cycleNum})

	def gameOver(self):
		connection.Send({"action": "gameEnd"})

	####################
	#Network Lobby
	####################
	#Events that happen while setting up the networked game

	def Network_slotTaken(self, data):
		self.gameEvents.append(data)

	def Network_playerAdded(self, data):
		self.gameEvents.append(data)

	def gameStart(self):
		connection.Send({"action": "gameStart"})

	def addAI(self):
		connection.Send({"action": "playerAdd"})

	####################
	#built in commands
	####################
	def Network_connected(self, data):
		pass
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()

	def Network_disconnected(self, data):
		pass

	def pump(self):#Moves along the data. Called twice per game loop
		connection.Pump()
		self.Pump()

