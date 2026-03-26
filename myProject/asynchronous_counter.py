from manim import *
from helper import *
import numpy as np


class GreyCounter(MovingCameraScene):
    def construct(self):
        # Show recursive Grey Code Generation Formula for 3 bits
        self.wait(0.5)

        lines = VGroup(
            MathTex(r"G_0", "=", r"B_1", r"\oplus", r"B_0"),
            MathTex(r"G_1", "=", r"B_2", r"\oplus", r"B_1"),
            MathTex(r"G_2", "=", r"B_2", r"\oplus", r"B_3")
        )

        for line in lines:
            line.set_color(BLUE)

        for line in lines:
            for eq in line.get_parts_by_tex("="):
                eq.set_color(WHITE)

        for tex in ["G_2", "G_1", "G_0"]:
            for line in lines:
                for part in line.get_parts_by_tex(tex):
                    part.set_color(GREY)

        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        for line in lines:
            self.play(Write(line))

        zero = MathTex(r"0").set_color(BLUE)
        zero.move_to(lines[2].get_part_by_tex(r"B_3"))

        self.play(ReplacementTransform(lines[2].get_part_by_tex(r"B_3"), zero))
        self.wait(1)

        self.play(FadeOut(lines[2][-1], target_position=lines[2][-3]),
                  FadeOut(lines[2][-2], target_position=lines[2][-3]))
        lines[2].remove(lines[2][-1], lines[2][-2])

        self.wait(1)

        self.play(lines.animate.to_corner(UR).scale(0.5).shift(RIGHT))

        # Flip Flop Initialization
        DFFs = VGroup(DFlipFlop() for _ in range(3))
        DFFs.arrange(buff=2)

        # Gate Initialization
        xor_gate_1 = XORGate(scale_factor=0.6)
        xor_gate_1.move_to(DFFs[0].get_output() + RIGHT)

        xor_gate_2 = XORGate(scale_factor=0.6)
        xor_gate_2.move_to(DFFs[1].get_output() + RIGHT * 1.2)

        and_gate_1 = ANDGate(scale_factor=0.6)
        and_gate_1.move_to(DFFs[1].get_output() + UP + RIGHT * 0.6)

        # Clock Initialization
        clk_text = Tex(r"CLK")
        clk_text.move_to(DFFs[0]).shift([-2, -2, 0])

        clk = Clock(radius=0.5, cycle_rate=PI / 2).next_to(clk_text, DOWN)

        # Wire Initialization

        wires = [
            Wire(points=[  # Q_bar(0) to D(0)
                DFFs[0].get_negated_output(),
                DFFs[0].get_negated_output() + RIGHT / 3,
                DFFs[0].get_input() + LEFT / 3,
                DFFs[0].get_input()
            ], edges=[
                (0, 1),
                (1, 2, 1.5, 1),
                (2, 3)
            ]).set_color(YELLOW),
            Wire(points=[  # Q(0) to XOR(1) and AND
                DFFs[0].get_output(),
                xor_gate_1.get_input_b(),
                (DFFs[0].get_output() + RIGHT / 6, True),
                DFFs[0].get_output() + RIGHT / 6 + UP * (and_gate_1.get_input_a() - DFFs[0].get_output())[1],
                and_gate_1.get_input_a()
            ], edges=[
                (0, 1, 0.7, 0),
                (2, 3),
                (3, 4)
            ]),
            Wire(points=[  # Q(1) to XOR(1) and AND
                DFFs[1].get_output(),
                and_gate_1.get_input_b(),
                (and_gate_1.get_input_b() + LEFT * (and_gate_1.get_input_b() - DFFs[1].get_output())[0] / 2, True),
                xor_gate_1.get_input_a()
            ], edges=[
                (0, 1, 0.5, 0),
                (2, 3, 1.05, 0)
            ]),
            Wire(points=[  # AND to XOR(2)
                and_gate_1.get_output(),
                and_gate_1.get_output() + RIGHT * 0.2,
                xor_gate_2.get_input_b() + LEFT * 0.3,
                xor_gate_2.get_input_b()
            ], edges=[
                (0, 1),
                (1, 2, 0.4, 1),
                (2, 3)
            ]),
            Wire(points=[  # Q(2) to XOR(2)
                DFFs[2].get_output(),
                DFFs[2].get_output() + RIGHT * 0.2,
                xor_gate_2.get_input_a() + LEFT * 0.2,
                xor_gate_2.get_input_a()
            ], edges=[
                (0, 1),
                (1, 2, 3, 1),
                (2, 3)
            ]),
            Wire(points=[  # XOR(2) to D(2)
                xor_gate_2.get_output(),
                DFFs[2].get_input()
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # XOR(1) to D(1)
                xor_gate_1.get_output(),
                DFFs[1].get_input()
            ], edges=[
                (0, 1)
            ]),
            VGroup(Wire(points=[  # CLK to all Edge Trigger DFF Inputs
                clk_text.get_edge_center(RIGHT),
                DFFs[0].get_edge_trigger_indicator() + LEFT * 0.1,
                DFFs[1].get_edge_trigger_indicator() + LEFT * 0.1,
                DFFs[2].get_edge_trigger_indicator() + LEFT * 0.1
            ], edges=[
                (0, 1, 0.5, 0),
                (0, 2, 0.8, 0),
                (0, 3, 0.95, 0)
            ]), Circle(radius=0.05, color=WHITE).move_to(DFFs[0].get_edge_trigger_indicator() + LEFT * 0.05),
                Circle(radius=0.05, color=WHITE).move_to(DFFs[1].get_edge_trigger_indicator() + LEFT * 0.05),
                Circle(radius=0.05, color=WHITE).move_to(DFFs[2].get_edge_trigger_indicator() + LEFT * 0.05)
            )
        ]

        self.play(LaggedStart(*[FadeIn(ff, shift=DOWN, target_position=ff.get_center() + UP) for ff in DFFs],
                              lag_ratio=0.4), run_time=2)

        self.play(FadeIn(xor_gate_1, shift=DOWN, target_position=xor_gate_1.get_center() + UP),
                  FadeIn(xor_gate_2, shift=DOWN, target_position=xor_gate_2.get_center() + UP),
                  FadeIn(and_gate_1, shift=DOWN, target_position=and_gate_1.get_center() + UP))
        self.play(*[Create(wire) for wire in wires], run_time=1)

        self.play(Succession(Create(clk_text), Create(clk)), run_time=1)
        clk.set_angle_value(PI)

        # Clock negative edge detection
        edge_trigger = ValueTracker(0)
        prev_clk_level = {"HIGH": 0}
        self.add(edge_trigger)

        def detect_edge(m):
            if prev_clk_level["HIGH"] and np.sin(clk.angle_tracker.get_value()) > 0:
                m.set_value(1)
            else:
                m.set_value(0)
            prev_clk_level["HIGH"] = int(np.sin(clk.angle_tracker.get_value()) <= 0)

        edge_trigger.add_updater(detect_edge)

        """
        0-Q_bar(0) to D(0)
        1-Q(0) to XOR(1) and AND
        2-Q(1) to XOR(1) and AND
        3-AND to XOR(2)
        4-Q(2) to XOR(2)
        5-XOR(2) to D(2)
        6-XOR(1) to D(1)
        7-CLK to all Edge Trigger DFF Inputs
        """

        # Wire updaters
        wire_states = [0] * 8
        wire_delay = [0] * 8
        wire_changing = [False] * 8
        wire_prop_delay = [0] * 8
        wire_prop_delay = [delay * 2 for delay in wire_prop_delay]
        wire_next_color = [WHITE] * 8

        def wire_updater(m, dt, i):
            if i == 0 and 1 - DFFs[0].get_state() or \
                    i == 1 and DFFs[0].get_state() or \
                    i == 2 and DFFs[1].get_state() or \
                    i == 3 and wire_states[1] and wire_states[2] or \
                    i == 4 and DFFs[2].get_state() or \
                    i == 5 and (DFFs[2].get_state() ^ wire_states[3]) or \
                    i == 6 and DFFs[0].get_state() ^ DFFs[1].get_state() or \
                    i == 7 and np.sin(clk.angle_tracker.get_value()) <= 0:
                if not wire_states[i] and not wire_changing[i]:
                    wire_changing[i] = True
                    wire_next_color[i] = YELLOW
            else:
                if wire_states[i] and not wire_changing[i]:
                    wire_changing[i] = True
                    wire_next_color[i] = WHITE

            if wire_changing[i]:
                wire_delay[i] += dt
                if wire_delay[i] > wire_prop_delay[i]:
                    wire_delay[i] = 0
                    wire_changing[i] = False
                    m.set_color(wire_next_color[i])
                    wire_states[i] = 1 if wire_next_color[i] == YELLOW else 0

        for i in range(len(wires)):
            wires[i].add_updater(lambda m, dt, i=i: wire_updater(m, dt, i))

        # Flip Flop updaters
        DFFs[0].add_updater(lambda m: m.set_state(wire_states[0]) if edge_trigger.get_value() else None)
        DFFs[1].add_updater(lambda m: m.set_state(wire_states[6]) if edge_trigger.get_value() else None)
        DFFs[2].add_updater(lambda m: m.set_state(wire_states[5]) if edge_trigger.get_value() else None)

        # Gate updaters
        xor_gate_1.add_updater(lambda m: m.set_color(YELLOW if wire_states[6] else WHITE))
        xor_gate_2.add_updater(lambda m: m.set_color(YELLOW if wire_states[5] else WHITE))
        and_gate_1.add_updater(lambda m: m.set_color(YELLOW if wire_states[3] else WHITE))

        # Skip to 000 and stop counter
        self.play(clk.cycle_rate.animate.set_value(2 * PI), run_time=4)
        while wire_states[1] or wire_states[2] or wire_states[4]:
            self.wait(0.25)
        self.play(clk.cycle_rate.animate.set_value(0), run_time=1)

        # 2 XOR Gates Initialisation

        grey_code_xor_1 = XORGate(scale_factor=0.6).rotate(PI / 2)
        grey_code_xor_1.move_to(xor_gate_1.get_center() + [-0.6, 2, 0])

        grey_code_xor_2 = XORGate(scale_factor=0.6).rotate(PI / 2)
        grey_code_xor_2.move_to(xor_gate_2.get_center() + [-0.5, 2, 0])

        self.play(Transform(lines[0].get_part_by_tex(r"\oplus").copy(), grey_code_xor_1),
                  Transform(lines[1].get_part_by_tex(r"\oplus").copy(), grey_code_xor_2))

        # New Wire Initialization
        B_2_junction = Dot(
            [DFFs[2].get_output()[0] + 0.2, 3 * xor_gate_2.get_input_a()[1] - 2 * DFFs[2].get_input()[1], 0])

        new_wires = VGroup(
            Wire(points=[  # Q(0) to GREY_XOR(0)
                ([grey_code_xor_1.get_input_a()[0], and_gate_1.get_input_a()[1], 0], True),
                grey_code_xor_1.get_input_a()
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # Q(1) to GREY_XOR(0)
                ([grey_code_xor_1.get_input_b()[0], and_gate_1.get_input_b()[1], 0], True),
                grey_code_xor_1.get_input_b()
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # Q(1) to GREY_XOR(1)
                ([DFFs[1].get_output()[0] - 0.1, and_gate_1.get_input_b()[1], 0], True),
                grey_code_xor_2.get_input_a()
            ], edges=[
                (0, 1, 0.7, 1)
            ]),
            Wire(points=[  # Q(2) to GREY_XOR(1)
                ([xor_gate_2.get_output()[0], 3 * xor_gate_2.get_input_a()[1] - 2 * DFFs[2].get_input()[1], 0], True),
                grey_code_xor_2.get_input_b()
            ], edges=[
                (0, 1, 0.8, 1)
            ]),
            Wire(points=[  # GREY_XOR(0) TO G(0)
                grey_code_xor_1.get_output(),
                (grey_code_xor_1.get_output() + UP * 0.3, True)
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # GREY_XOR(1) TO G(1)
                grey_code_xor_2.get_output(),
                (grey_code_xor_2.get_output() + UP * 0.3, True)
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # Q(2) to G(2)
                B_2_junction.get_center(),
                ([B_2_junction.get_center()[0], grey_code_xor_2.get_output()[1] + 0.3, 0], True)
            ], edges=[
                (0, 1)
            ])
        )

        """
        0- Q(0) to GREY_XOR(0)
        1- Q(1) to GREY_XOR(0)
        2- Q(1) to GREY_XOR(1)
        3- Q(2) to GREY_XOR(1)
        4- GREY_XOR(0) TO G(0)
        5- GREY_XOR(1) TO G(1)
        6- Q(2) to G(2)
        """

        wire_prop_delay = [0.2, 0.4, 0.6, 0.7, 1, 0.4, 0.5, 0]
        # New wire updaters
        new_wire_states = [0] * 7
        new_wire_delay = [0] * 7
        new_wire_changing = [False] * 7
        new_wire_prop_delay = [0] * 7
        new_wire_next_color = [WHITE] * 7

        def new_wire_updater(m, dt, i):
            if i == 0 and DFFs[0].get_state() or \
                    i == 1 and DFFs[1].get_state() or \
                    i == 2 and DFFs[1].get_state() or \
                    i == 3 and DFFs[2].get_state() or \
                    i == 4 and (new_wire_states[0] ^ new_wire_states[1]) or \
                    i == 5 and (new_wire_states[2] ^ new_wire_states[3]) or \
                    i == 6 and DFFs[2].get_state():
                if not new_wire_states[i] and not new_wire_changing[i]:
                    new_wire_changing[i] = True
                    new_wire_next_color[i] = YELLOW
            else:
                if new_wire_states[i] and not new_wire_changing[i]:
                    new_wire_changing[i] = True
                    new_wire_next_color[i] = WHITE

            if new_wire_changing[i]:
                new_wire_delay[i] += dt
                if new_wire_delay[i] > new_wire_prop_delay[i]:
                    new_wire_delay[i] = 0
                    new_wire_changing[i] = False
                    m.set_color(new_wire_next_color[i])
                    new_wire_states[i] = 1 if new_wire_next_color[i] == YELLOW else 0

        for i in range(len(new_wires)):
            new_wires[i].add_updater(lambda m, dt, i=i: new_wire_updater(m, dt, i))

        # Gate updaters
        grey_code_xor_1.add_updater(lambda m: m.set_color(YELLOW if new_wire_states[4] else WHITE))
        grey_code_xor_2.add_updater(lambda m: m.set_color(YELLOW if new_wire_states[5] else WHITE))

        # Transform equation components into its respective circuit component
        # Builds the 3 bit Grey Code Counter
        self.play(Transform(lines[0].get_part_by_tex(r"B_0").copy(), new_wires[0].junctions[0]),
                  Transform(lines[0].get_part_by_tex(r"B_1").copy(), new_wires[1].junctions[0]))

        self.play(Transform(lines[1].get_part_by_tex(r"B_1").copy(), new_wires[2].junctions[0]),
                  Transform(lines[1].get_part_by_tex(r"B_2").copy(), new_wires[3].junctions[0]))

        self.play(Transform(lines[2].get_part_by_tex(r"B_2").copy(), B_2_junction))

        self.play(*[Create(VGroup(*wire.wires)) for wire in new_wires[:4]])

        self.play(*[Create(wire) for wire in new_wires[4:]])

        grey_code_labels = VGroup(MathTex(r"G_0", color=GREY),
                                  MathTex(r"G_1", color=GREY),
                                  MathTex(r"G_2", color=GREY))
        grey_code_labels[0].move_to(grey_code_xor_1.get_output() + UP * 0.6)
        grey_code_labels[1].move_to(grey_code_xor_2.get_output() + UP * 0.6)
        grey_code_labels[2].move_to([B_2_junction.get_center()[0], grey_code_xor_2.get_output()[1] + 0.3, 0] + UP * 0.3)

        self.play(*[Transform(lines[i].get_part_by_tex(rf"G_{i}").copy(), grey_code_labels[i]) for i in range(3)])

        # Start Grey Code Counter
        new_wires[-1].add(B_2_junction)
        self.add(new_wires, grey_code_xor_1, grey_code_xor_2)
        self.play(clk.cycle_rate.animate.set_value(PI))

        # Zoom out
        self.play(
            self.camera.frame.animate.scale(1.8).shift(UP * 2),
            FadeOut(lines)
        )

        # Two Logic Level Graphs
        t_offset = ValueTracker(0)
        graph_speed = ValueTracker(0.5)
        self.add(t_offset)
        t_offset.add_updater(lambda m, dt: m.increment_value(dt * graph_speed.get_value()))

        X_OFFSET = 8

        clk_curve_start = 7 * UP + X_OFFSET * LEFT
        clk_curve = VGroup(Line(clk_curve_start, clk_curve_start, color=ORANGE))

        def get_clk_curve():
            last_line = clk_curve[-1]
            x = clk_curve_start[0] + t_offset.get_value()
            y = clk_curve_start[1] + wire_states[7] * 0.5  # Clock wire
            if y == last_line.get_start()[1]:
                new_line = Line(last_line.get_start(), np.array([x, y, 0]), color=ORANGE)
                clk_curve[-1] = new_line
            else:
                new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=ORANGE)
                clk_curve.add(new_line)
            fill_area = VMobject().set_points_as_corners(list(np.vstack([line.get_points() for line in clk_curve]))
                                                         + [RIGHT * x + 7 * UP, clk_curve_start]) \
                .set_fill(ORANGE, opacity=0.4).set_stroke(width=0)
            return VGroup(clk_curve, fill_area)

        clk_graph = always_redraw(get_clk_curve)

        def get_curve(value, curve_start, curve, graph_color):
            last_line = curve[-1]
            x = curve_start[0] + t_offset.get_value()
            y = curve_start[1] + value * 0.6  # D Flip Flop input wire
            if y == last_line.get_start()[1]:
                new_line = Line(last_line.get_start(), np.array([x, y, 0]), color=graph_color)
                curve[-1] = new_line
            else:
                new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=graph_color)
                curve.add(new_line)
            fill_area = VMobject().set_points_as_corners(list(np.vstack([line.get_points() for line in curve]))
                                                         + [RIGHT * (x + X_OFFSET) + curve_start, curve_start]) \
                .set_fill(graph_color, opacity=0.4).set_stroke(width=0)
            return VGroup(curve, fill_area)

        grey_curve_start = [[-X_OFFSET, 6, 0], [-X_OFFSET, 5, 0], [-X_OFFSET, 4, 0]]
        grey_curve = [VGroup() for _ in range(3)]
        grey_wire_index = [4, 5, 6]
        grey_graph_color = [BLUE_A, BLUE_C, BLUE_E]
        grey_graph = []
        for i in range(3):
            grey_curve[i].add(Line(grey_curve_start[i], grey_curve_start[i], color=grey_graph_color[i]))
            grey_graph.append(always_redraw(lambda i=i: get_curve(
                new_wire_states[grey_wire_index[i]], grey_curve_start[i], grey_curve[i], grey_graph_color[i]
            )))

        graph_labels = [MathTex("CLK"), MathTex(r"G_0"), MathTex(r"G_1"), MathTex(r"G_2")]

        [label.next_to(graph.get_corner(DL), LEFT) for label, graph in zip(graph_labels, [clk_graph, *grey_graph])]
        self.add(clk_graph, *[graph for graph in grey_graph])

        self.play(*[FadeIn(label) for label in graph_labels])

        self.wait(30)

        # Empty screen + Camera Transition
        self.play(self.camera.frame.animate.shift(UP * 20).set_run_time(1))
        self.clear()
        self.play(self.camera.frame.animate.shift(DOWN * 20).set_run_time(1))


class GreyCode(MovingCameraScene):
    def construct(self):
        # Ripple effect from incrementing
        binary = MathTex(*([r"\ldots"] + list(r"101101111")), font_size=48, color=BLUE) \
            .shift(3 * UP)
        add_arrow = Arrow(ORIGIN, 3 * DOWN, max_tip_length_to_length_ratio=0.15, stroke_width=6, color=GREEN) \
            .next_to(binary, DOWN)
        add_label = MathTex(r"+1", font_size=48, color=GREEN) \
            .next_to(add_arrow.get_center(), RIGHT)
        new_binary = MathTex(*([r"\ldots"] + list(r"101110000")), font_size=48, color=BLUE) \
            .next_to(add_arrow.get_end(), DOWN)

        self.play(Write(binary))
        self.wait(1)
        self.play(Create(add_arrow, rate_func=rush_into, run_time=1),
                  FadeIn(add_label, shift=DOWN, scale=0.1, rate_func=rush_from, run_time=1))
        self.play(Write(new_binary))

        # XOR of digits to show single transition

        self.play(FadeOut(add_arrow),
                  FadeOut(add_label),
                  binary.animate.shift(DOWN),
                  new_binary.animate.shift(UP))
        self.wait(1)

        ripple_end_line_1 = DashedLine(
            (binary[4].get_edge_center(RIGHT) + binary[5].get_edge_center(LEFT)) / 2 + 1 * UP,
            (binary[4].get_edge_center(RIGHT) + binary[5].get_edge_center(
                LEFT)) / 2 + 5 * DOWN,
            color=RED, stroke_width=2)
        ripple_end_line_2 = DashedLine(
            (binary[5].get_edge_center(RIGHT) + binary[6].get_edge_center(LEFT)) / 2 + 1 * UP,
            (binary[5].get_edge_center(RIGHT) + binary[6].get_edge_center(
                LEFT)) / 2 + 5 * DOWN,
            color=RED, stroke_width=2)

        def get_picker(point1, point2):
            return VGroup(Line(point1 + UP * 0.1, point1 + UP * 0.3),
                          Line(point1 + UP * 0.3, [point2[0], point1[1] + 0.3, 0]),
                          Line([point2[0], point1[1] + 0.3, 0], [point2[0], point1[1] + 0.1, 0]),
                          stroke_width=6).set_color(RED)

        self.play(Create(ripple_end_line_1), Create(ripple_end_line_2))

        # Generation of Grey Code with XOR
        grey_code = MathTex(*(["X"] + [r"\ldots"] + list(r"11011000")), font_size=48, color=GRAY)
        [grey_code[i].move_to(binary[i].get_center() + 3 * DOWN) for i in range(10)]
        grey_code[1].shift(LEFT * 0.2 + DOWN * 0.16)

        picker_states = [None, get_picker(binary[9].get_edge_center(UP), binary[8].get_edge_center(UP))]
        self.play(FadeIn(picker_states[1]))
        self.play(Transform(VGroup(binary[9].copy(), binary[8].copy()), grey_code[9]))
        for i in range(8, 0, -1):
            picker_states[0] = picker_states[1]
            picker_states[1] = get_picker(binary[i].get_edge_center(UP), binary[i - 1].get_edge_center(UP))
            self.play(ReplacementTransform(picker_states[0], picker_states[1]))
            self.play(ReplacementTransform(VGroup(binary[i].copy(),
                                                  binary[i - 1].copy()), grey_code[i]))

        new_grey_code = MathTex(*(["X"] + [r"\ldots"] + list(r"11001000")), font_size=48, color=GRAY)
        [new_grey_code[i].move_to(new_binary[i].get_center() + 3 * DOWN) for i in range(10)]
        new_grey_code[1].shift(LEFT * 0.2 + DOWN * 0.16)

        picker_states[0] = picker_states[1]
        picker_states[1] = get_picker(new_binary[9].get_edge_center(UP), new_binary[8].get_edge_center(UP))
        self.play(ReplacementTransform(picker_states[0], picker_states[1]))
        self.play(Transform(VGroup(new_binary[9].copy(), new_binary[8].copy()), new_grey_code[9]))
        for i in range(8, 0, -1):
            picker_states[0] = picker_states[1]
            picker_states[1] = get_picker(new_binary[i].get_edge_center(UP), new_binary[i - 1].get_edge_center(UP))
            self.play(ReplacementTransform(picker_states[0], picker_states[1]))
            self.play(ReplacementTransform(VGroup(new_binary[i].copy(),
                                                  new_binary[i - 1].copy()), new_grey_code[i]))
        self.wait(1)
        self.play(FadeOut(ripple_end_line_2))
        self.wait(1)

        # Empty screen + Camera Transition
        self.play(self.camera.frame.animate.shift(DOWN * 20).set_run_time(1))
        self.clear()
        self.play(self.camera.frame.animate.shift(UP * 20).set_run_time(1))

        self.wait(2)

        # Show recursive Grey Code Generation Formula
        lines = VGroup(
            MathTex(r"G_0", "=", r"B_1", r"\oplus", r"B_0"),
            MathTex(r"G_1", "=", r"B_2", r"\oplus", r"B_1"),
            MathTex(r"G_2", "=", r"B_2", r"\oplus", r"B_3"),
            MathTex(r"\vdots"),
            MathTex(r"G_i", "=", r"B_i", r"\oplus", r"B_{i-1}")
        )

        for line in lines:
            line.set_color(BLUE)

        for line in lines:
            for eq in line.get_parts_by_tex("="):
                eq.set_color(WHITE)

        for tex in ["G_2", "G_1", "G_0", "G_i"]:
            for line in lines:
                for part in line.get_parts_by_tex(tex):
                    part.set_color(GREY)

        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        lines.move_to(ORIGIN)

        for line in lines:
            self.play(Write(line))
            self.wait(0.4)

        self.wait(1)

        # Empty screen + Camera Transition
        self.play(self.camera.frame.animate.shift(RIGHT * 20).set_run_time(1))
        self.clear()
        self.play(self.camera.frame.animate.shift(LEFT * 20).set_run_time(1))


class ThreeDGreyCode(ThreeDScene):
    def construct(self):
        # only positive directions (first octant)
        ax = ThreeDAxes(
            x_range=[0, 3, 1],
            y_range=[0, 3, 1],
            z_range=[0, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )

        self.set_camera_orientation(phi=65 * DEGREES, theta=-105 * DEGREES)
        self.move_camera(frame_center=OUT, run_time=0.1)
        self.play(Create(ax))
        self.wait(1)

        cube = Cube(color=BLUE).move_to(ax.c2p(0.5, 0.5, 0.5)).set_stroke(width=6)
        cube.set_fill(opacity=0)
        self.play(Create(cube), run_time=1)

        vertices = [ax.c2p(i // 4, (i // 2) % 2, i % 2) for i in range(8)]
        # Add spherical dots on each vertex
        dots = VGroup(Dot3D(color=BLUE, point=vertex, resolution=(4, 4)) for vertex in vertices)
        self.play(
            LaggedStart(*[Create(dot) for dot in dots])
        )
        self.wait(2)
        self.play(ax.animate.set_opacity(0))
        self.wait(1)
        self.move_camera(frame_center=IN, run_time=1)
        self.wait(2)

        three_bit_labels = VGroup(
            *[MathTex(x).rotate(PI / 2, RIGHT).rotate(15 * DEGREES, IN)
              for x in [r"000", r"001", r"010", r"011", r"100", r"101", r"110", r"111"]])
        # self.add_fixed_in_frame_mobjects(*three_bit_labels)
        three_bit_labels.arrange(IN).shift(4 * RIGHT)
        self.play(*[Create(label) for label in three_bit_labels])
        self.wait(1)

        coords = VGroup()
        for i, p in enumerate(vertices):
            x, y, z = i // 4, (i // 2) % 2, i % 2
            label = MathTex(rf"({int(x)}, {int(y)}, {int(z)})").scale(0.4)
            label.move_to(p + 0.2 * (p - [0.5, 0.5, 0.5]))
            label.rotate(PI / 2, axis=RIGHT)
            coords.add(label)

        # self.add_fixed_orientation_mobjects(*coords)
        self.play(Succession(*[Transform(label, coord, run_time=0.5)
                               for label, coord in zip(three_bit_labels, coords)]))

        self.wait(1)

        line_color = [GREEN_E, RED]
        lines = VGroup(Line(vertices[i], vertices[i + 1], color=line_color[i % 2], stroke_width=6)
                       for i in range(len(vertices) - 1))
        lines.add(Line(vertices[7], vertices[0], color=RED, stroke_width=6))
        for i in range(len(lines)):
            self.play(dots[i].animate.set_color(GREEN_E), run_time=1)
            self.play(Create(lines[i], run_time=1))

        self.wait(2)

        new_cube = cube.copy()
        new_dots = dots.copy().set_color(BLUE)
        new_labels = three_bit_labels.copy()

        self.play(
            FadeIn(new_cube),
            FadeIn(new_dots),
            FadeIn(new_labels),
            cube.animate.shift(RIGHT * 5),
            dots.animate.shift(RIGHT * 5),
            three_bit_labels.animate.shift(RIGHT * 5),
            lines.animate.shift(RIGHT * 5)
        )

        order = [0, 1, 3, 2, 6, 7, 5, 4]
        new_lines = VGroup(Line(new_dots[order[i]].get_center(), new_dots[order[i + 1]].get_center(),
                                color=GREEN_E, stroke_width=6)
                           for i in range(len(order) - 1))
        new_lines.add(Line(new_dots[order[7]].get_center(), new_dots[order[0]].get_center(),
                           color=GREEN_E, stroke_width=6))
        for i in range(len(lines)):
            self.play(new_dots[order[i]].animate.set_color(GREEN_E), run_time=1)
            self.play(Create(new_lines[i], run_time=1))

        sym_plane = Square(color=GRAY, side_length=3, fill_color=GRAY, fill_opacity=0.4) \
            .rotate(PI / 2, UP).move_to(ax.c2p(0.5, 0.5, 0.5))

        self.play(GrowFromPoint(sym_plane, point=sym_plane.get_center()))

        self.wait(2)
        grey_code = VGroup(
            *[MathTex(x).rotate(PI / 2, RIGHT).rotate(15 * DEGREES, IN)
              for x in [r"000", r"001", r"011", r"010", r"110", r"111", r"101", r"100"]])
        [itm.move_to(ax.c2p(i / 2 - 1, (1 - i / 2) * np.tan(15 * DEGREES), -1)) for i, itm in enumerate(grey_code)]

        for label, code in zip(new_labels, grey_code):
            self.play(Transform(label, code), run_time=0.5)
        self.wait(2)

        # Empty screen + Camera Transition

        self.move_camera(frame_center=OUT * 20, run_time=0.1)
        self.clear()
        self.move_camera(frame_center=IN * 20, run_time=0.1)


class SyncCounter(MovingCameraScene):
    def construct(self):
        # Flip Flop Initialization
        DFFs = VGroup(DFlipFlop() for _ in range(3))
        DFFs.arrange(buff=2)

        # Gate Initialization
        xor_gate_1 = XORGate(scale_factor=0.6)
        xor_gate_1.move_to(DFFs[0].get_output() + RIGHT)

        xor_gate_2 = XORGate(scale_factor=0.6)
        xor_gate_2.move_to(DFFs[1].get_output() + RIGHT * 1.2)

        and_gate_1 = ANDGate(scale_factor=0.6)
        and_gate_1.move_to(DFFs[1].get_output() + UP + RIGHT * 0.6)

        # Clock Initialization
        clk_text = Tex(r"CLK")
        clk_text.move_to(DFFs[0]).shift([-2, -2, 0])

        clk = Clock(radius=0.5, cycle_rate=PI / 2).next_to(clk_text, DOWN)

        # Wire Initialization

        wires = [
            Wire(points=[  # Q_bar(0) to D(0)
                DFFs[0].get_negated_output(),
                DFFs[0].get_negated_output() + RIGHT / 3,
                DFFs[0].get_input() + LEFT / 3,
                DFFs[0].get_input()
            ], edges=[
                (0, 1),
                (1, 2, 1.5, 1),
                (2, 3)
            ]).set_color(YELLOW),
            Wire(points=[  # Q(0) to XOR(1) and AND
                DFFs[0].get_output(),
                xor_gate_1.get_input_b(),
                (DFFs[0].get_output() + RIGHT / 6, True),
                DFFs[0].get_output() + RIGHT / 6 + UP * (and_gate_1.get_input_a() - DFFs[0].get_output())[1],
                and_gate_1.get_input_a()
            ], edges=[
                (0, 1, 0.7, 0),
                (2, 3),
                (3, 4)
            ]),
            Wire(points=[  # Q(1) to XOR(1) and AND
                DFFs[1].get_output(),
                and_gate_1.get_input_b(),
                (and_gate_1.get_input_b() + LEFT * (and_gate_1.get_input_b() - DFFs[1].get_output())[0] / 2, True),
                xor_gate_1.get_input_a()
            ], edges=[
                (0, 1, 0.5, 0),
                (2, 3, 1.05, 0)
            ]),
            Wire(points=[  # AND to XOR(2)
                and_gate_1.get_output(),
                and_gate_1.get_output() + RIGHT * 0.2,
                xor_gate_2.get_input_b() + LEFT * 0.3,
                xor_gate_2.get_input_b()
            ], edges=[
                (0, 1),
                (1, 2, 0.4, 1),
                (2, 3)
            ]),
            Wire(points=[  # Q(2) to XOR(2)
                DFFs[2].get_output(),
                DFFs[2].get_output() + RIGHT * 0.2,
                xor_gate_2.get_input_a() + LEFT * 0.2,
                xor_gate_2.get_input_a()
            ], edges=[
                (0, 1),
                (1, 2, 3, 1),
                (2, 3)
            ]),
            Wire(points=[  # XOR(2) to D(2)
                xor_gate_2.get_output(),
                DFFs[2].get_input()
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # XOR(1) to D(1)
                xor_gate_1.get_output(),
                DFFs[1].get_input()
            ], edges=[
                (0, 1)
            ]),
            VGroup(Wire(points=[  # CLK to all Edge Trigger DFF Inputs
                clk_text.get_edge_center(RIGHT),
                DFFs[0].get_edge_trigger_indicator() + LEFT * 0.1,
                DFFs[1].get_edge_trigger_indicator() + LEFT * 0.1,
                DFFs[2].get_edge_trigger_indicator() + LEFT * 0.1
            ], edges=[
                (0, 1, 0.5, 0),
                (0, 2, 0.8, 0),
                (0, 3, 0.95, 0)
            ]), Circle(radius=0.05, color=WHITE).move_to(DFFs[0].get_edge_trigger_indicator() + LEFT * 0.05),
                Circle(radius=0.05, color=WHITE).move_to(DFFs[1].get_edge_trigger_indicator() + LEFT * 0.05),
                Circle(radius=0.05, color=WHITE).move_to(DFFs[2].get_edge_trigger_indicator() + LEFT * 0.05)
            )
        ]

        self.play(LaggedStart(*[FadeIn(ff, shift=DOWN, target_position=ff.get_center() + UP) for ff in DFFs],
                              lag_ratio=0.4), run_time=2)

        self.play(FadeIn(xor_gate_1, shift=DOWN, target_position=xor_gate_1.get_center() + UP),
                  FadeIn(xor_gate_2, shift=DOWN, target_position=xor_gate_2.get_center() + UP),
                  FadeIn(and_gate_1, shift=DOWN, target_position=and_gate_1.get_center() + UP))
        self.play(*[Create(wire) for wire in wires], run_time=1)

        self.play(Succession(Create(clk_text), Create(clk)), run_time=1)
        clk.set_angle_value(PI)

        # Clock negative edge detection
        edge_trigger = ValueTracker(0)
        prev_clk_level = {"HIGH": 0}
        self.add(edge_trigger)

        def detect_edge(m):
            if prev_clk_level["HIGH"] and np.sin(clk.angle_tracker.get_value()) > 0:
                m.set_value(1)
            else:
                m.set_value(0)
            prev_clk_level["HIGH"] = int(np.sin(clk.angle_tracker.get_value()) <= 0)

        edge_trigger.add_updater(detect_edge)

        """
        0-Q_bar(0) to D(0)
        1-Q(0) to XOR(1) and AND
        2-Q(1) to XOR(1) and AND
        3-AND to XOR(2)
        4-Q(2) to XOR(2)
        5-XOR(2) to D(2)
        6-XOR(1) to D(1)
        7-CLK to all Edge Trigger DFF Inputs
        """

        # Wire updaters
        wire_states = [0] * 8
        wire_delay = [0] * 8
        wire_changing = [False] * 8
        wire_prop_delay = [0] * 8
        wire_prop_delay = [delay * 2 for delay in wire_prop_delay]
        wire_next_color = [WHITE] * 8

        def wire_updater(m, dt, i):
            if i == 0 and 1 - DFFs[0].get_state() or \
                    i == 1 and DFFs[0].get_state() or \
                    i == 2 and DFFs[1].get_state() or \
                    i == 3 and wire_states[1] and wire_states[2] or \
                    i == 4 and DFFs[2].get_state() or \
                    i == 5 and (DFFs[2].get_state() ^ wire_states[3]) or \
                    i == 6 and DFFs[0].get_state() ^ DFFs[1].get_state() or \
                    i == 7 and np.sin(clk.angle_tracker.get_value()) <= 0:
                if not wire_states[i] and not wire_changing[i]:
                    wire_changing[i] = True
                    wire_next_color[i] = YELLOW
            else:
                if wire_states[i] and not wire_changing[i]:
                    wire_changing[i] = True
                    wire_next_color[i] = WHITE

            if wire_changing[i]:
                wire_delay[i] += dt
                if wire_delay[i] > wire_prop_delay[i]:
                    wire_delay[i] = 0
                    wire_changing[i] = False
                    m.set_color(wire_next_color[i])
                    wire_states[i] = 1 if wire_next_color[i] == YELLOW else 0

        for i in range(len(wires)):
            wires[i].add_updater(lambda m, dt, i=i: wire_updater(m, dt, i))

        # Flip Flop updaters
        DFFs[0].add_updater(lambda m: m.set_state(wire_states[0]) if edge_trigger.get_value() else None)
        DFFs[1].add_updater(lambda m: m.set_state(wire_states[6]) if edge_trigger.get_value() else None)
        DFFs[2].add_updater(lambda m: m.set_state(wire_states[5]) if edge_trigger.get_value() else None)

        # Gate updaters
        xor_gate_1.add_updater(lambda m: m.set_color(YELLOW if wire_states[6] else WHITE))
        xor_gate_2.add_updater(lambda m: m.set_color(YELLOW if wire_states[5] else WHITE))
        and_gate_1.add_updater(lambda m: m.set_color(YELLOW if wire_states[3] else WHITE))
        self.wait(1)

        # Zoom out
        self.play(
            self.camera.frame.animate.scale(1.5).shift(UP * 2)
        )
        self.wait(1.5)

        # Two Logic Level Graphs
        t_offset = ValueTracker(0)
        graph_speed = ValueTracker(0.5)
        self.add(t_offset)
        t_offset.add_updater(lambda m, dt: m.increment_value(dt * graph_speed.get_value()))

        X_OFFSET = 8

        clk_curve_start = 6 * UP + X_OFFSET * LEFT
        clk_curve = VGroup(Line(clk_curve_start, clk_curve_start, color=ORANGE))

        def get_clk_curve():
            last_line = clk_curve[-1]
            x = clk_curve_start[0] + t_offset.get_value()
            y = clk_curve_start[1] + wire_states[7] * 0.5  # Clock wire
            if y == last_line.get_start()[1]:
                new_line = Line(last_line.get_start(), np.array([x, y, 0]), color=ORANGE)
                clk_curve[-1] = new_line
            else:
                new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=ORANGE)
                clk_curve.add(new_line)
            fill_area = VMobject().set_points_as_corners(list(np.vstack([line.get_points() for line in clk_curve]))
                                                         + [RIGHT * x + 6 * UP, clk_curve_start]) \
                .set_fill(ORANGE, opacity=0.4).set_stroke(width=0)
            return VGroup(clk_curve, fill_area)

        clk_graph = always_redraw(get_clk_curve)

        def get_curve(value, curve_start, curve, graph_color):
            last_line = curve[-1]
            x = curve_start[0] + t_offset.get_value()
            y = curve_start[1] + value * 0.6  # D Flip Flop input wire
            if y == last_line.get_start()[1]:
                new_line = Line(last_line.get_start(), np.array([x, y, 0]), color=graph_color)
                curve[-1] = new_line
            else:
                new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=graph_color)
                curve.add(new_line)
            fill_area = VMobject().set_points_as_corners(list(np.vstack([line.get_points() for line in curve]))
                                                         + [RIGHT * (x + X_OFFSET) + curve_start, curve_start]) \
                .set_fill(graph_color, opacity=0.4).set_stroke(width=0)
            return VGroup(curve, fill_area)

        DFFs_curve_start = [[-X_OFFSET, 5, 0], [-X_OFFSET, 4, 0], [-X_OFFSET, 3, 0]]
        DFFs_curve = [VGroup() for _ in range(3)]
        DFFs_wire_index = [1, 2, 4]
        DFFs_graph_color = [BLUE_A, BLUE_C, BLUE_E]
        DFFs_graph = []
        for i in range(3):
            DFFs_curve[i].add(Line(DFFs_curve_start[i], DFFs_curve_start[i], color=DFFs_graph_color[i]))
            DFFs_graph.append(always_redraw(lambda i=i: get_curve(
                wire_states[DFFs_wire_index[i]], DFFs_curve_start[i], DFFs_curve[i], DFFs_graph_color[i]
            )))

        graph_labels = [MathTex("CLK"), MathTex("Bit 0"), MathTex("Bit 1"), MathTex("Bit 2")]

        [label.next_to(graph.get_corner(DL), LEFT) for label, graph in zip(graph_labels, [clk_graph, *DFFs_graph])]
        self.add(clk_graph, *[graph for graph in DFFs_graph])

        self.play(*[FadeIn(label) for label in graph_labels])

        self.wait(35)

        # Zoom in and Fade Out Graphs
        self.play(self.camera.frame.animate.scale(2 / 3).shift(3 * DOWN))

        # Reset graphs
        t_offset.set_value(0)
        graph_speed.set_value(0)
        for i in range(3):
            DFFs_curve[i].submobjects = []
            DFFs_curve[i].add(Line(DFFs_curve_start[i], DFFs_curve_start[i], color=DFFs_graph_color[i]))
        clk_curve.submobjects = []
        clk_curve.add(Line(clk_curve_start, clk_curve_start, color=ORANGE))

        # Add propagation delay
        wire_prop_delay = [0.2, 0.4, 0.6, 0.7, 1, 0.4, 0.5, 0]
        self.wait(2)

        # Highlight D-Flip Flops
        self.play(LaggedStart(*[Circumscribe(DFFs[i].label_q) for i in range(3)], lag_ratio=0.4), run_time=2)
        graph_speed.set_value(0.5)
        self.play(clk.cycle_rate.animate.set_value(PI / 4), run_time=2)

        # Zoom in
        self.play(self.camera.frame.animate.scale(1.5).shift(3 * UP))

        self.wait(4)

        self.play(AnimationGroup(graph_speed.animate.set_value(0), clk.cycle_rate.animate.set_value(0)))

        glitch_indicator_line_1 = DashedLine([-6.61, 7, 0], [-6.61, 2, 0], color=RED)
        glitch_indicator_line_2 = DashedLine([-6.43, 7, 0], [-6.43, 2, 0], color=RED)

        glitch_value_1 = MathTex("010", font_size=96, color=RED)
        glitch_value_2 = MathTex("000", font_size=96, color=RED)
        expected_value = MathTex("100", font_size=96, color=GREEN)
        expected_value_title = Tex("Expected Value: ", font_size=96)

        expected_value_title.move_to([3, 5, 0])
        expected_value.next_to(expected_value_title, RIGHT)

        glitch_value_1.next_to(expected_value, DOWN * 2 + LEFT)
        glitch_value_2.next_to(expected_value, DOWN * 2 + RIGHT)

        self.play(AnimationGroup(Create(glitch_indicator_line_1), Create(glitch_indicator_line_2)))
        self.wait(2)

        self.play(AnimationGroup(Transform(glitch_indicator_line_1, glitch_value_1),
                                 Transform(glitch_indicator_line_2, glitch_value_2)))
        self.play(Succession(Write(expected_value_title), Write(expected_value)))

        self.wait(2)
        glitch_value_1.save_state()
        glitch_value_2.save_state()
        self.play(AnimationGroup(Transform(glitch_value_1, expected_value),
                                 Transform(glitch_value_2, expected_value)),
                  rate_func=rush_into)
        self.play(AnimationGroup(Restore(glitch_value_1), Restore(glitch_value_2)), rate_func=rush_from)

        self.wait(2)

        self.play(
            Succession(self.camera.frame.animate.scale(2).set_run_time(4),
                       self.camera.frame.animate.shift(DOWN * 20).set_run_time(1))
        )
