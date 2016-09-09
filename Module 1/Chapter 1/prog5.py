import turtle

t = turtle.Turtle()
disp=turtle.Screen()
t.color("black","yellow")
t.begin_fill()
while 1:
	t.forward(100)
	t.left(190)
	if abs(t.pos())<1:
		break
t.end_fill()
disp.exitonclick()
