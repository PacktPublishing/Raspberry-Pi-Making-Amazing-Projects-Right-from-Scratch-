#python code to create a Sierpinski triangle

import pygame, sys
from pygame.locals import*
from math import sqrt

pygame.init()
clock=pygame.time.Clock()

disp = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Sierpinski triangle')

b = (0, 0, 0)
w = (255, 255, 255)

disp.fill(w)

l1 = []
l2 = []
l3 = []
l4 = []

#return midpoint of a line
def midpoint((x1,y1),(x2,y2)):
  return( (x1+x2)/2), ((y1+y2)/2)

def iteration(l):
  p1 = midpoint(l[0], l[1])
  p2 = midpoint(l[1], l[2])
  p3 = midpoint(l[2], l[0])
  pygame.draw.polygon(disp, b, (p1,p2,p3),1)
  l1.append(l[0])
  l1.append(p1)
  l1.append(p3)
  l2.append(p1)
  l2.append(l[1])
  l2.append(p2)
  l3.append(p2)
  l3.append(l[2])
  l3.append(p3)
  return l1, l2, l3

r = pygame.Rect(50, 100, 200, 150*sqrt(3))
# three coordinates of first triangle
l = [(r[0], r[1]), (r[0]+2*r[2], r[1]),(r[0]+r[2], r[1]+r[3])]
pygame.draw.polygon(disp, b, l, 1)

l4 =[[l]]
for change in range(6):# no of iterations
  c = l4
  l4 = []
  for j in c: 
    m = j
    for i in range(len(m)):
      l1 = []
      l2 = []
      l3 = []
      v = iteration(m[i])
      l4.append(v)
  pygame.display.update()
  clock.tick(1)

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()