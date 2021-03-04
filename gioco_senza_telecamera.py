import pygame
import sys
from pygame import mixer
from pygame.locals import *
import random

#Dichiarazione di variabili e costanti
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
playerX = 175
playerY = 480


#Inizializzazione di pygame con immagini
pygame.init()
playerImg = pygame.image.load("Player.png")
background = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()


#Colori
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)


def main():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #dimensioni schermo
    screen.fill(BLACK)
    global playerX, playerY

    while(True):
        screen.blit(background,(0, 0))
        screen.blit(playerImg,(playerX, playerY))
        for event in pygame.event.get():        #ascolta eventi (mouse, tastiera ecc)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    #muove in alto il robot
                    if playerY >= 0:
                        playerY=playerY-10
                if event.key == pygame.K_DOWN:  #muove in basso il robot
                    if playerY <= 500:
                        playerY= playerY+10
                if event.key == pygame.K_RIGHT: #muove in destra il robot
                    if playerX <= 350:
                        playerX=playerX+10
                if event.key == pygame.K_LEFT:  #muove in sinistra il robot
                    if playerX >= 0:
                        playerX=playerX-10

        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main()
