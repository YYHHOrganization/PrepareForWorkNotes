

# Scaling Up Dynamic Human-Scene Interaction Modeling

https://jnnan.github.io/trumans/

![image-20240911112715936](D:\myNote\Postgraduate\MotionGenerate\Scaling Up Dynamic Human-Scene Interaction Modeling\assets\image-20240911112715936.png)



### 摘要

面对数据稀缺和高级动作合成在人体场景交互（HSI）建模中的挑战，我们推出了 TRUMANS（跟踪场景中的人类动作）数据集，并提出了一种新颖的 **HSI 动作合成方法**。TRUMANS 是目前最全面的运动捕捉 HSI 数据集，涵盖了超过 15 小时的人类互动，分布在 100 个室内场景中。它详细捕捉了全身人类动作和局部物体动态，特别关注接触的真实性。该数据集通过将物理环境转换为精确的虚拟模型，并对人类和对象的外观及动作进行广泛增强，同时保持互动的真实感，从而进一步扩展。利用 TRUMANS，我们设计了一种基于扩散的自回归模型，能够高效生成任意长度的人类-场景交互（HSI）序列，同时考虑场景上下文和预期动作。在实验中，我们的方法在多种 3D 场景数据集上显示出显著的零样本泛化能力（例如 PROX、Replica、ScanNet、ScanNet++），生成的动作与原始运动捕捉序列非常相似，这得到了定量实验和人类研究的验证。