# Games104 笔记全

Games104的笔记参考官方：[GAMES104课程笔记05-Lighting, Materials and Shaders - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/04/13/GAMES104-NOTES-05.html#physical-based-material)

注：

- 标了高亮黄色的章节是还没整理完的，主要原因是太硬核了；
- 



# 一些可看的Demo及对应的章节部分

- CUDA编程（这个有时间再说），Compute Shader要看几个；
  - 目前看了Compute Shader上手程序的前两个工程，第三个是2D流体模拟，稍微看了点原理，感觉有点硬核而且偏物理就没继续看。笔记是【M_ComputeShader学习.md】，对应的Unity工程是MinimalCompute。
    - [ ] 三月计划1：2D流体那个demo看完，复刻一下吞星之鲸的地面效果（不确定跟2D流体是否有关）
    - [ ] 三月计划2：继续学习Compute Shader，并尝试看懂MinimalCompute工程的其他项目（偏物理硬核的暂不做要求），三月份计划额外看两个就行。

- 皮肤和毛发的渲染（拉下来跑开源项目，了解一下原理应该就够了，暂时优先级应该不高，非三月计划）
- 【三月计划】摸一下美术的PBR工作流（软件SD+SP），看个教程SD和SP各做两个demo就行，时间有限，先依据项目来看教程
  - 对应的知识点：[PBR的两套工作流](# （c）PBR的两套工作流)
  - SD看这几个：
    - [ ] 【1】基础教程系列：[Substance 3D Designer First Steps: 01 - Overview & Basics | Substance 3D (youtube.com)](https://www.youtube.com/watch?v=VyFgpitTsYg)及系列视频，以及[Substance Designer FUNDAMENTALS YOU MUST KNOW (For beginners) (youtube.com)](https://www.youtube.com/watch?v=uc7qysekuKo)
    - [ ] 【2】[Creating your first Substance Material Introduction | Substance 3D (youtube.com)](https://www.youtube.com/watch?v=i_q_JaCg7hk&list=PLB0wXHrWAmCwWfVVurGIQO_tMVWCFhnqE&index=1)
    - [ ] 【3】[Marble Tile | Beginner Substance Designer Tutorial (youtube.com)](https://www.youtube.com/watch?v=ov2jSf4fKR4)

  - SP看这几个：
    - [ ] 【1】[Substance 3D Painter First Steps: 01 - Creating a Project, Materials & Masking | Substance 3D (youtube.com)](https://www.youtube.com/watch?v=mv6pg1O9vEQ&list=PLB0wXHrWAmCw90iSI7Gj8XWnEN6NHt6kx&index=1)以及对应系列教程；
    - [ ] 【2】[Substance Painter 2021 Getting Started - Part 05 - Exporting & rendering | Substance 3D (youtube.com)](https://www.youtube.com/watch?v=4iUVOfGOxPI&list=PLB0wXHrWAmCwnqWfKdGEmbtSKN2EzvLrY&index=6)

- 体积云（做了一部分，基本原理差不多了）；
- 体积雾；
- 体积光；
- 大气渲染的demo
- HBAO/GTAO的实现；
- 用tesselation实现实时雪地交互，草地渲染；
- 地形系统可以再研究一下，毕竟开放世界肯定要用;
- Unity的光照系统学习（包含整个六、4的理论部分），以原神的群玉阁和铁道的贝洛伯格车站场景为例；
- 做一个角色移动系统，涉及动画相关的内容，正好算是复习一下（比如IK，布娃娃系统）；
- Unity可以玩一下Houdini+Vertex Animation。
- BFS+Dijsktra+A*的C++版本实现，可以做个小demo。
- Unity NevMesh寻路系统可以玩一下



# 一、源代码解读

## 1.代码获取

[BoomingTech/Piccolo: Piccolo (formerly Pilot) – mini game engine for games104 (github.com)](https://github.com/BoomingTech/Piccolo)

首先进入到Release页面：[Releases · BoomingTech/Piccolo (github.com)](https://github.com/BoomingTech/Piccolo/releases)，下载v0.0.9版本的源代码压缩包，解压缩之后用VS code将其打开，方便代码阅读，如下图：

![image-20240126162331318](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126162331318.png)

以下会分别介绍每个文件夹的作用。



## 2.每个文件的作用

### （1）综合

首先先来看一下总体的说明：

![image-20240126162832944](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126162832944.png)

- 第一列是所有以`.`开头的文件或文件夹，是各个平台或者工具的配置文件；有些操作系统会隐藏这些文件；
- 第二列是与cmake有关的内容；
- 第三列是系统的批处理文件，方便构建piccolo引擎而书写的脚本；
- 第四列是一些readme的说明等。

除了上图所示的这些文件和文件夹，还有一个engine文件夹没有描述，接下来来展开说明一下engine文件夹；



### （2）engine文件夹

![image-20240126163157120](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126163157120.png)

- 3rdparty存放的是第三方库的源码和一些二进制库；
- asset是小引擎在启动的时候默认关卡所需要的一些资产；
- bin文件夹上图并没有，是构建的时候才会出现的一个文件夹，并不在仓库里。里面会包括piccoloParser，该文件会参与到引擎的构建过程当中，会解析C++源代码，根据模板文件（在template文件夹中）生成一些功能性的代码；
- configs文件夹里存放的是编辑器在启动的时候所需要的一些配置文件；
- jolt-asset文件夹存放的是物理库jolt physics所需要的一些shader；
- shader文件夹是引擎启动的时候所必须的shader；
- source文件夹后面会展开来说；
- template文件夹存放的就是piccoloParser在生成代码的时候所需要的模板文件；

以下详细介绍source文件夹。



### （3）source文件夹

![image-20240126163819471](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126163819471.png)

- 第一个未显示的文件夹是_generated，是piccoloParser生成的功能性的代码；
- editor是编辑器的源代码；
- meta_parser是piccoloParser的源代码；
- precompile文件夹有一个cmake脚本和一个配置文件，这两个文件会使得我们在构建引擎工程之前都会使用piccoloParser解析一下源代码，从而生成所需要的功能性代码；
- runtime是引擎最核心的代码，里面是比较严格按照课程所说的分层结构来编写的（**课程内容见后面部分。**）
- test目前只有一个占位文件，后面需要编写单元测试这种的时候再放进test文件夹里；

接下来会介绍runtime文件夹；



### （4）runtime文件夹

![image-20240126164441692](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126164441692.png)

这里就是引擎的分层结构的知识点了，后面也会整理。`engine.cpp`和`engine.h`文件对应整个小引擎的入口文件。我们可以用可视化的方式来看runtime文件夹下所有文件的代码行数组成的矩阵数图（这个可视化的代码没开源，所以只能截图）：

![image-20240126165759624](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126165759624.png)

> 一个结论：
>
> - 最大的子文件夹是function文件夹，第二大是core文件夹，接着是resource和platform；



## 3.编译工程

在VS Code当中启动terminal，然后输入：

```cmake
cmake . -B build
```

这行命令的意思是以当前文件夹为工程根目录，生成工程在build文件夹里面。运行之后生成的文件就在build文件夹当中了。接着输入：
```cmake
cmake --build build
```

这行命令用于构建build文件夹里面的工程。**注：如果build有问题也可以用VS 2019打开build文件夹里面的sln文件，然后在Release模式下点击本地Windows调试器，没意外应该可以编译成功了。**

![image-20240126170813443](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126170813443.png)

编译成功之后如下图所示：

![image-20240126171040327](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126171040327.png)

> 操作说明：右键转动视角，点击右上角Editor Mode进入到游戏视角，可以控制小白人的移动，按住Alt键可以呼出鼠标；

将生成的sln文件用VS2019打开，可以看到如下的结构：

![image-20240127182614773](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127182614773.png)

- 这里的PiccoloRuntime是核心结构，里面是严格按照分层结构来写的；
- PiccoloEditor是编辑器，可以当成是一个单独的工程；
- PiccoloShaderCompile：shader比较特殊，虽然也是glsl的源码，但是编译出的二进制文件需要单独管理；
- PiccoloPreCompile：用了类似于虚幻的反射机制，在C++中定义各种数据类型，可以自动反射出在资源里面应该用什么方式去读取。**这个后面还会介绍，不过这种反射机制是游戏引擎非常重要的机制。**



## 4.引擎入口和运行流程介绍

在前面有提到，engine/source/runtime文件夹下面的`engine.cpp`和`engine.h`文件是引擎的入口文件，打开如下：

![image-20240126171557944](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126171557944.png)

可以看到，箭头所指的两个函数是空的占位函数，而我们先不用太关注const函数，因此只有红框内的函数是需要重点关注的。



### （1）用sourceTrail软件查看执行流

软件下载：[Release 2021.4.19 · CoatiSoftware/Sourcetrail (github.com)](https://github.com/CoatiSoftware/Sourcetrail/releases/tag/2021.4.19)，下载installer版本并安装即可。官方的教程如下：[Sourcetrail - Introduction (youtube.com)](https://www.youtube.com/watch?v=Cfu6f0uyzc8)

具体的执行流直接看这篇笔记就行：[Games104 源码解析笔记-CSDN博客](https://blog.csdn.net/hijackedbycsdn/article/details/131228832)

也可以直接复习对应的源码解读视频：[【自研开源游戏引擎】Piccolo源码解读，全网最适合入门的引擎教程_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1zP4y1R7Ys/?spm_id_from=333.1007.0.0&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)



大概现在看到了上述视频的16：11左右的部分，剩下的内容后面学完课程再来补充吧。





# 二、01 游戏引擎导论

## 1.丰富的游戏引擎生态

![image-20240126183157075](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126183157075.png)

大家非常熟悉的虚幻引擎、Unity引擎，还有前些年非常厉害的Crytek引擎（这些年有点掉队），这些都是商业级引擎。

全球的游戏大厂（比如育碧、EA、RAGE）都有自己的游戏引擎，比如大名鼎鼎的寒霜引擎。如果你是一个FPS游戏玩家，一定知道《战地》这款游戏，它那种开阔战场的感觉，就是寒霜引擎巨大能力的表现。

Anvil（铁砧）引擎是育碧做刺客信条的，虽然觉得育碧的游戏有点塑料，但不妨碍它的引擎做得好。《刺客信条》里面一个很著名的案例——巴黎圣母院，一场大火后，我们现在只能在《刺客信条》里面感受和体验巴黎圣母院的盛况了。

Valve的source引擎以及Torque、Armory、Godot这些免费引擎，主要以开发轻量级的休闲游戏为主，就复杂性而言，它们和那些商业引擎、大厂的引擎相比还是有差距的。



 随着游戏行业的发展，我们发现引擎（包括引擎内部的有些东西）非常复杂。早期的游戏运擎会自己写物理模块（比如解算器、物理碰撞检测），但后来这些问题越来越复杂，**就会出现专门做物理模块的，我们叫做middleware（中间件）**。如下图：

![image-20240126183355835](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126183355835.png)

> 比如做物理的Havok、PhysX，还有专门做声音的Wwise、fmod。游戏里面的声音效果是非常重要的，玩一个恐怖游戏，走进房间会听到脚步的回声。打仗的时候，一个炮弹在身边爆炸会有耳鸣感。像SpeedTree就是专门做植被的（比如阿凡达就是用SpeedTree做的植被）。还有比如PCG生成的中间件（关于PCG可以先简单看一篇科普文章[技术讨论：PCG相关 | 设计者笔记 (jskyzero.com)](https://design.jskyzero.com/2021/11/21/ProceduralContentGeneration/)，后面会再做补充）。



## 2.游戏引擎的概念

游戏引擎是十分复杂的。举个例子，下面是一个简单的双人对战场景：

![image-20240126184018381](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126184018381.png)

但从图中也可以看到，我们为了实现这个游戏场景需要非常多的考虑。

> 要把这个人渲染出来、要这个人能动起来，就需要有一个渲染系统、动画系统。这是看得见的，还有很多看不见的系统，比如要定义一个物理碰撞系统，需要知道你打不打得中我。
>
>  还有控制系统，因为一切输入都要能进得去。还有更复杂的，网络怎么同步？两个人在两台不同的计算机上，A同学按下一个键，他在自己的世界里就做了一个操作。在另外一个世界，B同学是不是也要看到同样的操作？如果他做了个闪避操作，到底算是闪避成功还是没有成功？
>
>  这就是这个系统的复杂度。

游戏引擎的复杂架构可以参考《游戏引擎架构》这本书。这本书有一张著名的图：

![image-20240126210805321](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126210805321.png)

> 看不清没关系，后面的笔记中会逐步介绍相关的内容。



## 3.游戏引擎的挑战

（1）来自算力的挑战

（2）**核心设计的边界条件——Realtime（实时）**

> **这其实就是游戏引擎的复杂度。而且，更让我们觉得痛苦的，也是游戏引擎的一个核心设计的边界条件——Realtime（实时）。**
>
>  Realtime是学习游戏引擎特别要记住的一个关键性概念，就是说，无论有多么厉害的算法，能做出多么好的效果，如果不能够在1/30秒（33毫秒）之内把计算结果提交出去，那么这个算法就是无效的。
>
> 实际上也不可能给出那么大的算力，比如我们在做游戏引擎的时候，整个预算只有33毫秒。但是每个系统，比如做一个非常漂亮的衣料模拟、做一个非常棒的水体效果、做一个非常酷的物理爆炸，可能只给你1-2毫秒。并且，由于玩家对帧率要求也越来越高。现在玩一个动作游戏，如果低于60帧，就觉得这个画面没办法接受。60帧意味着什么？计算只有15毫秒。Fitting到这么短的一个时间片里面，这就是现代游戏引擎设计的核心难点。

（3）强大的工具体系以及可协作的引擎工具链体系

也就是说，一个游戏引擎如果只是一大堆代码、一个SDK，实际上是没办法用的，必须要提供一个非常强大的工具体系。

（4）引擎是可更新的，需要能够在不影响已有功能和游戏的前提下能够添加新的特性。



## 4.如何学习游戏引擎？

![image-20240126191736662](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126191736662.png)

但是实际上，这些全看了需要非常多的时间，重要的是先建立一个体系结构，具体的细节依据感兴趣的方向再深入了解和学习。



## 5.课程内容介绍

（1）Basic Elements

- 引擎结构和分层；
- 数据组织和管理；

（2）Rendering——Real Time

- Model，Material，Shader，Texture
- Light and Shadow
- Render Pipeline
- Sky，Terrain，etc

（3）Animation

- 动画的基础概念
- 动画的组织结构和管线

（4）Physics

- 物理系统的基础概念
- Gameplay Applications
- Performance Optimization

（5）Gameplay

- Event System
- Scripts System
- Graph Driven

（6）Misc.Systems

- Effects
- Navigation
- Camera

（7）Tool Set

- C++ 反射
  - 核心是使得过去的工具和未来的工具彼此间可以兼容
- Data Schema

（8）Online Gaming

- Lockstep Synchronization
- State Synchronization
- Consistency

（9）Advanced Technology

- Motion Mathcing
- Procedural Content Generation（PCG）
- Data-Oriented Programming（DOP）
- Job System
- Lumen
- Nanite



后文会更详细的进行介绍。



# 三、02 引擎架构分层

## 1.游戏引擎的分层结构

可以分为五层的结构：

- Tool Layer
- Function Layer
  - 比如动画，渲染，物理，脚本，AI，FSM，相机，HUD和Input
- Resource Layer
  - 负责加载、管理不同的数据（比如来自DCC软件的）
- Core Layer
  - 上面的层需要频繁调用的代码，比如内存分配，线程管理，容器分配，数学模块等
- Platform Layer
  - 平台层

比较特殊的是中间件（Middleware），这一部分往往有两种存在形式：

- 作为SDK直接集成到引擎当中，在编译的时候一起参与构建；
- 变成独立的工具，与引擎只通过文件格式进行交换（其实就是比如在DCC中做完之后，导入到引擎当中）



**分层的逻辑在于**，位于下面的层是不能够调用上面层的接口的，但位于上面的层则可以调用底层的接口。底层的代码一般都比较稳定，完成之后很少动他们。



## 2.五层分层结构的具体介绍

举例：假设我们想要做一个动起来的角色，我们要如何使用引擎的分层结构呢？

### （1）资源层

（1）如何把资源（比如Maya建模的角色和对应绘制的贴图）导入到引擎当中？

一些比如美术资源的各种格式要转为引擎支持的格式，这一步叫做import资源，并且转为assets(比如说所有的png，jpg格式的文件导入引擎中会被转为dds格式)，这样做是为了方便引擎能更高效地处理。

- 直观理解比如写了一个word文档(比较大)，但是使用的时候转为txt文档使用(比较小)

> 补充：dds格式按照16个byte一块将图像元素一块一块排布好，这样可以直接扔进显卡里面成为纹理。



（2）需要定义一个资产，**用来将相关的美术资源关联在一起(比如纹理贴图和法线贴图)**，比如可以用XML格式存储：

![image-20240126214629270](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126214629270.png)

一个概念：**GUID**（唯一识别号）

- GUID is an extra protection of reference
- 希望能够给每个资产设置一个唯一标识号，这样资源之间的互相关联性就可以用GUID来判定。

> 补充知识点：可以看一下Unity的meta文件的作用：[unity中的.meta文件_unity .meta-CSDN博客](https://blog.csdn.net/keneyr/article/details/103917525)



（3）要有一个实时的资产管理器

- handle system，后面会展开讲；
- **资源层要管理所有资源的生命周期，十分重要。**因此GC系统就需要写好。
- 延迟加载技术（比如说原神某个角色突然出现，贴图会有一个明显的模糊变清晰的过程，这个可能就是延迟加载技术导致的），因为内存很小但是硬盘很大；



### （2）Tick——Function layer

每一个tick，系统会把该做的事情都做一遍。这里面有两个很重要的概念：`tickLogic`和`tickRender`，逻辑优先，渲染在后:

- 逻辑做的：把物理算一遍，计算相机属性，碰撞检测等(比如A是否有打中B，就是逻辑做的事情，不管玩家有没有看见)
- 渲染做的：比如裁剪，光照，相机的shadow等；

案例代码如下:

```c++
void tickMain(float delta_time)
{
    while(!exit_flag)
    {
        tickLogic(delta_time);
        tickRender(delta_time);
    }
}

void tickLogic(float delta_time)
{
    while(!exit_flag)
    {
        tickCamera(delta_time);
        tickMotor(delta_time);
        tickController(delta_time);
        tickAnimation(delta_time);
        tickPhysics(delta_time);
        //...
    }
}

void tickRender(float delta_time)
{
    if(!exit_flag)
    {
        tickRenderCamera();
        culling();
        rendering();
        postprocess();
        present();
    }
}
```

事实上，在Games104中开源的小引擎中也是类似的做法。

实际上，在引擎当中的功能层是十分复杂的（基本也是代码和算法最多的），很多功能会和游戏逻辑混在一起（比如相机的逻辑表现究竟是属于游戏还是游戏引擎）。



### （3）引擎的多线程架构

![image-20240126221726802](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240126221726802.png)

> 现在一些成熟的商业引擎（如Unity，Unreal）采用的是多线程的架构，并且他们可能会把一些特别容易并行化的运算（如物理，动画）单独fork出来，分散到很多线程上执行，即上图中间的架构。

更进阶的架构，Job System带来的困难点：很多系统之间具有一定的依赖关系，如何保证任务正确的执行顺序就是Job System的一个难点。**未来的引擎架构应该都是多核的结构。**



### （4）核心层

这里面主要的有比如数学库，或者数据结构的一些定义。由于C++内置的容器在调用的时候可能会产生大量的内存碎片，并且很难被管理，因此游戏引擎需要手动实现属于自己的数学库，以加快执行的效率，**也就是说引擎要进行比较好的内存管理**，有几条原则:

- 尽可能把数据放在一起
- 访问数据的时候尽可能按顺序访问
- 读写的时候尽可能一起去读写

> 补充：SIMD的概念：[SIMD简介 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/55327037)，后续有需要再做进一步整理。
> ![image-20240127141104504](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127141104504.png)

在游戏引擎中，我们一般会预先申请一大块内存，并由自己管理，从而追求最快的效率。



### （5）平台层

这里比较头疼的可能是DirectX，OpenGL，Vulkan之间的跨平台问题。在现代游戏引擎中有一个重要的层叫做RHI(Render Hardware Interface)，它重新定义层graphics API，然后把各个硬件的SDK的区别封装起来。比如下面就是一小段RHI代码：
![image-20240127142519396](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127142519396.png)

另外一个痛苦的点可能是不同平台的CPU架构可能都不一样（比如PS3和PC），这也是很麻烦的。



### （6）工具层

工具层相对来说比较灵活一些，引擎的其他层往往用C++进行开发，从而追求高效率。而工具层可以用其他语言开发（比如C#）。很多时候工具层的代码量是很大的。

工具层其他要做的事情：

![image-20240127143145108](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127143145108.png)



# 四、03 如何构建游戏世界

## 1.GO概念,组件式编程和事件系统

游戏物体分类:

- dynamic objects,比如角色,飞行物等
- static objects,比如房屋等建筑物
- environment,比如地形系统，天空，天气系统，以及植被系统等
- other game objects：比如trigger area,空气墙,navmesh,ruler（规则）等

以上统称为GameObject(GO)，物体包括属性property和行为behavior

> 可以想到的一种编程思路是,比如有无人机和能够发射子弹的无人机,构建一个基类Plane,然后利用继承关系来制作不同的子类,但这种可能会遇到菱形继承的问题,**这就引发了组件式编程的思路。**
>
> 通过组件式编程,无人机可以由以下组件组成:transform,model,motor,AI等

组件式编程的示例代码如下:

![image-20220809214555547](E:/%E7%B1%B3%E5%93%88%E6%B8%B8/%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E/games104/games104%E7%AC%94%E8%AE%B0/Games104%20%E7%AC%94%E8%AE%B0%20%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E%E6%9E%B6%E6%9E%84(1).assets/image-20220809214555547.png)

注意到这里面有一个tick函数,可以想到的思路是遍历GO当中的每个Component并且调用他们的tick函数,就可以触发游戏的更新逻辑.

不过,在现在的成熟引擎中,往往会按照系统进行tick,比如motor系统,controller系统(包括物理碰撞检测系统等),animation系统等,**这就是流水线思路**,可以方便批处理.

现在的两大商业引擎的相关架构如下:
![image-20220809214901254](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220809214901254.png)

注意:UObject和Object这两个类并不是GameObject,他们是更上一层的封装,提供最基本的如生命周期管理之类的方法。



完成了以上部分后,游戏还缺少交互,比如发射的子弹击中了敌人,想要让敌人这个GO知道自己被击中了,**这就是事件系统Event System**,这种统一成Event的机制本身就是一种解耦合。Event机制包括:

- Message sending and handling
- decoupling(解耦合) event sending and handling

类比游戏里就是A判定打中了B,就发送一个事件给B,B在下一次tick的时候对事件进行处理,并作出反应即可.

两大商业引擎的事件机制如下:

![image-20220809220542079](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220809220542079.png)



## 2.场景管理Scene Management

实践中,每个GO会有一个唯一的编号,可以根据这个编号或者物体的位置来找到这个物体.场景管理有如下方式:

- 不怎么管理,比如直接通知半径x范围内的物品即可
- 对世界划分格子,用grid来进行管理,这对于小场景物品分布均匀的场景来说是可以使用的方案
- 升级版**解决方案:hierarchy层级结构**:Hierarchical segmentation,比如说利用四叉树等,再比如八叉树,BVH(现在比较流行,比如视锥体裁剪，子弹弹道快速定位等)，BSP(binary space partitioning)等

> 关于BVH树如何做子弹弹道的快速定位不是很清楚，不过是不是可以理解成能够和场景快速求交呢？



## 3.时序性

在编写引擎的时候,我们不能够忽略事件的时序性,以及可能存在的循环引用现象,这里用下面一张图进行说明:

![image-20220809222057156](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220809222057156.png)

可以看到,有如下几种可能出现的问题:

- 不同的系统之间来回调用,比如motor触发了某个animation,animation会影响physics,physics又会回来影响motor
- 如果一个物体作为另一个物体的子物体,那么tick要有时序,比如先tick父物体再tick子物体。现在引擎很多是按照component来tick的，因此比较复杂（并行计算必须要考虑时序性）
- 如果消息系统没有统一管理的话,可能存在A给B发消息,B给A发消息,顺序问题和过多的消息引发混乱和歧义

解决方案之一：给Message**增加一个类似于邮局系统**,想要发送接收Message都需要走这个邮局系统,来保证时序性。（比如A要给B发消息，需要走邮局，下一个tick B才能收到消息，然后给A回复的时候依然要走邮局，来确保时序性。）实际实现上，component中往往会实现pretick和posttick函数来解决时序问题（todo：piccolo小引擎好像暂时没看到解决时序的代码）



## 4.Q&A

(1)如果一个Tick过长怎么处理?

> 有以下几种常见的处理方法:
>
> - 每个tick传入一个步长进去,对于位移这种会补偿起来,让玩家注意不到
> - 直接跳过一个tick,但是比较危险
> - 一般来说需要对引擎进行一定的优化,比如一场爆炸产生了过多的GO,系统难以很快处理,**此时的一个思路是采用deferred process**,比如一共50个GO,第一个tick处理25个,第二个tick处理另外25个,这样基本玩家也可以接受.

(2)tick的时候,渲染线程和逻辑线程如何进行同步?

> tick logic一般来说会比tick render更早一点,并且一般会分为两个线程来执行

(3)物理和动画互相影响的时候如何处理?

> 比如某个动画播放的时候想要看到比较好的物理效果,常见的处理方式利用插值的方法，一开始先播放动画,在动画播放到一定程度的时候将状态输入到物理系统当中,接下来由物理系统来进行演算。（状态越往后越依赖于物理系统）

（4）组件模式有什么优缺点？

> 缺点：
>
> - 直接实现的效率不如Hard Code高；
> - 组件之间也要有通讯接口机制，有的时候一个组件并不知道GO上有哪些其他的组件。举个例子，GO上有一个组件负责AI，他的逻辑是当GO血量高的时候运行逻辑A，当GO血量低的时候运行逻辑B，而AI组件并不知道角色身上是否有血量相关的组件，这就需要频繁地做query操作（我有这个组件吗？）。这种高频的query操作对效率的影响还是比较大的，不过这算是一个tradeoff。



# 五、04 游戏引擎中的渲染实践

游戏引擎中的渲染会遇到的困难：

- （1）要绘制的物体的效果非常多；
- （2）要考虑不同的GPU和CPU架构，以及这些设备的性能问题；
- （3）无论多复杂的场景，要保证帧率不掉，并且画质的提升（如1080p->4K）也会带来更大的渲染压力；
- （4）渲染不能占用过多的CPU，因为还要留算力给物理等相关的逻辑；

真实游戏开发的时候有一个重要的工作就是Profiling，现在很多时候是自动做的，分析每个模块占用的时间，如果过多的话就要优化。



渲染课程不会包括的内容：

- 卡通渲染(比如原神)
- 一些高质量的2D渲染引擎方案(比如Ori)
- 类似皮肤，毛发这种材质系统

首先复习一下渲染管线:

<img src="E:/%E7%B1%B3%E5%93%88%E6%B8%B8/%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E/games104/games104%E7%AC%94%E8%AE%B0/Games104%20%E7%AC%94%E8%AE%B0%20%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E%E6%9E%B6%E6%9E%84(1).assets/image-20220810214123121.png" alt="image-20220810214123121" style="zoom:67%;" />

## 1.computation——shading

shading当中常见的一些类型的运算，包括取常数，ALU做运算，纹理采样等操作。这里面的纹理采样过程比较复杂：

纹理采样必须要考虑走样的现象，同时要用到Mipmap，**做一次采样需要采样八个像素，做七次插值运算**(八个像素点,一共分成两层mipmap，每层进行双线性插值（每个双线性插值是三次插值），层与层之间进行一次三线性插值）。这就需要GPU的帮助：



## 2.GPU

如果要成为引擎的专家，对GPU一定要有所了解。这一部分的内容会**有点硬核**。

> 更多的关于GPU架构的知识，可以参考下面推荐的几篇文章：
>
> 【1】[深入GPU硬件架构及运行机制 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/545056819)

### (1)SIMD 和 SIMT

> SIMD（Single Instruction Multiple Data） 是单指令多数据，比如说四维向量的加法运算，一次做四次运算，这就是单指令多数据(C++里可以使用SSE扩展宏)；
>
> SIMT (Single Instruction Multiple Threads)是现代显卡性能高的原因，思想是在于GPU虽然内核小但是数量多，这样就可以在多核上执行相同的指令，提高效率：
>
> - 这样给我们的启发是，做绘制算法的时候可以尽量用同样的代码放在一起跑，各自跑各自的数据,会比较快。

两者对比如图:

![image-20220810221016641](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810221016641.png)



### (2)GPU架构和数据流

GPU的架构图如下（以Fermi架构为例，其实是比较老的架构了，但学习起来比较清晰）：

![image-20220810221136205](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810221136205.png)

这里面有几点说明:

- GPC(图形处理集群，在上图左下角可以看到)指的是一组内核,输入指令后可以并行执行,每个内核称为一个Core,比如这里比较典型的CUDA Core,Core里可以做大量的运算;
- 图中①所示的部分（Shared Memory）在GPU中十分重要，负责交换数据。同时需要注意的是Cache在现代计算机体系结构中十分重要;
- 之前的GPU中，SFU（上图有）会做一些比如sin,cos的运算，最新的GPU可能会直接集成Tensorflow这些深度学习技术，以及RT Core用于做实时光线追踪。

CPU和GPU之间的通信数据流如下:

![image-20220810221447541](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810221447541.png)

由于计算机的数据流动有一定成本（可以对比看一下上图当中的流动速度），**因此原则上尽可能让数据单向流动(从CPU->GPU)**。同时务必注意Cache的命中率，现代引擎要尽量保证Cache的命中率高一些。

以下是一些GPU Bound（黑话，理解成性能瓶颈吧，先不展开了）：

> Application performance is limited by:
>
> - Memory Bounds
> - ALU Bounds
> - TMU (Texture Mapping Unit) Bound
> - BW (Bandwidth) Bound

注：不同的系统有不同的GPU流水线结构，后面在需要的时候可以进行补充学习。



其他的一些渲染架构：

![image-20240127171314675](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127171314675.png)

其中下面的那个Tiled-Based GPUs是移动端的架构，图像是分块渲染的。这里和Games202讲的应该有重合之处，后面有需要会进行补充。有时间也可以去了解下Direct3D 12的架构。



## 3.Renderable

（1）Mesh Component

之前有说,GO由Component组成,这里面就有一个类似于Mesh Component(有的引擎可能叫SkinnedMeshComponent等，在这个Component中我们存了一个叫**Renderable**的结构，**原则上我们希望拿到这个Renderable就可以绘制出所需要的对象。**

这时就需要数据来存储这些结构,在现代引擎中往往通过记录`Vertex Data`以及面片的`Index Data`来实现(注:比如打开obj格式文件观察就可以看到类似现象.)

示意图如下:

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810222533373.png" alt="image-20220810222533373" style="zoom: 67%;" />

在存储顶点的时候，**注意存储顶点的法线方向**,因为有可能插值面法向得到的顶点法线方向在有硬表面(存在折线)的情况下会出问题，比如Cube。



（2）Material

- 除了上文的Mesh,还要存储**模型的材质信息**,在现代引擎的绘制系统中往往只定义视觉材质,而不去定义物理相关的材质(关于物理材质,指的是比如摩擦系数，弹性多少等，后面会展开说)。常见的材质系统有比如Phong模型，PBR模型，Subsurface Material——Burley SubSurface Profile等

（3）Texture

- 比如Albedo,normal,metallic,AO贴图等,也很重要；

（4）Shader

- 着色器代码也是一种重要的Renderable的数据；



## 4.在引擎中绘制物体

注:现在的游戏引擎中会尽可能地把绘制交给GPU来运算而不是CPU。

先复习一下Games101中提到的空间变换:

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810223806264.png" alt="image-20220810223806264" style="zoom: 80%;" />

### (1)Submesh & pool

我们对渲染系统提供一个GO的相关数据(比如Vertex Data,Index Data,Shader,Textures等)，进行绘制。不过这样有一个问题就是**一个GO不一定是单一的材质组成的**(比如一个人不同部位用不同材质)，此时就要用到**SubMesh**的概念。这样就可以进行SubMesh的分段处理，具体结构如下:

![image-20220810224117308](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810224117308.png)

接下来要考虑，如果不同的物体共用了某些资源或者Shader，要如何节约空间呢？这就引入了**Resource Pool**。比如把所有的Mesh放在一起，所有的Texture放到一起，形成各自的Pool，在需要用到某个Pool中的资源的时候就只需要提供索引即可。下面这张图就包含了这个过程。



### (2)Instance

实例化,比如说在生成一千个人(千人律者?)的时候，每个人其实都是把资源进行实例化得到的结果。**实例化的思想在游戏中十分重要**,在制作引擎的时候一定要区分好定义和实例的关系。Pool和Instance的关系如下:

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810224859243.png" alt="image-20220810224859243" style="zoom:67%;" />

像游戏中的墙壁这种GO，还有子弹击中墙壁的音乐音效都算是Instance。



### (3)批处理的思想

很多时候在场景中，我们要绘制许多完全一样的物体（包含一致的submesh和material），此时就可以用到GPU Batch Rendering。伪代码如下:

```c++
struct batchData
{
    SubmeshHandle m_submesh_handle;
    MaterialHandle m_material_handle;
    std::vector<PerInstanceData> m_per_instance_data;
    unsigned int m_instance_count;
}
Initialize Resource Pools;
Load Resources;
Collect batchData with same submesh and material;

for each BatchData:
{
    Update Parameters();
    Update Textures();
    Update Shader();
    Update VertexBuffer();
    Update IndexBuffer();
    Draw Instance();
}
```



## 5.可见性裁剪

culling的最基本思想:判断物体的包围盒是否在视锥体内即可(比如一个Frustum).

### (1)各种包围盒的示意

![image-20220810225937313](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810225937313.png)

常见比如AABB是轴向包围盒,以及常用做物理计算的凸包.

**这种视觉裁剪可以和之前所说的空间划分联系在一起,比如BVH Culling**:

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810230309301.png" alt="image-20220810230309301" style="zoom:67%;" />

好处是可以直接从上到下进行询问：比如根节点是否需要culling，如果需要的话子节点都直接裁掉了，否则再往子节点上走,提高效率。BVH在场景物体发生变换的时候具有比较好的改变结构的效率,所以在游戏引擎中大量使用。**BVH会比较适用于管理许多动态物体的场景**。

todo：后面有空整理一下BVH是如何进行动态更新的？



### (2)PVS(Potential Visibility Set)思想

一个直觉上比较简单的算法,执行效率也比较高,先用一个BSP-Tree构建起场景,并将场景划分为一个一个的"房间"，每个房间之间通过一个portal相连接。然后计算在某一个"房间"结点的时候，最多可以观察到哪几个结点，然后只对最多能观察到的结点进行渲染即可。示意图和伪代码如下:

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810230831089.png" alt="image-20220810230831089" style="zoom:67%;" />

<img src="E:/%E7%B1%B3%E5%93%88%E6%B8%B8/%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E/games104/games104%E7%AC%94%E8%AE%B0/Games104%20%E7%AC%94%E8%AE%B0%20%E6%B8%B8%E6%88%8F%E5%BC%95%E6%93%8E%E6%9E%B6%E6%9E%84(1).assets/image-20220810230843168.png" alt="image-20220810230843168" style="zoom:67%;" />

实际上，这里需要的编程能力还是比较高的。虽然现代引擎中很少直接使用PVS算法,但是其相关的思想还是很有用的,比如在一些3A大作中,虽然玩家感受到的是开放世界,但制作者还是制作了一个比较线性的流程,这个时候就可以设置一些`portal`,使得玩家在一个区域的时候只去加载其能看到的区块,这样不仅方便场景管理也很方便资源的加载过程。

> 补充：现在BSP Tree用的好像不多了，后面真有需要再整理吧。



### (3)GPU Culling

现在很多culling都直接用GPU来做,里面涉及一些比较深的技术,比如可以直接让显卡返回01二进制串,表示哪个物体要culling,哪个要保留,在以后工作的时候可能需要频繁跟显卡打交道。

**Early Z技术**（High-Z技术）

> 当像素数量过多的时候,可以先绘制一遍场景(此时不做渲染),只是把深度绘制出来,如果深度测试过不去直接不绘制相关内容,这样自然后面也不需要渲染了。复杂一些的会使用Hierarchy来进行Z的处理，但基本思想大同小异。



## 6.纹理压缩 Texure Compression

游戏里的纹理需要进行压缩,不能直接用JPEG这种压缩算法(因为没办法随机访问,比如访问JPEG格式的(100,100)像素点,可能会出问题)。所以引擎处理贴图的时候往往会将其分块(比如4×4),然后分别进行压缩处理.以下介绍Block Compression思想:

![image-20220810232220379](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810232220379.png)

对于每一个4×4的块,找到最亮和最暗的点,其他点可以认为是这两个值之间的插值(因为很多图片的相邻颜色间有关联度),所以只需要存储离这两个颜色的"颜色距离"并进行编码即可,如上图。**这种Block Compression思想在图形学中十分重要。**这种算法的压缩和解压缩的效率是十分高的。

手机端的压缩算法很多是ASTC这种，并不要求例如严格分块4×4。

> 其他纹理压缩格式补充：[你所需要了解的几种纹理压缩格式原理 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/237940807)
>
> [Compressed GPU texture formats – a review and compute shader decoders – part 1 – Maister's Graphics Adventures (themaister.net)](https://themaister.net/blog/2020/08/12/compressed-gpu-texture-formats-a-review-and-compute-shader-decoders-part-1/)



## 7.Renderable的由来——相关工具

Max，Maya，Blender，ZBrush。以及最近比较火的Scanning实体扫描，还有一些程序化生成的（Houdini，Unreal，这是一个很需要的研究方向）。优劣势对比如下:

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810232907571.png" alt="image-20220810232907571" style="zoom:67%;" />



## 8.Cluster-Based Mesh Pipeline

![image-20240127180420842](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127180420842.png)

看上图，首先会将整个模型分成一个个小的cluster，每个cluster具有固定数目的三角形数量（比如32或者64）。这样做是因为现代的GPU可以基于数据非常高效地创建几何细节，也就是可以凭空”创造“出几何细节。将分成的clusters提供给GPU，GPU对于固定尺寸的cluster处理速度是很快的。我们希望能够在处理的过程当中可以生成不同的细节，甚至可以根据相机的远近来决定细节的程度。可以看到下图中根据相机的远近自适应地决定哪些cluster需要被渲染。

![image-20220810233732857](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220810233732857.png)

后面如果有精力的话可以读一下UE5的Nanite系统，这个系统基于上述的思想更进了一步。

> Nanite：
>
> - Hierarchical LOD clusters with seemless boundary
> - Don't need hardware support, but using a hierarchical cluster culling on the precomputed BVH tree by persistent threads(CS) on GPU instead of task shader.

补充一下现在比较新的图形管线，todo：具体细节后面学的更多了再来整理吧。（注：本来下图当中的Hull和Domain这种应该是Tesselation shader里面的，看图应该是整合进了Mesh Shader当中。暂时还没有看到Unity与Mesh Shader有关的代码或者教程。）

![image-20240127181031335](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127181031335.png)



## 9.Q&A

（1）图形学程序如何Debug?

> 一般来说比较难,虽然现在很多软件有提供Debug的方式,但还是有一定的操作难度.一个比较好的方案是一次不要写太多的代码,而是尝试将任何和算法拆解,在写一部分之后确保这一部分没什么问题再去写下一部分.同时引擎代码也需要程序员有较为丰富的实战经验,来解决问题。



# 六、05 游戏渲染中光和材质的数学魔法

复习渲染方程:

![image-20220811213200968](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220811213200968.png)

在工程实践当中,渲染方程有如下的困难点：

- （1）visibility to lights，比如游戏中的阴影是很难做的，但是又需要去做阴影；
- （2）光本身的属性非常复杂，比如平行光、点光源、spot light、面光源(面光源很复杂)，同时物体和光源交互也很复杂；
- （3）渲染方程的积分项极其难解，很难做到实时性；
- （4）在真实世界中，所有的物体都可以抽象成为光源，这种递归性会使得系统非常复杂；



## 1.简单的解决方案

一个最简单的方案如下:

- （1）用比较简单的光源，比如点光源、spot light、或者方向光等。(设置一个主光源)
- （2）统一用一个ambient light来统一表示环境光
- （3）以上内容在图形学API当中都是支持的，比如OpenGL的`glLightfv`函数

进一步的**可以使用环境贴图**，比如一个cube map作为环境贴图。根据眼睛的角度和法线决定反射方向，然后在cube map中寻找对应的点，仔细想一下这种算法也是符合渲染方程的：

```c++
//cube map solution
int main()
{
    vec3 N = normalize(normal);
    vec3 V = normalize(camera_position - world_position);
    vec3 R = reflect(V,N);
    FragColor = texture(cube_texture,R);
}
```



## 2.材质模型

一个比较简单的经验模型就是**Blinn-Phong模型**。这里也默认规定了光是具有可叠加性的。不过Blinn-Phong模型有如下问题：

- ![image-20220811215847064](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220811215847064.png)

对于左侧的图，正常的结果应该是右面的渲染结果。但由于Blinn-Phong模型能量不保守，因此如果光源打进洞之后可能就会被震荡放大，最终造成左图的错误现象。

另外一个Blinn-Phong模型带来的问题是不够真实，很多时候无法表达现实生活中的物体（右图）。用一句话来说,Blinn-Phong好像做什么都有一种"塑料"的感觉。PBR模型改善了这一点,后面会介绍。



## 3.Shadow

### （1）Shadow map

解决的问题是我看到的场景中的每一个点,到光是否是可见的.(假设光是简单光源,比如点光源,方向光等).

早些时候的一些已经废弃的算法有planar shadow,shadow volume等,在游戏引擎当中我们使用的最多的算法还是**shadow map.**这是一种非常聪明的算法:

> 本质上,shadow map是站在光的角度,对场景物体进行渲染,这里只需要计算深度的信息即可,这个深度就可以体现出点到光的距离,这样在相机位置渲染的时候,每个点都通过反向投影,投影到光源视角下投影到的地方(方法是记录光照空间下的矩阵变换,将此时的判定点也转换到光照空间下),同样得到一个距离.如果得到的距离大于最近遮挡物的距离,说明在阴影中,否则不在阴影中.具体的示意图和算法如下:

![image-20220811221717327](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220811221717327.png)

具体的算法本身可以参考Games的其他系列,以及下面的链接:

[图形学基础 - 阴影 - ShadowMap及其延伸 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/384446688)

[Shadow Map阴影贴图小讲 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/144025113)



### （2）Shadow map带来的问题和解决方案

- 问题:从光源产生的采样率和从相机产生的采样率是不同的,会造成采样精度问题.简单解决方案是加一个bias,但在实际运行效果中可能会出现诸如角色的阴影离地一定距离的问题。额外内容也可以参考上面链接,或者后续展开.

以上的比如Blinn-Phong这种简单模型虽然在现代游戏中使用的不多,但是在一些低配环境或者是手游当中还是有作用的,接下来会学习一些进阶知识。



## 4.上一代3A游戏中的一些解决方案

> 可能有用的参考链接（todo：还没看，先贴着）：
>
> 【1】[游戏中的全局光照(四) Lightmap、LightProbe和Irradiance Volume - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/265463655)，以及该系列的其他文章。

### （1）Pre-computed Global Illumination

这是一种典型的空间换时间的方法。针对一个连续的球面积分的过程，一个可行的思路是将其离散化，这就想到了傅里叶变换。

![image-20220811233740960](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20220811233740960.png)

接下来介绍球谐函数。



### （2）球谐函数 spherical harmonics

参考链接:[球谐函数介绍（Spherical Harmonics） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/351289217)，以及Games202中关于球谐函数的介绍。

![image-20240127205939584](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127205939584.png)

![image-20240127210019661](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127210019661.png)

球谐函数的二阶导是0。

以下是在寒霜引擎中与球谐函数压缩irradiance和重建的PPT（相关链接：[Precomputed Global Illumination in Frostbite (ea.com)](https://www.ea.com/frostbite/news/precomputed-global-illumination-in-frostbite)）：

![image-20240127210400511](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127210400511.png)

![image-20240127210553175](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127210553175.png)

> 补充一下上面这页：可以看到代码中`sh[0]`，`sh[1]`，`sh[2]`分别对应p.y, p.z, p.x, 这个与前面介绍球谐函数的PPT是对应的，SH的一阶在笛卡尔坐标系下的表示就是y，z和x。在实现上，一共只用了12个SH系数（12是因为每个球谐函数系数对应RGB三个值，两阶一共四个系数）。有一个值得注意的细节，就是虽然SH有四个参数，但这四个参数的权重并不同。
>
> - $L_0$相当于对环境光场做了一次加权平均，而现代游戏基本都是HDR的，所以这里$L_0$使用BC6H（H应该指代的是HDR）的压缩方法；
> - 对于$L_1$来说，使用LDR空间下的压缩方法即可。
>
> 进行存储时可以对不同的系数使用不同的精度进行存储，这样任意点的环境光照可以使用RGBA的32bits来表示，换句话说每一点的光场相当于RGBA纹理图像上的一个像素。这样可以用极小的空间来存储环境光照的信息。

**更多这部分的知识可以看看Games202的PRT，思路应该就是PRT的思路。**



### （3）SH Lightmap：Precomputed GI

lightmap正是基于上面的思想而提出来的光照技术。我们可以将场景中每个点的光照离线烘焙到一张纹理图上，然后在渲染时读取纹理值来获得SH表达的环境光照。**可能以后不会有那么多的应用场景了，但思想值得学习借鉴，即把场景信息烘焙到2D Texture上的这种思想。**

![image-20240127211445235](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127211445235.png)

相当于把场景中的几何拍到一张Atlas上，这是怎么做的呢？

（a）首先，对整个世界做几何上的简化。在进行烘焙时不需要使用包含各种细节的网格，我们只需要使用一个精度相对较低的网格并进行参数化即可。

![image-20240127212239555](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127212239555.png)

> 需要把三维空间中复杂的几何投影到二维空间。需要对场景几何进行简化并在参数空间进行分配（这个应该指的是用参数来描述几何信息）。尽可能希望在同样的面积或者体积里分到的texture resolution基本是相似的。用上图来看的话，如果把每个texel标成不同的颜色（上图里的每个小格子），当反向投影会世界中时每个格子大小就会比较均匀。这个还是比较困难的，**后面理解了再做补充吧。**



（b）当美术完成场景建模后就可以开始烘焙了。显然计算lightmap是非常耗时的，但通过lightmap可以实现非常逼真的场景效果，而且在实际渲染时lightmap可以实现场景的实时渲染。

![image-20240127213156587](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127213156587.png)

当然lightmap也有一些缺陷，比如说离线烘焙时需要很长的时间、lightmap无法考虑动态的光源、同时存储lightmap也需要非常大的存储空间（可能几十M或者上百M）。



### （4）Light Probe：Probes In Game Space

除了lightmap外还可以在空间上设置一些**探针(probe)**来记录环境光照，而在计算物体的着色时只需要对附近probe进行插值即可估计该点的光照。当然如何设置这些probe是比较麻烦的。早期的实践中一般是由美术人工进行设置，而目前则可以使用一些自动化的工具来自动生成probe（**这种自动化生成probe的算法也是工业界所需要的**）。

![image-20240127213851234](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127213851234.png)

如上图左侧，在场景中撒上许多的probe记录环境光照，在实际计算的时候使用如右侧两幅图的四面体上的插值算法来计算实际上的光照。右下角其实是个动图，大的球在场景中移动时由于probe的影响会不断改变自身的颜色。

如果要考虑材质的反射行为则**需要设置专门的反射probe。**一般来说这样的反射probe不需要设置很多，但每个probe则需要有更高的精度（因为反射是比较高频的）。如下图：

![image-20240127214322788](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127214322788.png)

light probe同样可以进行实时渲染。不同于lightmap，基于light probe可以实现动态的场景和物体渲染，而且现代计算机的计算性能也允许对probe进行动态更新。优缺点如下：

- 优点：
  - 速度非常快；
  - 可以处理静态物体和动态物体，并且现在的计算机性能允许对probe动态更新；当然一般也不会每帧都更新，可能会用deferred update的策略；
- 缺点：
  - 效果上可能比不上lightMap，这是因为probe的采样比较稀疏；

这里强烈推荐学习一下Unity的Lighting相关的文档：[光照简介 - Unity 手册 (unity3d.com)](https://docs.unity3d.com/cn/current/Manual/LightingInUnity.html)



------



### （5）Physical-Based Material

#### （a）Microfacet Theory

有了光照后我们来考虑材质。基于物理的材质模型大量使用了**微表面理论(microfacet theory)**来模拟现实世界中材质，简单来说微表面理论认为材质的表面是由大量方向各异的光滑镜面组成，这些镜面的分布控制了不同材质的反射行为。

光线在物体表面上的反射可以分解为**体反射(body reflection)**和**表面反射(surface reflection)**两种。在体反射中光子会进入到物体的内部进行反射然后从物体表面的另一个点射出；而在表面反射中光子则会直接被反射出去。实际上物体表面的漫反射行为对应着体反射，我们可以使用Lambert模型进行表示；而表面反射的行为则可以基于微表面理论使用Cook-Torrance模型来进行表达。将二者组合到一起就构成来材质的BRDF。如下图所示：

![image-20240127214747042](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127214747042.png)

（i）Cook-Torrance模型可以拆分为三项。首先是**法向分布函数(normal distribution function)**，它表示材质不同方向上镜面法向的分布情况。法向分布函数包含一个参数$\alpha$来表示表面的粗糙度，$\alpha$越大表示表面越粗糙反射行为越接近漫反射，$\alpha$越小表示表面越光滑反射行为越接近理想镜面反射。**行业里基本上在用GGX模型**，GGX的模型相对于Beckmann的模型有长尾的优点，并且高光部分足够”尖“：

![image-20240127215555227](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127215555227.png)



（ii）Cook-Torrance模型中的另一项是**几何项(geometry attenuation term)**，它表示不同方向镜面的自遮挡行为。在Cook-Torrance模型中使用Smith模型将几何项分解为出射方向和入射方向两个方向上的可见性乘积，每个方向上的可见性使用GGX模型进行计算。

![image-20240127215808851](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127215808851.png)



（iii）Cook-Torrance模型中的最后一项是**Fresnel项(Fresnel equation)**，它表示不同材质光滑表面的理想反射行为。在实时渲染中一般使用Schilick近似来计算这一项。

![image-20240127220320265](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240127220320265.png)

为了获得真实材质的光学参数我们还需要进行实际的测量。[MERL BRDF数据库](https://cdfg.csail.mit.edu/wojciech/brdfdatabase)给出了常见材质的BRDF测量结果。



#### （b）Disney Principled BRDF  

为了方便不同背景的从业者进行使用，Disney提出了著名的**Disney Principled BRDF**来设计不同的材质模型。它的思想是设计材质模型时要尽可能方便艺术家进行理解，而不要过多地使用物理上面的概念。

具体的知识点在Games202的笔记中有进行整理。Disney Principled BRDF最早提出来应该是离线渲染的，不过现在实时渲染界也在追求类似的效果。



#### （c）PBR的两套工作流

（1）SG工作流

![image-20240128100121402](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128100121402.png)

拿到这些数据之后，就可以用下面的shader代码求解着色了（这段shader的代码还是很清晰的）：

![image-20240128100405077](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128100405077.png)

> 注意diffuse项有归一化的$\pi$，别忘了。



（2）MR工作流

在长期的实践中为了防止美术在设计时出错，人们还对SG模型进行了封装并得到了**metallic roughness模型(MR)**。MR模型同样包含三张图：一张base color图表示漫反射、一张roughness图表示粗糙度、还有一张metallic图表示材质的金属度。当metallic值很高时材质会更接近于金属材质产生大量的光泽反射，否则会接近于非金属材质以漫反射为主。

![image-20240128100625027](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128100625027.png)

MR模型不太适合表示介于金属和非金属之间的材质，但**大多数情况下仍然是工程中的首选。**

> 金属度可以这样理解：如果金属度非常低（即非金属类），则颜色并不会进入到Fresnel项当中去；如果是金属的话，base_color会被放入到Fresnel项里面。具体的MR工作流转换到SG工作流的代码在下面这张图里。

todo：似乎SP当中有metallic-smoothness的工作流，等实践一下确认了再把结论放过来。



**两套工作流之间的转换**

![image-20240128100724871](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128100724871.png)

**SG模型和MR模型的优缺点**

MR模型的缺点：在非金属与金属过渡的时候，容易产生一个小的白边。

> MR：
>
> - 优点
>   - 更容易编写，并且更不容易因为提供错误的F0数据而产生很糟糕的结果；
>   - 使用更少的texture memory，这是因为金属度和粗糙图都是灰度值即可存储；
> - 缺点
>   -  在贴图创建的时候非金属无法控制F0的值，不过大多数的实现有一个额外的specular值去override这个4%的默认值。（补充：我记得Unreal是这么做的，todo：待验证）;
>   -  在非金属与金属过渡的时候，容易产生一个小的白边，特别是在低分辨率的时候；
>
> SG
>
> - 优点
>   - Edge artifacts 更不明显；
>   - 可以在Specular贴图当中控制非金属的F0值；
> - 缺点
>   - 因为Specular贴图提供了对非金属F0的控制，所以它更容易受到使用不正确值的影响。如果在shader中处理不当，就有可能打破守恒定律 ；
>   - 由于要使用RGB贴图，因此需要更多的存储空间；



### （6）IBL（Image-Based Lighting）

IBR本身是使用真实图像作为光照的方法，但结合PBR材质可以实现非常逼真的实时渲染效果。这里其实就对应Games202里面的Split Sum方法，在这里就放一下PPT，更详细的可以去202的笔记里面看。

![image-20240128103526849](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128103526849.png)

![image-20240128103926515](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128103926515.png)

对于Diffuse项比较简单，我们首先通过预计算的方法对环境光照按照余弦进行积分，接着把积分后的值存储在一个表格中。实际渲染时进行查表并和漫反射系数进行相乘即可。提前预计算好的Diffuse Irradiance Map如下：

![image-20240128104901263](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128104901263.png)

对于Specular项，则使用Games202提到的Split Sum方法。我们首先需要将镜面反射的积分利用split-sum拆分成**光照项(lighting term)**和**BRDF项(BRDF term)**两部分，而这两项都可以通过预计算的方法事先存储在一个表格中。

![image-20240128105236862](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128105236862.png)



在Lighting term当中，会依据不同的粗糙度存储Cubemap的mipmap（虽然是mipmap的思想，但其实并不是跟普通的mipmap一样的算法，而是每一层级都要单独算出来），这样预计算完之后根据不同的粗糙度α就可以查对应的Pre-filtered environment map了：

![image-20240128105347583](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128105347583.png)

针对BRDF项，Split Sum方法是这样做的：

![image-20240128105848025](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128105848025.png)

这样最后把漫反射项和镜面反射项加起来即可得到完整的环境光照，如下图所示：

![image-20240128110115262](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128110115262.png)

可以看到，开启IBL可以让游戏的画面得到质的飞跃。



### （7）Classic Shadow Solution

cascade shadow是实时渲染中阴影的经典处理方法。它的思想是根据距离来调整shadow map的精度，近处的精度高远处的精度低。

Cascade Shadow的步骤如下：

![image-20240128110518719](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128110518719.png)

当然想要得到合理的阴影效果需要大量的技巧（dirty hack），而且cascade shadow需要大量的存储空间在计算上也需要大量的时间。比如说一个经典的挑战是如何在不同的cascade层级当中做blend操作：

![image-20240128110812507](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128110812507.png)

Shadow Cascade的优缺点如下：

- 优点：
  - best way to prevalent（消除） errors with shadowing: perspective aliasing
  - 快速产生深度图，3x up when depth writing only；
  - 产生很好的效果；
- 缺点：
  - 几乎不可能产生高质量的区域阴影；
  - 绘制的成本较高，shadow往往至少要绘制4ms左右，这对于游戏渲染一共给30ms来说还是挺头疼的。
  - 没有彩色阴影。半透明的表面会投射出不透明的阴影；



### （8）PCF、PCSS和VSSM

现在很多是引擎的标配，用来做软阴影的效果。这一部分也可以看Games202的课程。下面贴一张VSSM的图：

![image-20240128112207891](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128112207891.png)



总结一下，上个世代3A游戏的渲染效果一般由如下几部分组成（差不多6-12年前的游戏效果）：

- Lightmap + LightProbe
- PBR（SG+MR） + IBL
- Cascade shadow + VSSM/PCSS



## 5.Moving Wave of High Quality

随着各种shader模型的提出以及硬件计算性能的进步，上面介绍的实时渲染算法已经不能完全满足人们对画质的需求。GPU的发展是很迅速的，可以看下图：

![image-20240128112547659](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128112547659.png)

**实时光线追踪(real-time ray tracing)**就是一个很好的案例。随着显卡性能的提升我们可以把光线追踪算法应用在实时渲染中从而获得更加真实的光照和反射效果。

![image-20240128112720389](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128112720389.png)

> 大概就是显卡帮我们构建好了一个空间加速结构（BVH树），打出一个ray，就会用回调函数告诉我们是否有打到物体，然后我们用回调函数进一步处理逻辑。现在的游戏一般都用实时光追做一些反射效果之类的。



另一方面**实时全局光照(real-time global illumination)**也取得了很大的进步。这几年各种实时全局光照算法层出不穷，基于全局光照可以给游戏画面带来质的飞跃。

![image-20240128113026143](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128113026143.png)

在后面会专门对lumen进行介绍。



在材质渲染方面，随着geometry shader的出现人们可以获得几乎无限的几何细节。同时大量基于BSSDF的shader使得人们更准确地描述物理材质与光线的相互作用。

![image-20240128113232366](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128113232366.png)



### Virtual Shadow map

在虚幻5引擎中还使用了virtual shadow map来生成更加逼真的阴影。

这里我们先来回顾一下Virtual Texture的思想：把游戏里所有需要的纹理都pack到一张巨大无比的纹理上（virtual texture），要用的时候把它调出来用，不用的时候卸载掉。在Lecture 06中也会详细一些地介绍Virtual Texture地概念。

Virtual Shadow map的思想也是类似的。首先用算法去算哪些地方真的需要shadow map，密度是多少；接着在Virtual Shadow map上去分配对应的空间，一小块一小块（tiled）去生成shadow map；等到用camera渲染的时候能够求出要取哪个shadow map的值，并进一步进行运算。（todo：依然等后面有时间了补充一下具体实现）

Virtual Shadow map应该可以部分解决shadow cascade费时间，空间利用率高的问题。

![image-20240128113926345](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128113926345.png)



## 6.Shader Management

本节课最后讨论了游戏引擎中的shader管理问题。在现代3A游戏中每一帧的画面上可能都有上千个shader在运行。这些大量的shader一方面来自于美术对场景和角色的设计，另一方面不同材质在不同光照条件下的反应也使得程序员需要将不同情况下的shader组合到一起。

在Shader的管理上，一般来说程序需要写一个Uber Shader，里面用宏把各种情况分出来。因为GPU讨厌分支，所以这些分支都会被编译成铺天盖地的shader；

![image-20240128114459112](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128114459112.png)

比如说写了165个uber shader，可能会生成出75536个shader。



另外一个shader比较头疼的东西，就是跨平台编译，很麻烦。

![image-20240128114829213](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128114829213.png)

现在有开源工作在帮助我们在各个平台编译shader（todo：后面再看吧）。在写shader的时候，建议一开始就尝试编译成vulkan等其他版本，这样可以避免针对不同的平台再写一套。



# 七、06 游戏中地形大气和云的渲染 Part 1

现实世界中有着丰富的自然场景，如果只使用简单的绘制程序则很难给予玩家真实的游戏体验。因此在本节课中我们会介绍3A游戏中使用的自然场景渲染技术。

## 1.地形渲染landscape

目前的3A游戏中已经可以生成逼真的地形环境渲染效果。以微软的模拟飞行为例，最新一代的模拟飞行已经基本实现了真实地球的地貌绘制，此外基于地形绘制技术我们也可以生成其它星球的地形和地貌（如《无人深空》）。

### （1）Simple Idea——Heightfield

![image-20240128130512674](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128130512674.png)

表示地形最简单的方法是使用**高度场(heightfield)**。我们可以把地形看做是平面上具有不同高度的函数，然后通过在平面进行均匀采样来近似它。这种方法在遥感等领域仍然有着很多的应用。

> 很多自然界的东西都具有分形的特点，这个特性可以很好地辅助我们的开发。

高度场的缺陷在于当我们需要表示大规模的地形或者需要更精细的地形时所需的采样点数会成倍的增长。如果一平方米画一个格子的话对于开放世界来说就是灾难（存储空间太大了）。不过这里有下面的解决方案（基于LoD的基本思想）。

> 对地形的LoD技术需要很小心，因为地形是“连续”的，所以需要精心设计。



### （2）Adaptive Mesh Tessellation  

在游戏引擎中由于玩家观察的**视野(field of view, FOV)**是有限的，实际上我们不需要对所有的网格进行采样，只需关注**视野中的地形即可。**在这种思想下人们提出了两条采样原则：

- 首先是根据距离和视野来调整网格的疏密，对于不在视野范围内或是距离观察点比较遥远位置的地形无需使用加密的网格；
- Error Compare to Ground Truth（pre-computation）：另一条是在对地形进行采样时要考虑对网格进行加密或者化简后地形高度的误差不要超过一定的范围（因为采样点数量会改变，这个阈值是在视空间上，比如差一个像素），我们希望近处地形的误差尽可能小而远处的误差可以大一些。

下面这张图很形象地描述了相关算法的核心思想：

![image-20240128131242183](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128131242183.png)

可以看到，在FOV内侧的三角形分的十分密集，在FOV外部和远处的三角形则比较稀疏。随着FOV越来越窄（比如开六倍镜），表现在屏幕上就会显示更多的细节，此时三角形就要更精细。

**在考虑LoD的时候一定要考虑FOV带来的影响。**



#### （a）Triangle-Based Subdivision

对三角网格进行加密操作可以通过**三角网格剖分算法**来实现。对于均匀分布的网格，其中每个三角形都是等腰直角三角形。因此在进行剖分时可以直接选择三角形的斜边中点将它剖分成两个一样的小等腰直角三角形。显然这样的剖分方法等价于为二叉树添加叶节点。

![image-20240128132152843](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128132152843.png)

在进行剖分时还需要注意**T-junction**的问题：当我们对某个三角形进行剖分后必须同时将与它具有相同邻边的三角形同时进行剖分，否则会有顶点落在其它三角形的边上。

![image-20240128132618253](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128132618253.png)



利用现代GPU的计算性能和上面介绍的三角剖分算法就可以实现大规模场景地形的实时渲染。更多详情可以参考Unity在Siggraph 2021上的一篇工作：[Experimenting with Concurrent Binary Trees for Large Scale Terrain Rendering (youtube.com)](https://www.youtube.com/watch?v=0TzgFwDmbGg)


#### （b）QuadTree-Based Subdivision  

在游戏行业中更常用的高度场表达方式是使用**四叉树来表达地形**。这种方法更符合人的直觉，同时也可以直接使用纹理的存储方式来存储这种四叉树的结构。

![image-20240128135232438](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128135232438.png)

比如在实际开发中，可能一个block的大小是512m×512m，分成16个块（每块64m×64m），每块称为一个patch。最后实际应用上这项技术之后的效果如下：

![image-20240128135658478](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128135658478.png)

> 最后一张图里不同颜色的区域分块的密度是不一样的，但本质上都是基于quad做地形分割的。实际开发中，可以把一块512×512区域的heightfield，贴图，植被，建筑全部打包到一起，这样可以一次把该区域的全部数据加载上来。QuadTree方法暗含资源管理的思想在里面。



**quad-tree同样需要考虑T-junction的问题。**不过在quad-tree中可以通过将三角形顶点之间吸附到其它顶点上的方法来简化处理。

![image-20240128140339899](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128140339899.png)

#### （c）Triangulated Irregular Network（TIN）

在很多场景中均匀采样的地形会造成一些存储空间的浪费。实际上对于高度变化不大的区域只需要少量的三角形就可以进行表达，而对于高度变化剧烈的区域使用数量更多的三角形来还原地形的细节。

![image-20240128140748011](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128140748011.png)

可以看右边那幅图，比较平缓的区域用比较大的三角形，可以大大减少三角形的数量。不过这个技术并没有得到广泛的应用，了解即可。



### （3）Hardware Tessellation

利用现代GPU的强大计算能力我们可以把地形的细化完全放到GPU上进行实时计算。在DirectX 11中提供了hull shader、tessellator以及domain shader等工具来网格的实时细分。

![image-20240128150158757](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128150158757.png)

下面这张图可能更好理解这里的shader的作用：

![image-20240128150239953](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128150239953.png)

在更新的DirectX 12中则将这些概念合并到mesh shader中，通过mesh shader来实现全部的网格细分功能，从而极大地方便来游戏开发和图形程序。

![image-20240128150605150](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128150605150.png)

todo：有时间摸一下DX11和DX12的pipeline。关于tessellation的shader可以参考CatLikeCoding的教程：[Tessellation (catlikecoding.com)](https://catlikecoding.com/unity/tutorials/advanced-rendering/tessellation/)

此外还可以利用GPU的计算性能实现动态的地形绘制，从而进一步提升玩家的游戏体验，如下图：

![image-20240128151500192](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240128151500192.png)

> 这里最好跟着一些教程实现一些用tesselation能做的效果，比如草地渲染，雪地交互这种，具体的文档在学完对应的效果之后也会给出链接。



## 2.Non-Heightfield Terrain

有些游戏场景如洞穴可能无法使用高度场来进行表示。一个简单的Hack如下图所示：

![image-20240129141136563](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129141136563.png)

可以标记哪些地方是要挖的洞，然后对应的位置让顶点着色器输出NaN，这样GPU就不会渲染对应的三角形面片，从而达到挖洞的效果。



### （1）Crazy-Idea Volumetric Representation

虽然现在游戏里目前用的很少，但感觉还是有一定借鉴意义的。对于这种场景可以考虑使用体素来表达场景的几何，然后利用marching cube算法来生成表面。

> 在计算机图形学中，voxels常用于表示体数据，例如在医学成像中用来捕捉关于组织、器官或其他结构的信息。在科学模拟中，它们可以用来模拟三维空间中的物理现象，比如流体动力学或地质形态。此外，在三维建模和游戏开发中，有时会使用voxels来构建环境和物体，实现对复杂三维形状的高效表示和操作。
>
> 体素（voxel）类似于三维空间中的像素，但与二维像素不同，它们通常不直接包含其在空间中的具体位置信息。换句话说，虽然体素表示了三维空间中的数值，但它们的坐标位置通常不会被直接编码在体素的数值中。这种设计方式使得体素可以更灵活地用于表示三维空间中的数据，而不需要在每个体素上显式地存储其具体位置信息。

如下图：

![image-20240129141854335](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129141854335.png)

三维空间的每个点会存储一个权重值（比如0-16），用来存储空间这个位置是否有物质，以及物质的密度。这里就可以引出下面的Marching Cube算法。



**Marching Cube算法**

关于Marching Cube算法的基本介绍，可以参考这篇文章：[Marching cubes算法 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/561731427)。

![image-20240129142611453](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129142611453.png)

当然这种方法目前仍处于试验阶段，几乎没有游戏使用相关的技术来表示地形。主要也是因为要考虑的情况实在是太多了。



## 3.Terrian Texture

有了地形绘制的系统，接下来就是与地形相关的材质了。有了地形的几何表示后就可以为它添加纹理细节进行渲染。如下图：

![image-20240129143050848](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129143050848.png)

右上角那张贴图是一张混合贴图，每个channel对应一种材质的权重。这里就引发了一个新的问题，**如何更好地做材质的混合？**以下提供几种做法：
（1）Simple Texture Splatting：直接做混合，但这样会有问题，比如下图里蓝色圈内的部分，会有一个柔和的过渡，但是并不真实（因为沙子应该在石头缝里而不应该“浮于”石头表面），正确的自然界效果应该如右侧那两张图所示。

![image-20240129143358002](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129143358002.png)



（2）Advanced Texture Splatting

![image-20240129143806189](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129143806189.png)

> （这个链接是[Advanced Terrain Texture Splatting (gamedeveloper.com)](https://www.gamedeveloper.com/programming/advanced-terrain-texture-splatting)）
>
> 根据链接中的内容，蓝色线代表sand的depth，红色线代表石头的depth。注意，石头的顶部比沙子高。浅一点的线表示blend的权重。Height Maps+Alpha Blending对应图里的深色蓝线和红线表示Height map的值+blend权重之后的值；

左上角的方法：

- 用height对混合后的颜色进行调整。如果发现要做blend，height高的话相当于混合占比下降的就慢一些，height低的话很快退掉。

  - 可以想到，用这种方法的话石头比较高，“消失”的就比较慢；而沙子比较低，混合占比下降的会快，这样就会有一个层次的感觉，而不是单纯的blend；

  - 其实这个算法是这样的（似乎跟上面不太一样，不过可能思想差不多，实际需要的时候再看看吧）：
    ```glsl
    float3 blend(float4 texture1, float a1, float4 texture2, float a2)
    {
        return texture1.a + a1 > texture2.a + a2 ? texture1.rgb : texture2.rgb;
    }
    ```

    其中texture1和texture2的alpha通道存储的是高度，而a1和a2则对应opacity map里两者分别的混合系数

右下角的方法：

但是随着计算逐像素进行，artifacts开始出现在纹理之间的边界上。为了使结果平滑，我们将在深度上取几个像素而不是一个像素并混合它们。（属于是trick了，不理解也没事，用了效果好就行，有空得多关注关注这些trick）

```glsl
float3 blend(float4 texture1, float a1, float4 texture2, float a2)
{
    float depth = 0.2;
    float ma = max(texture1.a + a1, texture2.a + a2) - depth;

    float b1 = max(texture1.a + a1 - ma, 0);
    float b2 = max(texture2.a + a2 - ma, 0);

    return (texture1.rgb * b1 + texture2.rgb * b2) / (b1 + b2);
}
```

简单理解就是当高度差没有到0.2的时候，不要非石头就是沙子，而是用权重做一个插值，这样过渡的时候还是会有一个albedo的混合，效果也就更自然。



### （1）Sampling from Material Texture Array

当需要对多种不同材质进行混合时还可以使用texture array来管理不同材质的混合关系。注意要把Texture Array和3D Texture做区分。这个看下图里的Texture Array的示意图就能看出来了：

![image-20240129165129900](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129165129900.png)



### （2）Parallax and Displacement Mapping

![image-20240129165558180](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129165558180.png)

注：有时间复习一下视差映射。



### （3）Virtual Texture

这些方法效果是不错，不过还有一个问题要考虑。之前有提到对2D纹理进行采样是昂贵的（mipmap+双线性插值），因此直接对地形纹理进行混合时容易造成计算上的性能问题，如果没有设计好渲染管线则会导致渲染效率的下降。这就引出了Virtual Texture的思想。

Virtual Texture的核心思想：**只把需要的加载到内存中，不需要的进行卸载。**

在现代游戏引擎中大量使用了**虚拟纹理(virtual texture)**的技术来提高渲染性能。使用虚拟纹理时首先需要把纹理分解成若干个尺寸相同的tile，然后不同LOD的纹理则需要事先进行烘焙存储在硬盘上。在实际渲染时根据绘制目标的精度来决定所需的LOD以及对应的tile，然后将需要进行渲染的纹理tile加载到内存中作为实际的纹理贴图。这样的方式可以极大地缓解纹理读写的内存需求从而提高渲染效率。先看下图加深理解：

![image-20240129170936220](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129170936220.png)

现在引擎中基本会使用Virtual Texture的方法。这里为了加深理解贴一些相关的链接，值得看一下：

> 【1】[浅谈Virtual Texture - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/138484024)
>
> 【2】官方的PPT：[Microsoft PowerPoint - GTC_2010_Virtual_Textures.pptx (nvidia.com)](https://www.nvidia.com/content/GTC-2010/pdfs/2152_GTC2010.pdf)

**不过这个实现上有点太硬核了，目前觉得能够理解思路即可。**



显然虚拟纹理的性能瓶颈在于从硬盘加载纹理的IO过程。想要进一步提高效率甚至可以直接让GPU从硬盘进行加载。

![image-20240129182743618](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129182743618.png)

- DirectStorage：硬盘到内存，内存到显卡的加载过程使用的是压缩了的数据，在显卡上进行解压缩，这样可以充分利用显卡的性能，同时没那么消耗内存；
- DMA：直接通过GPU从硬盘加载纹理；



### （4）注意：浮点数精度溢出

![image-20240129183123225](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129183123225.png)

使用浮点型的时候，当表示的数值特别大的时候，误差也会因此变得特别大（回忆一下IEEE的浮点数表示法）。这种问题在游戏里挺常见的，比如下面这个原神视频（慎点）：[世界终焉！到达五百万米高度后，提瓦特开始崩坏？_原神 (bilibili.com)](https://www.bilibili.com/video/BV1f14y1e7vf/?spm_id_from=333.788.recommend_more_video.1&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)

一种解决方案是**Camera-Relative Rendering**，将相机设置为世界坐标的中心。

> 浮点数的绝对精度随着数字变大而减小。这意味着游戏对象的坐标距离场景原点越远，其精度就会变得越来越低。远处游戏对象的网格面可能出现在同一位置，并产生z-fighting伪影。为了解决这个问题，Camera-Relative Rendering用相机的位置取代了世界原点。
>
> 可以参考这篇文章：[Unity大世界虚拟仿真渲染问题笔记 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/165062873)

![image-20240129184657255](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129184657255.png)



## 4.其他的渲染专题

这一部分提到的渲染并不会讲细节，但后面可以自己作为专题来学习。（所以暂时看不太懂也没事）

（1）树渲染：近处用mesh表达，远处的话用插片的技术来展示，越远越稀疏，直到很远的时候就是billboard（并且billboard一次就会一大批）；植被渲染的中间件推荐speedtree；

（2）Decorator（草，小树丛，小石子这种） Rendering：尽量用简单的mesh来表达，具体技术后面再看吧；

（3）道路系统：最常见的实现方法是使用Spline绘制。不过比如拉出一条山路之后又要修改高度场。另外还有decal（比如弹孔），常见的做法是把道路和decal都拍到virtual texture上，这样提前bake好了，真正渲染时就比较快，如下图：

![image-20240129191847070](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129191847070.png)

现在很多是用程序化的方法来做地形。



# 八、06—2 游戏中地形大气和云的渲染 Part 2

这一部分介绍大气和云的渲染。**注：这一节实在是太硬了，有些东西应该还没搞懂，后面再补充吧**

## 1.Atmosphere

### （1）传统的拟合方法

![image-20240129214925786](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129214925786.png)

这样做的好处是很简单，坏处则是无法实现从天空垂直下落时的这种视觉效果，而且由于所有的参数都是写死的，因此可控性也比较差（比如美术想实现下雨的天，就不太能实现）。

**这个方法效果并不是特别好，接下来的做法则全程高能。。。。。。**



### （2）Participating Media

![image-20240129215316170](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129215316170.png)

大气可以抽象成由两种主要物质组成：

- 气体分子：比如氮气，氧气，二氧化碳，甲烷等；
- 气溶胶（aerosol）：指的是空气中的灰尘，或者是其他气溶胶的分子，也会对空气形成折射和反射；



### （3）光和Participating Media是如何交互的？

![image-20240129215645171](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240129215645171.png)

- Absorption：空气中的杂质会吸收光，这个公式是说每往前走一个单位距离，会被吸收一定的光，$\sigma_a$是一个参数；
- Out-scattering：光打中粒子之后，会像四面八方进行散射。这也是一个与光的方向有关的量；
- Emission：假设是高温气体（如火焰），或者闪电，会有自发光。在实际项目中可能不用考虑这一项，不然太复杂了；
- In-scattering：非常复杂。周围粒子的out-scattering也会打到待计算的例子，因此需要计算一个球面积分。

把上述的四种合到一起，就形成了RTE方程。在上面的PPT中写的是一个一维方程，不过实际上在三维空间中应该是一个梯度方程。（后面有需要再说吧，公式应该不用记，理解思想即可）

> 基于**辐射传输方程(radiative transfer equation, RTE)**我们可以得到出射光线的radiance在指定方向上的微分。



通过对RTE沿光路进行积分，我们可以得到光线穿越介质后的radiance。这个方程也称为**体渲染方程(volume rendering equation, VRE)**。

![image-20240130094151265](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130094151265.png)

> 上图这么理解（可以结合上图的英文）：
>
> 原则上就是从M点开始，一步一步算光被吸收的部分，散射出去的部分，in-scattering的部分。这个时候会产生两个值：
>
> - Transmittance（通透度）：在M点看到的东西（比如蓝色的）大概有多少会保留到在P点看到的东西（这是路径积分的结果）
> - Scattering Function：在传播的时候，叠加了沿途的所有粒子，他们通过各种散射最终达到P点，这个沿着光路路径的积分就是Scattering部分；

对之前的RTE积分得到的结果就是VRE，后面会用预计算的方式算好，所以也不用看推导了。



### （4）Scattering

两种不同的散射模型如下：

![image-20240130100429991](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130100429991.png)

> - Rayleigh 散射：当空气中的介质尺寸远小于光的波长的时候，就几乎会向四面八方均匀散射（其实还是会有一点方向性，见后面的图）。对于越短的波长散射的越厉害（蓝光，紫光），越长的波长散射的越小（红光）。
> - Mie 散射：尺寸接近或者大于光的波长的时候，就有一定的方向性。一般沿着光的方向会更强一点，但对波长不敏感（不管什么波长都一视同仁）



#### （a）Rayleigh 散射

首先来看Rayleigh散射：

![image-20240130100806935](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130100806935.png)

看右上角那幅图，可以看到短波（蓝光）辐射度比较大，长波（红光）则辐射的比较小。可以用下面的Phase Function来拟合Rayleigh散射：

![image-20240130101039666](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130101039666.png)

看起来很复杂，但可以拆解成两部分。

- （1）首先是Phase Function，这个其实就是对应右面那个花生的形状；
- 可以看到公式里引入了光的波长$\lambda$参数，当波长越短的时候散射的强度S越大；$\theta$指的是和光之间的夹角（scattering angle，各向同性）；$h$是海拔高度（因为大气的浓度在海拔为0的时候最大，越往上越稀疏），$N$是标准单位体积里的空气密度。
  - 这样就可以实现那种开飞机从上往下降落时的大气变化效果了
- （2）对Scattering Coefficient项来说，给定海拔高度和空气密度，这个值就是一个常数。

总结：当光线发生Rayleigh散射时太阳光中不同波长的色光会发生不同程度的散射。具体而言短波长的蓝光会出现大量的散射行为，而长波长的红光则只会发生少量的散射。这样的现象就导致了白天我们观察天空时眼睛会接收到来自四面八方散射的蓝光，因此天空呈蓝色；而在日出或是傍晚时太阳很斜，很多蓝光直接散射到大气外面了，此时蓝色的部分越来越少，红色的部分越来越多，此时天空呈红色（吸收现象也会导致天空呈现红色）。可以看这篇文章加深理解：[体积渲染(三): 瑞利散射(Rayleigh Scattering) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/351502720)



#### （b）Mie 散射

![image-20240130105118404](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130105118404.png)

Mie散射则与Rayleigh不同，散射的形状如右侧图所示。可以用下面的公式对其进行拟合：

![image-20240130105213997](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130105213997.png)

在上面的公式中：

- （1）Scattering Coefficient和Rayleigh差不多，也是和海拔高度，空气密度有关系，可以当成一个常数；
- （2）右侧公式主要由$\cos\theta$和$g$组成，$g=0$的时候Phase Function会退化成Rayleigh的形状，而当$g>=1$的时候就会越来越接近Mie本来的形状。当$g<0$的时候往光线相反方向散射的会更多（但一般不太用，一般用的时候$g>0$，$g$是一个美术可以调整的参数）

我们日常生活中常见的雾气和光晕都是Mie散射的结果。

- 比如说雾是空气中的小水珠形成的，算是气溶胶，而雾是白色的就是因为白色的太阳光照下来，所有波长无差别散射，就会形成白茫茫的雾。
- 对于日晕来说，因为Mie 散射有方向性，所以看到的光会汇聚到眼睛上，所以太阳旁边会看到光晕的现象。



#### （c）Variant Air Molecules Absorption

除了散射外，在大气渲染时还需要注意不同的气体分子对于不同波长的光线有着不同的吸收行为。比如臭氧和甲烷都是吸收长波的高手（比如海王星表面有很多甲烷，因此光线照过去之后红光都被吸收，就会呈现蓝色）。在制作大气的时候需要考虑吸收的现象，不过我们一般会假设大气中这些吸收的物质是均匀分布的。



#### （d）Single Scattering vs. Multi Scattering

![image-20240130110213171](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130110213171.png)

看下面这幅对比图能够更好的理解：

![image-20240130110415202](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130110415202.png)

可以大致看到，对于山的背面来说，如果不考虑Multi Scattering，则北面是没有任何光的，所以是纯黑色。而实际上应该考虑Multi Scattering，由于空气当中的多次散射，山的背面也是会接收到部分光的。注意这个概念要和GI区分开，因为这个现象不是由光线打到物体造成的，而是由Participating Media造成的。

**后面我们会逐步解决这里的问题。**



### （5）Ray Marching

基本思路：沿着一条射线，把沿途的效果一步一步积分起来。**实际上计算所有的大气效果的时候用的都是这个思路。**

![image-20240130113233015](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130113233015.png)

这里的T应该指的是transmittance，即前文介绍的通透度。可以用空间来换时间，把复杂的计算预先算好并存在一张表上。**这就是Precomputed Atmospheric Scattering的基本思路：**



### ==（6）Precomputed Atmospheric Scattering（这部分后面的Atmosphere还没整理）==

![image-20240130113712079](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130113712079.png)

图里的链接是[ebruneton.github.io/precomputed_atmospheric_scattering/](https://ebruneton.github.io/precomputed_atmospheric_scattering/)。回忆一下大气中的光学现象分为两个重要的部分：

- transmittance：通透度
- scattering

在Precomputed Atmospheric Scattering方法中，**对于transmittance项**，可以针对地球表面的任何一个点计算海拔高度**，并针对这个海拔高度存储两个值（结合上面左图来看）：

- （1）视线和天顶之间的夹角$\theta$；
- （2）从当前点往大气层去看，因为在计算transmittance的时候并不需要知道太阳在哪里，因此从当前点一路出发直到大气层的边界（上图的B点位置），此时就可以计算出$T(X_V->B)$的通透度了。

上图中的$X_V$指的是眼睛所在的位置，$X_M$是中间的一个点。有上面右图的表存储了$T(X_V->B)$，另外根据$X_M$的位置计算一下$T(X_M->B)$，两者相除就是对应要求的transmittance。

> **太抽象了。。。。需要看代码**



对于单次散射的情况，我们同样通过预计算的方法将散射参数化为海拔高度、观测角度以及太阳角度的函数。![image-20240130115335132](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130115335132.png)

看上图当中的$\eta, \phi, \theta$角的定义，这三个角不共平面，当正午太阳在最上面的时候$\mu_s$是1，傍晚的时候则为0。$\phi$指的是我的视线和太阳之间的夹角，

**注：todo：Atmosphere还没有整理完，太硬核了，后面再说吧。**



## 2.Cloud

### （1）早年的表示方法

#### （a）Mesh-Based Cloud Modeling

![image-20240130134235717](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134235717.png)

美术放一些Mesh表示大概要什么形状的云，然后用一些noise+腐蚀算法真的形成云的几何。基本没有人用的方法。



#### （b）Billboard Cloud

使用Billboard创建大量云的插片，并用alpha的混合来做，如下图：

![image-20240130134250689](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134250689.png)

这种方法比较古老，但似乎《原神》中就有这样的云，后面也会介绍一下对应的实现。



### （2）Volumetric Cloud Modeling

![image-20240130134301551](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134301551.png)

目前3A游戏一般会使用体积云的方式来对云进行渲染，尽管它有着比较高的计算复杂度但却可以实现逼真的渲染效果。以下介绍体积云实现的核心思路。



#### （a）Weather Texture

![image-20240130134315037](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134315037.png)

体积云使用一张名为Weather Texture的贴图，该贴图由两部分构成：

- （1）云在空间上的分布；
- （2）会用texture存储一个0-1之间的值，代表了云的厚度。

这样的话如果要移动云，就只需要平移Weather Texture对应的区域，如果要对云有所扰动也可以通过对Weather Texture进行扰动来实现。



#### （b）Noise Functions

![image-20240130134327821](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134327821.png)

有两个很重要的噪声，分别是Perlin Noise和Worley Noise。Perlin Noise可以模拟这种棉花丝的感觉，而Worley Noise相似于Voronoi Noise，可以用来拟合一些絮状的东西。这些Noise都是shader里面的老朋友了。



#### （c）Cloud Density Model

![image-20240130134344095](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134344095.png)

最左面这张图是没有Noise的，可以看到效果很糟糕。而对其用各种各样的noise进行腐蚀（各种加减操作，核心思想是用各层的noise咬掉一些低频的细节，然后再添加一些高频的噪声），此时就能形成比较像云的效果。



#### （d）Ray Marching渲染体积云

![image-20240130134358537](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240130134358537.png)

主要分为以下四个步骤：

- （1）当眼睛往天空看的时候，就沿着每个像素打出光线，看能否和“云”相交。
- （2）我们假设云在统一的高度，所以一开始会尽可能走比较大的step，直到hit到第一个云，开始用小的step，直到走出云；
- （3）在云的内部的时候，计算每个step到的点的通透度和散射等参数。在云中计算这些参数的技术比Atmosphere要简单一些（因为云的通透度比较低，可以做大量假设，对方程进行简化），具体看后面的详细介绍。（云的颜色还会受到大气的影响）

注意，Ray Marching并不会形成一个真的面片，而是一个存在GPU里的虚拟的texture，我们是用ray marching的方法将其解析出来。由于方法很expensive，一般会用低的速率进行采样。

> todo：体积云是一个值得动手尝试实现的效果，更详细的内容和实现会单独整理出一篇文档，并贴在这里。



## 3.Q&A

（1）体积云的渲染有什么优化方案？

- Ray Marching渲染的时候是很费的，有很多hack的方法：
  - 比如对屏幕进行下采样，然后渲染完之后再Blur
  - 使用大力水手DLSS技术

（2）大气散射计算的终止条件是什么？

- 差不多multi-scattering可能算了三次轮迭代就可以停止了。



# 九、 07 游戏中渲染管线、后处理和其他的一切

## 1.Ambient Occlusion

在07节，游戏中渲染管线，后处理和其他的一切。在这里介绍一下Games104的AO部分。**王希是这样说的：重要的不是公式，而是学习到的思想和方法。**

![image-20240202105359397](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202105359397.png)

很多时候会使用离线烘焙AO贴图，如下图：

![image-20240202105413713](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202105413713.png)

但这样的问题是无法Real-time实时进行AO的运算，因此诞生出了很多其他的算法，用于AO的实时计算，比如SSAO, HBAO, 等。注：现在这种离线烘焙的AO贴图依然在游戏中是很重要的。



### （1）SSAO和SSAO+

启发：现在很多的运算都可以基于Screen Space，这个思想是很有用的。

思想很简单：

![image-20240202105809163](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202105809163.png)

对于SSAO来说，实际上采样的N个点不应该在球面上采，而应该在半球面上采。这就是SSAO+；



### （2）HBAO

这个相关的内容在Games202的笔记当中有进行整理。

![image-20240202110030524](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202110030524.png)

部分解决了SSAO+的问题（使用attenuation function，如果距离太远了就不会对AO产生影响）。使用的Ray Marching的算法实现：

![image-20240202110050823](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202110050823.png)

注意事项：

- Fig2：每次采样方向要偏移一点，否则会有Alias的花纹（因为采样率低，会有pattern）；





### （3）GTAO

GT: ground truth，霸气的命名。

![image-20240202110843804](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202110843804.png)

要考虑不同角度来的光线的贡献度，垂直打进来的光线的贡献度较大。GTAO的另一个重要的贡献在于：

- 其基于不同的AO值（比如0.2，0.4），做了大量的数值分析工作，发现AO值和multi-scattering的值是有关联度的，可以用曲线进行拟合（下图右下角），这样后面可以根据AO值估算出光bounce的次数。这样就可以用single-scattering来模拟出multi-scattering的结果。这样就可以让AO也能有颜色（上图最右边）

![image-20240202110907740](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202110907740.png)

> [Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW VERSION_COLOR.pdf (activision.com)](https://www.activision.com/cdn/research/Practical_Real_Time_Strategies_for_Accurate_Indirect_Occlusion_NEW VERSION_COLOR.pdf)



### （4）RTAO

![image-20240202110930008](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202110930008.png)

这个是比较前沿的研究方向。每一个像素打出的sample数量是比较少的，但用一些时序上的方法（应该是类似202讲的TAA）这种进行时间上的复用。



## 2.Fog Everything

最开始的Fog是比较简单的，大概原理就是从眼睛出发，随着距离增加雾的透明度逐渐下降。方法有下面几个：

![image-20240202113014481](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202113014481.png)

Unity的默认Fog选项就是上面这几个，但是这几种Fog的表现力还是不足的。



### ==（1）Height Fog==（没太看懂）

> todo：这个每太看懂，后面再补充吧。

在现实生活中的雾要考虑高度的影响（因为雾是气溶胶，会沉积下来，比如爬山的时候山顶没有雾，但是山脚雾就很浓）。这就引出了Height Fog。

![image-20240202113251464](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202113251464.png)

这里假设Fog有一个最大值。

- 当高度低于某个高度时，下面的所有Fog都是这个最大值；
- 当高于这个高度时，认为Fog的强度是随着指数递减的；

在实际做的时候，往往还是要考虑Ray Marching。



### （2）Voxel-based Volumetric Fog

![image-20240202113742132](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202113742132.png)

这种漂亮的透光效果是不能用上面的Height Fog方法做出来的。体积雾的思路在于：

- （1）将相机可以观察到的空间进行体素化，并且这种体素化不是均匀的，实际上是根据视锥体进行切分的（看上图左上角），离相机近的地方切的很密，离相机远的地方会稀疏一些；
- （2）对体素化之后的grid做Ray Marching，in-scattering，multi-scattering的计算，这里与体积云是类似的。实践中一般也是用一些3D Texture存储中间计算的结果（看上面中间那张图，之所以分辨率是160x90x64是因为很多屏幕的分辨率是16：9的，这样能保证采样出来的结构比较好看，64是深度）



## 3.Anti-aliasing

产生走样的主要原因如下：光栅化相当于对连续的信号进行离散采样。一般有这么几种情况：

- （1）几何导致的：比如几何体的斜边结构；
- （2）纹理采样：反走样可以用mipmap来解决；
- （3）场景中有一些很高频的信号（比如高光），这种也容易产生走样。

Anti-aliasing的核心思想一般是“多采样几次之后取平均”：

![image-20240202114924436](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202114924436.png)

常见的反走样方法下面会介绍。

### （1）SSAA和MSAA

![image-20240202115120556](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202115120556.png)

现在的GPU直接就支持MSAA了，用一个flag就可以开启（所以没有复现的必要了）。不过像三角形无比密集的时候MSAA这个技术就不好用了。



### （2）FXAA（Fast Approximate Anti-aliasing）

![image-20240202122235591](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202122235591.png)

相当于给出一个原始图像，在图像上直接去做抗锯齿，只对边缘的部分进行抗锯齿处理。首先会把图片转为luminance（这个公式常用来把彩色照片转为黑白照片），然后寻找边界点，进行AA操作：

![image-20240202122513044](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202122513044.png)

接下来的步骤就是查看luminance是竖向变化的多还是横向变化的多。上图可以清晰地看到算法的过程，首先先判断要做横向还是纵向，然后再比较两边的邻居哪边更大。在上图中是横向变化多，且右边邻居的更大。此时就得到了一个offset（最右侧红色箭头），指示在做AA的时候要和右边的像素做混合。

接下来的步骤是执行Edge Searching Algorithm。



**Edge Searching Algorithm**

![image-20240202122949938](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202122949938.png)

这一步是FXAA的核心。假设现在要做AA的像素是右上角那幅图的绿色像素，要和上面的像素做blend，于是沿着水平的方向往左往右找一对对的像素（每对像素是一上一下），如果这一对像素之差和当前像素对的差值相差的比较多，**那么就认为找到了“边的端点”。**具体算法上图也有。找到这两个边的端点之后执行下图的算法逻辑：

![image-20240202123755216](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202123755216.png)

将到左边端点的长度和到右边端点的长度作比较，利用相似三角形的原理求出一个blending的权重。并利用这个权重进行blending操作。

![image-20240202124023334](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202124023334.png)

FXAA的速度是很快的。



### （3）TAA

核心思想是复用过去帧的信息，与当前渲染帧进行加权平均。这种思想也是比较常见的。TAA的关键是Motion Vector：记录当前帧的每一个像素点在上一帧的位置，这样就可以跟上一帧做blending了。

一个常见的hack：当物体在高速运动的时候会更多相信当前帧的结果，当基本静止的时候当前帧和过去帧的权重是差不多的。

TAA也是现在游戏引擎中非常常见的技术。TAA的一个问题是要跟过去的图像做blending，所以运动的场景可能会有一个小的偏移。另一个问题是在做不好的时候会出现残影。

![image-20240202124846537](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202124846537.png)



## 4.Post-Process（真正的魔法）

这里介绍几个常见的技术：Bloom，Tone Mapping（调整曝光），Color Grading（调色）。

### （1）Bloom

为游戏提供赛博朋克的感觉。**bloom**是一种非常常见的灯光效果，在光源的四周我们往往可以看到一圈放大的光晕。从物理的角度上讲，bloom的成因在于真实相机的镜头并不符合完美的针孔相机，因此在成像时会出现这样的光学现象。也有说法说跟Mie 散射有关，但这个不重要。重要的是如何把Bloom的效果用于游戏当中。

步骤如下：

（a）找到画面中比较亮的部分：

![image-20240202125756911](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202125756911.png)

这个thresold基本是一个magic number，由于现在游戏基本都是HDR的，所以thresold直接设置为1也不合适。可行的方案比如用平均亮度。

（b）对需要做Bloom的比thresold亮的地方做Gaussian Blur。

![image-20240202125957336](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202125957336.png)

> 一般是第一个pass横着做，第二个pass竖着做，这样可以降低计算量。

实际中往往还会做Pyramid Gaussian Blur：

![image-20240202130205704](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202130205704.png)

直接如（b）的操作做Blur，得到的模糊区域不够大，所以一般会用一个Pyramid，不断对图像下采样，在最低的一阶做blur，并逐步放大回来，和原图加权叠加到一起之后再做下一次blur，从而让blur的区域进一步放大。

> **这种mip或者half resolution的思想在渲染中也十分常见，是一种降低运算量的好方法。**



（c）将最后得到的Bloom的结果叠加到原始图像上，得到最终的结果。



### （2）Tone Mapping

![image-20240202130706021](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202130706021.png)

基本的想法就是把0-HDR很高的值（比如40），通过一个Curve映射回0~1的范围。经典的映射曲线如下：

（a）Filmic Curve

（b）ACES（现在慢慢再往这个上去靠）。同时ACES是来自于电影工业大量专业视觉工作者的总结，使用ACES曲线不仅会让画面更有表现力，而且它对于不同的显示设备都有很好的支持。

![image-20240202131215688](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202131215688.png)



### （3）Color Grading

**颜色分级(color grading)**是游戏设计者非常常用的一种调色方法，它的本质是建立一个颜色到颜色的映射从而获得不同的画面表现效果。

![image-20240202131605722](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202131605722.png)

![image-20240202131645617](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202131645617.png)

对于这个LUT，最直观的想法应该如上图左，存一个`256*256*256`的3D Texture，来找到对输入RGB值的输出。工业界实际并不需要这么大的分辨率，可能`16*16*16`就够了。当然也可以像右侧图那样拍成一张2D Texture来使用。



## 5.Rendering Pipeline

### （1）Forward & Deferred

最简单的pipeline如下：

![image-20240202133902658](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202133902658.png)

上图这个就是Forward Rendering。另外还有Deferred Rendering。两者的说明如下：

（1）Forward Rendering：绘制顺序是很重要的，一般是先绘制不透明物体，再绘制天空盒，最后由远及近绘制透明物体。透明物体还是有点麻烦的，比如扔手雷爆炸产生的烟就是透明物体，对这些烟的排序就会比较困难。

```c++
for n meshes:
	for m lights:
		color += shading(mesh, light)
```



（2）Deferred Rendering：现在游戏场景往往都是多光源的，因此延迟渲染现在用的越来越多了，逻辑如下：

```c++
# Pass 1 
for each object:
	write G-buffer;
# Pass 2
for each pixel:
	gbuffer = readGBuffer(G_Buffer, pixel);
	for each light:
		computeShading(gbuffer, light)
```

![image-20240202134623272](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202134623272.png)

优点：

- 渲染很容易Debug

缺点：

- G-buffer的使用还是很费的；



### （2）Tile-Based Rendering（Forward+ Rendering）

产生的源头是因为在移动端，对发热是很敏感的（存储芯片是最容易发热的）。

![image-20240202134905387](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202134905387.png)

一小块一小块进行渲染，这样可以减少对frame buffer的读写压力。这样带来的另外一个好处是可以把光给culling到每个tile当中。

![image-20240202135040554](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202135040554.png)

更进一步地，其实在第一步渲染深度的时候，可以知道每个tile的Zmin和Zmax，这样对于每个点光源来说，就可以更好的知道其会覆盖到哪些tile，从而能高效处理光照。

![image-20240202135310690](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202135310690.png)



### （3）Cluster-based Rendering

针对上图的改进，直接对深度也进行切分（这样就不用算上面的zmin，zmax了），形成一个个的cluster：

![image-20240202135516824](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202135516824.png)



### （4）Visiblity Buffer

在渲染中，其实可以把几何信息和材质信息分离开。目前游戏工业还发展出了基于V-buffer的渲染管线。V-buffer与G-buffer类似，但在V-buffer中储存的是像素的深度和面片信息，而在实际渲染时根据每个像素对应的几何信息来进行绘制。这样的渲染管线更加适合如今越来越复杂的几何场景。

关于Visibility Buffer的更多信息，可以看这个问题：[(96 封私信 / 80 条消息) Visibility Buffer有什么缺点，有可能代替G-buffer吗？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/340549627)；

![image-20240202161325305](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202161325305.png)

这个后面获取可以深入了解一下。



### （5）Real Rendering Pipeline

todo：后面有时间看看UE的[UE4 Render Pipeline | 十三 (xianlongok.site)](https://www.xianlongok.site/post/f83cc9a1/)



## 6.Frame Graph

在商业游戏引擎的渲染系统中，除了需要包含各种先进的渲染算法外还需要考虑如何对各种算法有序地进行管理。以虚幻引擎为例，整个渲染管线中包含了大量的可选算法，在实际渲染时需要进行相应的调度使它们按顺序进行执行。同时，像Vulkan和DirectX 12等现代图形API往往开放了大量的GPU底层接口进行编程。这使得程序员可以高效地实现对硬件计算资源的管理，但相应的如果开发时不够谨慎则容易造成整个系统的崩溃。

为了便于整个开发和渲染流程，游戏工业目前尝试使用**frame graph**这样的技术对整个渲染过程进行管理。它的思想是把整个渲染过程所需的算法和各种资源表示为一张**有向无环图(DAG)**，这样就可以通过对图的管理来实现不同资源的调度。当然frame graph这样的技术仍在探索阶段，但我们可以期待它在今后整个游戏工业界的表现。

![image-20240202163250986](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202163250986.png)



> Unity的SRP管线就类似于这个Frame Graph的概念，我们可以把所有的feature变成模块，提供给程序员进行配置。比如Unity的URP和HDRP管线就是基于SRP的，这个思想还是值得学习的。



## 7.Render to Monitor

当我们在GPU完成渲染后就需要把渲染的结果输出到显示屏幕上。这里需要注意的是当显示器的刷新频率和GPU的输出频率不一致时会产生画面割裂的情况（因为引擎的刷新频率是不一定的，复杂的场景可能帧率会低一点，但显示器的刷新频率是固定的），看起来就像是屏幕上下两块有一个错位，学名叫Screen Tearing。

为了克服这样的问题人们开发出了**V-Sync**技术，它会强制显示器等待GPU的输出结果（等framebuffer写完）再整个绘制frame buffer，这样就可以避免画面的不一致。当然V-Sync也带来了一些新的问题：在场景发生变化时画面的帧率会忽快忽慢影响玩家的游戏体验。如下图：

![image-20240202164206138](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202164206138.png)



### （1）Variable Refresh Rate

目前一些硬件厂商提出了**variable refresh rate**的概念，让显示器画面的刷新率可以由GPU根据需要来动态设置。

更多详情可以看这篇：[(96 封私信 / 80 条消息) 游戏显示器中的 GSYNC 与 FreeSync 技术原理是什么？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/590782271)



## 8.Q&A

（1）TAA如何去除鬼影？

- 有很多trick，Games202应该是有提的，比如连续两帧像素值相差太多就不信之前的结果了。



# 十、08 游戏引擎的动画技术基础

动画系统是游戏引擎的重要组成部分。从远古时代开始，我们的祖先就试图用各种手段让静止的画面动起来。直到近代，人们发现利用人眼的”视觉残留”效应可以将静止的画面产生运动的效果。这一发现构成了所有显示设备和电影动画的理论基础。目前游戏行业所使用的动画技术理论和经验基本都源自于电影行业对动画技术的探索。从早期的2D动画到如今大规模应用的三维动画，整个电影动画工业取得了令人瞩目的进步。

早期的动画主要是由艺术家逐帧手绘来实现，而在今天基于计算机的动画模拟技术已经成为了电影工业的主流。

回到游戏领域，早期的游戏动画都是制作者根据真实图片进行绘制来实现的，这与早期的二维动画异曲同工。后来随着GPU和3D游戏引擎的出现，人们开始使用计算机来直接生成游戏场景中的动画。而在今天的3A游戏大作中，结合真人动捕以及物理仿真的计算机动画已经可以以假乱真的效果。



**Challenges in Game Animation**

- （1）游戏不能预设玩家的行为，因此动画要和gameplay的逻辑有交互性；
- （2）Real-time带来的难点；在很多情况下我们甚至需要考虑游戏场景中有着上万个单位同时进行运动的情况，这样大规模的计算给游戏动画系统的性能造成了巨大的挑战。
- （3）除此之外，玩家对于现代游戏角色的动画也提出了更高的要求。我们希望游戏角色有着更加生动的表情，同时在运动过程中的行为尽可能自然，跟环境也有所互动。3A游戏中现在有一个比较火的研究内容，叫Motion Matching，将很多动作融合在一起，看起来就非常生动。



**课程目录：**

（1）Basics of Animation Technology

- 2D Animation
- 3D Animation
- Skinned Animation Implementation
- Animation Compression
- Animation DCC

（2）Advanced Animation Technology

- Animation Blend
- Inverse Kinematics
- Animation Pipeline
- Animation Graph
- Facial Animation
- Retargeting



## 1.2D Animation Techniques

### （1）Sprite Animation

首先我们来看游戏中二维动画的实现。二维动画是最早的游戏动画形式，直到今天仍然有很多游戏使用二维动画来进行表现。最简单的二维动画称为**sprite animation**，它是将游戏角色的行为逐帧绘制并在游戏中进行循环播放。

为了实现更加生动的表现效果，还可以在不同的视角下对同一动作进行绘制并且在实际游戏中根据需要选择合适的动作帧进行播放。这样就可以利用2D动画实现伪3D的效果。

如下图：

![image-20240202171305661](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202171305661.png)

在现代游戏中sprite animation仍然占有一席之地，很多游戏的特效就是通过预先渲染出的特效帧来实现的。

![image-20240202171351469](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202171351469.png)



### （2）Live2D

目前虚拟主播中大范围应用的**Live2D**技术同样来自于2D动画，通过对一系列图像进行变形就可以实现非常生动的表现效果。Live2D技术的核心是把角色的各个部位分解成不同的元素，通过对每个元素进行变形来实现虚拟人物的不同动作。在放置不同元素时还可以通过对图层顺序的变化进一步提升表现力。

![image-20240202171737888](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202171737888.png)

对于每一个图元则需要事先设置好它的网格来控制形变，这样角色的不同动作就可以通过对网格控制点的运动来进行描述。

![image-20240202171810859](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202171810859.png)

在制作动画的时候只要用关键帧+插值技术就可以了。



## 2.3D Animation Techiniques

**DoF（Degrees of Freedom）**

3D动画所需的技术要比2D动画复杂一些，在介绍具体的动画技术前我们需要先复习一下相关的数学知识。三维空间中物体的运动有**自由度(degrees of freedom, DoF)**的概念，对于刚体而言描述它的运动需要3个平移方向和3个旋转一共6个自由度。



### （1）Rigid Herarchical Animation

最简单的3D动画技术是把角色的不同部位都视为刚体，然后按照一定的层次把它们组织起来。早期的3D游戏就是使用这样的方法来实现三维角色的不同行为。

![image-20240202172330680](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202172330680.png)

这样的问题是当骨骼发生旋转的时候Mesh会穿模。



### （2）Per-vertex Animation

另一种实现三维动画的方法是利用网格的顶点来控制运动，这种技术称为**顶点动画(per-vertex animation)**。此时网格上的每个顶点有具有3个平移自由度，通过对网格顶点坐标的变换就可以实现模型的运动。这种动画方法在人物角色上的应用比较少，但在物理仿真中则相对比较常见。比如说模拟旗帜飘动，一些水流的效果。

![image-20240202172449679](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202172449679.png)

一般会先用物理引擎模拟出顶点动画的偏移值，并存成Texture，再到游戏引擎里面去用。

> 补充：houdini关于VAT的介绍视频：[VAT 1 | What are Vertex Animation Textures (youtube.com)](https://www.youtube.com/watch?v=3ep9mkwiOjU)，实操的案例后面会写成文档，并把文档名字放在这里。



### （3）Morph Target Animation

类似于顶点动画，**morph target animation**同样是利用顶点来控制模型的运动。和顶点动画不同的是，morph target animation不会直接操作网格顶点的坐标而是通过顶点的位置和权重来控制整个网格的行为。morph target animation在表现角色面部表情上有很广泛的应用。

![image-20240202172732972](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202172732972.png)



### （4）3D Skinned Animation

本节课的核心是介绍**蒙皮动画(skinned animation)**的相关技术。蒙皮动画是目前游戏行业最主流的三维动画技术，它通过控制角色内部骨骼的运动来实现整个角色的运动。和刚体动画相比，蒙皮动画可以实现更加真实和自然的运动效果。其核心思路在于针对每个顶点，受其影响的不只是单根骨骼，而是多根骨骼。

蒙皮动画同样可以应用在二维动画上。基于2D蒙皮动画的运动会比刚体动画有更加自然的表现效果，比如下图：

![image-20240202173034233](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202173034233.png)





### （5）Physics-based Animation

在蒙皮动画之外另一大类动画形式是**物理动画(physics-based animation)**。物理动画是完全基于物理法则的动画模拟方法，和蒙皮动画相比需要更加深入的数学物理知识进行描述。本课程中不会过多地介绍物理动画的相关内容。

一些物理动画的基础知识点：

- Ragdoll（布娃娃系统）；
- 布料模拟；
- IK；



## 3.Animation Content Creation

如何获得动画呢？早期的解决方法是由动画师在软件中通过关键帧来对角色的动作进行建模，而目前越来越多的游戏和电影则是通过真人动捕来获得更加自然的运动动画。



## 4.蒙皮动画的实现

接下来我们介绍蒙皮动画的实现细节。从整体上来看，蒙皮动画的实现包括以下5个步骤：

1. 建立网格模型；
2. 建立网格模型附着的骨骼；
3. 为网格上每个顶点赋予骨骼对应的权重（刷蒙皮）；
4. 利用骨骼完成角色的运动；
5. 结合顶点的骨骼权重实现网格的运动。

上述步骤看上去不是很难，但在实际编程中需要多加小心防止出现Mesh爆炸的问题。



### （1）涉及到的空间介绍

要描述骨骼的运动我们还需要引入相应的坐标系统。首先整个游戏世界定义了一个**世界坐标系(world space)**，所有的物体都位于这个坐标系中；对于每个单独的模型，模型自身还定义了一个**模型坐标系(model space)**；最后每个骨骼还定义了一个**局部坐标系(local space)**来描述网格顶点和骨骼的相对位置关系。任意两个坐标系之间的变换关系可以通过3个平移和3个旋转一共6个自由度来表示，这样每个顶点的坐标都可以从局部坐标系变换到模型坐标系再变换到世界坐标系上。

![image-20240202173701723](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202173701723.png)

其中每根骨骼的Local坐标系都是不一样的。我们的动画表达是在local Space上，需要先走一个树状结构一步步变化到Model Space，然后再变换到World Space当中。



### （2）Skeleton for Creatures

在此基础上就可以结合角色自身的特点构建出具有一定拓扑关系的**骨骼模型(skeleton)**，这一般可以通过一棵树来表示。对于类人型的骨骼，整棵树的根节点一般位于胯部（pelvis骨骼）。而对于四足动物等其它类型的骨骼其根部则会位于其它位置。

![image-20240202174116440](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202174116440.png)



### （3）Joint vs. Bone

我们定义骨骼与骨骼之间相连接的部位为一个**关节(joint)**。实际上我们不会直接按照骨骼进行编程，而是利用关节及他们直接的连接关系来表达整个骨骼的运动。在引擎里面操作的骨骼其实都转换为对关节的操作，而关节才是自由度比较高的那个。

在游戏建模中除了常见的四肢外可能还会根据角色的服装和特点来构建更加复杂的骨骼模型。比如说玩家手中的武器就是通过在角色手上绑定一个新的骨骼来实现的。

![image-20240202174748058](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202174748058.png)

> 很多时候眼球的运动就是通过骨骼来实现的。对右侧图来说，角色拿着武器是使用一个武器绑定的joint点来实现的，骑乘动物也是同理。



### （4）Root骨骼的定义

除此之外，在进行建模时我们往往还会定义一个root joint。不同于前面介绍过的胯部骨骼，root关节一般会定义在角色的两脚之间，这样方便把角色固定的地面上。类似地，对于坐骑的骨骼也往往会单独把root关节定义在接近地面的位置。

![image-20240202175056252](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202175056252.png)



### （5）Bind Animation for Objects

很多游戏动画需要将不同的骨骼绑定到一起。最直观的例子就是角色骑马的动画，此时角色和马都有自身独立的动画，而我们需要将它们组合到一起完成角色骑马的动作。要实现这种功能需要设计一个单独的mount关节（人身上有一个mount关节，马鞍上也有一个mount关节），然后通过这个关节将两个模型拼接到一起。需要注意的是在拼接时不仅要考虑关节坐标的一致性，更要保证两个模型的mount关节上有一致的朝向，这样才能实现模型正确的结合。

![image-20240202175355360](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202175355360.png)



### （6）Bind Pose——T-pose vs. A-pose

早期的骨骼建模会使用T-pose作为角色动作的基准。但在实践过程中发现T-pose会导致角色的肩部出现挤压的状况，因此现代3A游戏中更多地会使用A-pose这种姿势进行建模



### （7）Skeleton Pose

完成骨骼建模后，角色的运动就可以通过骨骼的**姿态(pose)**来进行描述。这里需要注意的是表达角色的不同动作时每个关节实际上具有9个自由度，除了刚体变换的6个自由度外还需要考虑3个放缩变换引入的自由度。这3个放缩自由度对于表现一些大变形的动作起着很重要的作用（比如人脸变形和一些比较Q弹的变化）。



## 5.动画系统的数学基础

### （1）2D Orientation Math

在这一节中我们会详细介绍三维空间中如何表示物体旋转这一问题，不过首先我们来回顾一下二维空间的旋转。对于二维空间中的点$(x, y)$，当它绕原点进行旋转时只需要一个旋转角度$\theta$就可以进行描述，旋转的过程可以通过一个旋转矩阵$R(\theta)$来进行表示。

![image-20240202175841700](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202175841700.png)



### （2）3D Orientation Math

#### （a）Euler Angle

三维空间中的旋转要更复杂一些。我们可以把任意三维空间的旋转分解为绕三个轴的旋转，每个旋转都对应一个三维旋转矩阵，这样就可以通过绕三个轴的旋转角度来进行表达。这种描述三维旋转的方法称为**欧拉角(Euler angle)**。欧拉角在很多领域都有大量的应用，比如说飞行器的导航和姿态描述一般都是基于欧拉角的（Pitch，Yaw，Roll），这个在比如做空战模拟系统的时候很有用。

![image-20240202180056040](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202180056040.png)

但是需要说明的是欧拉角有很多局限性：

- （1）比如说欧拉角是依赖于旋转顺序的。在使用欧拉角时必须指明绕三个旋转轴进行旋转的顺序，同样的欧拉角按照不同的顺序进行旋转会得到不同的结果。其实这个从矩阵乘法不具有可交换性就能看出来了。
- （2）欧拉角的另一个缺陷在于**万向锁(gimbal lock)**：万向节本身是让艺术家来做旋转调整的方式，在现实生活当中万向节也有很多应用（比如陀螺仪，相机稳定器）。不过在有些情况下按照欧拉角进行旋转会出现退化的现象，导致物体的旋转会被锁死在某个方向上。数学上的理解如下图：

![image-20240202180817396](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202180817396.png)

- （3）上述万向锁带来的另一个问题就是欧拉角的插值（不能是简单的线性插值）。而且欧拉角旋转的叠加也不是那么简单的。
- （4）欧拉角很难描述绕着任意轴旋转的表达。

在场景编辑的时候，我们会提供欧拉角的方案，使得艺术家更好理解。但在真正做动画的插值的时候，会使用**四元数。**



#### （b）Quaternion

在游戏引擎中更常用的旋转表达方式是**四元数(quaternion)**，它由Hamilton爵士于19世纪提出。我们知道二维空间中的旋转可以使用复数来进行表示。换句话说，二维平面上的旋转等价于复数乘法。类似地，我们可以认为四元数是复数在三维空间的推广。一个四元数$q$具有1个实部和3个虚部$i, j, k$，四元数的运算法则可以看下图：

![image-20240202181449780](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202181449780.png)

补充：如果四元数$q$是单位四元数的话，其共轭就是其逆；

可以证明，任意的三维旋转可以通过一个单位四元数来表示。当我们需要对点$\mathbf{v}$进行旋转时，只需要先把$\mathbf{v}$转换成一个纯四元数，然后再按照四元数乘法进行变换，最后取出虚部作为旋转后的坐标即可：

![image-20240202190614168](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202190614168.png)



**欧拉角转换为四元数**

进一步可以证明用欧拉角表达的旋转都对应着一个四元数的表示。同样地，四元数与旋转矩阵直接也存在着相应的转换关系。

![image-20240202190719492](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202190719492.png)



**Quaternion to Rotation Matrix**

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202190931231.png" alt="image-20240202190931231" style="zoom:67%;" />



**四元数的数学**

使用四元数来表达三维旋转的优势在于我们可以使用简单的代数运算来获得旋转的逆运算、旋转的组合以及两个单位向量之间的相差的旋转量。对于绕任意轴旋转的情况，我们同样可以利用旋转轴和旋转角度的信息来构造出四元数进行表达。

![image-20240202191329700](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202191329700.png)





## 补充：《游戏引擎架构》里关于骨骼的说明，有助于理解后续内容

### （1）骨骼

我们通常会把每个关节赋予0～N-1的索引。因为每个关节有一个且仅一个父关节，只要在每个关节储存其父关节的索引，即能表示整个骨骼层阶结构。由于根关节并无父，其父索引通常会设为无效的索引，例如-1。

#### （a）在内存中表示骨骼

骨骼通常由一个细小的顶层数据结构表示，该结构含有关节数组。关节的储存次序通常会保证每个子关节都位于其父关节之后。这也意味着，数组中首个关节总是骨骼的根关节。
在动画数据结构中，通常会使用关节索引(joint index）引用关节。例如，子关节通常以索引引用其父关节。同样地，在蒙皮三角形网格中，每个顶点使用索引引用其绑定关节。使用索引引用关节，无论在储存空间上（关节索引通常用8位整数）或查找引用关节的时间上（索引可直接存取数组中所需的关节)，都比使用关节名字高效得多。
每个关节的数据结构通常含以下信息。

- 关节名字，可以是字符串或32位字符串散列标识符。
- 骨骼中其父节点的索引。
- 关节的绑定姿势之逆变换(inverse bind pose transform)。关节的绑定姿势是指蒙皮网格顶点绑定至骨骼时，关节的位置、定向及缩放。我们通常会储存此变换之逆矩阵，其原因会在稍后深入探讨。

典型的骨骼数据结构如下：
```c++
struct Joint
{
    Matrix4x3 m_invBindPose; //绑定姿势的逆变换
    const char* m_name; //人类可读的关节名字
    U8 m_iParent; //父索引，或者用0xFF表示根关节
};

struct Skeleton
{
    U32 m_jointCount;  //关节数目
    Joint* m_aJoint;  //关节数组
}
```



### （2）姿势

把关节任意旋转、平移，甚至缩放，就能为骨骼摆出各种姿势。一个关节的姿势定义为关节相对某参考系(frame of reference）的位置、定向和缩放。关节的姿势通常以4x4或4×3矩阵表示，或表示为SQT数据结构（缩放/ scale、四元数旋转/ quaternion及矢量平移/ translation)。骨骼的姿势仅仅是其所有关节的姿势之集合，并通常简单地以SQT数组表示。



#### （a）local space

关节姿势最常见是相对于**父关节来指定的**。相对父关节的姿势能令关节自然地移动。例如，若旋转肩关节时，不改动肘、腕及手指相对父的姿势，那么如我们所料，整条手臂就会以肩关节为轴刚性地旋转。我们有时候用局部姿势(local pose）描述相对父的姿势。局部姿势几乎都储存为SQT格式，其原因将在稍后谈及动画混合时解释。

在图形表达上，许多三维制作软件，如Maya，会把关节表示为小球。然而，关节含旋转及缩放，不仅限于平移，所以此可视化方式或会有点误导成分。事实上，每个关节定义了一个坐标空间，原理上无异于其他我们曾遇到的空间（如模型空间、世界空间、观察空间)。因此，最好把关节显示为一组笛卡儿坐标轴。Maya提供了一个选项显示关节的局部坐标轴，如图11.7所示。

![image-20240202211953169](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202211953169.png)

![image-20240202212037896](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202212037896.png)

> 补充：这里的每个$P_j$应该就是相对于Local space的变换矩阵，即相对于当前关节的父关节。
>
> 在姿势或动画中忽略或限制缩放有许多好处。显然使用较低维度的缩放表示法能节省内存。(使用统一缩放，每动画帧每关节只需储存1个浮点标量;非统一缩放需要3个浮点数;完整的3×3缩放/shear矩阵需要9个浮点数。）限制引擎使用统一缩放，还有另一个好处,它能确保包围球不会变换成椭球体（ellipsoid)，而使用非统一缩放则会出现此情况。避免了椭球体就能大幅度简化按每关节计算的平截头体剔除及碰撞测试。



**在内存中表示关节姿势**

如前所述，关节姿势通常表示为SQT格式。在C++中，此数据结构可以是以下这样的。

```c++
struct JointPose
{
	Quaternion m_rot;
    Vector3 m_trans;
    F32 m_scale;  //仅为统一缩放
};
```

如果允许非统一变换，则可以这样定义关节姿势：
```c++
struct JointPose
{
	Quaternion m_rot;
    Vector3 m_trans;
    Vector3 m_scale;  //非统一缩放
    U8 m_padding[8]; //不知道是什么，但暂时不重要
};
```

整个骨骼的局部姿势可表示如下，当中m_aLocalPose数组是动态分配的，该数组刚可容纳匹配骨骼内关节数目的JointPose。

```c++
struct SkeletonPose
{
	Skeleton* m_pSkeleton;  //存储关节数目+关节数组
    JointPose* m_alocalPose; //多个局部关节姿势
};
```



#### （b）把关节姿势当作基的变更（重要）

![image-20240202213126026](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202213126026.png)



#### （c）全局姿势（到model space）

有时候，把关节姿势表示为模型空间或世界空间会很方便。这称为全局姿势(globalpose)。有些引擎用矩阵表示全局姿势，有些引擎则使用SQT格式。

![image-20240202213907559](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202213907559.png)

> 注：这里的矩阵是一步步往右乘的，理解思路就行，在本补充部分中矩阵都是右乘的。



**在内存中表示全局姿势**

我们可以扩展skeletonPose的数据结构，以包含全局姿势。当中我们再次基于骨骼中的关节数目动态分配m_aGlobalPose数组:

```c++
struct skeletonPose
{
	Skeleton* m_pSkeleton;  //存储关节数目+关节数组
    JointPose* m_alocalPose; //多个局部关节姿势
    Matrix4x4* m_aGlobalPose; //将关节转到模型空间的矩阵。
};
```



### （3）蒙皮及Skinning Matrix Palette

我们已了解如何用旋转、平移及缩放设置骨骼的姿势，也知道任何骨骼姿势都可以用一组局部($P_{j->p(j)}$)）或全局($P_{j->M}$）关节姿势变换表示。之后，我们会探讨把三维网格顶点联系至骨骼的过程。此过程称为蒙皮(skinning)。

#### （a）每顶点的蒙皮信息

蒙皮用的网格是通过其顶点系上骨骼的。每个顶点可绑定(bind）至一个或多个关节。若某顶点只绑定至一个关节，它就会完全跟随该关节移动。若绑定至多个关节，该顶点的位置就等于把它逐一绑定至个别关节后的位置，再取其加权平均。要把网格蒙皮至骨骼，三维建模师必须替每个顶点提供以下的额外信息:

- 该顶点要绑定到的(一个或多个）关节索引。
- 对于每个绑定的关节，提供一个**权重因子( weighting factor)**，以表示该关节对最终顶点位置的影响力。

如同计算其他加权平均时的习惯，每个顶点的权重因子之和为1。

通常游戏引擎会限制每个顶点能绑定的关节数目。典型的限制为每顶点4个关节，原因如下。

- 首先，4个8位关节索引能方便地包裹为一个32位字。
- 此外，每顶点使用2个、3个及4个关节所产生的质量很容易区分，但多数人并不能分辨出每顶点4个关节以上的质量差别。

因为关节权重的和必须为1，所以最后一个权重可以略去，也通常会被略去。(该权重可以在运行时用$w_3 = 1-(w_0+w_1+w_2)$计算出来。）因此，典型的蒙皮顶点数据结构可能如下:

```c++
struct SkinnedVertex
{
	float m_position[3]; //（px，py，pz）
    float m_normal[3];  // （nx，ny，nz）
    float m_u, m_v; //纹理坐标（u，v）
    U8 m_jointIndex[4]; //关节索引
    float m_jointWeight[3]; //关节权重，略去最后一个
};
```



#### （b）蒙皮的数学

蒙皮网格的顶点会追随其绑定的关节而移动。要用数学实践此行为，我们需要求一个矩阵，该矩阵能把网格顶点从原来位置（绑定姿势）变换至骨骼的当前姿势。我们称此矩阵为蒙皮矩阵（skinning matrix）。

如同所有网格顶点，蒙皮顶点的位置也是在模型空间定义的。无论其骨骼是绑定姿势或任何其他姿势亦然。所以，我们所求的矩阵会把顶点从绑定姿势的模型空间变换至当前姿势的模型空间。不同于之前所见的矩阵（如模型至世界矩阵)，蒙皮矩阵并非基变更(change of basis）的变换。**蒙皮矩阵把顶点变形至新位置，顶点在变换前后都在模型空间。**

##### （i）单个关节骨骼的例子

我们开始推导蒙皮矩阵的基本方程。由浅入深，我们先使用含单个关节的骨骼。那么，我们会使用两个坐标空间：模型空间（以下标$M$表示）及唯一关节的关节空间（以下标$J$表示)。关节的坐标轴最初为绑定姿势(以下标$B$表示)。在动画的某个时间点上，关节的轴会移至模型空间中另一位置及定向，我们称此为当前姿势（以下标$C$表示)。

![image-20240202215343121](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202215343121.png)

**求蒙皮矩阵的“诀窍”在于领会到，顶点绑定至关节的位置时，在该关节空间中是不变的。==因此我们可以把顶点于模型空间的绑定姿势位置转换至关节空间，再把关节移至当前姿势，最后把该顶点转回模型空间。==此模型空间至关节空间再返回模型空间的变换过程，其效果就是把顶点从绑定姿势“变形”至当前姿势。**

![image-20240202215707906](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202215707906.png)

接下来，**在数学上对其进行推导。**

从数学上查看此问题，我们以矩阵$B_{j->M}$表示关节$j$在**模型空间的绑定姿势**，此矩阵会把点/矢量从关节$j$的空间变换到模型空间。现在，考虑一个以模型空间表示的绑定姿势下的顶点$V_M^B$，要把此顶点变换至关节$j$的空间，我们只需要简单地乘以绑定姿势矩阵的逆矩阵，即

$B_{M->j} = (B_{j->M})^{-1}$：
$$
v_j = v_M^B B_{M->j} = v_M^B (B_{j->M})^{-1}
$$
别忘了在补充部分中矩阵是右乘的。这个$B_{j->M}$其实就是我们在（2）（c）中推导的公式，即用骨骼链算出来的矩阵。类似的，我们以矩阵$C_{j->M}$表示关节的当前姿势，那么要把$v_j$从关节空间转回模型空间，只需要把它乘以当前的姿势矩阵：
$$
V_M^C = v_j C_{j->M}
$$
若将$v_j$的展开式带入上式，即可得到把顶点直接从绑定姿势变换到当前姿势的方程：

![image-20240202220656037](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202220656037.png)



##### （ii）扩展至多个关节的骨骼

![image-20240202220956447](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202220956447.png)



##### （iii）引入模型空间到世界空间的变换

![image-20240202221228950](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202221228950.png)



##### （iv）把顶点蒙皮到多个joint

![image-20240202221447964](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202221447964.png)

**只能说《游戏引擎架构》这本书写的是真好，直接看Games104课程这个地方一直看不懂，看书就会了，醍醐灌顶。**



## 6.joint pose

> 想理解好这一部分，要先看《游戏引擎架构》这本书的动画系统——骨骼部分。已经整理到上一节的补充模块里面了。

### （1）Affine Matrix

有了三维旋转的表达方法后我们就可以利用关节的姿态来控制角色模型的运动。具体来说，我们每个关节的姿态可以分为平移、旋转和缩放三个部分，把它们组合到一起就可以通过一个**仿射矩阵(affine matrix)**来描述关节的姿态。

- 大部分的关节变化都是旋转，所以旋转是比较核心的部分。
- 那么Position的属性能否发生变化呢？答案也是可以的，比如角色在下蹲的时候Pelvis相对于Root的position就会发生变化，还有比如人的面部，一些机关结构都会涉及子节点相对于父节点的position变化。

![image-20240202192220824](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202192220824.png)



- Scale参数一般不会变，但是在捏脸系统里也是会用到的。

因此，结合了平移，旋转，缩放参数的矩阵如下（注：旋转矩阵的每个元素用四元数的系数来表示）：

![image-20240202192359343](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202192359343.png)



### （2）Local Space to Model Space

**这部分开始数学公式会比较逆天，这里的笔记会结合《游戏引擎架构》这本书加深理解**

一般的动画其实都是**存储在Local Space里面的变化（即相对于父joint的变化）**。这样做的好处在于：

- 很多动画其实只动了少量的骨骼，可以减少存储量。
- 如果是存储在模型空间下，插值会出问题。可以参考下面这张图：

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202193149076.png" alt="image-20240202193149076" style="zoom:80%;" />

在Model Space下做插值的话，骨头长度都会发生变化。

对于骨骼上的每一个关节，我们实际上只需要存储它相对于父节点的相对姿态。这样在计算绝对姿态时可以利用仿射矩阵的传递性从根节点出发进行累乘即可。

![image-20240202193610165](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202193610165.png)



### （3）Skinning Matrix（==这一节看前面的《游戏引擎架构》说明==）

在前面我们介绍过模型mesh的每个顶点是附着在骨骼上的，因此在关节姿态发生变化后顶点会跟着关节一起运动。

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202194109524.png" alt="image-20240202194109524" style="zoom:80%;" />

记顶点$V$在关节$J$定义的局部坐标系下的坐标为$V_b^l$，初始时刻进行绑定时$V$在模型坐标系下的坐标为$V_b^m$（上标表示在哪个空间里面，下标表示绑定时的位置）。核心思想在于在$t$时刻，当关节位姿发生变化后顶点在关节$J$定义的局部坐标保持不变。如下图：

![image-20240202195305966](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240202195305966.png)

后面内容看前面补充的《游戏引擎架构》里面的部分把，对应Skinning Matrix的推导写的非常好。



## 7.Interpolation

在动画制作过程中一般只会记录下一系列关键帧上骨骼的姿态，而要得到实际的动画还需要通过插值来获得中间帧上模型的运动。根据《游戏引擎架构》中的内容，其实这里不只是在时间上需要考虑插值，**动画混合**也需要对应的技术。

动画混合(animation blending)是指能令一个以上的动画片段对角色最终姿势起作用的技术。更准确地说，混合是把两个或更多的输入姿势结合，产生骨骼的输出姿势。比如说混合角色受伤时的动画和角色未受伤时的动画，就可以得到不同负伤状态下的动画。

动画混合也可以用于求出**不同时间点**的两个已知姿势之间的姿势。当我们要取得角色在某时间点的姿势，而该时间点并非刚好对应动画数据中的采样帧，那么就可使用这种动画混合。我们也可使用时间上的动画混合——通过在短时段内把来源动画逐渐混合至目标动画，就能把某动画圆滑地过渡至另一动画。

补充：Clip：A sequence of skeleton poses。

接下来的问题是，如何在两个pose之间进行插值。

### （1）Linear interpolation

对于translation和scale来说，用线性插值LERP就可以做插值了。

### （2）Quaternion Interpolation of Rotation

#### （a）NLERP

![image-20240203104544463](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203104544463.png)

- 左上角的图：NLERP其实就相当于在LERP的基础上加了一个归一化的过程。使用Quaternion而不是使用欧拉角进行插值。
- 右上角的图：**最短路径原则，**即从旋转1插值到旋转2，人的直觉一般是沿着最短路径，所以需要先做一个判断，避免沿着一个超过180°的方向做插值。（不做这个判断的话关节可能会有错误的翻转）
- NLERP的问题：在角度空间速度变化不均匀，两侧的速度比较快，中间速度比较慢。

解决方案是使用SLERP。



#### （b）SLERP

![image-20240203105115569](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203105115569.png)

基本思想是把两个旋转之间的夹角$\theta$找到，并用这个$\theta$角进行插值，这样可以控制速度是均匀变化的。不过这个插值由于要进行反三角函数运算，因此比较费。而且当$\theta$值比较小的时候，$\sin \theta$也很小，作为分母并不稳定。**因此在实践中往往用magic number，如果两个旋转角差值很小的时候，直接用NLERP就行，否则差值比较大的时候才用SLERP。**



## 8.Simple Animation Runtime Pipeline

我们把上面介绍过的算法整理一下就得到了一个简单的蒙皮动画管线如下。

![image-20240203105812731](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203105812731.png)

现代3A游戏在此基础上还会更多地把计算配置到GPU上来充分计算资源，也就是尽量把前面的步骤也放到GPU上面去算。或许[joeante/Unity.GPUAnimation: Simple but very fast GPU vertex shader based animation system for Unity.Entities (github.com)](https://github.com/joeante/Unity.GPUAnimation)这个关于Unity的GPU Animation方案会有帮助。



## 9.Animation Compression

**动画压缩(animation compression)**是计算机动画中非常实用的技术。实际上直接存储每个模型上每个关节的姿态需要占用非常多的资源，因此利用一些压缩技术来减少动画存储空间有着非常重要的意义。

在广泛的实践中人们发现不同关节不同自由度的信号之间有着巨大的差异。以大腿关节为例，在大多数情况下它的缩放自由度都是1而且大部分的平动自由度都是0，它的运动基本都是来自于旋转；而对于手指这样的关节，它的旋转很少但是平动会相对多一些。



### （1）DoF Reduction

因此最简单的动画压缩方法是直接缩减运动的自由度，把关节的缩放和平动自由度直接去掉只保存旋转。

### （2）关键帧

对于旋转自由度我们可以使用**关键帧(keyframe)**来对信号进行离散，然后通过插值来重建原始信号。在离散时还可以利用不等间距采样的方式来进一步压缩信号。一个基本的想法是去掉那些可以通过插值得到的帧，只保留用插值计算出来的结果和真实值相差比较大的帧，并认为是关键帧，代码如下：

```c++
keyframe = {}
for i = 1 to n-1 do
    frame_interp = Lerp(frame[i-1], frame[i+1])
    error = Diff(frame[i], frame_interp)
    if isNotAcceptable(error) then
        keyframe.insert(frame[i])
    end
end
```

上面这种旋转的插值其实不太符合现实中的规律，一般是使用Catmull-Rom Spline进行混合。Catmull-Rom曲线是C0,C1连续的。Catmull-Rom曲线只需要一个锐度参数$\alpha$以及4个控制点就可以获得C1连续的光滑曲线。基于Catmull-Rom曲线可以实现非常高精度的信号离散和重建效果。

![image-20240203112943179](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203112943179.png)



上图里那条蓝色的曲线是真实动画的旋转参数变化矩阵，用红色的Catmull-Rom曲线和关键点就可以近似拟合真实曲线了。（我感觉暂时理解成贝塞尔这种就行）

> 我在看到这的时候疑惑了一会catmull-Rom Spline插值和前面介绍的NLERP,SLERP这些有什么关系？补充一个我的理解：
>
> - 假设我们现在用了两个确定的pose要进行插值，并且所有的旋转、平移、缩放参数都是知道的，那么此时可以用各种LERP算法进行插值（比如NLERP,SLERP），这些方法不只是可以用于插帧两个关键帧之间的状态，也可以用于lerp两个动画的pose；
> - Catmull-Rom Spline插值则指的是我们现在有同一个动画两个key frame，计算中间帧的参数的一种插值方法。看起来这种方法没办法直接混合两个动画资产，要是对两个clip做混合还是得用上面那些lerp的方法去做。



### （3）Float Quantization

进一步压缩数据时还可以考虑使用低精度的存储方式来记录位移信号。比如说可以通过规范化的方法将32位浮点数转换为16位无符号整数来表示，这样虽然损失了一些精度但却可以极大地减少存储空间。

![image-20240203113450162](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203113450162.png)

其实就是把浮点数范围remap到整数的范围，如上面右图。



### （4）Quaternion Quatization

对四元数进行压缩时可以利用单位四元数每一位上数值的范围来进行化简。具体来说我们可以首先使用2个bit来表示四元数的哪一位被丢掉了（丢掉的是最大的那个，那个需要更多的bit来表示所以丢掉，用$\sqrt{1-剩下三个的平方和}$来算），剩下的3位可以分别使用15个bit来进行表达。这样一个四元数可以使用48个bit来进行存储，远小于使用4个float所需的128个bit。

![image-20240203114055652](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203114055652.png)



### （5）动画压缩的问题——Error Propagation

数据压缩必然会导致精度损失的问题。对于一些末端的关节，由于误差传播的效应可能会产生非常大的累计误差。这种现象的直观反映就是模型可能会产生视觉上可见的偏移，而这是灾难性的（因为像武器就是绑定在末端关节上的）。

要缓解这种累计误差首先需要定量化的描述误差。我们可以直接对比数据压缩前后模型每个顶点上的坐标差异，但这种做法的计算代价过于巨大。在行业里我们一般这样定义误差：

![image-20240203114714777](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203114714777.png)

在每个joint中定义两个垂直的点，给一个fixed offset。如果是重要的骨骼则offset给大一些，否则给小一点。这样就可以定量给出压缩前后的误差是多少。

而要缓解累计误差我们可以为不同的关节设置不同的存储精度，或是通过主动补偿的方式来进行修正（上一个joint产生了一个error，下一个joint对其进行反向的补偿，但这样可能会导致在末端骨骼产生非常高频的数据，结果很怪）。

总体而言，对于累计误差目前没有非常完善的处理方法。



## 10.Animation DCC Process

[GAMES104课程笔记08-Basics of Animation Technology - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/05/11/GAMES104-NOTES-08.html#interpolation)，看这个笔记的对应章节以及原视频38分钟左右的部分就行（涉及美术工作流，看视频更好理解）。以下是一些补充。

### （1）Mesh building

美术在做Mesh的时候做的是高模，但是高模不适合做蒙皮和动画。所以一般会用低模做动画。不过为了保证效果，动画师可能会在关节处额外的加几圈mesh（看视频是做了个细分这种），减少奇怪的变形。



### （2）Exporting

在导出动画的时候，要注意root发生位移的情况（比如跳跃的时候root也会发生位移）。在动画里root的移动一般会单独导出成位移曲线（root motion？）供给引擎使用。





# 十一、 09 高级动画技术：动画树，IK和表情动画

这一节讲述现代游戏引擎中的一些实战的技术。

## 1.Animation Blending

基于[DCC流程](https://peng00bo00.github.io/2022/05/11/GAMES104-NOTES-08.html#animation-dcc-process)我们可以获得不同的动画资源，然而这些资源往往是相互独立的，在实际游戏中我们还需要将不同类型的动画混合起来以实现更加自然的运动效果。以角色的跑动为例，人体的跑动包含低速的步行以及高速的跑动两个部分的动画。将两个动画混合起来就可以实现自然的变速效果。

要实现动画的混合非常简单，我们只需要对骨骼的姿态进行插值即可。但和上节课介绍的[关键帧插值](https://peng00bo00.github.io/2022/05/17/2022/05/11/GAMES104-NOTES-08.html#interpolation)不同，在进行动画混合时不仅需要考虑同一组动画关键帧之间的插值，还要考虑不同组动画不同关键帧的插值。对不同组动画的插值就用上一章提到的那些lerp方法就可以了。**不过在lerp的时候还要考虑权重。**

计算插值权重也比不是很难，比如我们可以按照当前角色运动的速度来选择两个相邻动作的关键帧。两个动作的权重即为对速度进行线性插值的权重。

![image-20240203122849465](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203122849465.png)

不过，在进行动画混合时还要考虑**时间线上对齐的问题。**要使插值后的动作更加自然，我们需要动画师在动画建模时将每个动画都按照能够循环播放的形式进行设计。同时，两组进行混合的动画最好要保证角色具有相同的肢体运动频率。这样可以保证混合后的动画更加自然，不会出现角色滑行的结果。**这里又诞生了一个新的问题，就是在blending的时候要分别使用两个动画的哪一帧呢？**

解决方案是对每个动画做一个normalization：

![image-20240203123455513](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203123455513.png)



### （1）Blend Space

上面介绍的动画混合技术主要针对的是角色一维运动（比如从走路到跑步的blend），我们可以基于同样的思想把角色在平面上的运动动画进行混合，进而获得角色不同方向上的连续动画。比如说我们可以把角色向左走路，向前走路，向右走路的动画做一个blend，这种就叫做1D blend space。另外，还可以再加入对移动速度的判断（对应walk&run），这就形成了2D blend space，如下：

![image-20240203132946199](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203132946199.png)

有时动画师会为角色的平面运动建立多个不同的预设clip，在这种情况下直接进行插值是比较困难的。为了解决这种问题我们可以利用Delaunay三角化的方式对平面进行划分，在需要对动作进行插值时首先选择动作所在的三角形，然后再利用重心坐标进行插值即可。

![image-20240203133021841](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203133021841.png)



### （2）Skeleton Mask Blending & Additive Blending

#### （a）Skeleton Mask Blending

除了平面运动外，有些角色的动作可能只依赖于一部分骨骼。以鼓掌动作为例，角色在鼓掌时只涉及上半身的骨骼运动而与下半身无关，因此我们可以把上半身鼓掌的动作融合到其它下半身动作中。要进行这样的处理也十分简单，我们也可以设置一个mask来标记混合动画时需要考虑角色的哪些骨骼。这样就可以单独录制不同的动作然后根据需要组合出新的动作。

#### （b）Addtive Blending

角色动作另一种常见的情况是动作本身只与关节相对姿态有关，而与绝对姿态无关。以点头动画为例，角色在点头时可以有不同的朝向，但在录制动画时只需要一套统一的动画。要处理这种情况则需要在保存动画时指明这个clip是只依赖于相对位姿的动画，在实际进行动画混合时再根据角色当前的姿态叠加上相对位姿。

**使用这种additive blending技术时需要额外注意角色的姿态，尤其要避免角色关节的姿态超过最大值的情况。**



这两种Blending方法的示意图如下：

![image-20240203133627791](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203133627791.png)



### （3）总结

- 1D Blend Space
  - Blend poses based on a single input value
- 2D Blend Space
  - Blend poses based on two input values
  - Triangular blend
- Masked Blending
- Additive Blending



## 2.Action State Machine（ASM）——状态机

在很多时候角色的动作不能直接通过对动画进行插值来获得。以跳跃为例，实际上角色的跳跃动作可以划分为起跳、浮空以及落地三个不同状态。不同的状态之间存在着一定的依赖关系，这会使得我们可能无法通过直接插值的方式来计算角色当前的动作。

实际上我们可以把角色的动作和状态视为图上的节点，这样角色的运动就等价于在不同节点之间进行游走。这种模型称为**动作状态机(action state machine, ASM)**。

剩下的没什么技术上不太知道的内容了，感觉去引擎实战一下即可。看笔记：[GAMES104课程笔记09-Advanced Animation Technology - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/05/17/GAMES104-NOTES-09.html)

## 3.Blend Tree 混合树

这一部分没什么技术上不太知道的内容了，感觉去引擎实战一下即可。看笔记：[GAMES104课程笔记09-Advanced Animation Technology - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/05/17/GAMES104-NOTES-09.html)

一个重点是Additive Blending的概念：

>  角色动作另一种常见的情况是动作本身只与关节相对姿态有关，而与绝对姿态无关。以点头动画为例，角色在点头时可以有不同的朝向，但在录制动画时只需要一套统一的动画。要处理这种情况则需要在保存动画时指明这个clip是只依赖于相对位姿的动画，在实际进行动画混合时再根据角色当前的姿态叠加上相对位姿。
>
> 关于在Unity中如何使用Additive Blending，可以参考[How To Animate Characters In Unity 3D | Animation Layers Explained (youtube.com)](https://www.youtube.com/watch?v=W0eRZGS6dhQ&t=1s)这个教程的中间左右的部分开始。



## 4.IK（Inverse Kenematics）

看笔记：[GAMES104课程笔记09-Advanced Animation Technology - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/05/17/GAMES104-NOTES-09.html)

以下算是对这节内容的补充。

我们目前介绍过的动画系统都是之间利用骨骼和关节的运动学公式来驱动角色的动作，这种方式称为**前向运动学(forward kinematics, FK)**。在很多情况下我们还需要考虑游戏场景对于角色肢体的约束，并且利用这些约束来求出角色合适的骨骼关节姿态，这种动画技术则称为**反向运动学(inverse kinematics, IK)**。IK在游戏中有着非常丰富的应用场景，比如说角色在崎岖不平的地面上行走时我们根据地面的起伏来调整前进的动画。

### （1）Two Bones IK

IK最简单的情况是只考虑角色两块骨骼的运动，然后利用约束来求解关节的姿态。这种问题的解法其实非常简单，我们可以利用骨骼的大小以及场景约束来构造三角形，然后利用几何关系来求解出所需的姿态。当然在三维空间中我们基于上述方法实际上会得到无穷多组解，因此在实际计算中还要引入一些额外的约束来保证解的唯一性。

![image-20240203141605851](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203141605851.png)

### （2）Multi-Joint IK

在IK问题中更常见的情况是链式的关节，此时我们需要求解出末端到达指定位置时每个关节对应的姿态。除此之外，在实际求解前还需要考虑解的存在性。很多时候可能并不存在能够满足需求的关节姿态。这里往往考虑两点：

- 如果把对应骨骼链上所有骨骼都拉直也够不到物体，则无解；
- （容易遗忘的情况）靠近的区域也会有一个盲区。比如说找到最长的一根骨骼B，然后把其他骨骼往最长的骨骼折，如果无法覆盖最长的骨骼则也是够不到的，如下图：

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203142037900.png" alt="image-20240203142037900" style="zoom:67%;" />

另一方面，角色的不同关节往往还具有不同类型的约束（每个joint有自己的活动范围）。在进行求解时需要考虑这些约束，否则会出现角色动作过于扭曲的状况。

总体来看，在三维空间中求解带约束的IK问题是非常复杂的，目前还没有通用的算法来进行实时求解。在现代游戏引擎中一般是通过一些启发式的算法来进行近似求解。

#### （a）CCD算法

**CCD(cyclic coordinate decent)**是目前游戏引擎中求解IK问题最主流的算法。它的求解过程非常简单：在每次迭代中按照关节顺序对当前关节进行旋转，使得末端关节指向目标位置。

![image-20240203143148245](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203143148245.png)

在标准CCD算法的基础上还可以对迭代过程进行优化，比如设置tolerance region控制每次旋转的角度，或是对接近根部关节的旋转施加额外的约束从而保证根部不会出现过大的旋转。或者说比如限制越靠近根节点旋转幅度越小，越靠近叶节点旋转幅度越大。

![image-20240203143426183](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203143426183.png)



#### （b）FABRIK（Forward And Backward Reaching Inverse kinematics）

**FABRIK(forward and backward reaching inverse kinematics)**也是一种经典的IK求解算法。它的思想是在每一轮迭代中进行一次前向计算以及一次反向计算：前向计算时从末端关节向根部关节移动骨骼，而在反向计算时则从根部出发向末端移动关节。通过不断迭代同样可以计算出合适的姿态。

这个FABRIK算法在做毕设的时候有学，具体可以上网找相关资料复习。（比如这篇[IK 运动动力学逆运算的快速，简单迭代算法FABRIK_fabrik inverse kinemetic c++-CSDN博客](https://blog.csdn.net/leon_zeng0/article/details/120386954)）

> 感觉下面这幅图就可以很好地理解FABRIK算法的核心思想：
>
> ![img](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/20210920004840604.gif)

FABRIK可以很容易地考虑关节约束的问题。当关节的转动角度存在约束时只需要把关节转到约束内垂直与目标的方向即可。（**todo：下面这张图没太看懂，但暂时应该不重要吧**）

![image-20240203201322415](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203201322415.png)



#### （c）Jacobian Matrix

实际上在游戏开发中，很多时候会遇到多约束点的情况（比如攀岩时候的四肢末梢）。虽然像FABRIK也提出了一套解决多端约束的方案，但工业界现在算是用的比较多的是Jacobian Matrix的方法。**Jacobian矩阵(Jacobian matrix)**是一种基于优化来求解IK问题的算法，它在机器人学中有着非常广泛的应用。关于Jacobian矩阵的细节我们会在后面的物理系统中进行详细的介绍。

> Jacobian 矩阵还是比较费的。todo：这段暂时先放弃，Jacobian矩阵就没搞懂过，后面看看怎么理解吧。基础概念可以看这个[Jacobian prerequisite knowledge (youtube.com)](https://www.youtube.com/watch?v=VmfTXVG9S0U&list=PLEZWS2fT1672lJI7FT5OXHJU6cTgkSzV2)



#### （d）其他IK方法

Physics-based Method：

- More natural
- Usually need lots of computation if no optimization

PBD(Position Based Dynamics)：

- Different from traditional physics-based method;
- Better visual performance;
- Lower computational cost

Fullbody IK in UE5

- XPBD(Extended PBD)

总体来看IK仍然是非常复杂的问题，在近几年得到了人们越来越多的关注。一些有挑战的工作比如解决IK算完导致的蒙皮穿模现象，在游戏中表现出对危险的预判（比如前面有个栏杆，我们希望的是快到栏杆角色就应该有躲闪的动作了），以及让IK更符合人类的平衡感。



### （3）Updated Animation Pipeline

同时需要注意的是IK也需要整合到动画管线中作为后处理来调整骨骼和关节的姿态。有了IK之后的动画管线如下图：
![image-20240203203915865](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203203915865.png)



## 5.Facial Animation

表情动画是动画系统中的重要组成部分，从人体的生理学基础来讲表情是由面部肌肉的运动来进行控制的。而表情动画的难点在于人的表情变化往往只有非常少的肌肉运动，换句话说不同面部表情之间的差异可能是非常细微的。

### （1）FACS

得益于电影工业对面部表情的探索，人们发现只需要面部五官进行组合就可以表现出不同的表情。这种表达表情的方式称为**FACS(facial action coding system)**，它一共包含46组基本单元。同时由于面部的对称性，实际上在制作表情动画时只需要一半左右的单元就可以表达不同的表情。

![image-20240203204413911](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203204413911.png)



### （2）Key Pose Blending

基于FACS就可以着手制作不同的表情动画了。在表情动画中我们一般是直接使用面部的网格而不是骨骼关节系统来描述表情，不过动画插值的思想和骨骼动画是一致的。

进行表情混合时需要注意直接对面部进行混合往往会得到错误的结果，这是由于人脸在表达不同表情时一般只会用到一小部分面部肌肉，直接对表情进行混合容易造成整个面部发生运动。要解决这个问题也十分简单，只需要存储一个基本表情然后利用前面介绍过的[additive blending](https://peng00bo00.github.io/2022/05/17/GAMES104-NOTES-09.html#additive-blending)技术对表情进行叠加即可。

![image-20240203204645718](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203204645718.png)

如上图，我们为每个AU存储对应区域相对于中性表情下顶点的offset，这样就可以把不同的定点变化合成到一起。（我的理解是一个Blend shape只会影响一个区域的mesh，并且blend shape的大小其实就确定offset的多少）。

不过目前也有一些使用骨骼来表达面部表情的实践。使用骨骼动画的优势在于它比较适合表达面部比较大的变形，比如说嘴巴张开。同时也可以用于眼球的转动或是游戏中常见的捏脸系统等等。



### （3）UV Texture Facial Animation

除了使用网格或是骨骼外，很多游戏也会使用二维纹理图像来实现表情动画，这种方法在很多卡通渲染的游戏中有着大量的应用（比如塞尔达传说旷野之息）。



### （4）Muscle Model Animation

目前在学术界还出现了通过直接对人的面部肌肉进行建模然后实现表情动画的方法。尽管这种方法还没有大规模应用在游戏业界，而且它的计算需求也远高于传统方法，但它却可以实现更加逼真的角色表情。

> 这个方法更多是在影视行业里面使用。



## 6.Animation Retargeting

本节课最后介绍了**动画重定向(animation retargeting)**技术在游戏行业中的应用。在动画制作中动画师往往只会对同一个动作进行一次建模，而在游戏中设计师则希望可把这个动作应用到各种不同的角色中。这种把一组动作从一个角色迁移到另一个角色的技术称为动画重定向，其中已经绑定好动作的模型称为**源角色(source character)**而需要施加动画的角色称为**目标角色(target character)**。

动画重定向最直接的做法是把对应骨骼和关节的动作直接复制过去。当然考虑到源角色和目标角色骨骼之间位置的差异，一般需要对关节姿态进行一定的补偿。

考虑到不同角色之间姿态的差异，在进行重定向时可以只施加**关节的相对运动（相对于binding pose）**。这种做法会得到更加自然以及符合人直觉的动画效果。



综合上面的内容就得到了动画重定向最基本的算法：

- 处理关节旋转时我们考虑关节的相对旋转（相对binding pose）；
- 处理骨骼的平移时则需要根据目标角色骨骼的实际长度进行补偿；
- 而对于缩放的情况则直接按照比例进行缩放；

这样就可以把源角色的动作迁移到目标角色身上。

![image-20240203210249134](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203210249134.png)



在实际工程中人们发现基于上面介绍的算法进行重定向时，由于源角色和目标角色本身骨骼的差异强行迁移动作容易造成目标角色悬空的现象。因此还需要对角色的高度再进行一定的补偿。如果源角色和目标角色的体型相差很多的话还会出现各种诡异的动画。要处理这种情况还需要利用一些IK的方法来进一步修正。

![image-20240203211334010](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203211334010.png)



### （1）不同骨骼结构如何做Retargeting？

比较直接的处理方法是利用骨骼和关节的对应关系来对关节运动进行插值，这样就可以把原始骨骼的动作重定向到新的骨骼上。实际上在Omniverse（Nvidia的）上就使用了类似的方法来处理动画重定向的问题。

![image-20240203211645431](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240203211645431.png)

会发现source Skeleton和Target Skeleton有一些共同骨骼，此时可以把相同的骨骼中间的部分映射到0~1的区间（如右图，target有三根骨骼而source有四根骨骼），然后把target joint中间的骨骼映射到source joint的对应区间，用求解的结果作为retarget的结果。



### （2）Retargeting现存的问题

- 穿模问题；
- 很多动作有一定语义，比如鼓掌。直接做retargeting的话可能导致target的角色在鼓掌的时候手合不起来；
- retargeting之后如何维持角色平衡感。



### （3）Morph Animation Retargeting

动画重定向的技术除了可以应用在骨骼上，实际上还可以应用在表情动画上。当然在迁移的时候由于不同模型尺度的差异，有时会出现穿模等诡异的问题。此时可以对网格施加一些额外的约束来强行获得正确的动画效果。



注：看完动画部分之后，可以复习一下Unity的动画系统：[【Unity动画系统详解 一】四个基本概念【Unity开发入门教程09】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV12Q4y1z7Lv/?spm_id_from=333.788&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)



# 十二、10 游戏引擎中物理系统的基础理论和算法

物理系统是游戏引擎的重要组成部分。在游戏中玩家和整个游戏世界的互动都是依赖于物理系统的实现，同时在现代游戏中大量的粒子效果也都是通过物理系统来进行驱动的。显然物理系统非常复杂，甚至于有很多公司专门去研究物理引擎的高效实现。而在本课程中我们同样把物理系统拆分成两节，这一节课主要介绍物理引擎的基本概念而在下一节课中则会更多地讨论游戏业界更前沿的物理仿真技术。

## 1.Physics Actors and Shapes

### （1）Actor

在物理引擎中根据对象自身的特点我们可以把它划分为静态对象、动态对象等。其中静态对象是指在仿真过程中不会发生改变的对象，比如说游戏中的地面、墙壁等等；与之对应的是动态对象，它们的运动状态会在游戏过程中动态地进行变化，而且它们的运动过程需要符合相应的动力学模型。

Actor可以分为这几类：

- Static Actor：比如说地面的挡板，放在那里不动，大部分游戏里static actor都是主要组成部分；
- dynamic actor：比如可以推动的箱子，符合动力学原理，可以被forces（力）/torques（力矩）/impulses（冲力）影响。这种在游戏里尽量不要太多，因为每帧都要解算。
- Trigger：与游戏逻辑高度相关；
- Kinematic：它是指不完全基于物理法则的物理对象，但往往与玩法高度相关。很多游戏的bug比如物体飞到天上这种往往是由Kinematic造成的。（慎重使用）



### （2）Actor Shapes

物理对象最重要的属性是它的**形状(shape)**。比较规则和简单的形状可以通过解析的方法来进行描述：

![image-20240204110045925](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204110045925.png)

- Sphere的碰撞检测应该是最简单的；
- Capsules：其实就相当于把球拆成两半，中间放个圆柱体；
  - 经常被用于角色；
- Boxes：长方体；
- Convex Meshes：凸包/凸多面体，必须是一个封闭空间的包裹（不能有洞），并且沿着任何面无限延申的话不会与其他面相交（凸包性）。这种能表达的形状会更丰富一些，比如做地形爆炸效果的时候可以用；
- 另外，也可以用triangle meshes和height fields（比如球在地面上弹来弹去）来表达物体对象；
  - 注：Dynamic Actors 一般是不能用triangle mesh的；

在进行物理仿真时我们首先会把物理对象进行一定的包裹，使用相对简单的几何形状来近似复杂的模型。



### （3）Shape Properties

在形状的基础上我们还需要对一些物理量进行定义，包括对象的质量或密度、质心以及物理材质等。在物理引擎里我们假设每个Actor的质量是均匀分布的。一些重要的概念如下：

- 质心：在做载具系统的时候很有用，能提升驾驶感；
- Physics Material：定义表面的摩擦力，弹力等参数。可能不同材质还会和不同的音效关联起来。



## 2.Forces and Movements

### （1）Forces

**力(force)**是改变物体运动状态的原因。在物理引擎中我们同样需要力来驱动整个游戏世界的仿真过程，其中常见的类型包括拉力、重力、摩擦力等。

在游戏世界中还有一种叫做Impulse的力，它比较适合用来模拟物体运动状态发生剧烈变化的情况，比如说车撞人，或者爆炸。



### （2）Movements

有了力或者冲量后就可以利用牛顿运动定律来驱动物体的运动了。

- 牛顿第一定律：当物体不受力的作用时，其会倾向于静止或是保持匀速直线运动。
  - $\vec{v}(t + \Delta t) = \vec{v}(t)$
  - $\vec{x}(t + \Delta t) = \vec{x}(t) + \vec{v}(t)\Delta t$

- 牛顿第二定律：当物体受到力的作用时，其加速度与力呈现正比关系。
  - Mass：物体阻抗力的变化的量；
  - $\vec{F} = m \vec{a}$ （F:Force，m：Mass，$\vec{a}$：Acceleration）
  - $\large \vec{a}(t) = \frac{d\vec{v}(t)}{dt} = \frac{d^2\vec{x}(t)}{dt^2}$

针对牛顿第二定律，此时有下面的推导：

![image-20240204112747277](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204112747277.png)

大部分物理世界的真实运动就上上图右侧那样，力是随着时间发生变化的，这时求解v和x就是一个积分式。



### （3）欧拉方法

#### （a）显式欧拉法

在进行数值积分时，我们可以把时间间隔设置成一个比较小的值然后对被积函数进行累加来近似实际的积分。具体来说，在计算物体的运动轨迹时我们首先计算物体在当前位置上受到的力并且积分得到加速度，然后再利用加速度来更新速度以及物体的位置。这种计算物体运动轨迹的方法称为**Euler方法(Euler’s method)**，也称为**显式积分(explicit integration)**。Euler方法实现起来非常简单，但需要注意的是它的本质是使用物体的当前状态来估计下一时刻的运动状态，此时**系统的能量是不守恒的，**因此求解出的结果很容易不收敛。

![image-20240204114006217](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204114006217.png)



#### （b）隐式欧拉法

为了提高数值积分的稳定性，人们还开发出了**隐式积分(implicit integration)**的技术。隐式积分的实现也很简单，只需要在求解加速度和速度时使用下一时刻而不是当前时刻的值即可，同时可以证明此时系统的能量会不断衰减。当然这又引入了另一个问题，即如何计算系统在下一时刻的物理量，这在很多情况下是比较困难的。

![image-20240204114225535](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204114225535.png)

不过这个方法的好处是能量是能够得以保留的，但是会出现能量衰减的现象。不过一般在游戏中能量衰减也不是不能接受。



#### （c）Semi-implicit Euler's Method（半隐式欧拉法）

在游戏引擎中更常用的积分方法是**半隐式Euler方法(semi-implicit Euler’s method)**，即在计算加速度时使用当前时刻的力推导下一时刻的速度，而在计算位置时使用刚才计算出的速度再更新位置。半隐式方法有非常高的数值稳定性，广泛应用于各种类型的物理仿真中。

![image-20240204114718969](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204114718969.png)

其实就是根据当前受的力（这里的假设是在微小的时间$\Delta t$内，力不会发生变化），根据牛顿第二定律计算出加速度，然后就可以计算出$\vec{v}(t_1)$了，然后再用这个$\vec{v}(t_1)$去计算$\vec{x}(t_1)$。这个方法非常适合让计算机去进行计算，很稳定。



## 3.Rigid Body Dynamics

有了牛顿定律和数值积分算法就可以开始进行物理仿真了，其中最简单的情况是**质点动力学(particle dynamics)**。在质点动力学中所有的物体都被抽象为没有具体形状的质点，此时我们只需要按照牛顿定律更新质点的运动状态即可。

在游戏引擎中更为常见的仿真场景是**刚体动力学(rigid body dynamics)**。和质点动力学不同，刚体动力学仿真需要考虑物体自身的形状，也因此需要在质点运动的基础上引入刚体旋转的相关概念。

两者的对比如下图：

![image-20240204115435022](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204115435022.png)

> 补充：
>
> - 动量Momentum：质量乘上速度；
> - 刚体动力学，这时比如扔出去一个物体这个物体还会自身旋转（这种一般是针对刚体，柔体的话很难）：
>   - Orientation：
>   - Angular velocity：角速度；
>   - Angular acceleration：角加速度；
>   - Inertia tensor：转动惯量；
>   - Angular momentum：角动量
>   - Torque：力矩
>
> 后面会更详细进行逐一介绍。



### （1）Orientation

刚体的**朝向(orientation)**可以使用一个旋转矩阵或者四元数来表示，它表示刚体当前姿态相对于初始姿态的旋转。

![image-20240204120826541](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204120826541.png)



### （2）角速度和角加速度

- 角速度：用一个量，既表示出了旋转轴，又表示出了旋转速度。需要注意的是在描述角速度时必须要指明旋转轴。
- 角加速度：**角加速度(angular acceleration)**类似于加速度，不过它描述的是角速度的变化。这里需要说明的是角速度的变化不仅包括绕当前轴转速的变化，它还包括旋转轴发生变化的情况（当然这种很复杂，就不说了）。

<img src="Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204121202993.png" alt="image-20240204121202993" style="zoom:80%;" />



### （3）转动惯量Rotation Intertia——I

**转动惯量(rotational inertia)**类似于质量，它描述了刚体抵抗旋转的能力。转动惯量与质量的一大区别在于转动惯量不是一个常数而是一个张量(矩阵)，当刚体的朝向发生改变时需要利用旋转矩阵来计算当前姿态下的转动惯量；同时转动惯量也与刚体上的质量分布密切相关。

> 维基百科的定义：
>
> 在经典力学中，**转动惯量**又称**[惯性矩](https://zh.wikipedia.org/wiki/惯性矩)**（英语：Moment of inertia），通常以*I*[[1\]](https://zh.wikipedia.org/wiki/轉動慣量#cite_note-1)表示，[国际单位制](https://zh.wikipedia.org/wiki/國際單位制)为$kg⋅m^2$。转动惯量是一个物体对于其旋转运动的[惯性](https://zh.wikipedia.org/wiki/慣性)大小的量度。一个刚体对于某转轴的转动惯量决定对于这物体绕着这转轴进行某种角加速度运动所需要施加的力矩。
>
> 转动惯量在[转动力学](https://zh.wikipedia.org/w/index.php?title=转动力学&action=edit&redlink=1)中的角色相当于线性动力学中的[质量](https://zh.wikipedia.org/wiki/質量)，描述[角动量](https://zh.wikipedia.org/wiki/角動量)、[角速度](https://zh.wikipedia.org/wiki/角速度)、[力矩](https://zh.wikipedia.org/wiki/力矩)和[角加速度](https://zh.wikipedia.org/wiki/角加速度)等数个量之间的关系。

![image-20240204130709645](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204130709645.png)



### （4）角动量

**角动量(angular momentum)**则描述了刚体旋转的状态，它是转动惯量与角速度的乘积。

![image-20240204130752754](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204130752754.png)



### （5）Torque——力矩

当外力不通过刚体的质心时会产生**力矩(torque)**，从而导致刚体发生旋转。

![image-20240204130936239](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204130936239.png)

在质点动力学的基础上把旋转部分也考虑进来对物体的运动状态进行更新就得到了刚体动力学的仿真方法，如下图所示（下图可以很好地看到刚体动力学与之前所学的内容之间的对应关系）：

![image-20240204131018270](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240204131018270.png)

理解概念就好，实际也不会要求从头写物理引擎。



### （6）Application——Billiard Dynamics

以台球游戏模拟为例，我们假设台球自身与桌面没有摩擦，这样台球的运动可以简化为二维平面运动。在进行仿真时需要把球杆给予台球的力(冲量)移动到球心来计算台球沿球杆方向的速度；同时这种移动还会对台球施加一个力矩使台球产生旋转，因此也需要更新台球的角速度。**总之这样一个简单的场景，他的物理也是很难的。**



## 4.Collision Resolution

在进行刚体仿真时我们需要考虑不同刚体之间的相互作用，也即所谓的碰撞问题。要求解碰撞问题的第一步是对刚体碰撞进行检测，目前在物理引擎中注意是使用两阶段的检测方法。

先用简单的AABB判断是否会碰撞；如果检测会发生碰撞再做更为精细的检测，并求解出碰撞点和碰撞信息。

用下图来表示这两个过程：

![image-20240205120022952](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205120022952.png)



### （1）Broad Phase

显然场景中大部分的物体是不会同时发生接触的，因此所谓的broad phase就是只利用物体的bounding box来快速筛选出可能发生碰撞的物体。目前物理引擎中常用的碰撞检测包括**空间划分(space partitioning)**以及**sort and sweep**两类方法。

#### （a）BVH Tree

我们在介绍渲染技术时就介绍过空间划分的相关概念，它的思想是把场景中的物体使用一个树状的数据结构进行管理从而加速判断物体是否相交的过程。BVH是空间划分的经典算法，它使用一棵二叉树来管理场景中所有物体的bounding box。BVH的特点是它可以通过动态更新节点来描述场景中物体的变化，因此可以快速地检测场景中的bounding box可能存在的碰撞。

> 这里使用BVH就和渲染那里基本一致了，不过在碰撞检测中使用BVH不如使用下述的Sort  and Sweep方法快。



#### （b）Sort and Sweep

sort and sweep是使用排序来检测碰撞的算法。它的思想非常直观：对于使用AABB进行表示的bounding box，两个bounding box出现碰撞时必然会导致它们的边界产生了重叠，而判断是否出现重叠则可以通过对bounding box的边界进行排序来进行计算。

![image-20240205121049407](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205121049407.png)

注意上图这种检测是要在三个轴都要检测的，不然如果只是判断x轴向发生相交的话也可以在空间上是错位的，实际不相交。另外，Sort and Sweep方法的另一个优势在于，在更新的时候速度很快（因为已经排好序了，加入新的物体或者是更新某个物体位置的时候只是对排序数组的少量元素进行更新，速度会很快。）

更多详细内容可以参考：[Sort, sweep, and prune: Collision detection algorithms · leanrada.com](https://leanrada.com/notes/sweep-and-prune/)

或者这篇中文的比较好理解：[粗检测阶段（一）：Sweep and Prune 算法 · Issue #22 · phenomLi/Blog (github.com)](https://github.com/phenomLi/Blog/issues/22)



### （2）Narrow Phase——Objectives

筛选出可能发生碰撞的物体后就需要对它们进行实际的碰撞检测，这个阶段称为narrow phase。除了进一步判断刚体是否相交外，在narrow phase中一般还需要去计算交点、相交深度以及方向等信息。

一般有三种方法进行检测：

- Basic Shape Intersection Test
- Minkowski Difference-based Methods
- Separating Axis Theorem

以下分别进行介绍。

#### （a）Basic Shape Intersection Test

![image-20240205125636457](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205125636457.png)

#### （b）两个都是凸包怎么办？—— Minkowski Difference-based Methods

对于凸多边形的情况则可以使用**Minkowski差异(Minkowski distance)**来判断它们是否相交。在介绍Minkowski距离之前首先要引入**Minkowski和(Minkowski sum)**的概念：对于两个点集$A$和$B$，它们的Minkowski和定义为两个集合中任意一对矢量相加后得到的新的点集。

这个地方对应课程里上有动图（[10.游戏引擎中物理系统的基础理论和算法 | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV16U4y117VU/?spm_id_from=333.337.search-card.all.click&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)）1：24：00左右，这里看视频吧就不整理笔记了。

另外，还有GJK算法也可以看课程复习，也可以看这篇文章：[碰撞检测算法之GJK算法 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/511164248)，写的非常不错。

当GJK算法判断出两个凸多边形相交后还可以进一步计算交点以及深度等信息。



#### （c）分离轴定理——SAT

**分离轴定理(separating axis theorem, SAT)**同样是一种计算凸多边形相交的算法，它的思想是平面上任意两个互不相交的图形我们必然可以找到一条直线将它们分隔在两端。对于凸多边形还可以进一步证明必然存在以多边形顶点定义的直线来实现这样的分隔，因此判断凸多边形相交就等价于寻找这样的分隔直线。这个在对应课程的1：33：00左右。

在二维场景下，使用SAT判断凸多边形是否相交时需要分别对两个图形的边进行遍历，然后判断另一个图形上的每个顶点是否落在边的同一侧。只要发现存在一条边可以分隔两个图形即说明它们互不相交，否则继续遍历直到用尽所有的边，此时两个图形必然是相交的。

可参考文章：[碰撞检测算法之分离轴定理 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/508874496)



在3D的情况下，对于三维图形的情况则不仅需要考虑面和面的分隔关系，还要考虑边和边的分隔关系：

![image-20240205133142048](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205133142048.png)

注：当图形的位置发生变化时还可以从上一次检测得到的分离轴开始重新进行检测，这样可以进一步提高算法的效率。



### （3）Collision Resolution

完成碰撞检测后就需要对发生碰撞的刚体进行处理，使它们相互分开。目前刚体的碰撞主要有三种处理思路，分别是penalty force、velocity constraints以及position constraints，本节课我们主要介绍前两种处理方法。

#### （a）Apply Penalty Force

**penalty force**是最直观的碰撞处理方法，它的思想是当两个物体相交后沿反方向分别施加一个排斥力把它们推开。这种方法要求设置比较大的排斥力以及很小的积分时间间隔，否则容易出现非常不符合直觉的碰撞效果，因此现代物理引擎中几乎不会使用penalty force来处理刚体碰撞问题。



#### （b）Velocity Constraints

目前物理引擎中主流的刚体碰撞处理算法是基于Lagrangian力学的求解方法，它会把刚体之间的碰撞和接触转换为系统的约束，然后求解约束优化问题。

**这一部分不手撕物理引擎的话不太用关注，差不多知道有这么种解法就行。**

![image-20240205134818119](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205134818119.png)



## 5.Scene Query

除了上面介绍过的内容外，在游戏中我们往往还需要对场景中的物体进行一些查询，这些查询操作也需要物理引擎的支持。

### （1）Ray Cast

**raycast**是非常基本的查询操作，我们希望能够获取某条射线在场景中击中的物体。实际上在光线追踪中就大量使用了raycast的相关操作，而在物理引擎中raycast也有大量的应用，比如说子弹击中目标就是使用raycast来实现的。

这里有比较常见的三种raycast类型：

- Multiple hits：需要知道所有的交点；
- closest hit：返回最近的交点；
- any hit：返回是否有交点即可，不在乎交点在哪；
  - 成本最低，速度最快



### （2）Sweep

**sweep**与raycast类似，不过在sweep中需要使用有一定几何形态的物体取击中场景中的其它物体。

![image-20240205135954550](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205135954550.png)

sweep其实是比较常见的，比如角色在平移的过程就像是在sweep，需要计算平移的角色跟场景的求交问题。不过一般就是求解一些简单的几何体，比如Capsule。

> Unity介绍SweepTest的API为：Tests if a rigidbody would collide with anything, if it was moved through the Scene.



### （3）Overlap

另一种常用的操作是**overlap**，此时我们需要判断场景中的物体是否位于某个几何形状中。overlap与碰撞检测非常类似，不过overlap一般只会使用简单的几何体来进行检测。像游戏中爆炸效果的检测就是使用overlap来实现的（检测手雷Overlap了哪些角色）。

![image-20240205140403984](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205140403984.png)



### （4）Collision Group

在物理引擎中还需要额外注意对场景中的物体进行分组，这样可以提高各种物理仿真算法的效率。

![image-20240205140532131](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205140532131.png)



## 6.Efficiency，Accuracy and Determinism

本节课最后讨论了物理仿真中的一些其它技巧。

### （1）Simulation Optimization

我们知道物理仿真是极其消耗计算资源的，如果在所有时刻都对场景中的物体进行模拟会造成计算资源的浪费。因此一种常用的手段是把场景中的物体划分为若干个island，当island内没有外力作用时就对它们进行休眠，这样就可以节约计算资源。

![image-20240205140717028](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205140717028.png)



### （2）CCD——Continuous Collision Detection

当物体运动的速度过快时可能会出现一个物体之间穿过另一个物体的现象（相当于碰撞那一刻在两个tick之间，被引擎错过去了），此时可以使用CCD的相关方法来进行处理。

![image-20240205141903706](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205141903706.png)

上图（a）展示了两种解决这种问题的思路：

- Let it go：不解决；
- 将相关的碰撞体（比如地板）加粗，这样就不会出现由于移速过快直接穿过去的情况了。

上图（b）则是真正的CCD策略，适用于（a）的方案无法解决的情况：

- 会做一个保守的估计，计算物体到环境之间的安全距离是多少，在快要接近的时候把计算的步长step调密，做更细致的检测。其实前面的sweeping在比较简单的几何体的情况下也可以进行这种检测；



### （3）Deterministic Simulation

在进行物理仿真时还需要考虑仿真结果的确定性。尽管在编程时我们使用的都是同一套物理定律，在程序运行阶段由于帧率、计算顺序以及浮点数精度等问题容易出现同一个场景在不同终端上产生不同的模拟结果。

- 这种确定性对于联网游戏来说非常的重要；

一些有启发的解决方案：

- 我们希望在不同的终端，物理引擎计算的步长是一致的，比如规定1s计算30帧；
- 在物理计算是有很多迭代算法，我们希望这些算法的迭代步长和迭代顺序都是一致的；（比如分离轴算法，从哪条边开始要是确定性的）；
- 考虑好浮点数的精度造成的偏差



## 7.Q&A

（1）游戏中物理、动画和渲染tick的速度是一样的吗？

一般来说渲染和动画可能差不多，但物理一般不会tick的特别快（跟逻辑同步，可能是30帧/s），逻辑甚至可能帧率更低。

（2）GPU可以做物理计算么？

可以的，比如Compute Shader，或者计算流体，布料这种。



# 十三、 11 物理系统：高级应用

## 1.Character Controller

> 注：[Collide And Slide - *Actually Decent* Character Collision From Scratch (youtube.com)](https://www.youtube.com/watch?v=YR6Q7dUz2uk)这个视频或许有用，有时间可以看看。

**角色控制器(character controller)**是玩家操作角色和游戏世界进行交互的接口。和很多人直观的认识不同，角色控制器在很多情况下实际上是一个非物理的。最常见的例子是玩家控制角色停止移动时角色会立即停住，而不是严格按照刚体仿真那样通过摩擦力来逐渐停止运动。某种意义上讲，角色控制器虽然是反物理的但却更符合人对物理世界的认知。

### （1）Controller的构建

在构建Character Controller时一般会使用简化后的形状来包裹角色，这样便于处理各种场景之间的互动。

![image-20240205171955180](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205171955180.png)

注意到内层的collider外面还有一层outer edge，这个是用来防止角色离物体太近的。



### （2）Collide with Environment

在角色和场景进行互动时最常见的情况是玩家控制的角色撞到了墙壁上。如果严格按照物理引擎进行模拟，此时角色会一直停在碰撞的位置；而现代游戏中更常见的处理方式是修改角色的运动方向，使得角色此时会沿墙壁方向进行滑动。

![image-20240205172325340](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205172325340.png)



### （3）Auto Stepping and its problem

上下楼梯同样也是角色在场景中的一种常见行为。如果严格按照物理仿真进行处理，胶囊的上下楼梯会非常地困难。因此在游戏引擎中需要单独考虑这种情况，当角色上下楼梯时自动修正角色的位置。

大概思路是当每帧要移动角色的时候，尝试把Controller抬高一点点并往前走。



### （4）Slope Limits and Force Sliding Down

对于斜坡这种情况，如果按照刚体运动学进行处理会导致角色下坡时直接从斜坡上滑下来，或是在上坡时由于具有过大的速度角色直接冲上它不应该到达的位置。为了避免这些问题需要单独考虑角色停在斜坡或是限制角色的位置。

- 一般会设置一个Max climb slope的角度；
- 在非常陡峭的斜坡上时角色会往下滑；



### （5）Controller Volume Update

角色控制器还需要考虑角色体积发生变化的情况。当玩家控制角色进行下蹲等动作时需要自动更新角色控制体的体积，否则容易出现角色卡在门口无法进入的问题。

![image-20240205173931214](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205173931214.png)

这里有一个注意事项，比如玩家在管道中下蹲，此时如果玩家发出站起来的指令时不能直接更新Controller，否则可能会直接运算物理碰撞，导致角色卡死在某个地方。



### （6）Controller Push Objects

当玩家控制角色和场景中的物体互动时需要对动态对象的运动状态加以更新（比如说推箱子）。比较常见的处理方式是发生碰撞时对动态对象施加一个相应的冲量来控制它们的运动。往往这样做：

- （a）当Character Controller和Dynamic Actor发生碰撞的时候，调用Hit的回调函数；
- （b）对Dynamic Actor施加一个力的作用；



### （7）Standing on Moving Platform

除此之外，角色控制器还需要考虑动态场景的情况。当角色位于运动的平台时需要根据平台的运动来调整角色的运动状态，否则会出现平台发生运动时角色的运动没有同步或是滞后的问题。

> 举一个常见的bug，就是角色站在平台上，且平台在向上移动。此时由于物理解算往往会有一帧左右的延迟，就会出现角色与平台向上不同步的情况，此时角色就会在平台上抖动（比如《原神》的升降台之前就有这个bug）。
>
> 解决方案是可以用raycast检测是否站在了平台上，如果在平台上且玩家没有新的输入就把controller和平台绑在一起，保证一起移动。



## 2.Ragdoll

**布娃娃(ragdoll)**系统是游戏角色动画的一个重要组成部分，它最常见的例子是角色的处决动画：当玩家控制的角色处决了某个游戏对象时，根据处决场景的不同被处决对象会发生相应场景互动的动作。

### （1）Map Skeleton to Rigid Bodies

实际上ragdoll与前面介绍过的[骨骼动画](https://peng00bo00.github.io/2022/05/11/GAMES104-NOTES-08.html#skinned-animation-implementation)密切相关。在模拟ragdoll的运动时，我们同样会在角色身上设置相应的节点并把不同节点之间的骨骼按照刚体进行模拟。不过出于实时计算上的考虑，ragdoll一般只会使用非常少量的节点和骨骼来进行模拟（最多可能就十几个rigid Body吧）。

![image-20240205175911507](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205175911507.png)



### （2）Human Joint Constraints

同样地，在ragdoll中需要考虑角色身上不同节点的运动是带有一定约束的。如果忽略了人体骨骼关节的约束则会导致非常扭曲的模拟效果。一般来说ragdoll关节的约束会由TA进行设置，如果设置的不好会出现一些反直觉的动画效果。

设置好之后，一般游戏里就不会再改了。



### （3）Animating Skeleton by Ragdoll

需要注意的是尽管我们可以使用ragdoll来模拟角色的动画，在实际游戏中仍然是需要通过骨骼关节系统来驱动整个角色的运动。由于ragdoll中的骨骼关节数量一般会少于实际角色的骨骼关节，我们需要使用[动画重定向](https://peng00bo00.github.io/2022/05/17/GAMES104-NOTES-09.html#animation-retargeting)技术来将ragdoll计算出的运动映射到实际的角色骨骼上。

![image-20240205180506627](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205180506627.png)

- Active joints指的是完全和布娃娃系统重合的joints；
- Leaf joints指的是布娃娃系统控制的joints的子节点，比如说布娃娃系统绑定到了胳膊，那么手指就算是Leaf joints。Leaf joints使用原来的pose，相当于跟着父节点动；
- Intermediate joints：对应的pose是从前后布娃娃系统对应的pose插值得到的；



### （4）Blending between Animation and Ragdoll

在使用时还需要注意角色动画切换到ragdoll的过程。还是以角色处决动画为例，在一开始被处决对象是使用预先录制的角色动画，然后在某一时刻会切换成ragdoll使用物理系统来实时计算角色的行为。

更进一步，在现代3A游戏中还会将角色动画和ragdoll实时计算出的动画进行混合（Powered Ragdoll）来提升玩家的代入感和游戏体验。

![image-20240205181657840](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205181657840.png)



## 3.Cloth

布料系统是游戏物理仿真中的重要一环。早期的布料模拟是使用预先录制的动画来实现的，我们可以在角色身上设置一些额外的骨骼来控制衣物的运动，这样就可以实现角色执行不同动作时衣物随之飘动的效果。

![image-20240205182047212](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205182047212.png)

> 移动端的游戏基本还是用骨骼动画来做的，毕竟确实是跑不动。



### （1）Rigid-body Based

另一种处理衣物的方法是使用刚体运动的方法来模拟衣物和角色以及场景的互动。这样的处理方法虽然需要更多的计算资源，但可以实现相对真实衣物运动的效果。

![image-20240205182509398](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205182509398.png)

> Unity插件Magica Cloth可能就是这么做的。



### （2）Mesh-Based Cloth Simulation

而在现代游戏引擎中衣物运动更多地是使用网格来进行模拟。这里首先要说明的是布料仿真中使用的网格是不同于渲染中所使用的网格，出于计算效率上的考虑布料仿真中使用的网格要比渲染中的网格要稀疏很多（甚至可能会稀疏十倍以上）。

同时在布料仿真中往往还会为网格上的每个顶点赋予一定位移的约束，从而获得更符合人直觉的仿真结果。如下图：

![image-20240205182936426](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205182936426.png)

> 要注意衣料穿模的问题，虽然这个问题现在的物理引擎很难去解决。



#### （a）Mass-Spring System

使用网格进行布料仿真的基本处理方法是使用质点弹簧系统进行模拟。我们为网格的顶点赋予一定的质量，然后将相邻顶点使用弹簧连接起来就形成了布料仿真的物理系统。这里需要注意的是除了弹簧弹力之外一般还需要为质点施加一定的阻尼来保证质点的运动最终能够停住。

在放置弹簧时除了横竖方向外一般还需要在对角方向上也设置一些弹簧，这样可以保证布料具有抵抗对角方向的刚度。

最后把外力施加在质点弹簧系统上就可以进行布料的运动仿真了。这里需要注意的是在进行仿真时不要忘记质点除了弹簧施加的弹力和阻尼外自身还会收到重力以及空气阻力的作用。

![image-20240205190109470](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205190109470.png)

其中，上图下面那个公式是基于Verlet Intergration，这个接下来会进行介绍。现在的布料模拟有时也会利用PBD的思想去进行求解，如下图：

![image-20240205190818496](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205190818496.png)

> 这个后面有需要再来补充吧。



#### （b）Verlet Integration

对质点弹簧系统进行仿真时不可避免地会使用到一些数值积分的方法，这里我们着重介绍一下Verlet积分算法。Verlet积分本质仍然是半隐式欧拉积分，不过在实际积分时可以将速度项约掉只保留位移和加速度项就能进行计算。因此Verlet积分不需要保存每一时刻的速度，我们只需要位移和力(加速度)就可以进行计算，从而提高布料仿真的效率。

![image-20240205190321388](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205190321388.png)



### （3）Self Collision

布料仿真的一大难点在于如何处理**自相交(self collision)**问题。由于我们使用了没有体积的网格来表示布料，在进行仿真时很容易出现网格直接相互的穿插。

目前布料自相交的问题还没有一个十分完善的解决方法。在工业界会使用一些trick来缓解自相交的问题，比如说对布料进行加厚、减少仿真时的时间步长（使得解算更精细）、限制顶点的速度以及使用SDF进行控制等。

![image-20240205191318128](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240205191318128.png)



## 4.Destruction

> 补充：Unity做破坏的包介绍：[4 Unity Destruction Libraries Compared - Which is best for you? (youtube.com)](https://www.youtube.com/watch?v=Ks0tL2i_emk)

玩家对场景的破坏是通过破坏系统来进行实现。一个好的破坏系统可以极大地提升玩家的游戏体验，有些游戏甚至是以破坏系统为核心玩法进行设计的（比如彩虹六号）。

这里不整理了，看笔记（[GAMES104课程笔记11-Applications in Physics System - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/06/05/GAMES104-NOTES-11.html)）或者课程的58分钟到1小时14分钟的部分（[11.物理系统：高级应用 | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Ya411j7ds/?spm_id_from=333.788&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)）。



## 5.Vehicle

对应课程1小时14分到1小时29分的部分，也不整理了。如果后面有时间又感兴趣可以看个教程做个Demo。



## 6.Advanced：PBD/XPBD

### （1）PBD

本节课最后讨论了PBD和XPBD两种更高级的物理仿真技术。和前面介绍过的仿真技术相比，PBD和XPBD是建立在**拉格朗日力学(Lagrangian mechanics)**基础上的仿真方法。在拉格朗日力学的框架中不再考虑力等物理概念，而是把物理定律视为系统的某种约束来描述运动。



### （2）XPBD



## 7.其他

### （1）参考文档

在Games104对应章节的PPT最后有相关的参考文档，感兴趣可以看看。



# 十四、12 游戏引擎中的粒子和声效系统

## 1.粒子系统

**粒子系统(particle system)**是现代游戏中非常重要的组成部分，游戏中大量的特效都是基于粒子系统来实现的。实际上粒子系统来自于电影行业对于视觉特效的追求，它最早可以追溯到1982年的电影《星际迷航2：可汗之怒》。

所谓的粒子是指具有一些物理信息的物体，常见的物理量包括位置、速度、大小、颜色等。同时粒子还需要考虑自身的**生命周期(life cycle)**，当粒子的生命周期结束后需要被系统回收。

![image-20240208144637099](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208144637099.png)

### （1）Particle Emitter

每一种不同的粒子都是由相应的**粒子发射器(particle emitter)**生成的。每一种粒子发射器需要指定自身的生成规则同时为粒子赋予相应的仿真逻辑（比如说发射粒子的速度，时机）。

![image-20240208144937421](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208144937421.png)



### （2）Particle System

在一个粒子系统中往往会同时具有多个不同的粒子发射器进行工作，它们之间相互配合就实现了丰富的粒子效果，一起构成了Particle System。



### （3）Particle Spawn

粒子系统在生成粒子时可以根据需求使用不同的生成策略。比较简单的生成方式是从单点生成粒子，而在现代粒子生成器中则可以从某个区域甚至依据物体的网格来生成粒子。

同时粒子生成器也可以根据需求只产生一次性的粒子，或是源源不断地生成新的粒子。（其实基本内容了解Unity的粒子系统即可）



### （4）Simulate

完成粒子的生成后就可以利用质点运动学的相关方法对粒子进行仿真。

![image-20240208145641241](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208145641241.png)

由于粒子系统一般不需要严格地遵守物理规律，在实践中一般来说类似于前面的物理系统，使用显式积分的方法即可求解出每帧的状态（加速度更新速度，速度更新位置）。



### （5）Particle Type

- Billboard Particle
- Mesh Particle
- Ribbon Particle

（1）早期的粒子系统会假定粒子都位于某个平面上进行运动，这种方法称为billboard particle。当观察者的视角发生变化时，billboard会随着观察者的视角一起变化从而保证它一直位于观察者的正前方。

> 关于Billboard的一个trick：如果是一个比较大的particle的话（比如火焰、烟），一般建议用Animate Texture，也就是纹理内容随时间变化，这样玩家就会被动画吸引，而不去关注billboard的现象了。

todo：关于Billboard的原理后面有复习需要了再进行总结。



（2）Mesh Particle

随着游戏技术的进步，后来还出现了mesh particle这种带有几何信息的粒子。这种形式的粒子可以用来模拟岩石、碎屑等带有明显几何信息的颗粒。一般来说这里的Mesh要有一点随机性（比如随机的旋转和放缩）。

> 一个trick：一般来说粒子系统都要带一些随机性。这样效果更好；



（3）Ribbon Particle

在很多游戏中还使用了ribbon particle这种带状的粒子用来模拟各种拖动的效果，比如说游戏中各种武器的特效一般都是使用这种技术来制作的。在使用ribbon particle时一般还会结合Centripetal Catmull曲线来形成光滑连贯的特效。原因如下：

- Catmull算法比较简单；
- 可以保证插值得到的曲线是严格穿过所有控制点的；

![image-20240208151624095](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208151624095.png)

### （6）Particle System Rendering

#### （a）Particle Sort

粒子在进行渲染时的一大难点在于如何进行排序。按照alpha混合的理论，我们需要从最远端开始由远及近地对场景中的物体进行绘制。由于场景中往往同时存在巨量的粒子，对这些粒子进行排序往往会耗费大量的计算资源。目前对于粒子进行排序主要有两种做法：

- 其一是全局排序。即无考虑发射器的信息，单纯对所有的粒子进行排序，这种做法可以获得正确的结果但需要非常多的计算资源；
- 另一种做法是按照emitter进行排序，这种方法可以极大地减少计算资源但可能会出现错误的排序结果。

![image-20240208152324786](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208152324786.png)



#### （b）Resolution

当粒子充满场景时半透明的粒子会导致我们必须在同一像素上进行反复的绘制，这往往会导致帧率极大的下降。

因此在对粒子进行渲染时还会结合下采样的技术来减少需要进行绘制的像素数。把降采样后的图像和透明的粒子按照透明度混合后再通过上采样来恢复原始分辨率。

![image-20240208153118027](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208153118027.png)

注：在绘制粒子的时候要考虑和深度图作比较，并且alpha通道不要忘了进行混合。

> 在现在的游戏引擎中，越来越多的渲染使用这种Down Sampling去做。（比如再用DLSS把分辨率变回去）



### （7）Processing Particles on GPU

显然粒子系统这种天然并行的系统非常适合使用GPU进行计算，在现代游戏中也确实是使用GPU来实现对粒子系统的仿真。GPU渲染粒子的优势在于：

- GPU有很好地计算并行性，非常适用于模拟大量的粒子；
- 可以节省CPU的资源，去做游戏相关的逻辑；
- GPU很容易访问到depth buffer，用于做碰撞计算；（Easy to access depth buffer to do collision）

![image-20240208154050787](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208154050787.png)

稍后我们会看到使用GPU来对粒子系统进行计算不仅可以节约CPU的计算资源，更可以加速整个渲染的流程。上图中所有的红色区域现在都可以移动到GPU上面去做。



#### （a）Initial State

我们可以通过维护若干个列表来实现对粒子系统的仿真。首先我们把系统中所有可能的粒子及其携带的信息放入particle pool中，并且在deal list中初始化所有的粒子编号。

- particle pool中存放了particle的对应数据，比如位置，颜色等；

![image-20240208175822749](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208175822749.png)



#### （b）Spawn Particles

当emitter生成新的粒子时只需要将dead list中的粒子推入当前帧的alive list即可。

![image-20240208180056660](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208180056660.png)

#### （c）Simulate

对粒子进行仿真时只需要考虑alive list中的粒子。如果某个粒子的生命周期结束了，则需要把该粒子编号重新放入dead list中，然后在写入下一帧的alive list时跳过该编号。当需要切换到下一帧时只需交换两个alive list即可。

![image-20240208180350732](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208180350732.png)

在上图里，先对上一步所处在Alive List 0当中的Particle做一次Simulate，发现6死了，就把6重新放入到Dead List当中，并把没死的放入到Alive List 1（对应当前帧）里。将Alive List 0 和Alive List 1不断进行交换，就可以很好地算出当前Alive的粒子有什么了（思想应该是类似于双缓冲区）。有了Compute Shader之后，由于其提供了原子操作，因此这个操作并不难。

对于Alive List来说，还可以继续做一步Frustum Culling，得到可见的粒子。**注意Alive List after Culling是一个单独的List，并不会影响Alive List，这是因为即使不在视锥体范围内，也要考虑粒子的生命周期。**



#### （d）Sort，Render and Swap Alive Lists

![](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208181231797.png)

> 这个GPU Particle的基本管理思想是很值得学习的，也比较常见。



#### （e）Parallel Mergesort

现在的问题是，如何在GPU上进行排序？在GPU上进行排序时需要使用并行的排序算法，其中比较经典的算法是**parallel mergesort**。

![image-20240208182852795](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208182852795.png)

> 个人理解（但不一定对）：这个推荐的Method2就是Y总的那种归并排序，双指针都从头遍历，放入到目标数组。
>
> 可能有用的链接：[经典排序算法以及负载平衡下的平行归并排序Parallel Merge Sort with Load Balancing_parallelmergesort-CSDN博客](https://blog.csdn.net/xudong_98/article/details/51622219)，这里后面有需要再看吧。



#### （f）Depth Buffer Collision

除此之外还可以在GPU中进行粒子和场景的碰撞检测。出于计算效率方面的考虑，在对粒子进行碰撞检测时一般只会使用屏幕空间和深度图来简化计算。

![image-20240208183143623](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208183143623.png)

> 还是我个人的理解，不一定对：
>
> 1.将粒子的位置重投影到前一帧屏幕空间的UV坐标；
>
> 2.读取前一帧的深度图；
>
> 3.通过步骤1计算出粒子的运动轨迹，检测粒子的运动轨迹是否与深度图之间会产生碰撞，但这里要考虑一个thickness value，看上图；
>
> 4.如果检测碰撞发生，则计算表面法线方向，并弹开粒子。



### （8）Advanced Particles

实际上在现代游戏中，不止游戏的特效需要粒子系统，很多时候人群，飞鸟这种也是用粒子系统来做的。

#### （a）Crowd Simulation

现代游戏的粒子系统已经远不局限于实现不同的视觉特效，实际上我们可以基于粒子系统来实现更加丰富的功能。比如说游戏中大量NPC的运动行为就可以利用粒子系统进行实现。

- 此时每个粒子不仅仅具有常见的物理属性，还会携带顶点等几何信息。
- 基于粒子的几何信息还可以让NPC动起来，甚至可以利用状态机的理论制作简单的动画。
- 基于SDF和类似Flowmap的相关技术还可以控制群体的运动行为。

![image-20240208185925148](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240208185925148.png)

> 现代引擎里往往SDF都能实时生成了。



#### （b）其他

- 在虚幻5引擎中就实现了非常强大的粒子系统，从而方便开发者设计各种复杂的玩法和场景。（UE5 Niagara）。一些UE5的demo包括Mesh和Particle之间的自然切换（一堆粒子变成人，人变成粒子），以及人和鸟群的交互行为（《原神》的鱼群有没有可能是用粒子效果做的？）
- 现在很多粒子特效制作不再使用像Unity原本的Particle System，而是使用类似VFX Graph的蓝图形式。



## 2.Sound System

音效是影响游戏氛围和玩家体验的重要一环，很多游戏都需要使用大量的音效来调动玩家的情绪。这里声音系统暂时就不记笔记了，可以参考课程56分钟开始或者官方笔记：[GAMES104课程笔记12-Effects - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/06/15/GAMES104-NOTES-12.html)



## 3.补充:Unity的Particle System

【1】关于Texture Sheet Animation部分甚至没有找到很好的参考链接，不得不说Unity的官方文档是真的。。。。。，感觉不如虚幻。关于Particle System参考小电脑的Effect-C1-FinalShow-URP项目即可，能做到需要的时候能拿来用应该就行。



# 十五、 13 引擎工具链基础

> 没有必要在Tool chain的部分自己造轮子，用先用的架构即可。

## 1.Tool Chain

**工具链(tool chain)**是沟通游戏引擎用户以及更底层run time(渲染系统、物理引擎、网络通信等)之间的桥梁。对于商业级游戏引擎来说，工具链的工程量往往要比run time大得多。

![image-20240210111110876](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240210111110876.png)

另一方面，工具链也是连接游戏引擎以及第三方DCC工具的核心。在现代游戏工业中需要使用到大量的第三方工具如MAYA、3DS MAX等，在进行游戏开发时需要通过工具链将这些第三方DCC的资源加载到游戏引擎中。

从更高级的视角来看，工具链的本质是调和不同背景和思维方式用户的一套平台。对于开发者，工具链需要方便开发者管理游戏中大量资源和对象；对于设计师，工具链需要帮助他们快速实现不同的游戏逻辑；而对于艺术家，工具链则需要帮助他们表达不同的创意。工具链需要服务这些拥有不同知识背景的用户以便更好地完成游戏开发的过程。



## 2.Complicated Tool

### （1）GUI

GUI是工具链与用户直接进行交互的接口，在现代软件工程中GUI是人机交互的必要模块。有两种实现GUI的基本模式：

- **immediate mode**

  - 在immediate mode中用户的操作会直接调用GUI模块进行绘制，让用户立刻看到操作后的效果。这种模式的特点是它非常直观而且易于实现，但它的效率和可拓展性往往不尽如人意。
  - 比如说Unity的UGUI就是这种。

  ![image-20240210112730126](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240210112730126.png)

- **Retained Mode**：在现代游戏引擎中更常用的GUI实现方式是**retained mode**。在retained mode中用户的操作不会直接进行绘制，而是会把用户提交的指令先存储到一个buffer中，然后在引擎的绘制系统中再进行绘制。这样做的好处是可以极大地提高系统的运行效率和可拓展性，当然代价是这种方式的实现要更加复杂。
  - 优点：扩展性很强，性能也很好。（推荐）
  - ![image-20240210113110376](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240210113110376.png)



### （2）Design Pattern

在设计GUI系统时需要**设计模式(design pattern)**相关的知识，这里简要介绍一些在GUI设计中常用的设计模式。

#### （a）MVC

MVC是经典的人机交互设计模式。MVC的思想是把**用户(user)**、**视图(view)**和**模型(model)**进行分离，当用户想要修改视图时只能通过**控制器(controller)**进行操作并由控制器转发给模型，从而避免用户直接操作数据产生各种冲突。

![image-20240210113452976](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240210113452976.png)

> 看上图的箭头，View无法反过头来影响Model，Model的修改只能通过Controller来进行。这个架构现在在前端也经常会使用。



#### （b）MVP

MVP可以看做是对MVC的演变。MVP模式对视图和模型进行了更彻底的分离，视图只负责对数据进行展示而模型只负责对数据进行处理，它们之间的通信则通过**展示者(presenter)**来实现。当用户想要修改数据时，用户的请求会通过view提交给presenter，然后再由它转发给model进行处理。

![image-20240210113829588](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240210113829588.png)



这样其实方便了做单元测试。因为实际上在测试Model功能的时候，并不需要关心View写的怎么样，这样就可以对Model进行单独的修改。不过MVP模型会提高presenter的复杂度。



#### （c）MVVM（推荐）

MVVM是目前游戏引擎中大量使用的UI设计模式，在MVVM中视图和模型的中间层称为**ViewModel**。在MVVM模式中，视图只包含简单的UI状态数据，这些数据通过ViewModel解析成合适的数据结构再提交给模型进行处理。

可以参考的文档：[什么是MVVM框架？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/59467370)

![image-20240210115422981](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240210115422981.png)



## 3.Load and Save

加载和保存各种不同类型的数据是工具链的核心功能。在保存数据时需要使用**序列化(serialization)**的技术来将各种不同的数据结构或是GO转换成二进制格式，而当需要加载数据时则需要通过**反序列化(deserialization)**从二进制格式恢复原始的数据。

- 最简单的序列化方法是把数据打包成text文件。text文件虽然简单，但实际上目前很多系统仍然是使用text文件进行信息的传输。目前常用的text文件格式包括json、yaml、xml等。
  - 举例：Unity Editor算是YAML的一个子集
- text文件可以方便开发人员理解存储数据的内容，但计算机对于文本的读取和处理往往是比较低效的。当需要序列化的数据不断增长时就需要使用更加高效的存储格式，通常情况下我们会使用二进制格式来对数据进行存储。
  - 二进制方式举例：虚幻引擎的UAsset

和text文件相比，二进制文件往往只占用非常小的存储空间，而且对数据进行读取也要高效得多。因此在现代游戏引擎中一般都会使用二进制文件来进行数据的保存和加载。

这部分的图看笔记吧：[GAMES104课程笔记13-Foundation of Tool Chains - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/07/06/GAMES104-NOTES-13.html)，太多了不记了。



## 4.Asset Reference

在很多情况下游戏的资产是重复的，此时为每一个实例单独进行保存就会浪费系统的资源。因此，在现代游戏引擎中会使用**资产引用(asset reference)**的方式来管理各种重复的资产。实际上资产的引用和去重是游戏引擎工具链最重要的底层逻辑之一。

![image-20240212101450938](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212101450938.png)

在游戏开发过程中工具链往往还需要提供对GO进行修改，从而实现不同的艺术效果。

![](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212101507422.png)

在调整和修改数据时直接进行复制很可能会破坏GO之间的关联而且容易造成数据的冗余，因此在现代游戏引擎中对于数据引入了**继承(inheritance)**的概念。数据之间的继承可以很方便地派生出更多更复杂的游戏对象，从而方便设计师和艺术家实现不同的效果。

![image-20240212101653335](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212101653335.png)



## 5.How to Load Asset

引擎工具链基础篇后面的部分直接看笔记吧：[GAMES104课程笔记13-Foundation of Tool Chains - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/07/06/GAMES104-NOTES-13.html)，应该不会是面试考察的重点。

补充知识：

【1】Google protocol buffers：[Protobuf: 高效数据传输的秘密武器 - 程序猿阿朗 - 博客园 (cnblogs.com)](https://www.cnblogs.com/niumoo/p/17390027.html)

![image-20240212104011237](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212104011237.png)



# 十六、14 引擎工具链高级概念与应用

## 1.Glance of Game Production

在现代游戏的开发过程中，设计师和艺术家往往需要使用大量的第三方工具来辅助进行游戏角色和场景的建模。同时对于不同类型的游戏，游戏玩法和关卡设计也往往存在着巨大的差别。因此对于工具链来说，它需要实现和不同开发工具的通信也要考虑不同用户的使用需求。除此之外WYSIWYG（所见即所得）原则又要求开发者在引擎中的体验必须和实际游戏时完全一致的，这对工具链的设计提出了更大的挑战。



## 2.World Editor

**世界编辑器(world editor)**是整合了游戏引擎中几乎所有功能的平台。以虚幻引擎为例，虚幻中的世界编辑器界面包括各种不同的面板以服务不同的开发者：

![image-20240212130350166](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212130350166.png)

实际使用上，不同的用户还可以对面板的分布进行自行调整。



### （1）Editor Viewport

**viewport**可以说是整个编辑器最重要的窗口，它是连接开发者与所构建的游戏世界的接口。实际上在viewport中所展示的正是游戏世界在运行时的状态，从而方便开发者对游戏内容进行各种调整。

**需要注意的是，Editor-Only的代码必须在released game中被挪出去，**否则很容易成为写外挂的人的入口。

> 所以实际上Editor Viewport跑的就是一个完整的游戏，这样才能实现所见即所得。很多引擎也支持多个viewport。



### （2）Everything is an Editable Object

在编辑器中所有的对象都是**可编辑对象(editable object)**，开发者可以根据需要调整这些对象的位置、姿态、材质等属性。因此游戏中所有的元素都必须抽象为这样的可编辑对象。

在同一个游戏场景中可能有成千上万个对象，因此我们需要一些高效的管理工具。在编辑器中往往会使用树状结构或是分层的方式来管理场景中的对象（Unity的Hierachy窗口），有时还要设置Layer（比如植被Layer），有时还会根据对象自身的特点设计相应的管理工具。

当开发者选中某个对象时需要使用[schema](https://peng00bo00.github.io/2022/07/06/GAMES104-NOTES-13.html#schema)来获取该对象自身的信息（对应Unity里面的Properties）。

![image-20240212131415957](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212131415957.png)



### （3）Content Browser

在编辑器中还需要实现**content browser**用来管理开发过程中设计的各种美术、场景资产。在游戏开发过程中很多的资产是可以重复利用的，通过content browser可以方便地查看、检索以及分享现有的资产，从而提升游戏开发的效率。



### （4）Editing

因此世界编辑器的核心功能是方便开发者去编辑游戏场景中的各种对象。

（1）而在编辑器的实现中，首先也是最重要的功能是如何实现通过鼠标来选取物体。

- 最简单的实现方法是使用渲染系统中的ray casting功能，利用鼠标的位置来发射光线并通过与物体bounding box求交来来选择物体。
  - 这种实现的缺陷在于当物体比较复杂时bounding box是不能完全反应物体的几何形状的，此时使用ray casting的效率可能会比较低。
- 另一种实现方法是在渲染流程中添加一个额外的选取帧，为图像上每一个像素赋予一个物体编号，这样使用鼠标进行选取时只需根据物体编号进行查询即可。当然这种实现方式对计算机的硬件提出了更高的要求，同时需要注意在游戏发布时去掉这部分编辑环境下的代码。
  - 这里注意要对一些物体的选择做特殊判断，比如说particle system可以制作一个虚拟的节点供用户选择（Unity）。



（2）选取得到物体后一般还会对物体进行一些几何变换，包括平移、旋转和缩放等，这些操作的具体实现往往还需要根据使用者的习惯来进行设计。比如说对美术而言，他们可能已经习惯于使用Maya，Blender这样的软件，因此游戏引擎也要实现比较符合他们习惯的操作。

（3）对地形进行设计时需要结合高度场、地形纹理以及各种装饰件等。这里有很多功能需要引擎去实现：

- 对于编辑器来说地形设计最常用的工具是**高度笔刷(height brush)**，如何对设计出的高度场进行平滑需要很多相关的经验。当然很多商业级引擎中还提供了自定义的工具来帮助设计师对效果进行定制。这一部分可以看一下houdini是如何设计的（后面可以玩一下houdini的刷地形）
- Instance Brush：比如说刷植被，刷树木。同时还要提供比如刷了一片树之后要能够修改某一棵树的属性。现在很多Instance Brush的操作也会使用PCG的方法去实现了。

（4）Environment：比如对大量光源的摆放，Road和River的摆放，这里就不过多展开了。



### （5）Rule System in Environment Editing

游戏中的各种对象需要按照一定的规则来组织起来，因此**规则系统(rule system)**也是编辑器的重要组件。

- 举个例子：路上不能长草，路要符合地形的高低起伏。

早期的游戏引擎往往不包括这样的系统，为了保证游戏世界的合理性需要设计师人工调整游戏中的各种对象。而在现代游戏引擎中则需要提供自动化的规则系统，通过程序化的方式来保证游戏中的各种对象遵循相互之间的规则。

![image-20240212133946190](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212133946190.png)

> 我的理解是Rules是提前制定好的，而上图中的那些贴图是自动计算出来的，用于控制植被不会分布的非常奇怪。



## 3. Editor Plugin Architecture

显然整个世界编辑器是一个非常复杂的软件程序，我们很难直接在开发过程中实现所有需要的功能。因此在现代游戏引擎中一般会设计相应的插件系统来帮助用户根据自身的需求来丰富编辑器的功能。实际上不仅是游戏引擎，很多现代软件都使用了类似的策略来允许用户对系统进行定制（比如QT Creator和Chrome）。

而对于游戏引擎而言，插件系统需要考虑的一个问题是如何对插件种类进行划分。我们可以按照游戏对象的种类(网格、粒子、动画等)对插件进行分类，也可以根据对象的内容(NPC、建筑、人群等)进行分类。因此现代游戏引擎的编辑器往往需要支持这种矩阵式的分类方法，允许用户根据喜好来选择和定制插件。

![image-20240212134611613](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212134611613.png)

在对插件系统进行整合时还需要考虑不同插件之间的版本问题。不同的版本之间可以按照**覆盖(covered)**或是**分布式(distributed)**的方式进行协作。

- Covered：新版本的plugin会把老版本的覆盖掉。
- Distributed：大部分的其实都是这种，比如说做粒子的plugin和做地形的plugin彼此应该要兼容。

![image-20240212134944546](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212134944546.png)



除了上面提到的两种模式外，对于几何数据往往还会使用**流水线(pipeline)**的模式将几何体的操作进行分解；而对于更加复杂的对象有时还会使用**洋葱圈(onion ring)**的模式同时和其他的插件进行协作。

![image-20240212135033582](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212135033582.png)



随着编辑器以及各种插件之间版本的迭代，插件系统一般还需要考虑版本控制的问题。一般有两种方案：

- 插件与 host application使用相同的版本号。
- 插件使用插件接口的版本号
  - 这种更为推荐，因为软件可能一直在升级但是插件接口的版本可能并不升级，所以根据接口进行版本控制更合适。



## 4.Design Narrative Tools

> 这里感觉可以看一下Unity的Timeline系统了，应该就是做这个的。

除了游戏资产的设计外，**叙事(story telling)**在整个游戏开发流程中同样是非常重要的一环。叙事可以看做一个线性的过程，相关的游戏资产需要在一个时间轴上按照顺序进行调度。

在虚幻引擎中使用了sequencer来跟踪游戏对象及其属性在时间轴上的变化。当我们把不同的对象利用sequencer在时间轴上组织起来就实现了简单的叙事。

![image-20240212140017597](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212140017597.png)

要使用sequencer首先需要选中对象然后把sequencer绑定到对象上，然后选择相关的属性并利用关键帧设置这些属性的变化，最后利用插值就完成了叙事。具体可以学习Unity的Timeline系统应该就懂了。

> 注：很多时候这种UI还可以基于timeline来做，比如说星穹铁道里面打到敌人之后，敌人脑袋上会冒出一大堆debuff，这种按顺序冒出的可能就是timeline做的。很多过场动画甚至会偷偷换掉场景。



## 5.Reflection and Gameplay

**反射(reflection)**是sequencer乃至整个游戏引擎编程中都非常重要的技术，通过反射我们可以让游戏引擎在运行阶段获取操作对象具有的各种属性。实际上对于游戏开发流程而言，游戏引擎的开发者很难实现预判用户的需求。因此反射对于现代游戏引擎而言几乎是一个必备的工具。

![image-20240212143056814](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240212143056814.png)



早期的游戏引擎是不基于反射技术来实现的，这导致开发者在进行编程时必须手动为游戏对象添加所有需要的属性和数据，使得工具链的开发很难与游戏开发进行匹配。

todo：反射部分还没有整理完，后面再继续进行整理。



# 十七、15 游戏引擎的GamePlay玩法基础

玩法系统是游戏引擎最重要的部分，它是区分游戏引擎和渲染器以及物理引擎的核心。实际上玩法系统往往会贯穿整个游戏引擎，与引擎的其它系统进行交互，这样才能满足游戏设计师的需求。

另一方面现代游戏的玩法是极其丰富的，即使是同一类型的游戏也具有多种多样的表现形式。这些丰富的游戏内容都需要通过玩法系统来进行实现。

而在游戏行业中玩法系统还面临着快速迭代的问题，同一个游戏的核心玩法在开发运营初期和后期可能会有着巨大的差别。因此玩法系统在设计时也需要考虑需求变更和快速迭代。



## 1.事件机制

玩法系统的核心是**事件机制(event mechanism)**，在游戏世界中不同类型的GO会通过事件/消息的方式进行通信从而驱动游戏世界的运行。

### （1）Publish-Subscribe Pattern

在游戏引擎中一般会使用**publish-subscribe**这样的模式来实现具体的通信过程。在publish-subscribe模式中每个GO有着自己的publish功能来向其它GO发送事件，同时自身的subscribe功能来实现接收事件以及相应的反馈。当然在publish-subscribe模式中还需要一个**event dispatcher**来执行高效的事件派送。

因此在publish-subscribe模式中的三要素为**事件定义(event definition)**、**注册回调(callback registration)**以及**事件派送(event dispatching)**。

#### （a）Event Definition

事件定义是实现事件机制的第一步，最简单的定义方式是为事件定义一个枚举类型以及相应的参数。此时我们可以使用继承的方式来实现不同类型事件的定义。但这种方式的缺陷在于：因为玩法系统往往是由设计师来实现的，因此很难提前知道有多少种类型的Event。

![image-20240220102704018](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220102704018.png)

在现代游戏引擎中会使用反射和代码渲染的方式来允许设计师自定义事件类型和相关的数据：

![image-20240220102748904](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220102748904.png)

> 实际上的事件定义系统要更加复杂。可以想到对于上面这种代码渲染的方式，理论上每新定义一个事件都要重新进行一次代码的渲染，而这会占用很多的时间。所以像Unreal采用的做法可能是将声明的事件所编译成的新代码作为dll注入引擎的Runtime，或者有的引擎会额外封装一层如C#的接口，这样会更容易挂接和扩展，还有的会用脚本语言供事件的注册（Unity？）。



#### （b）Callback Registration

当GO接收到事件后就会激活调用相应的回调函数来改变自身的状态，而为了正确地使用回调函数则首先需要对不同的回调函数进行注册。回调函数的一大特点在于它的注册和执行往往是分开的。这一特点可能会导致回调函数调用时相关的一些GO可能已经结束了生命周期，因此回调函数的安全性是整个事件系统的一大难题。比如下面这个场景：
![image-20240220104108971](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220104108971.png)



- 为了处理这样的问题我们可以使用**强引用(strong reference)**这样的机制来锁定相关GO的生命周期。强引用会保证所有和回调函数相关的资源在回调函数调用前不会被回收，从而确保系统的安全。
- 当然强引用的方式在一些场景下可能是不合适的，很多时候我们希望某些资源可以正确的卸载掉。因此我们还可以使用**弱引用(weak reference)**的机制在调用回调函数时判断资源是否已经被卸载掉（类似C++ 11的智能指针）。当然弱引用机制的滥用可能会影响整个系统的性能。

真正在做游戏引擎的时候，强引用和弱引用都是需要的。

- 情景1：很多GO具有嵌套关系，如果父物体没有被销毁的话子物体就不能被销毁，这就是一种强引用；
- 情景2：假设我们想要找到场景中此时能看到的所有人，并实施攻击，那么这个时候可以使用弱引用，这样可以判断当前对象是否已经不存在了。

> 针对Callback function，使用弱引用会更多一些。



#### （c）Event Dispatch

事件会通过分发系统来实现消息的传递。由于游戏中每一时刻往往存在着成千上万个GO和相应的回调函数，我们需要一个非常高效的分发系统才能保证游戏的实时性。

- 最简单的分发机制是把消息瞬时发出去。这种方式的缺陷在于它会阻塞前一个函数的执行，从而形成一个巨大的调用栈使得系统难以调试；此外很多回调函数在执行时会申请一些额外的资源，这就容易导致游戏的帧率很难稳定。另外还有一点就是这种一环套一环的调用很难并行化计算。

![image-20240220105658864](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220105658864.png)

- 现代游戏引擎中更常用的分发方式是使用**事件队列(event queue)**来收集当前帧上所有的事件，然后在下一帧再进行分发和处理。

![image-20240220105947858](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220105947858.png)

由于event queue中有不同类型的事件，因此我们还需要结合序列化和反序列化的操作来进行存储（这里要用到很多反射的知识，比如反射可以知道每个数据结构占用的内存是多少，这样的话给定一段内存空间，也可以反向填回去C++的数据结构）。event queue一般会使用ring buffer这样的数据结构来实现，这样可以重用一块统一的内存空间来提升效率。

> Ring buffer数据结构的基础知识，可以参考这篇文章：[ring buffer，一篇文章讲透它？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/534098236)



现代游戏引擎中往往会同时有多个不同的event queue来处理不同类型的事件，每个queue用来保存一些相对独立的事件。这种方式可以便于我们进行调试，也可以提升系统的性能。

当然event queue也有一些自身的问题：

- 首先，event queue无法保证event执行的顺序。因为事件是统一到下一帧再分发处理的，因此例如物理、动画系统的执行顺序很多时候不太可控，这就需要逻辑足够有鲁棒性，否则容易产生游戏bug。
  - 在引擎中为了解决这种问题甚至有时要hard code；
  - 或者是有的Event在postTick中处理，有的Event在preTick中处理，有的立刻处理
- 同时，对于一些实时性的事件event queue可能会导致执行的延误（因为往往会延迟一帧再处理）。这样可能动作的打击感会受到影响。



## 2. Game Logic

在事件机制的基础上就可以开始设计游戏的逻辑了。在早期的游戏开发中会直接使用C++来编写游戏的逻辑来获得更高的运行效率，而随着游戏系统变得越来越复杂这种直接基于高级语言的开发方式就不能满足开发者的需求了。

- C++很难做到热更新；
- C++开发的游戏，每次改动都要重新编译一遍，非常麻烦。

除此之外游戏引擎面对的用户往往是设计师而不是程序员，对于设计师来说直接使用编程语言来设计游戏可能是过于复杂的。因此在现代游戏引擎中**往往会使用脚本语言来实现游戏的开发工作，它的优势在于可以直接在虚拟机上运行。（比如Lua）**。这样做的一个好处是在脚本逻辑出问题时不会导致游戏本体崩掉。

### （1）**脚本语言是如何工作的？**

![image-20240220124349778](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220124349778.png)



### （2）对象的管理

在脚本语言和引擎这两部分中，最难的其实是对象的管理。比如说对于一个GO来说，在脚本中可以管控其生命周期，而在引擎中也可以管理其生命周期，那么由谁来管就成为了一个问题。

- 这里举个例子，进入到一个城市之后，会出现很多NPC，在离开城市之后NPC又会消失掉，这个逻辑是写在脚本里还是写在引擎里？

有两种流派：

- （1）把所有的GO放在引擎的内核去进行处理。这样做理论上没什么问题，但很多时候我们希望GO的创建和消亡能够和游戏逻辑绑定。其实很多欧美的单机游戏是使用引擎内核去处理的。
- （2）将GO的创建和销毁由脚本进行控制。通过脚本的GC进行控制。针对游戏玩法非常复杂的游戏（如MMO），这种方法可能更好。

两者的对比如下图所示：

![image-20240220125304157](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220125304157.png)



### （3）脚本系统的架构

- 引擎调用脚本中的代码。这种架构很常见，如Unity就是这样的架构。
- 用脚本去调用引擎。具体来说把引擎的功能封装成SDK库，用脚本去调用引擎暴露的接口。这种方法虽然现在用的不多，但思想可以学习。



### （4）热更新

脚本语言的另一大特点是可以进行热更新。一种简单的思路是修改掉函数指针：

![image-20240220130436192](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220130436192.png)



### （5）脚本语言的问题

- （1）执行效率一般会比较低：
  - 弱类型语言往往在编译的时候不容易优化；
  - 需要一个虚拟机来运行bytecode；
  - 解决方案：JIT（Just in time）。其中Lua的JIT比较出名。JIT的大概原理是虽然是解释性语言，但可以边解释边进行编译，这样在下次执行的时候就会直接跑机器码。JIT可以知道代码执行的路径（比如哪些if-else不会跑到，就会进行优化），因此处理得好的时候JIT也是很快的。比如说Lua JIT可能要比原生态的Lua快一个数量级。
- （2）比如Lua这种脚本语言是弱类型的，所以反射会很麻烦。

举几个脚本语言的例子：

- 魔兽世界使用Lua作为脚本语言，好处是轻量，效率也比较高。但问题是类库比较少，很多都要自己写；
- Python：扩展库很多，但是占用内存也很多；
- C#：随着Mono的产生，现在很多游戏也使用C#作为脚本语言。

> todo：有时间可以看一下HybridCLR，据说内存占用比较低，性能也很好。



## 3.可视化脚本

**可视化脚本(visual scripting)**是现代游戏引擎几乎必备的功能。和传统的脚本语言相比可视化脚本无需开发者直接进行编程，因此它对于设计师和艺术家而言更容易进行掌握。像虚幻和unity这样的商业级游戏引擎都实现了自身的可视化脚本功能。

当然可视化脚本本身也是一种编程语言，它需要实现相应的变量、语句、表达式、控制流程、函数甚至面向对象编程等功能。

这一部分直接看笔记吧：[GAMES104课程笔记15-Gameplay Complexity and Building Blocks - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/07/24/GAMES104-NOTES-15.html)，应该没有太多的考察点。



## 4.3C系统

这部分也是直接看笔记就行。Unity的Cinemachine应该是一个很值得学习的参考资料。



# 十八、16 Gameplay 基础AI

## 1.Navigation

游戏AI是玩法系统重要的组成部分，其中最基本的功能是允许玩家选择目的地进行**导航(navigation)**。

导航算法需要考虑游戏地图的不同表达形式，然后寻找到从起点到目的地的最短路径，有时还需要结合一些其它算法来获得更加光滑的路线。

![image-20240220142400171](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220142400171.png)

以下分别进行介绍。



### （1）Map Representation

因此我们首先需要考虑游戏中如何来表达地图，我们可以认为地图是玩家和NPC可以行动的区域。游戏中常见的地图形式包括路点**网络图(waypoint network)**、**网格(grid)**、**寻路网格(navigation mesh)**以及**八叉树(sparse voxel octree)**等。

Walkable area of players is determined by character motion capabilities

- Physical Collision
- Climbing slope/height
- Jumping distance
- …

有的时候Walkable Area针对不同属性的NPC也是不同的，比如有的区域步行的NPC无法越过，但是骑马的NPC就可以越过去。接下来会介绍不同的地图表现形式。

#### （a）Waypoint Network

waypoint network是早期游戏中最常用的地图表示方式。我们可以把地图上的路标使用节点来表示，然后可通行的节点使用边来连接起来就形成了一个网络结构。当玩家需要进行导航时只需要选择距离起点和目的地最近的两个路标，然后在网络图上进行导航即可。

![image-20240220155418483](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220155418483.png)

waypoint network的优势在于它非常易于实现，而且我们有成熟的路径搜索算法可以直接应用在网络图上；但它的缺陷在于路网图需要不断的依据开发中的地图进行更新，而且使用路网进行导航时角色会倾向于沿路径中心前进而无法利用两边的通道。因此在现代游戏中路网的应用并不是很多。



#### （b）Grid

网格同样是表达游戏地图的经典方法，常用的网格地图包括方格地图、三角形地图（不太常见）或是六边形地图（比如《文明》）等。使用网格来表示地图时只需要把不可通行的区域遮挡住就可以了，因此网格可以动态地反映地图环境的变化。

显然网格地图同样非常容易实现，而且支持动态更新，也便于调试；而它的缺陷在于网格地图的精度受制于地图分辨率，而且比较占用存储空间，而且使用网格很难表示3D的空间关系（比如从A到B，既可以走地面，又可以走上面的桥，这种情况用Grid就不好处理）。

Grid方法还会带来一个问题，比如10000×10000的Grid，每往下走一格实际上在内存上的寻址要移动10000个单位（因为二维数组的存储方式），这样容易带来Cache Miss。

![image-20240220155741677](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220155741677.png)



#### （c）NavMesh

为了克服Grid地图的这些问题，人们开发出了寻路网格这样的地图表达形式。在寻路网格中可通行的区域会使用多边形来进行覆盖，这样可以方便地表达不同区域直接相互连接的拓扑关系。这种NevMesh的寻路方法也是现代游戏的基本标配了。NevMesh是非流形的网格（关于流形，可以参考[几何学中最伟大的发明之一——流形，其背后的几何直觉与数学方法 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/622263134)）

![image-20240220160306414](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220160306414.png)

注：后面的笔记中会介绍NevMesh的生成方法。虽然现在有的SDK库已经可以帮忙生成NevMesh，但很多时候我们还要对生成的结果进行控制，此时了解该算法也是很有意义的。

注意：在寻路网格中我们还会要求每个多边形都必须是凸多边形，这样才能保证角色在行进中不会穿到可通行区域之外，并且MevMesh中每两个凸多边形有且只有一条共享边（Portal）。

![image-20240220171916748](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220171916748.png)

寻路网格是现代游戏中广泛应用的地图表达形式，而它的缺陷主要在于生成寻路网格的算法相对比较复杂，而且它无法表达三维空间的拓扑连接关系（比如一只鸟在天上飞的时候的寻路网格）。



#### （d）Sparse Voxel Octree

如果要制作三维空间中的地图则可以考虑八叉树这样的数据结构。

![image-20240220173041977](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220173041977.png)

这种方法需要不小的存储空间，而且寻路也比较麻烦，在这里就不展开了。



### （2）Path Finding

得到游戏地图后就可以使用寻路算法来计算路径了，当然无论我们使用什么样的地图表达方式我们首先都需要把游戏地图转换为拓扑地图，然后再使用相应的算法进行寻路。

![image-20240220173330716](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240220173330716.png)

可以看到，无论是Waypoint Network，Grid还是Navmesh，都可以抽象为一个图的结构，于是寻路就变成在图上寻找最短路径。

#### （a）DFS和BFS

寻路算法的本质是在图上进行搜索，因此我们可以使用**深度优先搜索(depth-first search, DFS)**来进行求解。另一种常用的图搜索算法是**广度优先搜索(width-first search, BFS)**。不过在实际上BFS和DFS比较费，而且不太容易计算加权的最短路径。



#### （b）Dijkstra算法

直接使用DFS或是BFS往往是过于低效的，实践中更常用的寻路算法是**Dijkstra算法(Dijkstra algorithm)**。这个算法的介绍可以看这篇：https://www.redblobgames.com/pathfinding/a-star/introduction.html。

这里给出Dijkstra算法的伪代码：
```c++
for each vertex v:
	dist[v] = infinity;
	prev[v] = none;
dist[source] = 0;
set all vertices to unexplored;
while destination not explored:
	v = least-valued unexplored vertex;
	set v to explored;
	for each edge(v, w):
		if dist[v] + len(v, w) < dist[w]:
			dist[w] = dist[v] + len(v, w);
			prev[w] = v; //prev用来记录路径
```



#### （c）A*寻路算法

一篇非常好的博客，介绍`A*`寻路算法：[Introduction to the A* Algorithm (redblobgames.com)](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

有时间也可以看看`A*`寻路算法和Dijkstra的实现，参考这篇就行：[Implementation of A* (redblobgames.com)](https://www.redblobgames.com/pathfinding/a-star/implementation.html#algorithm)。在[A-Star（A*）寻路算法原理与实现 - 知乎](https://zhuanlan.zhihu.com/p/385733813)学习这篇的时候已经学习完对应的代码了，可以复习这篇知乎文章即可。

其实`A*`寻路可以简单理解为在Dijkstra算法的基础上引入一项H项（启发项距离）。对于Grid的表示来说, h(n)可以是距离终点的曼哈顿距离：

![image-20240221111443602](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221111443602.png)



对于NevMesh则会复杂一点。一般工业界选择构成Graph的点是每两个Nevmesh中间的Portal的中点，这样得到的结果会更准确。

![image-20240221111711348](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221111711348.png)

由于在算距离终点的启发式距离的时候，我们并不知道会有哪些障碍物，所以直接计算到终点的欧拉距离即可（其实在很多游戏中，NPC从A点到B点也没什么障碍物，此时A*寻路算法的速度是很快的）。![image-20240221112021477](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221112021477.png)

> 显然启发式算法的设计对于最终计算得到的路径会产生显著的影响。当启发函数的值过低时可能会需要更多次循环才能寻找到路径（无启发项则会退化为Dijsktra算法），而当启发函数值过高时则可能无法找到最短路径。因此在实际应用中需要进行一定的权衡。



### （3）Path Smoothing

直接使用寻路算法得到的路径往往包含各种各样的折线不够光滑，因此我们还需要使用一些路径平滑的算法来获得更加光滑的路径。游戏导航中比较常用**funnel算法**来对折线路径进行平滑，它不仅可以应用在二维平面上也可以应用在寻路网格上。

一篇很好地讲Funnel 算法的博客：[几何寻路：漏斗算法（Funnel Algorithm）-CSDN博客](https://blog.csdn.net/fengkeyleaf/article/details/118832924)

暂时大概理解思路应该就行，具体的算法细节等需要的时候再看吧（其实细节还是挺多的，挺难的）。



### （4）Navmesh 生成

> [16.游戏引擎Gameplay玩法系统：基础AI (Part 1) | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV19N4y1T7eU?spm_id_from=333.788.videopod.sections&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)这里的50min左右开始。

如何从游戏地图上生成寻路网格是一个相对困难的问题。一般来说想要生成寻路网格首先需要将地图转换为体素，然后在体素地图上计算距离场得到区域的划分，最后就可以在划分好的区域中生成一个凸多边形网格作为寻路网格。

关于NavMesh的其他知识可以参考：[关于NavMesh，我所知道的 (wo1fsea.github.io)](https://wo1fsea.github.io/2016/08/20/About_NavMesh/)，以及这篇：[GAMES104课程笔记16-Basic Artificial Intelligence | Bo Peng](https://peng00bo00.github.io/blog/2022/GAMES104-NOTES-16/)，其中关于Region Segemention步骤中的Watershed algorithm，可以看这里：[图像分割的经典算法：分水岭算法 - 知乎](https://zhuanlan.zhihu.com/p/67741538)

- 除此之外我们还可以在多边形上设置不同的flag来触发不同的动画、声效以及粒子效果。
- 对于动态的环境（比如玩家可以制造障碍物）我们可以把巨大的场景地图划分为若干个tile。当某个tile中的环境发生改变时只需要重新计算该处的路径就可以得到新的路径。
- 还需要注意的是使用自动化算法生成的寻路网格是不包括传送点或者走捷径（比如从A点玩家可以放一个梯子直接爬下来）这样的信息的，有时为了提升玩家和场景的互动我们还需要手动设置这些传送点。当然这会导致寻路算法更加复杂。



## 2.Steering

这部分直接参考笔记吧，就不整理了：[GAMES104课程笔记16-Basic Artificial Intelligence | Bo Peng](https://peng00bo00.github.io/blog/2022/GAMES104-NOTES-16/)。对应的Games104的视频部分：[16.游戏引擎Gameplay玩法系统：基础AI (Part 2) | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1r34y1J7Sg?spm_id_from=333.788.player.switch&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)

这部分看完之后，强烈推荐补一下Unity的Nevmesh系统（【2】和【3】还没看）：

> 【1】[Unity NavMesh Tutorial - Basics (youtube.com)](https://www.youtube.com/watch?v=CHV1ymlw-P8)
>
> 【2】[Unity NavMesh Tutorial - Making it Dynamic (youtube.com)](https://www.youtube.com/watch?v=FkLJ45Pt-mY)
>
> 【3】[Unity NavMesh Tutorial - Animated Character (youtube.com)](https://www.youtube.com/watch?v=blPglabGueM&t=761s)



## 3.Crowd Simulation

**群体模拟(crowd simulation)**是游戏AI必须要处理的问题。在游戏场景中往往会具有大量的NPC，如何控制和模拟群体性的行为是现代游戏的一大挑战。一些常见的群体模拟的例子比如NPC的走动，鱼群，鸟群模拟等。

游戏场景中群体模拟的先驱是Reynolds，他同时也是steering系统的提出者。目前游戏中群体行为模拟的方法主要可以分为三种：

- **微观模型(microscopic models)**：自底向上，聚焦于个体行为，具体可以参考一下这个[Coding Adventure: Boids (youtube.com)](https://www.youtube.com/watch?v=bqtqltqcQhw&list=RDCMUCmtyQOKKmrMVaKuRXz02jbQ&index=19)（还没看）
- **宏观模型(macroscopic models)**：Crowd as a unified and continuous entity
- **混合模型(mesoscopic models)**：将Crowd进行分组。

### （1）微观模型

微观模型的思想是对群体中每一个个体进行控制从而模拟群体的行为，通常情况下我们可以设计一些规则来控制个体的行为。比如说：

- Seperation：当距离其他个体过近的时候，要steer away；
- Cohesion：to steer towards the "center of mass";
- Alignment: to line up with agents close by



### （2）宏观模型

宏观模型的思想则是在场景中设计一个势场或流场来控制群体中每个个体的行为。

![image-20240221151558761](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221151558761.png)

一个常见的例子是人群沿着人行道走。



### （3）混合模型

混合模型则综合了微观和宏观两种模型的思路，它首先把整个群体划分为若干个小组，然后在每个小组中对每个个体使用微观模型的规则来进行控制。这样的方法在各种RTS游戏中有着广泛的应用。

![image-20240221151913650](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221151913650.png)

> 一个可能的例子是比如玩家召唤出了一群小兵，并指示一个目的地，那么这群小兵就会以那个目的地作为行动的终点，但是在这个过程中每个个体又有自己的行为。总体来说是一个结合宏观群体和微观群体的方法。



### （4）Collision Avoidance

群体模拟中的一大难点在于如何保证个体之间不会出现碰撞的问题。比较常用的方法是对每个个体施加一定的力来控制它的运动，这样就可以操纵群体的运动行为。

> 显然不能对每个个体做寻路算法，因为这种开销是不能接受的。一种方法是在障碍物的周围放置距离场，根据NPC距障碍物的距离对其施加力。这种Force-based models可以用于火灾模拟人群逃生的行为。

另一种处理的方法是基于**速度障碍(velocity obstacle, VO)**来进行控制。

- VO的思想是当两个物体将要发生碰撞时相当于在速度域上形成了一定的障碍，因此需要调整自身的速度来避免相撞。
- 当参与避让的个体数比较多时还需要进行一些整体的优化，此时可以使用ORCA等算法进行处理。

![image-20240221192043394](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221192043394.png)

这两种方法非常的硬核，有需求再学吧，暂时不补充了。在真正实践的时候往往使用Forced-based model就足够解决问题了。



## 4.Sensing

**感知(sensing)**是游戏AI的基础，根据获得信息的不同我们可以把感知的内容分为**内部信息(internal information)**和**外部信息(external information)**。

- 内部信息包括AI自身的位置、HP以及各种状态。这些信息一般可以被AI直接访问到，而且它们是AI进行决策的基础。
- 而外部信息则主要包括AI所处的场景中的信息（Static&Dynamic Spatial Information），以及一些Character的信息。它会随着游戏进程和场景变化而发生改变。一些典型的如下：
  - Static Spatial Information：包括Navigation Data，又或者Tactical Map（战术地图），Smart Object，Cover Point等
  - Dynamic Spatial Information：一种常用表达方式是**influence map**，场景的变化会直接反映在influence map上。当AI需要进行决策时会同时考虑自身的状态并且查询当前的influence map来选择自身的行为（比如说有一伙敌人突然出现，influence map上可能就会出现一片高危险区，于是AI就会绕过这片区域）。

游戏AI进行感知时还需要注意我们不能假设AI可以直接获得所有游戏的信息，而是希望AI能够像玩家一样只利用局部感知的信息来进行决策。

更多内容看笔记吧，有额外需要再做补充。



## 5.Classic Decision Making Algorithms

在上面这些知识的基础上就可以开始构建游戏AI系统了。游戏AI算法的核心是**决策(decision making)**系统，经典的决策系统包括**有限状态机(finite state machine, FSM)**和**行为树(behavior tree, BT)**两种。这两种方法更像是走一步看一步的进行决策。

其实还有一些其他的算法，他们则是以目标为导向进行决策，将在后面进行总结：

- Hierachical Tasks Network
- Goal Oriented Action Planning
- Monto Carlo Tree Search
- Deep Learning



### （1）有限状态机

在有限状态机模型中我们认为AI的行为可以建模为在不同状态之间的游走，不同状态之间的切换称为**转移(transition)**。以吃豆人游戏为例，游戏AI可以使用一个包含3个状态的状态机来表示。

![image-20240221200415928](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221200415928.png)

有限状态机的缺陷在于现代游戏中AI的状态空间可能是非常巨大的，因此状态之间的转移会无比复杂。并且可移植性和可拓展性都比较差。



### （2）HFSM

为了克服有限状态机过于复杂的问题，人们还提出了**hierarchical finite state machine(HFSM)**这样的模型。在HFSM中我们把整个复杂的状态机分为若干层，不同层之间通过有向的接口进行连接，这样可以增加模型的可读性。但这样的缺点是不同层之间的跳转要走接口，响应速度会相对较慢。

![image-20240221200559260](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240221200559260.png)



### （3）行为树

这部分的概念照着PPT和官方笔记很容易看懂：[GAMES104课程笔记16-Basic Artificial Intelligence - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/07/26/GAMES104-NOTES-16.html#behavior-tree)，就不单独整理了。

一张图进行总结：

![image-20240222085210116](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222085210116.png)

> todo：后面看一下Unity的行为树怎么用。



# 十九、 17 Gameplay 高级AI

## 1.Hierarchical Tasks Network

**层次任务网络(hierarchical tasks network, HTN)**是经典的游戏AI技术，和上一节介绍过的行为树相比HTN可以更好地表达AI自身的意志和驱动力。

HTN的思想是把总体目标分解成若干个步骤，其中每个步骤可以包含不同的选项。AI在执行时需要按照顺序完成每个步骤，并且根据自身的状态选择合适的行为。举例下面这幅图：

![image-20240222105311056](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222105311056.png)



### （1）HTN Framework

HTN框架中包含两部分，**world state**和**sensor**两部分。其中world state是**AI对于游戏世界的认知**，而sensor则更像是Perception，是AI从游戏世界获取信息的渠道。

> 这里world state的概念很容易弄混，是AI对于游戏世界的认知。

![image-20240222110013607](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222110013607.png)

除此之外HTN还包括**domain**，**planner**以及**plan runner**来表示AI的规划以及执行规划的过程（见上图）。

- HTN domain：从Asset中直接加载的一种资产，能够描述Hierachical tasks之间的关系；
- Planner：根据HTN Domain和World State，制定plan；
- Plan Runner：执行plan，并且在task之后会更新world state。**值得注意的是**plan runner会监控所有正在执行中的task的状态，如果发现task无法继续执行了就会启动Replay的机制（后文会讲）。



### （2）HTN Task Types

在HTN中我们将任务分为两类，**primitive task**和**compound task**。前者比较简单，基本就是单一的动作，而后者则是HTN系统的核心和精髓。

#### （a）Primitive Task

primitive task一般表示一个具体的动作或行为。在HTN中每个primitive task需要包含precondition、action以及effects三个要素。

![image-20240222111910331](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222111910331.png)

简单理解，precondition是从游戏世界中读取是否满足前置条件，而Effects则会对游戏世界产生影响。注意即使Preconditions全部满足，一个Task也是有可能失败的（比如执行过程中失败）。



#### （b）Compound Task

而compound task则包含不同的方法，我们把这些方法按照一定的优先级组织起来并且在执行时按照优先级高到低的顺序进行选择。每个方法还可以包含其它的primitive task或者compound task，当方法内所有的task都执行完毕则表示任务完成。

![image-20240222112856576](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222112856576.png)

> 每个method可以认为是完成task的一种方案。比如说上图，会优先使用Method1，如果Method1的Precondition不满足的话则会考虑Method2，如果Method2的Precondition不满足的话会继续考虑Method3，依次类推。**这种方法的选择类似于行为树里的Selector**，而每个Method里又可以包含一系列的Task，**这一点又类似于行为树里的Sequence**。
>
> 这里有一些额外的细节，但总体来说按上面的理解就行。举个例子：
> ![image-20240222114533574](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222114533574.png)



### （3）HTN Domain

在此基础上就可以构造出整个HTN的domain，从而实现AI的行为逻辑。这里需要把一个Task定义为Root Task，然后再依次展开，形成一个类似树状的结构，如下图：
![image-20240222120818794](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222120818794.png)

举个例子如下：

![image-20240222120931668](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222120931668.png)

### （4）Planning

接下来就可以进行规划了，我们从root task出发不断进行展开逐步完成每个任务。主要看笔记[GAMES104课程笔记17-Advanced Artificial Intelligence - Bo's Blog (peng00bo00.github.io)](https://peng00bo00.github.io/2022/07/28/GAMES104-NOTES-17.html#planning)即可，不过这里有补充说明：

![image-20240222123551644](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222123551644.png)

> 针对这一步，我们假设当Precondition满足的时候，在执行Action的过程中不会失败，也就是Action一定能完成。并且完成的Action会产生一个对World State的Effect，这里我们会把world State拷贝一份出来，存入temporary memory，让Effect对temporary memory进行修改。**这里可能造成的潜在问题会在Replanning部分得到解决。**

最后Planning输出的是一系列的Primitive Task，供给后面的Plan Runner进行决策。



### （5）Run Plan

![image-20240222124911824](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222124911824.png)

在真正执行计划的时候很可能会出现失败的情况，此时就要启用Replanning的策略。



### （6）Replan

执行plan时需要注意有时任务会失败，这就需要我们重新进行规划，这一过程称为**replan**。当plan执行完毕或是发生失败，亦或是world state发生改变后就需要进行replan。

![image-20240222125339537](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222125339537.png)

总结来看：

- HTN和BT非常相似，但它更加符合人的直觉也更易于设计师进行掌握。同时其执行效率也比行为树更高。相对于BT的每次从根节点进行遍历，HTN在world state不发生改变或者是当前task并没有完成或失败的时候不需要重新开始决策。
- HTN的缺点在于，对设计师的要求比较高，容易设计出不合理的Task。并且由于玩家的行为是不可预测的，所以Task可能会频繁失败。还有一点就是如果环境变化比较剧烈，而HTN制定的计划又过于长或者缜密，反而可能会导致AI的不稳定和震荡。



## 2.Goal-Oriented Action Planning

**goal-oriented action planning(GOAP)**是一种基于规划的AI技术，和前面介绍过的方法相比GOAP一般会更适合动态的环境。在《古墓丽影》和《刺客信条：奥德赛》中都有用到GOAP的相关技术。

### （1）结构

![image-20240222170358138](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222170358138.png)

GOAP的整体结构与HTN非常相似，不过在GOAP中domain被替换为**goal set**和**action set**。

- （1）与HTN相比，GOAP当中的Goal Set是可以严格用数学定义的目标，而HTN中其实并没有显式地说明目标是什么，而是用Task去隐式表达出目标。
- （2）Action Set：与HTN有所区别，后面会说。
- （3）这里的Planning是一种规划问题，后面会提到GOAP采用构建图并求解最短路径的方法来进行规划。



#### （a）Goal Set

goal set表示AI所有可以达成的目标。在GOAP中需要显式地定义可以实现的目标，这要求我们把目标使用相应的状态来进行表达。

![image-20240222175131715](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222175131715.png)

> 这里和HTN的一个重点的不同在于，Goal Set中的每一个goal都是用很多state去定义的（一般来说都是用bool值来表达，比如说Goal是解毒，那么State1可能是中毒状态=false，State2可能是存活=true）。
>
> **这里就可以看到，在GOAP中一个Goal可以用若干bool值的state来定量进行表达。**



#### （b）Action Set

action set则接近于primitive task的概念，它表示AI可以执行的行为。需要注意的是action set还包含**代价(cost)**的概念，它表示不同动作的”优劣”程度。在进行规划时我们希望AI尽可能做出代价小的决策。

![image-20240222175823568](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222175823568.png)

> 引入cost是因为在GOAP方法中，我们其实并没有一棵树来存储Task彼此的结构，因此需要cost来帮助AI做判断。



### （2）Planning

GOAP在进行规划时会从目标来倒推需要执行的动作，这一过程称为**反向规划(backward planning)**。其实这也比较符合人类决策的过程（比如说我为了全图鉴，就要获得所有角色；为了获得所有角色，就要有原石；为了有原石，就要充钱( ╯□╰ )）。

在进行规划时首先需要根据优先级来选取一个目标，然后查询实现目标需要满足的状态。为了满足这些状态需求，我们需要从action set中选择一系列动作。需要注意的是很多动作也有自身的状态需求，因此我们在选择动作时也需要把这些需求添加到列表中。最后不断地添加动作和需求直到所有的状态需求都得到了满足，这样就完成了反向规划。具体过程为：

- （1）首先，依据优先级选择一个满足precondition条件的goal出来；
- （2）比较选择的goal里的所有state和world state。这样就可以找到还没有满足的state（unsatisfied state），并且把这些state放入到一个栈当中（见下图左上）；
- （3）在unsatisfied states组成的栈中选择栈顶元素，其代表的就是一个未满足的state，在action set中选择一个对应effect可以满足这个state的action，如果找到可以满足这个state的action就弹出栈顶元素（见下图右上）；
- （4）上一步选择的Action会被放入Plan Stack中，作为plan的一部分。同时检查该Action的precondition是否满足，如果不满足的话把对应的state加入到unsatisfied states组成的栈中。（见下图下半部分）

![image-20240222181824216](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222181824216.png)

最终想要规划的内容是，找到一个Action的序列，可以使得Stack of unsatisfied states正好能够清空，并且最好对应的cost也是最小的。



### （3）求解

GOAP的难点在于如何从action set进行选择，我们要求状态需求都能够得到满足而且所添加动作的代价要尽可能小。显然这样的问题是一个**动态规划(dynamic programming)**问题，我们可以利用图这样的数据结构来进行求解。在构造图时把状态的组合作为图上的节点，不同节点之间的有向边表示可以执行的动作，边的权重则是动作的代价。这样整个规划问题就等价于在有向图上的最短路径问题。

![image-20240222182233820](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240222182233820.png)

> 有几点说明：
>
> - 每个Node是states的集合，比如说我们要寻找从final goal开始，到current state的最短路径，那么每个Node里面可能是这样的{true, false, true.....}，即所有bool型state的状态；
> - Edge表示的是Action，当然要满足precondition的条件；

于是问题就转换成为了最短路径问题，可以用A*寻路算法来解决。其中的Heuristics项可以用unsatisfied state的数量来表示。



总结一下GOAP可以让AI的行为更加动态，而且可以有效地解耦AI的目标与行为（注：对比HTN，HTN can easily make precondition/effect mismatching mistakes）；

而GOAP的主要缺陷在于它会比较消耗计算资源，一般情况下GOAP需要的计算量会远高于BT和HTN。另外还有一点是GOAP需要设计很多bool值来表示整个游戏环境，这实际上对于很复杂的策略游戏（如RTS）是不太现实的。



## 3.蒙特卡洛树搜索

这部分其实与AI的关系会大一些了，在104笔记就不单独整理了，复习的时候可以看[17.游戏引擎Gameplay玩法系统：高级AI (Part 1) | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1iG4y1i78Q/?spm_id_from=333.788&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)这个视频的1：07：24~1：46：50的部分。



## 4.机器学习基础

毕竟研究生是读AI方向的，因此AI相关的感觉不太用记笔记，贴一个视频的链接吧（[17.游戏引擎Gameplay玩法系统：高级AI (Part 2) | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1ja411U7zK/?spm_id_from=333.788&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)）。后面有需要直接照着视频进行复习即可。



# 二十、 18 网络游戏的架构基础

网络游戏和单机游戏相比有很多难点：比如说如何保证每个玩家的游戏状态是一致的、如何进行网络同步、如何处理延迟和丢包、如何检测玩家的作弊行为、如何处理不同的设备和系统、如何设计高性能的服务器系统等等。这些网络游戏专有的问题都为游戏引擎的开发提出了更大的挑战。

## 1.网络协议

在介绍网络游戏相关的内容前我们先来介绍一下**网络协议(network protocols)**。实际上互联网的概念最早是由Vint和Robert提出的，他们设计了TCP/IP协议从而实现了不同设备基于电话线和卫星的通信。

### （1）网络分层

网络协议要解决的核心问题是如何实现两台计算机之间的数据通信，当软件应用和硬件连接不断地变得复杂时直接进行通信是非常困难的。因此人们提出了**中间层(intermediate layer)**的概念来隔绝掉应用和硬件，使得开发者可以专注于程序本身而不是具体的通信过程。

在现代计算机网络中人们设计了**OSI模型(OSI model)**来对通信过程进行封装和抽象。

![image-20240223100807211](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223100807211.png)



### （2）Socket

对于网络游戏开发来说一般不需要接触到很底层的通信协议，在大多数情况下只需要知道如何使用**socket**建立连接即可。socket是一个非常简单的结构体，我们只需要知道对方的IP地址和端口号就可以使用socket建立连接来发送和接收数据。建立连接时需要额外注意到底是使用IPv4还是IPv6，使用TCP还是UDP协议等问题。

![image-20240223101223378](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223101223378.png)

> 虽然现在国内大部分还是在使用IPv4，但是如果放眼全球的话很多地方已经开始使用IPv6了，所以如果引擎要支持全球联网的话一定要实现基于IPv6的socket。



### （3）TCP

TCP是最经典也是著名的网络协议，它可以确保发送端发送的数据包都按照顺序被接收端接收，并且具有流量控制、拥塞控制的功能。TCP的核心是**retransmission mechanism**，这个机制要求接收端收到消息后会向发送端发送一个ACK，而发送端只有接收到这个ACK之后才会继续发包。当然TCP实际使用的机制要比上述的过程复杂得多。

当TCP出现网络拥堵时会主动调节单次发包的数量。如果发包都能顺利地接收到则会提高发包数量以提升效率，反之则会减少发包数量以提升稳定性。

> 更多的内容可以看PPT或者直接复习计算机网络部分的TCP协议即可。



### （4）UDP

除了TCP之外人们还开发出了UDP这样的轻量级网络协议。UDP的本质是一个端到端的网络协议，它不需要建立长时间的连接，也不要求发送数据的顺序，因此UDP要比TCP简单得多。



在现代网络游戏中根据游戏类型的不同使用合适的网络协议，比如说对于实时性要求比较高的游戏会优先选择UDP，而策略类的游戏则会考虑使用TCP（比如《炉石传说》，对延迟其实并没有那么敏感）。在大型网络游戏中还可能会使用复合类型的协议来支持游戏中不同系统的通信需求（例如大型MMO游戏可能用TCP来做签名认证，判断登录信息，聊天功能，邮件功能等，用UDP协议来做战斗系统）。

![image-20240223102503770](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223102503770.png)



### （5）Reliable UDP

同时现代网络游戏中往往还会对网络协议进行定制。以TCP为例，虽然TCP协议比较稳定但是效率过于低了，而且实际在网络游戏中出现一定的丢包是可以接受的；而对于UDP来说它虽然非常高效但是却不够稳定。

因此现代网络游戏中往往会基于UDP来定制一个网络协议，这样既可以利用UDP的高效性又可以保证数据通信的有序性。我们往往需要以下的特性：

- （1）Keep-alive 的连接（TCP）
- （2）很多时候希望逻辑的信息包能够按顺序发送（TCP）
- （3）高响应速度，低延迟（UDP）
- （4）能够很好地broadcast消息（UDP）



#### （a）ACK & SEQ

ACK及其相关技术是保证数据可靠通信的基本方法：

- Positive acknowledgment (ACK)是在通信进程、计算机或设备之间传递以表示确认或接收消息的信号。
- Negative ACK（NACK）是用来拒绝先前接收到的消息或指示某种错误的信号。
- Sequence number (SEQ) is a counter used to keep track of every byte sent outward by a host
- Timeouts



#### （b）ARQ

**ARQ(automatic repeat request)**是基于ACK的错误控制方法，所有的通信算法都要实现ARQ的功能。这个具体可以看这篇博客：[TCP可靠传输：ARQ协议（停止等待、超时重传、滑动窗口、回退N帧、选择重传）-CSDN博客](https://blog.csdn.net/aaahuahua/article/details/119965804)。

**滑动窗口协议(sliding window protocol)**是经典的ARQ实现方法，它在发送数据时每次发送窗口大小的包然后检验回复的ACK来判断是否出现丢包的情况。有如下几种策略：

- Stop-and-wait ARQ：一个缺陷在于它需要等待接收端的ACK才能继续发送数据，因此在很多情况下它无法完全利用带宽。

- ##### Go-Back-N ARQ：对滑动窗口协议的一种改进方法是**Go-Back-N ARQ**，当出现丢包时它只会把窗口内的包重新发送。这也是游戏引擎中比较推荐的实现方法。

- 另一种改进方法是**selective repeat ARQ**，利用NACK的机制，它只会重新发送丢失或损坏的包从而进一步提升带宽的利用率。

> 这里有很多实现上的细节，不过现在有很多开源库在解决各种问题，所以也是属于有需要再看吧。



#### （c）解决丢包问题——FEC

在网络游戏中需要额外处理丢包的问题，因此我们在自定义网络协议时一般会结合**forward error correction(FEC)**的方法来避免数据的反复发送。简单理解使用FEC可以把丢包的内容还原回来。

![image-20240223111626139](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223111626139.png)

目前常用的FEC算法包括异或校验位以及Reed-Solomon codes两大类。

- 异或校验位是使用**异或(XOR)**运算来恢复丢失数据的方法。这里需要注意的是当同时有多个包丢失时，使用异或校验位是无法恢复数据的。
- **Reed-Solomon codes**是经典的信息传输算法，它利用Vandemode矩阵及其逆阵来恢复丢失的数据。（神奇的数学）

具体的算法看这篇吧：[谈谈网络通信中的 FEC 基础 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/104579290)，讲的很清楚了。



总结一下，在自定义UDP时需要考虑ARQ和FEC两类问题。

![image-20240223112913211](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223112913211.png)



## 2.Clock Synchronization

有了网络协议后就可以开始对网络游戏进行开发了，不过在具体设计游戏前我们还需要考虑不同玩家之间的时钟同步**(clock synchronization)**问题。

### （1）Round Trip Time

由于网络通信延迟的存在，客户端向服务器端发送一个包后都需要等待一定的时间才能收到回包，这个间隔的时间称为**round-trip time(RTT)**。RTT的概念类似于ping，不过它们的区别在于ping更加偏向于底层而RTT则位于顶部的应用层。

![image-20240223121337206](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223121337206.png)



### （2）Network Time Protocol

利用NTP就可以实现不同设备之间的时间同步。实际上不仅仅是网络游戏，现实生活中的各种电子设备进行同步都使用了NTP的技术。在实际设备的时间同步过程中一般会利用层次化的结构来进行实现（一层一层进行同步，不过NTP里往往用一层就行，即客户端去同步服务器的时间）。

NTP的算法实际上非常简单，我们只需要从客户端发送请求然后从服务器接收一个时刻就好，这样就可以得到4个时间戳。如果我们进一步假定网络上行和下行的延迟是一致的，我们可以直接计算出RTT的时间长短以及两个设备之间的时间偏差。当然需要注意的是在实际中网络上行和下行的带宽往往是不一致的，因此这个算法也不是十分的严谨。

![image-20240223122939336](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223122939336.png)

实际上我们可以基于信息论证明，在不可靠的通信中是无法严格校准时间的。不过在实践中我们可以通过不断的使用NTP算法来得到一系列RTT值，然后把高于平均值1.5倍的部分丢弃（认为这部分数据是受到网络波动影响的），剩下的RTT取平均值就可以作为真实RTT的估计。如下图所示：

![image-20240223123606400](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223123606400.png)



## 3.Remote Procedure Call（RPC）

### （1）Socket Programming

尽管利用socket我们可以实现客户端和服务器的通信，但对于网络游戏来说完全基于socket的通信是非常复杂的。这主要是因为网络游戏中客户端需要向服务器发送大量不同类型的消息，同时客户端也需要解析相应类型的返回数据，这就会导致游戏逻辑变得无比复杂。并且客户端和服务器往往有着不同的硬件和操作系统，这些差异会使得游戏逻辑更加复杂且难以调试。

### （2）RPC

因此在现代网络游戏中一般会使用**RPC(remote procedure call)**的方式来实现客户端和服务器的通信。基于RPC的技术在客户端可以像本地调用函数的方式来向服务器发送请求，这样使得开发人员可以专注于游戏逻辑而不是具体底层的实现。

![image-20240223125336908](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223125336908.png)

以下是一个使用GO语言的调用RPC的例子：

![image-20240223125540293](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223125540293.png)



在RPC中会大量使用**IDL(interface definiton language)**来定义不同的消息形式。比较经典的应该是Google的Protobuf（回忆在引擎工具链部分对应的Schema知识点）。

![img](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/zyH16Q8.png)

然后在启动时通过**RPC stubs**来通知客户端有哪些RPC是可以进行调用的。

![img](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/9LamOli.png) ![img](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/lU7y4gU.png)

当然真实游戏中的RPC在实际进行调用时还有很多的消息处理和加密工作。

![img](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/E8B4iMu.png)



## 4.网络拓扑结构

### （1）Peer-to-Peer

在设计网络游戏时还需要考虑网络自身的架构。最经典的网络架构是**P2P(peer-to-peer)**，此时每个客户端之间会直接建立通信。

当P2P需要集中所有玩家的信息时则可以选择其中一个客户端作为主机，这样其它的客户端可以通过连接主机的方式来实现联机。

> P2P的架构很多时候比较适用于少量玩家开房间联机的游戏功能，比如Minecraft。可能建立房间的玩家机器会被作为服务器，其他玩家作为客户端连接该服务器。

很多早期经典的游戏都是使用这样的网络架构来实现联网功能（局域网连接），比如求生之路2。



### （2）Dedicated Server（专用服务器）

在现代网络游戏中更多地会使用**dedicated server**这样的网络架构，此时网络中有一个专门的服务器向其它客户端提供服务。

从实践结果来看，对于小型的网络游戏P2P是一个足够好的架构，而对于大型的商业网络游戏则必须使用dedicated server这样的形式。



**高延迟的一种解决策略**

> 举个例子，某游戏在上海创建了一个服务器集群，而如果全国各地的客户端都直接连接上海的服务器的话，距离太远的网络延迟是不可接受的。一种解决方案是在全国范围内设置很多portal（如下图灰色部分），由portal统一接收消息，并且不同的portal会通过一条高速的链路（比如走光纤）直接传输到总服务器，从而解决距离远造成的延迟高的现象。

![image-20240223131739419](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20240223131739419.png)



## 5.Game Synchronization

在前面的章节中我们介绍过游戏世界是分层的。从玩家的角度来看，玩家的操作通过输入层一路向下到达游戏逻辑层，然后通过渲染器展示给玩家。而在网络游戏中，除了单机游戏都需要的分层外我们还需要考虑不同玩家之间的同步。在理想情况下我们希望客户端只负责处理玩家的输入，整个游戏逻辑都放在服务器端。

由于延迟的存在，不同玩家视角下的对方可能会有不同的行为表现，因此我们需要使用游戏同步技术来保证玩家的游戏体验是一致的。**目前常用的同步技术包括快照同步、帧同步以及状态同步等。**



### （1）Snapshot Synchronization

**快照同步(snapshot synchronization)**是一种相对古老的同步技术。在快照同步中客户端只负责向服务器发送当前玩家的数据，由服务器完成整个游戏世界的运行。然后服务器会为游戏世界生成一张快照，再发送给每个客户端来给玩家反馈。

- 快照同步可以严格保证每个玩家的状态都是准确的，但其缺陷在于它给服务器带来了非常巨大的挑战。因此在实际游戏中一般会降低服务器上游戏运行的帧率来平衡带宽，然后在客户端上通过插值的方式来获得高帧率。
- 由于每次生成快照的成本是相对较高的，为了压缩数据我们可以使用状态的变化量delta来对游戏状态进行表示。
- 快照同步非常简单也易于实现，但它基本浪费掉了客户端上的算力同时在服务器上会产生过大的压力，并且由于许多客户端带来的巨额上行带宽也是不可接受的。因此在现代网络游戏中基本不会使用快照同步的方式。



### （2）帧同步

**帧同步(lockstep synchronization)**是现代网络游戏中非常常用的同步技术。不同于快照同步完全通过服务器来运行游戏世界，在帧同步中服务器更多地是完成数据的分发工作。玩家的操作通过客户端发送到服务器上，经过服务器汇总后将当前游戏世界的状态返还给客户端，然后在每个客户端上运行游戏世界。



# 二十二、 20 面向数据编程与任务系统

DOP：Data-Oriented Programming：面向数据的编程

## 1.并行编程

并行化编程的基础：进程和线程的区别：[(99+ 封私信 / 69 条消息) 线程和进程的区别是什么？ - 知乎](https://www.zhihu.com/question/25532384/answer/411179772)。这是一个基本的概念，需要熟练掌握。

### （1）多任务模型——抢占式与非抢占式

![image-20250201193611410](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201193611410.png)

在操作系统中，多任务模型允许多个任务或进程）并发执行。

- preemptive：抢占式：操作系统可以随时中断当前运行的任务，并将CPU资源分配给其他任务。这种中断通常由时钟中断或更高优先级任务的到来触发。目前的操作系统一般都是抢占式的。（例如Windows）
- non-preemptive：非抢占式：此时任务一旦获得CPU，就会一直运行直到完成或主动放弃CPU（如等待I/O或调用阻塞函数）。



### （2）Thread Context Switch 线程上下文切换

![image-20250201194346922](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201194346922.png)

从上图可以看出，线程的切换需要中断，而中断需要相当多的CPU Cycle（2000个左右）。并且调进来的线程所需要的数据很可能并不在cache当中，因此还要从内存中再加载（又需要10000~1000000的CPU Cycle）。可见，**线程的切换是十分昂贵的。**这也就引出了后文Job System的设计。

更为具体的，可以看这篇：[进程/线程上下文切换会用掉你多少CPU？ - 知乎](https://zhuanlan.zhihu.com/p/79772089)，可看看原理。



### （3）并行化开发带来的问题

![image-20250201201442822](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201201442822.png)

上图里的Embarrassingly Parrallel常被翻译为“天然并行”或者“易并行”，是并行计算中的一个概念，用来描述一类可以轻松分解为**多个完全独立子任务**的问题。这类问题的特点是：子任务之间不需要通信或者同步，可以非常高效地并行执行，几乎不需要额外协调成本。**典型的例子是蒙特卡洛模拟、批处理、机器学习同时测试多个超参数组合、以及电影渲染中将不同帧分配给不同计算节点。**

而非Embarrassingly Parrallel也很常见，此时任务间需要通信或同步（比如流体动力学模拟当中的迭代算法），此时并行复杂度较高，需要解决竞态条件、死锁等问题。

可回顾：**死锁的必要条件**。

> 可补充：C++并行化编程。这部分Games104的PPT上介绍的比较详细，就不再整理了。可以参考：[Job System](https://games-1312234642.cos.ap-guangzhou.myqcloud.com/course/GAMES104/GAMES104_Lecture20.pdf)

并行化编程很可能会造成data race的问题，解决方案可以使用锁或者信号量（semaphore）。

使用锁lock带来的局限性：

- （1）会带来额外的性能开销；
- （2）如果上锁的线程异常终止了，很可能会造成死锁问题；
- （3）如果低优先级任务占有了锁，一个优先级更高的任务会拿不到锁；



另一种解决并行化编程可能出现的data race的问题，可以使用**原子操作。**C++ 11中有提供对应的操作（未实际测试）。

![image-20250201203057482](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201203057482.png)

C++中提供了`volatile`（限制编译器重排序行为），`atomic`等关键词来对多线程编程做更好的控制，以下链接可以简单看看：[C/C++ 中 volatile 关键字详解 | 菜鸟教程](https://www.runoob.com/w3cnote/c-volatile-keyword.html)



### （4）Compiler Reordering Optimizations

直接看Games104的课程即可。核心问题可以用下图来概括：

![image-20250201203300023](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201203300023.png)

此时在多线程的编程模式下，很可能会出现debug和release模式执行顺序不一致的问题。

> 编译器进行指令重排序的主要目的是提高程序的执行效率，包括利用指令集并行性、优化内存访问、减少依赖等待以及适应硬件特性。



## 2.游戏引擎并行架构

### （1）Fixed Multi-thread

一个简单的多线程模型如下：

![image-20250201204314039](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201204314039.png)

这也是大部分现代游戏引擎的做法。此时每个线程会在每个frame开始的时候交换数据。这样的架构有以下问题：

- （1）不能保证每个线程的workload是一致的。有的线程的比较大，有的比较小，不均匀。并且游戏场景是多变的，不同场景给每个线程会造成不同的workload。
- （2）假设预先配置了4个thread，运行在2核的电脑会比较麻烦，运行在8核的电脑上又浪费了4个核。



### （2）Thread Fork-Join

![image-20250201205237706](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201205237706.png)

也比较好理解，对于类似Animation的任务，其可以`Fork`出一些子线程，分别并行运算，并将结果`Join`到一起。这种方式也会造成一些问题：

- （1）逻辑上不好写：work split怎么分？需要多少个work threads？
- （2）太多的线程，在上下文切换的时候会带来额外性能开销；
- （3）从上图也可以看出，多个核不平衡的workload问题依旧没有得到解决。



**Unreal Parallel Framework**

其实虚幻引擎就是类似于Thread Fork-Join的架构：

![image-20250201205908182](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201205908182.png)

- Named Thread：明确的指出每个thread是针对什么的，比如逻辑thread，渲染thread；
- Worker Thread：把物理、动画、特效、粒子之类的可以扔进Worker thread做展开。

如果对多线程的要求没有那么高的话，Thread Fork-Join也是一个不错的架构。



### （3）Task graph

每个节点存Task，每条边存Dependency.

![image-20250201210515336](Games104%20%E7%AC%94%E8%AE%B0%E5%85%A8.assets/image-20250201210515336.png)

Task Graph也有一些问题：

- 实际上，游戏运行中往往依赖关系不是一成不变的，对于task graph来说动态的修改会比较麻烦；
- 早期的版本无法实现”某个task执行到一半，需要等待其他task完成才能继续执行“这个需求。



### （4）Job System

现代游戏引擎中使用的比较多的概念。**比较重要。**

#### （a）协程Coroutine

`yield`的意思是”让路“。在`Go`和`C#`中协程是比较好实现的，但在C++中比较头疼。**这部分也是常考题目。**

> 可以看[20.现代游戏引擎架构：面向数据编程与任务系统 (Part 1) | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1EP411V7jx/?spm_id_from=333.788.videopod.sections&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)这里的50min左右的地方，结合PPT来辅助复习。

协程不需要操作系统内核态的切换。

协程分为两种：

- 有栈协程：切换时会恢复上下文，这是比较常用的协程；
- 无栈协程：一般不推荐实现，但速度更快。除非是引擎非常底层且高度可控制的代码可以上无栈编程（甚至够猛直接上汇编也可以）。

> C++这种底层语言不支持Coroutine，但`Boost`里面似乎有，通过插入汇编代码手动分配栈空间来实现。（目前不打算尝试 ）不过C++协程有一些开源项目有实现。

其他可参考的链接：[【迭代器模式】深入理解协程 - 知乎](https://zhuanlan.zhihu.com/p/356632347)



#### （b）Fiber-based Job System

明天再做整理，先把视频看完。



## 3.ECS

大部分内容直接复习Games104的课和PPT就好，这里放一些不太好理解的。

### （1）Archetype的概念

> 在 **ECS（Entity-Component-System）** 架构中，**Archetype** 是一个核心概念，用于高效地组织和存储实体（Entity）及其组件（Component）。理解 Archetype 的概念对于掌握 ECS 的性能优势和设计思想至关重要。
>
> ---
>
> ### **1. 什么是 Archetype？**
> **Archetype** 是 **实体组件组合的类型**。它定义了具有相同组件组合的实体的存储结构。换句话说：
> - 每个 Archetype 对应一种 **唯一的组件组合**。
> - 所有具有相同组件组合的实体会被存储在同一个 Archetype 中。
>
> 例如：
> - 实体 A：`[Position, Velocity]`
> - 实体 B：`[Position, Velocity, Health]`
> - 实体 C：`[Position, Velocity]`
>
> 这里，实体 A 和 C 属于同一个 Archetype（`[Position, Velocity]`），而实体 B 属于另一个 Archetype（`[Position, Velocity, Health]`）。
>
> ---
>
> ### **2. Archetype 的存储结构**
> Archetype 的核心设计目标是 **高效的内存访问** 和 **快速的组件查询**。为了实现这一点，Archetype 采用以下存储方式：
>
> #### **(1) 组件数组（Component Arrays）**
> - 每个 Archetype 包含一组 **连续的数组**，每个数组存储一种组件的实例。
> - 例如，Archetype `[Position, Velocity]` 包含：
>   - 一个 `Position` 数组：`[Position1, Position2, ...]`
>   - 一个 `Velocity` 数组：`[Velocity1, Velocity2, ...]`
>
> #### **(2) 实体与组件的映射**
> - 每个 Archetype 维护一个 **实体列表**，记录属于该 Archetype 的所有实体。
> - 实体在组件数组中的索引与其在实体列表中的索引一一对应。
>
> #### **(3) 内存连续性**
> - 组件数组在内存中是 **连续存储** 的，这使得迭代和访问组件时具有极高的缓存命中率。
>
> ---
>
> ### **3. Archetype 的优势**
> Archetype 的设计带来了以下性能优势：
>
> #### **(1) 高效的内存访问**
> - 组件数据在内存中连续存储，适合 CPU 缓存机制，减少缓存未命中。
> - 迭代时可以直接遍历组件数组，无需跳转内存。
>
> #### **(2) 快速的组件查询**
> - 通过 Archetype 可以快速筛选出具有特定组件组合的实体。
> - 例如，查询所有具有 `[Position, Velocity]` 的实体时，只需遍历对应的 Archetype。
>
> #### **(3) 动态组件管理**
> - 当实体添加或删除组件时，ECS 会自动将其移动到新的 Archetype 中。
> - 这种设计避免了传统 OOP 中频繁的内存分配和释放。
>
> ---
>
> ### **4. Archetype 的工作原理**
>
> #### **(1) 创建 Archetype**
> - 当第一个具有某种组件组合的实体被创建时，ECS 会为该组合创建一个新的 Archetype。
> - 例如，创建实体 `[Position, Velocity]` 时，ECS 会生成一个 Archetype 并存储该实体。
>
> #### **(2) 添加/删除组件**
> - 当实体添加或删除组件时，ECS 会将其从当前 Archetype 移动到新的 Archetype。
> - 例如：
>   - 实体 A 原本属于 Archetype `[Position, Velocity]`。
>   - 添加 `Health` 组件后，ECS 会将其移动到 Archetype `[Position, Velocity, Health]`。
>
> #### **(3) 查询实体**
> - 查询时，ECS 会遍历所有 Archetype，筛选出符合查询条件的实体。
> - 例如，查询所有具有 `Position` 组件的实体时，ECS 会遍历所有包含 `Position` 的 Archetype。
>
> ---
>
> ### **5. Archetype 的示例**
>
> #### **场景描述**
> 假设有以下实体：
> - 实体 1：`[Position, Velocity]`
> - 实体 2：`[Position, Velocity, Health]`
> - 实体 3：`[Position, Velocity]`
>
> #### **Archetype 存储结构**
> - **Archetype A**：`[Position, Velocity]`
>   - 实体列表：`[实体1, 实体3]`
>   - 组件数组：
>     - `Position` 数组：`[Position1, Position3]`
>     - `Velocity` 数组：`[Velocity1, Velocity3]`
> - **Archetype B**：`[Position, Velocity, Health]`
>   - 实体列表：`[实体2]`
>   - 组件数组：
>     - `Position` 数组：`[Position2]`
>     - `Velocity` 数组：`[Velocity2]`
>     - `Health` 数组：`[Health2]`
>
> ---
>
> ### **6. Archetype 的挑战与优化**
>
> #### **(1) 内存碎片**
> - 当实体频繁添加/删除组件时，Archetype 的拆分和合并可能导致内存碎片。
> - **优化**：使用内存池或预分配策略减少动态内存分配。
>
> #### **(2) 查询性能**
> - 当 Archetype 数量过多时，查询性能可能下降。
> - **优化**：使用缓存或索引加速查询。
>
> #### **(3) 动态组件变化**
> - 频繁的组件变化会导致实体在 Archetype 之间移动，增加开销。
> - **优化**：尽量减少运行时组件的变化。
>
> ---
>
> ### **7. 总结**
> **Archetype** 是 ECS 架构中的核心概念，用于高效组织和存储实体及其组件。它的设计通过 **连续内存存储** 和 **组件组合分类**，显著提升了内存访问和查询性能。理解 Archetype 的工作原理，有助于更好地设计和优化基于 ECS 的系统。




# 附：《游戏引擎架构》阅读笔记

