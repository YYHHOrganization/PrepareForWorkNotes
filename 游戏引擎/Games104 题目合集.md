# Games104 题目合集



# Lecture 15~17 游戏引擎的Gameplay

【1】介绍一下publish-subscribe pattern，主要包含哪些部分？

【2】介绍一下C++ 智能指针：unique_ptr, shared_ptr, weak_ptr

【3】Event Dispatcher有什么策略？

- 直接分发；
- 使用Event Queue：Ring Buffer
- Batching

【4】Event Queue有什么问题？

- Pretick & PostTick

【5】脚本语言的基础原理是什么？比如说Lua语言（提示：虚拟机，可参考材料：Lua JIT）

【6】简单描述：热更新的原理是什么？

【7】可视化脚本的实现原理是什么？

- 变量，Statement，Control Flow，函数，类
- 可以考虑：WPF做UI，实现一套简单的蓝图系统，自设计一套Visual Script

【8】Component-based 架构是游戏开发中非常常用的模式（Unity，UE...）。

【9】不要在事件分发中加入优先级，因为会导致高耦合。理论上应该设计成执行效果与事件执行顺序无关。



【10】关于Navigation：

- （1）Map Representation：
  - Waypoint Network
  - Grid：Square/Triangle/Hexagon
  - Navigation Mesh：目前主流的做法：网格是非流形的（note：这是什么意思？）
  - Sparse Voxel Octree
- （2）Path Finding：
  - BFS，DFS
  - Dijkstra
  - A*算法
- （3）Path Smoothing：Funnel Algorithm
- （4）Navmesh生成的原理大致是什么？
  - NavMesh的更新：可以使用Tiled的思想



【11】关于Steering Behavior：这套系统大概需要考虑哪些部分？

【12】有关Crowd Simulation：

- Micro
- Macroscopic
- Mesoscopic

【13】Collision Avoidance：避免碰撞

- Force-based models
- Velocity-based models
  - VO
  - RVO
  - ORCA

【14】感知：Sensing or Perception

- internal information
- static spatial information：navigation & tactical
- dynamic spatial information： influence map， GameObjects
- sensing simulation

【15】决策算法：

- 







# todo：

【1】https://zhuanlan.zhihu.com/p/342322276?utm_id=0：剧情编辑器，先看一个这个

【2】Unity Animacer：有时间看看

【3】有时间可以看一下Unity的Navigation系统是否包含Games104所讲解的内容；

【4】项目里面有鱼群群体模拟相关的代码，可以再过一下逻辑

【5】简单过一下Sensing部分有哪些GDC开发者大会的演讲或者文章，可以参考一下；

【6】复习一下有限状态机；看一下Unity的Behavior Tree插件的源码

