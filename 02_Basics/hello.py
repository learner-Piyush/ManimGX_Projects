import manimgx as m


class Steps(m.Scene):
    def construct(self) -> None:
        circle = m.Circle()
        words = m.Text("Hello!")
        self.play(m.Create(circle))  # from 0 to 1 second
        self.play(m.FadeOut(circle))  # from 1 to 2 seconds
        self.play(m.Write(words))  # from 2 to 3 seconds
        self.wait(2)  # from 3 to 5 seconds