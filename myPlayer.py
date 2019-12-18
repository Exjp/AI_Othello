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

    def maxValue(self, alpha, beta,depth,seconds):
        if self._board.is_game_over() or depth == 0 or (time.time() - seconds >= 5):
            res = self._board.heuristique()
            return res


        for i in self._board.legal_moves():
            self._board.push(i)
            alpha = max(alpha, self.minValue(alpha, beta,depth - 1,seconds))
            self._board.pop()
            if alpha >= beta:
                return beta

        return alpha

    def minValue(self, alpha, beta,depth, seconds):
        if self._board.is_game_over() or depth == 0 or (time.time() - seconds >= 5):
            res = self._board.heuristique()
            return res

        for i in self._board.legal_moves():
            self._board.push(i)
            beta = min(beta, self.maxValue(alpha, beta,depth - 1, seconds))
            self._board.pop()
            if alpha >= beta:
                return alpha
        
        return beta

    def alphabeta(self):
        better = -1
        tmp = []
        score = 0
        seconds = time.time()
        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-100000, 1000000,4,seconds)
            self._board.pop()
            if not tmp:
                print("MOVE =============== ",move)
                print("RES ============ ",res)
                tmp = move
                score = res
            else:
                print("MOVE =============== ",move)
                print("RES ============ ",res)
                if res > score:
                    score = res
                    tmp = move
                elif res <= 0:
                    if len(tmp) == 0:
                        tmp = move
                elif res == 0 and better -1:
                    better = 0
                    tmp = move
        print("time it takes to choose a moove = ",(time.time() - seconds))
        return  tmp
        

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        if self._mycolor == self._board._BLACK:
            move = self.alphabeta()
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



