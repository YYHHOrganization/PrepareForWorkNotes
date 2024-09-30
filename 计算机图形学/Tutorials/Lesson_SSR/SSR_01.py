from manimlib import *

class SSR_algo_1(Scene):
    def cal_ray_intersection_with_plane(self, ray_dir, plane_z):
        """
        计算射线与平面的交点
        :param ray_dir: 射线的方向
        :param plane_z: 平面的z坐标
        :return: 射线与平面的交点
        """
        # 射线方程：P = P0 + t * D
        # 平面方程：z = plane_z
        # 将射线方程代入平面方程，得到t
        ray = normalize(ray_dir)
        t = (plane_z - 0.0) / ray[1]
        return [ray[0] * t, ray[1] * t, ray[2] * t]

    def construct(self):
        # 创建底面四个顶点
        frame = self.camera.frame

        frame.set_euler_angles(
            theta=30* DEGREES,
            phi=60 * DEGREES,
        )
        # frame.shift(2 * RIGHT + 2 * UP)
        frame.set_field_of_view(PI / 10)
        frame.shift(2 * OUT + RIGHT)

        # 绘制一下XYZ这三个轴
        axes = ThreeDAxes(x_range=(0.0, 5.0, 1.0), y_range=(0.0, 5.0,1.0), z_range=(0.0, 5.0,1.0),height=5, width=5, depth=5, axis_config={"color": BLUE})
        self.add(axes)
        # 显示轴的文字
        axes_labels = axes.get_axis_labels()
        self.add(axes_labels)
        self.play(Write(axes_labels))

        # 一个坐标系，显示三个箭头，right(1,0,0), up(0,1,0),forward(0,0,1)
        # x_axis = FillArrow(np.array([0, 0, 0]), np.array([2, 0, 0]), fill_color=RED)
        # y_axis = FillArrow(np.array([0, 0, 0]), np.array([0, 2, 0]), fill_color=GREEN)
        # z_axis = FillArrow(np.array([0, 0, 0]), np.array([0, 0, 2]), fill_color=BLUE)
        # # right, up, forward label
        # x_text = Text("right", font_size=20)
        # x_text.next_to(x_axis.get_end(), RIGHT)
        # y_text = Text("up", font_size=20)
        # y_text.next_to(y_axis.get_end(), UP)
        # z_text = Text("forward", font_size=20)
        # z_text.next_to(z_axis.get_end(), RIGHT)
        # self.add(x_text)
        # self.add(y_text)
        # self.add(z_text)
        #
        # self.add(x_axis, y_axis, z_axis)
        # self.play(ShowCreation(x_axis), ShowCreation(y_axis), ShowCreation(z_axis))

        # 四棱锥，分布在z=-3的平面上，底面是一个正方形
        base_points = [
            [-2, 5, -2],
            [-2, 5, 2],
            [2, 5, 2],
            [2, 5, -2],
        ]

        far_plane_points = [
            [-4, 10, -4],
            [-4, 10, 4],
            [4, 10, 4],
            [4, 10, -4],
        ]

        # 点四个点
        for point in base_points:
            dot = Dot(axes.c2p(point[0], point[1], point[2]), fill_color=RED)
            self.add(dot)

        # 绘制原裁剪面
        for point in far_plane_points:
            dot = Dot(axes.c2p(point[0], point[1], point[2]), fill_color=RED)
            self.add(dot)

        # 创建底面的多边形
        base = Polygon(axes.c2p(base_points[0][0], base_points[0][1], base_points[0][2]),
                          axes.c2p(base_points[1][0], base_points[1][1], base_points[1][2]),
                          axes.c2p(base_points[2][0], base_points[2][1], base_points[2][2]),
                          axes.c2p(base_points[3][0], base_points[3][1], base_points[3][2]))
        base.set_fill(opacity=0.2, color=BLUE)
        far_plane = Polygon(axes.c2p(far_plane_points[0][0], far_plane_points[0][1], far_plane_points[0][2]),
                            axes.c2p(far_plane_points[1][0], far_plane_points[1][1], far_plane_points[1][2]),
                            axes.c2p(far_plane_points[2][0], far_plane_points[2][1], far_plane_points[2][2]),
                            axes.c2p(far_plane_points[3][0], far_plane_points[3][1], far_plane_points[3][2]))
        far_plane.set_fill(opacity=0.2, color=GREEN)

        # 创建顶部的顶点
        top_point = [0, 0, 0]
        origin_text = Text("O", font_size=20)
        origin_text.next_to(axes.c2p(top_point[0], top_point[1], top_point[2]), RIGHT)
        self.add(origin_text)
        dot = Dot(axes.c2p(top_point[0], top_point[1], top_point[2]), fill_color=YELLOW)
        self.add(dot)

        # 绘制棱锥的侧面
        sides = []
        for i in range(4):
            side = Polygon(
                axes.c2p(top_point[0], top_point[1], top_point[2]),
                axes.c2p(far_plane_points[i][0], far_plane_points[i][1], far_plane_points[i][2]),
                axes.c2p(far_plane_points[(i + 1) % 4][0], far_plane_points[(i + 1) % 4][1], far_plane_points[(i + 1) % 4][2]),
            )
            side.set_fill(opacity=0.2, color=BLUE)
            sides.append(side)


        # 添加底面和侧面到场景中
        self.add(base)
        self.add(far_plane)
        for side in sides:
            self.add(side)

        # 添加动画效果（如从不同角度观察）
        self.wait()

        # 绘制一个黄色的P点，坐标是[1.5, 8, -1.5]
        p_point = [1.5, 8, -1.5]
        dot = Dot(axes.c2p(p_point[0], p_point[1], p_point[2]), fill_color=PINK)
        self.add(dot)
        self.play(ShowCreation(dot))
        self.play(Indicate(dot))
        p_text = Text("P", font_size=20)
        p_text.next_to(dot, RIGHT)
        # p_text.fix_in_frame()
        self.add(p_text)

        # 从原点连线到点p，并且求解其与底面的交点Q
        line = Line(axes.c2p(0, 0, 0), axes.c2p(p_point[0], p_point[1], p_point[2]), color=RED)

        self.add(line)
        self.play(ShowCreation(line))
        intersect_point = self.cal_ray_intersection_with_plane(p_point, 5.0)
        dot2 = Dot(axes.c2p(intersect_point[0], intersect_point[1], intersect_point[2]), fill_color=BLUE)
        self.add(dot2)
        self.play(ShowCreation(dot2))
        self.play(Indicate(dot2))
        q_text = Text("Q", font_size=20)
        q_text.next_to(dot2, RIGHT)
        # q_text.fix_in_frame()
        self.add(q_text)

        # step 1：Calculate Similar Triangles
        similar_text = Tex("How\\quad to\\quad calculate\\quad \\vec{p}?")
        similar_text.fix_in_frame()
        similar_text.to_edge(UP)
        self.play(FadeIn(similar_text))
        self.add(similar_text)
        self.wait(0.1)
        self.play(FadeOut(similar_text))
        # 高亮OP, OQ
        self.play(Indicate(line))
        similar_text_2 = Tex("\\frac{\\vec{OQ}}{|Near|} = \\frac{\\vec{OP}}{|ZView|}")
        similar_text_2.fix_in_frame()
        similar_text_2.to_edge(RIGHT)
        self.play(FadeIn(similar_text_2))
        self.add(similar_text_2)

        similar_text_3 = Text("|ZView| could be calculated from ZBuffer")
        similar_text_3.fix_in_frame()
        similar_text_3.to_edge(RIGHT + DOWN * 1.5)
        self.play(FadeIn(similar_text_3))
        self.add(similar_text_3)

        self.wait(0.5)
        self.play(FadeOut(similar_text_2))

        similar_text_4 = Tex("\\vec{OP} = \\frac{|ZView|}{|ZNear|} * \\vec{OQ}")
        similar_text_4.fix_in_frame()
        similar_text_4.to_edge(RIGHT)
        self.play(FadeIn(similar_text_4))
        self.add(similar_text_4)

        BL = axes.c2p(base_points[0][0], base_points[0][1], base_points[0][2])
        BR = axes.c2p(base_points[1][0], base_points[1][1], base_points[1][2])
        TR = axes.c2p(base_points[2][0], base_points[2][1], base_points[2][2])
        TL = axes.c2p(base_points[3][0], base_points[3][1], base_points[3][2])
        # point
        point_BL = Dot(BL, fill_color=RED)
        point_BR = Dot(BR, fill_color=RED)
        point_TR = Dot(TR, fill_color=RED)
        point_TL = Dot(TL, fill_color=RED)
        self.add(point_BL)
        self.add(point_BR)
        self.add(point_TR)
        self.add(point_TL)
        # indicate
        self.play(Indicate(point_BL))
        self.play(Indicate(point_BR))
        self.play(Indicate(point_TR))
        self.play(Indicate(point_TL))

        # text
        text_BL = Text("BL", font_size=20)
        text_BL.next_to(point_BL, RIGHT)
        self.add(text_BL)
        text_BR = Text("BR", font_size=20)
        text_BR.next_to(point_BR, RIGHT)
        self.add(text_BR)
        text_TR = Text("TR", font_size=20)
        text_TR.next_to(point_TR, RIGHT)
        self.add(text_TR)
        text_TL = Text("TL", font_size=20)
        text_TL.next_to(point_TL, RIGHT)
        self.add(text_TL)
        self.wait(0.1)

        # step 2: Calculate vec OQ
        self.play(FadeOut(similar_text_3))
        self.play(FadeOut(similar_text_4))
        OQ_Text = Tex("\\vec{OQ} = \\vec{OBL} + \\vec{BLQ}")
        OQ_Text.fix_in_frame()
        OQ_Text.to_edge(RIGHT)
        self.play(FadeIn(OQ_Text))
        self.add(OQ_Text)

        # arrow OQ
        arrow_OQ = Arrow(axes.c2p(0, 0, 0), axes.c2p(intersect_point[0], intersect_point[1], intersect_point[2]), stroke_color=RED)
        self.add(arrow_OQ)
        self.play(ShowCreation(arrow_OQ))
        self.play(Indicate(arrow_OQ))

        # arrow OBL
        arrow_OB = Arrow(axes.c2p(0, 0, 0), BL, stroke_color=RED)
        self.add(arrow_OB)
        self.play(ShowCreation(arrow_OB))
        self.play(Indicate(arrow_OB))

        # arrow BLQ
        arrow_BLQ = Arrow(BL, axes.c2p(intersect_point[0], intersect_point[1], intersect_point[2]), stroke_color=RED)
        self.add(arrow_BLQ)
        self.play(ShowCreation(arrow_BLQ))
        self.play(Indicate(arrow_BLQ))

        # BLQ could be calculated by Q's screen UV coordinate
        tip_BLQ = Text("vec BLQ can be calculated by Q's screen UV coordinate")
        tip_BLQ.fix_in_frame()
        tip_BLQ.to_edge(BOTTOM)
        tip_BLQ.shift(BOTTOM * 0.5)
        self.play(FadeIn(tip_BLQ))
        self.add(tip_BLQ)
        self.wait(0.1)





