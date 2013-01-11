#TRON by Taylor Poulos
#AndrewID: tpoulos
#email: poulos.taylor.w@gmail.com
#Created in Nov-Dec 2012
#15-112 Term Project

#Code to run a tron server
#Based on PodSixNet library by Chris McCormick
#URL: http://mccormick.cx/projects/PodSixNet/

####################
#IMPORTS
####################
from time import sleep, localtime
from weakref import WeakKeyDictionary
from time import time
import sys
import config

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

####################
#Channel
####################

#A class that represents the connection to a single client game
class TronChannel(Channel):
	def __init__(self, *args, **kwargs):
		Channel.__init__(self, *args, **kwargs)
	
	def Close(self):
		print self, 'Client disconnected'
	
	##################################
	# Game Specific Events
	##################################
	
	#These next four classes represent specific types of events
	#They are raised by the clients as four sepparate events
	#And are sent back to the players in a genneral game event class
	#They are split up so that in the future the server can respond in
	#More specific ways
	def Network_gameEnd(self, data):
		print "!! Game Over"
		self.sendGameEvent(data)

	def Network_gameStart(self, data):
		print "____________________________"
		print "GAME STARTING"
		print "############################"
		self.sendGameEvent(data)

	def Network_cycleTurn(self, data):
		print "@@ Cycle ", data["cycleNum"], " turned"
		self.sendGameEvent(data)

	def Network_cycleCrash(self, data):
		print "## Cycle ", data["cycleNum"], " crashed"
		self.sendGameEvent(data)

	#Sends the information back to the players as a general gameEvent action
	def sendGameEvent(self, rawData):
		data = rawData
		data["action"], data["gameEvent"] = "gameEvent", data["action"]
		self._server.SendToAll(data)

	#Adds a player to the server, and sends the information back to
	#The other players that a slot has been taken
	def Network_playerAdd(self, data):
		self._server.AddPlayer(data)
		
####################
#Server Class
####################

class TronServer(Server):
	channelClass = TronChannel
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = []
		print "____________________________"
		print 'Server Ready'
		print "############################"
	
	def AddPlayer(self, data):#Called when an AI is added by a player
		if(len(self.players) == config.MAX_PLAYERS):
			print "!! Game full"
		else:
			self.SendToAll({"action": "slotTaken", #If the server is not full
							"slotNumber": len(self.players)})
			#Add it to the list, but don't send it instructions
			#Because the AIs are just controlled by 
			#the player that creates them
			self.players.append([None])
			print "$$ AI connected"

	def Connected(self, channel, addr):#Called when a new client connects
		if(len(self.players) == config.MAX_PLAYERS):
			channel.Send({"action": "gameFull"})
			print channel, "!! Channel failed to connect"
		else:
			#Tells the player its slot number
			channel.Send({"action": "playerAdded", 
						  "slotNumber": len(self.players)})
			self.SendToAll({"action": "slotTaken",
				            "slotNumber": len(self.players)})
			self.players.append(channel)
			print "$$ Channel connected"

	def SendToAll(self, data):#Sends any piece of data to all players
		for player in self.players:
			if(player != [None]):#Skips any AI controlled players
				player.Send(data)
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.001)


####################
#Launching
####################

#Launches the server
s = TronServer(localaddr=("localhost", int(800)))
s.Launch()

