import numpy as np
import cv2
import os
from PIL import Image


#트레이닝 샘플 사진, 분석, 인식케스케이드
path = 'usercap'    #샘플사진 저장된 폴더
recognizer = cv2.face.LBPHFaceRecognizer_create()   #LBPH 분석

recognizer.read('train/face_train.yml') #트레이닝파일 읽기

#케스케이드 경로(정면)
faceCascade = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_frontalface_default.xml')
#케스케이드 경로(눈)
eyeCascade = cv2.CascadeClassifier('Cascades/haarcascades/haarcascade_eye.xml')
# 차영상
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=100)


#0 = 노트북 기본캠
cap = cv2.VideoCapture(0)

cap.set(3, 320) # set width
cap.set(4, 240)# set height


count = 0 #샘플촬영 카운트
face_id = 0 #샘플촬영 지정 id


id = 'none'  #얼굴인식시 분별id
backcheck = 0

name = []  #등록된 id


count_right = 0
count_left = 0

def cap_close():
    cap.release()
#     cv2.destroyAllWindows()

def creat_smaple_dir(slot):
    os.makedirs("usercap/NewUser_" + str(slot))


def recogsave(slot_id):
    global count

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 기본 frame에서 gray 변환
    # face 케스케이드 설정
    faces = faceCascade.detectMultiScale(
        gray,  # gray변환을 기준으로 인식
        scaleFactor=1.2,
        minNeighbors=5,  # 인접 인식범위와 간격
        minSize=(50, 50)  # 최소사이즈
    )

    for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # frame 창에 얼굴인식 틀띄우기
        roi_gray = gray[y:y + h, x:x + w]  # 인식된 영역
        roi_frame = frame[y:y + h, x:x + w]
        # eye케스케이드 설정
        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(5, 5)
        )
        # 인식된 face영역 내에서 eye틀띄우기
#         for (x2, y2, w2, h2) in eyes:
#             cv2.rectangle(roi_frame, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 255), 2)

        # 얼굴과 눈이 둘다 인식되면 폴더에 30장 저장
        count += 1;
        cv2.imwrite("usercap/NewUser_" + str(slot_id) + "/NewUser_" + str(slot_id) + '.' + str(count) + ".jpg",
                    gray[y:y + h, x:x + w])  # 샘플사진 저장
        print('sample' + str(count) + ' saved...')

    # cv2.putText(frame, str(count), (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)  # 찍은 샘플 카운트 텍스트표시
    # cv2.imshow('test', frame)  # test 타이틀바 창
    # cv2.imshow('gray', gray)  # gray 타이틀바 창

def newid_create():
    global count
    folder_count = len(os.listdir('usercap'))
    creat_smaple_dir(folder_count)
    while count<30:
        recogsave(folder_count)


def opencv_setup():
    global name
    name = os.listdir('usercap')
    name_buff = os.listdir('usercap')
    for k in name_buff:
        # print(int(k.split('_')[1]))
        name[int(k.split('_')[1])] = k.split('_')[0]


def traindata(path):
    # 샘플사진 폴더 내부의 사진
    samples = []
    for f in os.listdir(path):
        for v in os.listdir(os.path.join(path, f)):
            if v != 'Thumbs.db':
                samples.append(os.path.join(path, f, v))

    print(samples)

    faceSamples = []
    ids = []
    for sample in samples:
        PIL_img = Image.open(sample)
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(sample.split(".")[1])  # 파일명 user.1.1.jpg에서 .으로 분류하여 두번째 분류를 id로 저장
        faces = faceCascade.detectMultiScale(img_numpy)  # 얼굴인식
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
        # print(ids)
    return faceSamples, ids

def train():
    global path

    faces, ids = traindata(path)
    recognizer.train(faces, np.array(ids))

    recognizer.write('train/face_train.yml')
    print('new opencv training complete')

def recog():
    global id

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 기본 frame에서 gray 변환
    # face 케스케이드 설정
    faces = faceCascade.detectMultiScale(
        gray,  # gray변환을 기준으로 인식
        scaleFactor=1.2,
        minNeighbors=5,  # 인접 인식범위와 간격
        minSize=(50, 50)  # 최소사이즈
    )

    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # frame 창에 얼굴인식 틀띄우기
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        print(id)
        print(str(confidence))

        if (confidence < 150):
            id = name[id]
            confidence = "  {0}%".format(round(100 - confidence))
            cv2.imwrite("recogcap/" + str(id) + ".jpg", frame)  # 샘플사진 저장
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            cv2.imwrite("recogcap/" + str(id) + ".jpg", frame)  # 샘플사진 저장

        cv2.putText(frame, str(id), (x + 5, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)

    #cv2.imshow('test', frame)  # test 타이틀바 창

    #print(id)


def backrecog():
    global backcheck
    global count_right
    global count_left
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 기본 frame을 gray 변환

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(fgmask)

    for index, centroid in enumerate(centroids):
        if stats[index][0] == 0 and stats[index][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue

        x, y, width, height, area = stats[index]
        centerX, centerY = int(centroid[0]), int(centroid[1])

        if area > 300:
            cv2.circle(frame, (centerX, centerY), 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255))

            if (centerX >= 0 and centerX <= 120) and (centerY >= 50 and centerY <= 150):
                print(centerX, centerY)
                print('detected right')
                count_right += 1

            if (centerX >= 200 and centerX <= 320) and (centerY >= 50 and centerY <= 150):
                print(centerX, centerY)
                print('detected left')
                count_left += 1

        if count_right >=20:
            backcheck = 1
            count_right = 0
            count_left = 0

        if count_left >=20:
            backcheck = 2
            count_right = 0
            count_left = 0

#opencv_setup()
