from manim import *


class dictGraph2(Scene):
    def construct(self):
        paragraph1 = Paragraph("Unsurprisingly, this graph turns out to be disconnected.",
                               font_size=22)
        paragraph2 = Paragraph("Let's count the number of connected components of a given size.",
                               font_size=22)
        paragraph3 = Paragraph("Now, that's not very informative. Let's switch to log-log scale.",
                               font_size=22)
        paragraph4 = Paragraph("The plots look linear at small sizes in log-log scale, so they obey the power law.",
                               font_size=22).move_to(paragraph1.get_center())
        paragraphAux = Paragraph(" aux\naux", font_size=22)
        ax1 = Axes(
            x_range=[0, 8000, 1000],
            y_range=[0, 7000, 1000],
            tips=False,
            axis_config={"include_numbers": True}
        ).scale(0.7)
        VGroup(paragraph1, paragraph2, paragraph3, paragraph4, paragraphAux, ax1).arrange(DOWN, buff=0.1)
        x_label = ax1.get_x_axis_label(Text("size", font_size=20))
        y_label = ax1.get_y_axis_label(Text("number of connected components", font_size=20).rotate(1.5708),
                                        edge=LEFT, direction=LEFT)
        ax2 = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            tips=False,
            axis_config={"include_numbers": True, "scaling": LogBase(custom_labels=True)}
        ).scale(0.7).move_to(ax1.get_center())
        paragraph5 = Paragraph("It's interesting how a lot of distributions in nature obey a power law over a wide",
                               "range of magnitudes, including the initial star masses and the sizes of powercuts.",
                               font_size=22).move_to(paragraph1.get_center())

        sizesEn = []
        countsEn = []
        dotsEn = []
        sizesRu = []
        countsRu = []
        dotsRu = []
        numPointsEn = 17
        numPointsRu = 27
        animations=[]
        with open('componentsData_en_20k', 'r') as f:
            for i in range(numPointsEn):
                fields = f.readline().split()
                sizesEn.append(int(fields[0]))
                countsEn.append(int(fields[1]))
                dotsEn.append(Dot(ax1.c2p(int(fields[0]), int(fields[1])), color=BLUE))
                animations.append(Create(dotsEn[-1]))
        with open('componentsData_ru_20k', 'r') as f:
            for i in range(numPointsRu):
                fields = f.readline().split()
                sizesRu.append(int(fields[0]))
                countsRu.append(int(fields[1]))
                dotsRu.append(Dot(ax1.c2p(int(fields[0]), int(fields[1])), color=RED))
                animations.append(Create(dotsRu[-1]))
        labeldotEn = Dot(color=BLUE)
        labeldotRu = Dot(color=RED)
        VGroup(labeldotEn, labeldotRu).arrange(DOWN, buff=0.5).move_to(ax1.get_center() + RIGHT*2 + UP*2)
        labelEn = Text("English", font_size=24).move_to(labeldotEn.get_center() + RIGHT)
        labelRu = Text("Russian", font_size=24).move_to(labeldotRu.get_center() + RIGHT)
        lineEn = ax2.plot(lambda x: 10013.7*x**(-3.24863), color=BLUE, x_range=(0.001, 1))
        lineRu = ax2.plot(lambda x: 5665.68*x**(-2.14441), color=RED, x_range=(0.001, 1))
        labelLineEn = ax2.get_graph_label(lineEn, "power=-3.25", x_val=10, buff=-0.5, direction=LEFT).scale(0.5)
        labelLineRu = ax2.get_graph_label(lineRu, "power=-2.14", x_val=5, buff=-0.5, direction=RIGHT).scale(0.5)

        self.play(Write(paragraph1))
        self.play(Write(paragraph2))
        self.wait(2)
        self.play(Create(ax1), Create(x_label), Create(y_label), *animations,
                  Create(labeldotEn), Create(labelEn), Create(labeldotRu), Create(labelRu))
        animations.clear()
        self.wait(5)
        self.play(Write(paragraph3))

        for i in range(numPointsEn):
            animations.append(dotsEn[i].animate.move_to(ax2.c2p(sizesEn[i], countsEn[i])))
        for i in range(numPointsRu):
            animations.append(dotsRu[i].animate.move_to(ax2.c2p(sizesRu[i], countsRu[i])))
        self.play(Transform(ax1, ax2), *animations)
        animations.clear()
        self.wait(5)
        self.play(Write(paragraph4))
        self.play(Create(lineEn), Create(lineRu), Create(labelLineEn), Create(labelLineRu))
        self.wait(5)
        self.play(FadeOut(paragraph1), FadeOut(paragraph2), FadeOut(paragraph3), FadeOut(paragraph4))
        self.play(Write(paragraph5))
        self.wait(5)





