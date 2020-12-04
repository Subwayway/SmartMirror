import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt5.QtWidgets import *

import opencv_integrate
import time


class MyMain(QWidget):

    def __init__(self):
        super().__init__()

        #background color and size
        self.backcolor = QPalette()
        self.backcolor.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(self.backcolor)

        self.setWindowTitle('My First Application')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.move(0, 0)
        self.resize(1200, 600)

        #opencv 스레드
        self.th = Worker(parent=self)
        self.th.recognize.connect(self.img_recognize)
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
        TC = QDateTime.currentDateTime()
        TimeClock = QLabel(TC.toString("yyyy-MM-dd hh:mm:ss"))
        TimeClock.setStyleSheet("color: white;")

        img_sample1 = QPixmap('image_sample/c62.jpg')
        cat_img = QLabel()
        cat_img.setPixmap(img_sample1)

        textstack1 = QVBoxLayout()
        textstack1.addWidget(TimeClock)
        textstack1.addWidget(cat_img)

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



    @pyqtSlot(int)
    def time_update(self, msg):
        print(msg)
        self.TM = QDateTime.currentDateTime()
        self.TIME = NormalUI.TM.toString("yyyy-MM-dd hh:mm:ss")
        self.time.setText(NormalUI.TIME)
        if msg == 10 and self.cat_img.isVisible() == True:
            self.cat_img.setVisible(False)
        elif msg == 10 and self.cat_img.isVisible() == False:
            self.cat_img.setVisible(True)

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




class Worker(QThread):
    recognize = pyqtSignal(str)

    def __init__(self, sec=0, parent=None):
        super().__init__()

        self.check=0

    def run(self):
        while True:
            opencv_integrate.recog()
            if (opencv_integrate.id != 'unknown') and (self.check == 0):
                self.recognize.emit(opencv_integrate.id)
                self.check = 1

            if (opencv_integrate.id == 'unknown') and (self.check == 1):
                self.recognize.emit(opencv_integrate.id)
                self.check = 0

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyMain()
   app.exec_()
