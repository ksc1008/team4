from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

from keyboardEvent import ShorCut
from overlay_animations import animator
from overlay_objects.overlayObject import OverlayObject

import demo


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

        # OverlayObject 객체 리스트
        self.objects = []

        self.shortcut = ShorCut()
        self.shortcut.start()
        self.shortcut.exit_key.connect(self.shortcut_exit_key)
        self.animator.start()
        self.test = _t

    #       오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)

        for o in self.objects:
            o.draw(painter)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.test.exit(0)

    def addObject(self, obj: OverlayObject):    # 메인 윈도우의 objects에 새 오브젝트를 추가.
        self.objects.append(obj)
        obj.window = self

    @pyqtSlot()
    def shortcut_exit_key(self):
        # demo.py 참고
        self.addObject(demo.createTestObjectAndApplyAnimation(self.animator))


# Create the main window
