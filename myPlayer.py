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

    #approche 1: simplement retourner le nombre de jeton
    def end_heuristique1(self, player=None):
        if player is None:
            player = self._board._board._nextPlayer
        if player is self._board._WHITE:
            return self._board._nbWHITE
        return self._board._nbBLACK

    #approche 2: retourner le résultat (à appeler en fin de partie)
    def end_heuristique2(self, player=None):
        if player is None:
            player = self._board._nextPlayer
        winner = 1
        if self._board._nbWHITE > self._board._nbBLACK:
            winner = -1
        elif self._board._nbWHITE == self._board._nbBLACK:
            winner = 0
        if player is self._board._WHITE:
            return -winner
        return winner

    
    def evaluate_undercorner(self,x,y,player):
        if x<2:
            if y<2 and self._board._board[0][0] != self._board._EMPTY:
                return 10
            elif y> self._board._boardsize-3 and self._board._board[0][self._board._boardsize-1] != self._board._EMPTY:
                return 10
            else:
                return -100
        else:
            if y<2 and self._board._board[self._board._boardsize-1][0] != self._board._EMPTY:
                return 10
            elif y> self._board._boardsize-3 and self._board._board[self._board._boardsize-1][self._board._boardsize-1] != self._board._EMPTY:
                return 10
            else:
                return -100
    # Exemple d'heuristique : evaluer le board entier selon les bords
    def heuristique(self, player=None):
        if player is None:
            player = self._board._nextPlayer
        score = 0
        for x in range(self._board._boardsize):
            for y in range(self._board._boardsize):
                if self._board._board[x][y] is self._board._EMPTY:
                    continue
                point = 0
                if x == 0 or x == self._board._boardsize-1:
                    if y==0 or y == self._board._boardsize-1:
                        point=75
                    if y==1 or y == self._board._boardsize-2:
                        point= self.evaluate_undercorner(x,y,player)
                    else:
                        point =10
                elif y==0 or y == self._board._boardsize-1:
                    if x== 1 or x == self._board._boardsize-2:
                        point = self.evaluate_undercorner(x,y,player)
                    else:
                        point =10
                elif x==1 or x== self._board._boardsize-2:
                    if y==1 or y==self._board._boardsize-2:
                        point=self.evaluate_undercorner(x,y,player)
                else:
                    point+=1
                if self._board._board[x][y] is self._board._WHITE:
                    score-=point
                elif self._board._board[x][y] is self._board._BLACK:
                    score+=point
        #if player is self._WHITE:
        #    score *= -1 
        return score

    # Exemple d'heuristique simple : compte simplement les pieces et valoriser les coins
    def heuristique01(self, player=None):
        if player is None:
            player = self._board._board._nextPlayer
        corners = 0
        for x in range(2):
            for y in range(2):
                if self._board[x*(self._board._boardsize-1)][y*(self._board._boardsize-1)] is self._board_WHITE:
                    corners -= 50
                    print("corner "+str(x)+" "+str(y)+" can be white")
                elif self._board._board[x*(self._board._boardsize-1)][y*(self._board._boardsize-1)] is self._board._BLACK:
                    corners+= 50
                    print("corner "+str(x)+" "+str(y)+" can be black")
        #if player is self._WHITE:
        #    return self._nbWHITE - self._nbBLACK - corners 
        return self._board._nbBLACK - self.board._nbWHITE + corners

    # Exemple d'heuristique tres simple : compte simplement les pieces
    def heuristique0(self, player=None):
        if player is None:
            player = self._board._nextPlayer
        if player is self._board._WHITE:
            return self._board._nbWHITE - self._board._nbBLACK
        return self._board._nbBLACK - self._board._nbWHITE


    def maxValue(self, alpha, beta,color,depth,seconds):
        if self._board.is_game_over() or depth == 0 or (time.time() - seconds >= 5):
            res = self.heuristique()
            return res

        if not self._board.legal_moves():
            return minValue(alpha,beta,color, depth)
        for i in self._board.legal_moves():
            self._board.push(i)
            alpha = max(alpha, self.minValue(alpha, beta,color,depth - 1,seconds))
            self._board.pop()
            if alpha >= beta:
                return beta

        return alpha

    def minValue(self, alpha, beta,color,depth, seconds):
        if self._board.is_game_over() or depth == 0 or (time.time() - seconds >= 5):
            res = self.heuristique()
            return res
        if not self._board.legal_moves():
            return maxValue(alpha,beta,color, depth)
        for i in self._board.legal_moves():
            self._board.push(i)
            beta = min(beta, self.maxValue(alpha, beta,color,depth - 1, seconds))
            self._board.pop()
            if alpha >= beta:
                return alpha
        
        return beta

    def alphabeta(self,color):
        better = -1
        tmp = []
        score = 0
        seconds = time.time()
        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-100000, 1000000,color,4,seconds)
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
                    score = res
                elif res <= 0:
                    if len(tmp) == 0:
                        tmp = move
                elif res == 0 and better -1:
                    better = 0
                    tmp = move
        print("time it takes to choose a moove = ",(time.time() - seconds))
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



