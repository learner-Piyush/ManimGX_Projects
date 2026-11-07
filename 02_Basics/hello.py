import manimgx as m


class Hello(m.Scene):
    def construct(self) -> None:
        circle = m.Circle()
        self.play(m.Create(circle))
        self.wait()