import PyQt6
from PyQt6.QtCore import *
from PyQt6.QtGui import QFontDatabase, QPainter, QColor, QFont
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

import overlay_objects.loadingCircle
import pyperclip

from keyboardEvent import KeyboardEvents
from overlay_animations import animator, animation
from overlay_objects.overlayObject import OverlayObject
from overlay_objects.overlayLabel import OverlayLabel
from signalManager import SignalManager, KeyboardSignal, OverlaySignal, ProgramSignal, TraySignal
from option_window.gui_gpt import Option_MainWindow
from textLabel import TextLabel

import overlay_objects.overlayCircle
import overlay_objects.overlayPixmap
import overlay_objects.overlayCheck
import demo
import tray


class MainWindow(QMainWindow):
    font_folder = 'font'
    response = None

    def __init__(self, _t):
        super().__init__()

        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Bold.ttf')
        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Light.ttf')
        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Regular.ttf')
        QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Medium.ttf')

        # OverlayObject 객체 리스트
        self.objects = []

        self.keyboardSignal = KeyboardSignal
        self.overlaySignal = OverlaySignal
        self.programSignal = ProgramSignal
        self.traySignal = TraySignal

        self.animator = animator.Animator(self)
        self.animator.start()
        self._progApp = _t

        self._loadingCircle = None
        self._micCircle = None
        self._micImage = None
        self._micCircleWave = None
        self._contentLabel = None

        self.initiateWindow()
        self.initiateSignals()

        self.show()

    def initiateWindow(self):
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.showFullScreen()

    def initiateSignals(self):
        self.keyboardSignal = SignalManager().keyboardSignals
        self.overlaySignal = SignalManager().overlaySignals
        self.programSignal = SignalManager().programSignals
        self.traySignal = SignalManager().traySignals

        self.keyboardSignal.quit_key.connect(self.shortcut_quit_key)
        self.keyboardSignal.show_content_key.connect(self.shortcut_content_key)
        self.keyboardSignal.copy_key.connect(self.shortcut_copy_key)

        self.overlaySignal.message_arrived.connect(self.on_message_arrived)
        self.overlaySignal.throw_error.connect(self.error_handle)
        self.overlaySignal.start_prompt.connect(self.onPromptStart)
        self.overlaySignal.on_start_rec.connect(self.on_rec_start)
        self.overlaySignal.on_stop_rec.connect(self.on_rec_end)

        self.traySignal.option_clicked.connect(self.open_trayoption)


    # 오버라이드 할 paintEvent
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        for o in self.objects:
            o.draw(painter)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._progApp.exit(0)

    def addObject(self, obj: OverlayObject):  # 메인 윈도우의 objects에 새 오브젝트를 추가.
        self.objects.append(obj)
        obj.window = self

    def finAllObj(self):
        for o in self.objects:
            o.destroy()

    def open_trayoption(self):
        option = Option_MainWindow()
        option.exec()

    @pyqtSlot()
    def shortcut_quit_key(self):  # Ctrl + Q 입력시 프로그램 종료
        self.programSignal.stop.emit()
        self.close()

    @pyqtSlot()
    def shortcut_content_key(self):
        if self._contentLabel is not None:
            self.hideContent()
        else:
            self.showContent()

    @pyqtSlot()
    def on_rec_start(self):  # Ctrl + M 눌리면
        print("pressing")
        mic_width = 200
        mic_height = 200
        if self._micImage is None:
            self._micCircle = overlay_objects.overlayCircle.OverlayCircle()
            self._micImage = overlay_objects.overlayPixmap.OverlayPixmap('images/mic.png')
            self._micCircleWave = overlay_objects.overlayCircle.OverlayCircle()
            self.addObject(self._micCircleWave)
            self.animator.addAnim(
                self._micCircleWave.getWaveAnimation(self.width() / 2, self.height() * 2 / 3, mic_width, mic_height))

            animC1, animC2 = self._micCircle.circlePopIn(self.width() / 2, self.height() * 2 / 3, mic_width, mic_height)
            animM1, animM2 = self._micImage.micPopIn(self.width() / 2, self.height() * 2 / 3, mic_width * 0.9,
                                                     mic_height)

            animC1.after = lambda: self.animator.addAnim(animC2)
            animM1.after = lambda: self.animator.addAnim(animM2)

            self.addObject(self._micCircle)
            self.addObject(self._micImage)

            self.animator.addAnim(animC1)
            self.animator.addAnim(animM1)

    @pyqtSlot()
    def on_rec_end(self):  # Ctrl + M 때면
        print("released")
        if self._micImage is not None:
            self._micCircleWave.destroy()

            animM1, animM2 = self._micImage.micPopOut()
            animC1, animC2 = self._micCircle.circlePopOut()
            animM1.after = lambda: self.animator.addAnim(animM2)
            animC1.after = lambda: self.animator.addAnim(animC2)
            self.animator.addAnim(animM1)
            self.animator.addAnim(animC1)

            self._micImage = None
            self._micCircle = None
            self._micCircleWave = None

    @pyqtSlot()
    def shortcut_copy_key(self):
        if MainWindow.response is not None:
            pyperclip.copy(MainWindow.response)
            self.popBalloon('Copied!', QColor(80, 200, 120, 200))
        else:
            print('no answer from gpt.')
            self.popBalloon('Nothing to copy', QColor(0xcc, 0, 0, 200))

    @pyqtSlot(str)
    def on_message_arrived(self, data):
        MainWindow.response = data
        self.popCheckIn()
        self.onPromptEnd()

    @pyqtSlot(str)
    def error_handle(self, e):
        print(e)
        self.popBalloon(e, QColor(0xcc, 0, 0, 200), 3000)
        self.onPromptEnd()

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

    def popBalloon(self, text, back_color, duration=1000, font_color=QColor(255, 255, 255, 255)):
        ol = OverlayLabel(text, True)
        ol.setGeometry(self.width() / 2, self.height() / 6)
        ol.setRect(QRectF(self.width() / 2 - 225, self.height() / 6 - 43, 450, 150))
        ol.align = PyQt6.QtCore.Qt.AlignmentFlag.AlignHCenter
        ol.textColor = font_color
        ol.color = back_color
        ol.outline = back_color
        ol.textOpacity = 0
        ol.opacity = 0

        ol.font = QFont(['Roboto', ol.defaultFontFamily], ol.fontSize, weight=700)

        a1, a2 = ol.getContentOpenAnimation()

        self.addObject(ol)
        wait = animation.wait(duration)

        def after():
            a3, a4 = ol.getFadeoutAnimation()
            self.animator.addAnim(a3)
            self.animator.addAnim(a4)

        wait.after = after
        a2.after = lambda: [ol.removeAnim(a2), self.animator.addAnim(wait)]
        self.animator.addAnim(a1)
        self.animator.addAnim(a2)

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
        self._contentLabel = ol

    def hideContent(self):
        if self._contentLabel is not None:
            self._contentLabel.destroy()
            self._contentLabel = None

    def showLoadingCircle(self):
        if self._loadingCircle is None:
            self._loadingCircle = overlay_objects.loadingCircle.LoadingCircle()
            self._loadingCircle.setGeometry(self.width() / 2, self.height() / 6, 40, 7)
            self._loadingCircle.circle_interval = 0.065

            self.addObject(self._loadingCircle)
            self.animator.addAnim(self._loadingCircle.getCycleAnimation())

    def hideLoadingCircle(self):
        if self._loadingCircle is not None:
            self._loadingCircle.destroy()
            self._loadingCircle = None

    @pyqtSlot()
    def onPromptStart(self):
        self.showLoadingCircle()

    def onPromptEnd(self):
        self.hideLoadingCircle()
