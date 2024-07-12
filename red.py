import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import numpy as np
from numpy.random import exponential #for exponential distribution (distributio>


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

GPIO.output(redGPIO, GPIO.HIGH)
time.sleep(2)
GPIO.output(redGPIO,GPIO.LOW)
GPIO.output(greenGPIO,GPIO.HIGH)
time.sleep(2)
GPIO.cleanup()
