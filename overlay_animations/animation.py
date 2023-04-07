import time

from PyQt6.QtCore import QRect, QRectF


class Animation:

    def __init__(self, start, end, method, duration_ms, easing, isLoop=False, after=None):
        """
        대상을 특정 시간 동안 애니메이트 한다.

        :param start: 시작 값
        :param end: 끝 값
        :param method: (start, end, t) 를 인자로 갖는 update 콜백 메소드
        :param duration_ms: 지속 시간, 단위는 밀리초
        :param easing: easing 메소드
        :param isLoop: animation이 반복할 지 여부
        :param after: 애니메이션이 종료된 직후 호출할 콜백 메소드
        """

        self.animator = None
        self.isLoop = isLoop
        self.start = start
        self.end = end

        # 매 프레임 animator 에서 실행할 메소드.
        # 시작 값, 끝 값, 그리고 (0..1) 범위의 t 값을 인자로 받으면 원하는 방식으로 현재 값을 보간하고,
        # 대상 멤버에 대입하는 내용이 들어간다.
        self.method = method

        # Easing Method. https://easings.net/ 참고
        self.easing = easing

        # 애니메이션이 종료된 후 호출할 콜백 메소드. 애니메이션이 종료된 직후 한 번 호출된다.
        self.after = after

        self.duration = duration_ms
        self.elapsed = 0
        self.startTime = time.time_ns()

    def finishAnim(self):
        if self.after is not None:
            self.after()

        if self.animator is not None:
            self.animator.animations.remove(self)
        print('removed animation')

    def update(self):
        self.elapsed = (time.time_ns() - self.startTime) / 1000000
        t = self.easing(self.elapsed / self.duration)
        self.method(self.start, self.end, t)
        if self.elapsed >= self.duration:
            if self.isLoop:
                self.startTime += self.duration * 1000000
            else:
                self.finishAnim()

    def startAnim(self, _animator):
        self.animator = _animator
        self.startTime = time.time_ns()


def make_rect_anim(setter, fromRect: QRect, toRect: QRect, duration_ms, easing=None) -> Animation:
    """
    QRect의 크기 및 위치를 변형하는 애니메이션을 생성하는 메소드

    :param setter: 대상 QRect를 변경하는 setter.
    """
    if easing is None:
        easing = lambda t: (1 - pow(1 - t, 5))

    method = lambda r1, r2, t: (setter(QRect(
        (1 - t) * r1.topLeft() + t * r2.topLeft(),
        (1 - t) * r1.bottomRight() + t * r2.bottomRight())
    ))

    return Animation(fromRect, toRect, method, duration_ms, easing)

def make_rect_animF(setter, fromRect: QRectF, toRect: QRectF, duration_ms, easing=None) -> Animation:
    """
    QRect의 크기 및 위치를 변형하는 애니메이션을 생성하는 메소드

    :param setter: 대상 QRect를 변경하는 setter.
    """
    if easing is None:
        easing = lambda t: (1 - pow(1 - t, 5))

    method = lambda r1, r2, t: (setter(QRectF(
        (1 - t) * r1.topLeft() + t * r2.topLeft(),
        (1 - t) * r1.bottomRight() + t * r2.bottomRight())
    ))

    return Animation(fromRect, toRect, method, duration_ms, easing)


def make_var_anim(setter, fromX, toX, duration_ms, easing=None) -> Animation:
    """
    특정 변수 값을 변경하는 애니메이션을 생성하는 메소드

    :param setter: 대상 변수를 변경하는 setter
    """
    if easing is None:
        easing = lambda t: (1 - pow(1 - t, 5))
    method = lambda x1, x2, t: (setter((1 - t) * x1 + t * x2))

    return Animation(fromX, toX, method, duration_ms, easing)


def wait(duration_ms) -> Animation:
    """
    특정 밀리초 동안 아무것도 하지 않는 애니메이션을 생성. 애니메이션 간 Delay 구현시 사용 가능.
    """

    def m(x1, x2, t):
        pass

    easing = lambda t: t
    return Animation(0, 0, m, duration_ms, easing)


def defaultEasing(t):
    return 1 - pow(1 - t, 5)
