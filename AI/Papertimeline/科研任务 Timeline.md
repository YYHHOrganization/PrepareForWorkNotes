# 科研任务 Timeline

# 2025.04.16

- [x] （重要）能够正确表述attention的意义，self-attention和cross-attention的作用和意义。（可以讲一下）
- [ ] 关注三篇前置/并行文章：3DShape2VecSet、Dora、Michelangelo
- [ ] 看一下DiT
- [ ] 阅读3D Generation的综述：Advances in 3D Generation: A Survey
- [ ] 简要阅读以下工作：Texture Fields， **NeRF-Tex**



# 2025.04.14~2025.04.18 周报

科研进展相关：阅读与3D AIGC Mesh生成的相关综述和文章，具体如下：

- （1）综述：《Advances in 3D Generation: A Survey》，目前还没读完，争取周末阅读完成；
- （2）【阅读完毕】Siggraph的文章，涉及shape的高效编码方式：3DShape2VecSet
- （3）【阅读完毕】DMTET原始论文：结合显式和隐式优点的3D表征方式，但生成的Mesh质量不是很高，不作为后续方案考虑了。
- （4）【阅读完mesh相关的部分，纹理的还没看】：腾讯的Hunyuan3D相关的论文，包含Mesh生成，纹理全套工作流。
- （5）【正在阅读】Zero-123以及系列工作，应该会对后面有一定指导作用。

下周目标：

- 读新的论文，以及之前没有读完的内容；
- 人脸可以延续前面的3DMM做法，但细节编辑以及纹理生成目前的研究还是做的不好，下周会调研完成人脸重建纹理生成的一些方案，以及一般纹理生成的方案（特别关注UV域怎么做迁移），Mesh的编辑也会调研一下，因为之前直接做在3DMM上的效果并不好，需要看看其他文章有什么别的思路。
- 重新跑起来之前的base 程序，对现有的问题和瓶颈进行整理。



可以考虑读：MeshCraft，meshgen，instantMesh，MVEdit，SceneTex，MeshGPT，《Scalable Diffusion Models with Transformers》，《Michelangelo: Conditional 3D Shape Generation based on Shape-Image-Text Aligned Latent Representation》，《What’s the Situation with Intelligent Mesh Generation: A Survey and Perspectives》，Flux这个开源项目，《Advances in text‑guided 3D editing: a survey》，《CLAY: A Controllable Large-scale Generative Model for Creating High-quality 3D Assets》，开源项目：[NVIDIAGameWorks](https://github.com/NVIDIAGameWorks)/**[kaolin](https://github.com/NVIDIAGameWorks/kaolin)**，



## 2025.04.21~2025.04.25 周报

科研进展相关：

- 阅读综述论文：《Advances in text‐guided 3D editing: a survey》
- 重新配置环境，跑通当时的FaceG2E的代码，回顾论文；
- 实践huggingface的diffusers库的一些官方文档，加深对pipeline的理解和实践；

下周计划：

- 阅读完成FaceG2E的代码，确认上次修改的地方和要修改的地方；
- 明确当时SDS Loss失败的原因，研究解决方案（Displacement map和deformation map生成效果很差，需要查明原因）；
- FaceG2E这篇工作的不足之处在于texture的生成效果不够好，同时编辑能力较差，这是完全可以提升的点，会去找一下比较新的工作能否解决这两个问题。





2025.05.01~2025.05.09 周报

科研进展相关:

- (1)详细了解了一致性模型Consistency Model和Latent Consitency Model,并阅读完成相关的源码;
- (2)将FaceG2E的源码部分进行理解,找到可以更新的点;



## 2025.05.12

- 找一下三维重建的多视角项目，重建出来的3D模型的结果在各个尺度上应该是正确的。但Hunyuan3D由于靠AI进行预测，同时输入的可能只有三视图，此时重建的结果在各个尺度上可能不够准确。**尝试将三维重建的精准结果与Hunyuan3D只依赖于三视图生成的结果进行对比，看一下Hunyuan3D可能有什么不足。**
- 以人体动作为例，假如三视图的动作不一致，那么是否Hunyuan3D生成的结果是好的？比如每个视角动作有所差别，是否还能生成好看的结果？

- 
