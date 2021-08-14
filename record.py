import cv2
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('save.h264', fourcc, 25, (640, 480))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame
    if(ret) :
        cv2.imshow('frame_color', frame)    # 컬러 화면 출력       
        out.write(frame)

        if cv2.waitKey(1) == ord('q'): # q 누르면 종료
            breakcap.release()
cv2.destroyAllWindows()
