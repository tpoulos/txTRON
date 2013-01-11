[txTRON](https://github.com/tpoulos/txTRON)
===========================================
_It's like snake, but with motorcycles and lasers_


Background
----------
txTRON was originally created in the winter of 2012 as a term project for 15-112, 
Fundamentals of Programming, at Carnegie Mellon University.
Since then I have added several improvements, such as a better
menu system and some enhanced AI behaviors.


Features
--------
txTRON contains many advanced features, such as:

*	Multiple game modes, including adjustable game-speed, tail length, AI type and number, board size and starting positions.
*	three types of AI, including:
	*	Basic - Two behaviors create this simple AI: Taking a random turn every few (randomly chosen) moves, and always taking a move which will not crash unless no other option is available.
	*	LineLook - LineLook AI is the same as the Basic AI, except that instead of choosing a random safe move when the AI is about to crash, it choses the move with where it can travel the farthest without crashing.
	*	Avoider - Avoider AI always selects the move with the longest free travel distance.
*	Multi-player support through the library PodSixNet
*	Animated menu system
*	Support for all screen sizes in landscape mode
*	An entirely text based interface

To install and run:
-------------------
*	Install [Python 2.7.*](http://www.python.org/download/) and [pygame](http://www.pygame.org/download.shtml) (PodSixNet is included with the source)
*	run RUN_txTRON.py

To run networking:
------------------
*	run tron_server.py on the computer you wish to use as the host.
*	change the variable SERVER_IP in config.py to the IP of the server (or "localhost" if on the same machine as the server)
*	Run RUN_txTRON.py
*	enter networking tab to reserve a spot
*	Press spacebar on any computer to add an AI
*	Press enter on any computer to begin the game


For questions or comments email:
<poulos.taylor.w@gmail.com>