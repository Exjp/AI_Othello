import pygame
from pygame.locals import *
import Reversi

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Chorizo')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((100, 100, 100))


def displayBoard(b):
    radius = 50

    pygame.init()

  
    for i in range(1,10): 
        pygame.draw.aalines(background, (0, 0, 0), False, [(0, 100*i), (1000,100*i)],500)
        pygame.draw.aalines(background, (0, 0, 0), False, [(100*i, 0), (100*i,10000)],500)
    for x in range(b._boardsize):
        for y in range(b._boardsize):
            addPiece(x,y,b._board[y][x])
    
    

    # Blitter le tout dans la fenêtre
    screen.blit(background, (0, 0))
    pygame.display.flip()

def addPiece(X,Y,color):
    if color is 0:
        return
    radius = 50
    if(color == 1):
        pygame.draw.circle(background, (0, 0, 0), (50 + (X*100), 50 + (Y*100)), radius)
    if(color == 2):
        pygame.draw.circle(background, (255, 255, 255), (50 +(X*100), 50 + (Y*100)), radius)



#font = pygame.font.Font(None, 36)
#text = font.render("figatellu corse", 1, (10, 10, 10))
#textpos = text.get_rect()
#textpos.centerx = background.get_rect().centerx
#textpos.centery = background.get_rect().centery
#background.blit(text, textpos)
