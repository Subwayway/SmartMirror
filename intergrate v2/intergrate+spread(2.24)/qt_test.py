import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt5.QtWidgets import *

import opencv_integrate
import weather_crawling
import news_crawling
import spreadsheet

import time


class MyMain(QWidget):

    def __init__(self):
        super().__init__()

        # background color and size
        self.backcolor = QPalette()
        self.backcolor.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(self.backcolor)

        self.setWindowTitle('Sigong Mirror')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.th = Worker1(parent=self)

        self.th.recognize.connect(self.img_recognize)   # 얼굴인식 시그널
        self.th.Time_Update.connect(self.time_update)   # 시간 업데이트 시그널
        self.th.Weather_Update.connect(self.weather_update)  # 날씨 업데이트 시그널
        self.th.News_Update.connect(self.news_update)   # 뉴스 업데이트 시그널
        self.th.Select_Update.connect(self.select_update)

        self.th.start()  # 스레드시작

        print('id info save...')
        spreadsheet.save_dataall()  # 스프레드시트 id 정보 갱신 저장
        print('id info save success...')

        self.stackedWidget()
        self.showFullScreen()   # 전체화면

    # 화면전환을 위한 stack widget
    def stackedWidget(self):
        self.swUI = QStackedWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.swUI)


        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.TestStack1()   # 기본 UI
        self.TestStack2('a')    # opencv UI
        self.TestStack3()   # 선택지 결과 UI

        self.swUI.setCurrentIndex(0)    # 기본 ui 초기설정
        self.setLayout(vbox)

    # normal UI Stack
    def TestStack1(self):
        #현재시간 라벨
        self.TC = QDateTime.currentDateTime()
        self.TimeClock = QLabel(self.TC.toString("yyyy-MM-dd hh:mm:ss"))
        self.TimeClock.setFont(QFont('휴먼모음T', 30))
        self.TimeClock.setStyleSheet("color: white;")
        self.TimeClock.setAlignment(Qt.AlignCenter)

        #날씨 라벨
        weather_crawling.weather_read('성남시')

        self.weather = QLabel(weather_crawling.location + " " + weather_crawling.temp + "˚ " + weather_crawling.climate[0])
        self.weather.setFont(QFont('휴먼모음T', 20))
        self.weather.setStyleSheet("color: white;")

        img_weather = QPixmap('image_sample/'+ weather_crawling.climate[0] +'.png')
        self.weather_img = QLabel()
        self.weather_img.setPixmap(img_weather)

        #뉴스 라벨
        news_crawling.news_update()

        self.news1 = QLabel(news_crawling.news_value[0])
        self.news1.setFont(QFont('휴먼모음T', 15))
        self.news1.setStyleSheet("color: white;")
        self.news2 = QLabel(news_crawling.news_value[1])
        self.news2.setFont(QFont('휴먼모음T', 15))
        self.news2.setStyleSheet("color: white;")
        self.news3 = QLabel(news_crawling.news_value[2])
        self.news3.setFont(QFont('휴먼모음T', 15))
        self.news3.setStyleSheet("color: white;")
        self.news4 = QLabel(news_crawling.news_value[3])
        self.news4.setFont(QFont('휴먼모음T', 15))
        self.news4.setStyleSheet("color: white;")
        self.news5 = QLabel(news_crawling.news_value[4])
        self.news5.setFont(QFont('휴먼모음T', 15))
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

        stack1_layout = QVBoxLayout()
        stack1_layout.addStretch(1)
        stack1_layout.addWidget(self.TimeClock)
        stack1_layout.addStretch(1)
        stack1_layout.addLayout(weather_news)
        stack1_layout.addStretch(10)

        self.stack1.setLayout(stack1_layout)
        self.swUI.addWidget(self.stack1)

    # opencv UI Stack
    def TestStack2(self, recog_id):
        # 인식된 사람의 사진을 띄우기
        pixmap_recog = QPixmap('recogcap/' + str(recog_id) + '.jpg')
        print('recogcap/' + str(recog_id) + '.jpg')
        self.recog_img = QLabel()
        self.recog_img.setPixmap(pixmap_recog)

        # 인식된 사람의 id를 표시하기
        self.recog_label = QLabel(str(recog_id) + ' Recognized...')
        self.recog_label.setFont(QFont('휴먼모음T', 20))
        self.recog_label.setStyleSheet("color: white;")

        # 출퇴근/등록 선택 이미지
        select_img1 = QPixmap('image_sample/arrive.jpg')
        self.Select_img1 = QLabel()
        self.Select_img1.setPixmap(select_img1)

        select_img2 = QPixmap('image_sample/departure.jpg')
        self.Select_img2 = QLabel()
        self.Select_img2.setPixmap(select_img2)



        recog_result = QVBoxLayout()
        recog_result.addStretch(1)
        recog_result.addWidget(self.recog_img)
        recog_result.addWidget(self.recog_label)
        recog_result.addStretch(1)

        stack2_layout = QHBoxLayout()
        stack2_layout.addStretch(1)
        stack2_layout.addWidget(self.Select_img1)
        stack2_layout.addStretch(5)
        stack2_layout.addLayout(recog_result)
        stack2_layout.addStretch(5)
        stack2_layout.addWidget(self.Select_img2)
        stack2_layout.addStretch(1)

        self.stack2.setLayout(stack2_layout)
        self.swUI.addWidget(self.stack2)

    # 선택지 결과 화면
    def TestStack3(self):
        self.select_status = QLabel()
        self.select_status.setFont(QFont('휴먼모음T', 20))
        self.select_status.setStyleSheet("color: white;")

        self.id_info = QLabel()
        self.id_info.setFont(QFont('휴먼모음T', 20))
        self.id_info.setStyleSheet("color: white;")

        # 인식된 사람의 사진을 띄우기
        pixmap_recog2 = QPixmap('recogcap/' + 'none' + '.jpg')
        print('recogcap/' + 'none' + '.jpg')
        self.recog_img2 = QLabel()
        self.recog_img2.setPixmap(pixmap_recog2)

        stack3_layout = QVBoxLayout()
        stack3_layout.addStretch(1)
        stack3_layout.addWidget(self.select_status)
        stack3_layout.addStretch(1)
        stack3_layout.addWidget(self.recog_img2)
        stack3_layout.addStretch(1)
        stack3_layout.addWidget(self.id_info)
        stack3_layout.addStretch(1)

        self.stack3.setLayout(stack3_layout)
        self.swUI.addWidget(self.stack3)

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
        self.news1.setText(news_crawling.news_value[0])
        self.news2.setText(news_crawling.news_value[1])
        self.news3.setText(news_crawling.news_value[2])
        self.news4.setText(news_crawling.news_value[3])
        self.news5.setText(news_crawling.news_value[4])

    @pyqtSlot(str)
    def img_recognize(self, id):
        print(str(id) + 'recognized...')
        if (id != 'unknown') and (id != 'none'):
            self.recog_label.setText(str(id) + ' Recognized...')     # Teststack2를 먼저선언하면서 라벨과 이미지는 set함수를 통해 변경시킨다.
            self.recog_img.setPixmap(QPixmap('recogcap/' + str(id) + '.jpg'))
            self.Select_img1.setPixmap(QPixmap('image_sample/arrive.jpg'))  # 출근 이미지
            self.Select_img2.setPixmap(QPixmap('image_sample/departure.jpg'))   # 퇴근 이미지
            self.swUI.setCurrentIndex(1)    # qstackedwidget 의 인덱스를 opencv UI 로 변경한다.
        if id == 'unknown':
            self.recog_label.setText(str(id) + ' Recognized...')  # Teststack2를 먼저선언하면서 라벨과 이미지는 set함수를 통해 변경시킨다.
            self.recog_img.setPixmap(QPixmap('recogcap/' + str(id) + '.jpg'))
            self.Select_img1.setPixmap(QPixmap('image_sample/join.jpg'))    # 신규등록 이미지
            self.Select_img2.setPixmap(QPixmap('image_sample/cancel.jpg'))  # 취소 이미지
            self.swUI.setCurrentIndex(1)  # qstackedwidget 의 인덱스를 opencv UI 로 변경한다.
        if id == 'none':
            self.swUI.setCurrentIndex(0)    # qstackedwidget 의 인덱스를 기본 UI 로 변경한다.

    @pyqtSlot(str, str, str)
    def select_update(self, id, time_now, status):
        print('select updata on')
        if id != 'unknown':
            self.select_status.setText(id + ' ' + time_now + ' ' + status)
            self.recog_img2.setPixmap(QPixmap('recogcap/' + str(id) + '.jpg'))

            print('###sheet write...###')
            spreadsheet.ins_dataform(id, time_now, status)  # 스프레드 데이터 입력
            print('###user selected...###')

        if id == 'unknown':
            self.select_status.setText(id + ' ' + time_now + ' ' + status)
            print('###unknown selected...###')

        self.swUI.setCurrentIndex(2)


class Worker1(QThread):
    recognize = pyqtSignal(str)
    Time_Update = pyqtSignal(str)
    News_Update = pyqtSignal()
    Weather_Update = pyqtSignal()
    Select_Update = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__()

        self.check=0

    def run(self):
        while True:
            if opencv_integrate.id == 'none':
                opencv_integrate.recog()
            print(opencv_integrate.id)
            if (opencv_integrate.id != 'none') and (self.check == 0):
                self.recognize.emit(opencv_integrate.id)
                self.check = 1

                while opencv_integrate.backcheck ==0:
                    opencv_integrate.backrecog()
                    if opencv_integrate.backcheck == 1:
                        self.Select_Update.emit(opencv_integrate.id, self.Time_value.toString("yyyy-MM-dd hh:mm:ss"),
                                                "퇴근")
                        opencv_integrate.backcheck = 0
                        break

                    if opencv_integrate.backcheck == 2:
                        self.Select_Update.emit(opencv_integrate.id, self.Time_value.toString("yyyy-MM-dd hh:mm:ss"),
                                                "출근")
                        opencv_integrate.backcheck = 0
                        break

                time.sleep(25)
                opencv_integrate.id = 'none'

            if (opencv_integrate.id == 'none') and (self.check == 1):
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
