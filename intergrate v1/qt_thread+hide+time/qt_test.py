import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import *
import time

class MyApp(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        #[qpalette] 백그라운드 컬러 적용
        self.backcolor = QPalette()
        self.backcolor.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(self.backcolor)
        
        #이미지파일 적용
        pixmap1 = QPixmap('image_sample/c62.jpg')

        MyApp.cat_img = QLabel()
        MyApp.cat_img.setPixmap(pixmap1)
        
        #현재시간 라벨
        MyApp.TM=QDateTime.currentDateTime()
        MyApp.TIME=MyApp.TM.toString("yyyy-MM-dd hh:mm:ss")
        MyApp.time = QLabel(MyApp.TIME, self)
        MyApp.time.setAlignment(Qt.AlignCenter)
        MyApp.time.setStyleSheet("color: white;")

       
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(MyApp.time)
        vbox.addStretch(3)
        vbox.addWidget(MyApp.cat_img)
        vbox.addStretch(1)
        self.setLayout(vbox)
         
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)
        
        self.setWindowTitle('My First Application')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

class MyMain(MyApp):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.th = Worker(parent=self)
        self.th.sec_changed.connect(self.time_update)
        self.th.start()
        self.show()
        
    @pyqtSlot(int)
    def time_update(self, msg):
        print(msg)
        MyApp.TM = QDateTime.currentDateTime()
        MyApp.TIME = MyApp.TM.toString("yyyy-MM-dd hh:mm:ss")
        MyApp.time.setText(MyApp.TIME)
        if msg == 10 and MyApp.cat_img.isVisible() == True:
            MyApp.cat_img.setVisible(False)
        elif msg == 10 and MyApp.cat_img.isVisible() == False:
            MyApp.cat_img.setVisible(True)

class Worker(QThread):
    sec_changed = pyqtSignal(int)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.working = True
        self.sec = sec

    def run(self):
        while True:
            self.sec_changed.emit(self.sec)
            self.sec += 1
            self.sleep(1)
            MyApp.time.repaint()

            if self.sec==11:
                self.sec=0

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyMain()
   app.exec_()
