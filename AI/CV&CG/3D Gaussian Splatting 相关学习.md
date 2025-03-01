# 3D Gaussian Splatting 相关学习

# 一、原始论文解读

## 1.前置阅读材料

【1】首先，推荐阅读这篇：https://zhuanlan.zhihu.com/p/687549139，以及其后续文章。



## 2.数学知识详解

### （1）3D Gaussian的表达

#### （i）协方差矩阵的含义

可以参考：https://www.zhihu.com/tardis/zm/art/37609917

对于二维高斯分布来说，这里可以可视化一下协方差矩阵对分布的影响：https://blog.csdn.net/xfijun/article/details/53822490

以下是对本节开始的那篇知乎文章的补充：

- （1）在多元正态分布中，每个点的似然（likelihood）指的是在给定该点的情况下，观察到该点的概率密度。



#### （ii）矩阵特征值的含义，以及特征值分解

推荐参考文章：https://www.matongxue.com/madocs/228/，先看个大概。非常推荐看这个：https://zhuanlan.zhihu.com/p/673532604