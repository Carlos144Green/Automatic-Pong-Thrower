import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import digitalio
import board
import csv

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

    return distance


kit1 = ServoKit(channels=16, address=0x40, reference_clock_speed = 31000000, frequency=420)
kit2 = ServoKit(channels=16, address=0x41, reference_clock_speed = 31000000)
#GPIO.setmode(GPIO.BOARD)
time.sleep(1)				# delay for 1 seconds


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

positiveData = []
negativeData = []

clean = input("do you want to start a new file? \n Y/N: ")
if clean != 'Y':     
    with open('PositiveData.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = '\t')
        next(csv_reader)
        for line in csv_reader:
            positiveData.append(line)
        print(positiveData)
                
with open('PositiveData.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter = '\t')
    writer.writerow(["Distance","Power"])
    for line in positiveData:
        writer.writerow(line)
        
    while True:
        power = 200
        distance = 200
        while (power > 50) or (distance > 150):
            power = int(input("Enter Power Level 1-50: "))
            distance = ultra_sonic()
            if power == 1:
                writer.writerow([old_distance,old_power])
                distance = 1000
            print ("Distance : %.1f" % distance)
 
        if power ==2:
            break
        kit2.servo[shootServo].angle = 114
        time.sleep(.5)
        kit1.servo[PWM].angle = power
        time.sleep(2)
        kit2.servo[shootServo].angle = shootMax

        time.sleep(1)
        kit1.servo[PWM].angle = 0
        kit2.servo[shootServo].angle = shootMin
     
        old_power = power
        old_distance = distance

        
