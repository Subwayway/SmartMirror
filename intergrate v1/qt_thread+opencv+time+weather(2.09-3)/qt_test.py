import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt5.QtWidgets import *

import opencv_integrate
import weather_crawling
import time


class MyMain(QWidget):

    def __init__(self):
        super().__init__()

        #background color and size
        self.backcolor = QPalette()
        self.backcolor.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(self.backcolor)

        self.setWindowTitle('Sigong Mirror')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.move(0, 0)
        self.resize(1920, 1080)


        self.th = Worker1(parent=self)
        self.th.recognize.connect(self.img_recognize)
        self.th.Time_Update.connect(self.time_update)
        self.th.start()


        self.stackedWidget()
        self.show()

    # 화면전환을 위한 stack widget
    def stackedWidget(self):
        self.swUI = QStackedWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.swUI)


        self.stack1 = QWidget()
        self.stack2 = QWidget()


        self.TestStack1()   #기본 UI
        self.TestStack2('a')    #opencv UI

        self.swUI.setCurrentIndex(0)    #기본 ui 초기설정
        self.setLayout(vbox)

    def TestStack1(self):
        #현재시간 라벨
        self.TC = QDateTime.currentDateTime()
        self.TimeClock = QLabel(self.TC.toString("yyyy-MM-dd hh:mm:ss"))
        self.TimeClock.setFont(QFont('휴먼매직체', 30))
        self.TimeClock.setStyleSheet("color: white;")
        self.TimeClock.setAlignment(Qt.AlignCenter)

        #날씨 라벨
        weather_crawling.weather_read('성남시')

        self.weather = QLabel(weather_crawling.location + " " + weather_crawling.temp + "˚ " + weather_crawling.climate[0])
        self.weather.setFont(QFont('휴먼매직체', 20))
        self.weather.setStyleSheet("color: white;")

        img_weather = QPixmap('image_sample/'+ weather_crawling.climate[0] +'.png')
        weather_img = QLabel()
        weather_img.setPixmap(img_weather)

        box1 = QHBoxLayout()
        box1.addStretch(10)
        box1.addWidget(weather_img)
        box1.addStretch(1)

        box2 = QHBoxLayout()
        box2.addStretch(8)
        box2.addWidget(self.weather)
        box2.addStretch(1)

        textstack1 = QVBoxLayout()
        textstack1.addStretch(1)
        textstack1.addWidget(self.TimeClock)
        textstack1.addLayout(box2)  # weather text layout
        textstack1.addLayout(box1) # weather img layout
        textstack1.addStretch(10)

        self.stack1.setLayout(textstack1)
        self.swUI.addWidget(self.stack1)


    def TestStack2(self, recog_id):
        #인식된 사람의 사진을 띄우기
        pixmap_recog = QPixmap('recogcap/' + str(recog_id) + '.jpg')
        print('recogcap/' + str(recog_id) + '.jpg')
        self.recog_img = QLabel()
        self.recog_img.setPixmap(pixmap_recog)

        #인식된 사람의 id를 표시하기
        self.recog_label = QLabel(str(recog_id) + 'recognized...')
        self.recog_label.setFont(QFont('휴먼매직체', 20))
        self.recog_label.setStyleSheet("color: white;")

        teststack2 = QVBoxLayout()
        teststack2.addStretch(1)
        teststack2.addWidget(self.recog_label)
        teststack2.addWidget(self.recog_img)
        teststack2.addStretch(1)


        self.stack2.setLayout(teststack2)
        self.swUI.addWidget(self.stack2)



    @pyqtSlot(str)
    def time_update(self, value):
        self.TimeClock.setText(value)

    @pyqtSlot(str)
    def img_recognize(self, id):
        print(str(id) + 'recognized...')
        if id != 'unknown':
            self.recog_label.setText(str(id) + 'recognized...')     #Teststack2를 먼저선언하면서 라벨과 이미지는 set함수를 통해 변경시킨다.
            self.recog_img.setPixmap(QPixmap('recogcap/' + str(id) + '.jpg'))
            self.swUI.setCurrentIndex(1)    #qstackedwidget 의 인덱스를 opencv UI 로 변경한다.
        if id == 'unknown':
            #self.swUI.removeWidget(self.stack2)
            self.swUI.setCurrentIndex(0)    #qstackedwidget 의 인덱스를 기본 UI 로 변경한다.




class Worker1(QThread):
    recognize = pyqtSignal(str)
    Time_Update = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()

        self.check=0

    def run(self):
        while True:
            opencv_integrate.recog()
            if (opencv_integrate.id != 'unknown') and (self.check == 0):
                self.recognize.emit(opencv_integrate.id)
                self.check = 1
                time.sleep(5)
                opencv_integrate.id = 'unknown'

            if (opencv_integrate.id == 'unknown') and (self.check == 1):
                self.recognize.emit(opencv_integrate.id)
                self.check = 0

            self.Time_Update.emit(self.TimeUpdate())


    def TimeUpdate(self):
        self.Time_value = QDateTime.currentDateTime()
        return self.Time_value.toString("yyyy-MM-dd hh:mm:ss")


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyMain()
   app.exec_()
