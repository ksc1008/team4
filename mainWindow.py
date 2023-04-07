from PyQt6.QtCore import *
from PyQt6.QtGui import QFontDatabase, QPainter, QColor, QFont
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

import overlay_objects.loadingCircle
import pyperclip

from keyboardEvent import ShorCut
from overlay_animations import animator, animation
from overlay_objects.overlayObject import OverlayObject
from overlay_objects.overlayLabel import OverlayLabel
from textLabel import TextLabel

import overlay_objects.overlayCircle
import overlay_objects.overlayPixmap
import overlay_objects.overlayCheck
import demo


class MainWindow(QMainWindow):
    font_folder = 'font'
    response = None

    def __init__(self, _t):
        super().__init__()

        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Bold.ttf')
        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Light.ttf')
        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Regular.ttf')
        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Medium.ttf')

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

        self.shortcut.circle_key.connect(self.shortcut_circle_key)              # disabled
        self.shortcut.check_key.connect(self.shortcut_check_key)                # disabled

        self.shortcut.quit_key.connect(self.shortcut_quit_key)
        self.shortcut.show_content_key.connect(self.shortcut_content_key)
        self.shortcut.mic_key.connect(self.shortcut_mic_key)
        self.shortcut.release_mic_key.connect(self.shortcut_release_mic_key)
        self.shortcut.copy_key.connect(self.shortcut_copy_key)
        self.shortcut.message_arrived.connect(self.on_message_arrived)
        self.shortcut.throw_error.connect(self.error_handle)
        self.shortcut.start_prompt.connect(self.startPrompting)
        self.animator.start()
        self.test = _t

        self.re = False

        self.lc = None
        self.oc = None
        self.mp = None
        self.sw = None
        self.rc = None

        self.label = TextLabel(self)
        # self.mic_image = PixmapLabel(self, 'images/mic_white.png')
        self.label.setTextContents("♥")

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
    def shortcut_quit_key(self):  # Ctrl + Q 입력시 프로그램 종료
        self.finAllObj()
        self.label.close()
        self.shortcut.stop()
        self.shortcut.terminate()
        self.close()

    @pyqtSlot()
    def shortcut_circle_key(self):  # Ctrl + E 입력 시 Loading Circle 추가 혹은 제거
        if self.lc is None:
            self.showLoadingCircle()
        else:
            self.hideLoadingCircle()

    @pyqtSlot()
    def shortcut_check_key(self):  # Ctrl + F2 입력 시 체크 표시
        self.popCheckIn()

    @pyqtSlot()
    def shortcut_content_key(self):
        if self.rc is not None:
            self.hideContent()
        else:
            self.showContent()

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
            self.animator.addAnim(
                self.sw.getWaveAnimation(self.width() / 2, self.height() * 2 / 3, mic_width, mic_height))

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

    @pyqtSlot()
    def shortcut_copy_key(self):
        if MainWindow.response is not None:
            pyperclip.copy(MainWindow.response)
        else:
            print('no answer from gpt.')

    @pyqtSlot(str)
    def on_message_arrived(self, data):
        MainWindow.response = data
        self.popCheckIn()
        self.endPrompting()

    @pyqtSlot(str)
    def error_handle(self, e):
        print(e)
        self.endPrompting()

    def popCheckIn(self):
        check_width = 100
        check_height = 100
        check = overlay_objects.overlayCheck.OverlayCheck(self.width() / 2, self.height() * 1 / 6)
        cc = overlay_objects.overlayCircle.OverlayCircle()
        cc.setColor(QColor(80, 200, 120, 200), QColor(80, 200, 120, 200))
        cc.pop_t = 400
        cc.exp_t = 300
        animC1, animC2 = cc.circlePopIn(self.width() / 2, self.height() * 1 / 6, check_width, check_height)

        popinAnim = check.getPopinAnimation()
        wait = animation.wait(1500)
        wait.after = lambda: self.popCheckOut(cc, check)
        popinAnim.after = lambda: [self.animator.addAnim(wait), check.removeAnim()]
        self.popLabelIn()
        animC1.after = lambda: [self.animator.addAnim(animC2), self.addObject(check),
                                self.animator.addAnim(popinAnim)]
        self.addObject(cc)
        self.animator.addAnim(animC1)

    def popCheckOut(self, cc, check):
        cc.pop_t = 300
        cc.exp_t = 200
        animC1, animC2 = cc.circlePopOut()
        animC1.after = lambda: self.animator.addAnim(animC2)
        self.animator.addAnim(animC1)
        popoutAnim = check.getPopoutAnimation()
        popoutAnim.after = check.destroy

        self.animator.addAnim(popoutAnim)

    def popLabelIn(self):
        ol = OverlayLabel("Response Arrived!")
        ol.setGeometry(self.width() / 2, self.height() * 1 / 6 + 150)
        a = ol.getResponseOpenAnimation(1200)
        self.addObject(ol)
        self.animator.addAnim(a)

    def showContent(self):
        if MainWindow.response is None:
            return

        ol = OverlayLabel(MainWindow.response, True)
        ol.setGeometry(100, 80)
        ol.setRect(QRectF(self.width() / 6, self.height() / 8, self.width() / 3 * 2, self.height() - 100))
        ol.textOpacity = 0
        ol.opacity = 0
        a1, a2 = ol.getContentOpenAnimation()
        self.addObject(ol)
        self.animator.addAnim(a1)
        self.animator.addAnim(a2)
        self.rc = ol

    def hideContent(self):
        if self.rc is not None:
            self.rc.destroy()
            self.rc = None

    def showLoadingCircle(self):
        if self.lc is None:
            self.lc = overlay_objects.loadingCircle.LoadingCircle()
            self.lc.setGeometry(self.width() / 2, self.height() / 6, 40, 7)
            self.lc.circle_interval = 0.065

            self.addObject(self.lc)
            self.animator.addAnim(self.lc.getCycleAnimation())

    def hideLoadingCircle(self):
        if self.lc is not None:
            self.lc.destroy()
            self.lc = None

    @pyqtSlot()
    def startPrompting(self):
        self.showLoadingCircle()
        self.shortcut.readyToListen = True

    def endPrompting(self):
        self.hideLoadingCircle()
        self.shortcut.readyToListen = True
