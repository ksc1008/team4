from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui


class TextLabel(QLabel):

    def __init__(self, mainWindow):
        super().__init__(parent=mainWindow)
        self.font = self.font()
        self.palette = QPalette()
        self.left = 100
        self.top = 100
        self.fontSize = 15
        self.text = ""

        self.move(self.left, self.top)
        self.font.setPointSize(self.fontSize)
        self.setFont(self.font)

        self.setStyleSheet("color: white;"
                           "background-color: rgba(0,0,0,0.5);"
                           )
        self.setWordWrap(True)

    def setTextLabel(self, text):
        self.text = text
        self.setText(text)
        self.adjustSize()