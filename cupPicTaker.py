'''
This file was used to take pictures for training custom models
-Carlos Cuartas
'''
import numpy as np
import cv2
import uuid   # Unique identifier
import os
import time

IMAGES_PATH = os.path.join('data', 'images') #/data/images
labels = ['Plastic_Cup']
number_imgs = 20

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
img_num = 0
while True:
    ret, frame = cap.read()
    if cv2.waitKey(10) & 0xFF == ord('c'):
        imgname = os.path.join(IMAGES_PATH, labels[0]+'.'+str(uuid.uuid1())+'.jpg')
        cv2.imwrite(imgname, frame)
        time.sleep(1)
    cv2.imshow('Image Collection', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()