import pygame
import math
import random
import time

width = 900
height = 700

pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()

def Fractal_Tree(x1, y1, theta, depth):
    if depth:
	rand_length=random.randint(1,10)
	rand_angle=random.randint(10,20)
        x2 = x1 + int(math.cos(math.radians(theta)) * depth * rand_length)
        y2 = y1 + int(math.sin(math.radians(theta)) * depth * rand_length)
	if ( depth < 5 ):
		clr = ( 0 , 255 , 0 )
	else:
		clr = ( 255, 255 , 255 )
        pygame.draw.line(screen, clr , (x1, y1), (x2, y2), 2)
        Fractal_Tree(x2, y2, theta - rand_angle, depth - 1)
        Fractal_Tree(x2, y2, theta + rand_angle, depth - 1)

Fractal_Tree( (width/2), (height-10) , -90, 14)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            pygame.quit()
            exit(0)
