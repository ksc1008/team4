import time

from PyQt6.QtCore import QRect

import animator
import threading


class Animation:

    def __init__(self, source, target, method, duration_ms, easing, after=None):
        self.animator = None
        self.src = source
        self.target = target
        self.method = method
        self.duration = duration_ms
        self.elapsed = 0
        self.easing = easing
        self.after = after
        self.start = time.time_ns()

    def finishAnim(self):
        if self.after is not None:
            self.animator.startAnim(self.after)
        self.animator.removeAnim(self)
        print('removed animation')

    def invoke(self):
        self.elapsed = (time.time_ns() - self.start) / 1000000
        t = self.easing(self.elapsed / self.duration)
        self.method(self.src, self.target, t)
        if t >= 1:
            self.finishAnim()

    def startAnim(self, _animator: animator.Animator):
        self.animator = _animator
        self.start = time.time_ns()


def make_rect_anim(setter, fromRect: QRect, toRect: QRect, duration_ms, easing=None):
    if easing is None:
        easing = lambda t: (1 - pow(1 - t, 5))
    method = lambda r1, r2, t: (setter(QRect(
        (1 - t) * r1.topLeft() + t * r2.topLeft(),
        (1 - t) * r1.bottomRight() + t * r2.bottomRight())
    ))
    return Animation(fromRect, toRect, method, duration_ms, easing)


def make_var_anim(setter, fromX, toX, duration_ms, easing=None):
    if easing is None:
        easing = lambda t: (1 - pow(1 - t, 5))
    method = lambda x1, x2, t: (setter((1 - t) * x1 + t * x2))

    return Animation(fromX, toX, method, duration_ms, easing)
