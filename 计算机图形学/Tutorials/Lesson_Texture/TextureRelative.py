from manimlib import *

class UV_Space_Show_1(Scene):
    def construct(self):
        # 绘制UV空间两个轴，范围为[0,1]，每0.1添加一个坐标标签
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1, 0.1],
            width=6,
            height=6,
            axis_config={"color": BLUE},
            x_axis_config={}
        )
        # 没有二维的接口，自己放两个Text在对应位置
        x_label = Text("U", font_size=20)
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("V", font_size=20)
        y_label.next_to(axes.y_axis.get_end(), UP)
        axes.add(x_label, y_label)
        axes.add_coordinate_labels(font_size=22, num_decimal_places=1)
        self.add(axes)
        self.play(ShowCreation(axes))

        # add picture on UV space
        uv_space = ImageMobject("uv1.png")
        uv_space.set_height(6)
        # 图像的左下角在axes的原点位置
        uv_space.move_to(axes.c2p(0.5, 0.5))
        self.add(uv_space)
        self.play(FadeIn(uv_space))
