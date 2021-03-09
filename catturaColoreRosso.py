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

background = pygame.image.load("immaginiGioco\street.png")
gameOverImg = pygame.image.load("immaginiGioco\gameOver.png")

turboImg = pygame.image.load("immaginiGioco\Turbo.png")
turboScrittaImg = pygame.image.load("immaginiGioco\TurboScritta.png")
turboFiammaImg = pygame.image.load("immaginiGioco\TurboFiamma.png")

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
turboImg = pygame.transform.scale(turboImg,(enemyWidth, enemyWidth))
turboFiammaImg = pygame.transform.scale(turboFiammaImg,(enemyWidth, enemyWidth))
turboScrittaImg = pygame.transform.scale(turboScrittaImg,(400,300))
enemyX = xSpawnCorsia1
enemyX2 = xSpawnCorsia3

for veicolo,_ in dizVeicoli.items():    #cicla i veicoli nel dizionario e li ridimensiona in base alla grandezza della schermata
    dizVeicoli[veicolo] = pygame.transform.scale(dizVeicoli[veicolo],(enemyWidth, enemyHeight))

def spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed, turboOn):

    screen.blit(background,(0, 0))  #impostazione dello sfondo

    if fineSpawnNemiciRandom1 == True:
        veicoloRandom1 = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
        fineSpawnNemiciRandom1 = False

    screen.blit(veicoloRandom1,(enemyX, enemyY1))  

    if enemyY3 <= altezzaSchermo+enemyWidth:    #se l'ultima auto è ancora nello schermo
        enemyY1 = enemyY1 + speed   #incremento posizione della prima auto   
        if enemyY1 > spawn1:   #quando la prima auto scende sotto una certa y parte la seconda auto
            if fineSpawnNemiciRandom2 == True:
                veicoloRandom2 = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
                fineSpawnNemiciRandom2 = False

            screen.blit(veicoloRandom2,(enemyX, enemyY2))
            enemyY2 = enemyY2 + speed

            if enemyY2 > spawn2:   #quando la seconda auto scende sotto una certa y parte la terza auto
                if fineSpawnNemiciRandom3 == True:
                    veicoloRandom3 = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
                    fineSpawnNemiciRandom3 = False

                screen.blit(veicoloRandom3,(enemyX, enemyY3))
                enemyY3 = enemyY3 + speed

                if enemyY3 > spawn3:
                    spawnaSeconda = True
    else:   #inizio nuova fila di auto
        enemyY3 = -100
        enemyY2 = -100
        enemyY1 = -100
        fineSpawnNemiciRandom1 = True
        fineSpawnNemiciRandom2 = True
        fineSpawnNemiciRandom3 = True
        cntSpeed += 1

        #gestione di aumento della velocità graduale (più il contatore è un numero alto più la velocità aumenta lentamente)
        if turboOn == False:
            if cntSpeed < 8:  
                if cntSpeed % 2 == 0:
                    speed += 1
            if cntSpeed >= 8:
                if cntSpeed % 3 == 0:
                    speed += 1
            if cntSpeed >= 13:
                if cntSpeed % 4 == 0:
                    speed += 1

        #scelta random della corsia per lo spawn della fila di automobili
        num = random.randint(1,4)
        if num == 1:
            enemyX = xSpawnCorsia1
        elif num == 2:
            enemyX = xSpawnCorsia2
        elif num == 3:
            enemyX = xSpawnCorsia3

    if (enemyY3 >= limite1 and spawnaSeconda == True) or (enemyY6 <= altezzaSchermo+limite2 and spawnaSeconda == True):
        
        if fineSpawnNemiciRandom4 == True:
            veicoloRandom4 = random.choice(list(dizVeicoli.values())) #scelta random della skin del veicolo
            fineSpawnNemiciRandom4 = False

        screen.blit(veicoloRandom4,(enemyX2, enemyY4))

        if enemyY6 <= altezzaSchermo+enemyHeight:
            enemyY4 = enemyY4 + speed
            if enemyY4 > spawn1:
                if fineSpawnNemiciRandom5 == True:
                    veicoloRandom5 = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
                    fineSpawnNemiciRandom5 = False

                screen.blit(veicoloRandom5,(enemyX2, enemyY5))
                enemyY5 = enemyY5 + speed

                if enemyY4 > spawn2:
                    if fineSpawnNemiciRandom6 == True:
                        veicoloRandom6 = random.choice(list(dizVeicoli.values())) #scelta random del la skin del veicolo
                        fineSpawnNemiciRandom6 = False

                    screen.blit(veicoloRandom6,(enemyX2, enemyY6))
                    enemyY6 = enemyY6 + speed
                    fineSpawnNemiciRandom2 = False

        else:   #inizio di una nuova fila di auto
            enemyY4 = -100
            enemyY5 = -100
            enemyY6 = -100
            fineSpawnNemiciRandom4 = True
            fineSpawnNemiciRandom5 = True
            fineSpawnNemiciRandom6 = True
            #scelta random della corsia per lo spawn della fila di automobili
            num = random.randint(1,4) 
            if num == 1:
                enemyX2 = xSpawnCorsia1
            elif num == 2:
                enemyX2 = xSpawnCorsia2
            elif num == 3:
                enemyX2 = xSpawnCorsia3

    return enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed


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

def disegnaPlayer(playerX, playerY):
    screen.blit(playerImg,(playerX, playerY))  #la macchina viene impostata alla x rilevata da opencv

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

def spawnNitro(speed, cntSpeed, playerY, playerX, turboOn, nitroX, nitroY):
    if cntSpeed % 3 == 0 and cntSpeed != 0: #il turbo spawna ogni 3 file di macchine
        if turboOn == False:    #se il turbo è disattivato
            #viene creata l'immagine del turbo in una delle tre corsie e conmpie un movimento di discesa con l'incremento della sua y
            screen.blit(turboImg,(nitroX, nitroY))  
            nitroY += speed/2

            if (playerX >= nitroX-enemyWidth and playerX <= nitroX+enemyWidth) and (yStaticaGiocatore <= nitroY+enemyWidth and yStaticaGiocatore >= nitroY):    #se il giocatore "tocca" il turbo
                nitroY = 0  #si resetta la y del turbo
                screen.blit(turboImg,(0, config.Y_FUORI_SCHERMO))   #si toglie dallo schermo l'immagine del turbo
                turboOn = True

    else:   #se il turbo non spawna
        if playerY <= yStaticaGiocatore:    #il giocatore viene riportato alla sua y predefinita
            playerY += 2
        
        nitroY = 0  #si resetta la y del turbo
        turboOn = False #il turbo viene disattivato

        #spawn randomico del logo del turbo
        num = random.randint(1,4)
        if num == 1:
            nitroX = xSpawnCorsia1
        elif num == 2:
            nitroX = xSpawnCorsia2
        elif num == 3:
            nitroX = xSpawnCorsia3

    if turboOn == True: #se il turbo è attivato
        playerY -= speed/2   #il player avanza
        #viene mostrato il logo del turbo e la fiamma
        screen.blit(turboScrittaImg,(0, 0))
        screen.blit(turboFiammaImg,(playerX, playerY+enemyHeight))

    pygame.display.update()

    return speed, playerY, turboOn, nitroX, nitroY


def main():
    global enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6

    spawnaSeconda = False

    ultimaX = baseSchermo / 2  #alla partenza del programma, se opencv non rileva oggetti rossi, la macchina viene posizionata a metà dello schermo (asse x)

    velocitaNemico = 10

    #suono di sfondo e accensione auto
    (pygame.mixer.Sound('suoni\Background.wav').play(-1)).set_volume(0.1)
    pygame.mixer.Sound('suoni\Accensione_auto.mp3').play()
    pygame.mixer.Sound('suoni\Rumore_auto.mp3').play(-1)

    #variabili per il controllo dello spawn dei veicoli
    fineSpawnNemiciRandom1 = True
    fineSpawnNemiciRandom2 = True
    fineSpawnNemiciRandom3 = True
    fineSpawnNemiciRandom4 = True
    fineSpawnNemiciRandom5 = True
    fineSpawnNemiciRandom6 = True

    #variabili per lo spawn randomico della skin dei veicoli (inizializzazioni di convenzione per evitare errori)
    veicoloRandom1 = ambulanza
    veicoloRandom2 = ambulanza
    veicoloRandom3 = ambulanza
    veicoloRandom4 = ambulanza
    veicoloRandom5 = ambulanza
    veicoloRandom6 = ambulanza

    turboOn = False #variabile per il controllo dell'attivazione del turbo

    #inizializzazioni di convenzione per evitare errori
    nitroX = 0
    nitroY = 0

    speed = config.SPEED_INIZIALE   #velocità della auto nemiche
    cntSpeed = 0    #viene incrementata la velocità ogni volta che due linee di macchine scompaiono

    playerY = yStaticaGiocatore

    while True:
        
        enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed = spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed, turboOn)
        
        playerX, ultimaX = cercaColore(ultimaX)

        disegnaPlayer(playerX, playerY)

        controlloCollisioni(playerX, playerY, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6)

        speed, playerY, turboOn, nitroX, nitroY = spawnNitro(speed, cntSpeed, playerY, playerX, turboOn, nitroX, nitroY)

if __name__ == "__main__":
    main()
