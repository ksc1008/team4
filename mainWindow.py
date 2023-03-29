from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore

from keyboardEvent import ShorCut
from overlay_animations import animator


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mx = 400
        self.my = 400
        self.drawRect = QRect(600, 600, 0, 0)
        self.drawOpacity = 0

        self.texty = 450
        self.textOpacity = 0

        self.drawOpacity = 0

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.animator = animator.Animator(self)

        self.shortcut = ShorCut()
        self.shortcut.start()
        self.shortcut.exit_key.connect(self.shortcut_exit_key)

    #       오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)

        self.animator.update(painter)

    @pyqtSlot()
    def shortcut_exit_key(self):
        # Test Animation 시작. animator.py 참고
        self.animator.startTestAnimation()


# Create the main window
