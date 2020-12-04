import numpy as np
import cv2

#0 = 노트북 기본캠
cap = cv2.VideoCapture(0)

cap.set(3, 720) # set width
cap.set(4, 1080)# set height

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #기본 frame을 gray 변환
    
    cv2.imshow('test', frame)   #test 타이틀바 창
    cv2.imshow('gray', gray)    #gray 타이틀바 창
    
    # 27== ESC키, 누를시 종료
    k = cv2.waitKey(1)
    if k == 27:
        break
        
cap.release()
cv2.destroyAllWindows()