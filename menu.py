from numpy import diff
import pygame 
import sys 
import tkinter as tk
import time
from pygame import mixer
import subprocess


root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
# initializing the constructor 
pygame.init() 
# opens up a window 
screen = pygame.display.set_mode((width, height)) 
# white color 
color = (255,255,255) 

# light shade of the button 
color_light = (80,110,255) 

# dark shade of the button 
color_dark = (64,0,255) 

logo = pygame.image.load("immaginiGioco/logo.png")
sfondo = pygame.image.load("immaginiGioco/sfondoMenu.png")
sfondo = pygame.transform.smoothscale(sfondo,(width,height))

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 
bigfont = pygame.font.SysFont('Arial', 70)
grassetto= pygame.font.SysFont('Arial', 80,20)

#volume images
volumeDisattivato = pygame.image.load("ImmaginiGioco/VolumeDisattivato.png")
volumeAttivo = pygame.image.load("ImmaginiGioco/VolumeAttivo.png")
volumeDisattivato=pygame.transform.scale(volumeDisattivato,(50, 50))
volumeAttivo=pygame.transform.scale(volumeAttivo,(50, 50))

#funzione per fare partire il gioco con la lettura del colore rosso 
def playColore(difficolta,audio):
    diff = open("difficolta.txt", "w")
    diff.write(str(difficolta))
    diff.close()
    audioTxt = open("audio.txt","w")
    if audio:
        audioTxt.write("1")
    else:
        audioTxt.write("2")
    audioTxt.close()
    import SpeedHighwayColore
    

#funzione per fare partire il gioco con la lettura della posizione della faccia
def playFaccia(difficolta,audio):
    diff = open("difficolta.txt", "w")
    diff.write(str(difficolta))
    diff.close()
    audioTxt = open("audio.txt","w")
    if audio:
        audioTxt.write("1")
    else:
        audioTxt.write("2")
    audioTxt.close()
    import SpeedHighwayColore


def animazioneLogo():
    x=width
    while x>width/2-267:
        x=x-15
        screen.blit(sfondo,(0,0))
        screen.blit(logo,(x, (height)/13))  #la macchina viene impostata alla x rilevata da opencv
        pygame.display.update()   


def ritornaClassifica():
    classifica = open("classifica.txt", "r").read()
    classifica = classifica.split('\n')
    classifica.pop()
    for k in range (len(classifica)):
        classifica[k] = int(classifica[k])

    classifica.sort(reverse=True)
    print(classifica[0:5])
    return classifica[0:5]

#per mostrare la classifica
def showClassifica(txtExit):
    pygame.draw.rect(screen,(0,60,0), [0, 0, width, height])
    pygame.draw.rect(screen,color_dark, [30, 30, 90, height/13])
    screen.blit(txtExit , (40, 45))
    classifica=ritornaClassifica()

    if len(classifica) >= 5:

        for k in range (0,5):
            if(k==0):
                txtClas = grassetto.render(str(classifica[k]), True, color)
            else:
                txtClas = bigfont.render(str(classifica[k]), True, color)
            lung= len(str(classifica[k]))

            if k > 0:
                screen.blit(txtClas , ((width/2-(20*lung)), 80*(k+1)))
            else:
                screen.blit(txtClas , ((width/2-(25*lung)), 80*(k+1)))
        
    

    #per tornare al menù
    while True:
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if 30 <= mouse[0] <= 90 and 30 <= mouse[1] <= height/13:
                    screen.blit(sfondo,(0,0))
                    animazioneLogo()
                    return
        
        if 30 <= mouse[0] <= 90 and 30 <= mouse[1] <= height/13:
            pygame.draw.rect(screen,color_light, [30, 30, 90, height/13])
            screen.blit(txtExit , (40, 45))
        else:
            pygame.draw.rect(screen,color_dark, [30, 30, 90, height/13])
            screen.blit(txtExit , (40, 45))


        pygame.display.update()
  

def animazioneTasti(mouse, txtPlay, easy, txtDifficolta, txtHard, txtEasy, tipe, txtType, txtFrecce, txtColor, txtQuit, txtClassifica):
    #animazione tasto play
        if width/2-150 <= mouse[0] <= width/2+150 and (height*5)/13 <= mouse[1] <= (height*5)/13+((height*1)/13): 
            pygame.draw.rect(screen,color_light,[width/2-150, (height*5)/13, 300, (height*1)/13])    
            screen.blit(txtPlay , (width/2-30,(height*5)/13+15))
        else:
            pygame.draw.rect(screen,color_dark, [width/2-150, (height*5)/13, 300, (height*1)/13])
            screen.blit(txtPlay , (width/2-30,(height*5)/13+15))
        

        #animazione tasto difficoltà
        if width/2-150 <= mouse[0] <= width/2+150 and (height*7)/13<= mouse[1] <= (height*7)/13+((height*1)/13): 
            if(easy==True):
                pygame.draw.rect(screen,color_light, [width/2-150, (height*7)/13, 300, (height*1)/13])
                screen.blit(txtDifficolta , (width/2-130,(height*7)/13+15))
                screen.blit(txtHard , (width/2,(height*7)/13+15))
            #difficoltà difficile
            else:
                pygame.draw.rect(screen,color_light, [width/2-150, (height*7)/13, 300, (height*1)/13])
                screen.blit(txtDifficolta , (width/2-130,(height*7)/13+15))
                screen.blit(txtEasy , (width/2,(height*7)/13+15)) 
        else:
            if(easy==True):
                pygame.draw.rect(screen,color_dark, [width/2-150, (height*7)/13, 300, (height*1)/13])
                screen.blit(txtDifficolta , (width/2-130,(height*7)/13+15))
                screen.blit(txtHard , (width/2,(height*7)/13+15))
            #difficoltà difficile
            else:
                pygame.draw.rect(screen,color_dark, [width/2-150, (height*7)/13, 300, (height*1)/13])
                screen.blit(txtDifficolta , (width/2-130,(height*7)/13+15))
                screen.blit(txtEasy , (width/2,(height*7)/13+15)) 


        #animazione tasto per cambiare la modalità
        if width/2-150 <= mouse[0] <= width/2+150 and (height*9)/13 <= mouse[1] <= (height/2)+(((height*9)/13)/2):
            if tipe==True:
                pygame.draw.rect(screen,color_light, [width/2-150, (height*9)/13, 300, (height*1)/13])
                screen.blit(txtType , (width/2-100,(height*9)/13+15))
                screen.blit(txtFrecce , (width/2,(height*9)/13+15))
            else:
                pygame.draw.rect(screen,color_light, [width/2-150, (height*9)/13, 300, (height*1)/13])
                screen.blit(txtType , (width/2-100,(height*9)/13+15))
                screen.blit(txtColor , (width/2,(height*9)/13+15))
        else:
            if tipe==True:
                pygame.draw.rect(screen,color_dark, [width/2-150, (height*9)/13, 300, (height*1)/13])
                screen.blit(txtType , (width/2-100,(height*9)/13+15))
                screen.blit(txtFrecce , (width/2,(height*9)/13+15))
            else:
                pygame.draw.rect(screen,color_dark, [width/2-150, (height*9)/13, 300, (height*1)/13])
                screen.blit(txtType , (width/2-100,(height*9)/13+15))
                screen.blit(txtColor , (width/2,(height*9)/13+15))

        #animazione classifica
        if width/2-150 <= mouse[0] <= width/2+150 and (height*11)/13 <= mouse[1] <= (height*11)/13+((height*1)/13):
            pygame.draw.rect(screen,color_light,[width/2-150, (height*11)/13,300,(height*1)/13])
            screen.blit(txtClassifica , (width/2-75, (height*11)/13+15))
        else:
            pygame.draw.rect(screen,color_dark,[width/2-150, (height*11)/13,300,(height*1)/13])
            screen.blit(txtClassifica , (width/2-75, (height*11)/13+15))

        #animazione tasto quit
        if (width*3)/4 <= mouse[0] <= (width*3)/4+140 and (height*11)/13 <= mouse[1] <= (height*11)/13+40: 
            pygame.draw.rect(screen,color_light,[(width*3)/4, (height*11)/13,140,(height*1)/13])
            screen.blit(txtQuit , ((width*3)/4+40, (height*11)/13+15))
        else:
            pygame.draw.rect(screen,color_dark,[(width*3)/4, (height*11)/13,140,(height*1)/13])
            screen.blit(txtQuit , ((width*3)/4+40, (height*11)/13+15))

    



def main():
    #background music
    pygame.mixer.Sound('suoni/Background.wav').play(-1)

    # rendering a text written in 
    # this font 
    txtPlay=  smallfont.render('PLAY' , True , color)

    txtDifficolta=  smallfont.render('Difficulty:' , True , color)
    txtHard=smallfont.render('< Hard >' , True , color)
    txtEasy=smallfont.render('< Easy >' , True , color)

    txtType =smallfont.render('Type:' , True , color)
    txtColor =smallfont.render('< Color >' , True , color)
    txtFrecce =smallfont.render('< Frecce >' , True , color)

    txtQuit = smallfont.render('Quit' , True , color)

    txtClassifica= smallfont.render('Classification', True, color)

    txtExit = smallfont.render("< Exit", True, color)

   
    easy=True
    tipe=True

    #print background
    screen.blit(sfondo,(0,0))
    #print the logo
    #pygame.mixer.Sound('suoni\background.wav').play(-1)
    animazioneLogo()
    #screen.blit(logo,(width/2-267, (height*1)/13))  #la macchina viene impostata alla x rilevata da opencv
    
    audio=True
    #print audio image
    screen.blit(volumeAttivo,(50,height-150))

    #draw the rect of choose
    #rect for play colore
    pygame.draw.rect(screen,color_dark, [width/2-150, (height*5)/13, 300, (height*1)/13])

    #draw the choose for difficulty
    pygame.draw.rect(screen,color_dark, [width/2-150, (height*7)/13, 300, (height*1)/13])

    #draw the choose for tipe
    pygame.draw.rect(screen,color_dark, [width/2-150, (height*9)/13, 300, (height*1)/13])

    #rettangolo per la classifica
    pygame.draw.rect(screen,color_dark,[width/2-150, (height*11)/13,300,(height*1)/13])

    #rect for quit
    pygame.draw.rect(screen,color_dark,[(width*3)/4, (height*11)/13,140,(height*1)/13]) 

    


    # superimposing the text onto our button 
    #per aggiungere le scritte sui pulsanti
    #play
    screen.blit(txtPlay , (width/2-35,(height*5)/13+15))
    #difficoltà
    screen.blit(txtDifficolta , (width/2-120,(height*7)/13+15))
    screen.blit(txtEasy , (width/2,(height*7)/13+15))
    #tipologia
    screen.blit(txtType , (width/2-100,(height*9)/13+15))
    screen.blit(txtColor , (width/2,(height*9)/13+15))
    #classifica
    screen.blit(txtClassifica , (width/2-75, (height*11)/13+15))
    #quit
    screen.blit(txtQuit , ((width*3)/4+50, (height*11)/13+15))




    while True: 
        mouse = pygame.mouse.get_pos() 
       
        for ev in pygame.event.get(): 
            
            if ev.type == pygame.QUIT: 
                pygame.quit() 
                
            #checks if a mouse is clicked 
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                
                #if the mouse is clicked on the 
                # button the game is terminated 
                #per vedere se il mouse ha clicato su quit
                #per vedere se il mouse ha cliccato su play
                if width/2-150 <= mouse[0] <= width/2+150 and (height*5)/13 <= mouse[1] <= (height*5)/13+((height*1)/13):
                    if(tipe==True):
                        if(easy==True):
                            playColore(2,audio)
                        else:
                            playColore(1,audio)   

                    else:
                        if(easy==True):
                            playFaccia(2,audio)
                        else:
                            playFaccia(1,audio)

                #si chiede se sto cambiando la difficoltà
                if width/2-150 <= mouse[0] <= width/2+150 and (height*7)/13<= mouse[1] <= (height*7)/13+((height*1)/13):
                    #difficoltà facile
                    if(easy==True):
                        pygame.draw.rect(screen,color_dark, [width/2-150, (height*7)/13, 300, (height*1)/13])
                        screen.blit(txtDifficolta , (width/2-130,(height*7)/13+15))
                        screen.blit(txtHard , (width/2,(height*7)/13+15))
                        easy=False 
                    #difficoltà difficile
                    else:
                        pygame.draw.rect(screen,color_dark, [width/2-150, (height*7)/13, 300, (height*1)/13])
                        screen.blit(txtDifficolta , (width/2-130,(height*7)/13+15))
                        screen.blit(txtEasy , (width/2,(height*7)/13+15)) 
                        easy=True

                #si chiede se sto cambiando modalità
                if width/2-150 <= mouse[0] <= width/2+150 and (height*9)/13 <= mouse[1] <= (height/2)+(((height*9)/13)/2):
                    if tipe==True:
                        pygame.draw.rect(screen,color_dark, [width/2-150, (height*9)/13, 300, (height*1)/13])
                        screen.blit(txtType , (width/2-100,(height*9)/13+15))
                        screen.blit(txtFrecce , (width/2,(height*9)/13+15))
                        tipe=False
                    else:
                        pygame.draw.rect(screen,color_dark, [width/2-150, (height*9)/13, 300, (height*1)/13])
                        screen.blit(txtType , (width/2-100,(height*9)/13+15))
                        screen.blit(txtColor , (width/2,(height*9)/13+15))
                        tipe=True

                #si chiede se ho premuto la classifica
                if width/2-150 <= mouse[0] <= width/2+150 and (height*11)/13 <= mouse[1] <= (height*11)/13+40:
                    showClassifica(txtExit)
                    if audio == True:
                        screen.blit(volumeAttivo,(50,height-150))
                    else:
                        screen.blit(volumeDisattivato,(50,height-150))

                #si chiede se ho premuto il quit
                if (width*3)/4 <= mouse[0] <= (width*3)/4+140 and (height*11)/13 <= mouse[1] <= (height*11)/13+40: 
                    pygame.quit()
                
                #si chiede se ho premuto per disattivare l'audio
                if 50 <= mouse[0] <= 100 and height-150 <= mouse[1] <= height-50:
                    if audio==True:
                        pygame.mixer.stop()
                        screen.blit(sfondo,(0,0))
                        screen.blit(volumeDisattivato,(50,height-150))
                        screen.blit(logo,(width/2-267, (height)/13))
                        audio=False
                    else:
                        pygame.mixer.Sound('suoni/Background.wav').play(-1)
                        screen.blit(sfondo,(0,0))
                        screen.blit(volumeAttivo,(50,height-150))
                        screen.blit(logo,(width/2-267, (height)/13))
                        audio=True

        animazioneTasti(mouse, txtPlay, easy, txtDifficolta, txtHard, txtEasy, tipe, txtType, txtColor, txtFrecce, txtQuit, txtClassifica)
        pygame.display.update() 


main()