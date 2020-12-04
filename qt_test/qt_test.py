import sys
import time
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #[qpalette] 백그라운드 컬러 적용
        self.backcolor = QPalette()
        self.backcolor.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(self.backcolor)
        
        #이미지파일 적용
        pixmap1 = QPixmap('image_sample/c62.jpg')

        cat_img = QLabel()
        cat_img.setPixmap(pixmap1)

        #현재시간 라벨
        timedis = QLabel(time.strftime('%c', time.localtime(time.time())), self)
        timedis.setAlignment(Qt.AlignCenter)
        timedis.setStyleSheet("color: white;")

        font1 = timedis.font()
        font1.setPointSize(35)
        
        timedis.setFont(font1)
       
       
        #박스레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cat_img)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addWidget(timedis)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        
        
        
        self.setWindowTitle('My First Application')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.move(0, 0)
        self.resize(1920, 1080)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())