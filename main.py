import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import *
import mainWindow
from ChatGPT1 import MyWindow


class MySignal(QObject):
    button_clicked = pyqtSignal()
    shortcut = None

    def setSignal(self, sig):
        MySignal.shortcut = sig
        MySignal.shortcut.test_key.connect(self.shortcut_label_key)

    def __init__(self):
        super().__init__()
        self.shortcut = None

    @pyqtSlot()
    def shortcut_label_key(self):  # Ctrl + F1 입력시 label 보이기 / 숨기기
        print('slot works!')


def on_button_clicked():
    print('Button clicked')


if __name__ == '__main__':

    app = QApplication(sys.argv)

    gptWindow = MyWindow()
    window = mainWindow.MainWindow(app)
    gptWindow.initiate(window.shortcut)
    my_signal = MySignal()
    my_signal.setSignal(window.shortcut)
    # window.showFullScreen()

    try:
        sys.exit(app.exec())
    except SystemExit:
        window.animator.stop()
        window.close()

    print('window closed')
