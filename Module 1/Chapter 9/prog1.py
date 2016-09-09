from grovepi import *
from grove_oled import *

dht_sensor_port = 7

oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)

while True:
	   try:
		[ temp,hum ] = dht(dht_sensor_port,1)
		print "temp =", temp, "C\thumidity =", hum,"%" 	
		t = str(temp)
		h = str(hum)
		
		oled_setTextXY(0,1)
		oled_putString("WEATHER")
		
		oled_setTextXY(2,0)
		oled_putString("Temp:")
		oled_putString(t+'C')
		
		oled_setTextXY(3,0)
		oled_putString("Hum :")
		oled_putString(h+"%")
        except (IOError,TypeError) as e:
		print "Error"

