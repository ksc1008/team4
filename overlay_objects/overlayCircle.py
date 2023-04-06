from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QRect
from overlay_objects.overlayObject import OverlayObject
from overlay_animations import animation


class OverlayCircle(OverlayObject):
    def __init__(self):
        super().__init__()
        self.circle = QRect()
        self.outline = QColor(0, 0, 0, 0)
        self.color = QColor(0, 0, 0, 0)
        self.left = 0
        self.top = 0
        self.radius = 0
        self.expand = 1.1

        self.pop_t: int = 300
        self.exp_t: int = 100
        self.delay: int = 50

        self._anim = None

    def draw(self, painter: QPainter):
        painter.setPen(self.outline)
        painter.setBrush(self.color)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.drawEllipse(self.circle)

    def setCircle(self, circle: QRect):
        self.circle = circle

    def setColor(self, color: QColor, outline: QColor):
        self.color = color
        self.outline = outline

    def setGeometry(self, left, top, width):
        self.left = left
        self.top = top
        self.radius = width / 2

    def circlePopIn(self, left, top, width, height):
        if self._anim is not None:
            return self._anim
        self.color = QColor(255, 255, 255, 128)
        self.outline = QColor(255, 255, 255, 128)
        self.setColor(self.color, self.outline)

        leftS = left
        topS = top
        self.setGeometry(left, top, width)

        widthE = width * self.expand
        heightE = height * self.expand

        easeInOutQuint = lambda x: (16 * x * x * x * x * x) if x < 0.5 else (1 - pow(-2 * x + 2, 5) / 2)
        anim = animation.make_rect_anim(self.setCircle, QRect(int(leftS), int(topS), 0, 0),
                                        QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE), int(heightE)),
                                        self.pop_t, easeInOutQuint)

        easeOutQuint = lambda x: 1 - pow(1 - x, 5)
        anim2 = animation.make_rect_anim(self.setCircle,
                                         QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE),
                                               int(heightE)),
                                         QRect(int(leftS - width / 2), int(topS - height / 2), int(width), int(height)),
                                         self.exp_t, easeOutQuint)

        return anim, anim2

    def circlePopOut(self):
        leftS = self.left
        topS = self.top
        width = self.radius * 2
        height = self.radius * 2

        widthE = width * self.expand
        heightE = height * self.expand

        easeInQuint = lambda x: x * x * x * x
        anim = animation.make_rect_anim(self.setCircle,
                                        QRect(int(leftS - width / 2), int(topS - height / 2), int(width), int(height)),
                                        QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE),
                                              int(heightE)),
                                        self.exp_t + self.delay, easeInQuint)

        easeInOutQuint = lambda x: (16 * x * x * x * x * x) if x < 0.5 else (1 - pow(-2 * x + 2, 5) / 2)

        anim2 = animation.make_rect_anim(self.setCircle,
                                         QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE),
                                               int(heightE)),
                                         QRect(int(leftS), int(topS), 0, 0),
                                         self.pop_t, easeInOutQuint)

        anim2.after = lambda : self.destroy()

        return anim, anim2

    def getWaveAnimation(self, left, top, width, height):
        if self._anim is not None:
            return self._anim

        self.color = QColor(0, 0, 0, 0)
        self.outline = QColor(255, 255, 255, 128)
        self.setColor(self.color, self.outline)

        leftT = left - width / 2
        topT = top - height / 2

        expand = 1.4

        widthE = width * expand
        heightE = height * expand

        newTime = 1000

        method = lambda r1, r2, t: (self.setCircle(QRect(
            (1 - t) * r1.topLeft() + t * r2.topLeft(),
            (1 - t) * r1.bottomRight() + t * r2.bottomRight())
        ))

        easing = lambda t: t if t < 1 else t % 1

        newAnim = animation.Animation(QRect(int(leftT), int(topT), int(width), int(height)),
                                    QRect(int(left - widthE / 2), int(top - heightE / 2), int(widthE), int(heightE)),
                                      method, newTime, easing)

        self._anim = newAnim

        return newAnim

    def destroy(self):
        if self._anim is not None:
            self._anim.finishAnim()
        super().destroy()
