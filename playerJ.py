import time
import Reversi
from random import randint
from playerInterface import *
import math

class playerJ(PlayerInterface):
    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._opponent=None
    # Returns your player name, as to be displayed during the game
    def getPlayerName(self):
        return "Jean Bombeur"

    def _num_valid_moves(self,me):
        count=0
        for i in range(0,10):
            for j in range(0,10):
                if(self._board.lazyTest_ValidMove(me,i,j)):
                    count+=1
        return count

    # def _ouverture(self):
    #         # pieces = []
    #         # for x in range(0,self._boardsize):
    #         #     for y in range(0,self._boardsize):
    #         if self._board.is_valid_move(1,6,4):
    #             m = (1,6,4)
    #         elif self._board.is_valid_move(1,3,6):
    #             m = (1,3,6)
    #         elif self._board.is_valid_move(1,3,5):
    #             m = (1,3,5)
    #         elif self._board.is_valid_move(1,3,4):
    #             m = (1,3,4)
    #         elif self._board.is_valid_move(1,6,3):
    #             m = (1,6,3)
    #         elif self._board.is_valid_move(1,5,3):
    #             m = (1,5,3)
    #         elif self._board.is_valid_move(1,6,5):
    #             m = (1,6,5)
    #         elif self._board.is_valid_move(1,6,2):
    #             m = (1,6,2)
    #         elif self._board.is_valid_move(1,5,6):
    #             m = (1,5,6)
    #         elif self._board.is_valid_move(1,7,5):
    #             m = (1,7,5)
    #         return m
    
    def _heuristic(self):
        is_game_over=0
        if self._board.is_game_over():
            (w,b)=self._board.get_nb_pieces()
            if self._mycolor==1:
                if b>w :
                    is_game_over=10000
                else:
                    is_game_over=-10000
            else:
                if w>b :
                    is_game_over=10000
                else:
                    is_game_over=-10000

# Coin Parity Heuristic Value =
# 	100 * (Max Player Coins - Min Player Coins ) / (Max Player Coins + Min Player Coins)
        max_player_coins=0
        min_player_coins=0
        for i in range (0,10):
            for j in range (0,10):
                if self._board._board[i][j]==self._mycolor:
                    max_player_coins+=1
                elif self._board._board[i][j]==self._opponent:
                    min_player_coins+=1
        coin_parity_value=100*(max_player_coins-min_player_coins)/(max_player_coins+min_player_coins)
# if ( Max Player Moves + Min Player Moves != 0)
# 	Mobility Heuristic Value =
# 		100 * (Max Player Moves - Min Player Moves) / (Max Player Moves + Min Player Moves)
# else
# 	Mobility Heuristic Value = 0
        mobility_heuristic_value=0
        my_tiles=self._num_valid_moves(1)
        opp_tiles=self._num_valid_moves(2)
        if my_tiles+opp_tiles!=0:
            mobility_heuristic_value=100*(my_tiles-opp_tiles)/(my_tiles+opp_tiles)


        get_corner=self._board.testAndBuild_ValidMove(self._opponent,0,0)
        if get_corner:
            # anti_corner_opp-=100
            return -1000

        get_corner=self._board.testAndBuild_ValidMove(self._opponent,9,9)
        if get_corner:
            # anti_corner_opp-=100
            return -1000


        get_corner=self._board.testAndBuild_ValidMove(self._opponent,0,9)
        if get_corner:
            # anti_corner_opp-=100
            return -1000

        get_corner=self._board.testAndBuild_ValidMove(self._opponent,9,0)
        if get_corner:
            # anti_corner_opp-=100
            return -1000

        get_corner=self._board.testAndBuild_ValidMove(self._mycolor,0,0)
        if get_corner:
            return 1000


        get_corner=self._board.testAndBuild_ValidMove(self._mycolor,9,9)
        if get_corner:
            return 1000


        get_corner=self._board.testAndBuild_ValidMove(self._mycolor,0,9)
        if get_corner:
            return 1000


        get_corner=self._board.testAndBuild_ValidMove(self._mycolor,9,0)
        if get_corner:
            return 1000

# if ( Max Player Corners + Min Player Corners != 0)
# 	Corner Heuristic Value =
# 		100 * (Max Player Corners - Min Player Corners) / (Max Player Corners + Min Player Corners)
# else
# 	Corner Heuristic Value = 0
        corner_heuristic_value=0
        my_corners=0
        opp_corners=0
        if self._board._board[0][0]==self._mycolor:
            my_corners+=1
        elif self._board._board[0][0]==self._opponent:
            opp_corners+=1
        if self._board._board[0][9]==self._mycolor:
            my_corners+=1
        elif self._board._board[0][9]==self._opponent:
            opp_corners+=1
        if self._board._board[9][0]==self._mycolor:
            my_corners+=1
        elif self._board._board[9][0]==self._opponent:
            opp_corners+=1
        if self._board._board[9][9]==self._mycolor:
            my_corners+=1
        elif self._board._board[9][9]==self._opponent:
            opp_corners+=1

        if my_corners+opp_corners!=0:
            corner_heuristic_value=100*(my_corners-opp_corners)/(my_corners+opp_corners)

# if ( Max Player Stability Value + Min Player Stability Value != 0)
# 	Stability  Heuristic Value =
# 		100 * (Max Player Stability Value - Min Player Stability Value) / (Max Player Stability Value + Min Player Stability Value)
# else
# 	Stability Heuristic Value = 0
        stability_heuristic_value=0
        my_tiles=0
        opp_tiles=0
        for i in range (0,10):
            for j in range (0,10):
                T=[]
                if self._board._board[i][j]==self._mycolor:
                    for k in range(i-1,i+1):
                        for l in range(j-1,j+1):
                            if k>=0 or k<10 and l>=0 or l<10:
                                T=T+[self._board.testAndBuild_ValidMove(self._opponent,k,l)]
                elif self._board._board[i][j]==self._opponent:
                    for k in range(i-1,i+1):
                        for l in range(j-1,j+1):
                            if k>=0 or k<10 and l>=0 or l<10:
                                T=T+[self._board.testAndBuild_ValidMove(self._opponent,k,l)]
                b=0
                if T!=False:
                    for p in range(0,len(T)):
                        if T[p]==[i,j]:
                            if self._board._board[i][j]==self._mycolor:
                                my_tiles-=1
                            elif self._board._board[i][j]==self._opponent:
                                opp_tiles-=1
                            b=1
                    if b==0:
                        if self._board._board[i][j]==self._mycolor:
                            my_tiles+=1
                        elif self._board._board[i][j]==self._opponent:
                            opp_tiles+=1
                else:
                    if self._board._board[i][j]==self._mycolor:
                        my_tiles+=1
                    elif self._board._board[i][j]==self._opponent:
                        opp_tiles+=1
        if my_tiles+opp_tiles!=0:
            stability_heuristic_value=100*(my_tiles-opp_tiles)/(my_tiles+opp_tiles)
        (w,b)=self._board.get_nb_pieces()
        if w+b>=90:
            return coin_parity_value+mobility_heuristic_value+stability_heuristic_value+is_game_over
        return coin_parity_value+mobility_heuristic_value+100*corner_heuristic_value+stability_heuristic_value+is_game_over

    def _MaxValue(self,alpha,beta,length,start_time):
        if length==0 or time.time()-start_time>6:
            return self._heuristic()
        if self._board.is_game_over():
            return self._heuristic()
        for a in self._board.legal_moves():
            self._board.push(a)
            alpha=max(alpha,self._MinValue(alpha,beta,length-1,start_time))
            self._board.pop()
            if alpha>=beta:
                return beta
        return alpha

    def _MinValue(self,alpha,beta,length,start_time):
        if length==0 or time.time()-start_time>6:
            return self._heuristic()
        if self._board.is_game_over():
            return self._heuristic()
        for a in self._board.legal_moves():
            self._board.push(a)
            beta=min(beta,self._MaxValue(alpha,beta,length-1,start_time))
            self._board.pop()
            if beta<=alpha:
                return alpha
        return beta

    # Returns your move. The move must be a couple of two integers,
    # Which are the coordinates of where you want to put your piece
    # on the board. Coordinates are the coordinates given by the Reversy.py
    # methods (e.g. validMove(board, x, y) must be true of you play '(x,y)')
    # You can also answer (-1,-1) as "pass". Note: the referee will never
    # call your function if the game is over
    def getPlayerMove(self):
        MaxDepth=13
        start_time=time.time()

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        maximum=-math.inf
        movemax=None
        for i in range(2,MaxDepth):
            if time.time()-start_time>6:
                break
            for m in self._board.legal_moves():
                self._board.push(m)
                (c,x,y) = m
                if x==1 and y==1:
                    tmp=-1000
                elif x==1 and y==8:
                    tmp=-1000
                elif x==8 and y==1:
                    tmp=-1000
                elif x==8 and y==8:
                    tmp=-1000
                else:
                    tmp=self._MaxValue(-math.inf,math.inf,i-1,start_time)
                if maximum<=tmp:
                    movemax=m
                    maximum=tmp
                self._board.pop()
        (c,x,y) = movemax
        self._board.push(movemax)
        return (x,y)


    # Inform you that the oponent has played this move. You must play it
    # with no search (just update your local variables to take it into account)
    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    # Starts a new game, and give you your color.
    # As defined in Reversi.py : color=1 for BLACK, and color=2 for WHITE
    def newGame(self, color):
        self._mycolor=color
        self._opponent = 1 if color == 2 else 2

    # You can get a feedback on the winner
    # This function gives you the color of the winner
    def endGame(self, color):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
