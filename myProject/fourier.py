from manim import *


class RotatingVector(VGroup):
    def __init__(
            self,
            radius=1,
            phase=0,
            cycle_rate=PI,
            circle_visible=True,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.cycle_rate = cycle_rate
        self.radius = radius
        self.phase = phase

        self.circle = Circle(radius=radius, stroke_width=1, color=WHITE).set_stroke(opacity=0.2)
        if not circle_visible:
            self.circle.set_opacity(0)

        self.arrow = Arrow(
            start=self.circle.get_center(),
            end=rotate_vector(RIGHT, phase) * radius + self.circle.get_center(),
            buff=0,
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )

        def rotate_about_start(m, dt):
            m.rotate(
                cycle_rate * dt,
                about_point=m.get_start()
            )

        self.arrow.add_updater(rotate_about_start)

        self.add(self.circle, self.arrow)


class FourierSeries(Scene):
    def construct(self):
        """
        v4 = RotatingVector(radius=2 / (PI * -3), phase=-PI / 2, cycle_rate=-3)
        v2 = RotatingVector(radius=2 / (PI * -1), phase=-PI / 2, cycle_rate=-1)
        v1 = RotatingVector(radius=2 / (PI * 1), phase=-PI / 2, cycle_rate=1)
        v3 = RotatingVector(radius=2 / (PI * 3), phase=-PI / 2, cycle_rate=3)

        v2.add_updater(lambda m: m.move_to(v1.arrow.get_end()))
        v3.add_updater(lambda m: m.move_to(v2.arrow.get_end()))
        v4.add_updater(lambda m: m.move_to(v3.arrow.get_end()))
        """

        arrows = [RotatingVector(radius=(2/(PI*n)), phase=0, cycle_rate=n * j)
                  for n in range(1, 6, 2) for j in (1, -1)]
        # arrows.append(RotatingVector(radius=1, phase=0, cycle_rate=0))

        for i in range(1, len(arrows)):
            arrows[i].add_updater(lambda m, i=i: m.move_to(arrows[i-1].arrow.get_end()))
        [arrow.scale(2) for arrow in arrows]

        self.add(*arrows)

        self.wait(10)
