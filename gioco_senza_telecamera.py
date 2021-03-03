import pygame, sys
from pygame.locals import *
import random, time


pygame.init()


FramePerSec = pygame.time.Clock()

#COLORI
ROSSO   = (255, 0, 0)
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)

#DIMENSIONI DELLA FINESTRA DI GIOCO
LARGHEZZA = 400
ALTEZZA = 600


#FONTS
font = pygame.font.SysFont("Verdana", 60)
font_piccolo = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, NERO)

sfondo = pygame.image.load("AnimatedStreet.png")


#CREAZIONE DELLO SCHERMO BIANCO
DISPLAYSURF = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
DISPLAYSURF.fill(BIANCO)
pygame.display.set_caption("Game")

#variabili per la velocità e il punteggio
velocita = 5
punteggio = 0

class Nemico(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (random.randint(40,LARGHEZZA-40), 0))

      def move(self):
        global punteggio
        self.rect.move_ip(0,velocita)
        if (self.rect.bottom > 600):
            punteggio += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, LARGHEZZA - 40), 0)


class Giocatore(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < LARGHEZZA:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

#Setting up Sprites        
giocatore = Giocatore()
nemico = Nemico()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(nemico)
personaggi = pygame.sprite.Group()
personaggi.add(giocatore)
personaggi.add(nemico)

#Adding a new User event 
INC_velocita = pygame.USEREVENT + 1
pygame.time.set_timer(INC_velocita, 1000)

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_velocita:
              velocita += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



    DISPLAYSURF.blit(sfondo, (0,0))
    fonts = font_piccolo.render(str(punteggio), True, NERO)
    DISPLAYSURF.blit(fonts, (10,10))

    #Moves and Re-draws all Sprites
    for entita in personaggi:
        DISPLAYSURF.blit(entita.image, entita.rect)
        entita.move()

    #To be run if collision occurs between Player and Nemico
    if pygame.sprite.spritecollideany(giocatore, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(1)
                   
          DISPLAYSURF.fill(ROSSO)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entita in personaggi:
                entita.kill()
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(60)
