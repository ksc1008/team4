import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QMovie


class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()

        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.to_xy = xy
        self.speed = 60
        self.direction = [0, 0]  # x: 0(left), 1(right), y: 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.setupUi()
        self.show()

    def setupUi(self):
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        # frame 제거, stays on top 설정
        flags = QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType. \
            WindowStaysOnTopHint if self.on_top else QtCore.Qt.WindowType.FramelessWindowHint
        self.setWindowFlags(flags)

        # 배경 투명
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget)
        movie = QMovie(self.img_path)
        label.setMovie(movie)

        # movie 크기를 측정하기 위해서는 1번 실행해야 함   movie.frameRect().size(): movie 크기
        movie.start()
        movie.stop()

        # movie 크기 조정
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))

        movie.start()

        self.setGeometry(self.xy[0], self.xy[1], w, h)
