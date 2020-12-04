import numpy as np
import cv2
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('train/face_train.yml')
detector = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_PLAIN
    
id = 0

name = ['sana', 'chj', 'Bill', 'jang']

cap = cv2.VideoCapture(0)

cap.set(3, 720) # set width
cap.set(4, 1080)# set height

minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4)

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #기본 frame에서 gray 변환
    #face 케스케이드 설정
    faces = detector.detectMultiScale(
        gray,   #gray변환을 기준으로 인식
        scaleFactor=1.2,
        minNeighbors=5,     #인접 인식범위와 간격
        minSize=(int(minW), int(minH))    #최소사이즈
    )
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2) #frame 창에 얼굴인식 틀띄우기
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
        if(confidence < 70):
            id = name[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(frame, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(frame, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
        
    cv2.imshow('test', frame)   #test 타이틀바 창
    
    # 27== ESC키, 누를시 종료
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()