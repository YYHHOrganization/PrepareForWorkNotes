# Text-Guided 3D Face Synthesis - From Generation to Editing



# 一、大概内容

## 1.Abstract

​        文本引导的3D面部合成通过利用文本到图像（T2I）扩散模型取得了显著成果。然而，大多数现有工作只专注于直接生成，忽略了编辑，这限制了它们通过迭代调整来合成定制化的3D面部。在这篇论文中，我们提出了一个**从面部生成到编辑的统一文本引导框架**。在生成阶段，我们提出了一个几何-纹理解耦生成，以减轻由耦合引起的几何细节丢失。此外，解耦使我们能够利用生成的几何形状作为纹理生成的条件，从而获得高度几何-纹理对齐的结果。

​	我们进一步**使用一个微调的纹理扩散模型在RGB和YUV空间中增强纹理质量**（==增强纹理质量？看看后续怎么优化==）。在编辑阶段，我们首先使用一个预训练的扩散模型根据文本更新面部几何或纹理。

​	为了实现序列化编辑，我们引入了一个UV域一致性保持正则化，以防止对无关面部属性的意外变化。此外，我们提出了一个自我引导的一致性权重策略，以提高编辑效率，同时保持一致性。通过全面的实验，我们展示了我们方法在面部合成方面的优越性。项目页面：https://faceg2e.github.io/。（这一段的原文：To enable sequential editing, we introduce a UV domain consistency preservation regularization, preventing unintentional changes to irrelevant facial attributes. Besides, we propose a self-guided consistency weight strategy to improve editing efficacy while preserving consistency. Through comprehensive experiments, we showcase our method’s superiority in face synthesis）



## 2.Introduction

​	建模3D面孔是各种新兴应用的基本支柱，比如电影制作、视频游戏和增强现实/虚拟现实。传统上，创建详细复杂的3D人脸需要高技能的艺术家投入大量时间。随着深度学习的发展，现有的研究 [8, 10, 47, 56] 尝试使用生成模型从照片或视频中生成3D面孔。然而，生成的多样性主要受限于训练数据规模的限制。幸运的是，最近大规模的视觉-语言模型（比如CLIP [33]、Stable Diffusion [35]）为生成多样化的3D内容铺平了道路。通过整合这些模型，许多文本到3D的作品[23, 28, 29, 50, 52]可以以零样例（zero-shot）方式创建3D内容。

​	已经进行了许多关于文本到3D人脸合成的研究。它们要么使用CLIP，**要么采用文本到图像(T2I)模型的得分蒸馏采样(SDS)来引导3D人脸合成。**一些方法[46，53]采用神经场来生成视觉吸引人但质量较低的几何3D人脸。最近，Dreamface [54]已经展示了利用面部纹理上的SDS生成高质量3D面部纹理的潜力，但他们的几何精度不足，并且忽视了随后的面部编辑。少数作品[2，12，27]可以实现文本引导的面部编辑，允许进行粗粒度的编辑（例如，整体风格），但不能进行细粒度的调整（例如，唇色）。此外，他们在精确编辑控制的设计上的缺失导致在编辑过程中出现意外的变化，阻止了通过顺序编辑合成定制面部。

> 补充内容：
>
> 【1】SDS：score distillation sampling，得分蒸馏采样（Score Distillation Sampling，SDS）是一种机器学习技术，主要用于生成模型。这种方法通过对预先训练的模型生成的大量样本进行采样，再通过训练过程提取这些样本的特征（或称为“分数”），然后利用这些特征进行新样本的生成。这种方法可以高效地生成高质量的输出，同时保留并增强了原始模型的性能。
>
> **其他生成3D人脸的方法：NERF, CLIP**
>
> 【2】CLIP（Contrastive Language-Image Pretraining）是OpenAI发表的一种可以理解图像和文本之间关系的人工智能模型。CLIP通过同时学习图像和文本表示，然后通过文本描述从大量图像中找出相应的图像，或者相反，从大量的文本信息中找出与给定图片相匹配的描述，揭示了文本和图像之间的相互关联。这种方法能够以强大并且灵活的方式理解图像和文本，被广泛应用在图像分类，对象检测，文本到图像生成等各种任务中。

​	为了解决上述挑战，我们提出了一个名为**FaceG2E** 的文本引导的 3D 面部合成方法——从生成到编辑。我们提出了一个渐进式框架（progressive framework）来生成面部几何结构和纹理，然后进行由文本顺序控制的精确面部编辑。据我们所知，这是第一次尝试以顺序方式（sequential manner）编辑 3D 面部。我们提出了两个核心组件：（1）几何-纹理解耦生成和（2）自引导的一致性保持编辑。（(1) Geometry-texture decoupled generation and (2) Self-guided consistency preserved editing.）

​	为了具体说明，我们提出的几何-纹理解耦生成在两个独立阶段生成面部几何和纹理。通过结合无纹理渲染和SDS，我们引导T2I模型提供与几何相关的先验知识，**激发生成的几何形状中的细节（例如，皱纹，嘴唇形状）**。**在生成的几何形状基础上，我们利用ControlNet强制SDS意识到几何形状，确保精确的几何-纹理对齐。此外，我们对一个纹理扩散模型进行了微调，该模型融合了RGB和YUV颜色空间，用于在纹理领域计算SDS，从而提升了生成纹理的质量。**

> ==直观理解：==

​	我们新开发的自引导的一致性保持编辑使得人们可以按照文本进行高效的编辑，针对特定面部属性进行修改，而不会引起其他意外变化。在这里，我们首先使用预训练的图像编辑扩散模型来更新面部几何或纹理。然后我们引入了 UV 领域一致性保持规范化，以防止面部发生意外变化，使得顺序编辑成为可能。为了避免由于规范化导致编辑效果的退化，我们进一步提出了一个自引导的一致性加权策略。它通过将 T2I 模型的交叉注意力分数投影到 UV 领域，自适应地确定每个面部区域的规范化权重。如图 1 所示，我们的方法能够生成高保真度的 3D 面部几何结构和纹理，同时允许进行细粒度的面部编辑。通过提出的组件，我们在视觉和定量结果上都比其他 SOTA 方法表现得更好，如第 4 节所示。总之，我们的贡献包括：（这里省略贡献部分）



## 3.Related Work

### （1）Text-to-Image generation

这里就是正常介绍了一下Diffusion，以及使用Diffusion生成3D资产模型至今仍有较大的困难。



### （2）Text-to-3D generation

为了应对近年来文本到图像生成的成功，文本到3D生成在社区中引起了显著关注。早期方法[15, 21, 31, 39, 51]利用网格或隐式神经场来表示3D内容，并优化了2D渲染与文本提示之间的CLIP度量。然而，生成的3D内容的质量相对较低。最近，DreamFusion [32] 通过在强大的文本到图像扩散模型[38]中使用得分蒸馏采样（SDS）取得了令人印象深刻的成果。随后的工作通过减少生成时间[28]、改善表面材料表示[7]、以及引入精细的采样策略[19]进一步增强了DreamFusion。然而，高保真度和复杂3D面部的文本引导生成仍然具有挑战性。基于DreamFusion，我们精心设计了各阶段的得分蒸馏形式，通过利用各种扩散模型，实现了高保真度和可编辑的3D面部。



### （3）Text-to-3D face synthesis

最近，有人尝试从文本生成3D面孔。Describe3D [48] 和 Rodin [46] 提出了学习从文本到3D面孔的映射的方法，并在文本-面孔数据对上进行训练。他们仅使用在外貌描述上训练的映射网络来生成面孔，因此无法推广到域外的文本（例如名人或角色）。相反，我们的方法可以很好地推广到这些文本，并合成各种3D面孔。

其他作品[12、18、22、27、54]利用预训练的T2I模型进行SDS。Dreamface [54] 利用CLIP从candidates中选择面部几何形状。然后，他们使用纹理扩散网络进行SDS以生成面部纹理。Headsculpt [12]采用Stable Diffusion[35]和InstructPix2Pix [6]计算SDS，并依赖于SDS梯度的混合来约束编辑过程。这些方法不仅可以执行生成，还可以进行简单的编辑。然而，它们仍然缺乏精确编辑控制的设计，编辑结果中常常出现意想不到的变化。这使得它们无法通过顺序编辑合成高度定制的3D面孔。相反，我们的方法有助于准确编辑3D面孔，支持顺序编辑。

> 这里涉及到的工作（先把文章链接贴上来，有时间再看吧）：
>
> 【1】Describe3D：https://arxiv.org/pdf/2305.03302
>
> 【2】Rodin：https://arxiv.org/pdf/2212.06135
>
> 【3】Dreamface：https://arxiv.org/pdf/2304.03117
>
> 【4】Headsculpt：https://brandonhan.uk/HeadSculpt/，生成的结果全是洞，感觉肯定是不能用的，不过有时间看看思路是什么吧。
>
> 【5】InstructPix2Pix



## 4.Methodology

FaceG2E是一种渐进的文本到3D方法，首先生成一个高保真度的3D人脸，然后进行精细的面部编辑。如图2所示，我们的方法分为两个主要阶段：（a）几何-纹理解耦的生成，和（b）自引导一致性保持的编辑。

在第3.1节中，我们介绍了一些构成我们方法基础的预备知识。在第3.2节和第3.3节中，我们介绍了生成和编辑阶段。

### 对应文章3.1节 Preliminaries

![image-20241017161750603](./assets/image-20241017161750603.png)

![image-20241017161758455](./assets/image-20241017161758455.png)

> 补充：
>
> 【1】参数化3D 人脸模型：HIFI3D：论文为Highfidelity 3d digital human head creation from rgb-d selfies，链接：https://arxiv.org/abs/2010.05562
>
> 【2】SDS的基本介绍：



# 二、源码阅读

## 1.如何跑出这个代码

以下内容是在Colab当中跑的，重点核心部分如下（如果直接全部运行有问题就一句一句来，反正大概就是需要这些依赖的文件）：

```python
!git clone https://github.com/JiejiangWu/FaceG2E.git
%cd FaceG2E
!pip install diffusers==0.20.2
!pip install git+https://github.com/openai/CLIP.git
!pip install kornia
!git clone https://github.com/NVlabs/nvdiffrast
%cd nvdiffrast
!pip install .
%cd ..
!pip install "jax[cuda12_pip]==0.4.23" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
!pip install Ninja
```

然后，挂载Google Drive到Colab上，并把https://github.com/JiejiangWu/FaceG2E?tab=readme-ov-file这里提到的google Drive上的文件都放在对应的路径下面，用Linux的`unzip XXX`指令将文件解压。

> 有空格的文件名可能需要这么解压：`!unzip HIFI3D/Tencent\ AI-NEXT\ 3D\ Face\ Model\ \(East-Asian\ Version\).zip`

解压之后的文件布局：

![image-20241017160852185](./assets/image-20241017160852185.png)



![image-20241017161518464](./assets/image-20241017161518464.png)

接着在跑代码之前提前创建好exp/demo文件夹，否则可能会报错。

接着修改代码`util/io_util.py`中的第21行左右，原来的（**会导致报错**）：`imageio.imwrite(path,(img_.clip(0,1).detach().cpu().numpy()*255.).astype(np.uint8))`，修改完的版本为：

```python
import cv2
# 假设 img_ 是一个包含 RGB 数据的 Tensor
img_bgr = img_.clip(0, 1).detach().cpu().numpy() * 255.
img_bgr = img_bgr.astype(np.uint8)

# 将 RGB 转换为 BGR
img_bgr = img_bgr[..., ::-1]  # 对最后一个维度进行反转

# 使用 OpenCV 保存图像
cv2.imwrite(path, img_bgr)  # 这里有个坑，因为OpenCV似乎是以BGR格式存储RGB图像的
```



### 一个跑出的demo

```python
!python main.py --stage "coarse geometry generation" --text "a zoomed out DSLR photo of Emma Watson" --exp_root exp --exp_name demo --total_steps 201 --save_freq 40 --sds_input "norm grey-rendered" --texture_generation direct
```

这个会生成几何mesh，但diffusion贴图是一张纯灰色的贴图，Render之后的结果如下：

![image-20241017163231303](./assets/image-20241017163231303.png)

接下来我们生成Texture：

```python
!python main.py --stage "texture generation" --text "a zoomed out DSLR photo of Emma Watson"  --exp_root exp --exp_name demo --total_steps 401 --save_freq=40 --sds_input rendered --texture_generation latent --latent_sds_steps 200 --load_id_path "./exp/demo/a zoomed out DSLR photo of Emma Watson/coarse geometry generation/seed42/200_coeff.npy"
```

注意，这里的`200_coeff.npy`是上一步生成mesh的时候会生成的文件，这里需要保证对应的id_path是存在的，跑这个代码的结果为：



> 注：普通的Colab Tesla T4会一直报CUDA Out of Memory，无奈花钱租用A100了，效率至上，多点时间学别的。





## 2.Colab如何Debug代码

很可能由于算力不够或是其他的原因，我们需要去Google Colab上对代码进行debug以辅助代码的阅读，目前我能想到的是按照类似下篇的方式：https://stackoverflow.com/questions/51068987/how-to-add-a-breakpoint-in-jupyter-notebook，安装以下包：

```python
```

