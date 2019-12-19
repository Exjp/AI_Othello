# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._ulta_instinct = False
        self._flex = False
        self._mytime = time.time()
        self._nbmoves = 0
        self._quotes = ["I am Groot","Everything is going as expected...", "You're a though opponent, but I still have tricks in my sleeve.", "And it makes BIM BAM BOUM!",
         "Hoho, instead of running away, you're coming right to me?", "It makes PSHHH and it makes VROUM!!", "lol", "Want to have dinner after this?",
         "No way I'm losing now !", "\"When the sage points the moon the idiot looks at the finger\".","The cake is a lie.", "YOU. SHALL. NOT. PASS.",
         "It's over Anakin, I have the high ground!", "Yippee-ki-yay", "Hatsa la vista, baby","To infinity and beyond!","Try dodging this.",
         "Don't push it, or I'll give you a war you won't believe.","Kneel before me.", "I'll beat you. Not this turn, not the following turn... But I'll beat you.",
         "You know nothing, A.I. Snow.", "Winter is coming.", "PLUS ULTRRRAAAA!!", "My power is MAXIMUM!!", "Hodor.","Hodor?","HODOR!!",]
        print("Hello, nice to meet you")
        self._heuristiquetab = [
            [100 ,-50 ,40  ,10  ,10  ,10  ,10  ,40  ,-50 ,100 ],
            [-50 ,-100,25  ,-10 ,-10 ,-10 ,-10 ,25  ,-100,-50 ],
            [40  ,25  ,25  ,6   ,6   ,6   ,6   ,25  ,25  ,40  ],
            [10  ,-10 ,6   ,5   ,5   ,5   ,5   ,6   ,-10 ,10  ],
            [10  ,-10 ,6   ,5   ,5   ,5   ,5   ,6   ,-10 ,10  ],
            [10  ,-10 ,6   ,5   ,5   ,5   ,5   ,6   ,-10 ,10  ],
            [10  ,-10 ,6   ,5   ,5   ,5   ,5   ,6   ,-10 ,10  ],
            [40  ,25  ,25  ,6   ,6   ,6   ,6   ,25  ,25  ,40  ],
            [-50 ,-100,25  ,-10 ,-10 ,-10 ,-10 ,25  ,-100,-50 ],
            [100 ,-50 ,40  ,10  ,10  ,10  ,10  ,40  ,-50 ,100 ]]

    def getPlayerName(self):
        if self._mycolor == self._board._BLACK:
            return "Dark Knight"
        else:
            return "White Mage"

    def getresult(self,color):
        if self._mycolor == color:
            return 1
        else:
            return -1

    #approche 1: simplement retourner le nombre de jeton
    def end_heuristique1(self, player=None):
        if self._mycolor == self._board._WHITE:
            return self._board._nbWHITE
        return self._board._nbBLACK

    #approche 2: retourner le résultat (à appeler en fin de partie)
    def end_heuristique2(self, player=None):
        if player is None:
            player = self._board._nextPlayer
        winner = 1000
        if self._board._nbWHITE > self._board._nbBLACK:
            winner = -1000
        elif self._board._nbWHITE == self._board._nbBLACK:
            winner = 0
        if self._mycolor == self._board._WHITE:
            return -winner
        return winner

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

    def heuristique11(self,player=None):
        #self.update_heuristique()
        score = 0 
        for x in range(self._board._boardsize):
            for y in range(self._board._boardsize):

                if self._board._board[x][y] is self._board._EMPTY:
                    continue

                point = self._heuristiquetab[x][y]
                #point += self.evaluate_corner(x,y)

                if self._board._board[x][y] is self._board._WHITE:
                    score-=point
                elif self._board._board[x][y] is self._board._BLACK:
                    score+=point

        if self._mycolor == self._board._WHITE:
            return -score
        return score


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

    # Exemple d'heuristique simple : compte simplement les pieces et valoriser les coins
    def heuristique01(self, player=None):
        corners = 0
        for x in range(2):
            for y in range(2):
                if self._board[x*(self._board._boardsize-1)][y*(self._board._boardsize-1)] is self._board_WHITE:
                    corners -= 50
                    print("corner "+str(x)+" "+str(y)+" can be white")
                elif self._board._board[x*(self._board._boardsize-1)][y*(self._board._boardsize-1)] is self._board._BLACK:
                    corners+= 50
                    print("corner "+str(x)+" "+str(y)+" can be black")
        score = self._board._nbBLACK - self.board._nbWHITE + corners
        if self._mycolor == self._board._WHITE:
            return -score
        return score

    # Exemple d'heuristique tres simple : compte simplement les pieces
    def heuristique0(self, player=None):
        score = self._board._nbBLACK - self._board._nbWHITE
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
        if self._ulta_instinct and not self._flex:
            self._flex = True
            if score>0:
                print("Omaewa mo... shindeiru")
            elif score==0:
                print("Je peuc voir le futur... Nous allons rejouer dans 1 minute")
            else:
                print("It was at this moment "+ self.getPlayerName() +" knew... he f***ed up")
        return  tmp
        
    def update_heuristique(self):
        if self._board._board[0][0] != self._board._EMPTY:
            self._heuristiquetab[0][1] = 15
            self._heuristiquetab[1][0] = 15
            self._heuristiquetab[1][1] = 15
        else:
            self._heuristiquetab[0][1] = -50
            self._heuristiquetab[1][0] = -50
            self._heuristiquetab[1][1] = -100
        if self._board._board[0][self._board._boardsize-1] != self._board._EMPTY:
            self._heuristiquetab[0][self._board._boardsize-2] = 25
            self._heuristiquetab[1][self._board._boardsize-1] = 25
            self._heuristiquetab[1][self._board._boardsize-2] = 15
        else:
            self._heuristiquetab[0][self._board._boardsize-2] = -50
            self._heuristiquetab[1][self._board._boardsize-1] = -50
            self._heuristiquetab[1][self._board._boardsize-2] = -100
        if self._board._board[self._board._boardsize-1][0] != self._board._EMPTY:
            self._heuristiquetab[self._board._boardsize-2][0] = 25
            self._heuristiquetab[self._board._boardsize-1][1] = 25
            self._heuristiquetab[self._board._boardsize-2][1] = 15
        else:
            self._heuristiquetab[self._board._boardsize-2][0] = -50
            self._heuristiquetab[self._board._boardsize-1][1] = -50
            self._heuristiquetab[self._board._boardsize-2][1] = -100
        if self._board._board[self._board._boardsize-1][self._board._boardsize-1] != self._board._EMPTY:
            self._heuristiquetab[self._board._boardsize-2][self._board._boardsize-1] = 25
            self._heuristiquetab[self._board._boardsize-1][self._board._boardsize-2] = 25
            self._heuristiquetab[self._board._boardsize-2][self._board._boardsize-2] = 15
        else:
            self._heuristiquetab[self._board._boardsize-2][self._board._boardsize-1] = -50
            self._heuristiquetab[self._board._boardsize-1][self._board._boardsize-2] = -50
            self._heuristiquetab[self._board._boardsize-2][self._board._boardsize-2] = -100
        
        for x in range(3,self._board._boardsize-3):
            if self._board._board[x][0] != self._board._EMPTY:
                self._heuristiquetab[x][1] = 7
            else:
                self._heuristiquetab[x][1] = -10
            if self._board._board[x][self._board._boardsize-1] != self._board._EMPTY:
                self._heuristiquetab[x][self._board._boardsize-2] = 7
            else:
                self._heuristiquetab[x][self._board._boardsize-2] = -10
        for y in range(3,self._board._boardsize-3):
            if self._board._board[0][y] != self._board._EMPTY:
                self._heuristiquetab[1][y] = 7
            else:
                self._heuristiquetab[1][y] = -10
            if self._board._board[self._board._boardsize-1][y] != self._board._EMPTY:
                self._heuristiquetab[self._board._boardsize-2][y] = 7
            else:
                self._heuristiquetab[self._board._boardsize-2][y] = -10


    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        
        (w,b) = self._board.get_nb_pieces()
        if w+b>88:
            if not self._ulta_instinct:
                self._ulta_instinct = True
                print("this is it, i go full ultra instinct")
            move = self.alphabeta(self._mycolor,20)
        elif w+b>45:
            if (time.time() - self._mytime) / self._nbmoves < 12 :
                move = self.alphabeta(self._mycolor,4)
            else:
                print("no time to think !!")
                move = self.alphabeta(self._mycolor,3)
            #print(self._quotes[randint(0,len(self._quotes)-1)])
        else:
            move = self.alphabeta(self._mycolor,3)
        self._board.push(move)
        self._nbmoves += 1
        (c,x,y) = move
        assert(c==self._mycolor)
        return (x,y) 

    
    def playOpponentMove(self, x,y):
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("Ha, that was easy ^^")
        elif winner == self._EMPTY:
            print("We are on the same level, let's get married")
        else:
            print("you're so full of talent it hurts")



