import numpy as np
import manimgx as m


class SolarSystem(m.ThreeDScene):
    def construct(self) -> None:
        # Initial camera orientation: angled perspective
        self.set_camera_orientation(phi=68 * m.DEGREES, theta=-55 * m.DEGREES, zoom=0.95)

        # Space lighting: Sun at origin radiates outward onto all planetary surfaces
        sun_point_light = m.PointLight(location=m.ORIGIN, color="#FFF8E7", intensity=6.0, radius=28.0)
        sun_dir_light = m.SunLight(location=m.UP + 2 * m.OUT, color=m.WHITE, intensity=0.35)
        ambient_light = m.AmbientLight(color=m.WHITE, intensity=0.22)
        self.add(sun_point_light, sun_dir_light, ambient_light)

        # Distant background stars (avoiding the title overlay corner)
        np.random.seed(42)
        star_positions = (np.random.rand(100, 3) - 0.5) * 34
        for p in star_positions:
            # Keep stars clear of the ecliptic disk core
            if np.linalg.norm(p[:2]) < 8.2:
                p[:2] += np.sign(p[:2] + 1e-5) * 8.2
            # Keep stars clear of the top-left HUD corner
            if p[0] < -3.0 and p[1] > 1.8:
                p[1] -= 3.0

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

        # Fixed in-frame UI HUD
        title = m.Text("THE SOLAR SYSTEM", font_size=26, weight="BOLD", color="#FFD54F")
        subtitle = m.Text("3D Planetary Orbits Simulation", font_size=15, color="#B0BEC5")
        header = m.VGroup(title, subtitle).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.1)
        header.to_corner(m.UL, buff=0.45)
        self.add_fixed_in_frame_mobjects(header)

        # The Sun (radiant glowing core + soft coronal envelopes)
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

        # Dynamic motion updater
        def update_planets(dt: float) -> None:
            t = time_tracker.get_value()
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

        system_group = m.Group(*planet_mobjects, moon)
        system_group.add_updater(lambda mob, dt: update_planets(dt))

        # --- CINEMATIC ANIMATION TIMELINE ---
        # 1. Radiant birth of the Sun
        self.play(m.GrowFromCenter(sun_group), run_time=1.5)

        # 2. Orbits sweep outward
        self.play(
            m.LaggedStart(*[m.Create(orb) for orb in orbits], lag_ratio=0.12),
            run_time=2.0,
        )

        # 3. Celestial bodies appear in starting alignment
        self.play(
            m.LaggedStart(
                *[m.FadeIn(p, scale=0.6) for p in planet_mobjects],
                m.FadeIn(moon, scale=0.6),
                lag_ratio=0.10,
            ),
            run_time=2.0,
        )

        # 4. Planetary revolution begins; camera gently zooms and sweeps
        self.begin_ambient_camera_rotation(rate=0.14)
        self.move_camera(
            phi=60 * m.DEGREES,
            theta=-15 * m.DEGREES,
            zoom=1.1,
            added_anims=[time_tracker.animate.set_value(6.0)],
            run_time=5.0,
            rate_func=m.linear,
        )

        # 5. Wide panoramic perspective revealing the full solar system
        self.move_camera(
            phi=72 * m.DEGREES,
            theta=50 * m.DEGREES,
            zoom=0.88,
            added_anims=[time_tracker.animate.set_value(12.0)],
            run_time=5.0,
            rate_func=m.linear,
        )

        # 6. Smooth orbital continuation
        self.play(
            time_tracker.animate.set_value(14.0),
            run_time=2.0,
            rate_func=m.linear,
        )
        self.wait(1.0)
