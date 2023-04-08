import time
import threading

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QMainWindow

from overlay_animations.animation import Animation
from signalManager import SignalManager


class Animator(threading.Thread):
    """
    애니메이션을 관리하고 매 프레임 등록된 각 애니메이션을 update하는 컨트롤 클래스
    """

    def __init__(self, window: QMainWindow):
        super(Animator, self).__init__()
        self.window = window
        self.interval_s = 1 / 100
        self.time_elapsed = 0.0
        self.animations = []
        self.onLoop = False
        self.daemon = True
        self.shouldStop = False

        SignalManager().programSignals.stop.connect(self.stop)

    def setFramerate(self, fps):
        self.interval_s = 1 / fps

    def stop(self):
        self.shouldStop = True
        print('stop')

    def addAnim(self, animation: Animation):
        self.animations.append(animation)
        animation.startAnim(self)

    @pyqtSlot()
    def run(self):
        while not self.shouldStop:
            for t in self.animations:
                t.update()
            self.window.update()
            time.sleep(self.interval_s)

        print('ended running')
