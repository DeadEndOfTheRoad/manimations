from manim import *
import numpy as np


class Clock:
    def __init__(self, scale=1, speed=PI / 3):
        circle = Circle(radius=2, color=WHITE)

        circle_left = Arc(
            radius=2,
            start_angle=PI / 2,
            angle=PI,
            color=WHITE
        )

        circle_right = Arc(
            radius=2,
            start_angle=-PI / 2,
            angle=PI,
            color=YELLOW
        )

        tick_top = Line(
            circle.point_at_angle(PI / 2),
            circle.point_at_angle(PI / 2) + DOWN * 0.4,
            color=YELLOW,
            stroke_width=6
        )

        tick_bottom = Line(
            circle.point_at_angle(3 * PI / 2),
            circle.point_at_angle(3 * PI / 2) + UP * 0.4,
            color=WHITE,
            stroke_width=6
        )

        hand = Arrow(
            start=ORIGIN,
            end=UP * 1.5,
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        angle_tracker = ValueTracker(0)
        hand.add_updater(
            lambda m, dt: (angle_tracker.increment_value(dt * speed),
                           m.put_start_and_end_on(circle.get_center(),
                                                  rotate_vector(UP, angle_tracker.get_value()) * circle.radius * scale +
                                                  circle.get_center())
                           )
        )

        self.clock = VGroup(circle, circle_left, circle_right, tick_top, tick_bottom, hand).scale(scale)
        self.clock.move_to(ORIGIN)


class Module:
    def __init__(self, value=0, scale=1, colour=BLACK):
        box = Square()
        value = DecimalNumber(value, 0).shift(DOWN / 2)
        # Dynamic Input Indicator (posedge)
        dii = Triangle().rotate(270 * DEGREES).scale(0.2).align_to(box, LEFT).shift(DOWN / 2)
        d = MathTex('D', font_size=40).shift([-0.7, 0.4, 0])
        q = MathTex('Q', font_size=40).shift([0.7, 0.4, 0])
        q_bar = MathTex(r'\bar{Q}', font_size=40).shift([0.7, -0.4, 0])
        self.module = VGroup(box, value, dii, d, q, q_bar).scale(scale).set_color(colour)
        for i in [d, q, q_bar]:
            i.set_color(BLUE_D)


class JohnsonCounter(Scene):
    def construct(self):
        FlipFlops = VGroup(*[Module(0, 0.8, BLUE).module for _ in range(3)])
        FlipFlops.arrange(buff=1)

        clk_text = Tex(r"CLK")
        clk_text.align_to(FlipFlops[0], DL).shift([-2, -1, 0])

        cws = clk_text.get_edge_center(RIGHT)  # clock wire start

        clk_wire_corners = {
            "A": cws,
            "B": cws + [0.5, 0, 0],
            "C": cws + [0.5, 1.42, 0],
            "D": cws + [0.9, 1.42, 0],
            "E": cws + [3.1, 0, 0],
            "F": cws + [3.1, 1.42, 0],
            "G": cws + [3.5, 1.42, 0],
            "H": cws + [5.7, 0, 0],
            "I": cws + [5.7, 1.42, 0],
            "J": cws + [6.1, 1.42, 0]
        }

        clk_wire_edges = [
            ("A", "B"), ("B", "C"), ("C", "D"), ("B", "E"), ("E", "F"), ("F", "G"), ("E", "H"), ("H", "I"), ("I", "J")
        ]

        clk_wires = VGroup(*[
            Line(clk_wire_corners[a], clk_wire_corners[b])
            if i not in [2, 5, 8] else
            VGroup(
                Line(clk_wire_corners[a], clk_wire_corners[b]),
                Circle(radius=0.05, color=WHITE).move_to(clk_wire_corners[b] + [0.05, 0, 0])
            )
            for i, (a, b) in enumerate(clk_wire_edges)
        ])

        flip_flop_wires = [
            Line(FlipFlops[0], FlipFlops[1]),
            Line(FlipFlops[1], FlipFlops[2]),
            VGroup(
                Line(FlipFlops[2].get_corner(UR) + [0, -0.6, 0], FlipFlops[2][0].get_corner(UR) + [1, -0.6, 0]),
                Line(FlipFlops[2][0].get_corner(UR) + [1, -0.6, 0], FlipFlops[2][0].get_corner(UR) + [1, 1, 0]),
                Line(FlipFlops[2][0].get_corner(UR) + [1, 1, 0], FlipFlops[0][0].get_corner(UL) + [-1, 1, 0]),
                Line(FlipFlops[0][0].get_corner(UL) + [-1, 1, 0], FlipFlops[0][0].get_corner(UL) + [-1, 0, 0]),
                Line(FlipFlops[0][0].get_corner(UL) + [-1, 0, 0], FlipFlops[0][0].get_corner(UL))
            ).set_color(YELLOW)

        ]
        [line.shift(DOWN / 2) for line in flip_flop_wires]

        clock = Clock(scale=0.3, speed=PI / 2).clock.next_to(clk_text.get_center(), LEFT, buff=1)
        clock_hand = clock[-1]

        axes = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 1.2, 1],
            x_length=12,
            y_length=3,
            axis_config={"include_numbers": True},
            tips=False,
        )


        objs = []
        objs += FlipFlops
        objs += flip_flop_wires
        objs.append(clk_wires)
        objs.append(clock)
        objs.append(clk_text)
        objs.append(axes)

        [obj.shift(UR) for obj in objs]

        self.play(
            LaggedStart(*[AnimationGroup(FadeIn(obj), obj.animate.shift(DOWN))
                          for obj in objs],
                        lag_ratio=0.2, run_time=PI, rate_func=rush_into))

        counter = ValueTracker(0)
        prev_half = {"right": True}

        def clk_updater(m):
            right_now = np.cos(clock_hand.get_angle()) > 0

            m.set_color(YELLOW if right_now else WHITE)

            # detect transition
            if prev_half["right"] and not right_now:
                counter.set_value((counter.get_value() + 1) % 6)

            prev_half["right"] = right_now

        clk_wires.add_updater(clk_updater)

        flip_flop_values = [[0, 0, 0],
                            [1, 0, 0],
                            [1, 1, 0],
                            [1, 1, 1],
                            [0, 1, 1],
                            [0, 0, 1]]

        flip_flop_wire_values = [[0, 0, 1],
                                 [1, 0, 1],
                                 [1, 1, 1],
                                 [1, 1, 0],
                                 [0, 1, 0],
                                 [0, 0, 0]]

        for i, (wire, flip_flop) in enumerate(zip(flip_flop_wires, FlipFlops)):
            print(int(counter.get_value()), i)
            wire.add_updater(
                lambda m, i=i: m.set_color(YELLOW if flip_flop_wire_values[int(counter.get_value())][i] else WHITE))
            ff_value = flip_flop[1].get_value()
            flip_flop[1].add_updater(lambda m, i=i: m.set_value(flip_flop_values[int(counter.get_value())][i]))

        self.wait(30)

