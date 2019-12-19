from DisplayBoard import *
import pygame
from pygame.locals import *

import Reversi
import myPlayer
import RandomPlayer
import humanPlayer
import time
from io import StringIO
import sys

b = Reversi.Board(10)
player1 = None
player2 = None
while True:
    plays = input("enter player (r, i, or h)\n")
    plays2 = plays.split()
    if len(plays2)==2:
        if plays2[0] == "r":
            player1 = RandomPlayer.RandomPlayer()
        elif plays2[0] == "i":
            player1 = myPlayer.myPlayer()
        elif plays2[0] == "h":
            player1 = humanPlayer.humanPlayer()
        if plays2[1] == "r":
            player2 = RandomPlayer.RandomPlayer()
        elif plays2[1] == "i":
            player2 = myPlayer.myPlayer()
        elif plays2[1] == "h":
            player2 = humanPlayer.humanPlayer()
        if player1 is not None and player2 is not None:
            break

players = []
player1.newGame(b._WHITE)
player2.newGame(b._BLACK)
players.append(player2)
players.append(player1)

totalTime = [0,0] # total real time for each player
nextplayer = 0

mytime = 0

nextplayercolor = b._BLACK
nbmoves = 1
displayBoard(b)
outputs = ["",""]
sysstdout= sys.stdout
stringio = StringIO()
print(b.legal_moves())
while not b.is_game_over():
    
    print("Before move", nbmoves)
    print("Legal Moves: ", b.legal_moves())
    nbmoves += 1
    otherplayer = (nextplayer + 1) % 2
    othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
    
    currentTime = time.time()
    sys.stdout = stringio
    move = players[nextplayer].getPlayerMove()
    sys.stdout = sysstdout
    playeroutput = "\r" + stringio.getvalue()
    stringio.truncate(0)
    print(("[Player "+str(nextplayer+1) + "] ").join(playeroutput.splitlines(True)))
    outputs[nextplayer] += playeroutput
    totalTime[nextplayer] += time.time() - currentTime
    print("Total time for this player : ",totalTime[nextplayer])
    print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays" + str(move))
    (x,y) = move
    if not b.is_valid_move(nextplayercolor,x,y):
        print(otherplayer, nextplayer, nextplayercolor)
        print("Problem: illegal move")
        break
    b.push([nextplayercolor, x, y])
    players[otherplayer].playOpponentMove(x,y)

    nextplayer = otherplayer
    nextplayercolor = othercolor
    displayBoard(b)
    
print("The game is over")
print(b)
(nbwhites, nbblacks) = b.get_nb_pieces()
print("Time:", totalTime)
print("Winner: ", end="")
if nbwhites > nbblacks:
    print("WHITE")
elif nbblacks > nbwhites:
    print("BLACK")
else:
    print("DEUCE")
print("nbblacks :" + str(nbblacks) + "    nbwhites :" + str(nbwhites))
input("press enter to end")
endDisplay()

sys.exit()