import piglow
from time import sleep
from datetime import datetime

piglow.auto_update = True

show12hr = 1
ledbrightness = 10

piglow.all(0)

hourcount = 0
currenthour = 0

while True:
    time = datetime.now().time()
    print(str(time))
    hour = time.hour
    min = time.minute
    sec = time.second

    if show12hr == 1:
        if hour > 12:
            hour = hour - 12

    if currenthour != hour:
        hourcount = hour
        currenthour = hour

    arm3 = hour

    for x in range(6):
        piglow.led(13 + x, (arm3 & (1 << x)) * ledbrightness)

    arm2 = min

    for x in range(6):
        piglow.led(7 + x, (arm2 & (1 << x)) * ledbrightness)

    arm1 = sec

    for x in range(6):
        piglow.led(1 + x, (arm1 & (1 << x)) * ledbrightness)

    if hourcount != 0:
        sleep(0.5)
        piglow.white(ledbrightness)
        sleep(0.5)
        hourcount = hourcount - 1
    else:
        sleep(0.1)
