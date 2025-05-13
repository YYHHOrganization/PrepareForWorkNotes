# Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models

论文:

https://zju3dv.github.io/hghoi/files/paper.pdf

主页：

https://zju3dv.github.io/hghoi/index.html

ICCV 2023



本文提出了一种新颖的方法，用于生成与目标物体交互的人类的三维运动，重点解决合成**长距离和多样化运动**的挑战，而现有的自回归模型或基于路径规划的方法无法满足这一需求。我们提出了一个**分层生成框架**来解决这个挑战。具体来说，我们的框架首先生成一组**里程碑**，然后沿着这些里程碑合成运动。因此，长距离运动生成可以简化为合成多个由里程碑引导的短运动序列。在对 NSM、COUCH 和 SAMP 数据集的实验表明，我们的方法在质量和多样性上都大幅超越了之前的方法。

![image-20240905162814123](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905162814123.png)

我们的流程包括三个组件：首先，根据给定的物体合成目标姿态。然后，基于目标姿态预测一系列具有局部姿态的里程碑(就是关键帧吧)。最后，在这些里程碑之间填充轨迹和完整的运动序列。



**摘要**

本文提出了一种生成与目标物体交互的人类3D运动的新方法，重点解决合成**长距离和多样化**动作的挑战，这是现有自回归模型或基于路径规划的方法无法实现的。我们提出了一个**分层生成**框架来解决这个挑战。具体来说，我们的框架首先生成一组里程碑，然后沿着这些里程碑合成运动。因此，**长距离运动生成可以简化为合成若干个由里程碑引导的短动作序列**。在NSM、COUCH和SAMP数据集上的实验表明，我们的方法在质量和多样性上都大幅超越了之前的方法。源代码可在我们的项目页面 https://zju3dv.github.io/hghoi 获取。

**1. 引言**

场景感知运动生成旨在根据3D场景模型合成3D人类运动，使虚拟人类能够自然地在场景中游走并与物体互动，这在增强现实/虚拟现实（AR/VR）、电影制作和视频游戏等多种应用中具有广泛的应用前景。

与传统的人物控制运动生成方法不同，后者的目标是在用户控制信号的指导下即时生成短小或重复的动作，我们关注的是在给定人类起始位置和目标物体模型的情况下生成长期人-物交互的设置。这一设置带来了新的挑战。首先，整个接近过程和人-物交互应保持一致性，这要求能够建模人类与物体之间的长距离交互。其次，在内容生成的背景下，生成模型应该能够合成多样化的动作，因为真实人类接近和与目标物体互动的方式是多种多样的。



现有的运动合成方法大致可以分为在线生成和离线生成。

大多数**在线方法**专注于角色的**实时控制**。在给定目标物体的情况下，它们通常使用**自回归模型通过反复提供预测**来生成未来的动作。尽管它们在视频**游戏**等交互场景中得到了广泛应用，但其运动质量对长期生成来说并不令人满意。一个可能的原因是自回归过程中的误差累积，先前预测中的误差反馈作为模型输入，如[40, 26, 45, 46, 22]所讨论的那样。

为了提高运动质量，一些最近的离线方法采用了多阶段框架，首先生成轨迹，然后合成动作。TDNS通过结合cVAE模型和确定性规划方法**（如A*）来生成路径**。尽管这种策略可以产生合理的路径，但路径的多样性有限，这在我们第4.4节的实验结果中有所证明。



在本文中，我们提出了一种新颖的**离线方法**，用于合成长时间和多样化的人-物交互。我们的创新在于一种**分层生成策略**，首先预测一组里程碑，然后在这些里程碑之间生成人体运动。图1说明了基本思路。具体而言，给定**起始位置**和**目标物体**，我们设计了一个里程碑生成模块，以沿运动轨迹合成一组里程碑，每个里程碑编码局部姿势，并指示人类运动过程中的过渡点。基于这些里程碑，我们采用**运动生成模块**来生成**完整的运动序列**。得益于里程碑，我们将长序列生成简化为合成几个短运动序列。此外，每个里程碑处的局部姿势由考虑全局依赖性的Transformer生成，从而产生时间上连贯的结果，进一步促进了动作的一致性。





![image-20240905164313477](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905164313477.png)

**图1. 人-物交互的生成**
 给定一个物体，我们的方法首先预测一组里程碑，其中圆环表示位置，穿着粉色衣服的人类代表局部姿势。然后，在这些里程碑之间填充动作。该图展示了我们的方法能够为同一个物体生成多样化的里程碑和动作。时间的流动通过颜色编码展示，深蓝色表示后续的帧。





除了我们的分层生成框架外，我们还利用**扩散模型合成人-物交互**。之前的运动合成扩散模型组合了Transformer和去噪扩散概率模型（DDPM）。直接将它们应用于我们的设置计算负担极重，由于长运动序列，可能导致GPU内存爆炸。因为我们的分层生成框架将长期生成**转换为几个短序列的合成**，所以所需的GPU内存降低到与短期运动生成相同的水平。因此，我们可以有效地利用TransformerDDPM合成长时间运动序列，从而提高生成质量。

我们在NSM、COUCH和SAMP数据集上进行了广泛的实验，以验证我们的设计选择。在这些数据集上，我们的分层框架在运动质量和多样性上显著超越了之前的方法。



**2. 相关工作**

**2.1. 动作合成**

动作合成是计算机图形学和视觉领域一个长期存在的问题[68, 51, 42, 9]。随着深度学习的快速发展，最近的研究开始将神经网络应用于动作合成[14, 40, 26, 72]。一些方法是确定性的[28, 81, 44, 67]，而其他方法则试图通过变分自编码器（VAE）来预测随机动作[70, 1, 71, 79, 45]，以及生成对抗网络（GAN）[4, 34]。为了进一步提高性能，一些研究采用图卷积网络（GCN）[67, 10, 66, 35, 39]或Transformer[5]从人类骨骼中提取特征。为了解决人类动作的模糊性，一些研究[26, 55]提出使用相位信号来指导动作。

最近的研究开始考虑场景上下文[56, 6]。

NSM[56]是第一个旨在合成人类动作与具有特定动作标签的物体级交互的工作。

在NSM的基础上，**SAMP**[19]应用条件变分自编码器（**cVAE**）来预测多样化的动作。

这些工作[56, 19, 76]主要集中在与一两个物体的交互，而其他工作[6, 65]则将完整场景（包括地面和墙壁的信息）作为输入来生成动作。[6]通过首先预测轨迹然后基于场景的二维图像生成给定动作序列的未来动作。类似于这种流程，[65]应用了GAN[16]。此外，[64]提出了一个框架，首先在用户提供的路径上放置姿势，然后在全景扫描的三维场景中合成动作。[63]结合A*算法和cVAE生成多样化的人类动作。为了进一步控制人类动作，[80]采用了视线，而COUCH[76]明确建模手部接触以指导预测。一些方法[7, 21]还使物理模拟角色能够执行场景交互任务，包括坐下[7, 21]和搬运箱子[21]。还有一些工作关注抓取[58, 69]、操作[73]和与动态物体的交互[57]。

**我们的方法与其他方法的比较**。本工作遵循[56, 19]的设置，专注于物体级交互。与主要基于自回归模型生成动作的[56, 19]相比，我们设计了一个层次框架来合成动作。不同于[6, 64]，我们的工作专注于更长时间的生成（超过10秒），而[6]为2秒，[64]为6秒。我们的方式并不是像[63]那样通过额外的网络自回归规划路径来生成多样化的轨迹，而是直接预测一组里程碑，以描述固有多样化的接近过程。此外，大多数方法[19, 76, 64, 63]依赖于cVAE生成随机动作，而我们则**利用扩散概率模型（DDPM）[23]来合成轨迹和动作。**



**2.2. 扩散模型**

扩散模型[53]是一类基于似然的方法，通过逐渐去除信号中的噪声来生成样本。随后，[23, 54]开发了高质量图像生成的扩散模型。为了控制生成结果，[12]提出了分类器引导，以在多样性和保真度之间进行权衡。后来，无分类器模型[24]在文本条件图像生成方面取得了更好的效果[48]。此外，扩散模型已成功应用于其他领域，如视频生成[52, 25]和3D内容生成[47]。

有一些工作[74, 59, 31, 38]将DDPM应用于运动合成。[3, 8]也探索了潜在扩散模型[50]用于运动生成。然而，大多数工作专注于文本条件[74, 11]、音频驱动[82]和音乐驱动[60, 82]的动作生成，而我们的目标是人-物交互。在本研究中，我们将Transformer DDPM[23]应用于多阶段框架，该框架分别生成轨迹并合成动作。

还有一些同时进行的工作[27]将DDPM应用于场景中的动作合成。然而，[27]旨在短期动作生成（约2秒），而我们的目标是长期人类动作生成（超过10秒）。与现有工作[59, 27]不同，**我们**在多阶段框架中使用DDPM，其中**轨迹和动作是分别预测的**。

**3. 方法**

给定物体I和起始点s，我们的目标是合成人类与物体交互的3D人类动作$ \{(ri, θi)\}^N _{i=1}$。ri是根轨迹，θi表示第i帧的局部姿态。

我们设计了一个层次化的动作生成框架，如图2所示。首先，我们使用GoalNet[19]预测在物体上的交互目标。然后，我们生成目标姿态（第3.1节）以明确建模人-物体交互。接下来，我们的里程碑生成模块（第3.2节）估计里程碑的长度，从起始点到目标生成里程碑的轨迹，并放置里程碑姿态。因此，长距离动作生成被分解为短距离运动合成的组合。最后，我们设计了一个动作生成模块（第3.3节）来合成里程碑之间的轨迹并填充动作。

![image-20240905170017460](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905170017460.png)

Figure 2. Overview of our pipeline. Our pipeline consists of three components: First, the goal pose is synthesized given the object. Then, a number of milestones with local poses are predicted based on the goal pose. Finally, the trajectory and the full motion sequences are infilled between the milestones  





**3.1. 目标姿态生成**

我们称一个**人与物体交互并保持静止的姿态为目标姿态**。为了合成多样化的人类动作，我们首先生成一个与物体交互的目标姿态，遵循[58, 69, 63]。大多数方法[78, 75, 20]使用cVAE模型生成人体姿态，它们将姿态投影到连续空间中的标准正态分布[33]。经验上，我们发现cVAE模型在我们的设置中表现不佳。为了克服这一挑战，我们引入了**VQ-VAE**[61, 49]来建模数据分布，该模型利用离散表示在有限的一组点中聚类数据[37]。我们假设来自SAMP数据集[19]的目标姿态有限数据总是可以通过VQ-VAE进行聚类，但可能不足以学习VAE的连续潜在空间[41]。此外，基于不同人类姿势可能共享相似属性的观察[15, 29]（例如，人类可能以不同的手位坐下，但腿的位置相同），我们**将关节分成L（L = 5）个不同的不重叠组**，类似于MotionPuzzle[29]。

![image-20240905171022579](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905171022579.png)

图3. 部件VQ-VAE。部件VQ-VAE首先将骨架分成多个部分，并分别学习代码簿。不同部分的组合随后通过自回归预测模型进行建模。



**量化**。如图3所示，**目标姿态θg**被划分为独立的关节组，表示为$ θg = \{θgi\}^L _{i=1}$ 。然后，一个包含向量列表的离散代码簿Zi将编码器Ei输出的$z^i$与之进行比较，以找到在欧几里得距离上最接近的向量。与最小距离的L个向量将被连接并输入到共享解码器D中，以重建θg。损失函数定义为：

$ L(θg, D(z)) = ∥θg - D(z)∥^2_2 + \sum_{i=1}^{L} ∥sg[Ei(θgi)] - zi∥^2_2  $

​					       	$+β \sum_{i=1}^{L} ∥sg[zi] - Ei(θgi)∥^2_2,$

其中

$ z = [z1, ..., zL]$

$zi = \arg\min_{z'i \in Zi} ∥z'i - zˆi∥$

$zˆi = E(θgi)$

这里，符号sg[·]表示停止梯度操作符，而$∥sg[zi] - Ei(θgi)∥^2_2$是承诺损失[49]，其由权重因子β控制。

**生成**。在Ei和D可用的情况下，我们可以通过一系列基于部件的代码簿索引来表示$θg = {θg1, ..., θgL}$。更具体地，我们使用Ei从θgi中提取特征，并找到最接近的向量zi ∈ Zi。然后我们使用si ∈ {0, ..., |Zi| - 1}来指示zi在Zi中的索引。因此，θg可以用$s = {s1, ..., sL}$表示。

为了生成一个自然的目标姿态，我们将问题转换为预测一系列可以表示θg的索引。我们将推理过程构建为条件自回归过程，并利用变压器[62]来学习预测可能索引的分布[13]。条件包含目标周围的环境Og和动作ag。根据NSM [56]和COUCH [76]的方法，在目标周围创建一个预定义半径和高度的圆柱体积。在这个体积内，均匀采样球体并计算与这些球体对应的物体的占用情况。然后，这些占用情况被展平形成一个特征向量，记作Og。ag是一个指示动作类型的向量。这些变量作为标记输入到变压器中。我们的目标是学习序列的似然性：

$p(s | Og, ag) = \prod_{i} p(si | s<i, Og, ag).$

在预测了索引之后，我们将它们映射回其对应的代码簿条目，以获取量化特征z = [z1, ..., zL]，并将其输入解码器D以生成目标姿态θg。



**3.2. 里程碑生成**

基于起始姿态和目标姿态，我们可以生成里程碑轨迹，并合成里程碑处的局部姿态。遵循[74, 59]的方法，我们构建了一个 transformer  DDPM [23]，并将其应用于生成里程碑以提高质量。由于运动数据的长度未知且可以是任意的（例如，人类可能快速走向椅子然后坐下，或者在慢慢绕椅子走后再坐下），我们预测里程碑的长度，记作N。然后我们合成N个里程碑点，并在这些点上放置局部姿态。

**transformer  DDPM**。在这里，我们首先简要介绍DDPM [23]，它学习逆转扩散过程。形式上，扩散模型[53]被定义为以下形式的潜变量模型：

$p_\theta(x_0) := \int p_\theta(x_{0:T}) dx_{1:T},$

其中x0 ∼ q(x0)是数据，x1, . . . , xT是潜变量。$pθ(x0:T)$被公式化为马尔可夫链：

$p_\theta(x_{0:T}) := p(x_T) \prod_{t=1}^{T} p_\theta(x_{t-1} | x_t),$

$p_\theta(x_{t-1} | x_t) := N(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t)).$

扩散模型近似后验分布$q(x_{1:T} | x_0)$作为逐渐向数据添加方差调度βt的高斯噪声的马尔可夫链：

$q(x_{1:T} | x_0) := \prod_{t=1}^{T} q(x_t | x_{t-1}),$

$q(x_t | x_{t-1}) := N(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t I).$

与逐步在x0上添加噪声不同，DDPM将扩散过程公式化为：

$q(x_t | x_0) = N(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) I),$

其中αt = 1 - βt且$(\bar{\alpha}_t = \prod_{s=1}^{t} \alpha_s)$。因此，我们可以通过对噪声ϵ进行采样来生成xt作为训练数据。DDPM利用神经网络来建模$pθ(x_{t-1} | x_t)$，推理过程是逐渐去噪xt，从t = T到t = 1，其中xT ∼ N(0, I)。





![image-20240905174653403](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905174653403.png)



图4. 用于里程碑生成的变压器DDPM概述。该模型首先将长度标记$H^{tok}$和条件C作为输入，以预测数据长度。然后构建长度为N的噪声序列$x^{1:N}_T$。在扩散过程中，它在时间步t时接收C和序列$x^{1:N}_t$，以预测目标$ \hat{x}^{1:N}_0$。对于其他子模块，我们移除了长度预测头。



**3.3. 动作生成**

我们的方法不是逐帧预测动作[56, 19, 76]，而是基于生成的里程碑分层合成完整的序列。我们遵循[6, 64, 63]的方法，首先生成轨迹，然后合成动作。具体而言，在两个连续的里程碑之间，我们首先完成轨迹。然后，在连续的里程碑姿态的指导下填充动作。这两个步骤分别使用两个变压器DDPM（在第3.2节中描述）来完成。对于每一步，我们仔细设计DDPM的条件以生成目标输出。

**轨迹完成**。对于里程碑mi和mi+1之间的轨迹完成，我们假设它仅依赖于里程碑和物体。因此，我们将条件定义为：

$C_r = {I_i, I_{i+1}, O_i, O_{i+1}, m_i, m_{i+1}, t_{i}^{i+1}},$

其中Ii表示相对于里程碑i的物体表示，Oi表示围绕第i个里程碑的自我中心占用情况（与第3.1节中描述的占用特征形式相同），如NSM [56]和COUCH [76]所示。mi在公式(13)中已经展示。$t_i^{i+1}$表示(i + 1)-th里程碑在第i个里程碑坐标系中的位置和方向。在两个连续的里程碑之间，我们生成长度为2秒的轨迹，即61帧。类似的超参数可以在之前的方法中找到[64, 63]。

目标输出是在两个连续里程碑之间的轨迹。类似于里程碑点，我们使用双向方案合成第j帧的轨迹。轨迹由一组点组成，这些点具有与公式(13)中里程碑相同的表示。我们使用一个与第3.2节中类似的变压器DDPM $(f_r)$ 来生成轨迹。由于我们假设两个里程碑之间的轨迹长度是固定的，DDPM$ (f_r) $不包含长度预测头。

**动作填充**。为了合成长时间范围的动作，我们借助里程碑点和里程碑姿态将一个长序列转换为几个固定长度的短序列。对于连续里程碑姿态之间的子序列，我们的目标是生成轨迹上缺失的局部姿态。生成的动作必须满足轨迹，并自然地从一个里程碑过渡到下一个里程碑。像里程碑姿态生成一样，我们使用公式(15)中的逐帧条件的相同表示。条件定义为：

$C_p = {\theta_1, \theta_{61}, \gamma_1, ..., \gamma_{61}},$

其中θ1和θ61是两个连续里程碑的局部姿态。通过这些输入，我们使用另一个不带长度预测头的变压器DDPM (f_p) 生成平滑的动作。

**4. 实验**

**4.1. 实现细节**
 我们使用Adam优化器[32]训练部分VQ-VAE和变压器DDPM模型。所有模型的学习率固定为0.0001，批量大小为256。其余细节见补充材料。

**4.2. 数据集和评估指标**
 测试设置。我们的实验在SAMP [19]、COUCH [76]和NSM [56]数据集上进行。在提供一个起点、起始姿态、物体和终点的情况下，虚拟人被要求接近物体，与之互动，并离开以到达终点。消融研究是在SAMP数据集上进行的。

指标。根据以前的方法[19]，我们计算生成动作与真实动作之间的弗雷歇距离（FD）以衡量动作质量。我们还进行了用户研究，每个序列至少由3名用户评估，评分范围为1到5。此外，我们计算穿透比率[64, 75, 78]和脚滑动[72, 36]，以展示3D物体与合成动作之间的物理合理性。我们计算平均成对距离（APD）[71, 77]以评估多样性。具体而言，我们计算合成动作、角色在物体交互过程中的姿态以及轨迹的APD。根据之前的研究[56, 19]，我们计算PE（位置误差）和RE（旋转误差）以指示物体交互的精度。对于每个测试对象，我们生成多个序列。更多细节包含在补充材料中。

**4.3. 与其他方法的比较**
 **SAMP数据集上的结果**。在SAMP数据集[19]上，我们将我们的方法与在线方法SAMP [19]和MoE [72]进行比较。由于我们的方法是离线的，因此我们还将离线方法SLT [64]和TDNS [63]修改为适应我们的设置。对于SLT [64]，我们采用A∗ [18]来规划路径，并沿着路径选择点作为子目标，以形成SLT的输入。有关[64, 63]实现的更多细节见补充材料。由于MoE通常无法完成动作，因此我们不计算其穿透比率。如表1所示，我们的方法在较低的FD、更高的用户研究分数和更高的APD方面优于其他方法。此外，我们的方法在轨迹多样性方面显著高于SAMP [19]。尽管TNDS [63]提出了结合A∗ [18]和cVAE的神经映射器（NM），但生成轨迹的多样性仍不如我们的方法，正如APDT所示。



**COUCH数据集上的结果**
 由于我们的目标是合成多样化的动作，而不是控制角色，因此我们仅在COUCH数据集[76]上评估动作质量。表2显示，我们的方法超越了所有基准。我们的方法在APDT方面明显高于其他方法。我们观察到，TDNS [63]的APDT高于采用确定性A∗ [18]的方法[19, 64]，但远低于我们的方法。尽管COUCH [76]表现出比我们的方法更低的脚滑动，但有时会卡住，导致脚滑动较少，因为角色没有移动。

**NSM数据集上的结果**
 在NSM数据集[56]上，我们将我们的方法与SAMP [19]和NSM [56]进行了比较。表3显示，我们的方法优于基准。与确定性方法NSM相比，我们的方法能够生成随机运动和多样化的轨迹。

**拥挤场景中的结果**
 我们展示了在拥挤场景中生成的结果，如图5所示。我们的方法的穿透帧比例为3.8%，而SAMP为4.9%。更多细节见补充材料。

**定性结果**
 如图6所示，我们的方法在SAMP数据集上取得了比基线[19, 63]更好的结果。图7对比了我们的方法与COUCH和TDNS在COUCH数据集上的表现。更多定性结果见补充材料。

**4.4. 消融研究**
 **各子模块的影响**
 为了展示我们分层设计的有效性，我们评估了我们的方法与四个变体的性能，其中每个变体去除了一个子模块。表4表明，每个组件都提高了性能。生成完整轨迹会导致更丰富的轨迹，但动作质量较差且脚滑动较多。这验证了轨迹生成和动作生成分开的必要性。



**目标姿态生成**
 我们评估了我们的目标姿态生成器，并与几个变体进行比较，包括cVAE、DDPM和标准VQ-VAE。在此评估中，我们仅替换目标姿态生成模块，其余部分保持不变。表5显示，部件VQ-VAE生成的姿态比连续潜在空间模型更为多样化。与标准VQ-VAE的比较证明了我们设计的必要性。我们还尝试使用部件VQ-VAE进行运动填充，但表6中的结果显示其性能较差。

**里程碑生成**
 为了进一步研究里程碑的影响，我们将我们的方法与采用路径规划方法并沿路径选择点作为里程碑的变体进行了比较。对于此消融实验，我们实现了A∗和TDNS提出的NM [63]。如表7所示，A∗ [18]生成的轨迹多样性要差得多，动作质量显著下降，这从较低的APDT和较高的FD可以看出。NM [63]的轨迹多样性优于A∗，但仍然不及我们的方法。这些变体表现不佳的原因可能是轨迹多样性低，从而影响生成动作的分布以计算FD。

**运动填充**
 为了验证我们的运动填充模块，我们将其与ConvAE [30]和SLT [64]进行了比较。我们仅替换运动填充模块，其余部分保持不变。运动质量和多样性的比较如表8所示，我们的方法以更低的FD超越了ConvAE [30]和SLT [64]。

**DDPM与VAE的比较**
 为了展示DDPM的有效性，我们实现了一个cVAE变体，其中我们简单地用变压器cVAE [45, 63]替换了我们的变压器DDPM。如表9所示，尽管cVAE模型能够生成更多样化的轨迹，但其运动质量远未令人满意，FD值明显更高。

**与其他扩散模型的比较**
 我们的方法在MDM [59]和FLAME中的架构中脱颖而出。更多分析和消融研究的详细信息见补充材料。

**4.5. 限制**
 尽管我们的方法能够生成多样且自然的动作，但仍存在一些局限性。我们的方法是离线的，无法应用于交互场景。我们假设对象是静态的，因此无法处理移动对象。扩散模型需要较长的推理时间。在TITAN Xp GPU上，720帧序列的平均推理时间为7.13秒。慢速问题可能通过加速扩散模型的方法得到解决[43, 2]。

**5. 结论**
 在本工作中，我们提出了一种新颖的层次化流水线，用于人类与物体交互的运动合成。我们的方法首先生成目标姿态，然后预测一组里程碑。接下来，在里程碑的指导下合成动作。此外，我们在我们的层次化流水线中应用了DDPM。我们还表明，我们的框架能够生成比其他方法更为多样化和自然的人类与物体交互动作。

**致谢**
 我们感谢Jintao Lu、Zhi Cen、Zizhang Li和Kechun Xu的宝贵讨论。本研究部分得到了浙江实验室重点研究项目（编号：K2022PG1BB01）、国家自然科学基金（编号：62172364）以及浙江大学信息技术中心和计算机辅助设计与计算机图形学国家重点实验室的支持。



![image-20240905175157894](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905175157894.png)

cluttered   凌乱



继续翻译论文“Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models”地部分内容，请精确且清晰地翻译，只需要回答我中文翻译内容即可：“

Figure 3. Part VQ-VAE. Part VQ-VAE first splits the skeleton into multiple parts and learns the codebooks separately. The composition of different parts is subsequently modeled with the autoregressive prediction model.  





## 实验

修改:

把那个numpy==啥 改掉了

### python部分

![image-20240909135041503](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240909135041503.png)





### unity部分



###### interaction

![image-20240906165907434](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906165907434.png)

不合并也不优化

![image-20240906160611248](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906160611248.png)



合并不优化

<img src="D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906160650548.png" alt="image-20240906160650548" style="zoom:50%;" />

![image-20240906160459402](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906160459402.png)





合并且优化

<img src="D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906160707062.png" alt="image-20240906160707062" style="zoom:50%;" />

![image-20240906160509683](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906160509683.png)





初始会添加trigger的collider

![image-20240906162707375](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906162707375.png)

![image-20240906162642757](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906162642757.png)



挂了VoxelCollider 和Interaction

```C#
using System.Collections; // 引入系统集合命名空间
using System.Collections.Generic; // 引入系统集合的泛型功能
using UnityEngine; // 引入Unity引擎的基本功能

#if UNITY_EDITOR // 如果是在Unity编辑器模式下编译
using UnityEditor; // 引入Unity编辑器相关功能
#endif

[ExecuteInEditMode] // 允许在编辑模式下执行此脚本
[RequireComponent(typeof(VoxelCollider))] // 确保此游戏对象必须有一个 VoxelCollider 组件
public class Interaction : MonoBehaviour // 定义 Interaction 类，继承自 MonoBehaviour
{
    public VoxelCollider Geometry = null; // 声明一个 VoxelCollider 类型的变量，用于存储几何体信息

    public Transform[] Contacts = new Transform[0]; // 声明一个 Transform 数组，用于存储接触点

    public bool ShowContacts = false; // 布尔值，控制是否显示接触点

    [ContextMenu("Reorganize")] // 在上下文菜单中添加“Reorganize”选项
    public void Reorganize() // 定义重新组织接触点的方法
    {
        Transform container = transform.Find("Contacts"); // 查找当前物体下的名为“Contacts”的子物体
        if (container == null) // 如果没有找到
        {
            // 创建一个新的 GameObject 作为接触点容器并设置其父物体为当前物体
            container = new GameObject("Contacts").transform;
            container.SetParent(transform);
            container.localPosition = Vector3.zero; // 设置位置为零
            container.localRotation = Quaternion.identity; // 设置旋转为默认
            container.localScale = Vector3.one; // 设置缩放为1
        }
        foreach (Transform c in Contacts) // 遍历所有接触点
        {
            c.SetParent(container); // 将每个接触点的父物体设置为容器
        }
    }

    void Awake() // 当脚本实例被加载时调用
    {
        if (Application.isPlaying) // 如果正在运行游戏
        {
            Geometry = GetGeometry(); // 获取几何体
            BoxCollider trigger = gameObject.AddComponent<BoxCollider>(); // 添加一个 BoxCollider 作为触发器
            trigger.isTrigger = true; // 将其设置为触发器
            //trigger.size = 2f*Geometry.GetExtents(); // 注释掉的代码，用于设置触发器大小
            trigger.size = Geometry.GetExtents(); // 设置触发器的大小为几何体的扩展
            trigger.center = Geometry.GetCenter(); // 设置触发器的中心为几何体的中心
        }
    }

    public VoxelCollider GetGeometry() // 获取几何体的方法
    {
        if (Geometry == null) // 如果几何体为空
        {
            Geometry = GetComponent<VoxelCollider>(); // 获取当前物体上的 VoxelCollider 组件
        }
        return Geometry; // 返回几何体
    }

    public Vector3 GetExtents() // 获取扩展的方法
    {
        return Vector3.Scale(transform.lossyScale.Positive(), GetGeometry().GetExtents()); // 根据物体的缩放返回几何体的扩展
    }

    public void AddContact() // 添加接触点的方法
    {
        Transform container = transform.Find("Contacts"); // 找到接触点容器
        if (container == null) // 如果没有找到
        {
            container = new GameObject("Contacts").transform; // 创建新的容器
            container.SetParent(transform); // 设置父物体
            container.localPosition = Vector3.zero; // 设置位置为零
            container.localRotation = Quaternion.identity; // 设置旋转为默认
            container.localScale = Vector3.one; // 设置缩放为1
        }
        Transform contact = new GameObject("Contact").transform; // 创建新的接触点
        contact.SetParent(container); // 设置父物体为容器
        contact.transform.localPosition = Vector3.zero; // 设置位置为零
        contact.transform.localRotation = Quaternion.identity; // 设置旋转为默认
        contact.transform.localScale = Vector3.one; // 设置缩放为1
        contact.gameObject.layer = gameObject.layer; // 设置层级与当前物体相同
        ArrayExtensions.Add(ref Contacts, contact); // 将新接触点添加到 Contacts 数组
    }

    public void AddContact(string name, Vector3 position, Quaternion rotation) // 添加
        
        。。。。


[CustomEditor(typeof(Interaction))] // 指定此类为 Interaction 类的自定义编辑器
public class Interaction_Editor : Editor // 定义 Interaction_Editor 类，继承自 Editor
{
    public Interaction Target; // 声明一个 Interaction 类型的变量，用于引用目标 Interaction 组件

    void Awake() // 当脚本实例被加载时调用
    {
        Target = (Interaction)target; // 将目标设置为当前编辑器正在编辑的 Interaction 组件
    }

    public override void OnInspectorGUI() // 重写 OnInspectorGUI 方法以自定义检查器 GUI
    {
        Undo.RecordObject(Target, Target.name); // 记录当前对象的状态，以便在撤销操作时可以恢复

        Utility.SetGUIColor(UltiDraw.Grey); // 设置 GUI 的颜色为灰色
        using (new EditorGUILayout.VerticalScope("Box")) // 创建一个垂直布局框
        {
            Utility.ResetGUIColor(); // 重置 GUI 颜色
            EditorGUILayout.HelpBox("Contacts", MessageType.None); // 显示一个帮助框，标题为 "Contacts"
            Target.ShowContacts = EditorGUILayout.Toggle("Show Contacts", Target.ShowContacts); // 提供一个复选框来控制是否显示接触点
            
            for (int i = 0; i < Target.Contacts.Length; i++) // 遍历所有接触点
            {
                Target.Contacts[i] = (Transform)EditorGUILayout.ObjectField(Target.Contacts[i], typeof(Transform), true); // 显示对象字段以选择 Transform 对象
            }
            
            EditorGUILayout.BeginHorizontal(); // 开始一个水平布局
            if (Utility.GUIButton("Add", UltiDraw.DarkGrey, UltiDraw.White)) // 如果点击“Add”按钮
            {
                Target.AddContact(); // 调用目标的 AddContact 方法添加接触点
            }
            if (Utility.GUIButton("Remove", UltiDraw.DarkGrey, UltiDraw.White)) // 如果点击“Remove”按钮
            {
                Target.RemoveContact(); // 调用目标的 RemoveContact 方法移除接触点
            }
            EditorGUILayout.EndHorizontal(); // 结束水平布局
        }

        if (GUI.changed) // 如果 GUI 发生变化
        {
            EditorUtility.SetDirty(Target); // 标记目标为已修改，以便在编辑器中保存更改
        }
    }
}
#endif // 结束条件编译指令

```





## 相关/base论文

https://samp.is.tue.mpg.de/



![image-20240906143509387](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906143509387.png)

$I$ 交互对象的几何形状

$X_{i-1}$前一个状态

${X}_i$ 当前状态



$\hat{X}_i$ 当前状态

![image-20240905214009919](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240905214009919.png)





5个身体部位![image-20240906144020561](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906144020561.png)



#### GoalNet

![image-20240906144157470](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906144157470.png)



#### 路径导航-A*

![image-20240906144425175](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906144425175.png)

![image-20240906144503445](D:\myNote\Postgraduate\MotionGenerate\3D场景交互Hierarchical Generation of Human-Object Interactions with Diffusion Probabilistic Models\assets\image-20240906144503445.png)



ren:

unity 代码全看懂 晚可b



这是一个自动生成人物与场景交互的unity端的项目代码，结合所有代码，请问我要从哪里看起，以下是文档的一部分：

- ## 运行

  我们的代码使用 Unity 进行可视化和测试。我们依赖 Python 运行网络并通过套接字发送数据。

  ### 使用 Python 构建套接字服务器

  - 使用 Python 为每个模块构建套接字服务器。请查看 [Python](https://ayejng.aitianhu.com/python/README.md)。您应该在 IP 为 x.x.x.x 的计算机上运行服务器。
  - 请在 TrajClient 中指定 IP（当您打开 .unity 文件时，它会出现在左侧窗格中。如果想更改 IP，请双击它，并在右侧窗格中更改数字），并确保 Unity 中的端口号正确。

  ### HGHOI_Demo

  - 打开演示场景（Unity -> Assets -> Demo -> HGHOI_Demo.unity）。
  - 点击播放按钮。
  - 您可以先通过 SAMP 控制角色（WSAD, QE, 左 Shift, C, L）。
  - 您可以点击左侧的按钮（坐 / 躺）来测试 HGHOI。

  ### HGHOI_Test

  - 打开测试场景（Unity -> Assets -> Demo -> HGHOI_Demo.unity）。
  - 点击播放按钮。
  - 您可以看到测试开始。







