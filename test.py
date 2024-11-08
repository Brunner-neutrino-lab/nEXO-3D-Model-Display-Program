
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import numpy as np
from numpy.random import exponential #for exponential distribution (distribution of distance between events in Poisson process)


wallGPIO = 17 #physical/board pin 11
floorGPIO = 27 #physical/board pin 13
redGPIO = 9 #physical/board pin 21
greenGPIO = 11 #physical/board pin 23
blueGPIO = 25 #physical/board pin 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(wallGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(floorGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(redGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(greenGPIO, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blueGPIO, GPIO.OUT, initial=GPIO.LOW)

RED = GPIO.PWM(redGPIO,100)
GREEN = GPIO.PWM(greenGPIO,100)
BLUE = GPIO.PWM(blueGPIO,100)

RED.start(0)
GREEN.start(0)
BLUE.start(0)

flashtime = 1 #s that LEDs should flash

GPIO.output(wallGPIO, GPIO.HIGH)


# background
print("background")
RED.ChangeDutyCycle(0)
GREEN.ChangeDutyCycle(240/255 * 100)
BLUE.ChangeDutyCycle(40/255 * 100)
time.sleep(flashtime)

# 0vbb
print("0vbb")
RED.ChangeDutyCycle(255/255 * 100)
GREEN.ChangeDutyCycle(69/255 * 100)
BLUE.ChangeDutyCycle(0)  
time.sleep(flashtime)

# solar v
print("solar v")
RED.ChangeDutyCycle(245/255 * 100)
GREEN.ChangeDutyCycle(235/255 * 100)
BLUE.ChangeDutyCycle(10/255 * 100)   
time.sleep(flashtime)

# 2vbb
print("2vbb")
RED.ChangeDutyCycle(255/255 * 100)
GREEN.ChangeDutyCycle(20/255 * 100)
BLUE.ChangeDutyCycle(147/255 * 100)  
time.sleep(flashtime)

# xenon 137
print("Xe137")
RED.ChangeDutyCycle(200/255 * 100)
GREEN.ChangeDutyCycle(200/255 * 100)
BLUE.ChangeDutyCycle(200/255 * 100)
time.sleep(flashtime)


RED.ChangeDutyCycle(0)
GREEN.ChangeDutyCycle(0)
BLUE.ChangeDutyCycle(0)
GPIO.output(floorGPIO, GPIO.LOW)
GPIO.output(wallGPIO, GPIO.LOW)
    
GPIO.cleanup()

