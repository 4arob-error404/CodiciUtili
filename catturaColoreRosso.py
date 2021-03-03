'''
Author: Michele Alladio, Samuele Forneris
Descrizione:
Codice che implementa la cattura di oggetti di colore rosso tramite la libreria opencv.
Viene ricavata in modo ciclico la coordinata x dell'ogetto di colore rosso e viene utilizzata
per far muovere un quadrato di colore bianco mediante la libreria PyGame.
'''

import sys, cv2, pygame
import numpy as np

NERO = (0,0,0)    #RGB
BIANCO = (255,255,255)

ALTEZZA = 600   #altezza schermata PyGame
BASE = 640  #base schermata PyGame
Y_PREDEFINITA = 400 #y del quadrato nella schermata PyGame
dimSquare = 10  #dimensione del quadrato

cattura = cv2.VideoCapture(0)   #cattura tramite videocamera

def drawSquare(posX, posY): #disegno del quadrato bianco
        square = pygame.Rect(posX, posY, dimSquare, dimSquare) 
        pygame.draw.rect(screen, BIANCO, square)

def main():

    global screen   #schermo
    
    pygame.init()   #inizializzazione di pygame
    screen = pygame.display.set_mode((BASE,ALTEZZA))    #richiede una tupla

    while True:

        screen.fill(NERO)   #colore schermo nero
        
        _, frame = cattura.read()
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

        x, y, base, altezza = cv2.boundingRect(mascheraColoreRosso) #returna x, y, base e altezza

        drawSquare(x, Y_PREDEFINITA)   #disegno un quadrato in base a dove muovo l'oggetto rosso

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #se l'evento è l'uscita
                pygame.quit()
                sys.exit()  #il programma termina in maniera pulita
        
        pygame.display.update() #update della finestra di pygame
        

if __name__ == "__main__":
    main()




