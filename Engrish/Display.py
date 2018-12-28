import sys

from Data import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)
        QWidget.setLayout(self, self.vbox)

        self.font = QFont('Arial', 12, 2)
        self.style = 'color: yellow'

        self.pen = QPen(QColor(255,0,0,128))
        self.pen.setWidth(5)

        #self.poly = QPolygonF()
        #self.poly.append(QPointF(1000,1000))
        #self.poly.append(QPointF(100,150))
        #self.poly.append(QPointF(150,100))

        self.startTimer()

    def addLabel(self, text):
        label = QLabel()
        label.setText(text)
        label.setStyleSheet(self.style)
        label.setFont(self.font)
        self.vbox.addWidget(label)
        return label

    def startTimer(self):
        timer = QTimer(self)
        timer.setSingleShot(False)
        timer.timeout.connect(self.updateAll)
        timer.start(20)

    def updateAll(self):
        dt.update()
        if dt.state_poly:
            self.move(dt.minx, dt.miny)
            self.resize(dt.w, dt.h)
        self.update()

    def paintEvent(self, e):
        if dt.state_poly:
            qp = QPainter()
            qp.begin(self)
            qp.setPen(self.pen)
            #qp.setBrush(QColor(0,0,0,0))
            qp.drawRect(0,0,dt.w,dt.h)
            #qp.setBrush(QColor(255,255,255,128))
            #qp.setPen(QColor(0,0,0,0))
            #qp.drawPolygon(self.poly)
            qp.end()

class WidgetText(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(500,500)
        self.move(30, 30)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)
        QWidget.setLayout(self, self.vbox)

        self.font = QFont('Arial', 12, 2)
        self.style = 'color: yellow'

        self.prText = self.addLabel('???')
        self.sep = self.addLabel('============')
        self.frText = self.addLabel('???')
        self.sep2 = self.addLabel('============')
        self.trText = self.addLabel('???')

        self.startTimer()

    def addLabel(self, text):
        label = QLabel()
        label.setText(text)
        label.setStyleSheet(self.style)
        label.setFont(self.font)
        label.setWordWrap(True) 
        self.vbox.addWidget(label)
        return label

    def updateLabel(self):
        self.prText.setText(dt.prText)
        self.frText.setText(dt.frText)
        self.trText.setText(dt.trText)

    def startTimer(self):
        timer = QTimer(self)
        timer.setSingleShot(False)
        timer.timeout.connect(self.updateAll)
        timer.start(20)

    def updateAll(self):
        self.updateLabel()
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(0,0,0,128))
        qp.drawRect(0,0,500,500)
        qp.end()

def initDisplay():
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    w2 = WidgetText()
    w2.show()
    app.exec_()
