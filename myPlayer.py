# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Saucisse"

    def getresult(self,color):
    
        if self._mycolor == color:
            return 1
        else:
            return -1

    def getresult(self,color):
        if self._mycolor == color:
            return 1
        else:
            return -1
    
    def maxValue(self, alpha, beta,color,depth):
        if self._board.is_game_over() or depth == 0:
            res = self._board.heuristique()
            #res = self.getresult(color)
            return res


        for i in self._board.legal_moves():
            #print("i de maxvalue = ",i)
            self._board.push(i)
            alpha = max(alpha, self.minValue(alpha, beta, color,depth - 1))
            self._board.pop()
            if alpha >= beta:
                return beta

        return alpha

    def minValue(self, alpha, beta,color,depth):
        if self._board.is_game_over() or depth == 0:
            res = self._board.heuristique()
            #res = self.getresult(color)
            return res

        for i in self._board.legal_moves():
            #print("i de minvalue = ",i)
            self._board.push(i)
            beta = min(beta, self.maxValue(alpha, beta,color,depth - 1))
            self._board.pop()
            if alpha >= beta:
                return alpha
        
        return beta

    def getPlayerMove(self):
        
        better = -1
        tmp = []

        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-100, 100,self._mycolor,3)
            self._board.pop()
            (c,x,y) = move
            if res > 0:
                return (x,y)
            elif res <= 0:
                if len(tmp) == 0:
                    tmp = (x,y)
            elif res == 0 and better -1:
                better = 0
                tmp = (x,y)

        return  tmp

    
    def playOpponentMove(self, x,y):
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



