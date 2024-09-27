import numpy as np

from manimlib import *
from scipy.stats import qmc

class MSAA_01(Scene):
    def calculateBarycenter(self, a, b, c, p):
        # 使用叉乘来计算重心坐标
        ab = b - a
        ac = c - a
        pa = a - p
        factor = 1.0 / (ab[0] * ac[1] - ab[1] * ac[0])
        s = (ac[0] * pa[1] - ac[1] * pa[0]) * factor
        t = (ab[1] * pa[0] - ab[0] * pa[1]) * factor
        weights = [1 - s - t, s, t]
        # print(weights, sum(weights))
        return weights
    def isInTriangle(self, triangle, p):
        # 只要前两维
        a = triangle[0]
        b = triangle[1]
        c = triangle[2]
        barycenter = self.calculateBarycenter(a, b, c, p)
        if barycenter[0] >= 0 and barycenter[1] >= 0 and barycenter[2] >= 0:
            return True
        else:
            return False
    def generate_poisson_disc_samples(self, radius, num_samples):
        # 特殊情况，直接写死了，怕生成效果不好
        if num_samples == 4:
            sample = np.array([[0.625, 0.875], [0.125, 0.625], [0.375, 0.125], [0.875, 0.325]])
            sample = sample * 1.0 / self.scale_mode
            sample = np.concatenate([sample, np.zeros((sample.shape[0], 1))], axis=1)
            return sample
        else:
            rng = np.random.default_rng()
            engine = qmc.PoissonDisk(d=2, radius=radius, seed=rng)
            sample = engine.random(20)
            sample = sample[:num_samples]
            # sample 加一个维度，第三个维度是0
            sample = np.concatenate([sample, np.zeros((sample.shape[0], 1))], axis=1)

            return sample

    def check_subpixel_coverage(self, triangle, subpixels, dots, color=RED):
        index = 0
        for subpixel in subpixels:
            if not self.debug_mode:
                self.play(FlashyFadeIn(dots[index], run_time=0.001))
            # 判断subpixel是否在三角形内部
            if self.isInTriangle(triangle, subpixel):
                # subpixel在三角形内部，设置为红色
                dots[index].set_fill(color=color)
                self.sub_pixel_color[index] = color
            index += 1


    def construct(self):
        self.debug_mode = False
        self.scale_mode = 1
        intro_words = Text("""
                    MSAA Demo
                """)
        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.play(FadeOut(intro_words))
        #grid = NumberPlane((-10, 10), (-5, 5))
        #self.play(ShowCreation(grid))
        r2 = ScreenRectangle(height=6, aspect_ratio = 8.0/6.0)
        # 再rectangle里面绘制线段，让他变成类似屏幕像素的效果，6排8列(都是横着或者竖着的线)
        # r2.add(Line(r2.get_corner(UL), r2.get_corner(DR), color=RED))
        point_location = []
        row_num = (7 - 1) * self.scale_mode + 1
        col_num = (9 - 1) * self.scale_mode + 1
        for i in range(1, row_num):
            r2.add(Line(r2.get_corner(DL) + UP * i * 1.0/self.scale_mode, r2.get_corner(DR) + UP * i * 1.0/self.scale_mode, color=WHITE))
        for i in range(1, col_num):
            r2.add(Line(r2.get_corner(UL) + RIGHT * i * 1.0/self.scale_mode, r2.get_corner(DL) + RIGHT * i * 1.0/self.scale_mode, color=WHITE))
        # 计算每个像素的中心点
        for i in range(1, row_num):
            for j in range(1, col_num):
                point_location.append(r2.get_corner(DL) + UP * i * 1.0/self.scale_mode- UP * 0.5 * 1.0/self.scale_mode+ RIGHT * j * 1.0/self.scale_mode- RIGHT * 0.5 * 1.0/self.scale_mode)
        # 每个point_location的位置放置一个红点
        for point in point_location:
            r2.add(Dot(point, fill_color=RED, radius=0.1 / self.scale_mode))

        self.play(ShowCreation(r2))
        # self.wait(2)
        intro_words2 = Text(""" step 1: subpixel sampling """)
        intro_words2.to_edge(UP)
        self.play(Write(intro_words2))
        self.play(FadeOut(intro_words2))
        # self.wait(1)
        # 计算子像素点，然后进行绘制
        poisson_disc_samples = self.generate_poisson_disc_samples(0.3,4)
        subpixel_points = []
        dots = []
        self.sub_pixel_color = []
        # print(point_location)
        for point in point_location:
            subpixel_points.extend([point - UP * 0.5 * 1.0/self.scale_mode- RIGHT * 0.5 * 1.0/self.scale_mode + sample for sample in poisson_disc_samples])
        for point in subpixel_points:
            # amimation
            # r2.add(Dot(point, fill_color=YELLOW))
            tempDot = Dot(point, fill_color=YELLOW, radius=0.05 / self.scale_mode)
            dots.append(tempDot)
            self.sub_pixel_color.append(BLACK)
            if not self.debug_mode:
                self.play(FadeIn(tempDot, run_time=0.001))
            else:
                r2.add(tempDot)

        intro_words3 = Text(""" step 2: coverage test """)
        intro_words3.to_edge(UP)
        self.play(Write(intro_words3))
        self.play(FadeOut(intro_words3))
        # coverage test
        # 绘制两个三角形
        square_scale_mode = self.scale_mode ** 2
        triangle_1_location = [point_location[0 * square_scale_mode] + 0.14, point_location[7 * square_scale_mode] - 0.22, point_location[31 * square_scale_mode] + 0.17]
        # triangle_2_location = [point_location[6 * square_scale_mode] - 0.12, point_location[26 * square_scale_mode] + 0.31, point_location[37 * square_scale_mode] - 0.25]
        triangle_2_location = [point_location[32 * square_scale_mode] - 0.12, point_location[44 * square_scale_mode] + 0.31, point_location[1 * square_scale_mode] - 0.25]

        triangle1 = Polygon(triangle_1_location[0], triangle_1_location[1], triangle_1_location[2])
        triangle2 = Polygon(triangle_2_location[0], triangle_2_location[1], triangle_2_location[2])
        triangle1.set_fill(color=BLUE, opacity=0.5)
        triangle2.set_fill(color=GREEN, opacity=0.5)
        self.play(ShowCreation(triangle1))
        self.play(ShowCreation(triangle2))
        #self.wait(1)
        self.check_subpixel_coverage(triangle_1_location, subpixel_points, dots, color=BLUE)
        self.check_subpixel_coverage(triangle_2_location, subpixel_points, dots, color=GREEN)

        #self.wait(1)
        intro_words4 = Text(""" step 3: subpixel blending """)
        intro_words4.to_edge(UP)
        self.play(Write(intro_words4))
        self.play(FadeOut(intro_words4))
        # subpixel blending
        for i in range(len(point_location)):
            # 计算每个像素的颜色
            color = np.array([0.0, 0.0, 0.0], dtype=np.float64)
            for j in range(4):
                decode_color = color_to_rgb(self.sub_pixel_color[i * 4 + j])
                color += np.array(decode_color)
            color = color / 4
            # 以point_location[i]为中心，绘制一个rectangle
            r = Polygon(point_location[i] + UP * 0.5 * 1.0 / self.scale_mode + RIGHT * 0.5 * 1.0 / self.scale_mode, point_location[i] + UP * 0.5 * 1.0 / self.scale_mode- RIGHT * 0.5 * 1.0 / self.scale_mode,
                        point_location[i] - UP * 0.5 * 1.0 / self.scale_mode - RIGHT * 0.5 * 1.0 / self.scale_mode, point_location[i] - UP * 0.5 * 1.0 / self.scale_mode + RIGHT * 0.5 * 1.0 / self.scale_mode)
            c = rgb_to_color(color)
            r.set_fill(color=c, opacity=1)
            r2.add(r)
            if not self.debug_mode:
                if i < 10:
                    self.play(FadeIn(r, run_time=0.2))
                else:
                    self.play(FadeIn(r, run_time=0.02))
            # self.play(ShowCreation(r))

        # triangle1 和 triangle2 fade out
        self.play(FadeOut(triangle1))
        self.play(FadeOut(triangle2))