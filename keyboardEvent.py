import time

import win32api
from PyQt6.QtCore import QThread, pyqtSignal


# 단축키
class ShorCut(QThread):
    exit_key = pyqtSignal()
    circle_key = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.maintop = True
        self.running = True
        self.circle_pressing = False

    def run(self):
        while self.running:
            time.sleep(0.1)
            # exit
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x51) < 0:  # <Ctrl+Q> 입력
                print("<Ctrl+Q> -> [Exit]")
                self.exit_key.emit()

            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x45) < 0:  # <Ctrl+E> 입력
                if not self.circle_pressing:
                    self.circle_key.emit()
                    self.circle_pressing = True
            elif self.circle_pressing:
                self.circle_pressing = False


    def stop(self):
        self.running = False