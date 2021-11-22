# Python program to illustrate
# saving an operated video

# organize imports
import numpy as np
import cv2
import time
from adafruit_servokit import ServoKit

kit2 = ServoKit(channels=16, address=0x41, reference_clock_speed = 31000000)
yawServo = 2

kit2.servo[yawServo].angle = 0
time.sleep(.4)
kit2.servo[yawServo].angle = 180
time.sleep(.6)
kit2.servo[yawServo].angle = 90
time.sleep(1)

# This will return video from the first webcam on your computer.
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
i = 90
inc = 1
while(True):
    ret, frame = cap.read()
    # output the frame
    out.write(frame)
    
    if i > 179:
        inc = -1
    elif i < 1:
        inc = 1
    i+=inc
    
    kit2.servo[yawServo].angle = i
    
    # The original input frame is shown in the window
    cv2.imshow('Original', frame)
    
    # Wait for 'a' key to stop the program
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
