import numpy as np
import manimgx as m


class SolarSystem(m.ThreeDScene):
    def construct(self) -> None:
        # Initial camera orientation: angled perspective
        self.set_camera_orientation(phi=68 * m.DEGREES, theta=-55 * m.DEGREES, zoom=0.92)

        # Space lighting: Sun at origin radiates outward onto all planetary surfaces
        sun_point_light = m.PointLight(location=m.ORIGIN, color="#FFF8E7", intensity=6.5, radius=30.0)
        sun_dir_light = m.SunLight(location=m.UP + 2 * m.OUT, color=m.WHITE, intensity=0.35)
        ambient_light = m.AmbientLight(color=m.WHITE, intensity=0.22)
        self.add(sun_point_light, sun_dir_light, ambient_light)

        # Distant background stars (avoiding the title overlay corner)
        np.random.seed(42)
        star_positions = (np.random.rand(110, 3) - 0.5) * 36
        for p in star_positions:
            if np.linalg.norm(p[:2]) < 8.2:
                p[:2] += np.sign(p[:2] + 1e-5) * 8.2
            if p[0] < -2.5 and p[1] > 1.5:
                p[1] -= 3.2

        stars = m.Group(*[
            m.Dot(
                point=p,
                radius=float(np.random.uniform(0.015, 0.035)),
                color=m.WHITE,
                fill_opacity=float(np.random.uniform(0.35, 0.85)),
            )
            for p in star_positions
        ])
        self.add(stars)

        # Fixed in-frame UI HUD Header (Top-Left)
        title = m.Text("THE SOLAR SYSTEM", font_size=26, weight="BOLD", color="#FFD54F")
        subtitle = m.Text("3D Planetary Orbits Simulation", font_size=14, color="#B0BEC5")
        header = m.VGroup(title, subtitle).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.08)
        header.to_corner(m.UL, buff=0.45)

        # Fixed in-frame Info Box (Bottom-Right)
        info_card_title = m.Text("SYSTEM OVERVIEW", font_size=16, weight="BOLD", color="#FFD54F")
        info_card_desc = m.Text("Sun • 8 Planets • Asteroid Belt", font_size=13, color="#ECEFF1")
        info_card = m.VGroup(info_card_title, info_card_desc).arrange(m.DOWN, aligned_edge=m.RIGHT, buff=0.06)
        info_card.to_corner(m.DR, buff=0.45)

        self.add_fixed_in_frame_mobjects(header, info_card)

        # The Sun (radiant glowing core + coronal envelopes)
        sun_core = m.Sphere(
            center=m.ORIGIN,
            radius=0.60,
            resolution=(36, 36),
            stroke_width=0,
        ).set_color("#FFF59D").set_fill_by_checkerboard("#FFF59D", "#FFD54F", opacity=1.0)
        sun_core.set_material(m.Material(metallic=0.0, roughness=0.9))

        corona_inner = m.Sphere(
            center=m.ORIGIN,
            radius=0.72,
            resolution=(28, 28),
            stroke_width=0,
        ).set_color("#FFB300").set_fill_by_checkerboard("#FFB300", "#FFB300", opacity=0.35)

        corona_outer = m.Sphere(
            center=m.ORIGIN,
            radius=0.85,
            resolution=(24, 24),
            stroke_width=0,
        ).set_color("#FF8F00").set_fill_by_checkerboard("#FF8F00", "#FF8F00", opacity=0.15)

        sun_group = m.Group(sun_core, corona_inner, corona_outer)

        # Planetary data:
        # (name, orbit_radius, sphere_radius, speed, base_color, accent_color, start_angle)
        planets_specs = [
            ("Mercury", 1.25, 0.075, 2.3, "#9E9E9E", "#BDBDBD", 0.4),
            ("Venus",   1.75, 0.115, 1.7, "#E5C158", "#F5D77F", 1.9),
            ("Earth",   2.40, 0.135, 1.25, "#1E88E5", "#42A5F5", 3.4),
            ("Mars",    3.10, 0.095, 0.95, "#E53935", "#EF5350", 4.9),
            ("Jupiter", 4.10, 0.270, 0.65, "#D7CCC8", "#A1887F", 1.1),
            ("Saturn",  5.15, 0.220, 0.48, "#FFE082", "#FFD54F", 2.6),
            ("Uranus",  6.10, 0.165, 0.35, "#80DEEA", "#4DD0E1", 5.2),
            ("Neptune", 7.00, 0.155, 0.25, "#3949AB", "#5C6BC0", 3.9),
        ]

        orbits = m.Group()
        planet_mobjects = []
        planet_data = []

        time_tracker = m.ValueTracker(0.0)

        for name, r_orbit, r_planet, speed, c_base, c_accent, theta0 in planets_specs:
            # Orbital track in the ecliptic plane
            orbit_circle = m.Circle(
                radius=r_orbit,
                color=m.GREY_C,
                stroke_width=1.0,
                stroke_opacity=0.28,
            )
            orbits.add(orbit_circle)

            # Planet sphere with physical material shading
            p_sphere = m.Sphere(
                radius=r_planet,
                resolution=(24, 24),
                stroke_width=0,
            ).set_color(c_base).set_fill_by_checkerboard(c_base, c_accent, opacity=1.0)
            p_sphere.set_material(m.Material(metallic=0.1, roughness=0.55))

            if name == "Saturn":
                # Saturn's rings (tilted annulus orbiting with Saturn)
                ring = m.Annulus(
                    inner_radius=r_planet * 1.45,
                    outer_radius=r_planet * 2.50,
                    color="#FFE082",
                    fill_opacity=0.75,
                    stroke_width=0,
                )
                ring.rotate(27 * m.DEGREES, axis=m.RIGHT)
                p_mob = m.Group(p_sphere, ring)
            else:
                p_mob = p_sphere

            # Initial position
            init_x = r_orbit * np.cos(theta0)
            init_y = r_orbit * np.sin(theta0)
            p_mob.move_to(np.array([init_x, init_y, 0.0]))

            planet_mobjects.append(p_mob)
            planet_data.append((p_mob, r_orbit, speed, theta0))

        # Earth's Moon
        earth_mob = planet_mobjects[2]
        moon = m.Sphere(
            radius=0.038,
            resolution=(16, 16),
            stroke_width=0,
        ).set_color("#E0E0E0").set_fill_by_checkerboard("#E0E0E0", "#EEEEEE", opacity=1.0)
        moon.set_material(m.Material(metallic=0.05, roughness=0.8))
        moon_dist = 0.30
        moon_speed = 5.5
        moon.move_to(earth_mob.get_center() + np.array([moon_dist, 0.0, 0.0]))

        # The Asteroid Belt between Mars (3.10) and Jupiter (4.10)
        num_asteroids = 100
        np.random.seed(101)
        asteroid_radii = np.random.uniform(3.45, 3.82, num_asteroids)
        asteroid_thetas = np.random.uniform(0, 2 * np.pi, num_asteroids)
        asteroid_zs = np.random.uniform(-0.10, 0.10, num_asteroids)
        asteroid_speeds = np.random.uniform(0.72, 0.86, num_asteroids)
        asteroid_colors = ["#8D6E63", "#A1887F", "#9E9E9E", "#78909C"]

        asteroid_dots = []
        asteroid_data = []
        for i in range(num_asteroids):
            r_ast = asteroid_radii[i]
            th_ast = asteroid_thetas[i]
            z_ast = asteroid_zs[i]
            sp_ast = asteroid_speeds[i]
            c_ast = asteroid_colors[i % len(asteroid_colors)]

            ast_pos = np.array([r_ast * np.cos(th_ast), r_ast * np.sin(th_ast), z_ast])
            ast_dot = m.Dot(
                point=ast_pos,
                radius=float(np.random.uniform(0.018, 0.028)),
                color=c_ast,
                fill_opacity=float(np.random.uniform(0.5, 0.85)),
            )
            asteroid_dots.append(ast_dot)
            asteroid_data.append((ast_dot, r_ast, sp_ast, th_ast, z_ast))

        asteroid_group = m.Group(*asteroid_dots)

        # Dynamic motion updater
        def update_system(dt: float) -> None:
            t = time_tracker.get_value()
            # Update planets
            for mob, r_orb, spd, th0 in planet_data:
                angle = th0 + spd * t
                mob.move_to(np.array([r_orb * np.cos(angle), r_orb * np.sin(angle), 0.0]))

            # Update moon relative to earth
            m_angle = moon_speed * t
            moon.move_to(earth_mob.get_center() + np.array([
                moon_dist * np.cos(m_angle),
                moon_dist * np.sin(m_angle),
                0.04 * np.sin(m_angle),
            ]))

            # Update asteroids
            for dot, r_ast, sp_ast, th_ast, z_ast in asteroid_data:
                a_angle = th_ast + sp_ast * t
                dot.move_to(np.array([r_ast * np.cos(a_angle), r_ast * np.sin(a_angle), z_ast]))

        system_group = m.Group(*planet_mobjects, moon, asteroid_group)
        system_group.add_updater(lambda mob, dt: update_system(dt))

        # Helper to smoothly change info card
        def change_info(title_text: str, desc_text: str) -> m.AnimationGroup:
            new_title = m.Text(title_text, font_size=16, weight="BOLD", color="#FFD54F")
            new_desc = m.Text(desc_text, font_size=13, color="#ECEFF1")
            new_card = m.VGroup(new_title, new_desc).arrange(m.DOWN, aligned_edge=m.RIGHT, buff=0.06)
            new_card.to_corner(m.DR, buff=0.45)
            anim = m.Transform(info_card, new_card)
            return anim

        # --- CINEMATIC ANIMATION TIMELINE ---
        # 1. Radiant birth of the Sun
        self.play(m.GrowFromCenter(sun_group), run_time=1.5)

        # 2. Orbits and Asteroid Belt sweep outward
        self.play(
            m.LaggedStart(*[m.Create(orb) for orb in orbits], lag_ratio=0.10),
            m.FadeIn(asteroid_group),
            run_time=2.0,
        )

        # 3. Celestial bodies appear in starting alignment
        self.play(
            m.LaggedStart(
                *[m.FadeIn(p, scale=0.6) for p in planet_mobjects],
                m.FadeIn(moon, scale=0.6),
                lag_ratio=0.08,
            ),
            run_time=1.8,
        )

        # 4. Planetary revolution begins; camera gently sweeps
        self.begin_ambient_camera_rotation(rate=0.12)
        self.move_camera(
            phi=62 * m.DEGREES,
            theta=-15 * m.DEGREES,
            zoom=1.05,
            added_anims=[
                time_tracker.animate.set_value(5.0),
                change_info("ORBITAL DYNAMICS", "Keplerian motion: closer orbits travel faster"),
            ],
            run_time=4.5,
            rate_func=m.linear,
        )

        # 5. Flyby towards Earth & Moon system
        # Calculate Earth's quadrant around t=8.5s
        self.move_camera(
            phi=55 * m.DEGREES,
            theta=40 * m.DEGREES,
            frame_center=np.array([1.2, -1.0, 0.0]),
            zoom=1.65,
            added_anims=[
                time_tracker.animate.set_value(10.0),
                change_info("INNER SYSTEM: EARTH", "Habitable zone • 1.00 AU • Orbit: 365.25 d"),
            ],
            run_time=5.0,
            rate_func=m.linear,
        )

        # 6. Swoop to the Gas Giants: Saturn and its rings
        self.move_camera(
            phi=72 * m.DEGREES,
            theta=95 * m.DEGREES,
            frame_center=np.array([-2.2, 1.8, 0.0]),
            zoom=1.40,
            added_anims=[
                time_tracker.animate.set_value(15.0),
                change_info("GAS GIANTS: SATURN", "Prominent ice rings • 9.58 AU • Orbit: 29.5 y"),
            ],
            run_time=5.0,
            rate_func=m.linear,
        )

        # 7. Pull back to grand panoramic view of the entire solar system
        self.move_camera(
            phi=70 * m.DEGREES,
            theta=140 * m.DEGREES,
            frame_center=m.ORIGIN,
            zoom=0.88,
            added_anims=[
                time_tracker.animate.set_value(20.0),
                change_info("THE SOLAR SYSTEM", "Complete 8-planet planetary architecture"),
            ],
            run_time=5.0,
            rate_func=m.linear,
        )

        # 8. Final smooth orbit revolution to close
        self.play(
            time_tracker.animate.set_value(22.0),
            run_time=2.0,
            rate_func=m.linear,
        )
        self.wait(1.0)
