import numpy as np
import cv2

#케스케이드 경로
faceCascade = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_frontalface_default.xml')

#0 = 노트북 기본캠
cap = cv2.VideoCapture(0)

cap.set(3, 720) # set width
cap.set(4, 1080)# set height

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #기본 frame에서 gray 변환
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    
    for (x,y,w,h) in faces:
        cv2.rectangle(gray, (x,y), (x+w, y+h), (255,0,0),2) #gray 창에 얼굴인식 틀띄우기
        roi_gray = gray[y:y+h, x:x+w]   #인식된 영역
    
    cv2.imshow('test', frame)   #test 타이틀바 창
    cv2.imshow('gray', gray)    #gray 타이틀바 창
    
    # 27== ESC키, 누를시 종료
    k = cv2.waitKey(1)
    if k == 27:
        break
        
cap.release()
cv2.destroyAllWindows()