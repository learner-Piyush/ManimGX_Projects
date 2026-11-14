"""Linear Equation in One Variable - ManimGX 60-Second Vertical Short.

Explaining 2x + 3 = 11 step-by-step for YouTube Shorts and Instagram Reels.
Target resolution: 1080 x 1920 (9:16 vertical), 30 FPS, duration: exactly 60.0 seconds.
"""

import manimgx as m

# Configure vertical canvas and 30 FPS
m.config.pixel_width = 1080
m.config.pixel_height = 1920
m.config.frame_rate = 30
m.config.background_color = "#0B0F19"  # Dark navy / charcoal

# Design System Color Palette
COLOR_BG = "#0B0F19"
COLOR_VAR = "#00E5FF"      # Cyan for variable x
COLOR_NUM = "#FACC15"      # Yellow for numbers and constants
COLOR_OP = "#FB923C"       # Orange for operations (+, -, /)
COLOR_EQUAL = "#FFFFFF"    # White for equals sign
COLOR_RESULT = "#4ADE80"   # Bright green for verified result
COLOR_TEXT = "#F1F5F9"     # Crisp off-white for subtitles & labels
COLOR_MUTED = "#94A3B8"    # Slate grey for subtle labels & accents
COLOR_CARD = "#161E2E"     # Dark card background
COLOR_BORDER = "#334155"   # Border stroke color
COLOR_ACCENT = "#38BDF8"   # Sky blue accent
COLOR_CANCEL = "#EF4444"   # Red for cancellation emphasis


def build_equation(*parts: str, font_size: int = 72) -> m.MathTex:
    """Create a MathTex equation with consistent syntax coloring."""
    eq = m.MathTex(*parts, font_size=font_size)
    for sub in eq:
        tex = getattr(sub, "tex_string", "")
        if "x" in tex:
            sub.set_color(COLOR_VAR)
        elif tex in ("+", "-"):
            sub.set_color(COLOR_OP)
        elif tex == "=":
            sub.set_color(COLOR_EQUAL)
        elif any(c.isdigit() for c in tex):
            sub.set_color(COLOR_NUM)
    return eq


def build_balance_scale(center=m.DOWN * 2.4, width: float = 4.8):
    """Create a stylized balance scale with pans resting safely on beam ends."""
    fulcrum = m.Triangle(color=COLOR_ACCENT, fill_color=COLOR_CARD, fill_opacity=1.0)
    fulcrum.scale(0.35).move_to(center + m.DOWN * 0.35)
    pivot = fulcrum.get_top()

    beam = m.Line(
        pivot + m.LEFT * (width / 2),
        pivot + m.RIGHT * (width / 2),
        stroke_width=4,
        color="#E2E8F0",
    )

    left_plate = m.RoundedRectangle(
        corner_radius=0.08,
        width=1.6,
        height=0.22,
        fill_color="#1E293B",
        fill_opacity=0.95,
        stroke_color=COLOR_ACCENT,
        stroke_width=2,
    ).next_to(beam.get_start(), m.UP, buff=0.05)

    right_plate = m.RoundedRectangle(
        corner_radius=0.08,
        width=1.6,
        height=0.22,
        fill_color="#1E293B",
        fill_opacity=0.95,
        stroke_color=COLOR_ACCENT,
        stroke_width=2,
    ).next_to(beam.get_end(), m.UP, buff=0.05)

    pivot_dot = m.Dot(pivot, radius=0.08, color=COLOR_NUM)

    scale_rig = m.VGroup(fulcrum, beam, left_plate, right_plate, pivot_dot)
    return scale_rig, left_plate.get_top(), right_plate.get_top()


class LinearEquation(m.Scene):
    """60-second educational short explaining Linear Equations in One Variable."""

    def construct(self) -> None:
        # ==========================================
        # Global UI Shell: Header & Subtitle Banner
        # ==========================================
        # Top Header Pill
        header_bg = m.RoundedRectangle(
            corner_radius=0.35,
            width=6.0,
            height=0.76,
            fill_color="#111827",
            fill_opacity=0.95,
            stroke_color=COLOR_ACCENT,
            stroke_width=2,
        ).move_to([0, 5.2, 0])
        header_text = m.Text(
            "LINEAR EQUATIONS",
            font_size=32,
            weight="BOLD",
            color=COLOR_TEXT,
        ).move_to(header_bg.get_center())
        header_group = m.VGroup(header_bg, header_text)

        # Step Indicator Badge
        step_bg = m.RoundedRectangle(
            corner_radius=0.24,
            width=4.6,
            height=0.64,
            fill_color=COLOR_CARD,
            fill_opacity=0.9,
            stroke_color="#F59E0B",
            stroke_width=1.5,
        ).move_to([0, 4.15, 0])
        step_label = m.Text(
            "THE EQUATION",
            font_size=28,
            weight="BOLD",
            color="#FDE047",
        ).move_to(step_bg.get_center())
        step_group = m.VGroup(step_bg, step_label)

        # Bottom Subtitle Pill
        sub_bg = m.RoundedRectangle(
            corner_radius=0.28,
            width=6.8,
            height=1.15,
            fill_color="#0F172A",
            fill_opacity=0.95,
            stroke_color=COLOR_BORDER,
            stroke_width=1.5,
        ).move_to([0, -5.1, 0])
        sub_text = m.Text(
            "Can you find the value of x?",
            font_size=28,
            color=COLOR_TEXT,
        ).move_to(sub_bg.get_center())
        sub_group = m.VGroup(sub_bg, sub_text)

        def update_sub(new_string: str, run_time: float = 0.5) -> None:
            """Smoothly morph bottom subtitles without dropping font size."""
            nonlocal sub_text
            new_text_mobj = m.Text(
                new_string,
                font_size=28,
                color=COLOR_TEXT,
            ).move_to(sub_bg.get_center())
            self.play(m.ReplacementTransform(sub_text, new_text_mobj), run_time=run_time)
            sub_text = new_text_mobj

        def update_step(new_step_str: str, stroke_color: str = "#F59E0B", text_color: str = "#FDE047", run_time: float = 0.5) -> None:
            """Update the top step indicator badge."""
            nonlocal step_label, step_bg
            new_label = m.Text(
                new_step_str,
                font_size=28,
                weight="BOLD",
                color=text_color,
            ).move_to([0, 4.15, 0])
            new_bg = m.RoundedRectangle(
                corner_radius=0.24,
                width=max(4.4, new_label.width + 0.9),
                height=0.64,
                fill_color=COLOR_CARD,
                fill_opacity=0.9,
                stroke_color=stroke_color,
                stroke_width=1.5,
            ).move_to([0, 4.15, 0])
            self.play(
                m.ReplacementTransform(step_bg, new_bg),
                m.ReplacementTransform(step_label, new_label),
                run_time=run_time,
            )
            step_bg = new_bg
            step_label = new_label

        # ==========================================
        # SCENE 1: The Hook (0.00s - 5.40s)
        # ==========================================
        eq1 = build_equation("2", "x", "+", "3", "=", "11", font_size=74).move_to([0, 1.4, 0])

        self.play(
            m.FadeIn(header_group, shift=m.DOWN * 0.3),
            m.FadeIn(step_group, shift=m.DOWN * 0.2),
            m.FadeIn(sub_group, shift=m.UP * 0.3),
            run_time=1.0,
        )
        self.play(m.Write(eq1), run_time=1.5)
        # Highlight x in cyan
        self.play(m.Indicate(eq1[1], scale_factor=1.4, color=COLOR_VAR), run_time=1.0)
        self.play(m.Circumscribe(eq1, color=COLOR_ACCENT, buff=0.22), run_time=1.0)
        self.wait(0.9)

        # ===================================================
        # SCENE 2: Understanding Linear Equations (5.4s - 12.4s)
        # ===================================================
        update_step("DEGREE = 1", stroke_color=COLOR_VAR, text_color=COLOR_VAR, run_time=0.6)
        update_sub("Highest power of x is one!", run_time=0.6)

        brace = m.Brace(eq1[1], direction=m.UP, color=COLOR_VAR, buff=0.35)
        power_tag = m.Text("Power = 1", font_size=30, weight="BOLD", color=COLOR_VAR).next_to(brace, m.UP, buff=0.15)
        power_group = m.VGroup(brace, power_tag)

        self.play(m.Create(brace), m.Write(power_tag), run_time=1.2)
        self.play(m.Indicate(power_tag, scale_factor=1.2, color=COLOR_NUM), run_time=1.0)
        self.wait(1.6)
        self.play(m.FadeOut(power_group), run_time=1.0)
        self.wait(1.0)

        # ===================================================
        # SCENE 3: Subtract 3 from Both Sides (12.4s - 24.4s)
        # ===================================================
        update_step("STEP 1: SUBTRACT 3", stroke_color="#F97316", text_color="#FB923C", run_time=0.6)
        update_sub("Subtract 3 from both sides", run_time=0.6)

        scale_rig, left_pos, right_pos = build_balance_scale(center=m.DOWN * 2.4, width=4.8)
        left_weight = m.MathTex("2x+3", font_size=38, color=COLOR_TEXT).next_to(left_pos, m.UP, buff=0.12)
        right_weight = m.MathTex("11", font_size=38, color=COLOR_NUM).next_to(right_pos, m.UP, buff=0.12)
        scale_all = m.VGroup(scale_rig, left_weight, right_weight)

        self.play(m.FadeIn(scale_all, shift=m.UP * 0.4), run_time=1.3)

        # Expand equation: 2x + 3 - 3 = 11 - 3
        eq2 = build_equation("2", "x", "+", "3", "-", "3", "=", "11", "-", "3", font_size=66).move_to([0, 1.4, 0])
        eq2[4].set_color(COLOR_OP)
        eq2[5].set_color(COLOR_OP)
        eq2[8].set_color(COLOR_OP)
        eq2[9].set_color(COLOR_OP)

        self.play(m.TransformMatchingTex(eq1, eq2), run_time=1.5)

        # Cancellation emphasis: highlight +3 and -3 in cancellation red with label above
        cancel_label = m.Text(
            "= 0 (Cancels)",
            font_size=30,
            weight="BOLD",
            color=COLOR_CANCEL,
        ).next_to(eq2, m.UP, buff=0.35)

        self.play(
            m.FadeToColor(eq2[2:6], color=COLOR_CANCEL),
            m.Write(cancel_label),
            run_time=1.0,
        )
        update_sub("+3 and -3 cancel to zero!", run_time=0.6)

        # Transform to 2x = 8
        eq3 = build_equation("2", "x", "=", "8", font_size=74).move_to([0, 1.4, 0])
        new_left_wt = m.MathTex("2x", font_size=38, color=COLOR_VAR).next_to(left_pos, m.UP, buff=0.12)
        new_right_wt = m.MathTex("8", font_size=38, color=COLOR_NUM).next_to(right_pos, m.UP, buff=0.12)

        self.play(
            m.FadeOut(cancel_label),
            m.TransformMatchingTex(eq2, eq3),
            m.ReplacementTransform(left_weight, new_left_wt),
            m.ReplacementTransform(right_weight, new_right_wt),
            run_time=1.6,
        )
        self.play(m.Circumscribe(eq3, color=COLOR_NUM, buff=0.2), run_time=1.0)
        self.wait(1.0)
        self.play(m.FadeOut(m.VGroup(scale_rig, new_left_wt, new_right_wt)), run_time=1.0)
        self.wait(0.8)

        # ===================================================
        # SCENE 4: Divide Both Sides by 2 (24.4s - 34.8s)
        # ===================================================
        update_step("STEP 2: DIVIDE BY 2", stroke_color=COLOR_ACCENT, text_color=COLOR_ACCENT, run_time=0.6)
        update_sub("Divide both sides by 2", run_time=0.6)

        # Equation: \frac{2x}{2} = \frac{8}{2}
        eq4 = m.MathTex(r"\frac{2x}{2}", "=", r"\frac{8}{2}", font_size=72).move_to([0, 1.4, 0])
        eq4[0].set_color(COLOR_VAR)
        eq4[1].set_color(COLOR_EQUAL)
        eq4[2].set_color(COLOR_NUM)

        self.play(m.TransformMatchingTex(eq3, eq4), run_time=1.4)
        self.wait(0.8)

        # Simplify to x = 4
        update_sub("Result: x = 4!", run_time=0.6)
        eq5 = m.MathTex("x", "=", "4", font_size=88).move_to([0, 1.4, 0])
        eq5[0].set_color(COLOR_VAR)
        eq5[1].set_color(COLOR_EQUAL)
        eq5[2].set_color(COLOR_RESULT)

        self.play(m.TransformMatchingTex(eq4, eq5), run_time=1.4)

        # Solution reveal
        answer_box = m.SurroundingRectangle(
            eq5,
            color=COLOR_RESULT,
            corner_radius=0.18,
            buff=0.32,
            stroke_width=3,
        )
        answer_tag = m.Text(
            "SOLUTION",
            font_size=30,
            weight="BOLD",
            color=COLOR_RESULT,
        ).next_to(answer_box, m.UP, buff=0.16)
        solution_group = m.VGroup(answer_box, answer_tag)

        self.play(m.Create(answer_box), m.FadeIn(answer_tag, shift=m.DOWN * 0.1), run_time=1.2)
        self.play(m.Indicate(eq5[2], scale_factor=1.3, color=COLOR_RESULT), run_time=1.0)
        self.wait(1.8)
        self.play(m.FadeOut(solution_group), run_time=1.0)

        # ===================================================
        # SCENE 5: Verify the Answer (34.8s - 44.8s)
        # ===================================================
        update_step("VERIFY ANSWER", stroke_color=COLOR_RESULT, text_color=COLOR_RESULT, run_time=0.6)
        update_sub("Verify: Substitute x = 4", run_time=0.6)

        # Substitution: 2(4) + 3 = 11
        check1 = m.MathTex("2", "(4)", "+", "3", "=", "11", font_size=68).move_to([0, 1.4, 0])
        check1[0].set_color(COLOR_NUM)
        check1[1].set_color(COLOR_RESULT)
        check1[2].set_color(COLOR_OP)
        check1[3].set_color(COLOR_NUM)
        check1[4].set_color(COLOR_EQUAL)
        check1[5].set_color(COLOR_NUM)

        self.play(m.ReplacementTransform(eq5, check1), run_time=1.4)
        self.wait(0.6)

        # 8 + 3 = 11
        update_sub("2(4) becomes 8 + 3 = 11", run_time=0.6)
        check2 = m.MathTex("8", "+", "3", "=", "11", font_size=68).move_to([0, 1.4, 0])
        check2[0].set_color(COLOR_NUM)
        check2[1].set_color(COLOR_OP)
        check2[2].set_color(COLOR_NUM)
        check2[3].set_color(COLOR_EQUAL)
        check2[4].set_color(COLOR_NUM)

        self.play(m.TransformMatchingTex(check1, check2), run_time=1.3)
        self.wait(0.5)

        # 11 = 11 (Both sides match!)
        update_sub("11 = 11! Both sides match", run_time=0.6)
        check3 = m.MathTex("11", "=", "11", font_size=76).move_to([0, 1.4, 0])
        check3.set_color(COLOR_RESULT)

        check_badge = m.RoundedRectangle(
            corner_radius=0.18,
            width=4.0,
            height=0.78,
            fill_color="#064E3B",
            fill_opacity=0.9,
            stroke_color=COLOR_RESULT,
            stroke_width=2,
        ).move_to([0, 0.15, 0])
        check_msg = m.Text(
            "VERIFIED TRUE",
            font_size=28,
            weight="BOLD",
            color=COLOR_RESULT,
        ).move_to(check_badge.get_center())
        verified_group = m.VGroup(check_badge, check_msg)

        self.play(m.TransformMatchingTex(check2, check3), run_time=1.2)
        self.play(m.FadeIn(verified_group, shift=m.UP * 0.2), run_time=0.8)
        self.play(m.Indicate(check3, scale_factor=1.2, color=COLOR_RESULT), run_time=0.9)
        self.wait(0.5)
        self.play(m.FadeOut(m.VGroup(check3, verified_group)), run_time=0.8)

        # ===================================================
        # SCENE 6: Key Takeaway (44.8s - 52.2s)
        # ===================================================
        update_step("GOLDEN RULE", stroke_color="#F59E0B", text_color="#FDE047", run_time=0.5)
        update_sub("Whatever you do to one side...", run_time=0.5)

        rule_card_bg = m.RoundedRectangle(
            corner_radius=0.25,
            width=6.6,
            height=2.3,
            fill_color="#1E293B",
            fill_opacity=0.95,
            stroke_color="#F59E0B",
            stroke_width=2,
        ).move_to([0, 1.4, 0])

        rule_t1 = m.Text("THE GOLDEN RULE", font_size=30, weight="BOLD", color="#FDE047")
        rule_t2 = m.Text("Whatever you do to one side,", font_size=28, color=COLOR_TEXT)
        rule_t3 = m.Text("DO TO THE OTHER SIDE!", font_size=28, weight="BOLD", color=COLOR_ACCENT)
        rule_lines = m.VGroup(rule_t1, rule_t2, rule_t3).arrange(m.DOWN, buff=0.18).move_to(rule_card_bg.get_center())
        rule_card = m.VGroup(rule_card_bg, rule_lines)

        takeaway_scale, t_left, t_right = build_balance_scale(center=m.DOWN * 2.4, width=4.8)
        left_op = m.MathTex("-3", font_size=38, color="#FB923C").next_to(t_left, m.UP, buff=0.12)
        right_op = m.MathTex("-3", font_size=38, color="#FB923C").next_to(t_right, m.UP, buff=0.12)
        scale_takeaway_group = m.VGroup(takeaway_scale, left_op, right_op)

        self.play(m.FadeIn(rule_card, shift=m.DOWN * 0.2), m.FadeIn(scale_takeaway_group, shift=m.UP * 0.2), run_time=1.2)
        self.play(m.Indicate(rule_lines[2], scale_factor=1.1, color="#38BDF8"), run_time=1.0)
        self.wait(2.2)
        self.play(m.FadeOut(m.VGroup(rule_card, scale_takeaway_group)), run_time=1.0)

        # ===================================================
        # SCENE 7: Audience Challenge (52.2s - 60.0s)
        # ===================================================
        update_step("YOUR TURN!", stroke_color=COLOR_VAR, text_color=COLOR_VAR, run_time=0.5)
        update_sub("Can YOU solve 3x - 2 = 10?", run_time=0.5)

        # Challenge equation: 3x - 2 = 10
        chal_eq = build_equation("3", "x", "-", "2", "=", "10", font_size=76).move_to([0, 1.8, 0])
        chal_box = m.SurroundingRectangle(
            chal_eq,
            color=COLOR_VAR,
            corner_radius=0.18,
            buff=0.3,
            stroke_width=2.5,
        )

        cta_card_bg = m.RoundedRectangle(
            corner_radius=0.22,
            width=6.4,
            height=1.8,
            fill_color="#1E293B",
            fill_opacity=0.95,
            stroke_color="#F43F5E",
            stroke_width=2,
        ).move_to([0, -0.6, 0])

        cta_q = m.Text("Can YOU solve it?", font_size=32, weight="BOLD", color="#FFFFFF")
        cta_action = m.Text("Comment your answer below! 👇", font_size=28, weight="BOLD", color="#FB7185")
        cta_texts = m.VGroup(cta_q, cta_action).arrange(m.DOWN, buff=0.2).move_to(cta_card_bg.get_center())
        cta_group = m.VGroup(cta_card_bg, cta_texts)

        self.play(m.Write(chal_eq), run_time=1.3)
        self.play(m.Create(chal_box), run_time=0.8)
        self.play(m.FadeIn(cta_group, shift=m.UP * 0.3), run_time=1.1)
        self.play(m.Indicate(cta_texts[1], scale_factor=1.15, color="#F43F5E"), run_time=1.0)
        self.play(m.Circumscribe(chal_eq, color=COLOR_NUM, buff=0.25), run_time=1.2)
        self.wait(3.0)
        # End Scene 7: t = 60.0s
