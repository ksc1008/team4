import time

import win32api
from PyQt6.QtCore import QThread, pyqtSlot

# 단축키
from signalManager import SignalManager
from optiondata import Option_data
from option_window.ascii import Keyboard_ascii


class KeyboardEvents(QThread):
    def __init__(self):
        super().__init__()
        self.option_data = Option_data()
        self.ascii = Keyboard_ascii()
        self.running = True
        self.mic_pressing = False
        self.f2_pressing = False
        self.content_pressing = False
        self.copy_pressing = False

        self.keyboardSignals = SignalManager().keyboardSignals
        self.optionSignals = SignalManager().optionSignals
        SignalManager().programSignals.stop.connect(self.stop)
        self.optionSignals.changed_key.connect(self.key_update)


    def run(self):
        while self.running:
            time.sleep(0.1)
            # <Ctrl+Q> 눌리면 -> quit_key
            if win32api.GetAsyncKeyState(self.ascii.combination_ascii(self.option_data.quit_key_combination)) < 0 and win32api.GetAsyncKeyState(self.ascii.keytoascii(self.option_data.quit_key)) < 0:  # <Ctrl+Q> 입력
                print("[quit_key]")
                self.keyboardSignals.quit_key.emit()

            # <Ctrl+M> 눌리면 -> mic_pressing
            if win32api.GetAsyncKeyState(self.ascii.combination_ascii(self.option_data.pressing_mic_key_combination)) < 0 and win32api.GetAsyncKeyState(self.ascii.keytoascii(self.option_data.pressing_mic_key)) < 0:  # <Ctrl+M> 입력
                if not self.mic_pressing:
                    print("[pressing mic_key]")
                    self.keyboardSignals.mic_key.emit()
                    self.mic_pressing = True
                    time.sleep(0.5)
            elif self.mic_pressing:
                print("[release mic_key]")
                self.keyboardSignals.release_mic_key.emit()
                self.mic_pressing = False

            # <Ctrl+F3> 눌리면 -> content_key
            if win32api.GetAsyncKeyState(self.ascii.combination_ascii(self.option_data.show_content_key_combination)) < 0 and win32api.GetAsyncKeyState(self.ascii.keytoascii(self.option_data.show_content_key)) < 0:  # <Ctrl+F3> 입력
                if not self.content_pressing:
                    self.keyboardSignals.show_content_key.emit()
                    self.content_pressing = True
                    print("[show content key]")
            elif self.content_pressing:
                self.content_pressing = False

            # <Ctrl+F4> 눌리면 -> copy_key
            if win32api.GetAsyncKeyState(self.ascii.combination_ascii(self.option_data.copy_key_combination)) < 0 and win32api.GetAsyncKeyState(self.ascii.keytoascii(self.option_data.copy_key)) < 0:  # <Ctrl+F4> 입력
                if not self.copy_pressing:
                    self.keyboardSignals.copy_key.emit()
                    self.copy_pressing = True
                    print("<Ctrl+F4> -> [copy key]")
            elif self.copy_pressing:
                self.copy_pressing = False

    #키 업데이트 시 값 로딩
    def key_update(self):
        self.option_data.load_option()

    @pyqtSlot()
    def stop(self):
        self.running = False
        self.terminate()
