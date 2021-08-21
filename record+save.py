import cv2
import subprocess

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('qwer.avi', fourcc, 25.0, (640, 480))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame
    if(ret) :
        #gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환
        cv2.imshow('frame', frame)    # 컬러 화면 출력        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
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
