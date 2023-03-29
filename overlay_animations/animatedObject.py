from PyQt6.QtGui import QPainter

from overlay_animations import animator


class AnimatedObject:
    def __init__(self, _animator: animator.Animator):
        self.animations = []
        self.animator = _animator

    def startAnim(self):
        for a in self.animations:
            self.animator.startAnim(a)

    def draw(self, painter: QPainter):
        pass

    def destroy(self):
        print('destroyed animated object')
        self.animator.removeAnimatedObject(self)

