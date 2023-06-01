import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from signalManager import TraySignal, SignalManager

from option_window.gui import Ui_MainWindow as Gui_option
from option_window.gui_gpt import Option_MainWindow

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, _t, parent=None):
        icon = QIcon('images/icon.png')
        QSystemTrayIcon.__init__(self, icon, parent)
        tray_menu = QMenu(parent)

        self.traySignals = SignalManager().traySignals
        self._progApp = _t

        optionAction = tray_menu.addAction("설정")
        optionAction.triggered.connect(self.option_clicked)

        exitAction = tray_menu.addAction("종료")
        exitAction.triggered.connect(self.exit_program)

        self.setContextMenu(tray_menu)
        print("tray show")
        self.show()

    def option_clicked(self):
        print("option 실행")
        self.traySignals.option_clicked.emit()
        #self.option = Option_MainWindow()

    def exit_program(self):
        self._progApp.exit()