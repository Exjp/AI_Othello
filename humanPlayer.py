import Reversi
from random import randint
from playerInterface import *
import time

class humanPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "the chosen one"

    def getresult(self,color):
    
        if self._mycolor == color:
            return 1
        else:
            return -1
#approche 3: retourner le nombre de jeton si on gagne, et une val négative si on perd
    def end_heuristique3(self,player=None):
        score = 0
        if self._board._nbWHITE > self._board._nbBLACK:
            if self._mycolor == self._board._WHITE:
                return 100*self._board._nbWHITE
            return (-10000)+10*self._board._nbBLACK
        elif self._board._nbWHITE < self._board._nbBLACK:
            if self._mycolor == self._board._WHITE:
                return (-10000)+10*self._board._nbWHITE
            return 100*self._board._nbBLACK
        else:
            return 0

    def evalupleft(self,x,y):
        colmax = 9
        line =0
        color = self._board._board[x][y]
        score = 50
        while(colmax>=0 and line < 10):
            for col in range(colmax+1):
                if self._board._board[line][col] != color:
                    colmax = col-1
                    break
                score+=50
            line+=1
        return score
    
    def evalupright(self,x,y):
        colmax = 0
        line =0
        color = self._board._board[x][y]
        score = 50
        while(colmax<=9 and line < 10):
            for col in range(9,colmax-1,-1):
                if self._board._board[line][col] != color:
                    colmax = col+1
                    break
                score +=50
            line+=1
        return score
    
    def evalbottomleft(self,x,y):
        colmax = 9
        line =9
        color = self._board._board[x][y]
        score = 50
        while(colmax>=0 and line >= 0):
            for col in range(colmax+1):
                if self._board._board[line][col] != color:
                    colmax = col-1
                    break
            line-=1
        return score
    
    def evalbottomright(self,x,y):
        colmax = 0
        line =9
        color = self._board._board[x][y]
        score = 50
        while(colmax<=9 and line >=0):
            for col in range(9, colmax-1,-1):
                if self._board._board[line][col] != color:
                    colmax = col+1
                    break
            line-=1
        return score
    
    

    def evaluate_corner(self,x,y):
        if x == 0:
            if y==0:
                return self.evalupleft(x,y)
            elif y == self._board._boardsize-1:
                return self.evalupright(x,y)
        elif x == self._board._boardsize-1:
            if y==0:
                return self.evalbottomleft(x,y)
            elif y== self._board._boardsize-1:
                return self.evalbottomright(x,y)
        return 0
    
    def evaluate_undercorner(self,x,y):
        if x<2:
            if y<2 and self._board._board[0][0] != self._board._EMPTY:
                return 5
            elif y> self._board._boardsize-3 and self._board._board[0][self._board._boardsize-1] != self._board._EMPTY:
                return 5
            else:
                if x==1 and y == 1 or x == 1 and y == self._board._boardsize-2:
                    return -100
                return -50
        else:
            if y<2 and self._board._board[self._board._boardsize-1][0] != self._board._EMPTY:
                return 5
            elif y> self._board._boardsize-3 and self._board._board[self._board._boardsize-1][self._board._boardsize-1] != self._board._EMPTY:
                return 5
            else:
                if x==self._board._boardsize-2 and y == 1 or x == self._board._boardsize-2 and y == self._board._boardsize-2:
                    return -100
                return -50

# Exemple d'heuristique : evaluer le board entier selon les bords
    def heuristique(self, player=None):
        score = 0
        for x in range(self._board._boardsize):
            for y in range(self._board._boardsize):
                if self._board._board[x][y] is self._board._EMPTY:
                    continue
                point = 0
                if x == 0 or x == self._board._boardsize-1: #coins
                    if y==0 or y == self._board._boardsize-1:
                        point= self.evaluate_corner(x,y)
                    elif y==1 or y == self._board._boardsize-2: #sous coins
                        point= self.evaluate_undercorner(x,y)
                    elif y==2 or y == self._board._boardsize-3: #sous sous coins
                        point= 30
                    else:
                        point =20 # bords horizontaux
                elif x == 1 or x == self._board._boardsize-2:
                    if y<2 or y >self._board._boardsize-3:
                        point = self.evaluate_undercorner(x,y) #sous coins
                    elif y==2 or y ==self._board._boardsize-3:
                        point=25
                    else:
                        point =-10 #sous bords horizontaux
                elif x==2 or x== self._board._boardsize-3:
                    if y==0 or y==self._board._boardsize-1:
                        point = 30
                    elif y<3 or y>self._board._boardsize-4:
                        point=25 #sous coins
                else:
                    if y==0 or y == self._board._boardsize-1:
                        point= 20
                    elif y==1 or y == self._board._boardsize-2: #sous coins
                        point= -10
                    elif y==2 or y == self._board._boardsize-3: #sous sous coins
                        point= 6
                    else:
                        point =5
                if self._board._board[x][y] is self._board._WHITE:
                    score-=point
                elif self._board._board[x][y] is self._board._BLACK:
                    score+=point
        if self._mycolor == self._board._WHITE:
            return -score
        return score

    def maxValue(self, alpha, beta,color,depth,seconds):
        if self._board.is_game_over():
            return self.end_heuristique3()
        if depth == 0 or (time.time() - seconds >= 100):
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
        if self._board.is_game_over():
            return self.end_heuristique3()
        if depth == 0 or (time.time() - seconds >= 100):
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

    def alphabeta(self,color, depth):
        tmp = []
        score = 0
        nbmoves = 0
        seconds = time.time()
        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-600000, 600000,color,depth,seconds)

            if not tmp:
                tmp = move
                score = res
                nbmoves = len(self._board.legal_moves())
            else:
                if res > score:
                    score = res
                    tmp = move
                    score = res
                    nbmoves = len(self._board.legal_moves())
                elif res==score:
                    nbtmp = len(self._board.legal_moves())
                    if nbtmp < nbmoves:
                        tmp = move
                        score = res
                        nbmoves = nbtmp
            self._board.pop()
                
        print("time it takes to choose a move = ",(time.time() - seconds))
        print("chosing move of score " + str(score))
        return  tmp

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = [m for m in self._board.legal_moves()]
        num = moves[0][0]
        print(num)
        while True:
            txt = input()
            if txt == "a":
                moves = [m for m in self._board.legal_moves()]
                move = moves[randint(0,len(moves)-1)]
                break
            if txt == "":
                move = self.alphabeta(self._mycolor,4)
                break
            play = txt.split()
            if len(play)!=2:
                continue
            if play[0] == "ia":
                move = self.alphabeta(self._mycolor,int(play[1],10))
                break
            move = [num,int(play[0],10),int(play[1],10)]
            if move in self._board.legal_moves():
                break
        print("chosing move of score " + str(self.heuristique()))
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



