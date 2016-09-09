from pygame.locals import *
import pygame
import random
import sys
import time

pygame.init()

fpsClock = pygame.time.Clock()

gameSurface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pi Snake')

wormcolor = pygame.Color(0, 255, 0)
backgroundcolor = pygame.Color(255, 255, 255)
snakecolor = pygame.Color(0, 0, 0)
textcolor = pygame.Color(255, 0, 0)

snakePos = [120,240]
snakeSeg = [[120,240],[120,220]]
wormPosition = [400,300]
wormSpawned = 1
Dir = 'D'
changeDir = Dir
Score = 0
Speed = 8
SpeedCount = 0

def finish():
    finishFont = pygame.font.Font(None, 56)
    msg = "Game Over! Score = " + str(Score)
    finishSurf = finishFont.render(msg, True, textcolor)
    finishRect = finishSurf.get_rect()
    finishRect.midtop = (400, 10)
    gameSurface.blit(finishSurf, finishRect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    exit(0)

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
	    exit(0)	
        elif event.type == KEYDOWN:
            if event.key == ord('d') or event.key == K_RIGHT:
                changeDir = 'R'
            if event.key == ord('a') or event.key == K_LEFT:
                changeDir = 'L'
            if event.key == ord('w') or event.key == K_UP:
                changeDir = 'U'
            if event.key == ord('s') or event.key == K_DOWN:
                changeDir = 'D'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
		pygame.quit()
    		exit(0)

    if changeDir == 'R' and not Dir == 'L':
        Dir = changeDir
    if changeDir == 'L' and not Dir == 'R':
        Dir = changeDir
    if changeDir == 'U' and not Dir == 'D':
        Dir = changeDir
    if changeDir == 'D' and not Dir == 'U':
        Dir = changeDir

    if Dir == 'R':
        snakePos[0] += 20
    if Dir == 'L':
        snakePos[0] -= 20
    if Dir == 'U':
        snakePos[1] -= 20
    if Dir == 'D':
        snakePos[1] += 20

    snakeSeg.insert(0,list(snakePos))
    if snakePos[0] == wormPosition[0] and snakePos[1] == wormPosition[1]:
        wormSpawned = 0
        Score = Score + 1
        SpeedCount = SpeedCount + 1
        if SpeedCount == 5 :
            SpeedCount = 0
            Speed = Speed + 1
    else:
        snakeSeg.pop()

    if wormSpawned == 0:
        x = random.randrange(1,40)
        y = random.randrange(1,30)
        wormPosition = [int(x*20),int(y*20)]
    wormSpawned = 1
	
    gameSurface.fill(backgroundcolor)
    for position in snakeSeg:
        pygame.draw.rect(gameSurface,snakecolor,Rect(position[0], position[1], 20, 20))
    pygame.draw.circle(gameSurface,wormcolor,(wormPosition[0]+10, wormPosition[1]+10), 10, 0)
    pygame.display.flip()
    if snakePos[0] > 780 or snakePos[0] < 0:
        finish()
    if snakePos[1] > 580 or snakePos[1] < 0:
        finish()
    for snakeBody in snakeSeg[1:]:
        if snakePos[0] == snakeBody[0] and snakePos[1] == snakeBody[1]:
            finish()
    fpsClock.tick(Speed)
