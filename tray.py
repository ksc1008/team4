import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        icon = QIcon('images/icon.png')
        QSystemTrayIcon.__init__(self, icon, parent)
        tray_menu = QMenu(parent)

        optionAction = tray_menu.addAction("설정")
        # optionAction.triggered.connect()

        exitAction = tray_menu.addAction("종료")
        exitAction.triggered.connect(QCoreApplication.instance().quit)

        self.setContextMenu(tray_menu)


def main():
    app = QApplication(sys.argv)
    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon('icon.png'), w)
    trayIcon.show()
    sys.exit(app.exec())