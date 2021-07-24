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

#close the window
#윈도우 종료
cap.release()
cv2.destroyWindow('Face')
