import cv2
import subprocess
import os

if os.path.isfile("qwer.mp4"):
  os.remove("qwer.mp4")
  
if os.path.isfile("qwer.avi"):
  os.remove("qwer.avi")

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('qwer.avi', fourcc, 25.0, (640, 480))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame
    if(ret) :
        cv2.imshow('frame', frame)    # 화면 출력 
        out.write(frame)

        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

#command = "MP4Box -add qwer.avi qwer.mp4"
#Call = (["MP4Box -add qwer.avi qwer.mp4"])

#subprocess.call(["ls", "-al"])
#subprocess.call("ls -al", shell=True)

subprocess.run('MP4Box -add qwer.avi qwer.mp4', shell=True)
