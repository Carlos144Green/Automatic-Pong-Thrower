import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import digitalio
import board
import cv2
import numpy as np


def empty(a):
    pass
def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)
def make_240p():
    cap.set(3, 320)
    cap.set(4, 240)
def make_64p():
    cap.set(3, 240)
    cap.set(4, 64)
    

kit1 = ServoKit(channels=16, address=0x40, reference_clock_speed = 31000000, frequency=420)
kit2 = ServoKit(channels=16, address=0x41, reference_clock_speed = 31000000)

cv2.namedWindow("Slide Bar")  # Make window for trackbars
cv2.resizeWindow("Slide Bar", 700, 500)
cv2.createTrackbar("Hue Max", "Slide Bar", 145, 180, empty)
cv2.createTrackbar("Hue Min", "Slide Bar", 119, 180, empty)
cv2.createTrackbar("Sat Max", "Slide Bar", 186, 255, empty)
cv2.createTrackbar("Sat Min", "Slide Bar", 63, 255, empty)
cv2.createTrackbar("Val Max", "Slide Bar", 207, 255, empty)
cv2.createTrackbar("Val Min", "Slide Bar", 44, 255, empty)
cv2.createTrackbar("tweak1", "Slide Bar", 27, 100, empty)
cv2.createTrackbar("tweak2", "Slide Bar", 40, 100, empty)

cap = cv2.VideoCapture(0)
make_64p()    
    
_, img = cap.read()
rows, cols, _ = img.shape
x_medium = int(cols / 2)            # Object's x cords
y_medium = int(rows / 2)            # Object's y cords
xcenter = int(cols / 2)             # Screen x center
ycenter = int(rows / 2)             # Screen y center

kernel = np.ones([3, 3], np.uint8)  # Brush size
timeOut = 0
yawServo = 2
xposition = 90

kit2.servo[yawServo].angle = 0
time.sleep(.4)
kit2.servo[yawServo].angle = 180
time.sleep(.6)
kit2.servo[yawServo].angle = 90
time.sleep(1)

while True:
    success, img = cap.read()

    hue_M = cv2.getTrackbarPos("Hue Max", "Slide Bar")
    hue_m = cv2.getTrackbarPos("Hue Min", "Slide Bar")
    sat_M = cv2.getTrackbarPos("Sat Max", "Slide Bar")
    sat_m = cv2.getTrackbarPos("Sat Min", "Slide Bar")
    val_M = cv2.getTrackbarPos("Val Max", "Slide Bar")
    val_m = cv2.getTrackbarPos("Val Min", "Slide Bar")
    th1 = cv2.getTrackbarPos("tweak1", "Slide Bar")
    th2 = cv2.getTrackbarPos("tweak2", "Slide Bar")


    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)                                          # Convert to HSV
    #ranges = cv2.inRange(hsv, np.array([hue_m, sat_m, val_m]), np.array([hue_M, sat_M, val_M]))       # Get mask for color
    #ranges = cv2.inRange(hsv, np.array([0, 35, 197]), np.array([12, 255, 255]))       # Get range for balls
    ranges = cv2.inRange(hsv, np.array([0, 157, 146]), np.array([255, 255, 255]))       # Get range for cups
    ranges = cv2.morphologyEx(ranges, cv2.MORPH_OPEN, kernel)                           # Narc strays

    contours, rank = cv2.findContours(ranges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # Get table edges
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)         # Sort by area size

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt)>80:
           # print("owo")
           x_medium = int((x + x + w) / 2)
           break 
    
    tweak = 3
    
    cv2.line(img, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2) # Object x line
    cv2.line(img, (xcenter-tweak, 0), (xcenter-tweak, 480), (100, 100, 100), 2) # Object x top line
    cv2.line(img, (xcenter+tweak, 0), (xcenter+tweak, 480), (100, 100, 100), 2) # Object x bot line
    cv2.fillPoly(img,contours,(200,200,0))
    
    
    if x_medium < xcenter - tweak:
        if xposition + 1 < 180:
            xposition += 1
    elif x_medium > xcenter + tweak:
        if xposition - 1 > 0:
            xposition -= 1
    kit2.servo[yawServo].angle = xposition

    if timeOut > 10:
        xposition = 90
        timeOut = 0
        x_medium = int(cols / 2)            # Object's x cords
    if (xposition + 16 >180)|(xposition - 16 <0):
        timeOut += 1
    else:
        timeOut = 0
    
    
    
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # Resize
    cv2.imshow("kk", img)
    cv2.imshow("kk2", ranges)
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        GPIO.cleanup()
        break