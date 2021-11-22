import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import digitalio
import board
import csv
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def interpolate(x,y,distance):
    p1 = np.polyfit(x,y,1)
    p2 = np.polyfit(x,y,2)
    p3 = np.polyfit(x,y,3)
    p4 = np.polyfit(x,y,4)
    p5 = np.polyfit(x,y,5)
    p6 = np.polyfit(x,y,6)

    xp = np.linspace(0,150,1000)
    distance = np.polyval(p3,distance)
    return distance

def ultra_sonic():
    GPIO_TRIGGER.value= True
    time.sleep(0.00001)
    GPIO_TRIGGER.value= False
    start = time.time()

    while GPIO_ECHO.value == 0:
      start = time.time()

    while GPIO_ECHO.value == 1:
      stop = time.time()
    
    elapsed = stop-start
    distance = elapsed * 34300
    distance = round(distance / 2, 6)

    print ("Distance : %.1f" % distance)
    return distance



kit1 = ServoKit(channels=16, address=0x40, reference_clock_speed = 31000000, frequency=420)
kit2 = ServoKit(channels=16, address=0x41, reference_clock_speed = 31000000)
#GPIO.setmode(GPIO.BOARD)
time.sleep(1)   # delay for 1 seconds

PWM = 6
shootMin = 0
shootMax = 180
shootServo = 0
yawServo = 2

kit2.servo[shootServo].set_pulse_width_range(400, 2000)
kit1.servo[PWM].set_pulse_width_range(0, 2000)

kit2.servo[shootServo].angle = shootMin
kit1.servo[PWM].angle = 0

sig1 = digitalio.DigitalInOut(board.D20)
sig2 = digitalio.DigitalInOut(board.D21)
sig1.direction = digitalio.Direction.OUTPUT
sig2.direction = digitalio.Direction.OUTPUT

GPIO_TRIGGER = digitalio.DigitalInOut(board.D11)
GPIO_ECHO = digitalio.DigitalInOut(board.D8)

GPIO_TRIGGER.direction = digitalio.Direction.OUTPUT
GPIO_ECHO.direction = digitalio.Direction.INPUT

GPIO_TRIGGER.value= False

sig2.value= True
sig1.value= False
kit2.servo[yawServo].angle = 90

File = './PositiveData.csv'
raw = pd.read_csv(File, delimiter="\t")
x = raw.iloc[:,0]
y = raw.iloc[:,1]
n = len(x)


while True:

    power = 200
    distance = 200
    while (power > 50) or (distance > 155):
        shoot = input("shoot?: ")
        
        distance = ultra_sonic()
        power = interpolate(x,y,distance)
    
    kit2.servo[shootServo].angle = 114
    time.sleep(.5)
    kit1.servo[PWM].angle = power+.5
    time.sleep(2)
    kit2.servo[shootServo].angle = shootMax

    time.sleep(1)
    kit1.servo[PWM].angle = 0
    kit2.servo[shootServo].angle = shootMin

    
