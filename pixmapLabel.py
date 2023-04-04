from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class PixmapLabel(QLabel):
    def __init__(self, parent, image=None, left=100, top=100, width=100, height=100):
        super().__init__(parent)
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.image = image

        self.pixmap = QIcon(self.image).pixmap(QSize(self.width, self.height))

        self.bg_color = None
        self.opacity = 0

        self.setStyleSheet(f"background-color: rgba(0,0,0,{self.opacity});")
        self.setPixmap(self.pixmap)
        self.move(self.left, self.top)
        self.resize(self.width, self.height)

    def movePixmap(self, left, top):
        self.left = left
        self.top = top
        self.move(self.left, self.top)

    def showImageByPixmap(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.pixmap = QIcon(self.image).pixmap(QSize(self.width, self.height))
        self.setPixmap(self.pixmap)
        self.resize(self.width, self.height)
