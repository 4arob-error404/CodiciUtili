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
from datetime import datetime

root = tk.Tk()  #viene utilizzato per calcolare le dimensioni dello schermo (funziona sia su Windows che su Linux)

enemyY1 = -100
enemyY2 = -100
enemyY3 = -100
enemyY4 = -100
enemyY5 = -100
enemyY6 = -100

#inizializzazioni
pygame.init()

#veicoli
playerImg = pygame.image.load("immaginiGioco/Veicoli/giocatore.png")
macchinaRossa = pygame.image.load("immaginiGioco/Veicoli/macchinaRossa.png")
macchinaGialla = pygame.image.load("immaginiGioco/Veicoli/macchinaGialla.png")
macchinaAzzurra = pygame.image.load("immaginiGioco/Veicoli/macchinaAzzurra.png")
ambulanza = pygame.image.load("immaginiGioco/Veicoli/Ambulanza.png")
taxi = pygame.image.load("immaginiGioco/Veicoli/Taxi.png")
polizia = pygame.image.load("immaginiGioco/Veicoli/polizia.png")

dizVeicoli = {"macchinaRossa": macchinaRossa, "macchinaGialla": macchinaGialla, "macchinaAzzurra": macchinaAzzurra, 
                "ambulamza": ambulanza, "taxi": taxi, "polizia": polizia}

#esplosione
esplosione1 = pygame.image.load("immaginiGioco/esplosione/1.png")
esplosione2 = pygame.image.load("immaginiGioco/esplosione/2.png")
esplosione3 = pygame.image.load("immaginiGioco/esplosione/3.png")
esplosione4 = pygame.image.load("immaginiGioco/esplosione/4.png")
esplosione5 = pygame.image.load("immaginiGioco/esplosione/5.png")
esplosione6 = pygame.image.load("immaginiGioco/esplosione/6.png")
esplosione7 = pygame.image.load("immaginiGioco/esplosione/7.png")
esplosione8 = pygame.image.load("immaginiGioco/esplosione/8.png")
esplosione9 = pygame.image.load("immaginiGioco/esplosione/9.png")
esplosione10 = pygame.image.load("immaginiGioco/esplosione/10.png")
esplosione11 = pygame.image.load("immaginiGioco/esplosione/11.png")
esplosione12 = pygame.image.load("immaginiGioco/esplosione/12.png")
esplosione13 = pygame.image.load("immaginiGioco/esplosione/13.png")
esplosione14 = pygame.image.load("immaginiGioco/esplosione/14.png")

esplosione = {1: esplosione1, 2: esplosione2, 3: esplosione3, 4: esplosione4, 5: esplosione5,
                6: esplosione6, 7: esplosione7, 8: esplosione8, 9: esplosione9, 10: esplosione10,
                11: esplosione11, 12: esplosione12, 13: esplosione13, 14: esplosione14}

cespuglio1 = pygame.image.load("immaginiGioco/cespugli/cespuglio1.png")
cespuglio2 = pygame.image.load("immaginiGioco/cespugli/cespuglio2.png")
cespuglio3 = pygame.image.load("immaginiGioco/cespugli/cespuglio3.png")
cespuglio4 = pygame.image.load("immaginiGioco/cespugli/cespuglio4.png")
cespuglio5 = pygame.image.load("immaginiGioco/cespugli/cespuglio5.png")

#cespugli = {1: cespuglio1, 2: cespuglio2, 3: cespuglio3, 4: cespuglio4, 5: cespuglio5}

background = pygame.image.load("immaginiGioco/street.png")
gameOverImg = pygame.image.load("immaginiGioco/gameOver.png")

turboImg = pygame.image.load("immaginiGioco/Turbo.png")
turboScrittaImg = pygame.image.load("immaginiGioco/TurboScritta.png")
turboFiammaImg = pygame.image.load("immaginiGioco/TurboFiamma.png")

cuorePieno = pygame.image.load("immaginiGioco/Cuore.png")
cuoreVuoto = pygame.image.load("immaginiGioco/CuoreVuoto.png")
clock = pygame.time.Clock()
#settaggio dei font
BLACK = (0,0,0)
myFont = pygame.font.SysFont('Comic Sans MS', 40, 10)
txtPunteggio = myFont.render('SCORE:', False, BLACK)

cattura = cv2.VideoCapture(0)   #cattura tramite videocamera

classifica = open("classifica.txt", "a") #per salvare il punteggio

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
    #limiti usati per il corretto posizionamento dei nemici nelle corsie
    xSpawnCorsia1 = int((baseSchermo * config.X_SPAWN_CORSIA_1) / config.BASE)  #calcolo della x della corsia 1
    xSpawnCorsia2 = int((baseSchermo * config.X_SPAWN_CORSIA_2) / config.BASE)  #calcolo della x della corsia 2
    xSpawnCorsia3 = int((baseSchermo * config.X_SPAWN_CORSIA_3) / config.BASE)  #calcolo della x della corsia 3
    #limiti usati per gli spawn della seconda fila di macchine
    limite1 = int((altezzaSchermo * config.LIMITE1) / config.ALTEZZA)  
    limite2 = int((altezzaSchermo * config.LIMITE2) / config.ALTEZZA)
    #variabili per il posizionamento dei cuori  
    xCuore1 = int((baseSchermo * config.X_CUORE_1) / config.BASE)
    xCuore2 = int((baseSchermo * config.X_CUORE_2) / config.BASE)
    xCuore3 = int((baseSchermo * config.X_CUORE_3) / config.BASE)  
    #variabili per il posizionamento del punteggio
    punteggioY = int((altezzaSchermo * config.PUNTEGGIOY) / config.ALTEZZA)
    punteggioX = int((baseSchermo * config.PUNTEGGIOX) / config.BASE) 
    puntiX = int((baseSchermo * config.PUNTIX) / config.BASE)  
    #variabili per il posizionamento e lo spawn dei cespugli
    cespuglioX1 = int((baseSchermo * config.CESPUGLIO_X1) / config.BASE) 
    cespuglioX2 = int((baseSchermo * config.CESPUGLIO_X2) / config.BASE) 
    spawnCespuglio1 = int((altezzaSchermo * config.SPAWN_CESPUGLIO1) / config.ALTEZZA)
    spawnCespuglio2 = int((altezzaSchermo * config.SPAWN_CESPUGLIO2) / config.ALTEZZA)
    spawnCespuglio3 = int((altezzaSchermo * config.SPAWN_CESPUGLIO3) / config.ALTEZZA)
    spawnCespuglio4 = int((altezzaSchermo * config.SPAWN_CESPUGLIO4) / config.ALTEZZA)
    spawnCespuglioIniziale =  int((altezzaSchermo * config.SPAWN_CESPUGLIO_INIZIALE) / config.ALTEZZA)

    return altezzaSchermo, baseSchermo, yStaticaGiocatore, spawn1, spawn2, spawn3, xSpawnCorsia1, xSpawnCorsia2, xSpawnCorsia3, enemyWidth, enemyHeight, limite1, limite2, xCuore1, xCuore2, xCuore3, punteggioX, punteggioY, puntiX, cespuglioX1, cespuglioX2, spawnCespuglio1, spawnCespuglio2, spawnCespuglio3, spawnCespuglio4, spawnCespuglioIniziale

altezzaSchermo, baseSchermo, yStaticaGiocatore, spawn1, spawn2, spawn3, xSpawnCorsia1, xSpawnCorsia2, xSpawnCorsia3, enemyWidth, enemyHeight, limite1, limite2, xCuore1, xCuore2, xCuore3, punteggioX, punteggioY, puntiX, cespuglioX1, cespuglioX2, spawnCespuglio1, spawnCespuglio2, spawnCespuglio3, spawnCespuglio4, spawnCespuglioIniziale = calcolaDimensioni()

#dimensioni della cattura
cattura.set(cv2.CAP_PROP_FRAME_WIDTH, baseSchermo)
cattura.set(cv2.CAP_PROP_FRAME_HEIGHT, altezzaSchermo)
screen = pygame.display.set_mode((baseSchermo,altezzaSchermo))    #schermo

#ridimensionamento delle immagini in base alla grandezza della schermata
gameOverImg = pygame.transform.scale(gameOverImg,(baseSchermo, altezzaSchermo))
background = pygame.transform.scale(background,(baseSchermo, altezzaSchermo))
playerImg = pygame.transform.scale(playerImg,(enemyWidth, enemyHeight))
turboImg = pygame.transform.scale(turboImg,(enemyWidth, enemyWidth))
turboFiammaImg = pygame.transform.scale(turboFiammaImg,(enemyWidth, enemyWidth))
turboScrittaImg = pygame.transform.scale(turboScrittaImg,(400,300))
cuorePieno = pygame.transform.scale(cuorePieno,(enemyWidth,enemyWidth))
cuoreVuoto = pygame.transform.scale(cuoreVuoto,(enemyWidth,enemyWidth))
enemyX = xSpawnCorsia1
enemyX2 = xSpawnCorsia3

for veicolo,_ in dizVeicoli.items():    #cicla i veicoli nel dizionario e li ridimensiona in base alla grandezza della schermata
    dizVeicoli[veicolo] = pygame.transform.scale(dizVeicoli[veicolo],(enemyWidth, enemyHeight))

for immagine,_ in esplosione.items():
    esplosione[immagine] = pygame.transform.scale(esplosione[immagine],(enemyHeight, enemyHeight))

cespuglio1 = pygame.transform.scale(cespuglio1,(100, 100))
cespuglio2 = pygame.transform.scale(cespuglio2,(100, 100))
cespuglio3 = pygame.transform.scale(cespuglio3,(100, 100))
cespuglio4 = pygame.transform.scale(cespuglio4,(100, 100))
cespuglio5 = pygame.transform.scale(cespuglio5,(100, 100))

def spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed, turboOn, punteggio):

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
        punteggio += 100    #incremento del punteggio

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

    return enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed, punteggio


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

def controlloCollisioni(playerX, playerY, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, cntCollisioni, macchinaFantasma, punteggio,audio):
    if (((playerX >= enemyX-enemyWidth and playerX <= enemyX+enemyWidth) and (playerY <= enemyY1+enemyHeight and playerY >= enemyY3)) or ((playerX >= enemyX2-enemyWidth and playerX <= enemyX2+enemyWidth) and (playerY <= enemyY4+enemyHeight and playerY >= enemyY6))):  #controllo collisioni
        cntCollisioni += 1  #viene incrementato il contatore (si perde una vita)
        
        if cntCollisioni == 3:  #quando si perdono tutte e 3 le vite -> GameOver
            pygame.mixer.stop() #interruzione dei suoni di sottodondo
            if audio == 1:
                pygame.mixer.Sound('suoni/crash.wav').play()  #suono dello schianto

            for immagine,_ in esplosione.items():   #stampa della sequanza di esplosioni
                screen.blit(esplosione[immagine],(playerX-50, playerY-50))
                pygame.display.update()
                time.sleep(0.1)#tempo di attesa tra un'immagine e la successiva

            time.sleep(2)   #ferma per due secondi la finestra
            screen.blit(gameOverImg,(0, 0)) #immagine di gameOver
            #creen.blit(punteggio,(500,600))
            pygame.display.update() #update della finestra di python
            #per salvare il punteggio nel file
            classifica.write(str(punteggio) + "\n")
            classifica.close()    # ricordate sempre di chiudere i file!
            time.sleep(3)   
            import menu   #dopo quattro secondi chiude la finestra, interrompe il programma in modo pulito
            
        else:
            macchinaFantasma = True
            for immagine,_ in esplosione.items():   #stampa della sequanza di esplosioni
                screen.blit(esplosione[immagine],(playerX-50, playerY-50))
                pygame.display.update()
                time.sleep(0.1)#tempo di attesa tra un'immagine e la successiva

    return cntCollisioni, macchinaFantasma

def spawnNitro(speed, cntSpeed, playerY, playerX, turboOn, nitroX, nitroY, punteggio):
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
            playerY += speed/2
        
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
        punteggio += 10 #incremento del punteggio
        #viene mostrato il logo del turbo e la fiamma
        screen.blit(turboScrittaImg,(0, 0))
        screen.blit(turboFiammaImg,(playerX, playerY+enemyHeight))

    return speed, playerY, turboOn, nitroX, nitroY, punteggio

def stampaVita(cntCollisioni):
    if cntCollisioni == 0:
        screen.blit(cuorePieno,(baseSchermo-xCuore1, spawn2))
        screen.blit(cuorePieno,(baseSchermo-xCuore2, spawn2))
        screen.blit(cuorePieno,(baseSchermo-xCuore3, spawn2))
    elif cntCollisioni == 1:
        screen.blit(cuoreVuoto,(baseSchermo-xCuore1, spawn2))
        screen.blit(cuorePieno,(baseSchermo-xCuore2, spawn2))
        screen.blit(cuorePieno,(baseSchermo-xCuore3, spawn2))
    elif cntCollisioni == 2:
        screen.blit(cuoreVuoto,(baseSchermo-xCuore1, spawn2))
        screen.blit(cuoreVuoto,(baseSchermo-xCuore2, spawn2))
        screen.blit(cuorePieno,(baseSchermo-xCuore3, spawn2))

def stampaPunteggio(punteggio):
    txtPunti = myFont.render(str(punteggio), False, BLACK)
    screen.blit(txtPunteggio , (punteggioX, punteggioY))
    screen.blit(txtPunti, (puntiX, punteggioY))

def stampaCespugli(cespuglioY1, cespuglioY2, cespuglioY3, cespuglioY4, cespuglioY5, speed):

    if cespuglioY1 <= spawnCespuglioIniziale:   #se l'ultimo cespuglio è ancora nelllo schermo
        cespuglioY1 += speed    #viene incrementata la sua y
    else:   #altrimenti vengono riposizionati tutti i cespugli per la partenza di una nuova fila
        cespuglioY1 = -100
        cespuglioY2 = -100
        cespuglioY3 = -100
        cespuglioY4 = -100
        cespuglioY5 = -100

    #spawn e incremento delle y dei diversi cespugli
    if cespuglioY1 >= spawnCespuglio1:
        cespuglioY2 += speed
        if cespuglioY1 >= spawnCespuglio2:
            cespuglioY3 += speed
            if cespuglioY1 >= spawnCespuglio3:
                cespuglioY4 += speed
                if cespuglioY1 >= spawnCespuglio4:
                    cespuglioY5 += speed

    #stampa dei cespugli
    screen.blit(cespuglio1,(cespuglioX1,cespuglioY1))
    screen.blit(cespuglio2,(cespuglioX1,cespuglioY2))
    screen.blit(cespuglio3,(cespuglioX1,cespuglioY3))
    screen.blit(cespuglio4,(cespuglioX2,cespuglioY4))
    screen.blit(cespuglio5,(cespuglioX2,cespuglioY5))

    return cespuglioY1, cespuglioY2, cespuglioY3, cespuglioY4, cespuglioY5


def main():
    global enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6

    spawnaSeconda = False

    ultimaX = baseSchermo / 2  #alla partenza del programma, se opencv non rileva oggetti rossi, la macchina viene posizionata a metà dello schermo (asse x)

    velocitaNemico = 10 * config.DIFFICOLTA

    #suono di sfondo e accensione auto
    audio = int((open("audio.txt","r").read())[0])
    if audio == 1:
        (pygame.mixer.Sound('suoni/Background.wav').play(-1)).set_volume(0.1)
        pygame.mixer.Sound('suoni/Accensione_auto.mp3').play()
        pygame.mixer.Sound('suoni/Rumore_auto.mp3').play(-1)

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

    speed = config.SPEED_INIZIALE * config.DIFFICOLTA  #velocità della auto nemiche
    cntSpeed = 0    #viene incrementata la velocità ogni volta che due linee di macchine scompaiono

    playerY = yStaticaGiocatore #y del giocatore inizializzata alla sua posizione standard

    cntCollisioni = 0   #contatore delle vite (quando arriva a 3 si perde)
    macchinaFantasma = False
    delay = 0   #delay per evitare collisioni quando l'auto è un fantasma

    punteggio = 0   #punteggio del giocatore

    #variabili per il posizionamento dei cespugli
    cespuglioY1 = -100
    cespuglioY2 = -100
    cespuglioY3 = -100
    cespuglioY4 = -100
    cespuglioY5 = -100

    while True:
        #GESTIONE DEI NEMICI
        enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed, punteggio = spawnNemici(enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, spawnaSeconda, velocitaNemico, fineSpawnNemiciRandom1, fineSpawnNemiciRandom2, fineSpawnNemiciRandom3, fineSpawnNemiciRandom4, fineSpawnNemiciRandom5, fineSpawnNemiciRandom6, veicoloRandom1, veicoloRandom2, veicoloRandom3, veicoloRandom4, veicoloRandom5, veicoloRandom6, speed, cntSpeed, turboOn, punteggio)

        #GESTIONE DEL COLORE ROSSO 
        playerX, ultimaX = cercaColore(ultimaX)

        #GESTIONE DEL GIOCATORE
        disegnaPlayer(playerX, playerY)

        #GESTIONE DEI CESPUGLI
        cespuglioY1, cespuglioY2, cespuglioY3, cespuglioY4, cespuglioY5 = stampaCespugli(cespuglioY1, cespuglioY2, cespuglioY3, cespuglioY4, cespuglioY5, speed)

        #GESTIONE DEL TURBO
        speed, playerY, turboOn, nitroX, nitroY, punteggio = spawnNitro(speed, cntSpeed, playerY, playerX, turboOn, nitroX, nitroY, punteggio)
        
        #GESTIONE DELLA VITA
        stampaVita(cntCollisioni)

        #GESTIONE DEL PUNTEGGIO
        stampaPunteggio(punteggio)

        #GESTIONE DELLE COLLISIONI
        if macchinaFantasma == False:
            cntCollisioni, macchinaFantasma = controlloCollisioni(playerX, playerY, enemyX, enemyY1, enemyY2, enemyY3, enemyX2, enemyY4, enemyY5, enemyY6, cntCollisioni, macchinaFantasma, punteggio, audio)

        if macchinaFantasma == True:    #se la macchina è un "fantasma"
            delay += 1  #viene incrementato il delay
            if delay > config.TEMPO_FANTASMA / speed:   #se il delay è maggiore di una certa soglia calcolata in rapporto alla speed
              macchinaFantasma = False  #la macchina ritorna "reale"
              delay = 0 #viene azzerato il delay

        clock.tick(60)  #60 fps
        pygame.display.update() #update della finestra di python

main()