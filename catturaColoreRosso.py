'''
Author: Michele Alladio, Samuele Forneris, Alessandro Seimandi, Nicolò La Valle
Descrizione:
Codice che implementa la cattura di oggetti di colore rosso tramite la libreria opencv.
Viene ricavata in modo ciclico la coordinata x dell'ogetto di colore rosso e viene utilizzata
per far muovere una macchina mediante la libreria PyGame.
'''

import pygame, sys, cv2
import numpy as np
from pygame import mixer
from pygame.locals import *

#variabili globali
SCORE = 0
ALTEZZA = 700   #altezza schermata PyGame
BASE = 640  #base schermata PyGame
Y_PREDEFINITA = 550 #y della macchina nella schermata PyGame

#Colori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#inizializzazioni
pygame.init()
playerImg = pygame.image.load("player.png")
background = pygame.image.load("street.png")
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

def loop():
    ultimaX = BASE / 2  #alla partenza del programma, se opencv non rileva oggetti rossi, la macchina viene posizionata a metà dello schermo (asse x)

    while True:

        screen.fill(BLACK)   #colore schermo nero

        screen.blit(background,(0, 0))  #impostazione dello sfondo
        
        _, frame = cattura.read()
        frame = cv2.flip(frame, 1)  #flip dell'immagine sull'asse orizzontale

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #cattura del colore rosso
        rosso_pallido = np.array([136, 87, 111])
        rosso_acceso = np.array([180, 255, 255])

        #creazione della maschera del colore da catturare
        mascheraColoreRosso = cv2.inRange(hsv_frame, rosso_pallido,rosso_acceso)

        rosso = cv2.bitwise_and(frame, frame, mask=mascheraColoreRosso)

        #omissione degli altri colori (viene mostrato a schermo solo il rosso)
        cv2.imshow("Frame", frame)
        cv2.imshow("Rosso", rosso)

        xRosso, yRosso, base, altezza = cv2.boundingRect(mascheraColoreRosso) #returna x, y, base e altezza

        if xRosso == 0: #se opencv non rileva oggetti rossi la x viene impostata a 0 e la macchina
            xRosso = ultimaX    #per evitare questo, quando succede, la x viene impostata all'ultima posizione rilevata
        ultimaX = xRosso    #si aggiorna l'ultima posizione rilevata

        screen.blit(playerImg,(xRosso, Y_PREDEFINITA))  #la macchina viene impostata alla x rilevata da opencv

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #se l'evento è l'uscita
                pygame.quit()
                sys.exit()  #il programma termina in maniera pulita

        clock.tick(60)  #60 fps
        pygame.display.update() #update della finestra di pygame

def main():
    loop()
        

if __name__ == "__main__":
    main()




