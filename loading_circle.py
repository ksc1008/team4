import math

from PyQt6.QtCore import Qt, QDateTime, pyqtSlot
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow

from shortcut import ShorCut


class Loading_Circle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowTransparentForInput
        )

        self.setGeometry(50, 50, 250, 250)

        # 멤버 변수
        self.t = 0.0
        self.sp = 0.0
        self.pos = [50, 50]
        self.radius = 30
        self.dot_size = 6
        self.color = QColor(180, 180, 180)
        self.circle_count = 5
        self.circle_interval = 0.045
        self.circle_delay = 0.05
        self.cycle_time = 1.5
        self.slow_progress_speed = 0.1

        # 시작 시간
        self.timerStart = QDateTime.currentMSecsSinceEpoch()  # 1970-01-01T00:00:00 이후 경과 시간

        # Shortcut
        self.shortcut = ShorCut()
        self.shortcut.start()
        self.shortcut.exit_key.connect(self.shortcut_exit_key)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        painter.setPen(self.color)  # 공 윤곽선
        painter.setBrush(self.color)  # 공 채우기

        elapsed = QDateTime.currentMSecsSinceEpoch() - self.timerStart
        self.sp = elapsed / 1000 * self.slow_progress_speed
        self.t = (elapsed % (self.cycle_time * 1000)) / (self.cycle_time * 1000)

        self.sp *= 2 * math.pi
        for i in range(self.circle_count):
            x1 = self.t + self.circle_delay * i
            if x1 > 1.0:
                x1 -= 1.0
            num = (self.easing(x1) + 0.25 + self.circle_interval * i) * 2 * math.pi
            x = self.radius * math.cos(num + self.sp) + self.radius - self.dot_size / 2
            y = self.radius * math.sin(num + self.sp) + self.radius - self.dot_size / 2

            # Draw
            painter.drawEllipse(int(x) + self.pos[0], int(y) + self.pos[1], self.dot_size, self.dot_size)

            self.update()

    def easing(self, x):
        if x < 0.5:
            return 8 * x ** 4
        else:
            return 1 - ((-2 * x + 2) ** 4) / 2

    @pyqtSlot()
    def shortcut_exit_key(self):
        self.close()
        self.shortcut.stop()
        self.shortcut.terminate()
