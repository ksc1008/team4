import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import *
import mainWindow
from ChatGPT1 import MyWindow
from keyboardEvent import KeyboardEvents
from optiondata import Option_data
from signalManager import SignalManager
import tray
from option_window.gui_gpt import Option_MainWindow
import document_loader.indexCreator


if __name__ == '__main__':

    option_data = Option_data()

    app = QApplication(sys.argv)
    if option_data.openai_api_key != '':
        document_loader.indexCreator.loadDB()

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
        SignalManager().traySignals.history_save.emit()
        window.close()

    print('window closed')
