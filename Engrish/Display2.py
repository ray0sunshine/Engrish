from googletrans import Translator
from desktopmagic.screengrab_win32 import getRectAsImage
from collections import deque
from pynput.mouse import Controller

import keyboard as key
import pytesseract as ts
import time
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

q = deque(maxlen=4)
trans = Translator()
mouse = Controller()

def getScreenText(area):
    ret = ts.image_to_string(getRectAsImage(area), lang = 'chi_sim')
    return ret.strip()

def getMousePos():
    q.extend(mouse.position)
    print(mouse.position)
    if len(q) >= 4:
        box = tuple(q)
        q.clear()
        print(box)
        translation = trans.translate(getScreenText(box))
        print(translation.text)

class Widget(QWidget):
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

        self.poly = QPolygonF()
        self.poly.append(QPointF(1000,1000))
        self.poly.append(QPointF(100,150))
        self.poly.append(QPointF(150,100))

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
        timer.timeout.connect(self.update)
        timer.start(20)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(0,0,0,128))
        qp.drawRect(0,0,250,500)
        qp.setBrush(QColor(255,255,255,128))
        qp.setPen(QColor(0,0,0,0))
        qp.drawPolygon(self.poly)
        qp.end()

key.add_hotkey('q', getMousePos, suppress=True)
#key.add_hotkey('ctrl+f12', getMousePos)
#key.wait('esc')

# hotkeys
# get mouse positioning
# UI display
# Randomize over multiple varied get sections (pick most common result)
# Polygon grab
# Grab screen section / move a lense
# Filter image / raise contrast etc for better OCR
# Re-arrange the text by lines and separators to better translate
# Translate
# Overlay on top

# trans = Translator()
# translation = trans.translate('これもまたたわごとではない')
# print(translation.text)

app = QApplication(sys.argv)
w = Widget()
w.show()
app.exec_()
