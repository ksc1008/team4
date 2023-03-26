import time

import win32api
from PyQt6.QtCore import QThread, pyqtSignal


# 단축키
class ShorCut(QThread):
    exit_key = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.maintop = True
        self.running = True

    def run(self):
        while self.running:
            time.sleep(0.1)
            # exit
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x51) < 0:  # <Ctrl+Q> 입력
                print("<Ctrl+Q> -> [Exit]")
                self.exit_key.emit()


    def stop(self):
        self.running = False
