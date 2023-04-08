import time

import win32api
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

# 단축키
from signalManager import SignalManager


class KeyboardEvents(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.mic_pressing = False
        self.f2_pressing = False
        self.f3_pressing = False
        self.f4_pressing = False

        self.keyboardSignals = SignalManager().keyboardSignals
        SignalManager().programSignals.stop.connect(self.stop)

    def run(self):
        while self.running:
            time.sleep(0.1)
            # <Ctrl+Q> 눌리면 -> quit_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x51) < 0:  # <Ctrl+Q> 입력
                print("<Ctrl+Q> -> [quit_key]")
                self.keyboardSignals.quit_key.emit()

            # <Ctrl+M> 눌리면 -> mic_pressing
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x4D) < 0:  # <Ctrl+M> 입력
                if not self.mic_pressing:
                    print("<Ctrl+M> -> [pressing mic_key]")
                    self.keyboardSignals.mic_key.emit()
                    self.mic_pressing = True
                    time.sleep(0.5)
            elif self.mic_pressing:
                print("[release mic_key]")
                self.keyboardSignals.release_mic_key.emit()
                self.mic_pressing = False

            # <Ctrl+F3> 눌리면 -> content_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x72) < 0:  # <Ctrl+F3> 입력
                if not self.f3_pressing:
                    self.keyboardSignals.show_content_key.emit()
                    self.f3_pressing = True
                    print("<Ctrl+F3> -> [show content key]")
            elif self.f3_pressing:
                self.f3_pressing = False

            # <Ctrl+F4> 눌리면 -> copy_key
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x73) < 0:  # <Ctrl+F4> 입력
                if not self.f4_pressing:
                    self.keyboardSignals.copy_key.emit()
                    self.f4_pressing = True
                    print("<Ctrl+F4> -> [copy key]")
            elif self.f4_pressing:
                self.f4_pressing = False

    @pyqtSlot()
    def stop(self):
        self.running = False
        self.terminate()
