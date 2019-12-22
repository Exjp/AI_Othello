# -*- coding: utf-8 -*-

import sys
import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)     #the board we play on
        self._mycolor = None                #our colour
        self._ultra_instinct = False        #for the first time we see the end of the game
        self._flex = False                  #to annouce if we think we lose or we win
        self._nbmoves = 0                   #total number of moves
        self._nbtimewasted = 0              #number of moves on which we wasted time
        self._quotes = ["I am Groot","Everything is going as expected...", "You're a though opponent, but I still have tricks in my sleeve.",
         "And it makes BIM BAM BOUM!","Hoho, instead of running away, you're coming right to me?", "It makes PSHHH and it makes VROUM!!", "lol",
         "Want to have dinner after this?", "No way I'm losing now !", "\"When the sage points the moon, the idiot looks at the finger\".","The cake is a lie.", 
         "YOU. SHALL. NOT. PASS.", "It's over Anakin, I have the high ground!", "Yippee-ki-yay", "Hatsa la vista, baby","To infinity and beyond!","Try dodging this.",
         "Don't push it, or I'll give you a war you won't believe.","Kneel before me.", "I'll beat you. Not this turn, not the following turn... But I'll beat you.",
         "You know nothing, A.I. Snow.", "Winter is coming.", "PLUS ULTRRRAAAA!!", "My power is MAXIMUM!!", "Hodor.","Hodor?","HODOR!!","ok boomer.",
         "You're much stronger than you look.","Avengers... ASSEMBLE!","  :)","  :D","   :o", ":^)","  ^^","  :(","I love pizza. I mean, who doesn't?","Why so serious?",
         "No, Luke, I AM your father!", "Who's your daddy now?", "TEQUILA!", "My name is Bond, A.I. Bond", "Eenee-Minee-Mynee-Moe.","I don't even know what I'm doing",
         "This game is funny, what's its name again?", "I had a dream, in which I won this game.", "I understand EVERYTHING now !", "The prophecy is true.",
         "An A.I. has no name.", "Roses are red, violets are blue, at the end of the game, the loser will be YOU.", "I'm hungry.", "Have you turned the gas off?",
         "I play Pokemon Go everyday."]
                                            #a bunch of quotes we say during the game
        print("Hello, nice to meet you")    #we say hello because we're polite

#getter for our name    
    def getPlayerName(self):
        if self._mycolor == self._board._BLACK:
            return "Dark Knight"
        else:
            return "White Mage"

#getter for the result
    def getresult(self,color):
        if self._mycolor == color:
            return 1
        else:
            return -1

#approach 4: heuristic to call in case of a game_over, return high positive or negative value, depending on if we lose or win
    def end_heuristique4(self,player=None):
        score = (self._board._nbBLACK - self._board._nbWHITE)*5000
        if self._mycolor == self._board._WHITE:
            return -score
        return score

#function to give a score to each corner, to evaluate if the position is established or not
    def evalupleft(self,x,y):
        colmax = 9
        line =0
        color = self._board._board[x][y]
        score = 150
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
        score = 150
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
        score = 150
        while(colmax>=0 and line >= 0):
            for col in range(colmax+1):
                if self._board._board[line][col] != color:
                    colmax = col-1
                    break
                score +=50
            line-=1
        return score
    
    def evalbottomright(self,x,y):
        colmax = 0
        line =9
        color = self._board._board[x][y]
        score = 150
        while(colmax<=9 and line >=0):
            for col in range(9, colmax-1,-1):
                if self._board._board[line][col] != color:
                    colmax = col+1
                    break
                score +=50
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

#function to evaluate the cases around the corner  
    def evaluate_undercorner(self,x,y):
        if x<2:
            if y<2 and self._board._board[0][0] != self._board._EMPTY:
                return 0
            elif y> self._board._boardsize-3 and self._board._board[0][self._board._boardsize-1] != self._board._EMPTY:
                return 0
            else:
                if x==1 and y == 1 or x == 1 and y == self._board._boardsize-2:
                    return -150
                return -110
        else:
            if y<2 and self._board._board[self._board._boardsize-1][0] != self._board._EMPTY:
                return 0
            elif y> self._board._boardsize-3 and self._board._board[self._board._boardsize-1][self._board._boardsize-1] != self._board._EMPTY:
                return 0
            else:
                if x==self._board._boardsize-2 and y == 1 or x == self._board._boardsize-2 and y == self._board._boardsize-2:
                    return -150
                return -110

# our heuristic, to give a score for a board
    def heuristique(self, player=None):
        score = 0
        for x in range(self._board._boardsize):
            for y in range(self._board._boardsize):
                if self._board._board[x][y] is self._board._EMPTY:
                    continue
                point = 0
                if x == 0 or x == self._board._boardsize-1: 
                    if y==0 or y == self._board._boardsize-1:   #corners
                        point= self.evaluate_corner(x,y)
                    elif y==1 or y == self._board._boardsize-2: #undercorners
                        point= self.evaluate_undercorner(x,y)
                    elif y==2 or y == self._board._boardsize-3: 
                        point= 50                               #underundercorners on the horizontal sides
                    else:
                        point =20                               #horizontal sides
                elif x == 1 or x == self._board._boardsize-2:
                    if y<2 or y >self._board._boardsize-3:
                        point = self.evaluate_undercorner(x,y)  #undercorners
                    elif y==2 or y ==self._board._boardsize-3:
                        point=25                                #underundercorners
                    else:
                        point =-10                              #horizontal undersides
                elif x==2 or x== self._board._boardsize-3:
                    if y==0 or y==self._board._boardsize-1:
                        point = 50                              #underundercorners on the vertical sides
                    elif y<3 or y>self._board._boardsize-4:
                        point=25                                #underundercorners
                    else:
                        point=4                                 #half-centered cases
                else:
                    if y==0 or y == self._board._boardsize-1:
                        point= 20                               #vertical sides
                    elif y==1 or y == self._board._boardsize-2: 
                        point= -10                              #vertical undersides
                    elif y==2 or y == self._board._boardsize-3: 
                        point= 4                                #half-centerd cases
                    else:
                        point =3                                #other cases
                if self._board._board[x][y] is self._board._WHITE:
                    score-=point
                elif self._board._board[x][y] is self._board._BLACK:
                    score+=point
        if self._mycolor == self._board._WHITE:
            return -score
        return score

#maxValue function to determine the best move when it's our turn
    def maxValue(self, alpha, beta,color,depth,seconds,currentTime):
        if self._board.is_game_over():
            return self.end_heuristique4()
        if depth == 0:
            return self.heuristique()
        if time.time() - currentTime >= seconds:
            return -50000

        if not self._board.legal_moves():
            return minValue(alpha,beta,color, depth)
        for i in self._board.legal_moves():
            self._board.push(i)
            alpha = max(alpha, self.minValue(alpha, beta,color,depth - 1,seconds,currentTime))
            self._board.pop()
            if alpha >= beta:
                return beta

        return alpha

#minvalue function to determine the best move when it's the opponent turn
    def minValue(self, alpha, beta,color,depth, seconds,currentTime):
        if self._board.is_game_over():
            return self.end_heuristique4()
        if depth == 0:
            return self.heuristique()
        if time.time() - currentTime >= seconds:
            return -50000

        if not self._board.legal_moves():
            return maxValue(alpha,beta,color, depth)
        for i in self._board.legal_moves():
            self._board.push(i)
            beta = min(beta, self.maxValue(alpha, beta,color,depth - 1, seconds,currentTime))
            self._board.pop()
            if alpha >= beta:
                return alpha

        return beta

    
#alphabeta function, goes to a certain depth to find the best move to play, needs enough time to process
    def alphabeta(self,color, depth,seconds):
        tmp = []
        score = 0
        nbmoves = 0
        currentTime = time.time()
        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-600000, 600000,color,depth,seconds, currentTime)

            if not tmp:
                tmp = (move,res)
                score = res
                nbmoves = len(self._board.legal_moves())
            else:
                if res > score:
                    score = res
                    tmp = (move,res)
                    nbmoves = len(self._board.legal_moves())
                elif res==score:
                    nbtmp = len(self._board.legal_moves())

                    if nbtmp > nbmoves:
                        tmp = (move,res)
                        score = res
                        nbmoves = nbtmp
            self._board.pop()
        return  tmp

#iterative alphabeta, calls an alphabeta on every depth, until the time limit risks to be reached                
    def alphabetait(self,color,time_limit):
        startTime = time.time()
        seconds = time_limit
        depth = 2
        coup1 = None
        coup2 = None
        (w,b)= self._board.get_nb_pieces()


        while depth <= 100-(w + b):
            leftTime = seconds -  (time.time() - startTime)
            if coup1 is None:
                coup1 = self.alphabeta(color,depth,leftTime)
            else:
                coup2 = coup1
                coup1 = self.alphabeta(color,depth,leftTime)
            if coup1[1]>5000 or (time.time() - startTime > seconds*(14/100)):
                print("depth "+str(depth)+"   time "+str(time.time()-startTime)+"/"+str(seconds))
                if time.time() - startTime > seconds:
                    self._nbtimewasted+=1
                    print("score  "+str(coup2[1]))
                    return coup2[0]               
                print("score  "+str(coup1[1]))
                return coup1[0]
            depth += 1

#alphabeta to call at the end. Returns the first move that can lead to a win
    def end_alphabeta(self,color, depth,seconds):
        bestmove = None
        score = 0
        currentTime = time.time()
        for move in self._board.legal_moves():
            self._board.push(move)
            res = self.minValue(-600000, 600000,color,depth,seconds, currentTime)
            if res>0:
                bestmove=move
                score = res
                self._board.pop()
                break
            if not bestmove:
                bestmove = move
                score = res
            else:
                if res > score:
                    score = res
                    bestmove = move
            self._board.pop()
        if self._ultra_instinct and not self._flex:
            self._flex = True
            if res>0:
                print("Omaewa mo... shindeiru")
            elif res==0:
                print("Je peux voir le futur... Nous allons rejouer dans 1 minute")
            else:
                print("It was at this moment "+ self.getPlayerName() +" knew... he f***ed up")     
        return bestmove
        
#get a move from an iterative alphabeta strategy. Takes more or less time to think depending of the state of the game
    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        currentTime = time.time()
        print(self._quotes[randint(0,len(self._quotes)-1)])
        move = None
        moves = self._board.legal_moves()
        if len(moves)==1:
            print("I have only one option.")
            move = moves[0]
            self._board.push(move)
            self._nbmoves += 1
            return (move[1],move[2])
        num = moves[0][0]
        (w,b) = self._board.get_nb_pieces()
        if w+b<87:
            for x in range(2):
                for y in range(2):
                    move = [num,x*(self._board._boardsize-1),y*(self._board._boardsize-1)]
                    if move in moves:
                        self._board.push(move)
                        self._nbmoves += 1
                        return (move[1],move[2])
        if w+b>87:
            if not self._ultra_instinct:
                self._ultra_instinct = True
                print("this is it, i go full ultra instinct")
            move = self.end_alphabeta(self._mycolor,15,1000)
        elif w+b>64:
            move = self.alphabetait(self._mycolor,20)
        elif w+b>44:
            move = self.alphabetait(self._mycolor,15)
        elif w+b>24:
            move = self.alphabetait(self._mycolor,12)
        else:
            move = self.alphabetait(self._mycolor,8)
        self._board.push(move)
        self._nbmoves += 1
        (c,x,y) = move
        assert(c==self._mycolor)
        return (x,y) 

 #play the opponent move on our own board   
    def playOpponentMove(self, x,y):
        self._board.push([self._opponent, x, y])

#sets our color and our opponent's
    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

#print a little message at the end of the game. Also print the number of turn where time is wasted
    def endGame(self, winner):
        if self._mycolor == winner:
            print("Ha, that was easy ^^")
        elif winner == self._board._EMPTY:
            print("We are on the same level, let's get married")
        else:
            print("you're so full of talent it hurts")
        print("I, "+self.getPlayerName()+ ", wasted time on "+str(self._nbtimewasted)+"/"+str(self._nbmoves)+"moves")



