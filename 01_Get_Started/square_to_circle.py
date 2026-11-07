import manimgx as m


class SquareToCircle(m.Scene):
    def construct(self) -> None:
        title = m.Text("Square to Circle", font_size=36, color=m.WHITE).to_edge(m.UP, buff=0.8)
        square = m.Square(side_length=3.0, color=m.BLUE, fill_opacity=0.5)
        circle = m.Circle(radius=1.6, color=m.PINK, fill_opacity=0.5)

        self.play(m.Write(title))
        self.play(m.Create(square))
        self.wait(0.5)
        self.play(m.Transform(square, circle), run_time=1.5)
        self.wait(1.0)

