import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt5.QtWidgets import *

import opencv_integrate
import weather_crawling
import news_crawling
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
        self.th.Weather_Update.connect(self.weather_update)
        self.th.News_Update.connect(self.news_update)

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
        self.weather_img = QLabel()
        self.weather_img.setPixmap(img_weather)

        #뉴스 라벨
        news_crawling.news_update()

        self.news1 = QLabel(news_crawling.news_value[0])
        self.news1.setFont(QFont('휴먼매직체', 15))
        self.news1.setStyleSheet("color: white;")
        self.news2 = QLabel(news_crawling.news_value[1])
        self.news2.setFont(QFont('휴먼매직체', 15))
        self.news2.setStyleSheet("color: white;")
        self.news3 = QLabel(news_crawling.news_value[2])
        self.news3.setFont(QFont('휴먼매직체', 15))
        self.news3.setStyleSheet("color: white;")
        self.news4 = QLabel(news_crawling.news_value[3])
        self.news4.setFont(QFont('휴먼매직체', 15))
        self.news4.setStyleSheet("color: white;")
        self.news5 = QLabel(news_crawling.news_value[4])
        self.news5.setFont(QFont('휴먼매직체', 15))
        self.news5.setStyleSheet("color: white;")


        #레이아웃
        weather_layout = QVBoxLayout()
        weather_layout.addWidget(self.weather)
        weather_layout.addWidget(self.weather_img)

        news_layout = QVBoxLayout()
        news_layout.addWidget(self.news1)
        news_layout.addWidget(self.news2)
        news_layout.addWidget(self.news3)
        news_layout.addWidget(self.news4)
        news_layout.addWidget(self.news5)

        weather_news = QHBoxLayout()
        weather_news.addStretch(1)
        weather_news.addLayout(news_layout)
        weather_news.addStretch(10)
        weather_news.addLayout(weather_layout)
        weather_news.addStretch(1)

        textstack1 = QVBoxLayout()
        textstack1.addStretch(1)
        textstack1.addWidget(self.TimeClock)
        textstack1.addStretch(1)
        textstack1.addLayout(weather_news)
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

    @pyqtSlot()
    def weather_update(self):
        weather_crawling.weather_read('성남시')
        self.weather.setText(weather_crawling.location + " " + weather_crawling.temp + "˚ " + weather_crawling.climate[0])
        self.weather_img.setPixmap('image_sample/'+ weather_crawling.climate[0] +'.png')

    @pyqtSlot()
    def news_update(self):
        news_crawling.news_update()
        print(news_crawling.news_value[0])

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
    News_Update = pyqtSignal()
    Weather_Update = pyqtSignal()

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

            self.TimeUpdate()
            self.NewsUpdate()
            self.WeatherUpdate()


    def TimeUpdate(self):
        self.Time_value = QDateTime.currentDateTime()   #현재시간값

        self.Time_Update.emit(self.Time_value.toString("yyyy-MM-dd hh:mm:ss"))


    #현재시간 00초 마다 뉴스 갱신
    def NewsUpdate(self):
        self.news_updatetime = QTime.currentTime()

        self.news_trigger = 0

        if self.news_updatetime.second() == 0 and self.news_trigger == 0:
            self.News_Update.emit()
            self.news_trigger = 1

        if self.news_updatetime.second() != 0 and self.news_trigger == 1:
            self.news_trigger = 0

    #현재시간 10분마다 날씨 갱신
    def WeatherUpdate(self):
        self.weather_updatetime = QTime.currentTime()

        self.weather_trigger = 0

        if self.weather_updatetime.minute() == 10 and self.weather_trigger == 0:
            self.Weather_Update.emit()
            self.weather_trigger = 1

        if self.weather_updatetime.second() != 10 and self.weather_trigger == 1:
            self.weather_trigger = 0

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyMain()
   app.exec_()
