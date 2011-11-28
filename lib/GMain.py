import pygame
import sys
from pygame.locals import *
from data import *
from world import *


xy = (800, 600)
Surface = pygame.display.set_mode(xy)
pygame.display.set_caption("xAiJ :: Version beta")
background = (50,50,50)
worldgame = world(Surface)

def main():
    pygame.init()
    
    while(True):
        Draw()
        getInput()
        
    
def getInput():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        worldgame.KeyEvent(key, event)
        if event.type == QUIT:
            pygame.quit(); sys.exit()

            
def Draw():
    Surface.fill(background)
    worldgame.Draw()
    pygame.display.flip()
