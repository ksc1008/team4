from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *

from overlay_animations import animation
from overlay_animations.animation import Animation
from overlay_animations.animator import Animator


class TextLabel(QLabel):
    def __init__(self, parent, left=100, top=100, fontSize=32, opacity=0):
        super().__init__(parent)
        self.font = self.font()
        self.left = left
        self.top = top
        self.fontSize = fontSize
        self.text = ''

        self.color = QColor(255, 255, 255, 0)
        self.bg_color = None
        self.opacity = opacity

        self.move(self.left, self.top)
        self.font.setPointSize(self.fontSize)
        self.setFont(self.font)

        self.setStyleSheet(f"color: white;"
                           "border-radius: 5px;"
                           "padding: 3px;"
                           f"background-color: rgba(0,0,0,{self.opacity});"
                           )

        self.setWordWrap(True)
        shadow = QGraphicsDropShadowEffect()

        # setting blur radius
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0))

        # adding shadow to the label
        self.setGraphicsEffect(shadow)

        self.startAnim = None

    def setTextContents(self, text):
        self.text = text
        self.setText(text)
        self.adjustSize()

    def setSize(self, width, height):
        self.setMinimumWidth(width)
        self.setMinimumHeight(height)

    def parseColor(self, color: QColor) -> str:
        print(str.format('rgba({0},{1},{2},{3})', color.red(), color.green(), color.blue(), color.alpha()))
        return str.format('rgba({0},{1},{2},{3})', color.red(), color.green(), color.blue(), color.alpha())

    def setFontAlpha(self, alpha):
        self.color.setAlpha(alpha)

    def setBgAlpha(self, alpha):
        self.opacity = alpha

    def applyStyleSheet(self):
        self.setStyleSheet(
            str.format('color: {0};', self.parseColor(self.color)) +
            "border-radius: 5px;"
            "padding: 3px;"
            f"background-color: rgba(0,0,0,{self.opacity});")

    def t(self, start, end, t):
        fAlpha = start * (1 - t) + end * t
        bAlpha = fAlpha * 0.8
        self.setFontAlpha(fAlpha)
        self.setBgAlpha(bAlpha)
        self.applyStyleSheet()

    def removeAnim(self):
        self.startAnim = None

    def pop_in(self, animator: Animator):
        self.applyStyleSheet()
        anim = Animation(0, 255, self.t, 1000, animation.defaultEasing)
        anim.after = self.removeAnim
        self.startAnim = anim
        animator.addAnim(anim)
        self.show()

    def pop_out(self):
        if self.startAnim is not None:
            self.startAnim.finishAnim()
            self.startAnim = None
        self.setBgAlpha(0)
        self.setFontAlpha(0)
        self.hide()
