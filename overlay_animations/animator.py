import time
import threading

from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QMainWindow

from overlay_animations import testAnimation


class Animator(threading.Thread):

    def __init__(self, window: QMainWindow):
        super(Animator, self).__init__()
        self.window = window
        self.interval_s = 1/144
        self.time_elapsed = 0.0
        self.animations = []
        self.animatedObjects = []
        self.onLoop = False
        self.daemon = True
        self.shouldStop = False

    def stop(self):
        self.shouldStop = True
        print('stop')
    def removeAnim(self, animation):
        self.animations.remove(animation)

    def removeAnimatedObject(self, animatedObject):
        self.animatedObjects.remove(animatedObject)

    def startAnim(self, animation):
        self.animations.append(animation)
        animation.startAnim(self)

    def run(self):
        while not self.shouldStop:
            if len(self.animations) > 0:
                for t in self.animations:
                    t.invoke()
                self.window.update()

            time.sleep(self.interval_s)

        print('ended running')

    def update(self, painter: QPainter):
        for a in self.animatedObjects:
            a.draw(painter)


    # 테스트 애니메이션 시작
    def startTestAnimation(self):
        obj = testAnimation.TestAnimation(self)
        self.animatedObjects.append(obj)
        obj.startAnim()

    # Loading Circle 시작. (구현 안 됨)
    def startLoadingCircle(self):
        pass

    # 녹음 애니메이션 시작. (구현 안 됨)
    def startRecAnimation(self):
        pass

    def stopLoadingCircle(self):
        pass

    def stopRecAnimation(self):
        pass

    # 텍스트 띄움
    def PopUpText(self, text: str):
        pass


