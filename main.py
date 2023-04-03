import sys

from PyQt6.QtWidgets import *
import mainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow(app)
    # window.showFullScreen()

    try:
        sys.exit(app.exec())
    except SystemExit:
        window.animator.stop()
        window.close()

    print('window closed')
