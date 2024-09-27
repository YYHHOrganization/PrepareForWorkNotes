from manimlib import *

class Blinn_Phong_Pic1(Scene):
    def construct(self):
        surface_text = Text("Blinn Phong Model")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)
        line = Line(LEFT * 5 + DOWN * 2, RIGHT * 5 + DOWN * 2)
        line.set_color(WHITE)
        self.play(ShowCreation(line))
        sun = Circle(radius=0.1)
        sun.set_color(YELLOW)
        sun_pos = 2 * UP + 2 * RIGHT
        sun.move_to(sun_pos)
        self.add(sun)
        self.play(FadeIn(sun))
        sun_text = Text("Sun", font_size=20)
        sun_text.next_to(sun, RIGHT)
        self.play(FadeIn(sun_text))
        self.add(sun_text)

        camera_pos = [-5, 2, 0]
        camera = Circle(radius=0.1)
        camera.set_color(PURPLE)
        camera.move_to(camera_pos)
        self.add(camera)
        self.play(FadeIn(camera))
        camera_text = Text("Camera", font_size=20)
        camera_text.next_to(camera, RIGHT)
        self.play(FadeIn(camera_text))
        self.add(camera_text)

        # render pos
        render_pos = [0, 0, 0] + DOWN * 2
        render = Circle(radius=0.1)
        render.set_color(GREEN)
        render.move_to(render_pos)
        self.add(render)
        self.play(FadeIn(render))

        # arrow:render->sun
        arrow1 = Arrow(render_pos + DOWN * 0.05, sun_pos, stroke_color=YELLOW)
        light_direction = normalize(sun_pos - render_pos)
        self.add(arrow1)
        self.play(ShowCreation(arrow1))
        light_direction_text = Text("Light Direction", font_size=20)
        light_direction_text.next_to(arrow1, UP)
        self.play(FadeIn(light_direction_text))
        self.add(light_direction_text)

        # arrow:render->camera
        arrow2 = Arrow(render_pos + DOWN * 0.05, camera_pos, stroke_color=PURPLE)
        view_direction = normalize(camera_pos - render_pos)
        self.add(arrow2)
        self.play(ShowCreation(arrow2))
        camera_direction_text = Text("Camera Direction", font_size=20)
        camera_direction_text.next_to(arrow2, LEFT)
        camera_direction_text.move_to(camera_direction_text.get_center() + RIGHT)
        self.play(FadeIn(camera_direction_text))
        self.add(camera_direction_text)


        # normal
        normal_vector = DashedLine(render_pos, render_pos + 4.3 * UP, color=BLUE)
        normal_vector_value = normalize(UP)
        self.add(normal_vector)
        self.play(ShowCreation(normal_vector))
        normal_text = Text("Normal Vector", font_size=20)
        normal_text.next_to(normal_vector, UP)
        self.play(FadeIn(normal_text))
        self.add(normal_text)
        self.wait(1)

        # now calculate lambert
        self.play(FadeOut(surface_text))
        lambert_text = Text("Lambert Part: Lambert = max(0, N dot L)")
        lambert_text.fix_in_frame()
        lambert_text.to_edge(UP)
        self.play(FadeIn(lambert_text))
        self.add(lambert_text)
        self.wait(0.1)

        # 高亮显示normal_vector和light_direction
        self.play(Indicate(normal_vector))
        self.play(Indicate(arrow1))
        self.wait(0.1)

        # angle between normal and light
        end_angle = angle_of_vector(normal_vector_value)
        # print(end_angle)
        start_angle = angle_of_vector(light_direction)
        angleShow = Arc(start_angle, end_angle - start_angle, radius=0.5, color=RED, arc_center=render_pos)
        self.add(angleShow)
        self.play(ShowCreation(angleShow))

        self.play(FadeOut(lambert_text))
        self.play(FadeOut(angleShow))
        self.wait(1)

        phong_text = Text("Phong Part: Phong = max(0, R dot V)^n")
        phong_text.fix_in_frame()
        phong_text.to_edge(UP)
        self.play(FadeIn(phong_text))
        self.add(phong_text)
        self.wait(0.1)
        # phong shading
        # 计算R向量
        reflect_vector = 2 * np.dot(normal_vector_value, light_direction) * normal_vector_value - light_direction
        reflect_arrow = Arrow(render_pos, render_pos + 4 * reflect_vector, stroke_color=RED)
        self.add(reflect_arrow)
        self.play(ShowCreation(reflect_arrow))
        reflect_text = Text("Reflect Vector", font_size=20)
        reflect_text.next_to(reflect_arrow, UP)
        self.play(FadeIn(reflect_text))
        self.add(reflect_text)
        # indicate reflect vector and view direction
        self.play(Indicate(reflect_arrow))
        self.play(Indicate(arrow2))
        self.wait(1)

        end_angle = angle_of_vector(view_direction)
        # print(end_angle)
        start_angle = angle_of_vector(reflect_vector)
        angleShow2 = Arc(start_angle, end_angle - start_angle, radius=0.5, color=RED, arc_center=render_pos)
        self.add(angleShow2)
        self.play(ShowCreation(angleShow2))
        self.play(FadeOut(angleShow2))

        self.wait(1)
        # blinn phong
        self.play(FadeOut(phong_text))
        blinn_phong_text = Text("Blinn Phong Part: Blinn Phong = max(0, N dot H)^n")
        blinn_phong_text.fix_in_frame()
        blinn_phong_text.to_edge(UP)
        self.play(FadeIn(blinn_phong_text))
        self.play(FadeOut(reflect_arrow))
        self.play(FadeOut(reflect_text))

        half_vector = normalize(view_direction + light_direction)
        half_arrow = Arrow(render_pos, render_pos + half_vector * 4, stroke_color=WHITE)
        self.add(half_arrow)
        self.play(ShowCreation(half_arrow))
        half_text = Text("Half Vector", font_size=20)
        half_text.next_to(half_arrow, UP)
        self.play(FadeIn(half_text))
        self.add(half_text)
        self.wait(1)
        # indicate
        self.play(Indicate(half_arrow))
        self.play(Indicate(normal_vector))
        self.wait(0.1)
        # arc
        end_angle = angle_of_vector(normal_vector_value)
        start_angle = angle_of_vector(half_vector)
        angleShow3 = Arc(start_angle, end_angle - start_angle, radius=0.5, color=RED, arc_center=render_pos)
        self.add(angleShow3)
        self.play(ShowCreation(angleShow3))
        self.wait(1)




class Blinn_Phong_Tutorial(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        surface_text = Text("Blinn Phong Interactive Scene")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)
        plane = Square3D(side_length=8)
        plane.set_color(WHITE)
        surfaces = [plane]

        # Set perspective
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=0 * DEGREES,
            phi=70 * DEGREES,
        )
        surface = surfaces[0]

        # self.play(
        #     FadeIn(surface),
        #     ShowCreation(surface, lag_ratio=0.01, run_time=1)
        # )
        self.add(surface)

        # Set light, 假装有一个Sphere表示光源
        light = Sphere(radius=0.1)
        light.set_color(YELLOW)
        light_pos = 2 * OUT + 2 * RIGHT
        light.move_to(light_pos)
        # 加一个text，表示是光源
        light_text = Text("Light Source", font_size=20)
        light_text.next_to(light, RIGHT)
        light_text.rotate(PI/2, axis=RIGHT)
        self.add(light)
        self.add(light_text)

        # draw the normal vector
        normal_vector = FillArrow(start=ORIGIN, end=ORIGIN + 2.0 * OUT, fill_color=BLUE, thickness=0.05)
        normal_vector.rotate(PI/2, axis=OUT)
        normal_text = Text("Normal Vector", font_size=20)
        normal_text.next_to(normal_vector, OUT)
        normal_text.rotate(PI/2, axis=RIGHT)
        self.add(normal_vector)
        self.add(normal_text)

        light_direction = FillArrow(start=ORIGIN, end=light_pos, fill_color=YELLOW, thickness=0.05)
        self.add(light_direction)

        camera_pos = [-2, -2, 3]
        camera_direction = FillArrow(start=ORIGIN, end=camera_pos, fill_color=PURPLE, thickness=0.05)
        self.add(camera_direction)


