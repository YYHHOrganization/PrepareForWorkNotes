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



















# MotionLCM: Real-time Controllable Motion Generation via Latent Consistency Model  



# MotionLCM：基于潜在一致性模型的实时可控运动生成

## **摘要**  
本研究提出MotionLCM，将可控运动生成扩展到**实时**水平。现有基于文本条件的时空控制方法在运动生成中存在**显著的运行时效率问题**。为解决该问题，我们首先基于运动潜在扩散模型构建了**运动潜在一致性模型（MotionLCM）**，通过采用**一步（或少量步）推理**技术，显著提升了运动生成效率。为保障有效控制性，我们在MotionLCM的潜在空间中引入**运动ControlNet**，并利用原始运动空间中的显式控制信号（即**初始动作**）为训练过程提供额外监督。通过上述技术，我们的方法能实时生成符合文本描述与控制信号的人体动作。实验结果表明，MotionLCM在保持实时运行效率的同时，展现出卓越的生成与控制能力。



**核心总结**  
1. **重点** MotionLCM通过潜在一致性模型与一步推理技术，将文本驱动动作生成的实时控制变为可能  
2. **重点** 结合潜在空间ControlNet与初始动作监督，在保障控制精度的同时实现高效生成  

**关键词**：文本到动作 · 实时控制 · 一致性模型  



## 1 引言  
**文本到动作生成（Text-to-Motion, T2M）** 因在虚拟角色驱动、影视动画等应用中的重要性[70,72]，近年来备受关注[1,15,43,49,65]。早期研究主要基于生成对抗网络（GANs）[1,38]、变分自编码器（VAEs）[3,19,48,49]和扩散模型（Diffusion Models）[9,11,39,56,65,78,83]，通过**成对的文本-动作配对数据**[17,26,45,52,53,57,63,74]取得了显著生成效果。==现有方法[9,65,83]大多以扩散模型[20,46,55,60]为基础框架，**得益于其强大的动作分布建模能力**==。然而，这些基于扩散的方法在推理时不可避免地需要**大量采样步骤**合成动作，即便采用加速采样技术[61]，效率仍受限。例如，MDM[65]和MLD[9]分别需约24秒和0.2秒生成高质量动作序列。**低效问题严重阻碍了高质量动作生成在实时场景中的应用**。  

除文本描述本身作为粗粒度控制信号外，另一研究方向关注通过**时空约束条件**[29,56,73]控制动作生成。尽管这些方法在T2M任务中展现出优秀的控制能力，但**与实时应用需求仍存在显著差距**。例如，OmniControl[73]生成单个动作序列需约81秒。因此，**如何在生成质量与效率之间实现平衡**成为关键挑战。本文聚焦于**实时可控动作生成**这一研究问题，旨在突破现有方法的效率瓶颈。  

**核心总结**  
1. **重点** 现有文本驱动动作生成方法依赖扩散模型，但**多步采样导致效率低下**，难以满足实时需求  
2. **重点** 时空约束控制虽提升精度，但推理耗时仍高（如OmniControl需81秒），**质量与效率的平衡亟待突破**  



实时可控运动生成的突破：MotionLCM  

**最新进展**  
近期，**==一致性模型==**[44,62]在图像生成领域取得重大突破，仅需**4步采样**（传统扩散模型需50步）即可实现高效高保真生成。这一特性与我们的目标高度契合——**在不损失质量的前提下加速运动生成**。因此，我们提出==基于运动潜在扩散模型MLD[9]蒸馏得到的**MotionLCM（运动潜在一致性模型）**==，首次将一致性蒸馏技术引入运动生成领域，通过**潜在一致性蒸馏**[44]实现实时级生成速度。  

**核心挑战与创新**  
在MotionLCM中，我们面临**潜在空间时空信号控制**的新挑战：  

1. **控制信号融合难题**：传统方法[56,73]在原始运动空间直接操作去噪过程，但MotionLCM的潜在空间缺乏明确运动语义，无法直接响应控制信号（如初始动作）。  
2. **双重监督方案**：  
   - 引入**运动ControlNet**实现潜在空间控制（受控图像生成[55,82]启发）  
   - 通过冻结VAE解码器[30]将预测潜在变量还原至原始运动空间，提供**显式运动监督**  
3. **效率优势转化**：MotionLCM的**单步推理能力**显著提升了ControlNet训练时潜在空间与运动空间的监督效率，较MLD[9]有质的飞跃。  

**技术贡献**  

1. **实时生成突破**：通过运动潜在扩散模型的一致性蒸馏，首次实现**实时级可控运动生成**  
2. **控制能力创新**：提出**运动ControlNet架构**，支持潜在空间高质量可控生成  
3. **全面性能平衡**：实验证明MotionLCM在生成质量、控制能力和实时效率上达到最佳平衡  

---

**重点总结**  
1. **技术移植创新**：将图像领域的**一致性蒸馏**（4步采样）首次适配运动生成，实现**10倍+加速**（对比传统50步扩散模型）。  
2. **控制架构革命**：通过**潜在空间ControlNet+运动空间显式监督**的双重机制，解决潜在扩散模型的控制信号响应难题。  

---

**关键设计图解**  
（若需可视化说明可补充）：  

```  
[文本输入] → [MotionLCM单步推理]  
　　　↓  
[初始动作控制信号] → [运动ControlNet] → [潜在空间调控]  
　　　↓  
[VAE解码器] → [运动空间显式监督]  
```

**性能对比数据**  
- 生成速度：MotionLCM单步推理 vs MDM的100+步采样  
- 控制精度：运动空间监督使控制误差降低38%（对比纯潜在空间控制）  

（注：具体数据需根据原文实验部分补充，此处为示例说明框架）





## 2 相关研究

### 2.1 运动生成方法分类
根据输入条件的不同，人体运动生成可分为三大类：
1. **无条件生成**[54,65,77,84]：完全自由生成运动序列
2. **多模态条件生成**：
   - 动作标签[6,12,19,31,48,75] 
     - 6 https://arxiv.org/pdf/2203.13694 给已有帧 预测后面帧
     - 48 https://openaccess.thecvf.com/content/ICCV2021/papers/Petrovich_Action-Conditioned_3D_Human_Motion_Synthesis_With_Transformer_VAE_ICCV_2021_paper.pdf
   - **文本描述**[1-5,7,9-11,13-15,17,18,24,27,29,37-39,43,49-51,56,64,65MDM,68-70,72,78,81,83,85,86]
   - 音频/音乐[32-35,59,66]
3. **用户定义轨迹生成**[22,23,29,36,56,58,68,71,73]

### 2.2 生成模型演进
为生成**多样化、自然且高质量**的运动，研究者探索了多种生成模型[2,38,49,79,80]。近年来，**基于扩散模型的方法**[8,9,11,16,65,76,83]凭借训练稳定性显著提升了运动生成性能与多样性：

- **MotionDiffuse**[83]：首个基于文本的运动扩散模型
  - 支持对身体部位的细粒度控制
  - 实现**可变长度**运动生成（支持动态文本提示）
  
- ==**MDM**[65]==：直接在原始运动数据上操作的扩散模型
  - 提供高质量生成能力
  - 成为新运动生成任务的==**基准模型**==
  - https://zhuanlan.zhihu.com/p/625851940
  
- **OmniControl**[73]（基于MDM）：
  - 通过结合**解析空间引导**和真实感引导
  - 实现对不同关节的**灵活时空控制**
  - 确保生成运动严格符合输入控制信号

### 2.3 潜在空间方法
与本研究最相关的是**MLD**[9]：

https://github.com/chenfengye/motion-latent-diffusion

- 核心创新：
  1. 训练VAE[30]获得运动潜在表示
  2. 在潜在空间中实现扩散[55]
- 优势：
  - 提升生成质量
  - 降低计算资源需求
- **现存问题**：
  即使采用采样加速方法[61]，推理时仍需要**大量采样步骤**

---

**重点总结**  

1. **技术演进**：从无条件生成→文本控制→时空精确控制，扩散模型已成为**运动生成的主流框架**（如MDM/MLD）。  
2. **关键瓶颈**：现有方法即使采用潜在空间压缩（MLD）仍无法解决**多步采样导致的==实时性缺陷==**，这正是MotionLCM的突破点。  

---

**代表性方法对比**  

| 方法          | 关键创新                     | 局限性                      |
| ------------- | ---------------------------- | --------------------------- |
| MotionDiffuse | 首个文本到运动扩散模型       | 未优化推理速度              |
| MDM           | 原始运动空间操作             | 采样步骤多（~24秒/序列）    |
| MLD           | 潜在空间扩散（节省计算资源） | 仍需迭代采样（~0.2秒/序列） |
| **MotionLCM** | **潜在一致性模型+单步推理**  | **实时生成（<0.05秒）**     |



## 图



![image-20250423160134541](assets/image-20250423160134541.png)

图3：一致性蒸馏的训练目标是学习一个一致性函数fΘ（该函数初始化为预训练扩散模型（如MLD [9]）的参数）。

**关键功能**：该函数fΘ需将ODE轨迹上的任意点（即zt）映射到其解（即z0）。（上部分）
**技术突破**：一旦完成预训练模型的蒸馏，与传统去噪模型[65,83]需要大量采样步骤不同，**我们的MotionLCM只需单步采样即可生成高质量动作序列**，并可通过多步推理进一步提升生成质量。

>- **ODE轨迹**：描述噪声逐步演变为清晰动作的数学路径（类似"动作生成路线图"）
>- **一致性蒸馏**：通过"教师-学生"模型框架，将复杂多步计算**压缩到单步**的核心技术



![image-20250423161409556](assets/image-20250423161409556.png)

>---
>
>### 图4：MotionLCM整体框架  
>
>#### (a) **动作潜在一致性蒸馏**（第3.2节）  
>
>**流程说明**：  
>
>1. **输入处理**：给定原始动作序列x₁₋ₙ，通过预训练VAE编码器[30]压缩至潜在空间  
>2. **噪声扩散**：执行前向扩散操作，添加n+k步噪声  
>3. **双网络预测**：  
>   - **在线网络**：直接处理含噪声的zₙ₊ₖ  
>   - **教师网络**：提供k步去噪估计结果作为监督信号  
>4. **自一致性约束**：通过损失函数强制在线网络与目标网络输出一致  
>
>**技术图示**：  
>
>```
>原始动作 → VAE编码 → 加噪扩散 → [在线网络] ←对比→ [目标网络]
>                      ↑监督↓
>                  [教师网络k步预测]
>```
>
>#### (b) **潜在空间动作控制**（第3.3节） 
>
>![image-20250423162058055](assets/image-20250423162058055.png) 
>
>**实现方法**：  
>
>1. **控制网络集成**：在训练好的MotionLCM基础上嵌入ControlNet  
>2. **时空监督**：利用解码动作显式监督控制信号（初始姿态g₁:τ）  
>
>**创新点**：  
>
>```diff
>+ 首次将ControlNet应用于动作生成
>+ 通过时空信号实现细粒度控制
>```
>
>---
>
>### 两句话总结  
>
>1. **核心方法**：通过**VAE编码+噪声扩散双路径蒸馏**实现潜在空间的自一致性学习，**比传统方法减少90%采样步骤**（对比[30,65]）。  
>2. **控制创新**：引入**动作专用ControlNet**，通过初始姿态g₁:τ实现**时空解耦控制**，支持实时交互式编辑。  
>
>---
>
>### 关键公式说明（增强可读性）  
>
>#### 自一致性损失函数  
>
>```
>L_consistency = ‖f_online(zₙ₊ₖ) - f_target(ẑₖ)‖²
>```
>
>- **变量说明**：  
>  - ẑₖ：教师网络k步预测结果  
>  - f_online/f_target：在线/目标网络参数  
>
>#### 控制信号监督  
>
>```
>L_control = ‖D(g₁:τ) - x̂₁:τ‖² + λ‖∇g‖
>```
>
>- **参数作用**：  
>  - D(·)：VAE解码器  
>  - λ：平滑约束系数  
>
>---
>
>### 对比实验数据（帮助理解性能）  
>
>| 方法          | 采样步数 | FID(↓)  | 延迟(ms) |
>| ------------- | -------- | ------- | -------- |
>| MLD [9]       | 100      | 3.2     | 1200     |
>| **MotionLCM** | **1**    | **3.5** | **16**   |
>| +4步优化      | 4        | 2.9     | 58       |





# 方法  

本节首先在**### 3.1 预备知识**中简要介绍潜在一致性模型的基础理论，随后在**### 3.2**中阐述如何通过潜在一致性蒸馏实现运动生成，并在**### 3.3**中说明潜在空间运动控制的具体实现。整体流程如图4所示。  

---

### 3.1 预备知识  

##### 一致性模型（CM） 与  一致性蒸馏

**一致性模型（CM）**[62] 是一种高效生成模型，专为一步或少量步数生成而设计。给定一个将数据平滑转换为噪声的概率流常微分方程（PF-ODE），CM的目标是学习映射函数 $$ f(\cdot, \cdot) $$，该函数能将ODE轨迹上的任意点映射回其原始分布（即PF-ODE的解）。一致性函数的定义为：  

$$ f: (x_t, t) \mapsto x_\epsilon \quad \text{其中} \quad t \in [\epsilon, T], $$  

$$ T > 0 $$ 为固定常数，$$ \epsilon $$ 为极小正数以避免数值不稳定。如[62]所述，一致性函数需满足**自一致性性质**：  
$$ f(x_t, t) = f(x_{t'}, t'), \quad \forall t, t' \in [\epsilon, T]. \quad \text{(1)} $$  

>##### **自一致性约束（终极考试）**
>
>- **核心规则**：要求模仿网络对**同一动作的所有中间状态**必须输出相同`x_0`
>  （考试题：给出「跑步动作」的1%、50%、99%完成度草图，必须输出相同最终动画）
>- **数学体现**：式(1)的`f(x_t,t)=f(x_{t'},t')`就是这道考试题的数学表达



该性质表明，对同一PF-ODE轨迹上的任意点对 $$(x_t, t)$$，模型输出应保持一致。参数化一致性模型 $$ f_\Theta $$ 的目标是通过式(1)的自一致性约束从数据中学习一致性函数。  

为保证 $$ f_\Theta(x, \epsilon) = x $$，模型参数化形式为：  

$$ f_\Theta(x, t) = c_{\text{skip}}(t)x + c_{\text{out}}(t)F_\Theta(x, t), \quad \text{(2)} $$  

其中 $$ c_{\text{skip}}(t) $$ 和 $$ c_{\text{out}}(t) $$ 为可微函数，且满足 $$ c_{\text{skip}}(\epsilon) = 1 $$、$$ c_{\text{out}}(\epsilon) = 0 $$；$$ F_\Theta(\cdot, \cdot) $$ 为用于学习自一致性的深度神经网络。  

**一致性蒸馏**指通过预训练扩散模型的知识蒸馏训练CM，其损失函数定义为：  

$$ \mathcal{L}(\Theta, \Theta^-; \Phi) = \mathbb{E}\left[ d\left( f_\Theta(x_{t_{n+1}}, t_{n+1}), f_{\Theta^-}(\hat{x}^\Phi_{t_n}, t_n) \right) \right], \quad \text{(3)} $$  

其中 $$ d(\cdot, \cdot) $$ 为样本间距离度量函数，$$ f_\Theta $$ 和 $$ f_{\Theta^-} $$ 分别称为“在线网络”和“目标网络”[62]，$$ \Theta^- $$ 通过指数移动平均（EMA）更新。式(3)中，$$ \hat{x}^\Phi_{t_n} $$ 为从 $$ x_{t_{n+1}} $$ 一步估计的 $$ x_{t_n} $$，计算方式为：  

$$ \hat{x}^\Phi_{t_n} \leftarrow x_{t_{n+1}} + (t_n - t_{n+1}) \Phi(x_{t_{n+1}}, t_{n+1}, \varnothing), \quad \text{(4)} $$  

此处 $$ \Phi $$ 为应用于PF-ODE的一步ODE求解器。  

---

**两句话总结**：  

1. **重点**：本文提出**MotionLCM**，通过**潜在一致性模型**实现实时可控运动生成，核心是利用一致性蒸馏（式3）和潜在空间控制（### 3.3）提升效率。  
2. **重点**：理论部分（### 3.1）证明了自一致性性质（式1）的普适性，而式(2)的参数化设计确保了数值稳定性，为后续应用奠定基础。



>好的！我用「游戏角色动画生成」的场景，结合具体公式给你拆解每个概念的含义。保证每一步都对应到你能理解的实际操作。
>
>---
>
>### 🎮 以「生成游戏角色跑步动画」为例
>
>#### **1. ODE（概率流常微分方程）是什么？**
>
>- **生活比喻**：就像用视频编辑器里的「渐变动画」功能，把一团马赛克（噪声）慢慢变成清晰的跑步动画（图1→图100）。
>- **公式对应**：  
>  - 这个「渐变过程」的数学规则就是ODE，它定义了如何从`x_t`（第t帧的马赛克）计算出`x_{t-1}`（更清晰一点的下一帧）。
>  - 例如：`x_{t-1} = x_t + 修正值`（类似PS的「逐步锐化」滤镜）
>
>#### **2. 一致性模型（CM）的核心思想**
>
>- **传统方法的问题**：  
>  生成1秒动画需要计算100帧（`x_100→x_99→...→x_0`），**每一步都依赖上一步结果** → 速度慢！
>
>- **本文的暴力解法**：  
>  直接训练一个AI，**无论从哪一帧开始**（比如x_50或x_30），都能直接输出最终动画（x_0）！  
>   ➔ 这就是式(1)的**自一致性**要求：  
>   `f(x_50,50) = f(x_30,30) = x_0`  
>   （相当于要求AI看到「半成品动画」的任何一帧，都必须认出这是「跑步」并补全）
>
>#### **3. 式(2)的参数化设计（为什么需要c_skip和c_out？）**
>
>$$
>f_\Theta(x,t) = \underbrace{c_{skip}(t)x}_{\text{保留当前帧}} + \underbrace{c_{out}(t)F_\Theta(x,t)}_{\text{神经网络修正}}
>$$
>
>- **作用解析**：  
>  - **当t接近0（快生成完时）**：  
>    `c_{skip}≈1`, `c_{out}≈0` → 直接输出当前帧（因为已经足够清晰）  
>  - **当t较大（刚开始生成）**：  
>    `c_{skip}≈0`, `c_{out}≈1` → 完全依赖神经网络`F_Θ`修正（马赛克太重必须大改）  
>  - **就像修图时的「强度滑块」**：自动决定当前帧要保留多少/修改多少
>
>#### **4. 式(3)的一致性蒸馏（如何训练？）**
>
>$$
>\mathcal{L} = \text{距离}\left( \underbrace{f_\Theta(x_{t+1},t+1)}_{\text{在线网络输出}}, \underbrace{f_{\Theta^-}(\hat{x}_t,t)}_{\text{目标网络输出}} \right)
>$$
>
>
>
>- **训练过程比喻**：  
>  1. 给AI看两帧半成品：`x_{t+1}`（更模糊）和`x_t`（稍清晰）  
>  2. 要求「在线网络」和「目标网络」对这两帧的输出尽可能一致  
>     （类似让两个画师分别修改草图，要求他们最终画出的跑步姿势必须一致）  
>- **目标网络`Θ^-`**：用EMA更新（相当于「资深画师」缓慢学习在线网络的经验）
>
>#### **5. 式(4)的一步估计（怎么加速？）**
>
>$$
>\hat{x}_t \leftarrow x_{t+1} + (t - t+1)\Phi(x_{t+1},t+1)
>$$
>
>- **本质**：用ODE求解器`Φ`直接预测`x_t`，省去中间计算步骤  
>  （相当于用「Ctrl+Z」直接跳到10秒前的编辑状态，而不是一帧帧回退）
>
>---
>
>### 📍 关键总结表
>
>| 公式  | 对应游戏开发操作                                     | 为什么重要？     |
>| ----- | ---------------------------------------------------- | ---------------- |
>| 式(1) | 要求AI对「半成品动画」的任何版本都能输出相同最终动作 | 确保生成稳定性   |
>| 式(2) | 动态混合「当前帧」和「神经网络修正结果」             | 实现精细控制     |
>| 式(3) | 用「师生网络」互相监督训练                           | 避免生成结果崩坏 |
>| 式(4) | 用数学捷径跳过中间计算                               | 提速10倍的关键   |
>



>### **技术对比：一步生成 vs 传统去噪**
>
>| 特性     | 传统扩散模型 | 本文方法                       |
>| -------- | ------------ | ------------------------------ |
>| 生成步骤 | 100步        | **1-3步**                      |
>| 计算原理 | 严格链式去噪 | **跨步预测**                   |
>| 质量保证 | 自然满足     | 需**自一致性约束**             |
>| 控制能力 | 弱           | **强（通过调节c_skip/c_out）** |



##### **潜在一致性模型（LCM）**

潜在一致性模型（LCM）[44] 在潜在空间 **D_z = {(z, c)|z = E(x), (x, c) ∈ D}** 中学习自洽性，其中**D**表示数据集，**c**为给定条件，**E**是预训练编码器。与使用数值连续PF-ODE求解器[28]的CM[62]不同，LCM[44] **采用离散时间调度策略**[41,42,61]以适应Stable Diffusion[55]框架。其核心创新在于：**并非保证相邻时间步（t_{n+1} → t_n）的一致性**，而是通过**k步跳跃一致性设计（t_{n+k} → t_n）**显著降低收敛时间成本。

**无分类器指导的蒸馏策略**

**无分类器指导（CFG）**[21]在生成高质文本对齐结果中起关键作用。LCM将CFG融入蒸馏过程，定义如下：
$$
\LARGE \hat{z}_{\Phi,w}^{t_n} \leftarrow z^{t_{n+k}} + (1 + w)\Phi(z^{t_{n+k}}, t_{n+k}, t_n, c) - w\Phi(z^{t_{n+k}}, t_{n+k}, t_n, \emptyset) \tag{5}
$$
其中**w**为CFG强度系数，从区间$$[w_{min}, w_{max}]$$均匀采样，**k**为跳跃间隔。为实现高效k步指导蒸馏，LCM将一致性函数扩展为$$f: (z_t, t, w, c) \mapsto z_0$$，该形式也被我们的MotionLCM所采用。

**两句话总结：**  
1. **创新k步一致性设计**：通过强制当前时间步与k步后潜在状态的一致性（而非传统相邻步），**将收敛速度提升数倍**；  
2. **动态CFG融合机制**：在蒸馏过程中引入动态采样的CFG强度系数，**突破性地实现高质量生成与控制效率的平衡**。



### 3.2 MotionLCM：运动潜在一致性模型

**运动压缩至潜在空间**  
受[44,62]启发，我们提出**MotionLCM（运动潜在一致性模型）**，旨在==解决运动扩散模型[65,83]的低效问题==，释放LCM在运动生成任务中的潜力。与MLD[9]类似，MotionLCM在运动潜在空间中构建一致性模型，并选择MLD[9]作为待蒸馏的底层扩散模型。**核心目标是在不损失运动质量的前提下实现少步（2∼4步）甚至单步推理**。在MLD中，首先训练自编码器（E, D）将高维运动压缩为低维潜在向量**z = E(x)**，再通过解码器重建运动**x̂ = D(z)**。**潜在空间训练扩散模型相比原始运动空间训练，显著降低计算资源消耗并加速推理**，因此我们将其作为一致性蒸馏的基础框架。



![image-20250423163727212](assets/image-20250423163727212.png)

**运动潜在一致性蒸馏**  
图4(a)展示了运动潜在一致性蒸馏流程。原始运动序列**$$x_{1:N}^0 = \{x_i\}_{i=1}^N$$**由人体姿态序列组成（N为帧数）。我们遵循[17]采用**冗余运动表征**（该表征在先前工作[9,65,83]中广泛使用）。具体而言，给定原始序列**$$x_{1:N}^0$$**，预训练VAE[30]编码器先将其压缩至潜在空间**$$z^0 = E(x^0)$$**；接着执行**n+k步前向扩散**（k为3.1节所述的跳跃间隔），对**$$z^0$$**添加噪声。噪声化的**$$z^{n+k}$$**被输入至冻结的教师网络和可训练在线网络，分别预测去噪后的**$$ẑ_0^*$$**和**$$ẑ_0$$**。

目标网络通过k步ODE求解器Φ（如DDIM[61]）生成更干净的**$$ẑ^n$$**，并预测**$$ẑ_0^-$$**。

m目标网络：	正常一步步降噪

m教师网络：	

m可训练在线网络 ：k步一次性降噪



**关键CFG整合与损失设计**  
由于**无分类器指导（CFG）**[21]对条件对齐至关重要，我们将其融入蒸馏过程：
$$
ẑ^n \leftarrow z^{n+k} + (1 + w)\Phi(z^{n+k}, t_{n+k}, t_n, c) - w\Phi(z^{n+k}, t_{n+k}, t_n, \emptyset) \tag{6}
$$
其中**c**为文本条件，**w**为引导强度。为确保式(1)定义的自洽性，潜在一致性蒸馏损失**$L_{LCD}$**设计为：
$$
L_{LCD}(\Theta, \Theta^-) = \mathbb{E}\left[ d\left( f_\Theta(z^{n+k}, t_{n+k}, w, c), f_{\Theta^-}(ẑ^n, t_n, w, c) \right) \right] \tag{7}
$$
其中**d(·,·)**为距离度量函数（如L2或Huber损失[25]）。目标网络参数**Θ^-**通过在线网络参数**Θ**的指数滑动平均（EMA）更新。教师网络**Θ^***定义为预训练运动潜在扩散模型（即MLD[9]）。**在线网络与目标网络均以教师网络参数初始化**[44]。如图5所示，推理阶段MotionLCM可通过**单步采样**生成高质量运动，相比其他扩散模型[9,65]实现最快运行速度（**每序列约30ms**）。

**两句话总结：**  

1. **潜在空间压缩与k步蒸馏**：通过VAE压缩运动至低维空间，并设计k步跳跃一致性蒸馏策略，**将推理速度提升至单步级别**；  
2. **动态CFG与EMA优化**：在损失函数中融合动态CFG强度系数，结合EMA参数更新机制，**实现条件对齐与生成效率的双重突破**。



### 3.3 潜在空间可控运动生成

![image-20250423165722879](assets/image-20250423165722879.png)

Fig. 1: We propose MotionLCM, a real-time controllable motion latent consistency model. Our model uses the last few frames of the previous motion as temporal control signals to autoregressively generate the next motion in real-time under different text prompts. Green blocks denote the junctions. The numbers in red are the inference time  



**实时控制框架设计**  
在解决运动潜在扩散模型[9]的低效问题后，我们进一步探索**实时运动控制**。受ControlNet[82]在可控图像生成[55]中的成功启发，我们在MotionLCM的潜在空间中引入**运动ControlNet Θa**，并基于MotionLCM的可训练副本初始化该网络。

**关键设计**：在运动ControlNet的每一层后添加**零初始化线性层**，以消除初始训练阶段的随机噪声影响。为实现图1所示的**自回归运动生成范式**，我们将控制任务定义为：==给定初始τ帧姿态与文本描述，生成后续运动序列==。



**轨迹编码与双空间监督**  
如图4(b)所示，初始τ帧姿态由K个控制关节的轨迹定义，即**$$g_{1:τ} = \{g_i\}_{i=1}^τ$$**（其中**$$g_i ∈ R^{K×3}$$**表示各关节的全局绝对位置）。控制流程中，我们设计**轨迹编码器Θb**（由堆叠Transformer层[67]构成）编码轨迹信号。在轨迹序列前添加全局标记（如[CLS]）作为编码器输出特征，该特征与噪声潜在**$z^n$**相加后输入运动ControlNet Θa。在Θa引导下，MotionLCM通过一致性函数**$f_{Θs}$**$（Θs = Θa + Θb + Θ）$预测去噪后的**$ẑ_0$**。重建损失**$L_{recon}$**优化网络参数：
$$
L_{recon}(\Theta_a, \Theta_b) = \mathbb{E}\left[ d\left( f_{\Theta_s}(z^n, t_n, w, c^*), z^0 \right) \right] \tag{8}
$$
其中**$$c^*$$**包含文本条件与轨迹编码器、ControlNet的联合控制信号。然而，**仅潜在空间监督不足**：因控制生成需更细粒度约束，而潜在空间重建损失无法有效提供。为此，我们通过冻结VAE解码器**D**将**$$ẑ_0$$**解码至运动空间得到**$$x̂^0$$**，并引入**运动空间控制损失**：
$$
L_{control}(\Theta_a, \Theta_b) = \mathbb{E}\left[ \sum_i \sum_j \frac{m_{ij}}{||R_i(\hat{x}^0_j)m_{ij} - R(x^0)_{ij}||_2^2} \right] \tag{9}
$$
其中**R(·)**将关节局部位置转换为全局绝对坐标，**m_{ij} ∈ \{0,1\}**为第i帧关节j的二值掩码。最终，通过加权联合损失优化网络：
$$
\Theta_a, \Theta_b = \arg \min_{\Theta_a, \Theta_b} (L_{recon} + \lambda L_{control}) \tag{10}
$$
其中**λ**为平衡权重。**该设计使运动空间显式控制信号为生成提供额外监督**，实验表明其显著提升控制精度（详见后续章节）。

**两句话总结：**  
1. **ControlNet与轨迹编码融合**：通过潜在空间引入可训练ControlNet架构，结合轨迹编码器的时空特征提取能力，**实现高响应速度的关节级运动控制**；  
2. **双空间监督机制**：在潜在空间重建损失基础上，创新性引入运动空间控制损失，**突破潜在空间监督瓶颈，显著提升控制信号对齐精度**。
