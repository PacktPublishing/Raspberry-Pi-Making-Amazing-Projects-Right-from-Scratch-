from grovepi import *
from grove_oled import *
import tweepy
import sqlite3
import datetime

dht_sensor_port = 7

oled_init()
oled_clearDisplay()
oled_setNormalDisplay()
oled_setVerticalMode()
time.sleep(.1)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

conn = sqlite3.connect('raspi_weather.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE weather(id INTEGER PRIMARY KEY, time TEXT,
                   	temp INTEGER, hum INTEGER)
''')


while True:
	   try:
		[ temp,hum ] = dht(dht_sensor_port,1)
		print "temp =", temp, "C\thumidity =", hum,"%" 	
		t = str(temp)
		h = str(hum)
                time = str(datetime.datetime.time(datetime.datetime.now()))
		
		oled_setTextXY(0,1)
		oled_putString("WEATHER")
		
		oled_setTextXY(2,0)
		oled_putString("Temp:")
		oled_putString(t+'C')
		
		oled_setTextXY(3,0)
		oled_putString("Hum :")
		oled_putString(h+"%")
                api.update_status("Temperature : " + t + ", " + "Humidity : " + h + "% ")
                cursor.execute('''INSERT INTO weather(time, temp, hum)
                                  VALUES(?,?,?)''', (time, t, h))
                       
        except (IOError,TypeError) as e:
		print "Error"
