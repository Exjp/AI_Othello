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

    def maxValue(self, alpha, beta,color,depth):
        if self._board.is_game_over() or depth == 0:
            res = self._board.heuristique()
            return res

        if not self._board.legal_moves():
            return minValue(alpha,beta,color, depth)
        for i in self._board.legal_moves():
            self._board.push(i)
            alpha = max(alpha, self.minValue(alpha, beta, color,depth - 1))
            self._board.pop()
            if alpha >= beta:
                return beta

        return alpha

    def minValue(self, alpha, beta,color,depth):
        if self._board.is_game_over() or depth == 0:
            res = self._board.heuristique()
            return res
        if not self._board.legal_moves():
            return maxValue(alpha,beta,color, depth)
        for i in self._board.legal_moves():
            self._board.push(i)

            beta = min(beta, self.maxValue(alpha, beta,color,depth - 1))
            self._board.pop()
            if alpha >= beta:
                return alpha
        
        return beta

    def alphabeta(self,color):
        better = -1
        tmp = []
        score = 0

        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-60000, 600000,color,4)
            self._board.pop()
            if not tmp:
                tmp = move
                score = res
            else:
                if res > score:
                    tmp = move
                    score = res
                elif res <= 0:
                    if len(tmp) == 0:
                        tmp = move
                elif res == 0 and better -1:
                    better = 0
                    tmp = move
        print("chosing move of score" + str(score))
        return  tmp
        

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        if self._mycolor == self._board._BLACK:
            move = self.alphabeta(self._mycolor)
        elif self._mycolor == self._board._WHITE:
            moves = [m for m in self._board.legal_moves()]
            move = moves[randint(0,len(moves)-1)]
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        #print(self._board)
        #time.sleep(2)
        return (x,y) 

    
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



