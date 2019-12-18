# -*- coding: utf-8 -*-

''' Fichier de règles du Reversi pour le tournoi Masters Info 2019 en IA.
    Certaines parties de ce code sont fortement inspirée de 
    https://inventwithpython.com/chapter15.html

    '''

class Board:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0

    # Attention, la taille du plateau est donnée en paramètre
    def __init__(self, boardsize = 8):
      self._nbWHITE = 2
      self._nbBLACK = 2
      self._nextPlayer = self._BLACK
      self._boardsize = boardsize
      self._board = []
      for x in range(self._boardsize):
          self._board.append([self._EMPTY]* self._boardsize)
      _middle = int(self._boardsize / 2)
      self._board[_middle-1][_middle-1] = self._BLACK 
      self._board[_middle-1][_middle] = self._WHITE
      self._board[_middle][_middle-1] = self._WHITE
      self._board[_middle][_middle] = self._BLACK 
      
      self._stack= []
      self._successivePass = 0

    def reset(self):
        self.__init__()

    # Donne la taille du plateau 
    def get_board_size(self):
        return self._boardsize

    # Donne le nombre de pieces de blanc et noir sur le plateau
    # sous forme de tuple (blancs, noirs) 
    # Peut être utilisé si le jeu est terminé pour déterminer le vainqueur
    def get_nb_pieces(self):
      return (self._nbWHITE, self._nbBLACK)

    # Vérifie si player a le droit de jouer en (x,y)
    def is_valid_move(self, player, x, y):
        if x == -1 and y == -1:
            return not self.at_least_one_legal_move(player)
        return self.lazyTest_ValidMove(player,x,y)

    def _isOnBoard(self,x,y):
        return x >= 0 and x < self._boardsize and y >= 0 and y < self._boardsize 

    # Renvoie la liste des pieces a retourner si le coup est valide
    # Sinon renvoie False
    # Ce code est très fortement inspiré de https://inventwithpython.com/chapter15.html
    # y faire référence dans tous les cas
    def testAndBuild_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        tilesToFlip = [] # Si au moins un coup est valide, on collecte ici toutes les pieces a retourner
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y):
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. Let's collect
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
    
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    # Pareil que ci-dessus mais ne revoie que vrai / faux (permet de tester plus rapidement)
    def lazyTest_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y): # On a au moins 
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. 
                    self._board[xstart][ystart] = self._EMPTY
                    return True
                 
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        return False

    def _flip(self, player):
        if player == self._BLACK:
            return self._WHITE 
        return self._BLACK

    def is_game_over(self):
        if self.at_least_one_legal_move(self._nextPlayer):
            return False
        if self.at_least_one_legal_move(self._flip(self._nextPlayer)):
            return False
        return True 

    def push(self, move):
        [player, x, y] = move
        assert player == self._nextPlayer
        if x==-1 and y==-1: # pass
            self._nextPlayer = self._flip(player)
            self._stack.append([move, self._successivePass, []])
            self._successivePass += 1
            return
        toflip = self.testAndBuild_ValidMove(player,x,y)
        self._stack.append([move, self._successivePass, toflip])
        self._successivePass = 0
        self._board[x][y] = player
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK += 1 + len(toflip)
            self._nbWHITE -= len(toflip)
            self._nextPlayer = self._WHITE
        else:
            self._nbWHITE += 1 + len(toflip)
            self._nbBLACK -= len(toflip)
            self._nextPlayer = self._BLACK

    def pop(self):
        [move, self._successivePass, toflip] = self._stack.pop()
        [player,x,y] = move
        self._nextPlayer = player 
        if len(toflip) == 0: # pass
            assert x == -1 and y == -1
            return
        self._board[x][y] = self._EMPTY
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK -= 1 + len(toflip)
            self._nbWHITE += len(toflip)
        else:
            self._nbWHITE -= 1 + len(toflip)
            self._nbBLACK += len(toflip)

    # Est-ce que on peut au moins jouer un coup ?
    # Note: cette info pourrait être codée plus efficacement
    def at_least_one_legal_move(self, player):
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(player, x, y):
                   return True
        return False

    # Renvoi la liste des coups possibles
    # Note: cette méthode pourrait être codée plus efficacement
    def legal_moves(self):
        moves = []
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(self._nextPlayer, x, y):
                    moves.append([self._nextPlayer,x,y])
        if len(moves) is 0:
            moves = [[self._nextPlayer, -1, -1]] # We shall pass
        return moves

    #approche 1: simplement retourner le nombre de jeton
    def end_heuristique1(self, player=None):
        #if player is None:
        #    player = self._nextPlayer
        #if player is self._WHITE:
        #    return self._nbWHITE
        return self._nbBLACK

    #approche 2: retourner le résultat (à appeler en fin de partie)
    def end_heuristique2(self, player=None):
        if player is None:
            player = self._nextPlayer
        winner = 1000
        if self._nbWHITE > self._nbBLACK:
            winner = -1000
        elif self._nbWHITE == self._nbBLACK:
            winner = 0
        #if player is self._WHITE:
        #    return -winner
        return winner

    #approche 3: retourner le nombre de jeton si on gagne, et une val négative si on perd
    def end_heuristique3(self,player=None):
        if player is None:
            player = self._nextPlayer
        if self._nbWHITE > self._nbBLACK:
            return (-1000)+10*self._nbBLACK
        else:
             return 25*self._nbBLACK
    
    def evaluate_undercorner(self,x,y,player):
        if x<2:
            if y<2 and self._board[0][0] != self._EMPTY:
                return 10
            elif y> self._boardsize-3 and self._board[0][self._boardsize-1] != self._EMPTY:
                return 10
            else:
                return -100
        else:
            if y<2 and self._board[self._boardsize-1][0] != self._EMPTY:
                return 10
            elif y> self._boardsize-3 and self._board[self._boardsize-1][self._boardsize-1] != self._EMPTY:
                return 10
            else:
                return -100

    
    # Exemple d'heuristique : evaluer le board entier selon les bords
    def heuristique(self, player=None):
        if player is None:
            player = self._nextPlayer
        score = 0
        for x in range(self._boardsize):
            for y in range(self._boardsize):
                if self._board[x][y] is self._EMPTY:
                    continue
                point = 0
                if x == 0 or x == self._boardsize-1:
                    if y==0 or y == self._boardsize-1:
                        point=100
                    if y==1 or y == self._boardsize-2:
                        point= self.evaluate_undercorner(x,y,player)
                    else:
                        point =10
                elif y==0 or y == self._boardsize-1:
                    if x== 1 or x == self._boardsize-2:
                        point = self.evaluate_undercorner(x,y,player)
                    else:
                        point =10
                elif x==1 or x== self._boardsize-2:
                    if y==1 or y==self._boardsize-2:
                        point=self.evaluate_undercorner(x,y,player)
                else:
                    point+=1
                if self._board[x][y] is self._WHITE:
                    score-=point
                elif self._board[x][y] is self._BLACK:
                    score+=point
        #if player is self._WHITE:
        #    score *= -1 
        return score

    # Exemple d'heuristique simple : compte simplement les pieces et valoriser les coins
    def heuristique01(self, player=None):
        if player is None:
            player = self._nextPlayer
        corners = 0
        for x in range(2):
            for y in range(2):
                if self._board[x*(self._boardsize-1)][y*(self._boardsize-1)] is self._WHITE:
                    corners -= 50
                    print("corner "+str(x)+" "+str(y)+" can be white")
                elif self._board[x*(self._boardsize-1)][y*(self._boardsize-1)] is self._BLACK:
                    corners+= 50
                    print("corner "+str(x)+" "+str(y)+" can be black")
        #if player is self._WHITE:
        #    return self._nbWHITE - self._nbBLACK - corners 
        return self._nbBLACK - self._nbWHITE + corners

    # Exemple d'heuristique tres simple : compte simplement les pieces
    def heuristique0(self, player=None):
        if player is None:
            player = self._nextPlayer
        #if player is self._WHITE:
        #    return self._nbWHITE - self._nbBLACK
        return self._nbBLACK - self._nbWHITE

    def _piece2str(self, c):
        if c==self._WHITE:
            return 'O'
        elif c==self._BLACK:
            return 'X'
        else:
            return '.'

    def __str__(self):
        toreturn=""
        for l in self._board:
            for c in l:
                toreturn += self._piece2str(c)
            toreturn += "\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        toreturn += "(successive pass: " + str(self._successivePass) + " )"
        return toreturn

    __repr__ = __str__


