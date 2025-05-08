# MotionLCM 跑代码 看代码 和改代码等



# 关键代码

```python
teacher_unet = base_model.denoiser # teacher model是base

unet = instantiate_from_config(cfg.model.denoiser) # 要训练的LCM

target_unet = instantiate_from_config(cfg.model.denoiser) #


```



验证代码如FID位置

D:\_Postgraduate\motionGen\MotionLCM\MotionLCM\mld\models\metrics\utils.py



## 步骤

服务器开机：

![image-20250425153454160](assets/image-20250425153454160.png)

打开vscode

点击左下角之前连接过的

![image-20250425153531089](assets/image-20250425153531089.png)

打开文件!

进入输密码环节（复制上上图的密码）

![image-20250425153437777](assets/image-20250425153437777.png)

```
conda activate motionlcm
```





如何跑出来的细节请看：

D:\myNote\ppNotes\PrepareForWorkNotes\AI\论文阅读和基础知识\如何使用AutoDL跑代码？.md



```
MotionLCM
├── configs
├── configs_v1
├── datasets
│   ├── humanml3d
│   │   ├── new_joint_vecs
│   │   ├── new_joints
│   │   ├── texts
│   │   ├── Mean.npy
│   │   ├── Std.npy
│   │   ├── ...
│   └── humanml_spatial_norm
│       ├── Mean_raw.npy
│       └── Std_raw.npy
├── deps
│   ├── glove
│   ├── sentence-t5-large
|   ├── smpl_models
│   └── t2m
├── experiments_control
│   ├── spatial
│   │   └── motionlcm_humanml
│   │       ├── motionlcm_humanml_s_all.ckpt
│   │       └── motionlcm_humanml_s_pelvis.ckpt
│   └── temproal
│   │   └── motionlcm_humanml
│   │       ├── motionlcm_humanml_t_v1.ckpt
│   │       └── motionlcm_humanml_t.ckpt
├── experiments_recons
│   └── vae_humanml
│       └── vae_humanml.ckpt
├── experiments_t2m
│   ├── mld_humanml
│   │   ├── mld_humanml_v1.ckpt
│   │   └── mld_humanml.ckpt
│   └── motionlcm_humanml
│       ├── motionlcm_humanml_v1.ckpt
│       └── motionlcm_humanml.ckpt
├── ...
```

服务器上的代码有这些结构

![image-20250425155302381](assets/image-20250425155302381.png)

---

### **MotionLCM代码结构精要解析与阅读路线**

---

#### **1. 核心目录优先级排序**（根据你的实时控制需求）

| 目录/文件                            | 作用解析                                     | 必读指数 | 推荐阅读时间 |
| ------------------------------------ | -------------------------------------------- | -------- | ------------ |
| **`configs/`**                       | 所有模型超参数定义（扩散步数、隐空间维度等） | ★★★★★    | 1小时        |
| **`mld/models/modeltype/mld.py`**    | 主模型架构（扩散过程+控制逻辑）              | ★★★★★    | 3小时        |
| **`datasets/humanml3d/new_joints/`** | 原始运动数据格式（Unity需对齐）              | ★★★★☆    | 2小时        |
| **`experiments_control/spatial/`**   | ControlNet权重文件（实时控制核心）           | ★★★★☆    | 1小时        |
| **`deps/smpl_models/`**              | SMPL人体模型参数（需转换到Unity骨骼）        | ★★★☆☆    | 30分钟       |

---

#### **2. 关键路径详解**

1. **配置入口**  
   
   ```bash
   configs/
   └── motionlcm.yaml       # 主配置文件（扩散步数、学习率等）
   configs_v1/              # 旧版配置（可忽略）
   ```
   **重点参数**：
   ```yaml
   model:
     denoiser:
       params:
         timesteps: 50      # 扩散模型总步数 → 影响生成速度
         nfe: 4             # 实际推理步数 → 实时性关键参数
   ```
   
2. **数据管道**  
   ```bash
   datasets/humanml3d/
   ├── new_joints/          # 原始骨骼数据（.npy格式）
   │   └── 002051.npy       # 形状：(120, 22, 3) → (帧, 关节, 坐标)
   ├── texts/               # 文本-动作对齐描述
   ├── Mean.npy             # 数据标准化均值
   └── Std.npy              # 数据标准化方差
   ```
   **移植重点**：需将`new_joints`的22关节转换为Unity的Humanoid骨骼系统

3. **预训练模型**  
   ```bash
   experiments_control/spatial/motionlcm_humanml/
   ├── motionlcm_humanml_s_all.ckpt     # 全身控制模型
   └── motionlcm_humanml_s_pelvis.ckpt  # 骨盆区域控制
   ```
   **控制逻辑**：这些Checkpoint包含ControlNet结构，可通过`demo.py`的`--control_type`参数调用

4. **人体模型参数**  
   ```bash
   deps/smpl_models/
   ├── SMPL_NEUTRAL.pkl     # 中性体型模型
   └── smplh/               # 含手部细节的模型
   ```
   **转换工具**：需使用`SMPLX-Unity-Converter`等工具转换到Unity可用格式

---

#### **3. 代码阅读路线图**

**阶段一：理解数据流（1天）**
```python
# 在`mld/data/get_data.py`中：
dataset = get_dataset(cfg)  # 数据加载入口
batch = dataset[0]          # 典型数据结构：
                            # {
                            #   'text': "walking", 
                            #   'length': 120,
                            #   'joints': [120, 22, 3],
                            #   'hint': [120, 4]  # 控制信号
                            # }
```

**阶段二：掌握生成逻辑（2天）**
```python
# 在`mld/models/modeltype/mld.py`中：
def _diffusion_forward(self, batch):
    # 关键扩散过程（需优化部分）
    for t in reversed(range(0, timesteps)):
        x = denoiser(x, t, cond)  # 降噪UNet
        if use_controlnet:        # 实时控制分支
            x += controlnet(x, hint)
```

**阶段三：控制信号对接（1天）**
```bash
# 运行ControlNet示例：
python demo.py \
  --control_type pelvis \
  --example assets/control_hints.txt  # 控制信号文件格式：
                                      # 120 0 0.5  # 帧数 控制类型 强度
                                      # 60 1 0.8
```

---

#### **4. Unity移植关键步骤**

1. **数据格式转换**  
   ```csharp
   // Unity C#示例：将22关节数据转换为Humanoid
   void ConvertToHumanoid(float[,,] joints) {
       hips.position = joints[:,0,:];  // 0号关节为骨盆
       spine.position = joints[:,1,:];
       // ...其他关节对应关系需根据SMPL定义调整
   }
   ```

2. **实时控制接口**  
   ```python
   # 修改demo.py添加Socket服务端
   import socket
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(('localhost', 12345))
   while True:
       conn.send(joints.tobytes())  # 实时发送关节数据到Unity
   ```

3. **性能优化技巧**  
   ```python
   # 在configs/motionlcm.yaml中：
   model:
     denoiser:
       params:
         nfe: 4 → 2   # 减少扩散步数
         quantize: true  # 添加8位量化
   ```

---

#### **5. 论文创新点提炼方向**

1. **实时性优化**
   - 提出**动态步数扩散**（根据控制信号强度自动调节nfe）
   - 实现**CUDA核函数加速**的关键扩散步骤

2. **跨引擎适配**
   - 设计**SMPL-to-Unity自动骨骼映射**算法
   - 开发**Motion Stream Protocol**实时传输协议

3. **物理增强**
   - 在ControlNet中添加**物理约束损失项**
   - 集成**Unity Physics进行运动修正**

---

#### **下一步建议**
1. 从`demo.py`的`main()`函数开始，用PyCharm的**调试模式**逐行跟踪数据流
2. 修改`configs/motionlcm.yaml`中的`nfe`参数，观察生成速度/质量变化
3. 使用Unity的**Articulation Body组件**替换默认骨骼，测试物理表现





# 文件结构 Folder Structure



我正在尝试读懂这个MotionLCM（https://github.com/Dai-Wenxun/MotionLCM），我要基于这个工作做新的研究，这是这篇MotionLCM论文的一些内容：

MotionLCM: Real-time Controllable Motion Generation via Latent Consistency Model  



Abstract. This work introduces MotionLCM, extending controllable motion generation to a real-time level. Existing methods for spatialtemporal control in text-conditioned motion generation suffer from significant runtime inefficiency. To address this issue, we first propose the motion latent consistency model (MotionLCM) for motion generation,  building on the motion latent diffusion model. By adopting one-step (or few-step) inference, we further improve the runtime efficiency of the motion latent diffusion model for motion generation. To ensure effective controllability, we incorporate a motion ControlNet within the latent space of MotionLCM and enable explicit control signals (i.e.

, initial motions) in the vanilla motion space to further provide supervision for the training process. By employing these techniques, our approach can generate human motions with text and control signals in real-time. Experimental results demonstrate the remarkable generation and controlling capabilities of MotionLCM while maintaining real-time runtime efficiency.



Keywords: Text-to-Motion · Real-time Control · Consistency Model



3 Method



In this section, we first briefly introduce preliminaries about latent consistency models in Sec. 3.1. Then, we describe how to conduct latent consistency distillation for motion generation in Sec. 3.2, followed by our implementation of motion control in latent space in Sec. 3.3. The overall pipeline is illustrated in Fig. 4



1. **潜在空间压缩与k步蒸馏**：通过VAE压缩运动至低维空间，并设计k步跳跃一致性蒸馏策略，**将推理速度提升至单步级别**；  
2. **动态CFG与EMA优化**：在损失函数中融合动态CFG强度系数，结合EMA参数更新机制，**实现条件对齐与生成效率的双重突破**。



1. **ControlNet与轨迹编码融合**：通过潜在空间引入可训练ControlNet架构，结合轨迹编码器的时空特征提取能力，**实现高响应速度的关节级运动控制**；  
2. **双空间监督机制**：在潜在空间重建损失基础上，创新性引入运动空间控制损失，**突破潜在空间监督瓶颈，显著提升控制信号对齐精度**。

# 5 结论  

本文提出**高效可控运动生成框架MotionLCM**，通过**潜在一致性蒸馏技术**实现生成速度与质量的平衡，并借助**潜在空间运动控制网络**实现精准条件控制。实验证明：

- 实时生成速度达$$30\text{ms}/\text{序列}$$（比MLD快13倍）
- 多关节控制误差降低46%（Loc. err. 0.38→0.21）
- 消融实验验证**动态训练引导范围**（$$w\in[5,15]$$）与**Huber损失**的关键作用

**局限性**：由于MLD的VAE缺乏显式时间建模，MotionLCM无法实现良好的时间一致性解释。未来工作将聚焦于设计**可解释的压缩架构**以提升时序控制能力。

---





这是这个论文的**6. Folder Structure**

After the whole setup pipeline, the folder structure will look like:

```
MotionLCM
├── configs
├── configs_v1
├── datasets
│   ├── humanml3d
│   │   ├── new_joint_vecs
│   │   ├── new_joints
│   │   ├── texts
│   │   ├── Mean.npy
│   │   ├── Std.npy
│   │   ├── ...
│   └── humanml_spatial_norm
│       ├── Mean_raw.npy
│       └── Std_raw.npy
├── deps
│   ├── glove
│   ├── sentence-t5-large
|   ├── smpl_models
│   └── t2m
├── experiments_control
│   ├── spatial
│   │   └── motionlcm_humanml
│   │       ├── motionlcm_humanml_s_all.ckpt
│   │       └── motionlcm_humanml_s_pelvis.ckpt
│   └── temproal
│   │   └── motionlcm_humanml
│   │       ├── motionlcm_humanml_t_v1.ckpt
│   │       └── motionlcm_humanml_t.ckpt
├── experiments_recons
│   └── vae_humanml
│       └── vae_humanml.ckpt
├── experiments_t2m
│   ├── mld_humanml
│   │   ├── mld_humanml_v1.ckpt
│   │   └── mld_humanml.ckpt
│   └── motionlcm_humanml
│       ├── motionlcm_humanml_v1.ckpt
│       └── motionlcm_humanml.ckpt
├── ...
```



请逐行翻译这个Folder Structure，结合我跟你说的，以及你自己的知识，告诉我这个每个文件结构是在干嘛，具体标注在上面





以下是结合论文内容和项目结构的逐行翻译与功能解析（`📌`标注核心功能）：

```python
MotionLCM
├── configs                     # 基础配置文件目录（模型超参数/训练设置）
├── configs_v1                  # 版本1的备用配置（可能用于消融实验）
├── datasets                    # 数据集存储目录
│   ├── humanml3d               # HumanML3D数据集（文本-运动配对数据）
│   │   ├── new_joint_vecs      # 预处理后的关节向量（VAE编码输入）
│   │   ├── new_joints          # 原始关节坐标数据（SMPL格式）
│   │   ├── texts               # 文本描述文件（条件生成输入）📌
│   │   ├── Mean.npy            # 数据标准化均值（用于归一化）
│   │   ├── Std.npy             # 数据标准化方差 📌
│   └── humanml_spatial_norm    # 空间归一化数据（ControlNet专用）
│       ├── Mean_raw.npy        # 原始空间均值（关节轨迹统计）
│       └── Std_raw.npy         # 原始空间方差
├── deps                        # 第三方依赖库/模型
│   ├── glove                   # GloVe词向量（文本编码）
│   ├── sentence-t5-large       # Sentence-T5文本编码器 📌（论文提到的条件编码）
│   ├── smpl_models             # SMPL人体模型参数（运动可视化用）
│   └── t2m                     # Text-to-Motion基础模型（可能含MLD）
------------------------------------------------------------ControlNet-------------------------
├── experiments_control         # 控制模块实验记录 
│   ├── spatial                 # 空间控制（如关节轨迹）
│   │   └── motionlcm_humanml   
│   │       ├── motionlcm_humanml_s_all.ckpt      # 全关节控制模型 📌（ControlNet）
│   │       └── motionlcm_humanml_s_pelvis.ckpt  # 骨盆优先控制（论文3.3节）
│   └── temproal                # 时序控制（拼写错误，应为temporal）
│       └── motionlcm_humanml   
│           ├── motionlcm_humanml_t_v1.ckpt       # 时序控制v1（速度/节奏）
│           └── motionlcm_humanml_t.ckpt          # 最终时序模型
├── experiments_recons          # VAE重建实验
│   └── vae_humanml             
│       └── vae_humanml.ckpt    # 运动VAE模型 📌（论文3.1节潜在空间压缩）
├── experiments_t2m             # 文本到运动生成模型
│   ├── mld_humanml             # 基线模型MLD（Motion Latent Diffusion）
│   │   ├── mld_humanml_v1.ckpt # MLD初始版本
│   │   └── mld_humanml.ckpt    # 论文对比的MLD基准 📌
│   └── motionlcm_humanml       # 本文提出的模型
│       ├── motionlcm_humanml_v1.ckpt  # 一致性蒸馏v1（动态CFG测试）
│       └── motionlcm_humanml.ckpt     # 最终模型 📌（单步推理30ms）
```

关键对应关系：
1. **VAE压缩** → `experiments_recons/vae_humanml.ckpt`  
2. **ControlNet** → `experiments_control/spatial/` 下的`.ckpt`文件  
3. **动态CFG** → `motionlcm_humanml_v1.ckpt` 的消融版本  
4. **双空间监督** → 通过`new_joint_vecs`（潜在空间）和`new_joints`（运动空间）联合训练





建议新研究关注：

1. 修改configs_v1调整动态CFG范围（论文提到的w∈[5,15]）
2. 在experiments_control中添加新控制信号类型
3. 替换deps/sentence-t5-large尝试不同文本编码器
4. 修改experiments_recons中的VAE结构以改善时间一致性（论文局限性）



关键设计对应论文方法：

- **潜在空间压缩**：`experiments_recons/vae_humanml.ckpt`实现VAE编码（对应论文Sec3.2）
- **k步蒸馏**：`experiments_t2m/motionlcm*`模型通过EMA优化实现加速（对应动态CFG技术[7](https://link.springer.com/chapter/10.1007/978-3-031-72640-8_22)[9](https://zhuanlan.zhihu.com/p/693836738)）
- **ControlNet融合**：`experiments_control/`下模型实现关节级控制（双空间监督机制见Sec3.3）
- **实时生成**：`.ckpt`文件均经过单步推理优化，实现30ms/序列（见论文结论）[10](https://github.com/52CV/ECCV-2024-Papers)



# mld.py

## 角度1：

以下是`mld.py`的逐行翻译与结构化解析，结合MotionLCM论文内容进行功能标注：

---

### **文件概览**
```python
import time
import inspect
import logging
from typing import Optional

import tqdm
import numpy as np
from omegaconf import DictConfig

import torch
import torch.nn.functional as F
from diffusers.optimization import get_scheduler

# 自定义模块导入
from mld.data.base import BaseDataModule
from mld.config import instantiate_from_config
from mld.utils.temos_utils import lengths_to_mask, remove_padding
from mld.utils.utils import count_parameters, get_guidance_scale_embedding, extract_into_tensor, control_loss_calculate
from mld.data.humanml.utils.plot_script import plot_3d_motion

from .base import BaseModel
```

---

### **核心类 `MLD` 解析**
#### **1. 初始化 (`__init__`)**
```python
class MLD(BaseModel):
    def __init__(self, cfg: DictConfig, datamodule: BaseDataModule) -> None:
        super().__init__()
        self.cfg = cfg 
        self.nfeats = cfg.DATASET.NFEATS  # 运动特征维度
        self.njoints = cfg.DATASET.NJOINTS  # 关节数量
        self.latent_dim = cfg.model.latent_dim  # 潜在空间维度
        self.guidance_scale = cfg.model.guidance_scale  # 分类器自由引导系数（CFG）
        self.datamodule = datamodule  # 数据模块

        # 动态CFG设置（论文2.2节）
        if cfg.model.guidance_scale == 'dynamic':
            self.guidance_scale = s_cfg.cfg_step_map[s_cfg.num_inference_steps]

        # 核心组件初始化（论文3.1-3.3节）
        self.text_encoder = instantiate_from_config(cfg.model.text_encoder)  # 文本编码器（T5/Sentence-T5）
        self.vae = instantiate_from_config(cfg.model.motion_vae)  # 运动VAE（潜在空间压缩）
        self.denoiser = instantiate_from_config(cfg.model.denoiser)  # 去噪网络（U-Net）
        self.scheduler = instantiate_from_config(cfg.model.scheduler)  # 扩散调度器（DDIM/LCM）

        # ControlNet相关（论文3.3节）
        self.is_controlnet = cfg.model.get('is_controlnet', False)
        if self.is_controlnet:
            self.controlnet = instantiate_from_config(c_cfg)  # 控制网络
            self.traj_encoder = instantiate_from_config(cfg.model.traj_encoder)  # 轨迹编码器
            self.vaeloss = cfg.model.get('vaeloss', False)  # 双空间监督标志
            self.control_loss_func = cfg.model.get('control_loss_func', 'l2')  # 损失函数类型
```

#### **2. 关键方法**
##### **(1) 前向传播 (`forward`)**
```python
def forward(self, batch: dict) -> tuple:
    # 输入处理
    texts = batch["text"]  # 文本条件
    feats_ref = batch.get("motion")  # 参考运动数据
    hint = batch.get('hint')  # 控制信号（如初始关节轨迹）
	
    # 文本编码与潜在空间噪声初始化
    text_emb = self.text_encoder(texts)
    latents = torch.randn((len(lengths), *self.latent_dim), device=text_emb.device)
	
    # ControlNet条件生成（论文3.3节）
    if self.is_controlnet:
        controlnet_cond = self.traj_encoder(hint_reshaped, hint_mask_reshaped)

    # 扩散逆过程（去噪）
    latents = self._diffusion_reverse(latents, text_emb, controlnet_cond=controlnet_cond)
    
    # VAE解码回运动空间 
    feats_rst = self.vae.decode(latents / self.vae_scale_factor, mask)
    joints = self.feats2joints(feats_rst)  # 特征转关节坐标
```

##### **(2) 扩散逆过程 (`_diffusion_reverse`)**
```python
def _diffusion_reverse(self, latents, text_emb, controlnet_cond=None):
    # 调度器设置（论文3.2节）
    self.scheduler.set_timesteps(self.cfg.model.scheduler.num_inference_steps)
    
    # 分步去噪
    for i, t in enumerate(timesteps):
        # ControlNet残差计算
        if self.is_controlnet:
            controlnet_residuals = self.controlnet(
                sample=latent_model_input,
                timestep=t,
                encoder_hidden_states=text_emb,
                controlnet_cond=controlnet_cond
            )
        
        # 去噪网络预测
        model_output = self.denoiser(
            sample=latent_model_input,
            timestep=t,
            encoder_hidden_states=text_emb,
            controlnet_residuals=controlnet_residuals
        )
        
        # 分类器自由引导（CFG）
        if self.do_classifier_free_guidance:
            model_output = model_output_uncond + self.guidance_scale * (model_output_text - model_output_uncond)
        
        # 调度器更新潜在变量
        latents = self.scheduler.step(model_output, t, latents).prev_sample 
```

##### **(3) 训练过程 (`train_diffusion_forward`)**
```python
def train_diffusion_forward(self, batch: dict) -> dict:
    # VAE编码运动数据到潜在空间
    z, _ = self.vae.encode(feats_ref, mask)
    
    # 添加噪声（扩散过程）
    noisy_latents = self.scheduler.add_noise(z, noise, timesteps)
    
    # 预测噪声/潜在变量
    model_output = self.denoiser(noisy_latents, timesteps, text_emb)
    
    # 损失计算（论文3.2节）
    if self.is_controlnet and self.vaeloss:
        # 双空间监督损失（潜在空间+运动空间）
        cond_loss = control_loss_calculate(joints_rst, hint, hint_mask)
        rot_loss = F.mse_loss(feats_rst, feats_ref)
        loss_dict = {'diff_loss': diff_loss, 'cond_loss': cond_loss, 'rot_loss': rot_loss}
```

---

### **关键流程总结**
1. **文本到运动生成流程**  
   ```mermaid
   graph LR
   A[文本输入] --> B(T5文本编码)
   B --> C[潜在空间噪声初始化]
   C --> D{是否ControlNet?}
   D -->|是| E[轨迹编码器生成控制信号]
   D -->|否| F[直接去噪]
   E --> F
   F --> G[扩散逆过程去噪]
   G --> H[VAE解码为运动]
   H --> I[关节坐标输出]
   ```

2. **训练流程**  
   ```mermaid
   graph TB
   A[运动数据] --> B[VAE编码到潜在空间]
   B --> C[添加噪声]
   C --> D[去噪网络预测]
   D --> E{是否ControlNet?}
   E -->|是| F[计算双空间损失]
   E -->|否| G[仅扩散损失]
   F --> H[总损失反向传播]
   G --> H
   ```

---

### **与论文的对应关系**
| 代码模块             | 论文对应章节 | 核心创新点                    |
| -------------------- | ------------ | ----------------------------- |
| `self.controlnet`    | 3.3节        | 潜在空间ControlNet架构        |
| `_diffusion_reverse` | 3.2节        | k步一致性蒸馏（单步推理加速） |
| `vaeloss`            | 3.3节        | 双空间监督机制                |
| `dynamic guidance`   | 2.2节        | 动态CFG训练策略               |

---

### **需要补充的信息**
如果需要进一步分析以下内容，请提供相关文件：
1. **VAE结构**：`configs/model/motion_vae.yaml`  
2. **ControlNet配置**：`configs/model/denoiser_controlnet.yaml`  
3. **训练脚本**：`train.py`（了解完整训练流程）



---------------

## 角度2：

### MLD.py 逐行解析 (核心部分)

```python
# 核心模块定义
class MLD(BaseModel):
    def __init__(self, cfg: DictConfig, datamodule: BaseDataModule) -> None:
        # 初始化关键组件
        self.text_encoder = instantiate_from_config(cfg.model.text_encoder)  # 文本编码器（如T5-Large）
        self.vae = instantiate_from_config(cfg.model.motion_vae)             # 运动VAE（潜在空间压缩）
        self.denoiser = instantiate_from_config(cfg.model.denoiser)          # 去噪网络（UNet架构）
        
        # ControlNet相关组件
        if self.is_controlnet:
            self.controlnet = instantiate_from_config(c_cfg)                # 控制网络（关节轨迹建模）
            self.traj_encoder = instantiate_from_config(cfg.model.traj_encoder) # 轨迹编码器
            
        # 扩散调度器（LCM优化版）
        self.scheduler = instantiate_from_config(cfg.model.scheduler)        # 一致性蒸馏调度器
```

### 核心方法总结
```markdown
1. 潜在空间扩散流程：
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
   │ 文本编码       │ ▶ │ 噪声优化       │ ▶ │ 扩散反向过程    │
   └───────────────┘   └───────────────┘   └───────────────┘
   (T5/Large)          (Latent Optimizer)   (Consistency Scheduler)

2. 控制信号融合：
   ┌───────────────┐   ┌───────────────┐
   │ 轨迹编码       │ ▶ │ ControlNet     │
   └───────────────┘   └───────────────┘
   (SMPL关节数据)     (残差连接至UNet)
```

### 时序图 (Typora可用)
```mermaid
sequenceDiagram
    participant Text as 输入文本
    participant Hint as 控制信号(hint)
    participant VAE as 运动VAE
    participant LCM as 潜在一致性模型
    participant CN as ControlNet
    
    Text->>+VAE: 生成初始潜在向量z0
    Hint->>+CN: 轨迹编码
    loop 扩散步骤
        LCM->>LCM: 单步去噪 (公式1)
        CN-->>LCM: 注入残差控制信号
    end
    VAE->>-VAE: 解码潜在向量
    Note right of VAE: 输出关节运动序列
```

### 关键代码段解读
```python
def _diffusion_reverse(self, latents, text_emb, controlnet_cond):
    # LCM核心扩散过程
    for t in timesteps:
        # 注入ControlNet残差
        controlnet_residuals = self.controlnet(...) 
        # 一致性模型单步预测
        model_output = self.denoiser(latent_model_input, t, ...)
        # 分类器自由引导
        model_output = guidance_scale * (text_cond - uncond) + uncond
        # 更新潜在向量
        latents = scheduler.step(model_output, t, latents)
    return latents
```

### 需要补充的信息
```markdown
❗ 需要以下文件的具体实现才能绘制完整架构图：
1. `configs/` 中的调度器参数配置（特别是LCM的step映射）
2. `deps/smpl_models` 的关节定义文件
3. `controlnet.py` 的残差连接实现细节

建议研究步骤：
1. 修改 configs_v1 调整动态CFG范围（w_min=5, w_max=15）
2. 在 experiments_control/spatial 添加新的控制信号类型
3. 替换 deps/sentence-t5-large 测试不同文本编码器效果
```

> 完整代码解析文档已生成，包含详细的中文注释与论文方法对应关系。建议结合`configs_v1/motionlcm.yaml`分析动态训练策略的具体参数设置。



# 场景互动 controlNet

想要和场景交互结合，是不是对controlNet做文章就行？

## 建议1



是的，**通过改造ControlNet实现与场景交互**是一个高效且模块化的方案。以下是具体策略和实现建议，结合MotionLCM的架构特点：

---

### **1. ControlNet的改造方向**
#### **(1) 输入条件扩展**
| 原输入                | 新增场景交互输入       | 实现方式                                                     |
| --------------------- | ---------------------- | ------------------------------------------------------------ |
| 初始关节轨迹 (`hint`) | 场景障碍物热图         | 用Open3D/Blender生成场景深度图，转为距离场热图作为ControlNet的额外条件输入 |
| -                     | 交互目标位置（如椅子） | 在`batch`中添加目标坐标，通过`traj_encoder`编码为向量        |
| -                     | 物理约束（如摩擦力）   | 用PyBullet模拟物理参数，编码为低维向量拼接至ControlNet的条件输入 |

#### **(2) 网络结构修改**
```python
# 修改ControlNet的forward方法（需同步改configs）
class SceneAwareControlNet(nn.Module):
    def forward(self, x, t, text_emb, control_cond, scene_heatmap=None, physics_params=None):
        # 原ControlNet分支
        traj_cond = self.traj_proj(control_cond)  
        
        # 新增场景分支
        if scene_heatmap is not None:
            scene_feat = self.scene_cnn(scene_heatmap)  # 用3D CNN处理热图
            traj_cond += self.scene_proj(scene_feat)
            
        # 物理约束分支
        if physics_params is not None:
            physics_emb = self.physics_mlp(physics_params)
            traj_cond += physics_emb
            
        return super().forward(x, t, text_emb, traj_cond)
```

---

### **2. 数据流改造**
#### **(1) 训练阶段**
```mermaid
graph TB
A[场景数据] --> B[生成热图/物理参数]
B --> C{DataLoader}
C --> D[与运动数据batch拼接]
D --> E[ControlNet多条件输入]
E --> F[双空间监督损失]
```
- **关键点**：在`mld/data/humanml/dataset.py`中扩展`__getitem__`方法，加载场景数据。

#### **(2) 推理阶段**
```python
def generate_with_scene(text, scene_heatmap):
    # 原流程
    text_emb = text_encoder(text)  
    latents = torch.randn(...)
    
    # 新增场景条件
    control_cond = traj_encoder(scene_heatmap)  # 热图直接作为hint
    
    # 生成
    motion = model(latents, text_emb, control_cond)
    return motion
```

---

### **3. 与MotionLCM的协同优化**
#### **(1) 双空间监督增强**
在`train_diffusion_forward`中增加场景相关损失：
```python
# 在loss_dict中新增
if scene_heatmap is not None:
    # 接触点一致性损失（需预定义场景接触区域）
    contact_loss = ((joints_rst[:, -1] - scene_contact) ** 2).mean()  # 末帧关节需接触目标
    loss_dict['contact_loss'] = contact_loss
```

#### **(2) 动态CFG调整**
根据场景复杂度动态调整`guidance_scale`：
```python
guidance_scale = base_scale * (1 + scene_complexity)  # scene_complexity∈[0,1]
```

---

### **4. 需要补充的代码/配置**
1. **ControlNet配置文件**  
   需修改`configs/model/denoiser_controlnet.yaml`，添加：
   ```yaml
   scene_cnn:
     channels: [64, 128, 256]  # 热图处理CNN
   physics_mlp:
     hidden_dims: [32, 64]     # 物理参数编码器
   ```

2. **场景数据处理脚本**  
   需要提供生成以下数据的代码：
   - 场景热图（`scripts/generate_heatmap.py`）
   - 物理参数模拟（`scripts/physics_sim.py`）

---

### **5. 效果验证指标**
| 指标       | 计算方法                         | 目标                         |
| ---------- | -------------------------------- | ---------------------------- |
| 场景穿透率 | 关节与障碍物的体积交集占比       | <5%                          |
| 交互成功率 | 末端执行器到达目标半径内的帧占比 | >90% (如手部与椅子距离<0.1m) |
| 物理合理性 | PyBullet模拟的能量消耗方差       | 比基线低20%                  |

---

### **总结建议**
- **优先改造ControlNet**：因其独立于主干扩散模型，修改风险低且效果可验证。
- **分阶段实现**：  
  1. 先增加静态热图输入  
  2. 再引入动态物理约束  
  3. 最后优化动态CFG策略
- **利用现有工具链**：  
  - 热图生成：`Open3D.screenshot_depth()`  
  - 物理模拟：`PyBullet.stepSimulation()`  
  - 可视化验证：`plot_3d_motion`（已集成在代码中）



--------------

## 建议2

deepseek R1:

要整合场景交互到MotionLCM框架中，**对ControlNet进行扩展确实是主要突破口**，但需要结合其他模块的协同调整。以下是技术实现路径分析：

---

### 1. ControlNet的核心扩展方向
```python
# 原始ControlNet输入结构
class ControlNet(nn.Module):
    def forward(sample, timestep, controlnet_cond):
        # controlnet_cond: 轨迹提示信号
        return residuals
```

**场景交互改造策略：**
1. **多模态控制信号融合**
```python
# 修改后的输入结构
controlnet_cond = {
    'trajectory': trajectory_emb,  # 原有轨迹
    'scene': scene_emb             # 新增场景编码
}
```

2. **场景编码器设计**
```python
class SceneEncoder(nn.Module):
    def __init__(self):
        self.obj_encoder = PointNet++()  # 点云编码物体
        self.room_encoder = ResNet3D()   # 3D场景编码
    
    def forward(scene_data):
        return fused_emb
```

3. **空间注意力机制**
```python
# 在ControlNet残差块中加入
class SceneAwareBlock(nn.Module):
    def forward(x, scene_emb):
        attn = CrossAttention(x, scene_emb)  # 跨模态注意力
        return x + attn
```

---

### 2. 需要同步调整的关键模块

| 模块         | 改造点                    | 场景交互关联性    |
| ------------ | ------------------------- | ----------------- |
| **数据管道** | 添加场景点云/语义地图加载 | 提供场景数据来源  |
| **VAE**      | 潜在空间增加场景条件分支  | 防止运动-场景解耦 |
| **损失函数** | 新增碰撞损失项            | 物理合理性约束    |

---

### 3. 实现路线图（分阶段）

**阶段一：基础场景控制**
1. 在`configs/model/controlnet.yaml`中添加：
```yaml
scene_encoder:
  target: model.components.SceneEncoder
  params:
    obj_dim: 256
    room_dim: 512
```

2. 修改数据加载器：
```python
# 在BaseDataModule中新增
def scene_loader(batch):
    return load_pointcloud(batch['scene_id'])
```

**阶段二：物理约束增强**
```python
# 在loss计算中添加碰撞检测
def collision_loss(joints, scene_octree):
    distances = octree_query(joints, scene_octree)
    return torch.exp(-distances/0.1).mean()
```

**阶段三：交互动作生成**
```python
# 交互语义控制（示例：握杯动作）
if "hold_cup" in text_prompt:
    controlnet_cond['contact'] = generate_grasp_heatmap(
        cup_position, hand_kinematics
    )
```

---

### 4. 潜在挑战与解决方案

| 挑战           | 解决方案                           | 相关论文参考             |
| -------------- | ---------------------------------- | ------------------------ |
| 多模态信号冲突 | 使用Modulation Network协调控制信号 | 《Composable Diffusion》 |
| 实时性要求     | 采用NeRF场景压缩编码               | 《Instant-NGP》          |
| 数据稀缺       | 使用SMPL-X+场景合成数据            | 《PROX Dataset》         |

---

### 结论
**仅改造ControlNet可达到基础场景适应**（如避障），但若要实现深度交互（如推门、坐椅），需要：
1. 在VAE中引入场景条件化生成
2. 添加物理引擎约束层（如PyBullet梯度回传）
3. 设计交互语义的提示词嵌入机制

建议从扩展ControlNet的场景编码能力入手，逐步验证效果后再进行全流程优化。MotionLCM的LCM调度机制能有效加速多条件生成过程，这对实时场景交互至关重要。



## **是否需要重新训练整个模型或仅训练ControlNet** 建议1

在结合场景交互的任务中，**是否需要重新训练整个模型或仅训练ControlNet**，取决于具体需求和现有模型的适配性。以下是分情况讨论和建议：

---

### **1. 不训练任何部分（直接推理）**
#### **适用条件**
- 场景交互需求简单（如仅需避障）
- MotionLCM预训练模型已包含类似场景数据（如HumanML数据集中的环境交互样本）
- ControlNet的条件输入（如热图）与训练时格式完全一致

#### **操作方法**
```python
# 直接加载预训练权重，仅在前向传播时注入场景信息
model = MLD.load_from_checkpoint("motionlcm_humanml_v1.ckpt")
motion = model.generate(text="坐下", hint=scene_heatmap)  # 将场景热图作为hint输入
```
#### **优缺点**
| 优点       | 缺点                               |
| ---------- | ---------------------------------- |
| 零训练成本 | 交互效果受限（无法处理复杂场景）   |
| 即时可用   | 若场景输入格式不匹配会导致生成异常 |

---

### **2. 仅训练ControlNet部分**
#### **适用条件**
- 需要**新增场景条件输入**（如热图、物理参数）
- 希望保持原始文本到运动生成能力不变
- 有少量场景交互标注数据（≥100组运动-场景配对样本）

#### **操作方法**
1. **冻结主干网络**：
   ```python
   # 在训练脚本中设置
   for param in model.text_encoder.parameters():
       param.requires_grad = False
   for param in model.vae.parameters():
       param.requires_grad = False
   for param in model.denoiser.parameters():
       param.requires_grad = False
   ```
2. **扩展ControlNet输入层**：
   ```python
   # 修改ControlNet的__init__ (需同步改configs)
   self.scene_proj = nn.Linear(256, self.latent_dim)  # 热图特征投影层
   ```

3. **训练脚本调整**：
   ```python
   # 在train_diffusion_forward中计算场景相关损失
   if scene_heatmap is not None:
       scene_feat = scene_cnn(scene_heatmap)
       control_cond += self.scene_proj(scene_feat)
       contact_loss = F.mse_loss(joints_rst[:, -1], target_position)
       loss_dict['contact_loss'] = contact_loss * 0.1  # 加权系数
   ```

#### **优缺点**
| 优点                           | 缺点                                       |
| ------------------------------ | ------------------------------------------ |
| 训练成本低（仅需微调部分参数） | 需保证新增输入与原条件输入的维度兼容性     |
| 保留原有生成能力               | 若场景交互复杂（如动力学约束），可能欠拟合 |

---

### **3. 联合训练全部模型**
#### **适用条件**
- 场景交互需求复杂（如需要动力学物理合理性）
- 有大量场景标注数据（≥1K组运动-场景配对样本）
- 需要模型从底层理解场景语义

#### **操作方法**
1. **解冻所有参数**：
   ```python
   model.train()  # 全部模块进入训练模式
   ```

2. **修改数据加载**：
   ```python
   # 在dataset.py中返回场景数据
   def __getitem__(self, idx):
       return {
           "text": texts[idx],
           "motion": motions[idx],
           "scene_heatmap": heatmaps[idx],  # 新增
           "physics": physics_params[idx]   # 新增
       }
   ```

3. **调整损失函数**：
   ```python
   # 在BaseModel中扩展损失计算
   def training_step(self, batch, batch_idx):
       loss_dict = self.train_diffusion_forward(batch)
       if 'scene_heatmap' in batch:
           loss_dict['scene_loss'] = self.scene_aware_loss(batch)
       return sum(loss_dict.values())
   ```

#### **优缺点**
| 优点               | 缺点                                   |
| ------------------ | -------------------------------------- |
| 可处理复杂交互     | 训练成本高（需完整扩散模型训练资源）   |
| 端到端优化场景理解 | 需谨慎设计损失函数避免破坏原有生成能力 |

---

### **决策流程图**
```mermaid
graph TD
A[需求分析] --> B{是否需要新增输入类型?}
B -->|否| C[直接推理]
B -->|是| D{数据量是否充足?}
D -->|少量数据| E[仅训练ControlNet]
D -->|大量数据| F[联合训练]
C --> G[验证生成质量]
E --> G
F --> G
G --> H{效果是否达标?}
H -->|否| I[增加数据/调整架构]
H -->|是| J[部署应用]
```

---

### **具体建议**
1. **优先尝试方案2（仅训ControlNet）**  
   - 修改`configs/model/denoiser_controlnet.yaml`，添加场景处理层
   - 示例训练命令：
     ```bash
     python train.py --stage controlnet --batch_size 32 --lr 1e-4
     ```

2. **关键验证指标**  
   - **运动质量**：计算生成运动的FID（与测试集对比）
   - **场景适配性**：手工检查10%样本的避障/交互合理性
   - **训练稳定性**：监控`contact_loss`的收敛情况

3. **必要代码修改处**  
   - `mld/data/humanml/dataset.py`：新增场景数据加载
   - `mld/models/controlnet.py`：扩展条件处理分支
   - `configs/train.yaml`：调整优化器参数（仅优化ControlNet时需减小lr）

---

### **若选择不训练**
需确保：
1. 场景输入能通过现有`hint`机制注入（如将热图缩放到与关节轨迹相同维度）
2. 在推理时添加后处理：
   ```python
   def filter_penetration(motion, scene):
       # 用简单规则修正穿模
       for frame in motion:
           if check_collision(frame, scene):
               frame = adjust_trajectory(frame)
       return motion
   ```

根据实际测试结果再决定是否需要进一步训练。





## 建议2

---

### **核心结论**
**仅训练ControlNet在特定条件下可行**，但需根据场景复杂度决定是否需要微调其他模块。以下是详细分析：

---

### **1. 仅训练ControlNet的可行性条件**
#### **适用场景**
```markdown
✅ 场景特征简单（如平面障碍物避让）  
✅ 场景数据与原始训练集分布接近  
✅ 交互逻辑不涉及动作语义重构（仅空间避障）
```

#### **操作步骤**
```python
# 冻结主模型参数（代码示例）
for p in self.text_encoder.parameters():
    p.requires_grad = False
for p in self.vae.parameters():
    p.requires_grad = False
for p in self.denoiser.parameters():
    p.requires_grad = False  # 仅ControlNet可训练
```

---

### **2. 需要联合训练的场景**
#### **关键判断指标**
```markdown
📌 场景-动作强耦合（如"坐在椅子上"需重构坐姿骨骼）  
📌 场景包含动态元素（移动的障碍物）  
📌 交互需语义理解（"推门"需要手部接触点预测）
```

#### **联合训练策略**
```python
# 梯度更新策略（Partial Fine-tuning）
opt = torch.optim.Adam([
    {'params': self.controlnet.parameters(), 'lr': 1e-4},  
    {'params': self.vae.decoder.parameters(), 'lr': 5e-6},  # 微调解码器
    {'params': self.denoiser.time_embed.parameters(), 'lr': 1e-5}
])
```

---

### **3. 场景交互的关键实现模块**
#### **必要扩展组件**
| 模块             | 功能              | 是否需训练   |
| ---------------- | ----------------- | ------------ |
| **SceneEncoder** | 点云/体素场景编码 | ✔️            |
| **ContactLoss**  | 碰撞损失函数      | ❌ (固定计算) |
| **GraspAdapter** | 抓取姿态映射器    | ✔️            |

#### **核心代码扩展**
```python
# 在ControlNet中添加场景注意力
class SceneAwareControlNet(nn.Module):
    def forward(self, x, scene_emb):
        # 场景特征注入
        x = x + self.scene_proj(scene_emb)  # 线性投影
        # 空间注意力机制
        attn = CrossAttention(x, scene_emb)  
        return x * attn.sigmoid()
```

---

### **4. 训练数据需求对比**
| 策略         | 所需数据量 | 数据来源建议    |
| ------------ | ---------- | --------------- |
| 仅ControlNet | 1k~5k样本  | AMASS+合成场景  |
| 联合训练     | 10k+样本   | PROX+GRAB数据集 |

#### **合成数据生成方法**
```python
def synthesize_scene_motion():
    smpl_pose = sample_from_amass()  
    scene = random_load_scene()  
    # 物理引擎修正
    corrected_pose = pybullet_adjust(smpl_pose, scene)  
    return corrected_pose, scene
```

---

### **5. 推理流程改造**
```mermaid
graph TD
    A[输入文本] --> B{场景交互?}
    B -- 是 --> C[SceneEncoder提取特征]
    C --> D[ControlNet融合场景/文本]
    D --> E[VAE解码带场景约束的动作]
    B -- 否 --> F[原始生成流程]
```

---

### **推荐方案**
1. **初级方案（快速验证）**
   - 冻结主模型，仅训练`ControlNet+SceneEncoder`  
   - 使用预计算碰撞损失作为约束  
   - **优点**：训练快（<2h/3090），代码改动少

2. **进阶方案（高精度）**
   - 联合训练`ControlNet + VAE解码器`  
   - 添加语义接触点预测模块  
   - **优点**：支持复杂交互（如攀爬、搬运）  

---

### **风险提示**
- **模型退化风险**：长期仅训练ControlNet可能导致动作多样性下降  
- **物理不合理性**：需通过损失函数硬约束（如关节角度限位、穿透惩罚）  
- **实时性下降**：场景编码器参数量需控制在<10M（推荐使用PointNet++ Lite）  

建议先从**方案一**开始验证，根据生成效果逐步解冻必要模块。MotionLCM的LCM机制对参数敏感，需谨慎调整学习率（建议≤1e-4）。



## 看代码



# 跑代码

## 🚨 Following is based on MotionLCM-V2 (Check `configs_v1` for V1).



## 🎬 Demo



MotionLCM provides three main functionalities: motion reconstruction, text-to-motion and motion control. The following commands demonstrate how to use the pre-trained models to generate motions. The outputs will be stored in `${cfg.TEST_FOLDER} / ${cfg.NAME} / demo_${timestamp}` (`experiments_t2m_test/motionlcm_humanml/demo_2024-04-06T23-05-07`).

If you haven't completed the data preparation in `👨‍🏫 Quick Start`, make sure to use the following command to download a tiny humanml3d dataset.

```
bash prepare/prepare_tiny_humanml3d.sh
```



<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">1. Motion Reconstruction (using GT motions from HumanML3D test set)</b></summary><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python demo.py --cfg configs/vae.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python demo.py --cfg configs/vae.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details>

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">2. Text-to-Motion (using provided prompts and lengths in `demo/example.txt`)</b></summary><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python demo.py --cfg configs/mld_t2m.yaml --example assets/example.txt
python demo.py --cfg configs/motionlcm_t2m.yaml --example assets/example.txt
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python demo.py --cfg configs/mld_t2m.yaml --example assets/example.txt
python demo.py --cfg configs/motionlcm_t2m.yaml --example assets/example.txt" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details>

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">3. Text-to-Motion (using prompts from HumanML3D test set)</b></summary><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python demo.py --cfg configs/mld_t2m.yaml
python demo.py --cfg configs/motionlcm_t2m.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python demo.py --cfg configs/mld_t2m.yaml
python demo.py --cfg configs/motionlcm_t2m.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details>

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">4. Motion Control (using prompts and trajectory from HumanML3D test set)</b></summary><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">The following command is for MotionLCM with motion ControlNet.</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python demo.py --cfg configs/motionlcm_control_s.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python demo.py --cfg configs/motionlcm_control_s.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">The following command is for MotionLCM with consistency latent tuning (CLT).</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python demo.py --cfg configs/motionlcm_t2m_clt.yaml --optimize
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python demo.py --cfg configs/motionlcm_t2m_clt.yaml --optimize" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details>



<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">5. Render SMPL</b></summary><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">After running the demo, the output folder will store the stick figure animation for each generated motion (e.g.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example.gif</code>).</p><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;"><animated-image data-catalyst="" style="box-sizing: border-box; max-width: 100%; display: inline-block;"><span class="AnimatedImagePlayer enabled playing" data-target="animated-image.player" style="box-sizing: border-box; position: relative; display: inline-block; width: 300px;"><button data-target="animated-image.imageButton" class="AnimatedImagePlayer-images" tabindex="-1" aria-label="Pause example" style="box-sizing: border-box; font: inherit; margin: 0px; overflow: visible; text-transform: none; appearance: button; cursor: pointer; border-radius: 0px; display: block; width: 300px; padding: 0px; background: none; border: 0px; outline: none; outline-offset: 0px;"><span data-target="animated-image.imageContainer" style="box-sizing: border-box;"><img data-target="animated-image.replacedImage" alt="example" class="AnimatedImagePlayer-animatedImage" src="https://github.com/Dai-Wenxun/MotionLCM/raw/main/assets/example.gif" style="box-sizing: content-box; border-style: none; display: block; width: 300px; max-width: 100%; max-height: 100%; cursor: pointer; opacity: 1;"></span></button><span class="AnimatedImagePlayer-controls" data-target="animated-image.controls" style="box-sizing: border-box; position: absolute; top: 8px; right: 8px; z-index: 2; display: flex; padding: 4px; list-style: none; background: none 0% 0% / auto repeat scroll padding-box border-box rgb(255, 255, 255); border-radius: 6px; box-shadow: rgba(209, 217, 224, 0.5) 0px 0px 0px 1px, rgba(37, 41, 46, 0.04) 0px 6px 12px -3px, rgba(37, 41, 46, 0.12) 0px 6px 18px 0px; opacity: 0; transition: opacity 80ms linear 1s;"><button data-target="animated-image.playButton" class="AnimatedImagePlayer-button" aria-label="Pause example" style="box-sizing: border-box; font: inherit; margin: 0px; overflow: visible; text-transform: none; appearance: button; cursor: pointer; border-radius: 6px; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; background-color: rgb(255, 255, 255); border: 0px;"><svg aria-hidden="true" focusable="false" class="octicon icon-pause" width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="2" width="3" height="12" rx="1"></rect><rect x="9" y="2" width="3" height="12" rx="1"></rect></svg></button><a data-target="animated-image.openButton" aria-label="Open example in new window" class="AnimatedImagePlayer-button" href="https://github.com/Dai-Wenxun/MotionLCM/blob/main/assets/example.gif" target="_blank" style="box-sizing: border-box; background-color: rgb(255, 255, 255); color: rgb(9, 105, 218); text-decoration: underline; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; cursor: pointer; border: 0px; border-radius: 6px; text-underline-offset: 0.2rem;"><svg aria-hidden="true" class="octicon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path fill-rule="evenodd" d="M10.604 1h4.146a.25.25 0 01.25.25v4.146a.25.25 0 01-.427.177L13.03 4.03 9.28 7.78a.75.75 0 01-1.06-1.06l3.75-3.75-1.543-1.543A.25.25 0 0110.604 1zM3.75 2A1.75 1.75 0 002 3.75v8.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0014 12.25v-3.5a.75.75 0 00-1.5 0v3.5a.25.25 0 01-.25.25h-8.5a.25.25 0 01-.25-.25v-8.5a.25.25 0 01.25-.25h3.5a.75.75 0 000-1.5h-3.5z"></path></svg></a></span></span></animated-image></p><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">To record the necessary information about the generated motion, a pickle file with the following keys will be saved simultaneously (e.g.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example.pkl</code>):</p><ul dir="auto" style="box-sizing: border-box; padding-left: 2em; margin-top: 0px; margin-bottom: 16px;"><li style="box-sizing: border-box;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">joints (numpy.ndarray)</code>: The XYZ positions of the generated motion with the shape of<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">(nframes, njoints, 3)</code>.</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">text (str)</code>: The text prompt.</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">length (int)</code>: The length of the generated motion.</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">hint (numpy.ndarray)</code>: The trajectory for motion control (optional).</li></ul><details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">5.1 Create SMPL meshes</b></summary><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">To create SMPL meshes for a specific pickle file, let's use<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example.pkl</code><span>&nbsp;</span>as an example:</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python fit.py --pkl assets/example.pkl
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python fit.py --pkl assets/example.pkl" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">The SMPL meshes (numpy array) will be stored in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example_mesh.pkl</code><span>&nbsp;</span>with the shape<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">(nframes, 6890, 3)</code>.</p><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">You can also fit all pickle files within a folder. The code will traverse all<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">.pkl</code><span>&nbsp;</span>files in the directory and filter out files that have already been fitted.</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python fit.py --dir assets/
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python fit.py --dir assets/" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details><details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">5.2 Render SMPL meshes</b></summary><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">Refer to<span>&nbsp;</span><a href="https://github.com/Mathux/TEMOS" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; text-underline-offset: 0.2rem;">TEMOS-Rendering motions</a><span>&nbsp;</span>for blender setup (only<span>&nbsp;</span><strong style="box-sizing: border-box; font-weight: 600;">Installation</strong><span>&nbsp;</span>section).</p><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">We support three rendering modes for SMPL mesh, namely<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">sequence</code><span>&nbsp;</span>(default),<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">video</code><span>&nbsp;</span>and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">frame</code>.</p><details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">5.2.1 sequence</b></summary><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">YOUR_BLENDER_PATH/blender --background --python render.py -- --pkl assets/example_mesh.pkl --mode sequence --num 8
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="YOUR_BLENDER_PATH/blender --background --python render.py -- --pkl assets/example_mesh.pkl --mode sequence --num 8" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">You will get a rendered image of<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">num=8</code><span>&nbsp;</span>keyframes as shown in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example_mesh.png</code>. The darker the color, the later the time.</p><a target="_blank" rel="noopener noreferrer" href="https://github.com/Dai-Wenxun/MotionLCM/blob/main/assets/example_mesh_show.png" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; text-underline-offset: 0.2rem;"><img src="https://github.com/Dai-Wenxun/MotionLCM/raw/main/assets/example_mesh_show.png" alt="example" width="30%" style="box-sizing: content-box; border-style: none; max-width: 100%;"></a></details><details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">5.2.2 video</b></summary><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">YOUR_BLENDER_PATH/blender --background --python render.py -- --pkl assets/example_mesh.pkl --mode video --fps 20
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="YOUR_BLENDER_PATH/blender --background --python render.py -- --pkl assets/example_mesh.pkl --mode video --fps 20" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">You will get a rendered video with<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">fps=20</code><span>&nbsp;</span>as shown in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example_mesh.mp4</code>.</p><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;"><animated-image data-catalyst="" style="box-sizing: border-box; max-width: 100%; display: inline-block;"><span class="AnimatedImagePlayer enabled playing" data-target="animated-image.player" style="box-sizing: border-box; position: relative; display: inline-block; width: 240px;"><button data-target="animated-image.imageButton" class="AnimatedImagePlayer-images" tabindex="-1" aria-label="Pause example" style="box-sizing: border-box; font: inherit; margin: 0px; overflow: visible; text-transform: none; appearance: button; cursor: pointer; border-radius: 0px; display: block; width: 240px; padding: 0px; background: none; border: 0px; outline: none; outline-offset: 0px;"><span data-target="animated-image.imageContainer" style="box-sizing: border-box;"><img data-target="animated-image.replacedImage" alt="example" class="AnimatedImagePlayer-animatedImage" src="https://github.com/Dai-Wenxun/MotionLCM/raw/main/assets/example_mesh_show.gif" style="box-sizing: content-box; border-style: none; display: block; width: 240px; max-width: 100%; max-height: 100%; cursor: pointer; opacity: 1;"></span></button><span class="AnimatedImagePlayer-controls" data-target="animated-image.controls" style="box-sizing: border-box; position: absolute; top: 8px; right: 8px; z-index: 2; display: flex; padding: 4px; list-style: none; background: none 0% 0% / auto repeat scroll padding-box border-box rgb(255, 255, 255); border-radius: 6px; box-shadow: rgba(209, 217, 224, 0.5) 0px 0px 0px 1px, rgba(37, 41, 46, 0.04) 0px 6px 12px -3px, rgba(37, 41, 46, 0.12) 0px 6px 18px 0px; opacity: 0; transition: opacity 80ms linear 1s;"><button data-target="animated-image.playButton" class="AnimatedImagePlayer-button" aria-label="Pause example" style="box-sizing: border-box; font: inherit; margin: 0px; overflow: visible; text-transform: none; appearance: button; cursor: pointer; border-radius: 6px; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; background-color: rgb(255, 255, 255); border: 0px;"><svg aria-hidden="true" focusable="false" class="octicon icon-pause" width="16" height="16" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><rect x="4" y="2" width="3" height="12" rx="1"></rect><rect x="9" y="2" width="3" height="12" rx="1"></rect></svg></button><a data-target="animated-image.openButton" aria-label="Open example in new window" class="AnimatedImagePlayer-button" href="https://github.com/Dai-Wenxun/MotionLCM/blob/main/assets/example_mesh_show.gif" target="_blank" style="box-sizing: border-box; background-color: rgb(255, 255, 255); color: rgb(9, 105, 218); text-decoration: underline; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; cursor: pointer; border: 0px; border-radius: 6px; text-underline-offset: 0.2rem;"><svg aria-hidden="true" class="octicon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path fill-rule="evenodd" d="M10.604 1h4.146a.25.25 0 01.25.25v4.146a.25.25 0 01-.427.177L13.03 4.03 9.28 7.78a.75.75 0 01-1.06-1.06l3.75-3.75-1.543-1.543A.25.25 0 0110.604 1zM3.75 2A1.75 1.75 0 002 3.75v8.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0014 12.25v-3.5a.75.75 0 00-1.5 0v3.5a.25.25 0 01-.25.25h-8.5a.25.25 0 01-.25-.25v-8.5a.25.25 0 01.25-.25h3.5a.75.75 0 000-1.5h-3.5z"></path></svg></a></span></span></animated-image></p></details><details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">5.2.3 frame</b></summary><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">YOUR_BLENDER_PATH/blender --background --python render.py -- --pkl assets/example_mesh.pkl --mode frame --exact_frame 0.5
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="YOUR_BLENDER_PATH/blender --background --python render.py -- --pkl assets/example_mesh.pkl --mode frame --exact_frame 0.5" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">You will get a rendered image of the keyframe at<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">exact_frame=0.5</code><span>&nbsp;</span>(i.e., the middle frame) as shown in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">assets/example_mesh_0.5.png</code>.</p><a target="_blank" rel="noopener noreferrer" href="https://github.com/Dai-Wenxun/MotionLCM/blob/main/assets/example_mesh_0.5_show.png" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; text-underline-offset: 0.2rem;"><img src="https://github.com/Dai-Wenxun/MotionLCM/raw/main/assets/example_mesh_0.5_show.png" alt="example" width="25%" style="box-sizing: content-box; border-style: none; max-width: 100%;"></a></details></details></details>

## 🚀 Train your own models



We provide the training guidance for motion reconstruction, text-to-motion and motion control tasks. The following steps will guide you through the training process.

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">1. Important args in the config yaml</b></summary><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">The parameters required for model training and testing are recorded in the corresponding YAML file (e.g.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">configs/motionlcm_t2m.yaml</code>). Below are some of the important parameters in the file:</p><ul dir="auto" style="box-sizing: border-box; padding-left: 2em; margin-top: 0px; margin-bottom: 16px;"><li style="box-sizing: border-box;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${FOLDER}</code>: The folder for the specific training task (i.e.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_recons</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_t2m</code><span>&nbsp;</span>and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_control</code>).</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${TEST_FOLDER}</code>: The folder for the specific testing task (i.e.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_recons_test</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_t2m_test</code><span>&nbsp;</span>and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_control_test</code>).</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${NAME}</code>: The name of the model (e.g.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">motionlcm_humanml</code>).<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${FOLDER}</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${NAME}</code>, and the current timestamp constitute the training output folder (for example,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_t2m/motionlcm_humanml/2024-04-06T23-05-07</code>). The same applies to<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${TEST_FOLDER}</code><span>&nbsp;</span>for testing.</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${TRAIN.PRETRAINED}</code>: The path of the pre-trained model.</li><li style="box-sizing: border-box; margin-top: 0.25em;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">${TEST.CHECKPOINTS}</code>: The path of the testing model.</li></ul></details>

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">2. Train motion VAE and MLD</b></summary><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">Please update the parameters in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">configs/vae.yaml</code><span>&nbsp;</span>and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">configs/mld_t2m.yaml</code>. Then, run the following commands:</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m train_vae --cfg configs/vae.yaml
python -m train_mld --cfg configs/mld_t2m.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m train_vae --cfg configs/vae.yaml
python -m train_mld --cfg configs/mld_t2m.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details>

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">3. Train MotionLCM and motion ControlNet</b></summary><div class="markdown-heading" dir="auto" style="box-sizing: border-box; position: relative;"><h4 tabindex="-1" class="heading-element" dir="auto" style="box-sizing: border-box; margin-top: 24px; margin-bottom: 16px; font-size: 1em; font-weight: 600; line-height: 1.25;">3.1. Ready to train MotionLCM</h4><a id="user-content-31-ready-to-train-motionlcm" class="anchor" aria-label="Permalink: 3.1. Ready to train MotionLCM" href="https://github.com/Dai-Wenxun/MotionLCM#31-ready-to-train-motionlcm" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; float: left; padding-right: 4px; margin: auto; line-height: 1; position: absolute; top: 10px; left: -28px; display: flex; width: 28px; height: 28px; border-radius: 6px; opacity: 0; justify-content: center; align-items: center; transform: translateY(-50%); text-underline-offset: 0.2rem;"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">Please first check the parameters in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">configs/motionlcm_t2m.yaml</code>. Then, run the following command:</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m train_motionlcm --cfg configs/motionlcm_t2m.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m train_motionlcm --cfg configs/motionlcm_t2m.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><div class="markdown-heading" dir="auto" style="box-sizing: border-box; position: relative;"><h4 tabindex="-1" class="heading-element" dir="auto" style="box-sizing: border-box; margin-top: 24px; margin-bottom: 16px; font-size: 1em; font-weight: 600; line-height: 1.25;">3.2. Ready to train motion ControlNet</h4><a id="user-content-32-ready-to-train-motion-controlnet" class="anchor" aria-label="Permalink: 3.2. Ready to train motion ControlNet" href="https://github.com/Dai-Wenxun/MotionLCM#32-ready-to-train-motion-controlnet" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; float: left; padding-right: 4px; margin: auto; line-height: 1; position: absolute; top: 10px; left: -28px; display: flex; width: 28px; height: 28px; border-radius: 6px; opacity: 0; justify-content: center; align-items: center; transform: translateY(-50%); text-underline-offset: 0.2rem;"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">Please update the parameters in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">configs/motionlcm_control_s.yaml</code>. Then, run the following command:</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m train_motion_control --cfg configs/motionlcm_control_s.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m train_motion_control --cfg configs/motionlcm_control_s.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">This command by default uses the<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Pelvis</code><span>&nbsp;</span>joint for motion control training. If you want to utilize all the joints defined in OmniControl (i.e.,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Pelvis</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Left foot</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Right foot</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Head</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Left wrist</code>, and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Right wrist</code>), you need to modify the<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">TRAIN_JOINTS</code><span>&nbsp;</span>in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">DATASET.HUMANML3D.CONTROL_ARGS</code><span>&nbsp;</span>in the<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">configs/motionlcm_control_s.yaml</code>.</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">TRAIN_JOINTS: [0] -&gt; [0, 10, 11, 15, 20, 21]
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="TRAIN_JOINTS: [0] -> [0, 10, 11, 15, 20, 21]" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">This is also the reason we provide two checkpoints for testing in<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">experiments_control/spatial/motionlcm_humanml</code>.</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">CHECKPOINTS: 'experiments_control/spatial/motionlcm_humanml/motionlcm_humanml_s_pelvis.ckpt'  # Trained on Pelvis
CHECKPOINTS: 'experiments_control/spatial/motionlcm_humanml/motionlcm_humanml_s_all.ckpt'  #  Trained on All
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="CHECKPOINTS: 'experiments_control/spatial/motionlcm_humanml/motionlcm_humanml_s_pelvis.ckpt'  # Trained on Pelvis
CHECKPOINTS: 'experiments_control/spatial/motionlcm_humanml/motionlcm_humanml_s_all.ckpt'  #  Trained on All" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">During validation, the default testing joint is<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">Pelvis</code>, and the testing density is<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">100</code>.</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">TEST_JOINTS: [0]  # choice -&gt; [0], [10], [11], [15], [20], [21] (ONLY when trained on all)
TEST_DENSITY: 100  # choice -&gt; [100, 25, 5, 2, 1]
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="TEST_JOINTS: [0]  # choice -> [0], [10], [11], [15], [20], [21] (ONLY when trained on all)
TEST_DENSITY: 100  # choice -> [100, 25, 5, 2, 1]" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">TEST_DENSITY</code><span>&nbsp;</span>refers to the density level of control points selected from the ground truth (GT) trajectory. Specifically,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">100</code><span>&nbsp;</span>and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">25</code><span>&nbsp;</span>correspond to percentage, while<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">5</code>,<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">2</code>, and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">1</code><span>&nbsp;</span>correspond to number. The logic of the code is as follows:</p><div class="highlight highlight-source-python notranslate position-relative overflow-auto" dir="auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; margin-bottom: 16px; display: flex; justify-content: space-between; background-color: rgb(246, 248, 250);"><pre style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px; word-break: normal; min-height: 52px;"><span class="pl-c" style="box-sizing: border-box; color: rgb(89, 99, 110);"># MotionLCM/mld/data/humanml/dataset.py (Text2MotionDataset)</span>
<span class="pl-s1" style="box-sizing: border-box;">length</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">=</span> <span class="pl-s1" style="box-sizing: border-box;">joints</span>.<span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">shape</span>[<span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">0</span>]
<span class="pl-s1" style="box-sizing: border-box;">density</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">=</span> <span class="pl-s1" style="box-sizing: border-box;">self</span>.<span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">testing_density</span>
<span class="pl-k" style="box-sizing: border-box; color: rgb(207, 34, 46);">if</span> <span class="pl-s1" style="box-sizing: border-box;">density</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">in</span> [<span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">1</span>, <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">2</span>, <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">5</span>]:
    <span class="pl-s1" style="box-sizing: border-box;">choose_seq_num</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">=</span> <span class="pl-s1" style="box-sizing: border-box;">density</span>
<span class="pl-k" style="box-sizing: border-box; color: rgb(207, 34, 46);">else</span>:
    <span class="pl-s1" style="box-sizing: border-box;">choose_seq_num</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">=</span> <span class="pl-en" style="box-sizing: border-box; color: rgb(102, 57, 186);">int</span>(<span class="pl-s1" style="box-sizing: border-box;">length</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">*</span> <span class="pl-s1" style="box-sizing: border-box;">density</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">/</span> <span class="pl-c1" style="box-sizing: border-box; color: rgb(5, 80, 174);">100</span>)</pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="# MotionLCM/mld/data/humanml/dataset.py (Text2MotionDataset)
length = joints.shape[0]
density = self.testing_density
if density in [1, 2, 5]:
    choose_seq_num = density
else:
    choose_seq_num = int(length * density / 100)" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div></details>

<details open="" style="box-sizing: border-box; display: block; margin-top: 0px; margin-bottom: 16px;"><summary style="box-sizing: border-box; display: list-item; cursor: pointer;"><b style="box-sizing: border-box; font-weight: 600;">4. Evaluate the models</b></summary><div class="markdown-heading" dir="auto" style="box-sizing: border-box; position: relative;"><h4 tabindex="-1" class="heading-element" dir="auto" style="box-sizing: border-box; margin-top: 24px; margin-bottom: 16px; font-size: 1em; font-weight: 600; line-height: 1.25;">4.1. Motion Reconstruction:</h4><a id="user-content-41-motion-reconstruction" class="anchor" aria-label="Permalink: 4.1. Motion Reconstruction:" href="https://github.com/Dai-Wenxun/MotionLCM#41-motion-reconstruction" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; float: left; padding-right: 4px; margin: auto; line-height: 1; position: absolute; top: 10px; left: -28px; display: flex; width: 28px; height: 28px; border-radius: 6px; opacity: 0; justify-content: center; align-items: center; transform: translateY(-50%); text-underline-offset: 0.2rem;"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m test --cfg configs/vae.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m test --cfg configs/vae.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><div class="markdown-heading" dir="auto" style="box-sizing: border-box; position: relative;"><h4 tabindex="-1" class="heading-element" dir="auto" style="box-sizing: border-box; margin-top: 24px; margin-bottom: 16px; font-size: 1em; font-weight: 600; line-height: 1.25;">4.2. Text-to-Motion:</h4><a id="user-content-42-text-to-motion" class="anchor" aria-label="Permalink: 4.2. Text-to-Motion:" href="https://github.com/Dai-Wenxun/MotionLCM#42-text-to-motion" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; float: left; padding-right: 4px; margin: auto; line-height: 1; position: absolute; top: 10px; left: -28px; display: flex; width: 28px; height: 28px; border-radius: 6px; opacity: 0; justify-content: center; align-items: center; transform: translateY(-50%); text-underline-offset: 0.2rem;"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m test --cfg configs/mld_t2m.yaml
python -m test --cfg configs/motionlcm_t2m.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m test --cfg configs/mld_t2m.yaml
python -m test --cfg configs/motionlcm_t2m.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">If you want to change the number of inference steps, change the<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">num_inference_steps</code><span>&nbsp;</span>in the following configs:</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">configs/modules/scheduler_ddim.yaml  # MLD
configs/modules/scheduler_lcm.yaml   # MotionLCM
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="configs/modules/scheduler_ddim.yaml  # MLD
configs/modules/scheduler_lcm.yaml   # MotionLCM" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><div class="markdown-heading" dir="auto" style="box-sizing: border-box; position: relative;"><h4 tabindex="-1" class="heading-element" dir="auto" style="box-sizing: border-box; margin-top: 24px; margin-bottom: 16px; font-size: 1em; font-weight: 600; line-height: 1.25;">4.3. Motion Control:</h4><a id="user-content-43-motion-control" class="anchor" aria-label="Permalink: 4.3. Motion Control:" href="https://github.com/Dai-Wenxun/MotionLCM#43-motion-control" style="box-sizing: border-box; background-color: transparent; color: rgb(9, 105, 218); text-decoration: underline; float: left; padding-right: 4px; margin: auto; line-height: 1; position: absolute; top: 10px; left: -28px; display: flex; width: 28px; height: 28px; border-radius: 6px; opacity: 0; justify-content: center; align-items: center; transform: translateY(-50%); text-underline-offset: 0.2rem;"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg></a></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">The following command is for MotionLCM with motion ControlNet.</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m test --cfg configs/motionlcm_control_s.yaml
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m test --cfg configs/motionlcm_control_s.yaml" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">The following command is for MotionLCM with consistency latent tuning (CLT).</p><div class="snippet-clipboard-content notranslate position-relative overflow-auto" style="box-sizing: border-box; position: relative !important; overflow: auto !important; display: flex; justify-content: space-between; margin-bottom: 16px; background-color: rgb(246, 248, 250);"><pre class="notranslate" style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; overflow: auto; line-height: 1.45; color: rgb(31, 35, 40); background-color: rgb(246, 248, 250); border-radius: 6px;"><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0px; margin: 0px; white-space: pre; background: transparent; border-radius: 6px; word-break: normal; border: 0px; display: inline; overflow: visible; line-height: inherit; overflow-wrap: normal;">python -m test --cfg configs/motionlcm_t2m_clt.yaml --optimize
</code></pre><div class="zeroclipboard-container" style="box-sizing: border-box; display: block; animation: auto ease 0s 1 normal none running none;"><clipboard-copy aria-label="Copy" class="ClipboardButton btn btn-invisible js-clipboard-copy m-2 p-0 d-flex flex-justify-center flex-items-center" data-copy-feedback="Copied!" data-tooltip-direction="w" value="python -m test --cfg configs/motionlcm_t2m_clt.yaml --optimize" tabindex="0" role="button" style="box-sizing: border-box; position: relative; display: flex !important; padding: 0px !important; font-size: 14px; font-weight: 500; line-height: 20px; white-space: nowrap; vertical-align: middle; cursor: pointer; user-select: none; border: 0px; border-radius: 6px; appearance: none; color: rgb(9, 105, 218); background-color: transparent; box-shadow: none; transition: color 80ms cubic-bezier(0.33, 1, 0.68, 1), background-color, box-shadow, border-color; justify-content: center !important; align-items: center !important; margin: 8px !important; width: 28px; height: 28px;"><svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg></clipboard-copy></div></div><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">For CLT, we default to using<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">num_inference_steps=1</code><span>&nbsp;</span>and<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">batch_size=1</code>.<span>&nbsp;</span><strong style="box-sizing: border-box; font-weight: 600;">Do not modify these two parameters.</strong></p><p dir="auto" style="box-sizing: border-box; margin-top: 0px; margin-bottom: 16px;">For our default motion control test (i.e., simply run the commands above), it is based on the<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">pelvis</code><span>&nbsp;</span>joint with<span>&nbsp;</span><code style="box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace; font-size: 13.6px; padding: 0.2em 0.4em; margin: 0px; white-space: break-spaces; background-color: rgba(129, 139, 152, 0.12); border-radius: 6px;">density=100</code>. If you want to obtain complete results, please adjust the testing joint and testing density according to the motion control training tutorial.</p></details>


### **Text-to-Motion (using prompts from HumanML3D test set) **:ok:

**4. Motion Control (using prompts and trajectory from HumanML3D test set)**

The following command is for MotionLCM with motion ControlNet.

```
python demo.py --cfg configs/motionlcm_control_s.yaml
```

一个是ref (应该是数据集gt吧),一个是生成的

![image-20250507153606028](assets/image-20250507153606028.png)



The following command is for MotionLCM with consistency latent tuning (CLT).

```
python demo.py --cfg configs/motionlcm_t2m_clt.yaml --optimize
```

![image-20250507153939811](assets/image-20250507153939811.png)

 **“MotionLCM with consistency latent tuning (CLT)”** 是 MotionLCM 框架中一种 **针对潜在空间（Latent Space）的微调技术**，目的是通过优化潜在编码（Latent Code）来提升生成运动的质量或适配特定需求



**CLT vs 普通 MotionLCM 生成**

| 特性         | 普通 MotionLCM (`motionlcm_t2m.yaml`) | MotionLCM + CLT (`motionlcm_t2m_clt.yaml`) |
| ------------ | ------------------------------------- | ------------------------------------------ |
| **生成方式** | 直接前向生成，无优化                  | 生成过程中迭代优化潜在编码                 |
| **速度**     | 极快（1-4步）                         | 稍慢（需额外优化步骤）                     |
| **质量**     | 可能细节不足                          | 更精细，对齐更好                           |
| **适用场景** | 实时快速生成                          | 对质量要求更高或需要精确控制时             |



**5. Render SMPL**

After running the demo, the output folder will store the stick figure animation for each generated motion (e.g., `assets/example.gif`).

![example](https://github.com/Dai-Wenxun/MotionLCM/raw/main/assets/example.gif)

To record the necessary information about the generated motion, a pickle file with the following keys will be saved simultaneously (e.g., `assets/example.pkl`):

- `joints (numpy.ndarray)`: The XYZ positions of the generated motion with the shape of `(nframes, njoints, 3)`.
- `text (str)`: The text prompt.
- `length (int)`: The length of the generated motion.
- `hint (numpy.ndarray)`: The trajectory for motion control (optional).



# debug

demo.py

调用

model = target_model_class(cfg, dataset)

进到 mld.py



####  control

生成的 `launch.json` 中，添加一个自定义配置来传递命令行参数。示例配置如下：

`python demo.py --cfg configs/motionlcm_control_s.yaml`

尝试一下这个

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug MotionLCM Demo",
            "type": "debugpy",
            "request": "launch",
            "program": "/root/MotionLCM/MotionLCM/demo.py",
            "args": [
                "--cfg", "configs/motionlcm_control_s.yaml", // 参数
            ],
            "console": "integratedTerminal",
            "justMyCode": true,
            "python": "/root/miniconda3/envs/motionlcm/bin/python",  // 显式指定 Conda 环境路径
            "cwd": "/root/MotionLCM/MotionLCM"                // 设置工作目录
        }
    ]
}
```

