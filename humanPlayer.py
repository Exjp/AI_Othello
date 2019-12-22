import Reversi
from random import randint
from playerInterface import *
import pygame
from pygame.locals import *
import myPlayer
import time
import sys

class humanPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self.ai = myPlayer.myPlayer()

    def getPlayerName(self):
        return "the chosen one"

    def getresult(self,color):
    
        if self._mycolor == color:
            return 1
        else:
            return -1

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
        num = moves[0][0]
        while True:
            txt = input()
            if txt == "a":
                move = moves[randint(0,len(moves)-1)]
                break
            if txt == "" or txt == "ia":
                movee = self.ai.getPlayerMove()
                move = (num,movee[0],movee[1])
                break
            play = txt.split()
            if len(play)!=2:
                continue
            move = [num,int(play[0],10),int(play[1],10)]
            if move in moves:
                break
        print("chosing move of score " + str(self.ai.heuristique()))
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        return (x,y) 

    
    def playOpponentMove(self, x,y):
        self._board.push([self._opponent, x, y])
        self.ai.playOpponentMove(x,y)

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2
        self.ai.newGame(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


class clickerPlayer(PlayerInterface):
    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self.ai = myPlayer.myPlayer()

    def getPlayerName(self):
        return "the chosen one"

    def getresult(self,color):
    
        if self._mycolor == color:
            return 1
        else:
            return -1

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
        num = moves[0][0]
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    movee = self.ai.getPlayerMove()
                    move = (num,movee[0],movee[1])
                    break
                if event.button ==1:
                    pos = pygame.mouse.get_pos()
                    move = [num,int(pos[0]/(getsizegame()/10)),int(pos[1]/(getsizegame()/10))]
                    if move in moves:
                        self.ai._board.push(move)
                        break
                    print("your move is invalid")
                if event.button == 2:
                    print("exit")
                    sys.exit()
        print("chosing move of score " + str(self.ai.heuristique()))
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        return (x,y) 

    
    def playOpponentMove(self, x,y):
        self._board.push([self._opponent, x, y])
        self.ai.playOpponentMove(x,y)

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2
        self.ai.newGame(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
    
