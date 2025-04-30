# Control Net

代码地址：[github.com/lllyasviel/…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Flllyasviel%2FControlNet)

论文地址：[arxiv.org/abs/2302.05…](https://link.juejin.cn/?target=https%3A%2F%2Farxiv.org%2Fabs%2F2302.05543v1)



分析：

https://juejin.cn/post/7210369671656505399

https://blog.csdn.net/qq_45752541/article/details/132619474





不得不读 | 深入浅出ControlNet，一种基于生成扩散模型Stable Diffusion、可控生成的AIGC绘画生成算法！ - AI生成创作的文章 - 知乎
https://zhuanlan.zhihu.com/p/617017935

## 原理



## **Adding Conditional Control to Text-to-Image Diffusion Models**

## **摘要**

- ControlNet，试图控制预训练大型扩散模型，以支持额外的输入条件。ControlNet以端到端方式学习特定任务的条件输入，即使训练数据集很小(< 50k)，效果也很健壮。
- 此外，训练ControlNet的速度与微调扩散模型一样快，而且该模型可以在个人设备上训练。或者，如果强大的计算集群可用，该模型可以扩展到大量(数百万到数十亿)的数据。
- 论文表明，像Stable Diffusion这样的大型扩散模型可以用ControlNet来增强，以支持像边缘map、分割map、关键点等条件输入。这将丰富大型扩散模型的控制方法，并进一步促进相关应用： 
- [https://github.com/lllyasviel/ControlNet](https://link.zhihu.com/?target=https%3A//github.com/lllyasviel/ControlNet)

## **背景**

- 随大型文本到图像模型的出现，生成视觉效果生动的图像只需要用户输入一个简短的描述性提示文本（prompt）。对此，可能有几个问题:
- 这种基于文本提示的生成，是否满足了我们的需求?
- 在图像处理中，许多长期存在的任务都有明确的问题解决公式，这些大型模型能否应用于促进这些特定的任务？应该构建什么样的框架可以统一来处理各种各样的问题条件和用户控制?
- 在特定的任务中，大型模型能否保持从数十亿张图像中获得的优势和能力?
- 为回答这些问题，本文研究了各种图像处理应用，并有三个发现：
- 首先，特定任务域的可用数据规模并不总是像一般图像-文本域那样大。许多具体任务(如对象形状、姿态理解等)的最大数据集大小往往在100k以下，即比LAION5B 小50000倍。这将需要鲁棒的神经网络训练方法，以避免过拟合，并在大模型针对特定问题进行训练时保持泛化能力。
- 其次，大型计算集群并不总是可用的。这使得快速训练方法对于在可接受的时间和内存空间内(例如在个人设备上)优化大型模型以执行特定任务非常重要。这将进一步需要利用预先训练的权重，以及微调策略或迁移学习。
- 第三，各种图像处理问题具有不同形式的问题定义、用户控制或图像标注。在解决这些问题时，虽然图像扩散算法可以手工做一些调整，例如，约束去噪过程、编辑多头注意力激活等，但考虑到一些特定的任务，如深度图转图像、姿势关键点到人像等，需要将原始输入解释为对象级或场景级的理解，要在许多任务中实现通用的学习解决方案，端到端学习是必不可少的。
- 端到端神经网络ControlNet，控制大型图像扩散模型来学习特定于任务的输入条件。ControlNet将大型扩散模型的权重克隆为一个“可训练副本”和一个“锁定副本”:锁定副本保留了从数十亿张图像中学习到的网络能力，而可训练副本则在特定任务的数据集上进行训练，以学习条件控制。
- 可训练和锁定神经网络块与一种称为“零卷积”的独特类型的卷积层连接，其中卷积权值以学习的方式从零逐步转变到优化后的参数。由于保留了权值，这样一来在不同规模的数据集上也具有鲁棒性。由于零卷积不会给深度特征添加新的噪声，因此与从头开始训练新层相比，训练速度与微调扩散模型一样快。
- 用不同条件的各种数据集训练几个ControlNet，例如，Canny边缘、Hough线、用户涂鸦、人体关键点、分割图、深度图等。还用小数据集(样本小于50k甚至1k)和大数据集(数百万样本)对ControlNets进行了实验。表明在一些任务中，如深度到图像，在个人计算机(一台Nvidia RTX 3090TI)上训练ControlNets，与在大型计算集群上训练的商业模型具有竞争力的结果。

### **HyperNetwork和神经网络结构**

- HyperNetwork起源于一种语言处理方法，用于训练一个小的循环神经网络来影响一个大的神经网络的权重。HyperNetwork也被应用于生成对抗网络等图像生成任务。ControlNet和HyperNetwork在影响神经网络行为的方式上有相似之处。ControlNet使用一种特殊类型的卷积层，称为“零卷积”。早期的神经网络研究广泛讨论了网络权值的初始化问题，包括高斯分布初始化权值的合理性以及用零初始化权值可能带来的风险。在ProGAN和StyleGAN以及Noise2Noise等工作中也讨论了初始卷积权值的操作。

### **扩散概率模型**

- 近来，扩散概率模型取得了巨大的研究进展，例如**去噪扩散概率模型(DDPM)**、**去噪扩散隐式模型(DDIM)**和基于分数的扩散模型等。研究人员在处理高分辨率图像时往往会考虑节省计算能力的策略，或直接使用基于金字塔或多阶段的方法，常见比如使用**U-net**作为神经网络结构。为了降低训练扩散模型所需的计算能力，基于图像潜在特征的思想，提出了**潜在扩散模型(latent diffusion model, LDM)**方法，并进一步扩展到**Stable Diffusion**。

### **文本到图像扩散模型**

- 扩散模型可以应用于文本到图像生成任务，以达到最先进的图像生成效果。这通常是通过使用**CLIP**等**预训练**好的语言模型将文本输入编码为潜在向量来实现的。例如，Glide是一个文本引导的扩散模型，同时支持图像生成和编辑。Disco Diffusion是clip引导实现、用于处理文本提示。Stable Diffusion实现潜在扩散。Imagen是一个文本到图像的结构，它不使用潜在图像，而是使用金字塔结构直接扩散像素。

### **预训练扩散模型的控制生成**

- 最先进的图像扩散模型，是由文本到图像的方法主导的，所以增强对扩散模型控制的最直接的方法，通常是文本引导。这种类型的控制也可以通过操纵CLIP特性来实现。图像扩散过程本身可以提供一些功能来实现颜色级别的细节变化(社区称之为img2img)。图像扩散算法当然支持inpainting作为控制结果的重要方式。而文本inversion和DreamBooth方法，基于具有相同主题或目标对象的小样本图像数据集，去自定义控制生成结果中的内容。

### **图像转换**

- Pix2Pix提出了图像到图像转换的概念，早期的方法以条件生成神经网络为主。在Vision Transformers(ViTs)得到普及后，使用自回归方法也获得了不错的结果。目前最强大的图像到图像转换方法里，Taming Transformer属于vision transformer类，具有生成图像和执行图像到图像转换的功能。Palette是一个统一的基于扩散的图像到图像转换框架。PITI是一种基于扩散的图像到图像转换方法，它利用大规模的预训练来提高生成结果的质量。在草图引导扩散等特定领域，像论文《Sketch-guided text-to-image diffusion models》则属于基于优化的方法，用于控制扩散过程。

 ## **方法**



- ControlNet通过对神经网络模块的**输入条件**进行操作，从而进一步控制整个神经网络的整体行为。其中，“神经网络模块”是指将一组神经层作为一个常用单元组合在一起构建神经网络，如“resnet”块、“convn-bn-relu”块、多头注意力块、transformer模块等。
- 以二维特征为例，给定特征x∈h×w×c，{h, w, c}为高度、宽度和通道，神经网络模块F(·;Θ)和一组参数Θ将x转换为另一个特征y：

![img](https://pic4.zhimg.com/80/v2-af0c4947e5c719e276b531fdc6ad31b3_720w.webp)

![img](https://pic3.zhimg.com/80/v2-30ed6992569b7199ebc660616810cf4e_720w.webp)

- 如果将所有参数锁定在Θ中，然后将其**克隆**为**可训练的副本Θc**。复制的Θc使用外部条件向量c进行训练。在本文中，称原始参数和新参数为“锁定副本”和“可训练副本”。制作这样的副本而不是直接训练原始权重的动机是：避免数据集较小时的过拟合，并**保持**从数十亿张图像中学习到的**大型模型的能力**。
- 神经网络模块由一种称为“**零卷积**”的独特类型的卷积层连接，即1×1卷积层，权重和偏差都用零初始化。将零卷积运算表示为**Z(·;·)**，使用参数{Θz1，Θz2}的两个实例组成ControlNet结构：

![img](https://pic2.zhimg.com/80/v2-4234c70e7e1d498c9f11054e513485e5_720w.webp)

**Θc**:可训练的副本 //  **c**:外部条件向量  //  **Z(·;·)** :零卷积运算  //  **F(·;Θ)** : 神经网络模块（一组参数Θ将x转换为另一个特征y）  

//  **yc**:该神经网络模块的输出

![img](https://pic2.zhimg.com/80/v2-53b373197b14b7f95918268ba6d7ddc5_720w.webp)

- 其中yc成为该神经网络模块的输出。因为零卷积层的权值和偏差都初始化为零，所以在**第一个训练步骤**中，有：

![img](https://pic2.zhimg.com/80/v2-f3744c29c8e2b7188319398992d4c3b1_720w.webp)

- 这可以转换为**yc = y**（m相当于右边那个ControlNet没用了）
- 表明，在第一个训练步骤中，神经网络块的可训练副本和锁定副本的所有输入和输出都与它们的状态一致，就像ControlNet不存在一样。换句话说，当一个ControlNet应用于一些神经网络块时，在进行任何优化之前，它不会对深层神经特征造成任何影响。任何神经网络块的能力、功能和结果质量都得到了完美的保留，任何进一步的优化都将变得像微调一样快(与从零开始训练这些层相比)。
- 下面简单地推导零卷积层的梯度计算。考虑权值W和偏差B的1 × 1卷积层，在任意空间位置p和通道索引i处，给定输入特征i∈h×w×c，正向通过可写成 （m Z（I；{W,B}相当于刚才的）Z（：Θ）吧 就是它的参数）

![img](https://pic2.zhimg.com/80/v2-2bf347e7a5065e43235b9d7def53351d_720w.webp)

- 零卷积有W = 0和B = 0(在优化之前)，对于Ip,i非零的任何地方，梯度变为：

![img](https://pic1.zhimg.com/80/v2-4a539ceef0f9ec3e955c80b2d713a78c_720w.webp)

- 可以看到，尽管**零卷积**可以**导致特征项i的梯度变为零**，但**权值和偏差的梯度不受影响**。在第一次梯度下降迭代中，只要特征I是非零，权重W就会被优化为非零矩阵。值得注意的是，在例子中，**特征项I**是从数据集中采样的输入数据或**条件向量**，这自然地确保了I不为零。例如，考虑一个具有总体损失函数L和学习率βlr的经典梯度下降，如果“外部”梯度∂L/∂Z(I;{W, B})不为零，有：

![img](https://pic4.zhimg.com/80/v2-7dc4e9d603311aee2749c705d3049bdf_720w.webp)

- 其中W∗是一阶梯度下降后的权值;是Hadamard乘积（逐元素相乘）。在这一步之后，可得到：

![img](https://pic4.zhimg.com/80/v2-d998cfae107c6cf1419178cd08d42813_720w.webp)

- 获得非零梯度，神经网络开始学习。通过这种方式，零卷积成为一种独特的连接层类型，以学习的方式逐步从零增长到优化参数。



## **扩散模型中的ControlNet**

(https://juejin.cn/post/7210369671656505399)

- 以Stable Diffusion为例，介绍利用ControlNet对具有任务特定条件的大型扩散模型进行控制的方法。
- **Stable Diffusion**是一个大型的文本到图像扩散模型，训练了数十亿张图像。该模型本质上是一个带有编码器、中间块和跳接解码器的**U-net**。编码器和解码器都有12个块，完整模型有25个块(包括中间块)。其中8个块是下采样或上采样卷积层，17个块是主块，**每个主块包含4个resnet层和2个Vision transformer (vit)**。每个Vit都包含若干交叉注意和/或自注意机制。文本采用OpenAI CLIP编码，扩散时间步长采用位置编码。



##### 预处理步骤

- Stable Diffusion使用类似于VQ-GAN的预处理方法，将整个512 × 512图像数据集转换为较小的64 × 64“潜在图像”进行训练。这需要ControlNets将基于图像的条件转换为64 × 64的特征空间，以匹配卷积大小。使用一个由4个4核和2 × 2步长卷积层组成的微型网络E(·)(由ReLU激活，通道为16,32,64,128，初始化为高斯权值，与完整模型联合训练)将图像空间条件ci编码为特征映射：

![img](https://pic3.zhimg.com/80/v2-644c568e31ae2174e312adba0c939b22_720w.webp)

- 其中cf为转换后的特征图。该网络将512 × 512的图像条件转换为64 × 64的特征图。如图所示，使用ControlNet来控制U-net的各个层。

- m添加了一个小网络E将图像空间条件转化为特征图条件。512 × 512->64 × 64

  **或者我们可以把他的图改吧改吧**，画成这样：![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c435098e512243279f6cb22520c16e16~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp?)

##### 网络

![img](https://pic2.zhimg.com/80/v2-b9a897817a2d04200fefa1fb8e2ec2b1_720w.webp)

- ControlNet的方式在计算上是高效的:由于原始权重是锁定的，因此训练不需要在原始编码器上进行梯度计算。这样可以加快训练速度，节省GPU内存，因为可以避免原来模型一半的梯度计算。
- 使用ControlNet训练一个扩散模型只需要在每次训练迭代中增加约23%的GPU内存和34%的时间(在单个Nvidia A100 PCIE 40G上测试)。具体来说，使用ControlNet创建了Stable Diffusion的12个编码块和1个中间块的可训练副本。12个块有4种分辨率(64 × 64，32 × 32，16 × 16，8 × 8)，每种3个块。输出被添加到U-net的12个跳过连接和1个中间块。SD是一个典型的U-net结构，这种ControlNet结构也可用于其他扩散模型。 
- m总的来说：将Encoder复制训练，decoder部分进行skip connection。

『hello』

## **训练**

(https://juejin.cn/post/7210369671656505399)



训练的目标函数为：
$$
\left.\mathcal{L}=\mathbb{E}_{\boldsymbol{z}_0, t, \boldsymbol{c}_t, \boldsymbol{c}_{\mathrm{r}}, \epsilon \sim \mathcal{N}(0,1)}\left[\| \epsilon-\epsilon_\theta\left(z_t, t, \boldsymbol{c}_t, \boldsymbol{c}_{\mathrm{f}}\right)\right) \|_2^2\right]
$$


使用的就是人家Stable Diffusion原始的目标函数改了改。『』

先看一下原始的Stable Diffusion的目标函数：
$$
L_{L D M}:=\mathbb{E}_{\mathcal{E}(x), \epsilon \sim \mathcal{N}(0,1), t}\left[\left\|\epsilon-\epsilon_\theta\left(z_t, t\right)\right\|_2^2\right]
$$
将采样$z_t$使用网络$\epsilon_\theta$去噪之后和原图经过网络$\epsilon$获得的潜变量计算$L_2$loss，看其重建的效果。

图像扩散模型学习逐步去噪来生成样本。去噪可以发生在像素空间或从训练数据编码的“潜在”空间。Stable Diffusion算法使用潜在空间作为训练域。

给定一个图像z0，扩散算法逐步向图像中添加噪声，并产生一个噪声图像zt，其中t是噪声添加的次数。当t足够大时，图像近似于纯噪声。给定一组条件，包括时间步长t，图像扩散算法学习一个网络θ来预测噪声加入到噪声图像zt中





那再回到
$$
\left.\mathcal{L}=\mathbb{E}_{\boldsymbol{z}_0, t, \boldsymbol{c}_t, \boldsymbol{c}_{\mathrm{r}}, \epsilon \sim \mathcal{N}(0,1)}\left[\| \epsilon-\epsilon_\theta\left(z_t, t, \boldsymbol{c}_t, \boldsymbol{c}_{\mathrm{f}}\right)\right) \|_2^2\right]
$$
将原始图像经过$\epsilon$之后获得潜变量，和经过网络$\epsilon_\theta$重建之后的图算$L_2$loss。原来Stable Diffusion中解码器要处理的是采样$z_t$和时间步长$t$，在这里加了两个控制条件：

- 文字prompt $c_t$
- 任务相关的prompt $c_f$

训练过程中将50 %的文本提示$c_t$随机替换为空字符串。这样有利于ControlNet网络从控制条件中识别语义内容。这样做的目的是，当Stable Diffusion没有prompt的时候，编码器能从输入的控制条件中获得更多的语义来代替prompt。（这也就是classifier-free guidance。）



##### 改进训练

- 接下来讨论几种改进ControlNet训练的策略，比如计算设备非常有限(例如，在笔记本电脑上）时。
- 小规模训练。当计算设备有限时，切断部分ControlNet和Stable Diffusion之间的连接可以加速收敛。默认情况下，将ControlNet连接到“SD中间块”和“SD解码器块1,2,3,4”，如图3所示。断开与解码器1,2,3,4的链接，**只连接中间块**，可以将训练速度提高约1.6倍(在RTX 3070TI笔记本GPU上测试)。当模型显示出结果与条件之间的**合理关联时**，可以在继续训练中将断开的环节**重新连接**起来，以便进行准确的控制。
- 大规模训练。拥有强大的计算集群(至少8个Nvidia A100 80G或同等规模)和大型数据集(至少100万张训练图像对)时，和数据容易获得的任务下，例如Canny检测到的边缘映射。在这种情况下，由于过拟合的风险相对较低，可以**先训练ControlNets**进行足够大的迭代次数(通常超过50k步)，然后解锁Stable Diffusion的所有权重，共同训练整个模型。



## **实验**

设置中，采样器为DDIM。默认使用20个步骤，三种类型的prompt来测试模型:

(1)No prompt:使用空字符串“”作为prompt。

(2)Default prompt:由于Stable diffusion本质上是用prompt训练的，空字符串可能是模型的一个意外输入，如果没有提供prompt，SD倾向于生成随机纹理。更好的设置是使用无意义的prompt，如“一张图片”、“一张漂亮的图片”、“一张专业的图片”等。在设置中，使用“专业、详细、高质量的图像”作为默认prompt。

(3)Automatic prompt:为了测试全自动流程最好的效果，还使用自动图像caption方法(如BLIP)。使用“Default prompt”模式获得的结果生成prompt，再次使用生成的prompt进行扩散生成。

(4)User prompt:用户给出prompt。



## **Related Work**

链接：https://www.zhihu.com/question/614056414/answer/3273259612



### **2.2. 图像扩散Image Diffusion**

​	**图像扩散模型**最早由Sohl- Dickstein等人[80]引入，最近被应用于图像生成[17, 42]。[潜在扩散模型](https://www.zhihu.com/search?q=潜在扩散模型&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3273259612})（LDM）[71]在潜在图像空间[19]中执行扩散步骤，这降低了计算成本。文本到图像扩散模型通过预先训练的[语言模型](https://www.zhihu.com/search?q=语言模型&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3273259612})（如CLIP [65]）将文本输入编码为[潜在向量](https://www.zhihu.com/search?q=潜在向量&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3273259612})，从而实现了最先进的图像生成结果。Glide [57]是一个支持图像生成和编辑的文本[引导扩散模型](https://www.zhihu.com/search?q=引导扩散模型&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3273259612})。Disco Diffusion [5]在[clip](https://www.zhihu.com/search?q=clip&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3273259612})引导下处理文本提示。Stable Diffusion [81]是潜在扩散[71]的大规模实现。Imagen [77]使用金字塔结构直接扩散像素，而不使用潜在图像。商业产品包括DALL-E2[61]和Midjourney[54]。

​	**Image Diffusion Models** were first introduced by Sohl-Dickstein et al. [80] and have been recently applied to image generation [17, 42]. The **Latent Diffusion Models (LDM)** [71] perform the diffusion steps in the latent image space [19], which reduces the computation cost. **Text-to-image diffusion models** achieve state-of-the-art image generation results by encoding text inputs into latent vectors via pretrained language models like CLIP [65]. **Glide** [57] is a text-guided diffusion model supporting image generation and editing. **Disco Diffusion** [5] processes text prompts with CLIP guidance. **Stable Diffusion** [81] is a large-scale implementation of latent diffusion [71]. **Imagen** [77] directly diffuses pixels using a pyramid structure without using latent images. Commercial products include **DALL-E2** [61] and **Midjourney** [54].



my：

**Image Diffusion Models**

**Diffusion Models**







###### 优化 或者基于此的工作

https://cloud.tencent.com/developer/article/2328560



gControlNet



[SD controlNet work?](https://stats.stackexchange.com/questions/627767/how-does-the-qr-code-monster-model-for-sd-controlnet-work)

Extending Text2Video-Zero for Multi-ControlNet







![image-20231102204046445](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20231102204046445.png)

其他

t2i

近年来，扩散模型[12]在图像合成领域取得了巨大成功。它旨在通过迭代去噪过程从高斯噪声中生成图像。其实现建立在严格的物理原理基础上[38, 39]，包括扩散过程和逆过程。在扩散过程中，图像X0通过T次迭代添加随机高斯噪声转换为高斯分布XT。逆过程则是通过多个去噪步骤从XT中恢复X0。

近年来，许多扩散方法集中在文本到图像（T2I）生成任务上。例如，Glide [23]提出将文本特征融入去噪过程中的变换器块。随后，DALL-E [30]、Cogview [6]、Make-a-scene [10]、Stable Diffusion [32]和Imagen [34]显著提高了T2I生成性能。广泛采用的策略是在特征空间进行去噪，并通过交叉关注模型将文本条件引入去噪过程。尽管它们取得了令人满意的合成质量，但仅靠文本提示无法提供可靠的结构指导。

PITI [43]提出通过缩小其他类型条件的特征与文本条件之间的距离来提供结构指导。[42]提出利用目标草图和中间结果之间的相似度梯度来约束最终结果的结构。还有一些方法[11, 9, 1]旨在调制预训练的T2I模型中的交叉关注图，以指导生成过程。这种方法的一个优点是它们无需单独训练，但在复杂场景中仍然不太实用。作为并发工作，[45]学习了专门的控制网络以实现预训练T2I模型的条件生成。[14]提出基于一组控制因素重新训练扩散模型。





zhihu 

最近，扩散模型[12]在图像生成领域取得了巨大成功。图像生成领域最常见生成模型有GAN和VAE，2020年，DDPM（Denoising Diffusion Probabilistic Model）被提出，被称为扩散模型（Diffusion Model），同样可用于图像生成。和其他生成模型一样，实现从噪声（采样自简单的分布）生成目标数据样本。扩散模型包括两个过程：前向过程（forward process）和反向过程（reverse process），其中前向过程又称为扩散过程（diffusion process），图像X0通过T次迭代添加随机高斯噪声转换为高斯分布XT。其中反向过程可用于生成数据样本，是通过多个去噪步骤从XT中恢复X0。

**OK1:**

​	Recently, diffusion models [1] have achieved tremendous success in the field of image generation. The most common models for image generation are GAN and VAE. In 2020, DDPM (Denoising Diffusion Probabilistic Model) was introduced, referred to as the diffusion model, and it can also be used for image generation. Like other generative models, it aims to generate target data samples from noise (sampled from a simple distribution).

​	The diffusion model comprises two processes: the forward process and the reverse process. The forward process, also known as the diffusion process, transforms the image X0 into a Gaussian distribution XT through T iterations by adding random Gaussian noise. The reverse process can be used to generate data samples by recovering X0 from XT through multiple denoising steps.





优化：

​	Recently, diffusion models [1] have achieved significant success in the field of image generation. The most common models for image generation are GAN and VAE. In 2020, DDPM (Denoising Diffusion Probabilistic Model) was introduced, known as the diffusion model, and it can be used for image generation as well. Like other generative models, its goal is to generate target data samples from noise, which is sampled from a simple distribution.

​	The diffusion model consists of two processes: the forward process and the reverse process. The forward process, also referred to as the diffusion process, transforms the initial image X0 into a Gaussian distribution XT through T iterations by adding random Gaussian noise. The reverse process can be employed to generate data samples by recovering X0 from XT through multiple denoising steps

[1]Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in Neural Information Processing Systems, 33:6840–6851, 2020. 3





ddim:

回到2020年的十月，斯坦福大学的研究人员Jiaming Song提出了**DDIM**（Diffusion Denoising Implicit Model），在提升了DDPM采样效率的基础上，仅用50步就能达到1000步采样的效果。DDIM不仅实现了高效率的采样方法，其作为确定性的采样方法还为后续的研究开创了一种类似于**GAN Invesion**的方法，用于实现各种真实图像的编辑与生成。

继之而来的，是2021年五月OpenAI所发布的**“Classifier Guidance”**（亦被称为Guided Diffusion）。这篇论文提出了一项重要的策略，即通过基于分类器的引导来指导扩散模型生成图像。借助其他多项改进，扩散模型首次成功击败了生成领域的巨头“GAN”，同时也为OpenAI的**DALLE-2**（一个图像和文本生成模型）的发布奠定了基础。

2022年的四月，来自OpenAI的**DALLE-2**横空出世，通过利用扩散模型以及海量数据，DALLE-2呈现出了前所未有的理解和创造能力。

Stable Diffusion release,其工作更为强大的3D生成等领域，将图像生成再度推进，使其更加贴近人类需求。



在2020年10月，斯坦福大学的研究员宋佳明介绍了DDIM（Diffusion Denoising Implicit Model）。在DDPM的效率改进基础上，DDIM仅需50步就实现了1000步采样的效果。DDIM不仅实现了高效采样，还开创了一种类似GAN逆向的确定性采样方法，用于图像编辑和生成。

随后，在2021年5月，OpenAI发布了“分类器引导”（也称为Guided Diffusion）。这篇论文介绍了一种关键策略，即通过基于分类器的引导来指导扩散模型生成图像。结合各种其他增强措施，扩散模型成功超越了生成领域的巨头，特别是“GAN”。此外，这项工作为OpenAI随后发布的DALL-E 2奠定了基础，这是一种强大的图像和文本生成模型。

在2022年4月，OpenAI推出了DALL-E 2，利用扩散模型和大规模数据展示了前所未有的理解和创造能力。

2022年发布的“Stable Diffusion”进一步推动了图像生成，尤其是在3D生成等领域，使其更符合人类需求。

In October 2020, Jiaming Song, a researcher at Stanford University, introduced the **DDIM** (Diffusion Denoising Implicit Model). Building on the efficiency improvements of DDPM, DDIM achieved the effect of 1000-step sampling in just 50 steps. DDIM not only enabled efficient sampling but also pioneered a deterministic sampling method, reminiscent of **GAN Inversion**, for image editing and generation.

Following this, in May 2021, OpenAI released **"Classifier Guidance"** (also known as Guided Diffusion). This paper introduced a crucial strategy of guiding diffusion models to generate images using classifier-based guidance. Coupled with various other enhancements, diffusion models successfully surpassed the giants in the generative field, notably "GAN." 

In April 2022, OpenAI unveiled **DALL-E 2**, which leveraged diffusion models and massive data to exhibit unprecedented levels of understanding and creative capabilities.

The release of Stable Diffusion in 2022 further propelled image generation, , making it more aligned with human needs.



优化去掉日期：

Jiaming Song, a researcher at Stanford University, introduced the **DDIM** (Diffusion Denoising Implicit Model). Building on the efficiency improvements of DDPM, DDIM achieved the effect of 1000-step sampling in just 50 steps. DDIM not only enabled efficient sampling but also pioneered a deterministic sampling method, reminiscent of **GAN Inversion**, for image editing and generation.

Following this, OpenAI released **"Classifier Guidance"** (also known as Guided Diffusion). This paper introduced a crucial strategy of guiding diffusion models to generate images using classifier-based guidance. Coupled with various other enhancements, diffusion models successfully surpassed the giants in the generative field, notably "GAN."

In April 2022, OpenAI unveiled **DALL-E 2**, which leveraged diffusion models and massive data to exhibit unprecedented levels of understanding and creative capabilities.

The release of Stable Diffusion in 2022 further propelled image generation, making it more aligned with human needs.



优化去掉加粗：

​	Jiaming Song, a researcher at Stanford University, introduced the DDIM (Diffusion Denoising Implicit Model). Building on the efficiency improvements of DDPM, DDIM achieved the effect of 1000-step sampling in just 50 steps. DDIM not only enabled efficient sampling but also pioneered a deterministic sampling method, reminiscent of GAN Inversion, for image editing and generation.

​	Following this, OpenAI released "Classifier Guidance" (also known as Guided Diffusion). This paper introduced a crucial strategy of guiding diffusion models to generate images using classifier-based guidance. Coupled with various other enhancements, diffusion models successfully surpassed the giants in the generative field, notably "GAN."

​	In April 2022, OpenAI unveiled DALL-E 2, which leveraged diffusion models and massive data to exhibit unprecedented levels of understanding and creative capabilities.

​	The release of Stable Diffusion in 2022 further propelled image generation, making it more aligned with human needs.





总的

Diffusion Models

​	Recently, diffusion models [1] have achieved tremendous success in the field of image generation. The most common models for image generation are GAN and VAE. In 2020, DDPM (Denoising Diffusion Probabilistic Model) was introduced, referred to as the diffusion model, and it can also be used for image generation. Like other generative models, it aims to generate target data samples from noise (sampled from a simple distribution).

​	The diffusion model comprises two processes: the forward process and the reverse process. The forward process, also known as the diffusion process, transforms the image X0 into a Gaussian distribution XT through T iterations by adding random Gaussian noise. The reverse process can be used to generate data samples by recovering X0 from XT through multiple denoising steps.

​	Jiaming Song, a researcher at Stanford University, introduced the DDIM (Diffusion Denoising Implicit Model)[2]. Building on the efficiency improvements of DDPM, DDIM achieved the effect of 1000-step sampling in just 50 steps. DDIM not only enabled efficient sampling but also pioneered a deterministic sampling method, reminiscent of GAN Inversion, for image editing and generation.

​	Following this, OpenAI released "Classifier Guidance" (also known as Guided Diffusion)[3]. This paper introduced a crucial strategy of guiding diffusion models to generate images using classifier-based guidance. Coupled with various other enhancements, diffusion models successfully surpassed the giants in the generative field, notably "GAN."

​	In April 2022, OpenAI unveiled DALL-E 2, which leveraged diffusion models and massive data to exhibit unprecedented levels of understanding and creative capabilities.

​	The release of Stable Diffusion in 2022 further propelled image generation, making it more aligned with human needs[4].



[1]Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in Neural Information Processing Systems, 33:6840–6851, 2020. 3

[2]Song J, Meng C, Ermon S. Denoising diffusion implicit models[J]. arXiv preprint arXiv:2010.02502, 2020.

[3]Ho J, Salimans T. Classifier-free diffusion guidance[J]. arXiv preprint arXiv:2207.12598, 2022.

[4]Rombach R, Blattmann A, Lorenz D, et al. High-resolution image synthesis with latent diffusion models[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2022: 10684-10695.





## Plan

https://zhuanlan.zhihu.com/p/617017935







受ControlNet启发，我们提出CC_ControlNet.

我们计划实现CC_ControlNet，在文生图的基础加入额外的编辑方案，控制扩散模型，使其生成更接近用户需求。我们的主要目的是实现动漫角色或卡通角色等风格化角色的自定义换装。我们将分为几个阶段来实现，第一阶段，输入动漫角色图片、及角色图片及对需要替换的衣服进行手动涂抹做mask操作后的图片，以及一段对新衣装的描述，实现涂抹部分根据文本信息进行生成。第二阶段，可以给定特定服装，对特定角色进行换装，并自动检测服装位置，无需手动提供mask后的图片。、

​	Based on ControlNet inspiration, we propose CC_ControlNet.We plan to implement CC_ControlNet, incorporating additional editing schemes on the basis of document-based graph, controlling the diffusion model to generate outputs more closely aligned with user requirements. Our primary objective is to achieve custom outfitting for stylized characters such as anime or cartoon characters. We'll execute this in several stages. In the first phase, we'll input anime character images, images of the characters with manually edited mask operations for the clothes to be replaced, and a textual description of the new attire. This stage aims to generate the edited portions based on the provided textual information. In the second phase, specific attire will be applied to designated characters, automatically detecting clothing positions without the need for manually provided masked images.



我们计划实现CC_ControlNet，在文生图的基础加入额外的编辑方案，控制扩散模型，使其生成更接近用户需求。我们的主要目的是实现动漫角色或卡通角色等风格化角色的自定义换装。我们将分为几个阶段来实现，第一阶段，输入动漫角色图片、及角色图片及对需要替换的衣服进行手动涂抹做mask操作后的图片，以及一段对新衣装的描述，实现涂抹部分根据文本信息进行生成。第二阶段，可以给定特定服装，对特定角色进行换装，并自动检测服装位置，无需手动提供mask后的图片。、



OK1:

​	Drawing inspiration from ControlNet, we introduce CC_ControlNet.Our plan involves implementing CC_ControlNet, which incorporates additional editing schemes based on text-to-image generation. This will allow us to control the diffusion model, generating outputs that closely align with user requirements. Our primary goal is to achieve customized outfitting for stylized characters, such as anime or cartoon characters. We will carry out this project in multiple stages. In the initial phase, we will input anime character images, along with images of characters that have undergone manual mask operations for the clothes to be replaced. Additionally, we will provide a textual description of the new attire. The objective of this stage is to generate the edited portions based on the provided textual information. In the second phase, specific attire will be automatically applied to the characters, with clothing positions detected automatically, eliminating the need for manually provided masked images。

​	

以Stable Diffusion为例，我们介绍在角色换装这个特定任务条件下，利用CC_ControlNet对大型扩散模型进行控制的方法。我们将使用 CC_ControlNet来控制Stable Diffusion的U-net的各个层。CC_ControlNet将通过操作神经网络的输入条件来控制神经网络的行为。我们将各个encoder层进行拷贝，而decoder部分进行skip connection。通过迭代的过程，**重复应用ControlNet操作来优化神经网络块**。

Using Stable Diffusion as an example, we introduce the method of controlling large-scale diffusion models with CC_ControlNet for the specific task of character outfit swapping. We will employ CC_ControlNet to regulate the various layers of the U-net in Stable Diffusion. CC_ControlNet will manipulate the behavior of the neural network by operating on its input conditions. We will duplicate each encoder layer and establish skip connections within the decoder section. Through an iterative process, we will repeatedly apply ControlNet operations to optimize the neural network blocks.





总的：

​	Drawing inspiration from ControlNet, we introduce CC_ControlNet.Our plan involves implementing CC_ControlNet, which incorporates additional editing schemes based on text-to-image generation. This will allow us to control the diffusion model, generating outputs that closely align with user requirements. Our primary goal is to achieve customized outfitting for stylized characters, such as anime or cartoon characters. We will carry out this project in multiple stages. In the initial phase, we will input anime character images, along with images of characters that have undergone manual mask operations for the clothes to be replaced. Additionally, we will provide a textual description of the new attire. The objective of this stage is to generate the edited portions based on the provided textual information. In the second phase, specific attire will be automatically applied to the characters, with clothing positions detected automatically, eliminating the need for manually provided masked images。

​	Using Stable Diffusion as an example, we introduce the method of controlling large-scale diffusion models with CC_ControlNet for the specific task of character customization. We will employ CC_ControlNet to regulate the various layers of the U-net in Stable Diffusion. CC_ControlNet will manipulate the behavior of the neural network by operating on its input conditions. We will duplicate each encoder layer.In the decoder section, skip connections are established. Through an iterative process, we will repeatedly apply CC_ControlNet operations to optimize the neural network blocks.



Character Customization With Stable Diffusion
