'''
Author: Michele Alladio, Samuele Forneris, Alessandro Seimandi, Nicolò La Valle
Descrizione:
costanti utilizzate all'interno del videogioco
'''

#costanti generiche (adattate per la presona che ha creato il programma)
ALTEZZA = 700   #altezza schermata
BASE = 1400 #base schermata

Y_PREDEFINITA = 450 #y della macchina nella schermata PyGame

SPAWN_1 = 80    #altezza che, una volta raggiunta dalla prima auto, fa spawnare la seconda macchina della fila
SPAWN_2 = 100   #altezza che, una volta raggiunta dalla prima auto, fa spawnare la terza macchina della fila
SPAWN_3 = 900   #altezza che, una volta raggiunta dalla prima auto, fa spawnare la prima macchina della fila

#coordinate per il corretto spawn dei nemici nelle corsie
X_SPAWN_CORSIA_1 = 450 
X_SPAWN_CORSIA_2 = 650
X_SPAWN_CORSIA_3 = 860

ENEMY_WIDTH = 82    #base macchina nemico
ENEMY_HEIGHT = 140  #altezza macchina nemico

Y_FUORI_SCHERMO = -100  #coordinata di convenzione per far sparire immagini dalla schermata

TEMPO_FANTASMA = 800    #tempo che verrà diviso per la speed corrente per evitare collisioni quando l'auto è "fantasma"

#costanti per il posizionamento dei cuori
X_CUORE_1 = 280
X_CUORE_2 = 200
X_CUORE_3 = 120

#costanti per il posizionamento del punteggio
PUNTEGGIOX = 1100
PUNTEGGIOY = 30
PUNTIX = 1260

#costanti per il posizionamento dei cespugli
CESPUGLIO_X1 = 100
CESPUGLIO_X2 = 1200
SPAWN_CESPUGLIO1 = 130
SPAWN_CESPUGLIO2 = 360
SPAWN_CESPUGLIO3 = 500
SPAWN_CESPUGLIO4 = 730
SPAWN_CESPUGLIO_INIZIALE = 1500

#limiti prestabiliti per lo spawn della seconda riga di nemici
LIMITE1 = 300
LIMITE2 = 100

#costanti
SCORE = 0   #punteggio
SPEED_INIZIALE = 8  #velocità iniziale

DIFFICOLTA = int((open("difficolta.txt", "r").read())[0])
