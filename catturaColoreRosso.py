'''
Author: Michele Alladio, Samuele Forneris, Alessandro Seimandi, Nicolò La Valle
Descrizione:
Codice che implementa la cattura di oggetti di colore rosso tramite la libreria opencv.
Viene ricavata in modo ciclico la coordinata x dell'ogetto di colore rosso e viene utilizzata
per far muovere una macchina mediante la libreria PyGame.
'''

import pygame, sys, cv2, random,  time
import numpy as np
from pygame import mixer
from pygame.locals import *
import tkinter as tk
import config   #libreria contenente le costanti da utilizzare

root = tk.Tk()  #viene utilizzato per calcolare le dimensioni dello schermo (funziona sia su Windows che su Linux)

enemyY1 = -100
enemyY2 = -100
enemyY3 = -100
enemyY4 = -100
enemyY5 = -100
enemyY6 = -100

#inizializzazioni
pygame.init()

playerImg = pygame.image.load("veicoli\giocatore.png")
macchinaRossa = pygame.image.load("veicoli\macchinaRossa.png")
macchinaGialla = pygame.image.load("veicoli\macchinaGialla.png")
macchinaAzzurra = pygame.image.load("veicoli\macchinaAzzurra.png")
ambulanza = pygame.image.load("veicoli\Ambulanza.png")
taxi = pygame.image.load("veicoli\Taxi.png")
polizia = pygame.image.load("veicoli\polizia.png")

dizVeicoli = {"macchinaRossa": macchinaRossa, "macchinaGialla": macchinaGialla, "macchinaAzzurra": macchinaAzzurra, 
                "ambulamza": ambulanza, "taxi": taxi, "polizia": polizia}

background = pygame.image.load("street.png")
gameOverImg = pygame.image.load("gameOver.png")
clock = pygame.time.Clock()

#settaggio dei font
myFont = pygame.font.SysFont('Comic Sans MS', 30)
punteggio = myFont.render('Some Text', False, (0, 0, 0))

cattura = cv2.VideoCapture(0)   #cattura tramite videocamera
#dimensioni della cattura
#cattura.set(cv2.CAP_PROP_FRAME_WIDTH, BASE)
#cattura.set(cv2.CAP_PROP_FRAME_HEIGHT, ALTEZZA)

#calcola diversi parametri per adattare il gioco a qualsiasi schermo
def calcolaDimensioni():
    altezzaSchermo = int(root.winfo_screenheight())    #calcolo dell'altezza dello schermo
    baseSchermo = int(root.winfo_screenwidth())   #calcolo della base dello schermo
    yStaticaGiocatore = int((altezzaSchermo * config.Y_PREDEFINITA) / config.ALTEZZA) #calcolo della y della macchina nella schermata PyGame 
    enemyWidth = int((baseSchermo * config.ENEMY_WIDTH / config.BASE))    #calcolo della base macchina nemico
    enemyHeight = int((altezzaSchermo * config.ENEMY_HEIGHT / config.ALTEZZA))    #calcolo dell'altezza macchina nemico
    spawn1 = int((altezzaSchermo * config.SPAWN_1) / config.ALTEZZA)    #calcolo dell'altezza che, una volta raggiunta dalla prima auto, fa spawnare la seconda macchina della fila
    spawn2 = int((altezzaSchermo * config.SPAWN_2) / config.ALTEZZA)   #calcolo dell'altezza che, una volta raggiunta dalla prima auto, fa spawnare la terza macchina della fila
    spawn3 = altezzaSchermo + enemyHeight
    xSpawnCorsia1 = int((baseSchermo * config.X_SPAWN_CORSIA_1) / config.BASE)  #calcolo della x della corsia 1
    xSpawnCorsia2 = int((baseSchermo * config.X_SPAWN_CORSIA_2) / config.BASE)  #calcolo della x della corsia 2
    xSpawnCorsia3 = int((baseSchermo * config.X_SPAWN_CORSIA_3) / config.BASE)  #calcolo della x della corsia 3
    #limiti usati per gli spawn della seconda fila di macchine
    limite1 = int((altezzaSchermo * config.LIMITE1) / config.ALTEZZA)  
    limite2 = int((altezzaSchermo * config.LIMITE2) / config.ALTEZZA)  

    return altezzaSchermo, baseSchermo, yStaticaGiocatore, spawn1, spawn2, spawn3, xSpawnCorsia1, xSpawnCorsia2, xSpawnCorsia3, enemyWidth, enemyHeight, limite1, limite2

altezzaSchermo, baseSchermo, yStaticaGiocatore, spawn1, spawn2, spawn3, xSpawnCorsia1, xSpawnCorsia2, xSpawnCorsia3, enemyWidth, enemyHeight, limite1, limite2 = calcolaDimensioni()

screen = pygame.display.set_mode((baseSchermo,altezzaSchermo))    #schermo
#ridimensionamento delle immagini in base alla grandezza della schermata
gameOverImg = pygame.transform.scale(gameOverImg,(baseSchermo, altezzaSchermo))
background = pygame.transform.scale(background,(baseSchermo, altezzaSchermo))
playerImg = pygame.transform.scale(playerImg,(enemyWidth, enemyHeight))
enemyX = xSpawnCorsia1
enemyX2 = xSpawnCorsia3

for veicolo,_ in dizVeicoli.items():    #cicla i veicoli nel dizionario e li ridimensiona in base alla grandezza della schermata
    dizVeicoli[veicolo] = pygame.transform.scale(dizVeicoli[veicolo],(enemyWidth, enemyHeight))

def spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, veicoloRandom):
    screen.blit(background,(0, 0))  #impostazione dello sfondo

    screen.blit(veicoloRandom,(enemyX, enemyY1))    

    if enemyY3 <= altezzaSchermo+enemyWidth:    #se l'ultima auto è ancora nello schermo
        enemyY1 = enemyY1 + config.SPEED   #incremento posizione della prima auto   
        if enemyY1 > spawn1:   #quando la prima auto scende sotto una certa y parte la seconda auto
            screen.blit(veicoloRandom,(enemyX, enemyY2))
            enemyY2 = enemyY2 + config.SPEED   #incremento posizione della seconda auto 
            if enemyY2 > spawn2:   #quando la seconda auto scende sotto una certa y parte la terza auto
                screen.blit(veicoloRandom,(enemyX, enemyY3))
                enemyY3 = enemyY3 + config.SPEED   #incremento posizione della terza auto
                if enemyY3 > spawn3:
                    spawnaSeconda = True
    else:   #inizio nuova fila di auto
        enemyY3 = -100
        enemyY2 = -100
        enemyY1 = -100
        veicoloRandom = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
        #scelta random della corsia per lo spawn della fila di automobili
        num = random.randint(1,4)
        if num == 1:
            enemyX = xSpawnCorsia1
        elif num == 2:
            enemyX = xSpawnCorsia2
        elif num == 3:
            enemyX = xSpawnCorsia3

    if (enemyY3 >= limite1 and spawnaSeconda == True) or (enemyY6 <= altezzaSchermo+limite2 and spawnaSeconda == True):
        screen.blit(veicoloRandom,(enemyX2, enemyY4))
        if enemyY6 <= altezzaSchermo+enemyHeight:
            enemyY4 = enemyY4 + config.SPEED
            if enemyY4 > spawn1:
                screen.blit(veicoloRandom,(enemyX2, enemyY5))
                enemyY5 = enemyY5 + config.SPEED
                if enemyY4 > spawn2:
                    screen.blit(veicoloRandom,(enemyX2, enemyY6))
                    enemyY6 = enemyY6 + config.SPEED
        else:   #inizio di una nuova fila di auto
            velocitaNemico += 1
            enemyY4 = -100
            enemyY5 = -100
            enemyY6 = -100
            veicoloRandom = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
            #scelta random della corsia per lo spawn della fila di automobili
            num = random.randint(1,4) 
            if num == 1:
                enemyX2 = xSpawnCorsia1
            elif num == 2:
                enemyX2 = xSpawnCorsia2
            elif num == 3:
                enemyX2 = xSpawnCorsia3

    return enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, veicoloRandom

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
    
    return xRosso+limite1, ultimaX

def disegnaPlayer(playerX):
    screen.blit(playerImg,(playerX, yStaticaGiocatore))  #la macchina viene impostata alla x rilevata da opencv

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #se l'evento è l'uscita
            pygame.quit()
            sys.exit()  #il programma termina in maniera pulita

    clock.tick(60)  #60 fps
    pygame.display.update() #update della finestra di pygame

def controlloCollisioni(playerX, playerY, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6):
    if (((playerX >= enemyX-enemyWidth and playerX <= enemyX+enemyWidth) and (playerY <= enemyY1+enemyHeight and playerY >= enemyY3)) or ((playerX >= enemyX2-enemyWidth and playerX <= enemyX2+enemyWidth) and (playerY <= enemyY4+enemyHeight and playerY >= enemyY6))):
        pygame.mixer.stop() #interruzione dei suoni di sottodondo
        pygame.mixer.Sound('suoni\crash.wav').play()  #suono dello schianto
        time.sleep(2)   #ferma per due secondi la finestra
        screen.blit(gameOverImg,(0, 0)) #immagine di gameOver
        screen.blit(punteggio,(500,600))
        pygame.display.update() #update della finestra di python
        time.sleep(4)   
        pygame.quit()   #dopo quattro secondi chiude la finestra
        sys.exit()  #interrompe il programma in modo pulito

def main():
    global enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6
    spawnaSeconda = False

    ultimaX = baseSchermo / 2  #alla partenza del programma, se opencv non rileva oggetti rossi, la macchina viene posizionata a metà dello schermo (asse x)

    velocitaNemico = 10

    #suono di sfondo e accensione auto
    (pygame.mixer.Sound('suoni\Background.wav').play(-1)).set_volume(0.1)
    pygame.mixer.Sound('suoni\Accensione_auto.mp3').play()
    pygame.mixer.Sound('suoni\Rumore_auto.mp3').play(-1)

    veicoloRandom = random.choice(list(dizVeicoli.values())) #prima scelta random della skin del veicolo

    #varibili per lo spawn random dei veicoli nemici

    while True:
        
        enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, veicoloRandom = spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, veicoloRandom)
        
        playerX, ultimaX = cercaColore(ultimaX)

        disegnaPlayer(playerX)

        controlloCollisioni(playerX, yStaticaGiocatore, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6)
        

if __name__ == "__main__":
    main()


