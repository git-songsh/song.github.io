#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import cv2

font = cv2.FONT_ITALIC
face_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
cap = cv2.VideoCapture(-1)

while True:
    ret, frame = cap.read()             
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    cap.release()
    cv2.destroyAllWindows()
            

