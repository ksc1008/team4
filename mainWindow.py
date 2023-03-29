from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

from keyboardEvent import ShorCut
from overlay_animations import animator


class MainWindow(QMainWindow):

    def __init__(self, _t):
        super().__init__()

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
        self.animator.start()
        self.test = _t

    #       오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)

        self.animator.update(painter)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.test.exit(0)

    @pyqtSlot()
    def shortcut_exit_key(self):
        self.animator.startTestAnimation()


# Create the main window
