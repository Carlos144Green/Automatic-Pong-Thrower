import time
import Jetson.GPIO as GPIO
from adafruit_servokit import ServoKit
import digitalio
import board

kit1 = ServoKit(channels=16, address=0x40, reference_clock_speed = 31000000, frequency=420)
kit2 = ServoKit(channels=16, 	address=0x41, reference_clock_speed = 31000000)
#GPIO.setmode(GPIO.BOARD)
time.sleep(1)				# delay for 1 seconds


PWM = 6
kit1.servo[PWM].angle = 180
shootMin = 0
shootMax = 180
shootServo = 0
kit2.servo[shootServo].set_pulse_width_range(400, 2000)


sig1 = digitalio.DigitalInOut(board.D24)
sig2 = digitalio.DigitalInOut(board.D26)
sig1.direction = digitalio.Direction.OUTPUT
sig2.direction = digitalio.Direction.OUTPUT

sig2.value= True
sig1.value= False

while True:

	kit2.servo[shootServo].angle = shootMax
	print("max")
	time.sleep(2)

	kit2.servo[shootServo].angle = shootMin

	print("min")
	time.sleep(2)
