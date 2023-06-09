import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import *
import mainWindow
from ChatGPT1 import MyWindow
from keyboardEvent import KeyboardEvents
import document_loader.indexCreator


if __name__ == '__main__':

    app = QApplication(sys.argv)
    document_loader.indexCreator.loadDB()
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
