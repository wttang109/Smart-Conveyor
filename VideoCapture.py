# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 11:42:28 2019

@author: Sunny
http://answers.opencv.org/question/34273/python-and-videocapture-from-webcam/
"""
import numpy as np
import cv2

isValid = True

captureLeft = cv2.VideoCapture(0)

if not captureLeft.isOpened()  :
    print("can't open the camera")

while(True):
    # Capture frame-by-frame
    try:
        retLeft, frameLeft = captureLeft.read()

    except:
        print("error the take a image")
        isValid = False

    if isValid == True:
        try:
            # Our operations on the frame come here
#            grayLeft = cv2.cvtColor(frameLeft, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('frameLeft',frameLeft)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            print("Error during the convertion")

# When everything done, release the capture
captureLeft.release()
cv2.destroyAllWindows()



