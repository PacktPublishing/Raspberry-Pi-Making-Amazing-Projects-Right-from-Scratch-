# Sierpinski Triangle and Koch Snowflake

import pygame,math,sys
red = 255, 0, 0
black = 0, 0, 0
yellow=255,255,0
a = 100, 300
b=400, 600
le = 200
resolution = 800, 800
s = pygame.display.set_mode(resolution)
pygame.display.set_caption("Sierpinski Triangle & Koch snowflake")
pygame.display.update()


def angle(le, state):
	e = lines(le, state, 0, a)
	i = lines(le, state, 120, e)
	h = lines(le, state, 240, i)


def lines(le, state, angle, p):
	if state == 0:
		e = cordinates(le, angle, p)
		pygame.draw.line(s, red, p, e)
		return e
	else:
		h = lines(le / 2, state - 1, angle, p)
		i = lines(le / 2, state - 1, angle + 120, h)
		j = lines(le / 2, state - 1, angle + 240, i)
		k = cordinate(le, angle , j)
		return k

def angles(le, state):
	e = line(le, state, 0, b)
	i = line(le, state, 120, e)
	h = line(le, state, 240, i)
	
	
def line(le, state, angle, p):
	if state == 0:
		e = cordinates(le, angle, p)
		pygame.draw.line(s, yellow, p, e)
		pygame.display.update()
		return e
	else:
		h = line(le / 3, state - 1, angle, p)
		i = line(le / 3, state - 1, angle - 60, h)
		j = line(le / 3, state - 1, angle + 60, i)
		k = line(le / 3, state - 1, angle, j)
		return k
		

def cordinate(le, angle, a):
	angle = angle * 3.14 / 180
	w = math.cos(angle) * le
	h = math.sin(angle) * le
	return a[0] + w, a[1] - h

def cordinates(le, angle, b):
	angle = angle * 3.14 / 180
	w = math.cos(angle) * le
	h = math.sin(angle) * le
	return b[0] + w, b[1] - h

def quite():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	return 0


while 1:
	for i in range(5):
		angle(le, i)
		angles(le, i)
		pygame.display.update()
		pygame.time.delay(300)
		s.fill(black)
		quite()