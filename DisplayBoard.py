import pygame
from pygame.locals import *
import Reversi
sizegame = 700
screen = pygame.display.set_mode((sizegame, sizegame))
pygame.display.set_caption('reversy')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((100, 100, 100))


def displayBoard(b):
    radius = int(sizegame/20)

    pygame.init()

    background.fill((100, 100, 100))
    for i in range(1,10): 
        pygame.draw.aalines(background, (0, 0, 0), False, [(0, int(sizegame/10)*i), (sizegame,int(sizegame/10)*i)],int(sizegame/2))
        pygame.draw.aalines(background, (0, 0, 0), False, [(int(sizegame/10)*i, 0), (int(sizegame/10)*i,sizegame)],int(sizegame/2))
    for x in range(b._boardsize):
        for y in range(b._boardsize):
            addPiece(x,y,b._board[x][y])
    for x in range(b._boardsize):
        for y in range(b._boardsize):
            drawlegalmove(b,x,y,b._board[x][y])
    
    

    # Blitter le tout dans la fenêtre
    screen.blit(background, (0, 0))
    pygame.display.flip()





def endDisplay():
    pygame.display.quit()
    pygame.quit()

def addPiece(X,Y,color):
    radius = int(sizegame/20)
    if color is 0:
        return
    elif(color == 1):
        pygame.draw.circle(background, (0, 0, 0), (int(sizegame/20) + (X*int(sizegame/10)), int(sizegame/20) + (Y*int(sizegame/10))), radius)
    elif(color == 2):
        pygame.draw.circle(background, (255, 255, 255), (int(sizegame/20) +(X*int(sizegame/10)), int(sizegame/20) + (Y*int(sizegame/10))), radius)
    
def drawlegalmove(b,X,Y,color):
    size = int(sizegame/10)
    moves = b.legal_moves()
    if color == 0 and ([1,X,Y] in moves or [2,X,Y] in moves):
        pygame.draw.rect(background, (255,255,0),(X*int(sizegame/10),Y*int(sizegame/10), size,size),1)

def getsizegame():
    return sizegame

#font = pygame.font.Font(None, 36)
#text = font.render("figatellu corse", 1, (10, 10, 10))
#textpos = text.get_rect()
#textpos.centerx = background.get_rect().centerx
#textpos.centery = background.get_rect().centery
#background.blit(text, textpos)
