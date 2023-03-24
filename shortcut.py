import time

import win32api
from PySide6.QtCore import QThread, Signal

# 단축키
class ShorCut(QThread):
    main_to_second = Signal()
    second_to_main = Signal()
    exit_key = Signal()

    def __init__(self):
        super().__init__()
        self.maintop = True
        self.running = True

    def run(self):
        while self.running:
            time.sleep(0.1)
            # 창 전환
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x70) < 0:  # <Ctrl+F1> 입력
                if self.maintop:
                    print("<Ctrl+F1> -> [main to second]")
                    self.main_to_second.emit()
                    self.maintop = False
                else:
                    print("<Ctrl+F1> -> [second to main]")
                    self.second_to_main.emit()
                    self.maintop = True
            # exit
            if win32api.GetAsyncKeyState(0x11) < 0 and win32api.GetAsyncKeyState(0x51) < 0:  # <Ctrl+Q> 입력
                print("<Ctrl+Q> -> [Exit]")
                self.exit_key.emit()

    def stop(self):
        self.running = False
