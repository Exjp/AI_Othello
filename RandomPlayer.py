import Reversi
from random import randint
from playerInterface import *
import time

class RandomPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "R4ND0M"

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
        move = moves[randint(0,len(moves)-1)]
        time.sleep(0.5) 
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
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



