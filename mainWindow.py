from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

import overlay_objects.loadingCircle
from keyboardEvent import ShorCut
from overlay_animations import animator
from overlay_objects.overlayObject import OverlayObject
from textLabel import TextLabel

from pixmapLabel import PixmapLabel
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

        self.showFullScreen()

        # OverlayObject 객체 리스트
        self.objects = []

        self.shortcut = ShorCut()
        self.shortcut.start()
        self.shortcut.quit_key.connect(self.shortcut_quit_key)
        self.shortcut.circle_key.connect(self.shortcut_circle_key)
        self.shortcut.demo_key.connect(self.shortcut_demo_key)
        self.shortcut.label_key.connect(self.shortcut_label_key)
        self.shortcut.mic_key.connect(self.shortcut_mic_key)
        self.shortcut.release_mic_key.connect(self.shortcut_release_mic_key)
        self.animator.start()
        self.test = _t

        self.lc = None
        self.re = False

        self.label = TextLabel(self)
        self.mic_image = PixmapLabel(self, 'images/mic_white.png')
        self.label.setTextContents("ChatGPT로 부터의 1 개의 답변.")

    # 오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)

        for o in self.objects:
            o.draw(painter)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.test.exit(0)

    def addObject(self, obj: OverlayObject):  # 메인 윈도우의 objects에 새 오브젝트를 추가.
        self.objects.append(obj)
        obj.window = self

    def finAllObj(self):
        for o in self.objects:
            o.destroy()

    @pyqtSlot()
    def shortcut_demo_key(self):  # Ctrl + D 입력 시 demo 실행
        # demo.py 참고
        self.addObject(demo.createTestObjectAndApplyAnimation(self.animator))

    @pyqtSlot()
    def shortcut_quit_key(self):  # Ctrl + Q 입력시 프로그램 종료
        self.finAllObj()
        self.label.close()
        self.shortcut.stop()
        self.shortcut.terminate()
        self.close()

    @pyqtSlot()
    def shortcut_circle_key(self):  # Ctrl + E 입력 시 Loading Circle 추가 혹은 제거
        if self.lc is None:
            self.lc = overlay_objects.loadingCircle.LoadingCircle()
            self.addObject(self.lc)
            self.animator.addAnim(self.lc.getCycleAnimation())


        else:
            self.lc.destroy()
            self.lc = None

    @pyqtSlot()
    def shortcut_label_key(self):  # Ctrl + F1 입력시 label 보이기 / 숨기기
        if not self.re:
            self.label.pop_in(self.animator)
            self.re = True
        else:
            self.label.pop_out()
            self.re = False

    @pyqtSlot()
    def shortcut_mic_key(self):  # Ctrl + M 눌리면
        print("pressing")
        self.mic_image.show()

    @pyqtSlot()
    def shortcut_release_mic_key(self):  # Ctrl + M 때면
        print("released")
        self.mic_image.hide()

    @pyqtSlot()
    def popUp(self):
        pass