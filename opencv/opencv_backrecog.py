import numpy as np
import cv2

# 0 = 노트북 기본캠
cap = cv2.VideoCapture(0)

cap.set(3, 720)  # set width
cap.set(4, 1080)  # set height

fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=100)

while True:
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

        if area > 100:
            cv2.circle(frame, (centerX, centerY), 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255))

            if (centerX >= 50 and centerX <=150) and (centerY >= 50 and centerY <= 150):
                print(centerX, centerY)
                print('detected left')

            if (centerX >= 450 and centerX <=550) and (centerY >= 50 and centerY <= 150):
                print(centerX, centerY)
                print('detected right')



    cv2.rectangle(frame, (50, 50), (150, 150), (0, 255, 0), 2)
    cv2.rectangle(frame, (450, 50), (550, 150), (0, 255, 0), 2)

    cv2.imshow('test', frame)  # test 타이틀바 창
    cv2.imshow('gray', gray)  # gray 타이틀바 창
    cv2.imshow('background', fgmask)

    # 27== ESC키, 누를시 종료
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()