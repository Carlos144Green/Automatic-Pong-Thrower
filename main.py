import RPi.GPIO as GPIO			# using Rpi.GPIO module
from time import sleep			# import function sleep for delay

GPIO.setwarnings(False)			# enable warning from GPIO
GPIO.setmode(GPIO.BOARD)

AN1 = 33				# set pwm1 pin on MD10-hat
DIG2 = 18				# set dir2 pin on MD10-Hat
DIG1 = 37				# set dir1 pin on MD10-Hat

GPIO.setup(AN1, GPIO.OUT)		# set pin as output
GPIO.setup(DIG2, GPIO.OUT)		# set pin as output
GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
sleep(1)				# delay for 1 seconds
p1 = GPIO.PWM(AN1, 100)			# set pwm for M1

GPIO.output(DIG1, GPIO.HIGH)		# set DIG1 as HIGH, M1B will turn ON
GPIO.output(DIG2, GPIO.LOW)		# set DIG2 as HIGH, M2B will turn ON


try:					
  while True:
   p1.start(100)			# set speed for M1 at 100%
   sleep(5)				#delay for 2 second
   p1.start(30)			# set speed for M1 at 100%
   sleep(5)				#delay for 2 second
   p1.start(0)			# set speed for M1 at 100%
   sleep(5)	

except:					# exit programe when keyboard interupt
   p1.start(0)				# set speed to 0

					# Control+x to save file and exit
