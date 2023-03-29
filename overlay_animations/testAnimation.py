from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor

from overlay_animations import animatedObject, animation, animator


class TestAnimation(animatedObject.AnimatedObject):
    def __init__(self, _animator: animator.Animator):
        self.box = QRect(100, 100, 400, 400)
        self.boxFrom = QRect(100, 100, 400, 400)
        self.boxTo = QRect(300, 300, 700, 700)
        self.color = QColor(180, 180, 180)

        super().__init__(_animator)
        t = animation.make_rect_anim(self.moveBox, self.boxFrom, self.boxTo, 2000)
        t.after = self.destroy
        self.animations.append(t)

    def draw(self, painter: QPainter):
        painter.setPen(self.color)  # 공 윤곽선
        painter.setBrush(self.color)  # 공 채우기
        painter.setOpacity(0.9)
        painter.drawRect(self.box)

    def moveBox(self, q):
        self.box = q


