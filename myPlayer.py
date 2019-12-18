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
        if self._mycolor == self._board._BLACK:
            return "Saucisse"
        else:
            return "BIM BAM BOUM"

    def getresult(self,color):
    
        if self._mycolor == color:
            return 1
        else:
            return -1

    def maxValue(self, alpha, beta,color,depth):
        if self._board.is_game_over():
            return self._board.end_heuristique1()
        if depth == 0:
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
        if self._board.is_game_over():
            return self._board.end_heuristique1()
        if depth == 0:
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

    def alphabeta(self,color, depth):
        tmp = []
        score = 0
        nbmoves = 0
        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-60000, 600000,color,depth)
            if not tmp:
                tmp = move
                score = res
                nbmoves = len(self._board.legal_moves())
            else:
                if res > score:
                    tmp = move
                    score = res
                    nbmoves = len(self._board.legal_moves())
                elif res==score:
                    nbtmp = len(self._board.legal_moves())
                    if nbtmp > nbmoves:
                        tmp = move
                        score = res
                        nbmoves = nbtmp
            self._board.pop()
            
        print("chosing move of score" + str(score))
        return  tmp
        

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        if self._mycolor == self._board._BLACK:
            (w,b) = self._board.get_nb_pieces()
            if w+b>89:
                move = self.alphabeta(self._mycolor,10)
            else:
                move = self.alphabeta(self._mycolor,3)
            
        elif self._mycolor == self._board._WHITE:
            moves = [m for m in self._board.legal_moves()]
            move = moves[randint(0,len(moves)-1)]
            (w,b) = self._board.get_nb_pieces()
            if w+b>89:
                move = self.alphabeta(self._mycolor,10)
            else:
                move = self.alphabeta(self._mycolor,3)
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



