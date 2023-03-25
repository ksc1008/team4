import time
import threading

from PyQt6.QtWidgets import QMainWindow


class Animator(threading.Thread):

    def __init__(self, window: QMainWindow):
        super(Animator, self).__init__()
        self.window = window
        self.interval_s = 1/144
        self.time_elapsed = 0.0
        self.animations = []
        self.onLoop = False
        self.daemon = True

    def removeAnim(self, animation):
        self.animations.remove(animation)

    def startAnim(self, animation):
        self.animations.append(animation)
        animation.startAnim(self)
        if not self.onLoop:
            try:
                self.onLoop = True
                self.start()
            except RuntimeError as e:
                print(e)

    def run(self):
        self.onLoop = True
        while len(self.animations) > 0:
            for t in self.animations:
                t.invoke()
            self.window.update()
            time.sleep(self.interval_s)
        self.onLoop = False
