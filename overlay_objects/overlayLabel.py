import PyQt6
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QFont, QFontDatabase
from PyQt6.QtCore import QRect, QRectF

import mainWindow
from overlay_animations.animation import Animation
from overlay_objects.overlayObject import OverlayObject
from overlay_animations import animation


class OverlayLabel(OverlayObject):
    def __init__(self, text: str):
        super().__init__()
        self.circle = QRect()
        self.outline = QColor(0, 0, 0, 255)
        self.color = QColor(0, 0, 0, 255)
        self.textColor = QColor(255, 255, 255, 255)
        self.manualColor = QColor(255, 255, 255, 150)

        self.boxWidth = 450
        self.boxHeight = 85
        self.fontSize = 16
        self.manualFontSize = 12

        self.manualLeft = 'Ctrl + F3 : show text'
        self.manualRight = 'Ctrl + F4 : copy text'

        self.left = 500
        self.top = 200
        self.opacity = 0.8
        self.textOpacity = 1
        self.manualOpacity = 1

        self.rect = QRectF(0, 0, 0, 0)

        self.text = text

        self.pop_t: int = 300
        self.exp_t: int = 100
        self.delay: int = 50
        self.wrapMode = PyQt6.QtGui.QTextOption.WrapMode.NoWrap

        self._anims = []

    def draw(self, painter: QPainter):
        painter.setOpacity(self.opacity)
        painter.setPen(self.outline)
        painter.setBrush(self.color)

        path = QPainterPath()
        path.addRoundedRect(self.rect, 10, 10)
        painter.drawPath(path)

        painter.setOpacity(self.textOpacity)
        font = QFont([mainWindow.MainWindow.roboto_fonts[0], 'Arial'], self.fontSize, weight=400)
        opt = PyQt6.QtGui.QTextOption()
        opt.setWrapMode(self.wrapMode)
        opt.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignHCenter)

        painter.setFont(font)
        painter.setPen(self.textColor)
        self.rect.adjust(5, 15, -5, -5)
        painter.drawText(self.rect, self.text, opt)

        bound = painter.boundingRect(self.rect, self.text, opt)

        self.drawManual(painter)

    def drawManual(self, painter):
        painter.setOpacity(self.manualOpacity)
        opt = PyQt6.QtGui.QTextOption()
        opt.setWrapMode(self.wrapMode)
        opt.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignBottom | PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        font = QFont([mainWindow.MainWindow.roboto_fonts[1], 'Arial'], self.manualFontSize, weight=300)
        painter.setFont(font)
        painter.setPen(self.manualColor)

        opt.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignBottom | PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        painter.drawText(self.rect, self.manualLeft, opt)
        opt.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignBottom | PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        painter.drawText(self.rect, self.manualRight, opt)
        self.rect.adjust(-5, -15, 5, 5)

    def setColor(self, color: QColor, outline: QColor):
        self.color = color
        self.outline = outline

    def setWrappingMode(self, isWrapEnabled: bool):
        if isWrapEnabled:
            self.wrapMode = PyQt6.QtGui.QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere
        else:
            self.wrapMode = PyQt6.QtGui.QTextOption.WrapMode.NoWrap

    def setOpacity(self, opacity):
        self.opacity = opacity

    def setGeometry(self, left, top):
        self.left = left
        self.top = top

    def setRect(self, rect):
        self.rect = rect

    def removeAnim(self, anim):
        self._anims.remove(anim)

    def getOpenAnimation(self, delay_until_close):
        sz = self.fontSize

        def setTextOpacity(o):
            self.textOpacity = o
            self.manualOpacity = o
            self.opacity = o * 5 if o < 0.16 else 0.8

        setter = lambda w: [self.setRect(QRectF(self.left - w / 2, self.top - self.boxHeight / 2, w, self.boxHeight)),
                            setTextOpacity(w / self.boxWidth)]

        def easeinoutquart(x):
            if x < 0.5:
                return 8 * x * x * x * x
            else:
                return 1 - pow(-2 * x + 2, 4) / 2

        def addAnim(anim):
            self._anims.append(anim)

        firstAnim = animation.make_var_anim(setter, 0, self.boxWidth, 1000, easeinoutquart)

        w2 = animation.wait(delay_until_close)
        w2.after = lambda: [w2.animator.addAnim(self.getCloseAnimation()), self.removeAnim(w2)]

        firstAnim.after = lambda: [self.removeAnim(firstAnim), firstAnim.animator.addAnim(w2), addAnim(w2)]
        addAnim(firstAnim)

        return firstAnim

    def getCloseAnimation(self):

        def setTextOpacity(o):
            self.textOpacity = o
            self.manualOpacity = pow(o, 10)

        setter = lambda w: [self.setRect(QRectF(self.left - w / 2, self.top - self.boxHeight / 2, w, self.boxHeight)),
                            setTextOpacity(w / self.boxWidth)]
        easeinexpo = lambda x: 0 if x == 0 else pow(2, 10 * x - 10)

        anim = animation.make_var_anim(setter, self.boxWidth, 0, 600, easeinexpo)
        anim.after = lambda: [self.removeAnim(anim), self.destroy()]

        self._anims.append(anim)
        return anim

    def destroy(self):
        for a in self._anims:
            a.finishAnim()
        super().destroy()
