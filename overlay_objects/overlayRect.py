from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QColor

from overlay_objects.overlayObject import OverlayObject


class OverlayRect(OverlayObject):
    """
    MainWindow 에 paint될 간단한 QRect 오브젝트
    """

    def __init__(self):
        super().__init__()
        self.rect = QRect(0, 0, 0, 0)
        self.opacity = 0.9
        self.color = QColor(180, 60, 60)

    def draw(self, painter: QPainter):
        painter.setPen(self.color)  # 공 윤곽선
        painter.setBrush(self.color)  # 공 채우기
        painter.setOpacity(self.opacity)
        painter.drawRect(self.rect)

    def setRect(self, rect: QRect):
        self.rect = rect

    def setOpacity(self, opacity):
        self.opacity = opacity
