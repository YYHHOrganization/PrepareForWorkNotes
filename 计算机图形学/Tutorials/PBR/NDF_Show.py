from manimlib import *

class PBR_D(Scene):
    def Trowbridge_Reitz_GGX(self, alpha, n_dot_h):
        # Trowbridge-Reitz GGX分布
        # float NdotH  = max(dot(N, H), 0.0);
        alpha2 = alpha * alpha
        n_dot_h2 = n_dot_h * n_dot_h
        denominator = (n_dot_h2 * (alpha2 - 1) + 1)
        res = alpha2 / (np.pi * denominator * denominator)
        return min(res, 1.0)

    def construct(self):
        # 展示D函数：x是粗糙度alpha，y轴是n·h，z轴是D
        axes = ThreeDAxes((0.0, 1.0, 0.1), (0.0, 1.0, 0.1), (0.0, 1.0, 0.1), width=6, height=6, depth=6, z_axis_config={'include_tip': False})
        axes.add_axis_labels('alpha', 'n dot h', 'D')
        # 每0.1添加一个coordinate label
        axes.add_coordinate_labels(font_size=22, num_decimal_places=1)
        self.add(axes)
        self.wait(0.1)
        self.play(ShowCreation(axes))

        # 添加D函数图像
        # Axes.get_graph will return the graph of a function
        D_graph = axes.get_graph(lambda x, y: self.Trowbridge_Reitz_GGX(x, y), color=BLUE)
        self.play(ShowCreation(D_graph))
        self.add(D_graph)