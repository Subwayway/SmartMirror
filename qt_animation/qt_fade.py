import sys
import time
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # [qpalette] 백그라운드 컬러 적용
        self.backcolor = QPalette()
        self.backcolor.setColor(QPalette.Background, QColor(0, 0, 0))
        self.setPalette(self.backcolor)

        # 이미지파일 적용
        pixmap1 = QPixmap('image_sample/c62.jpg')

        self.cat_img = QLabel()
        self.cat_img.setPixmap(pixmap1)


        # 현재시간 라벨
        timedis = QLabel(time.strftime('%c', time.localtime(time.time())), self)
        timedis.setAlignment(Qt.AlignCenter)
        timedis.setStyleSheet("color: rgba(255,255,255,50%);")

        font1 = timedis.font()
        font1.setPointSize(10)

        timedis.setFont(font1)

        # test label
        self.testtext = QLabel("hello")
        self.testtext.setAlignment(Qt.AlignCenter)
        self.testtext.setStyleSheet("color: rgba(255,255,255,100%);")

        # 박스레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.cat_img)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(timedis)
        vbox.addLayout(hbox)
        vbox.addWidget(self.testtext)

        self.setLayout(vbox)

        self.setWindowTitle('My First Application')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.move(0, 0)
        self.resize(1500, 600)
        self.show()

        self.fade(self.cat_img)
        self.fade(self.testtext)


    def anima(self):
        self.anim = QPropertyAnimation(self.testtext, b"label")
        self.anim.setDuration(10000)
        self.anim.setStartValue(self.testtext.setStyleSheet("color: rgba(255,255,255,0%);"))
        self.anim.setEndValue(self.testtext.setStyleSheet("color: rgba(255,255,255,75%);"))
        self.anim.start()

    def fade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())