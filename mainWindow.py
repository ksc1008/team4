from PyQt6.QtCore import *
from PyQt6.QtGui import QFontDatabase, QPainter, QColor
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui

import overlay_objects.loadingCircle
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
    roboto_fonts = []

    def __init__(self, _t):
        super().__init__()

        roboto_bold = QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Bold.ttf')
        roboto_light = QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Light.ttf')
        roboto = QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Regular.ttf')
        roboto_medium = QFontDatabase.addApplicationFont(MainWindow.font_folder + '/Roboto-Medium.ttf')
        MainWindow.roboto_fonts = [QFontDatabase.applicationFontFamilies(roboto)[0],            # weight 400
                                   QFontDatabase.applicationFontFamilies(roboto_light)[0],      # weight 300
                                   QFontDatabase.applicationFontFamilies(roboto_medium)[0],      # weight 500
                                   QFontDatabase.applicationFontFamilies(roboto_bold)[0]]       # weight 700
        print(MainWindow.roboto_fonts)

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
            self.lc.setGeometry(self.width() / 2, self.height() / 6, 45, 8)

            self.addObject(self.lc)
            self.animator.addAnim(self.lc.getCycleAnimation())
        else:
            self.lc.destroy()
            self.lc = None

    @pyqtSlot()
    def shortcut_check_key(self):  # Ctrl + F2 입력 시 체크 표시
        self.popCheckIn()

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
        ol.setGeometry(self.width() / 2, self.height() * 1 / 6+150)
        a = ol.getOpenAnimation(1200)
        self.addObject(ol)
        self.animator.addAnim(a)

