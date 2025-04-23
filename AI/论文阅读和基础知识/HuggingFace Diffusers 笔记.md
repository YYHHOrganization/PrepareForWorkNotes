# HuggingFace Diffusers 笔记

参考链接：https://huggingface.co/docs/diffusers/index

# 一、基础准备

先用AutoDL创建一个服务器，然后直接在base conda环境中做测试即可，先安装diffusers和transformers库：
```bash
pip install diffusers["torch"] transformers
```



## 1.配置Huggingface镜像

https://hf-mirror.com/ 这篇下面有进行介绍。以下是需要输入配置的指令：
```bash
pip install -U huggingface_hub
export HF_ENDPOINT=https://hf-mirror.com
```



# 二、实操

## 1.基本认知

```python
from diffusers import DDPMScheduler, UNet2DModel

scheduler = DDPMScheduler.from_pretrained("google/ddpm-cat-256")
model = UNet2DModel.from_pretrained("google/ddpm-cat-256").to("cuda")

scheduler.set_timesteps(50)
# print(scheduler.timesteps)

import torch

sample_size = model.config.sample_size
noise = torch.randn((1, 3, sample_size, sample_size), device="cuda") # (1, 3, 256, 256),指的是（batch_size, channel, height, width）

# 以下为去噪的过程代码
input = noise  # 初始化为纯噪声（latent space维度）

for t in scheduler.timesteps:  # 遍历所有timestep（从大到小，如1000→0）
    with torch.no_grad():
        # 步骤1：UNet预测噪声残差
        noisy_residual = model(input, t).sample  # 输入当前噪声图+时间步，输出预测的噪声
    
    # 步骤2：Schedular会根据当前的噪声图和时间步，计算出上一步的噪声图（去除一部分噪声）
    previous_noisy_sample = scheduler.step(noisy_residual, t, input).prev_sample  # 计算去噪后的图像
    
    # 步骤3：更新输入为去噪后的图像
    input = previous_noisy_sample  # 作为下一轮迭代的输入

# 把去噪后的结果转换为图像
from PIL import Image
import numpy as np
print('==============now input====================')
print(input.shape)  # (1, 3, 256, 256)
# print(input) # 范围是[-1, 1]
print('==============end====================')

image = (input / 2 + 0.5).clamp(0, 1).squeeze() # squeeze()去掉batch_size维度
image = (image.permute(1, 2, 0) * 255).round().to(torch.uint8).cpu().numpy() # permute函数是为了把维度从(3, 256, 256)变成(256, 256, 3)，*255是为了把范围从[0,1]变成[0,255]，round()四舍五入，to(torch.uint8)转换为uint8类型
image = Image.fromarray(image)
image.save("cat_manualDiffusion.png")  # 保存图片
```

 You’ll initialize the necessary components, and set the number of timesteps to create a `timestep` array. The `timestep` array is used in the denoising loop, and for each element in this array, the model predicts a less noisy image. The denoising loop iterates over the `timestep`’s, and at each timestep, it outputs a noisy residual and the scheduler uses it to predict a less noisy image at the previous timestep. This process is repeated until you reach the end of the `timestep` array.



## 2.Deconstruct the Stable Diffusion pipeline

本节的目标是拆解Stable Diffusion。Stable Diffusion是运作在Latent Space下的。The encoder compresses the image into a smaller representation, and a decoder converts the compressed representation back into an image. For text-to-image models, you’ll need a tokenizer and an encoder to generate text embeddings. From the previous example, you already know you need a UNet model and a scheduler.

对SD有一个基本的回顾：

> 以下是精简版回答，以表格形式总结Stable Diffusion核心组件及流程：
>
> ---
>
> ### **1. 核心组件功能**
> | 组件     | 作用                                                  | 训练阶段                                                     | 推理阶段（生成图像）                                         |
> | -------- | ----------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
> | **CLIP** | 文本编码器，将提示词转换为语义向量（Text Embeddings） | 固定权重（通常不训练），直接使用预训练模型                   | 将用户输入的文本提示编码为UNet可理解的向量                   |
> | **VAE**  | 图像编码器/解码器，在像素空间和潜在空间之间转换       | 训练：编码图像为潜在表示（压缩维度），解码重建图像           | 编码器：仅用于训练；解码器：将UNet输出的潜在表示解码为最终图像 |
> | **UNet** | 噪声预测器，在潜在空间逐步去噪                        | 训练：学习预测添加到潜在表示中的噪声（输入带噪潜在向量+时间步+文本条件） | 迭代去噪：根据CLIP文本条件，逐步预测并移除噪声，生成干净的潜在表示 |
>
> ---
>
> ### **2. 训练 vs 推理流程对比**
> | 阶段     | 输入                         | 输出                     | 关键操作                                                     |
> | -------- | ---------------------------- | ------------------------ | ------------------------------------------------------------ |
> | **训练** | 1. 图像 → VAE编码为潜在表示  | 重建图像（VAE解码）      | 1. 对潜在表示加噪声<br>2. UNet学习预测噪声（条件：CLIP文本+时间步） |
> |          | 2. 文本 → CLIP编码为嵌入向量 | 噪声预测损失（UNet输出） |                                                              |
> | **推理** | 1. 文本 → CLIP生成嵌入向量   | 生成图像（VAE解码）      | 1. 从随机噪声开始<br>2. UNet迭代去噪（条件：CLIP文本+调度器控制时间步） |
> |          | 2. 随机噪声 → UNet逐步去噪   |                          | 3. 最终潜在表示 → VAE解码为图像                              |
>
> ---
>
> ### **关键点总结**
> - **CLIP**：文本理解（不参与扩散训练，仅提供条件）。  
> - **VAE**：空间压缩（训练时编码/解码；推理时仅解码）。  
> - **UNet**：扩散核心（训练时学噪声预测，推理时执行去噪）。  
> - **流程差异**：训练时UNet学习噪声预测；推理时用学到的模型逐步去噪生成图像。