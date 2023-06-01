from PyQt6.QtCore import pyqtSignal, QObject


# 싱글톤 객체 -> 프로그램 수명 주기중, 단 하나의 unique한 객체만 존재함을 보장
class SignalManager(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            print('an event manager instance created')
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.keyboardSignals = KeyboardSignal()
            self.overlaySignals = OverlaySignal()
            self.programSignals = ProgramSignal()
            self.traySignals = TraySignal()
            self.optionSignals = OptionSignal()
            print('signal manager has init')
            cls._init = True


class KeyboardSignal(QObject):
    test_key: pyqtSignal = pyqtSignal()
    mic_key = pyqtSignal()
    release_mic_key = pyqtSignal()
    show_content_key = pyqtSignal()
    copy_key = pyqtSignal()
    quit_key = pyqtSignal()


class OverlaySignal(QObject):
    throw_error = pyqtSignal(str)
    message_arrived = pyqtSignal(str)
    start_prompt = pyqtSignal()
    on_start_rec = pyqtSignal()
    on_stop_rec = pyqtSignal()
    answer_streaming = pyqtSignal(str)


class ProgramSignal(QObject):
    stop = pyqtSignal()

class TraySignal(QObject):
    option_clicked = pyqtSignal()

class OptionSignal(QObject):
    current_path_saved = pyqtSignal(str)
    current_checked_api = pyqtSignal(str)
    current_parameter = pyqtSignal(list)
    changed_path_saved = pyqtSignal(str)
    changed_checked_api = pyqtSignal(str)
    changed_parameter = pyqtSignal(list)
