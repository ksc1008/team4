import sys
import PyQt6.QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6 import QtGui

class CustomWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mx = 400
        self.my = 400

#       오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)

        #뒷 배경 그리기

        # 1. 투명도를 설정하고
        painter.setOpacity(0.2)
        # 2. 색상을 정하고
        painter.setBrush(PyQt6.QtGui.QColorConstants.White)
        # 3. 사각형으로 칠한다.
        painter.drawRect(self.rect())

        #원 그리기

        # 1. 투명도를 설정하고
        painter.setOpacity(0.8)
        # 2. 색상을 정하고
        painter.setBrush(PyQt6.QtGui.QColorConstants.Red)
        # 3. 원형으로 칠한다.
        painter.drawEllipse(self.mx,self.my,300,300)


app = QApplication(sys.argv)

# Create the main window
window = CustomWindow()
window.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

# Run the application
window.showFullScreen()
sys.exit(app.exec())
