# Fractal Koch

import turtle

def koch(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
           koch(t, order-1, size/3)
           t.left(angle)

def main():
   	myTurtle = turtle.Turtle()
   	myWin = turtle.Screen()
	myTurtle.penup()
	myTurtle.backward(250)
	myTurtle.pendown()
	koch ( myTurtle, 4, 500 )
   	myWin.exitonclick()

main()
