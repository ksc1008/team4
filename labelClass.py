from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui


class Label(QLabel):
    def __init__(self, parent, left = 100, top = 100, fontSize = 15, opacity = 0.5):
        super().__init__(parent)
        self.font = self.font()
        self.left = left
        self.top = top
        self.fontSize = fontSize
        self.text = ''

        self.pixmap = None

        self.color = None
        self.bg_color = None
        self.opacity = opacity

        self.move(self.left, self.top)
        self.font.setPointSize(self.fontSize)
        self.setFont(self.font)

        self.setStyleSheet(f"color: white;"
                           f"background-color: rgba(0,0,0,{self.opacity});"
                           )
        self.setWordWrap(True)

    def setTextContents(self, text):
        self.text = text
        self.setText(text)
        self.adjustSize()

    def moveLabel(self, left, top):
        self.left = left
        self.top = top
        self.move(self.left, self.top)

    def setImageByPixmap(self, image, width, height):
        self.pixmap = QIcon(image).pixmap(QSize(width, height))
        self.setPixmap(self.pixmap)
        self.resize(width, height)
