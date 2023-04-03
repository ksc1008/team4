from PyQt6.QtWidgets import *


class TextLabel(QLabel):
    def __init__(self, parent, left = 100, top = 100, fontSize = 15, opacity = 0.5):
        super().__init__(parent)
        self.font = self.font()
        self.left = left
        self.top = top
        self.fontSize = fontSize
        self.text = ''

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
