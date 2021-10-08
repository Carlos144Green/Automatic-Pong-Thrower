import time
import Jetson.GPIO as GPIO
from adafruit_servokit import ServoKit
GPIO.setmode(GPIO.BOARD)
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16, reference_clock_speed = 31000000)

pitchMax =100
pitchMin =30

shootMin = 0
shootMax = 180

shootServo = 0
pitchServo = 1


kit.servo[pitchServo].angle = pitchMin
kit.servo[shootServo].actuation_range = 180
kit.servo[shootServo].set_pulse_width_range(400, 2000)


while True:
	kit.servo[shootServo].angle = shootMax

	print("max")
	time.sleep(2)
	kit.servo[shootServo].angle = shootMin

	print("min")
	time.sleep(2)
	
