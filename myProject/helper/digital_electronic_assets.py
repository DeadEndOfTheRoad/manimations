from manim import *
from collections import Counter


class Clock(VGroup):
    def __init__(self, radius=1, cycle_rate=PI, is_running=True, **kwargs):
        self.radius = radius
        self.cycle_rate = ValueTracker(cycle_rate)

        self.is_running = is_running
        self.origin = Dot()
        self.circle_left = Arc(
            radius=radius,
            start_angle=PI / 2,
            angle=PI,
            color=WHITE
        )

        self.circle_right = Arc(
            radius=radius,
            start_angle=-PI / 2,
            angle=PI,
            color=YELLOW
        )

        self.tick_top = Line(
            UP * radius,
            UP * radius + DOWN * 0.2 * radius,
            color=YELLOW,
            stroke_width=6
        )

        self.tick_bottom = Line(
            DOWN * radius,
            DOWN * radius + UP * 0.2 * radius,
            color=WHITE,
            stroke_width=6
        )

        self.hand = Arrow(
            start=self.origin.get_center(),
            end=DOWN * radius,
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )

        self.angle_tracker = ValueTracker(0)

        self.hand.add_updater(lambda m, dt: self.step_hand(dt))

        super().__init__(self.origin, self.circle_left, self.circle_right,
                         self.tick_top, self.tick_bottom, self.hand, **kwargs)

    def step_hand(self, dt):
        if not self.is_running:
            return
        self.angle_tracker.increment_value(dt * self.cycle_rate.get_value())
        self.hand.put_start_and_end_on(self.origin.get_center(),
                                       self.origin.get_center() +
                                       rotate_vector(UP, self.angle_tracker.get_value()) * self.radius)

    def set_angle_value(self, value):
        self.angle_tracker.set_value(value)

    def set_cycle_rate(self, value):
        self.cycle_rate.set_value(value)


class DFlipFlop(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.box = Square(side_length=1.6, color=BLUE)

        # Dynamic Input Indicator
        self.edge_trigger_indicator = Triangle(color=BLUE).scale(0.1).rotate(-90 * DEGREES)
        self.edge_trigger_indicator.shift(
            self.box.get_edge_center(LEFT) - self.edge_trigger_indicator.get_edge_center(LEFT) + DOWN * 0.625
        )

        label_color = BLUE_C

        self.label_d = MathTex("D", font_size=28, color=label_color).next_to(
            self.box.get_corner(UL), [0.35, -0.35, 0]
        )
        self.label_q = MathTex("Q", font_size=28, color=label_color).next_to(
            self.box.get_corner(UR), [-0.35, -0.35, 0]
        )
        self.label_qbar = MathTex(r"\bar{Q}", font_size=28, color=label_color).next_to(
            self.box.get_corner(DR), [-0.35, 0.35, 0]
        )

        self.state_text = DecimalNumber(0, num_decimal_places=0, font_size=36, color=label_color)

        self.add(
            self.box,
            self.edge_trigger_indicator,
            self.label_q,
            self.label_qbar,
            self.label_d,
            self.state_text
        )

    def set_state(self, value):
        self.state_text.set_value(value)

    def get_state(self):
        return self.state_text.get_value()

    def toggle_value(self):
        self.set_state(1 - self.state_text.get_value())

    def get_input(self):
        return self.get_corner(UL) + DOWN * 0.175

    def get_output(self):
        return self.get_corner(UR) + DOWN * 0.175

    def get_negated_output(self):
        return self.get_corner(DR) + UP * 0.175

    def get_edge_trigger_indicator(self):
        return self.get_corner(DL) + UP * 0.175


class ANDGate(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        self.scale_factor = scale_factor
        points = [[-0.5, 1, 0], [-0.5, -1, 0], [0.5, -1, 0], [0.5, 1, 0]]
        points = [[value * self.scale_factor * 0.5 for value in point] for point in points]
        self.base = ArcPolygon(*points, arc_config=[
            {'angle': 0},
            {'angle': 0},
            {'angle': PI},
            {'angle': 0}
        ], **kwargs)
        super().__init__(self.base, **kwargs)

        self.input_a_anchor = Dot(self.get_edge_center(LEFT) + UP * 0.25 * self.scale_factor).set_opacity(0)
        self.input_b_anchor = Dot(self.get_edge_center(LEFT) + DOWN * 0.25 * self.scale_factor).set_opacity(0)
        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.input_a_anchor, self.input_b_anchor, self.output_anchor)

    def get_output(self):
        return self.output_anchor.get_center()

    def get_input_a(self):
        return self.input_a_anchor.get_center()

    def get_input_b(self):
        return self.input_b_anchor.get_center()


class ORGate(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        self.scale_factor = scale_factor
        points = [[-0.5, 1, 0], [-0.5, -1, 0], [1.5, 0, 0]]
        points = [[value * self.scale_factor * 0.5 for value in point] for point in points]
        self.base = ArcPolygon(*points, arc_config=[
            {'angle': -PI / 2},
            {'angle': PI / 4},
            {'angle': PI / 4}
        ], **kwargs)
        super().__init__(self.base, **kwargs)

        self.input_a_anchor = Dot(self.get_edge_center(LEFT) + (
                UP * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.input_b_anchor = Dot(self.get_edge_center(LEFT) + (
                DOWN * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.input_a_anchor, self.input_b_anchor, self.output_anchor)

    def get_output(self):
        return self.output_anchor.get_center()

    def get_input_a(self):
        return self.input_a_anchor.get_center()

    def get_input_b(self):
        return self.input_b_anchor.get_center()


class NORGate(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        self.scale_factor = scale_factor
        self.radius = 0.08
        points = [[-0.5, 1, 0], [-0.5, -1, 0], [1.5, 0, 0]]
        points = [[value * self.scale_factor * 0.5 for value in point] for point in points]
        self.base = ArcPolygon(*points, arc_config=[
            {'angle': -PI / 2},
            {'angle': PI / 4},
            {'angle': PI / 4}
        ])
        self.add(self.base)

        self.input_a_anchor = Dot(self.get_edge_center(LEFT) + (
                UP * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.input_b_anchor = Dot(self.get_edge_center(LEFT) + (
                DOWN * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.output_anchor = Dot(self.get_edge_center(RIGHT))
        self.add(self.input_a_anchor, self.input_b_anchor)

        self.bubble = Circle(radius=self.radius * self.scale_factor, color=WHITE).move_to(
            self.get_output() + RIGHT * self.radius * self.scale_factor)
        self.add(self.bubble)

        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.output_anchor)

    def get_output(self):
        return self.output_anchor.get_center()

    def get_input_a(self):
        return self.input_a_anchor.get_center()

    def get_input_b(self):
        return self.input_b_anchor.get_center()


class NANDGate(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        self.scale_factor = scale_factor
        self.radius = 0.08
        points = [[-0.5, 1, 0], [-0.5, -1, 0], [0.5, -1, 0], [0.5, 1, 0]]
        points = [[value * self.scale_factor * 0.5 for value in point] for point in points]
        self.base = ArcPolygon(*points, arc_config=[
            {'angle': 0},
            {'angle': 0},
            {'angle': PI},
            {'angle': 0}
        ])
        self.add(self.base)

        self.input_a_anchor = Dot(self.get_edge_center(LEFT) + UP * 0.25 * self.scale_factor).set_opacity(0)
        self.input_b_anchor = Dot(self.get_edge_center(LEFT) + DOWN * 0.25 * self.scale_factor).set_opacity(0)
        self.output_anchor = Dot(self.get_edge_center(RIGHT))
        self.add(self.input_a_anchor, self.input_b_anchor)

        self.bubble = Circle(radius=self.radius * self.scale_factor, color=WHITE).move_to(
            self.get_output() + RIGHT * self.radius * self.scale_factor)
        self.add(self.bubble)

        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.output_anchor)

    def get_output(self):
        return self.output_anchor.get_center()

    def get_input_a(self):
        return self.input_a_anchor.get_center()

    def get_input_b(self):
        return self.input_b_anchor.get_center()


class XORGate(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        self.scale_factor = scale_factor
        self.radius = 0.08
        points = [[-0.5, 1, 0], [-0.5, -1, 0], [1.5, 0, 0]]
        points = [[value * self.scale_factor * 0.5 for value in point] for point in points]
        self.base = ArcPolygon(*points, arc_config=[
            {'angle': -PI / 2},
            {'angle': PI / 4},
            {'angle': PI / 4}
        ])

        self.curved_line = ArcBetweenPoints(points[0] + LEFT * 0.3 * self.scale_factor * 0.5,
                                            points[1] + LEFT * 0.3 * self.scale_factor * 0.5,
                                            angle=-PI / 2)

        super().__init__(self.base, self.curved_line, **kwargs)

        self.input_a_anchor = Dot(self.get_edge_center(LEFT) + (
                UP * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.input_b_anchor = Dot(self.get_edge_center(LEFT) + (
                DOWN * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.input_a_anchor, self.input_b_anchor, self.output_anchor)

    def get_output(self):
        return self.output_anchor.get_center()

    def get_input_a(self):
        return self.input_a_anchor.get_center()

    def get_input_b(self):
        return self.input_b_anchor.get_center()


class XNORGate(VGroup):
    def __init__(self, scale_factor=1, **kwargs):
        super().__init__(**kwargs)
        self.scale_factor = scale_factor
        self.radius = 0.08
        points = [[-0.5, 1, 0], [-0.5, -1, 0], [1.5, 0, 0]]
        points = [[value * self.scale_factor * 0.5 for value in point] for point in points]
        self.base = ArcPolygon(*points, arc_config=[
            {'angle': -PI / 2},
            {'angle': PI / 4},
            {'angle': PI / 4}
        ])
        self.curved_line = ArcBetweenPoints(points[0] + LEFT * 0.3 * self.scale_factor * 0.5,
                                            points[1] + LEFT * 0.3 * self.scale_factor * 0.5,
                                            angle=-PI / 2)
        self.add(self.base, self.curved_line)

        self.input_a_anchor = Dot(self.get_edge_center(LEFT) + (
                UP * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.input_b_anchor = Dot(self.get_edge_center(LEFT) + (
                DOWN * 0.5 + RIGHT * (np.sqrt(2) - np.sqrt(5) / 2)) * self.scale_factor * 0.5).set_opacity(0)
        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.input_a_anchor, self.input_b_anchor)

        self.bubble = Circle(radius=self.radius * self.scale_factor, color=WHITE).move_to(
            self.get_output() + RIGHT * self.radius * self.scale_factor)
        self.add(self.bubble)

        self.output_anchor = Dot(self.get_edge_center(RIGHT)).set_opacity(0)
        self.add(self.output_anchor)

    def get_output(self):
        return self.output_anchor.get_center()

    def get_input_a(self):
        return self.input_a_anchor.get_center()

    def get_input_b(self):
        return self.input_b_anchor.get_center()


class Wire(VGroup):
    def __init__(self, points, edges, **kwargs):
        junctions = []
        for i, p in enumerate(points):
            if len(p) == 2 and p[1]:
                junctions.append(Dot().move_to(p[0]))
                points[i] = p[0]
        wires = []
        for i, j, *interpolation in edges:
            if interpolation:
                axis_to_interpolate = interpolation[1]
                axis_dir = UP if axis_to_interpolate else RIGHT
                offset = (points[j][axis_to_interpolate] - points[i][axis_to_interpolate])
                point_a = points[i] + offset * interpolation[0] * axis_dir
                point_b = points[j] - offset * (1 - interpolation[0]) * axis_dir
                wires.extend([
                    Line(points[i], point_a),
                    Line(point_a, point_b),
                    Line(point_b, points[j])
                ])
            else:
                wires.append(Line(points[i], points[j]))

        self.wires = wires
        self.junctions = junctions

        super().__init__(*self.wires, *self.junctions, **kwargs)


