import pygame
import sys
import cv2
import os
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WINDOW_HEIGHT =1024
WINDOW_WIDTH = 1024
pygame.init()
clock = pygame.time.Clock()


playerImg = pygame.image.load("veicoli\Player.png")
playerImg = pygame.transform.scale(playerImg,(75,150))
kernel = np.ones((8 ,8), np.uint8)
cap = cv2.VideoCapture(0)  
HAAR_PATH = "./"

# Face
FACE_HAAR = os.path.join(HAAR_PATH, "haarcascade_frontalcatface.xml")
face_cascade = cv2.CascadeClassifier(FACE_HAAR)

def cv2ImageToSurface(cv2Image):
    if cv2Image.dtype.name == 'uint16':
        cv2Image = (cv2Image / 256).astype('uint8')
    size = cv2Image.shape[1::-1]
    if len(cv2Image.shape) == 2:
        cv2Image = np.repeat(cv2Image.reshape(size[1], size[0], 1), 3, axis = 2)
        format = 'RGB'
    else:
        format = 'RGBA' if cv2Image.shape[2] == 4 else 'RGB'
        cv2Image[:, :, [0, 2]] = cv2Image[:, :, [2, 0]]
    surface = pygame.image.frombuffer(cv2Image.flatten(), size, format)
    return surface.convert_alpha() if format == 'RGBA' else surface.convert()

def face_tracking(frame):
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(image_gray, 1.3, 5)
    if len(faces) > 0:
        return faces[0]
    else:
        return 0,0,0,0

def main():
    global screen
    screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    screen.fill(BLACK)

    ultimaX = WINDOW_WIDTH / 2

    while True:
        screen.fill(BLACK)
        clock.tick(60)
       
       
        _, frame= cap.read()
        frame = cv2.flip(frame, 1)
        x, y, w, h = face_tracking(frame)

        if w > 30 and h > 30:
            if x == 0:
                x = ultimaX
            ultimaX = x 

        screen.blit(playerImg,(ultimaX, 10))
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

    pygame.destroyAllWindows()

if __name__=="__main__":
    main()