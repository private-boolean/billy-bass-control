from gpiozero.pins.mock import MockFactory
from gpiozero import Device, Button, LED, Motor
from time import sleep
import time

import platform

# Set the default pin factory to a mock factory if running on Windows. (Assume 'Linux' means Raspberry Pi)
if 'Windows' == platform.system():
    Device.pin_factory = MockFactory()

mouth = LED(23)
body = LED(24)
tail = LED(25)

runningTime = 1.5 # seconds

mouthPattern = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
bodyPattern  = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
tailPattern  = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0]

timeStart = time.time()
currTime = time.time()
elapsedTime = currTime - timeStart

while elapsedTime < runningTime:
    print("t = %fs" % (elapsedTime))
    
    currTime = time.time()
    elapsedTime = currTime - timeStart


