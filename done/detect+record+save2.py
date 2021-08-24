import cv2
import subprocess
import os

if os.path.isfile("qwer.mp4"):
  os.remove("qwer.mp4")
  
if os.path.isfile("qwer.avi"):
  os.remove("qwer.avi")

cap = cv2.VideoCapture(0)
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('qwer.avi', fourcc, 25.0, (640, 480))

while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
    bodies = fullbody_cascade.detectMultiScale(gray, 1.8, 2, 0, (30, 30))

    for (x,y,w,h) in bodies:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3, 4, 0)
        
    if (ret):
        cv2.imshow('Frame',img)
        out.write(img)

        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
subprocess.run('MP4Box -add qwer.avi qwer.mp4', shell=True) # avi 파일을 mp4 파일로 변환
