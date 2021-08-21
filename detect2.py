'''
import cv2

#괄호안에 파일명을 쓰면 파일이 로드됌
cap = cv2.VideoCapture('test_human1.mp4') #비디오 파일 불러오기
font = cv2.FONT_HERSHEY_SIMPLEX #사람 감지 글씨체 정의

#create the window & change the window size
#윈도우 생성 및 사이즈 변경
cv2.namedWindow('Face')

#fullbody detect
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_fullbody.xml')



while(True):
    #read the camera image
    #카메라에서 이미지 얻기
    ret, frame = cap.read()
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayframe, 1.8, 2, 0, (30, 30))

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3, 4, 0)
        cv2.putText(frame, 'Detected human', (x-5, y-5), font, 0.9, (255,255,0),2)

    cv2.imshow('Face',frame)

    #wait keyboard input until 10ms
    #300ms 동안 키입력 대기
    #키를 누르면 꺼진다. 사진의 형태에서 얼굴 감지
    """if cv2.waitKey(300) >= 0:
		break"""
	#영상의 형태에서 얼굴 감지, space 입력시 중지

    if cv2.waitKey(1) != 255:
        break;
"""	
    if len(faces) == 1:
	facefound += 1
"""#이부분수정	
	
#close the window
#윈도우 종료
cap.release()
cv2.destroyWindow('Face')

'''

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

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

humanfound = 0
# allow the camera to warmup
time.sleep(0.1)

while (True):
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # grab the raw NumPy array representing the image, then initialize the timestamp

        # and occupied/unoccupied text
        img = frame.array
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        rects = detect(gray, fullbody_cascade)
        vis = img.copy()
        draw_rects(vis, rects, (0, 255, 0))

        # show the frame
        cv2.imshow("Frame", vis)
        key = cv2.waitKey(1) & 0xFF

        if len(rects)>0:
            humanfound += 1

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        print(str(humanfound))
