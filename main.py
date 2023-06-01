import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import *
import mainWindow
from ChatGPT1 import MyWindow
from keyboardEvent import KeyboardEvents
import tray
from option_window.gui_gpt import Option_MainWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)

    widget = QWidget()
    trayIcon = tray.SystemTrayIcon(app, widget)
    #tray 실행

    keyboardEvent = KeyboardEvents()
    keyboardEvent.start()

    gptWindow = MyWindow()
    window = mainWindow.MainWindow(app)
    # window.showFullScreen()


    try:
        sys.exit(app.exec())
    except SystemExit:
        window.close()

    print('window closed')
