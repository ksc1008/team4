import time

import win32api
from PyQt6.QtCore import QThread, pyqtSignal


# 단축키
class ShorCut(QThread):
    quit_key = pyqtSignal()
    circle_key = pyqtSignal()
    mic_key = pyqtSignal()
    release_mic_key = pyqtSignal()
    demo_key = pyqtSignal()
    label_key = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.circle_pressing = False
        self.mic_pressing = False

    def run(self):
        while self.running:
            time.sleep(0.1)

            # <Ctrl+Q> 눌리면 -> quit_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x51) < 0:  # <Ctrl+Q> 입력
                print("<Ctrl+Q> -> [quit_key]")
                self.quit_key.emit()

            # <Ctrl+E> 눌리면 -> circle_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x45) < 0:  # <Ctrl+E> 입력
                if not self.circle_pressing:
                    self.circle_key.emit()
                    self.circle_pressing = True
            elif self.circle_pressing:
                self.circle_pressing = False

            # <Ctrl+M> 눌리면 -> mic_key
            # <Ctrl+M> 때면 -> mic_key_release
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x4D) < 0:  # <Ctrl+M> 입력
                if not self.mic_pressing:
                    print("<Ctrl+M> -> [pressing mic_key]")
                    self.mic_key.emit()
                    self.mic_pressing = True
            elif self.mic_pressing:
                print("[release mic_key]")
                self.release_mic_key.emit()
                self.mic_pressing = False

            # <Ctrl+D> 눌리면 -> demo_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x44) < 0:  # <Ctrl+D> 입력
                print("<Ctrl+D> -> [Demo key]")
                self.demo_key.emit()

            # <Ctrl+F1> 눌리면 -> label_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x70) < 0:  # <Ctrl+F1> 입력
                print("<Ctrl+F1> -> [label key]")
                self.label_key.emit()

    def stop(self):
        self.running = False
