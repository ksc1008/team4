import sys
import PyQt6.QtGui
import threading
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6 import QtGui
import animator
import animation


class CustomWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mx = 400
        self.my = 400
        self.drawRect = QRect(600, 600, 0, 0)
        self.drawOpacity = 0

        self.texty = 450
        self.textOpacity = 0

        self.drawOpacity = 0

    #       오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)

        # 원 그리기

        # 1. 투명도를 설정하고
        painter.setOpacity(0.8)
        # 2. 색상을 정하고
        painter.setBrush(PyQt6.QtGui.QColorConstants.Red)
        # 3. 원형으로 칠한다.
        painter.drawEllipse(self.mx, self.my, 300, 300)

        painter.setOpacity(0.9)
        painter.setBrush(PyQt6.QtGui.QColorConstants.Black)
        painter.drawRect(QRect(0, 0, 250, 40))

        painter.setOpacity(self.drawOpacity)
        painter.setBrush(PyQt6.QtGui.QColorConstants.Black)
        painter.drawRect(self.drawRect)

        painter.setOpacity(1)
        painter.setPen(PyQt6.QtGui.QColorConstants.White)
        painter.setFont(QFont('Arial', 18, 700))
        painter.drawStaticText(QPointF(10, 10), QStaticText('Press ESC to quit.'))

        painter.setOpacity(self.textOpacity)
        painter.setPen(PyQt6.QtGui.QColorConstants.White)
        painter.setFont(QFont('Arial', 32, 700))
        painter.drawStaticText(QPointF(340, 475), QStaticText('Welcome to the Animation'))



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


def setter(q):
    window.drawRect = q
def setter2(x):
    window.drawOpacity = x
def setterText(x):
    window.textOpacity = x

_animator = animator.Animator(window)

afterAnimation = animation.make_var_anim(
    setterText, 0, 1, 500
)

anim = animation.make_rect_anim(setter, QRect(600, 550, 0, 100), QRect(300, 450, 600, 100), 1500)
anim.after = afterAnimation

_animator.startAnim(anim)
_animator.startAnim(animation.make_var_anim(
    setter2, 0, 1, 1000
))

window.showFullScreen()

# Run the application
sys.exit(app.exec())
