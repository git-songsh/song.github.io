from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import subprocess
import os

if os.path.isfile("qwer.mp4"):
  os.remove("qwer.mp4")
  
if os.path.isfile("qwer.avi"):
  os.remove("qwer.avi")

def detect(img, cascade):
    rects = fullbody_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30))
                                            #  flags=cv2.CASCADE_SCALE_IMAGE
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
flag = 0
humanfound = 0 
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('ss.avi', fourcc, 25.0, (640, 480))

while (True):
    # 임의 숫자 / 사람 감지 횟수가 일정 횟수를 증가하면 다음 단계 진행 
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        rects = detect(gray, fullbody_cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))

        # show the frame
        cv2.imshow("Frame", vis)
        out.write(vis)
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        if cv2.waitKey(1) == ord('q'):
            flag = 1
            break

    if flag == 1:
        break
        
cap.release()
cv2.destroyAllWindows()

subprocess.run('MP4Box -add qwer.avi qwer.mp4', shell=True)
