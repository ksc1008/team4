import math

from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor
from overlay_objects.overlayObject import OverlayObject
from overlay_animations.animation import Animation


class LoadingCircle(OverlayObject):

    def __init__(self):
        super().__init__()
        self.opacity = 0.8
        self.color = QColor(255, 255, 255)
        self.circle_count = 5
        self.circle_interval = 0.045
        self.circle_delay = 0.05
        self.pos = QPointF(50, 50)
        self.radius = 30
        self.dot_size = 6

        self.primaryT = 0
        self.secondaryT = 0
        self.primaryCycleTime: int = 1500
        self.secondaryCycleTime: int = 10000

        self._anim = None

    def setGeometry(self, left, top, radius, size):
        self.pos = QPointF(left, top)
        self.radius = radius
        self.dot_size = size

    def draw(self, painter: QPainter):
        def easing(t):
            if t < 0.5:
                return 8 * t ** 4
            else:
                return 1 - ((-2 * t + 2) ** 4) / 2

        painter.setOpacity(self.opacity)
        painter.setPen(self.color)  # 공 윤곽선
        painter.setBrush(self.color)  # 공 채우기

        for i in range(self.circle_count):
            x1 = self.primaryT + self.circle_delay * i
            if x1 > 1.0:
                x1 -= 1.0
            num = (easing(x1) + 0.25 + self.circle_interval * i + self.secondaryT) * 2 * math.pi
            x = self.radius * math.cos(num)
            y = self.radius * math.sin(num)

            newPos = QPointF(x, y) + self.pos

            # Draw
            painter.drawEllipse(newPos, self.dot_size, self.dot_size)

    def getCycleAnimation(self):
        if self._anim is not None:
            return self._anim
        newTime = math.lcm(self.primaryCycleTime, self.secondaryCycleTime)
        ratio1 = newTime / self.primaryCycleTime
        ratio2 = newTime / self.secondaryCycleTime

        def method(start, end, t):
            self.primaryT = math.fmod(t * ratio1, 1)
            self.secondaryT = math.fmod(t * ratio2, 1)

        noEasing = lambda t: t

        newAnim = Animation(0, 0, method, newTime, noEasing, True)
        self._anim = newAnim

        return newAnim

    def destroy(self):
        if self._anim is not None:
            self._anim.finishAnim()
        super().destroy()
