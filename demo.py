import sys
from PyQt6.QtCore import QRect
from overlay_animations import animation
from overlay_objects import overlayRect
from overlay_animations import animator
from overlay_objects.overlayObject import OverlayObject


def createTestObjectAndApplyAnimation(_animator: animator.Animator) -> OverlayObject:
    """
    윈도우에 draw 되는 오브젝트를 하나 만들고, 해당 오브젝트에 적용되는 여러 animation을 생성 후, animator에 추가하는 메소드

    :param _animator: main window의 animator
    :return: 애니메이션이 적용된 OverlayObject
    """

    # Window에 draw되는 사각형 오브젝트.
    obj = overlayRect.OverlayRect()

    # --------------------------------------------------
    #                  First Animation
    # --------------------------------------------------

    # custom Easing 함수 지정시 필요. https://easings.net/ 참고
    easeInOutQuint = lambda x: (16 * x * x * x * x * x) if x < 0.5 else (1 - pow(-2 * x + 2, 5) / 2)

    # obj의 멤버 변수를 변형시킬 첫번째 애니메이션
    # 사전에 정의된 make_rect_anim 을 이용해 Animation 객체 생성
    anim = animation.make_rect_anim(obj.setRect, QRect(100, 100, 200, 200), QRect(500, 500, 500, 500), 2000,
                                    easeInOutQuint)

    # --------------------------------------------------
    #             Second, Third Animation
    # --------------------------------------------------

    # 첫번째 애니메이션이 끝난 직후 실행될 두번째 애니메이션. 첫번째와 달리 Animation 생성자를 직접 호출하여 객체를 생성할 예정
    # Animation 객체 직접 생성시 update callback method 지정 필요
    updateCallback = lambda q1, q2, t: obj.setRect(QRect(
        (1 - t) * q1.topLeft() + t * q2.topLeft(),
        (1 - t) * q1.bottomRight() + t * q2.bottomRight()))

    # 두번째 Animation 객체 생성
    anim2 = animation.Animation(QRect(500, 500, 500, 500), QRect(200, 200, 0, 0), updateCallback, 1000, easeInOutQuint)

    # 두번째 애니메이션과 동시에 페이드 아웃 효과를 부여할 애니메이션. obj 객체의 멤버 변수 opacity를 변경하는 애니메이션
    # 세번째 Animation 객체는 사전에 정의된 make_var_anim 을 이용해 생성.
    anim3 = animation.make_var_anim(obj.setOpacity, 0.9, 0, 2000)

    # anim 종료 후, animator에 anim2와 anim3를 추가(실행) 하고,
    anim.after = lambda: [_animator.addAnim(anim2), _animator.addAnim(anim3)]
    # anim3 종료 후, obj를 파괴하시오
    anim3.after = lambda: obj.destroy()

    # anim을 애니메이터에 추가
    _animator.addAnim(anim)
    return obj
