class PlayerInterface():
    # Returns your player name, as to be displayed during the game
    def getPlayerName(self):
        return "Saucisse"

    # Returns your move. The move must be a couple of two integers,
    # Which are the coordinates of where you want to put your piece
    # on the board. Coordinates are the coordinates given by the Reversy.py
    # methods (e.g. validMove(board, x, y) must be true of you play '(x,y)')
    # You can also answer (-1,-1) as "pass". Note: the referee will never
    # call your function if the game is over
    def getPlayerMove(self):
        better = -1
        tmp = []

        for i in self._board.legal_moves():
            self._board.push(i)
            #print("début alphabeta = ",i)
            res = minValue(b, -100, 100)
            b.pop()
            
            #print("res = ",res)
            if res == 1:
                return i
            elif res == -1:
                if len(tmp):
                    tmp = i
            elif res == 0 and better -1:
                better = 0
                tmp = i

        return  tmp

    # Inform you that the oponent has played this move. You must play it
    # with no search (just update your local variables to take it into account)
    def playOpponentMove(self, x,y):
        pass

    # Starts a new game, and give you your color.
    # As defined in Reversi.py : color=1 for BLACK, and color=2 for WHITE
    def newGame(self, color):
        pass

    # You can get a feedback on the winner
    # This function gives you the color of the winner
    def endGame(self, color):
        pass


