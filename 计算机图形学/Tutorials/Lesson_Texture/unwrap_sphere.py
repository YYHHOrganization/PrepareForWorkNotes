from manimlib import *

class UnWrap_Sphere(Scene):
    def translateToUVSpace(self, points, sphere_center, sphere_radius):  # 球面坐标转换到UV空间的公式
        # uv_coordinates = []
        # for point in points:
        #     n = normalize(point - sphere_center)
        #     u = np.arctan2(n[0], n[2]) / (2 * np.pi) + 0.5
        #     v = n[1] * 0.5 + 0.5
        #     uv_coordinates.append([u, v])
        #     # print(u, v)
        # return uv_coordinates
        """
                将球面上的点转换为 UV 坐标

                :param points: 一个 N x 3 的数组，每一行都是一个点的 (x, y, z) 坐标
                :param sphere_center: 球心的坐标 (x, y, z)
                :return: 一个 N x 2 的数组，每一行对应于 (u, v) 坐标
                """
        uv_coords = []

        for point in points:
            # 将点转换为相对于球心的向量
            relative_point = point - sphere_center
            # 计算向量的长度
            length = np.linalg.norm(relative_point)
            # 确保点在球面上，即长度应该等于半径
            if not np.isclose(length, sphere_radius):
                raise ValueError("The point is not on the sphere surface.")

            # 计算 UV 值
            u = math.atan2(relative_point[1], relative_point[0])  # atan2(y, x)
            v = math.acos(-relative_point[2] / sphere_radius)  # acos(z/radius)
            # 归一化 (u, v)
            u_normalized = (u + math.pi) / (2 * math.pi)  # 将 u 从 [-π, π] 转换到 [0, 1]
            v_normalized = v / math.pi  # 将 v 从 [0, π] 转换到 [0, 1]
            # print(u_normalized, v_normalized)

            uv_coords.append([1 - u_normalized, v_normalized])
            # print(u_normalized, v_normalized)

        return np.array(uv_coords)


    def construct(self):
        surface_text = Text("Unwrap Sphere")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)

        frame = self.camera.frame

        frame.set_euler_angles(
            theta=120 * DEGREES,
            phi=60 * DEGREES,
        )

        # (0,0,10) 绘制一个point
        point = Dot(np.array([0, 0, 1]), color=RED)
        self.add(point)
        self.wait(0.1)
        self.play(FadeOut(point))

        # 绘制一下XYZ这三个轴
        axes = ThreeDAxes()
        self.add(axes)
        # 显示轴的文字
        axes_labels = axes.get_axis_labels()
        self.add(axes_labels)
        self.play(Write(axes_labels))

        self.add(surface_text)
        self.wait(0.1)
        day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        sphere_radius = 2.5
        sphere = Sphere(radius=sphere_radius)
        # sphere.rotate(PI / 2, RIGHT)
        # sphere.rotate(PI / 2, UP)
        # sphere.shift(4 * LEFT)
        surfaces = [
            TexturedSurface(surface, day_texture)
            for surface in [sphere]
        ]
        for mob in surfaces:
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=1)

        # Set perspective
        # frame = self.camera.frame

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=1),
        )

        self.add(surface)
        self.wait(0.1)

        image = ImageMobject(day_texture)
        image.set_height(3)
        image.shift(LEFT* 4 + DOWN * 2)
        # image.to_corner(UR + LEFT * 20 - 2 * UP)
        image_uv_start = image.get_corner(DL)
        self.add(image)
        image.fix_in_frame()

        # show points on sphere
        sphere_center = sphere.get_center()
        dot = Dot(sphere_center, fill_color=RED, radius=0.05)
        # dot.fix_in_frame()
        self.add(dot)


        theta_show_num = 5
        phi_show_num = 5
        points=[]
        thetas=[]
        phis=[]
        # 用球面坐标点出theta和phi方向上下的点
        for i in range(-theta_show_num, theta_show_num + 1):
            theta = i * TAU * 0.3 / theta_show_num
            for j in range(0, phi_show_num + 1):
                phi = j * TAU * 0.25/ phi_show_num
                point = sphere_center + sphere_radius * np.array([
                    np.sin(phi) * np.cos(theta),
                    np.sin(phi) * np.sin(theta),
                    np.cos(phi)
                ])
                # 弧度值转角度值
                thetas.append(theta // DEGREES)
                phis.append(phi // DEGREES)
                points.append(point)

        uv_coordinates = self.translateToUVSpace(points, sphere_center, sphere_radius)
        show_text = Text("UV Space")
        show_text.to_corner(DR)
        show_text.fix_in_frame()
        self.add(show_text)

        index = 0
        for point in points:
            dot = Dot(point, fill_color=RED, radius=0.05)
            self.add(dot)
            # self.play(FadeIn(dot))
            self.play(Indicate(dot))
            # 加一个tex指示index
            index_text = Text(str(index), font_size=10)
            index_text.next_to(dot, RIGHT)
            self.add(index_text)
            # dot.fix_in_frame()
            # draw arrow
            arrow = Arrow(sphere_center, point, stroke_color=BLUE)
            # arrow.fix_in_frame()
            self.add(arrow)
            self.play(ShowCreation(arrow))
            self.play(FadeOut(arrow))

            thetaAndPhiText = Text("Theta: {:.2f} \n Phi: {:.2f}".format(thetas[index], phis[index]), font_size=25)
            thetaAndPhiText.fix_in_frame()
            thetaAndPhiText.next_to(dot, RIGHT)
            # thetaAndPhiText.rotate(PI / 2, axis=LEFT, about_point=thetaAndPhiText.get_center())
            self.add(thetaAndPhiText)
            self.play(FadeIn(thetaAndPhiText))

            # self.play(FadeIn(dot))

            self.play(FadeOut(thetaAndPhiText))
            uv_dot = Dot(image_uv_start + np.array([uv_coordinates[index][0] * image.get_width(), uv_coordinates[index][1] * image.get_height(), 0]), fill_color=YELLOW, radius=0.05)
            # self.play(dot.animate.move_to(image_uv_start + np.array([uv_coordinates[index][0] * image.get_width(), uv_coordinates[index][1] * image.get_height(), 0])))
            self.add(uv_dot)
            self.play(FadeIn(uv_dot))
            self.play(Indicate(uv_dot))
            uv_dot.fix_in_frame()
            uv_index_text = Text(str(index), font_size=10)
            uv_index_text.next_to(uv_dot, UP)
            uv_index_text.fix_in_frame()
            self.add(uv_index_text)
            index += 1
            self.wait(0.1)
