from manim import *
from helper import *


class GreyDecoder(MovingCameraScene):
    def construct(self):
        # Show recursive Grey Code Generation Formula for 3 bits
        self.wait(0.5)

        lines = VGroup(
            MathTex(r"G_0", "=", r"B_0", r"\oplus", r"B_1"),
            MathTex(r"G_1", "=", r"B_1", r"\oplus", r"B_2"),
            MathTex(r"G_2", "=", r"B_2")
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

        self.wait(1)

        self.play(*[
            AnimationGroup(
                MoveAlongPath(lines[i][0],
                              ArcBetweenPoints(
                                  lines[i][0].get_center(),
                                  lines[i][2].get_center(),
                                  angle=PI / 2
                              )),
                MoveAlongPath(lines[i][2],
                              ArcBetweenPoints(
                                  lines[i][2].get_center(),
                                  lines[i][0].get_center(),
                                  angle=PI / 2
                              ))
            ) for i in range(3)
        ])

        arrow_b2 = Arrow(
            lines[2][2].get_edge_center(UP),
            lines[1][4].get_edge_center(DOWN),
            max_tip_length_to_length_ratio=0.15,
            color=RED, stroke_width=6
        )

        arrow_b1 = Arrow(
            lines[1][2].get_edge_center(UP),
            lines[0][4].get_edge_center(DOWN),
            max_tip_length_to_length_ratio=0.15,
            color=RED, stroke_width=6
        )

        self.play(Succession(
            FadeIn(arrow_b2, scale=0.1),
            FadeIn(arrow_b1, scale=0.1)
        ))

        # Empty screen + Camera Transition
        self.play(self.camera.frame.animate.shift(LEFT * 20).set_run_time(1))
        self.clear()
        self.play(self.camera.frame.animate.shift(RIGHT * 20).set_run_time(1))

        temp_dots = VGroup(*[Dot(color=GRAY) for _ in range(3)])
        temp_dots.arrange(buff=2).to_edge(UP).shift(UP)

        grey_inputs = VGroup(*[
            VDict({"dot": Dot(color=GRAY),
                   "line": Line(UP, ORIGIN, color=GRAY, stroke_width=6),
                   "label": MathTex(rf"G_{i}", color=GRAY).shift(RIGHT * 0.5)
                   }) for i in range(3)
        ])

        grey_values = Group(*[ValueTracker(0) for _ in range(3)])
        grey_inputs.arrange(buff=2).to_edge(UP)

        self.add(*grey_values)

        self.play(Transform(temp_dots, grey_inputs), run_time=1, rate_func=rate_functions.ease_out_bounce)

        xor_gate_1, xor_gate_2 = XORGate().rotate(-PI / 2), XORGate().rotate(-PI / 2)

        xor_gate_1.move_to((grey_inputs[0]["dot"].get_center() + grey_inputs[1]["dot"].get_center()) / 2 + DOWN * 4)
        xor_gate_2.move_to((grey_inputs[1]["dot"].get_center() + grey_inputs[2]["dot"].get_center()) / 2 + DOWN * 2)

        self.play(Create(xor_gate_1), Create(xor_gate_2), run_time=2)

        wires = VGroup(
            Wire(points=[  # G(2) to XOR(1)
                grey_inputs[2]["dot"].get_center(),
                xor_gate_2.get_input_a()
            ], edges=[
                (0, 1, 0.5, 1)
            ]),
            Wire(points=[  # G(1) to XOR(1)
                grey_inputs[1]["dot"].get_center(),
                xor_gate_2.get_input_b()
            ], edges=[
                (0, 1, 0.5, 1)
            ]),
            Wire(points=[  # XOR(1) to XOR(0)
                xor_gate_2.get_output(),
                xor_gate_1.get_input_a()
            ], edges=[
                (0, 1, 0.5, 1)
            ]),
            Wire(points=[  # G(0) to XOR(0)
                grey_inputs[0]["dot"].get_center(),
                xor_gate_1.get_input_b()
            ], edges=[
                (0, 1, 0.5, 1)
            ]),
            Wire(points=[  # G(2) to B(2)
                grey_inputs[2]["dot"].get_center(),
                ([grey_inputs[2]["dot"].get_center()[0], xor_gate_1.get_output()[1] - 1, 0], True)
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # XOR(1) to B(1)
                xor_gate_2.get_output(),
                ([xor_gate_2.get_output()[0], xor_gate_1.get_output()[1] - 1, 0], True)
            ], edges=[
                (0, 1)
            ]),
            Wire(points=[  # XOR(0) to B(0)
                xor_gate_1.get_output(),
                (xor_gate_1.get_output() + DOWN, True)
            ], edges=[
                (0, 1)
            ]),
        )

        """
        0-G(2) to XOR(1)
        1-G(1) to XOR(1)
        2-XOR(1) to XOR(0)
        3-G(0) to XOR(0)
        4-G(2) to B(2)
        5-XOR(1) to B(1)
        6-XOR(0) to B(0)
        """
        # Wire updaters
        wire_states = [0] * 7

        def wire_updater(m, i):
            if i == 0 and grey_values[2].get_value() or \
                    i == 1 and grey_values[1].get_value() or \
                    i == 2 and wire_states[0] ^ wire_states[1] or \
                    i == 3 and grey_values[0].get_value() or \
                    i == 4 and wire_states[0] or \
                    i == 5 and wire_states[2] or \
                    i == 6 and wire_states[3] ^ wire_states[2]:
                m.set_color(YELLOW)
                wire_states[i] = True
            else:
                m.set_color(WHITE)
                wire_states[i] = False

        for i in range(len(wires)):
            wires[i].add_updater(lambda m, i=i: wire_updater(m, i))

        # XOR Gate updaters
        xor_gate_1.add_updater(lambda m: m.set_color(YELLOW if wire_states[6] else WHITE))
        xor_gate_2.add_updater(lambda m: m.set_color(YELLOW if wire_states[5] else WHITE))

        binary_labels = VGroup(*[
            MathTex(rf"B_{i}", color=BLUE).move_to(wires[-i-1].junctions[0].get_center() + RIGHT*0.5) for i in range(3)
        ])

        self.play(LaggedStart(*[Create(wire) for wire in wires],
                              *[Create(label) for label in binary_labels]),
                  lag_ratio=0.2)

        grey_code = ["000", "001", "011", "010", "110", "111", "101", "100"]
        for i in range(8):
            self.play(
                grey_values[0].animate.set_value(int(grey_code[i][2])),
                grey_values[1].animate.set_value(int(grey_code[i][1])),
                grey_values[2].animate.set_value(int(grey_code[i][0])),
                run_time=0.1
            )

            self.wait(1)

    xor_1_rect = SurroundingRectangle(

    )
