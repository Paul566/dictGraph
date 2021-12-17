from manim import *


class dictGraph1(Scene):
    def construct(self):
        paragraph1 = Paragraph("Take a set of words.", font_size=22)
        paragraph2 = Paragraph("If two words differ by one \ncharacter, connect them.", font_size=22,
                               line_spacing=0.5)
        paragraph3 = Paragraph("We will end up with a graph.", font_size=22)
        paragraph4 = Paragraph("Now do this for the 20,000 \nmost common English words,", font_size=22, line_spacing=0.5)
        paragraph5 = Paragraph("because why not.", font_size=22)
        VGroup(paragraph1, paragraph2, paragraph3, paragraph4, paragraph5).arrange(DOWN, buff=0.1).move_to(RIGHT*4)

        self.play(Write(paragraph1))

        v1 = LabeledDot(Text("while"), stroke_width=2, fill_color=BLACK).scale(0.7)
        v2 = LabeledDot(Text("white"), stroke_width=2, fill_color=BLACK).scale(0.7)
        v3 = LabeledDot(Text("the"), stroke_width=2, fill_color=BLACK).scale(0.7)
        v4 = LabeledDot(Text("they"), stroke_width=2, fill_color=BLACK).scale(0.7)
        v5 = LabeledDot(Text("whole"), stroke_width=2, fill_color=BLACK).scale(0.7)
        vertices = [v1, v2, v3, v4, v5]
        graph1 = Graph(vertices, [], layout='circular', labels={v: v for v in vertices},
                       vertex_type=LabeledDot, vertex_config={"stroke_color": WHITE, "fill_color": BLACK,
                                      "stroke_width": 0}).move_to(LEFT * 3)

        v1alt = LabeledDot(Text("while", t2c={'l':YELLOW}), stroke_color=YELLOW,
                             fill_color=BLACK, stroke_width=2).move_to(v1.get_center()).scale(0.7)
        v2alt = LabeledDot(Text("white", t2c={'t': YELLOW}), stroke_color=YELLOW,
                             fill_color=BLACK, stroke_width=2).move_to(v2.get_center()).scale(0.7)
        v1changed = LabeledDot(Text("white", t2c={'t': YELLOW}), stroke_color=YELLOW,
                           fill_color=BLACK, stroke_width=2).move_to(v1.get_center()).scale(0.7)
        v2changed = LabeledDot(Text("while", t2c={'l': YELLOW}), stroke_color=YELLOW,
                           fill_color=BLACK, stroke_width=2).move_to(v2.get_center()).scale(0.7)
        v1copy = v1.copy()
        v2copy = v2.copy()

        self.play(Create(graph1))
        self.wait()

        self.play(Write(paragraph2))
        self.play(Transform(v1, v1alt), Transform(v2, v2alt))
        self.play(Transform(v1, v1changed), Transform(v2, v2changed))
        self.play(Transform(v1, v1alt), Transform(v2, v2alt))
        self.play(Transform(v1, v1changed), Transform(v2, v2changed))
        self.play(Transform(v1, v1alt), Transform(v2, v2alt))
        self.play(Transform(v1, v1copy), Transform(v2, v2copy))
        self.play(graph1.animate.add_edges((v1, v2)))
        self.play(graph1.animate.add_edges((v1, v5)))
        self.play(graph1.animate.add_edges((v3, v4)))
        self.wait()
        self.play(Write(paragraph3))
        self.play(Write(paragraph4))
        self.play(Write(paragraph5))
        self.wait()
        self.play(FadeOut(graph1), FadeOut(paragraph1), FadeOut(paragraph2), FadeOut(paragraph3), FadeOut(paragraph4), FadeOut(paragraph5))