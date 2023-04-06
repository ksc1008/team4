from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import QRect
from PyQt6 import QtSvg
from overlay_animations import animation
from overlay_objects.overlayObject import OverlayObject


class OverlayPixmap(OverlayObject):
    def __init__(self, image_path: str):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.image_path = image_path
        self.pixmap = QPixmap(self.image_path)
        self.rect = QRect(0, 0, 0, 0)
        self.opacity = 1
        self.expand = 1.2

        self.pop_t: int = 300
        self.exp_t: int = 100
        self.delay: int = 50

    def draw(self, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing,True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform,True)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(self.rect, self.pixmap)

    def setRect(self, target_rect: QRect):
        self.rect = target_rect

    def setImageToPixmap(self, path: str):
        self.image_path = path
        self.pixmap = QPixmap(self.image_path)

    def setGeometry(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def micPopIn(self, left, top, width, height):

        leftS = left
        topS = top
        width = width / 2
        height = height / 2
        self.setGeometry(left, top, width, height)

        leftT = leftS - width / 2
        topT = topS - height / 2

        widthE = width * self.expand
        heightE = height * self.expand

        easeInOutQuint = lambda x: (16 * x * x * x * x * x) if x < 0.5 else (1 - pow(-2 * x + 2, 5) / 2)
        anim = animation.make_rect_anim(self.setRect, QRect(int(leftS), int(topS), 0, 0),
                                        QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE),
                                              int(heightE)),
                                        self.pop_t + self.delay, easeInOutQuint)

        easeOutQuint = lambda x: 1 - pow(1 - x, 5)
        anim2 = animation.make_rect_anim(self.setRect,
                                         QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE),
                                               int(heightE)),
                                         QRect(int(leftT), int(topT), int(width), int(height)),
                                         self.exp_t, easeOutQuint)

        return anim, anim2

    def micPopOut(self):
        leftS = self.left
        topS = self.top
        width = self.width
        height = self.height

        leftT = leftS - width / 2
        topT = topS - height / 2

        widthE = width * self.expand
        heightE = height * self.expand

        easeInQuint = lambda x: x * x * x * x
        anim = animation.make_rect_anim(self.setRect,
                                        QRect(int(leftT), int(topT), int(width), int(height)),
                                        QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE), int(heightE)),
                                        self.exp_t, easeInQuint)

        easeInOutQuint = lambda x: (16 * x * x * x * x * x) if x < 0.5 else (1 - pow(-2 * x + 2, 5) / 2)
        anim2 = animation.make_rect_anim(self.setRect,
                                         QRect(int(leftS - widthE / 2), int(topS - heightE / 2), int(widthE),
                                               int(heightE)),
                                         QRect(int(leftS), int(topS), 0, 0),
                                         self.pop_t, easeInOutQuint)

        anim2.after = lambda : self.destroy()

        return anim, anim2