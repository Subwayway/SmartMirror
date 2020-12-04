import numpy as np
import cv2
import os

#케스케이드 경로(정면)
faceCascade = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_frontalface_default.xml')
#케스케이드 경로(정면)
eyeCascade = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_eye.xml')


#0 = 노트북 기본캠
cap = cv2.VideoCapture(0)

cap.set(3, 720) # set width
cap.set(4, 1080)# set height

#파일 넘버 입력
#face_id = input('\n enter user id : ')
#print("\n face capture start!!")

#샘플사진 디렉토리 자동 생성
for i in range(0,10):
    if not os.path.exists('usercap/sample'+str(i)):
        os.makedirs('usercap/sample'+str(i))
        face_id = i
        break

count = 0
while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #기본 frame에서 gray 변환
    #face 케스케이드 설정
    faces = faceCascade.detectMultiScale(
        gray,   #gray변환을 기준으로 인식
        scaleFactor=1.2,
        minNeighbors=5,     #인접 인식범위와 간격
        minSize=(20, 20)    #최소사이즈
    )
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),2) #frame 창에 얼굴인식 틀띄우기
        roi_gray = gray[y:y+h, x:x+w]   #인식된 영역
        roi_frame = frame[y:y+h, x:x+w]
        #eye케스케이드 설정
        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor = 1.2,
            minNeighbors=5,
            minSize=(5, 5)
        )
        #인식된 face영역 내에서 eye틀띄우기
        for (x2, y2, w2, h2) in eyes:
            cv2.rectangle(roi_frame,  (x2,y2), (x2+w2, y2+h2), (255,255,255),2)
            
            #얼굴과 눈이 둘다 인식되면 폴더에 20장 저장
            count+=1;
            cv2.imwrite("usercap/sample"+str(face_id)+"/sample." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])#샘플사진 저장
            
    cv2.putText(frame, str(count), (20,20), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255),1)#찍은 샘플 카운트 텍스트표시
    cv2.imshow('test', frame)   #test 타이틀바 창
    cv2.imshow('gray', gray)    #gray 타이틀바 창
    
    # 27== ESC키, 누를시 종료
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif count >= 30:   #20번 촬영시 종료
        break
cap.release()
cv2.destroyAllWindows()