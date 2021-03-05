'''
Authors: Michele Alladio, Samuele Forneris, Alessandro Seimandi, Nicolò La Valle
Descrizione:
Codice che implementa la cattura di oggetti di colore rosso tramite la libreria opencv.
Viene ricavata in modo ciclico la coordinata x dell'ogetto di colore rosso e viene utilizzata
per far muovere una macchina mediante la libreria PyGame.
'''

import pygame, sys, cv2, random,  time
import numpy as np
from pygame import mixer
from pygame.locals import *

#variabili globali
SCORE = 0
ALTEZZA = 700  #altezza schermata PyGame
#BASE = 1170  #base schermata PyGame
BASE = 1400
Y_PREDEFINITA = 550 #y della macchina nella schermata PyGame
SPEED = 10
SPAWN_1 = 20
SPAWN_2 = 140
X_SPAWN_CORSIA_1 = 450
X_SPAWN_CORSIA_2 = 650
X_SPAWN_CORSIA_3 = 860

enemyX = X_SPAWN_CORSIA_1
enemyX2 = X_SPAWN_CORSIA_3
enemyY1 = -100
enemyY2 = -100
enemyY3 = -100
enemyY4 = -100
enemyY5 = -100
enemyY6 = -100

#inizializzazioni
pygame.init()
playerImg = pygame.image.load("player.png")
enemyImg = pygame.image.load("enemy.png")
background = pygame.image.load("street.png")
gameOverImg = pygame.image.load("gameOver.png")
gameOverImg = pygame.transform.scale(gameOverImg,(BASE, ALTEZZA))
background = pygame.transform.scale(background,(BASE, ALTEZZA))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((BASE,ALTEZZA))    #schermo

#settaggio dei font
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
#game_over = font.render("Game Over", True, BLACK)

cattura = cv2.VideoCapture(0)   #cattura tramite videocamera
#dimensioni della cattura
#cattura.set(cv2.CAP_PROP_FRAME_WIDTH, BASE)
#cattura.set(cv2.CAP_PROP_FRAME_HEIGHT, ALTEZZA)

def spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico):
    screen.blit(background,(0, 0))  #impostazione dello sfondo
    screen.blit(enemyImg,(enemyX, enemyY1))    

    if enemyY3 <= ALTEZZA+100:    #se l'ultima auto è ancora nello schermo
        enemyY1 = enemyY1 + SPEED   #incremento posizione della prima auto   
        if enemyY1 > SPAWN_1:   #quando la prima auto scende sotto una certa y parte la seconda auto
            screen.blit(enemyImg,(enemyX, enemyY2))
            enemyY2 = enemyY2 + SPEED   #incremento posizione della seconda auto 
            if enemyY1 > SPAWN_2:   #quando la seconda auto scende sotto una certa y parte la terza auto
                screen.blit(enemyImg,(enemyX, enemyY3))
                enemyY3 = enemyY3 + SPEED   #incremento posizione della terza auto
                if enemyY1 > SPAWN_2 + 220:
                    spawnaSeconda = True
    else:   #inizio nuova fila di auto
        enemyY3 = -100
        enemyY2 = -100
        enemyY1 = -100
        #scelta random della corsia per lo spawn della fila di automobili
        num = random.randint(1,4)
        if num == 1:
            enemyX = X_SPAWN_CORSIA_1
        elif num == 2:
            enemyX = X_SPAWN_CORSIA_2
        elif num == 3:
            enemyX = X_SPAWN_CORSIA_3

    if (enemyY3 >=300 and spawnaSeconda == True) or (enemyY6 <= ALTEZZA+100 and spawnaSeconda == True):
        screen.blit(enemyImg,(enemyX2, enemyY4))
        if enemyY6 <= ALTEZZA+100:
            enemyY4 = enemyY4 + SPEED
            if enemyY4 > SPAWN_1:
                screen.blit(enemyImg,(enemyX2, enemyY5))
                enemyY5 = enemyY5 + SPEED
                if enemyY4 > SPAWN_2:
                    screen.blit(enemyImg,(enemyX2, enemyY6))
                    enemyY6 = enemyY6 + SPEED
        else:   #inizio di una nuova fila di auto
            velocitaNemico += 1
            enemyY4 = -100
            enemyY5 = -100
            enemyY6 = -100
            #scelta random della corsia per lo spawn della fila di automobili
            num = random.randint(1,4)   
            if num == 1:
                enemyX2 = X_SPAWN_CORSIA_1
            elif num == 2:
                enemyX2 = X_SPAWN_CORSIA_2
            elif num == 3:
                enemyX2 = X_SPAWN_CORSIA_3

    return enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico

def cercaColore(ultimaX):
    _, frame = cattura.read()
    frame = cv2.flip(frame, 1)  #flip dell'immagine sull'asse orizzontale

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #cattura del colore rosso
    rosso_pallido = np.array([136, 87, 111])
    rosso_scuro = np.array([180, 255, 255])

    #creazione della maschera del colore da catturare
    mascheraColoreRosso = cv2.inRange(hsv_frame, rosso_pallido,rosso_scuro)

    rosso = cv2.bitwise_and(frame, frame, mask=mascheraColoreRosso)

    #omissione degli altri colori (viene mostrato a schermo solo il rosso)
    cv2.imshow("Frame", frame)
    cv2.imshow("Rosso", rosso)

    xRosso, yRosso, base, altezza = cv2.boundingRect(mascheraColoreRosso) #returna x, y, base e altezza

    if xRosso == 0: #se opencv non rileva oggetti rossi la x viene impostata a 0 e la macchina
        xRosso = ultimaX    #per evitare questo, quando succede, la x viene impostata all'ultima posizione rilevata
    ultimaX = xRosso    #si aggiorna l'ultima posizione rilevata
    
    return xRosso+300, yRosso+200, ultimaX

def disegnaPlayer(playerX):
    screen.blit(playerImg,(playerX, Y_PREDEFINITA))  #la macchina viene impostata alla x rilevata da opencv

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #se l'evento è l'uscita
            pygame.quit()
            sys.exit()  #il programma termina in maniera pulita

    clock.tick(60)  #60 fps
    pygame.display.update() #update della finestra di pygame

def controlloCollisioni(playerX, playerY, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6):
    if (((playerX >= enemyX-50 and playerX <= enemyX+50) and (playerY <= enemyY1+80 and playerY >= enemyY3)) or ((playerX >= enemyX2-50 and playerX <= enemyX2+50) and (playerY <= enemyY4+80 and playerY >= enemyY6))):
        pygame.mixer.stop() #interruzione dei suoni di sottodondo
        pygame.mixer.Sound('crash.wav').play()  #suono dello schianto
        time.sleep(2)   #ferma per due secondi la finestra
        screen.blit(gameOverImg,(0, 0)) #immagine di gameOver
        pygame.display.update() #update della finestra di python
        time.sleep(4)   
        pygame.quit()   #dopo quattro secondi chiude la finestra
        sys.exit()  #interrompe il programma in modo pulito

def main():
    global enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6
    spawnaSeconda = False

    ultimaX = BASE / 2  #alla partenza del programma, se opencv non rileva oggetti rossi, la macchina viene posizionata a metà dello schermo (asse x)

    velocitaNemico = 10

    #suono di sfondo e accensione auto
    (pygame.mixer.Sound('background.wav').play(-1)).set_volume(0.1)
    pygame.mixer.Sound('Accensione_auto.mp3').play()
    pygame.mixer.Sound('Rumore_auto.mp3').play(-1)

    while True:
        
        enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico = spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico)
        
        playerX, playerY, ultimaX = cercaColore(ultimaX)

        disegnaPlayer(playerX)

        controlloCollisioni(playerX, playerY, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6)
        

if __name__ == "__main__":
    main()


