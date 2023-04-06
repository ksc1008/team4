from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

import overlay_objects.loadingCircle
from keyboardEvent import ShorCut
from overlay_animations import animator
from overlay_objects.overlayObject import OverlayObject
from textLabel import TextLabel

import overlay_objects.overlayCircle
import overlay_objects.overlayPixmap
import overlay_objects.overlayCheck
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
        self.shortcut.check_key.connect(self.shortcut_check_key)
        self.shortcut.demo_key.connect(self.shortcut_demo_key)
        self.shortcut.label_key.connect(self.shortcut_label_key)
        self.shortcut.mic_key.connect(self.shortcut_mic_key)
        self.shortcut.release_mic_key.connect(self.shortcut_release_mic_key)
        self.animator.start()
        self.test = _t

        self.re = False

        self.lc = None
        self.oc = None
        self.mp = None
        self.sw = None
        self.check = None

        self.label = TextLabel(self)
        # self.mic_image = PixmapLabel(self, 'images/mic_white.png')
        self.label.setTextContents("ChatGPT로 부터의 1 개의 답변.")

    # 오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

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
    def shortcut_check_key(self):  # Ctrl + E 입력 시 Loading Circle 추가 혹은 제거
        if self.check is None:
            self.check = overlay_objects.overlayCheck.OverlayCheck()

            self.addObject(self.check)
            self.animator.addAnim(self.check.getAnimation())
        else:
            self.check.destroy()
            self.check = None

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
        mic_width = 200
        mic_height = 200
        if self.mp is None:
            self.oc = overlay_objects.overlayCircle.OverlayCircle()
            self.mp = overlay_objects.overlayPixmap.OverlayPixmap('images/mic.png')
            self.sw = overlay_objects.overlayCircle.OverlayCircle()
            self.addObject(self.sw)
            self.animator.addAnim(self.sw.getWaveAnimation(self.width() / 2, self.height() * 2 / 3, mic_width, mic_height))

            animC1, animC2 = self.oc.circlePopIn(self.width() / 2, self.height() * 2 / 3, mic_width, mic_height)
            animM1, animM2 = self.mp.micPopIn(self.width() / 2, self.height() * 2 / 3, mic_width * 0.9, mic_height)

            animC1.after = lambda: self.animator.addAnim(animC2)
            animM1.after = lambda: self.animator.addAnim(animM2)

            self.addObject(self.oc)
            self.addObject(self.mp)

            self.animator.addAnim(animC1)
            self.animator.addAnim(animM1)


    @pyqtSlot()
    def shortcut_release_mic_key(self):  # Ctrl + M 때면
        print("released")
        if self.mp is not None:
            self.sw.destroy()

            animM1, animM2 = self.mp.micPopOut()
            animC1, animC2 = self.oc.circlePopOut()
            animM1.after = lambda: self.animator.addAnim(animM2)
            animC1.after = lambda: self.animator.addAnim(animC2)
            self.animator.addAnim(animM1)
            self.animator.addAnim(animC1)

            self.mp = None
            self.oc = None
            self.sw = None

    @pyqtSlot()
    def popUp(self):
        pass
