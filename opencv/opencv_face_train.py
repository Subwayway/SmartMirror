import numpy as np
import cv2
import os
from PIL import Image

#트레이닝 샘플 사진, 분석, 인식케스케이드
path = 'usercap'    #샘플사진 저장된 폴더
recognizer = cv2.face.LBPHFaceRecognizer_create()   #LBPH 분석
detector = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_frontalface_default.xml')

def traindata(path):
    #샘플사진 폴더 내부의 사진
    samples = []
    for f in os.listdir(path):
        for v in os.listdir(os.path.join(path,f)):
            if v != 'Thumbs.db':
                samples.append(os.path.join(path, f, v))
    
    print(samples)
    
    faceSamples = []
    ids = []
    for sample in samples:
        PIL_img = Image.open(sample)
        img_numpy = np.array(PIL_img,'uint8')
        id = int(sample.split(".")[1])  #파일명 user.1.1.jpg에서 .으로 분류하여 두번째 분류를 id로 저장
        faces = detector.detectMultiScale(img_numpy)    #얼굴인식
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
        #print(ids)
    return faceSamples, ids

print("\n start face training...")
faces, ids = traindata(path)
recognizer.train(faces, np.array(ids))

recognizer.write('train/face_train.yml')

print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))