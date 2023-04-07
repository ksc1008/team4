from PyQt6.QtGui import QPainter


class OverlayObject:
    """
    MainWindow 에 등록 되어 paint될 오브젝트를 규정하는 추상 클래스
    """

    def __init__(self):
        self.window = None

    def draw(self, painter: QPainter):
        pass

    def destroy(self):
        if self.window is not None:
            self.window.objects.remove(self)
        print('destroyed an object')
