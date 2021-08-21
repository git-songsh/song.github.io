"""
import picamera
import time
import datetime

def record():
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    now = datetime.datetime.now()
    filename = now.strftime('%Y-%m-%d %H:%M:%S')
    camera.start_recording(output = filename + '.h264') #h.264 코덱
    camera.wait_recording(5)
    camera.stop_recording()
        
while True:
  record()
"""  
  
 


                        
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


humanfound = 0
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('save.h264', fourcc, 25, (640, 480))

def detect(img, cascade): # fullbody 인식하는 함수
    rects = fullbody_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30))
                                            #  flags=cv2.CASCADE_SCALE_IMAGE
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color): # 인식한 부분 사각형 표시하는 함수
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
while (humanfound < 100):
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
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        if len(rects)>0: # 사람이 한명이상 인식되면 
            humanfound += 1 # 사람 감지 횟수를 1씩 증가시킴 - 카메라 openCV 통해 2차 확인 
        else:
            humanfound = 0
            a = 0 
            flag = 1
            break
            
        if humanfound > 1:
          out.write(frame)
          
        if cv2.waitKey(1) == ord('q'): # q 누르면 종료
            break

#out.release()
#cv2.destroyAllWindows()
