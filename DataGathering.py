import numpy as np
import cv2
import uuid   # Unique identifier
import os
import time

IMAGES_PATH = os.path.join('data', 'images') #/data/images
labels = ['Plastic_Cup']
number_imgs = 20

cap = cv2.VideoCapture(0)
for label in labels:
    print('Collecting images for {}'.format(label))
    for img_num in range(number_imgs):
        input('Collecting images for {}, image number {}'.format(label, img_num))
        ret, frame = cap.read()
        imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')
        cv2.imwrite(imgname, frame)
        cv2.imshow('Image Collection', frame)
        time.sleep(2)        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
