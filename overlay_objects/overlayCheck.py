import math

import PyQt6.QtCore
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QColor, QPen

from overlay_animations import animation
from overlay_objects.overlayObject import OverlayObject
from overlay_animations.animation import Animation


class OverlayCheck(OverlayObject):

    def __init__(self):
        super().__init__()
        self.opacity = 1
        self.color = QColor(0, 255, 0)
        self.pos = QPointF(50, 50)
        self.size = 1.5

        self.path1from = QPointF(0, 20)
        self.path1to = QPointF(20, 40)
        self.path1final = QPointF(20, 40)
        self.path2from = QPointF(20, 40)
        self.path2to = QPointF(50, 0)
        self.path2final = QPointF(50, 0)
        self.penWidth = 12

        self.drawPath2 = False

        self._anim = None

    def draw(self, painter: QPainter):
        painter.setOpacity(1)
        painter.setPen(QPen(self.color, self.penWidth * self.size, cap=PyQt6.QtCore.Qt.PenCapStyle.RoundCap))
        painter.drawLine(self.pos + self.path1from * self.size,
                         self.pos + self.path1to * self.size)
        if self.drawPath2:
            painter.drawLine(self.pos + self.path2from * self.size,
                             self.pos + self.path2to * self.size)

    def setPath(self, t, mid):
        if t >= mid:
            self.path1to = self.path1final
            self.path2to = (self.path2from * (1 - t) + self.path2final * (t - mid)) / (1 - mid)
            self.drawPath2 = True
        else:
            self.path1to = (self.path1from * (mid - t) + self.path1final * t) / mid
            self.drawPath2 = False

    def removeAnim(self):
        self._anim = None

    def getAnimation(self):
        path1 = self.path1from - self.path1to
        path1len = math.sqrt(pow(path1.x(), 2) + pow(path1.y(), 2))

        path2 = self.path2from - self.path2to
        path2len = math.sqrt(pow(path2.x(), 2) + pow(path2.y(), 2))

        ratio = path1len / (path1len + path2len)
        setter = lambda x: self.setPath(x, ratio)

        def easeinoutquart(x):
            if x < 0.5:
                return 8 * x * x * x * x
            else:
                return 1 - pow(-2 * x + 2, 4) / 2

        anim = animation.make_var_anim(setter, 0, 1, 300, easeinoutquart)
        anim.after = self.removeAnim
        self._anim = anim

        return anim

    def destroy(self):
        if self._anim is not None:
            self._anim.finishAnim()
        super().destroy()
