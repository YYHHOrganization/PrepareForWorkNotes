# MotionLCM：实时动作生成与控制模型

介绍一下 

[@wxDai](https://www.zhihu.com/people/deb0676a720bd48d97b21f32f4f1d156)

 最新发布的MotionLCM，一个支持实时动作生成和可控生成的单步扩散模型！[论文](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2404.19759)、[代码](https://link.zhihu.com/?target=https%3A//github.com/Dai-Wenxun/MotionLCM)、[demo](https://link.zhihu.com/?target=https%3A//huggingface.co/spaces/wxDai/MotionLCM)、[项目主页](https://link.zhihu.com/?target=https%3A//dai-wenxun.github.io/MotionLCM-page)、[视频展示](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV1uT421y7AN/)等均已公开。



MotionLCM聚焦文生动作的基础任务，旨在生成合理、逼真的人体动作。以往基于[diffusion model](https://zhida.zhihu.com/search?content_id=242316111&content_type=Article&match_order=1&q=diffusion+model&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NDQ5NjA5NDQsInEiOiJkaWZmdXNpb24gbW9kZWwiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNDIzMTYxMTEsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.NHX6RW8-MkGEQFa-HDgFVzFtOODmlwWdGHuWr7j4YGE&zhida_source=entity)的工作面临的最大的挑战就是效率问题，即推理时间非常长。受到consistency model的启发，MotionLCM提出了在隐空间一步生成合理的latent，并通过decoder获得合理的动作。MotionLCM支持1-4步的推理管线，1步和4步的效果几乎无异。其效率和diffusion-based models相比有了很大的提高。下面是[FID](https://zhida.zhihu.com/search?content_id=242316111&content_type=Article&match_order=1&q=FID&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NDQ5NjA5NDQsInEiOiJGSUQiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNDIzMTYxMTEsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.3pyjBSZZnPN0lEZ7xvXuU2G9Q_fmQROcRXVy2VUlh3Y&zhida_source=entity)和速度的比较。我们生成一个～200帧的动作大概只需要30ms，平均到每一帧计算的话可以近似成～6k fps。

![img](https://pic1.zhimg.com/v2-0b660ee79c4271bed6ff057393ec18ae_1440w.jpg)

MotionLCM是效果最好的实时动作生成模型

毫无疑问，我们已经实现了速度和生成质量的trade-off。为了把这个工作往前推一步，我和文勋、靖博在讨论的时候思考一件事情：生成算法的实时性最大的应用场景是什么？我们一致同意探索一下MotionLCM的可控性，因为编辑、可控这件事是对实时性要求最高的。用户在给定一些条件（例如轨迹）的情况下，如何实时地判断并根据控制的结果编辑输出的动作，这是需要算法即时反馈的。所以我们对[latent space](https://zhida.zhihu.com/search?content_id=242316111&content_type=Article&match_order=1&q=latent+space&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NDQ5NjA5NDQsInEiOiJsYXRlbnQgc3BhY2UiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyNDIzMTYxMTEsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9._xpBoUGdoDesxG7Mb9qo1v8kdf0OLw67x6XTQdN7iBI&zhida_source=entity)的diffusion加入了控制模块，也就是Motion ControlNet，实现对动作的可控生成。从数值结果上看，我们的控制算法比效果最好的方法快1k倍。同时质量也不相上下。

![img](https://pic3.zhimg.com/v2-e74f1b90ff5e80852270a2afe53c39e0_1440w.jpg)

动作控制结果比较

我们在下面的视频中提供了一些文本转运动和可控运动生成结果的演示。 MotionLCM 支持密集或稀疏条件控制信号。

[MotionLCM B站demowww.bilibili.com/video/BV1uT421y7AN/![img](https://pica.zhimg.com/v2-09a660c51d59d30508786bbde7023bea_ipico.jpg)](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV1uT421y7AN/)

此外，我们提供了一个huggingace交互界面供大家测试，支持输出diverse结果、不同的动作时长。由于目前平台上没有GPU，只有共享的CPU资源，不能在平台上体验实时生成效果。可以down下来之后在本地部署体验。

![img](https://pic1.zhimg.com/v2-1460da57b637201b646a9d765ff60840_1440w.jpg)

huggingface demo

*Blog written by Ling-Hao Chen. Credit also with Wenxun, Jingbo, Jinpeng, Bo, Yansong.*







#### 测试

https://huggingface.co/spaces/wxDai/MotionLCM

A person sitting and raises his right hand, resting his head on it.

确实是不错的





一个人坐下后抬起左手，身体往左倾斜，慢慢靠在椅子上，并最终将头靠在左手上

A person sits down, raises his left hand, leans to the left, slowly leans back on the chair, and finally rests his head on his left hand.

这个效果一般



一个男人从站着到跪下，用右手捂住眼睛，左手多次捶地

A man kneels down from standing, covers his eyes with his right hand in frustration, and hits the ground with his left hand several times.



![image-20250416161439668](assets/image-20250416161439668.png)

A man transitions from standing to kneeling, repeatedly pounding the ground with his left fist in frustration while covering his eyes with his right hand in a gesture

![image-20250416164029010](assets/image-20250416164029010.png)

