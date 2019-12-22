from DisplayBoard import *
import pygame
from pygame.locals import *
from random import randint

import Reversi
import myPlayer
import RandomPlayer
import humanPlayer
import myPlayerv0
import time
from io import StringIO
import sys


b = Reversi.Board(10)
player1 = None
player2 = None
while True:
    plays = input("enter players (r, i, i2, z, or h)\n")
    plays2 = plays.split()
    if len(plays2)==2:
        if plays2[0] == "r":
            player1 = RandomPlayer.RandomPlayer()
        elif plays2[0] == "i":
            player1 = myPlayer.myPlayer()
        elif plays2[0] == "h":
            player1 = humanPlayer.humanPlayer()
        elif plays2[0] == "i2":
            player1 = myPlayerv0.myPlayer()
        elif plays2[0] == "z":
            player1 = humanPlayer.clickerPlayer()
        if plays2[1] == "r":
            player2 = RandomPlayer.RandomPlayer()
        elif plays2[1] == "i":
            player2 = myPlayer.myPlayer()
        elif plays2[1] == "h":
            player2 = humanPlayer.humanPlayer()
        elif plays2[1] == "i2":
            player2 = myPlayerv0.myPlayer()
        elif plays2[1] == "z":
            player2 = humanPlayer.clickerPlayer()
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
rand = int(input("how many random moves?\n"),10)

while not b.is_game_over():
    
    print("\n\n\nBefore move", nbmoves)
    print("Legal Moves: ", b.legal_moves())
    nbmoves += 1
    otherplayer = (nextplayer + 1) % 2
    othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
    
    currentTime = time.time()
    sys.stdout = stringio
    if rand>0:
        moves = [m for m in b.legal_moves()]
        movee = moves[randint(0,len(moves)-1)]
        players[nextplayer]._board.push(movee)
        move = (movee[1],movee[2])
        rand-=1
        time.sleep(0.25)
    else:
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
    (nbwhites, nbblacks) = b.get_nb_pieces()
    print("nbblacks :" + str(nbblacks) + "    nbwhites :" + str(nbwhites))
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
    player1.endGame(b._WHITE)
    player2.endGame(b._WHITE)
elif nbblacks > nbwhites:
    print("BLACK")
    player1.endGame(b._BLACK)
    player2.endGame(b._BLACK)
else:
    print("DEUCE")
print("nbblacks :" + str(nbblacks) + "    nbwhites :" + str(nbwhites))
input("press enter to end")

endDisplay()

sys.exit()
