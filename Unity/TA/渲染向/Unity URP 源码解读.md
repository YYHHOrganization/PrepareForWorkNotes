# Unity URP 源码解读

代码基于Unity 2022.3.13版本，URP对应的版本为14.0.9。



# 一、管线pipeline

参考：https://zhuanlan.zhihu.com/p/555310238

## 1.UniversalRenderPipelineAsset.cs

在Runtime/data里面。

### 属性

- **Rendering Settings&General Settings**
  - rendererDataList (渲染器数据列表)
  - defaultRendererIndex (默认开启的渲染器索引)
  - requireDepthTexture (是否生成_CameraDepthTexture, 在Shader中使用)
  - requireOpaqueTexture (是否生成_CameraOpaqueTexture, 在Shader中使用)
  - opaqueDownsampling (_CameraOpaqueTexture的降采样倍率)
  - m_SupportsTerrainHoles：==先不用管==
- **Quality Settings**
  - supportsHDR (是否开启HDR)
  - MSAA (_2x、_4x、_8x) (开启2、4、8倍MSAA[抗锯齿](https://zhida.zhihu.com/search?content_id=211535106&content_type=Article&match_order=1&q=抗锯齿&zhida_source=entity))
  - renderScale (cameraColorTarget、cameraDepthTarget的分辨率缩放)
- **Light Settings**
  - mainLightRenderingMode (PerVertex、PerPixel)
  - mainLightShadowsSupported (是否开启主光源阴影)
  - mainLightShadowmapResolution (主光源阴影贴图分辨率)
  - additionalLightsRenderingMode (PerVertex、PerPixel)
  - additionalLightsPerObjectLimit (每个物体接收的最大额外光源数量)
  - additionalLightShadowsSupported (是否开启额外光源阴影)
  - additionalLightsShadowmapResolution (额外光源阴影贴图分辨率)
  - supportsLightLayers (是否开启光照图层)
    - https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/features/rendering-layers.html
  - **Reflection Probes Settings**
    - reflectionProbeBlending (是否开启多个[反射探针](https://zhida.zhihu.com/search?content_id=211535106&content_type=Article&match_order=1&q=反射探针&zhida_source=entity)混合)
    - reflectionProbeBoxProjection (是否开启盒体投影)

- **Shadows Settings**
  - shadowDistance (多少距离内生成阴影)
  - shadowCascadeCount (CSM层数)
  - cascade2Split、cascade3Split、cascade4Split (第一二层、二三层、三四层的划分距离)
  - shadowDepthBias (阴影深度偏移值)
  - shadowNormalBias (阴影法线偏移值)
  - softShadowsSupported (是否开启软阴影)

> GPT解释了如下两个字段：
>
> 1. **`m_ConservativeEnclosingSphere`**:
>    - 这个布尔字段指示是否使用保守包围球算法来计算阴影。如果设置为 `true`，则会考虑一个更大的包围球来包裹光源的影响区域。这种方法可以减少阴影计算时可能发生的错误，特别是在光源或物体的位置变化比较大的情况下。
>    - 使用保守包围球的好处是可以减少阴影伪影（shadow artifacts），例如阴影不正确或阴影断裂等问题，从而提高最终渲染的质量。
> 2. **`m_NumIterationsEnclosingSphere`**:
>    - 这是一个整数值，表示用于计算包围球的迭代次数。这个值越高，计算的精确度可能越高，但同时会增加计算成本。在进行阴影计算时，这个值用来控制如何细化包围球的定义。
>    - 通过增加迭代次数，可以使包围球更准确地适应光源和几何形状，从而改善阴影的质量和减少阴影中的噪声。



- **Post Processing Settings**
  - colorGradingMode (LDR、HDR)

- **Advanced Settings**

  - useSRPBatcher (是否开启SRP合批)
  - supportsDynamicBatching (是否开启[动态合批](https://zhida.zhihu.com/search?content_id=211535106&content_type=Article&match_order=1&q=动态合批&zhida_source=entity))

- 其他：

  - StoreActionsOptimization：https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/api/UnityEngine.Rendering.Universal.StoreActionsOptimization.html
  - data driven lens flare：
    - https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/shared/lens-flare/lens-flare-component.html
  - color grading LUT：

  > 在图形和游戏开发中，**LUT（Lookup Table）** 是一种用于颜色分级的技术，它允许开发者快速且高效地对图像进行颜色调整。您提到的代码注释涉及到 LUT 的大小与 HDR （高动态范围）颜色分级模式的使用，下面将详细解释相关内容。
  >
  > ### LUT 的基本原理
  >
  > 1. **什么是 LUT**：
  >    - Lookup Table（查找表）是一个预计算的数组，用于快速将输入颜色映射到输出颜色。在颜色分级中，LUT 可以使得颜色调整变得简单且高效。
  > 2. **如何工作**：
  >    - 在颜色分级过程中，输入的颜色值会通过 LUT 查找对应的输出颜色。例如，输入 RGB 颜色 (R, G, B) 会被送入 LUT，然后根据 LUT 中的预定义映射获取新的颜色值。
  >    - 通常，LUT 是以立方体（3D LUT）或一维表（1D LUT）的形式存储的，该表包含了不同颜色值之间的关系。
  >
  > ### 注释内容的解释
  >
  > - **LUT Size**：
  >   - 注释中提到的 `16^3` 和 `32` 指的是 LUT 的大小，以立方体的形式表示。`16^3` 表示有 16 级 R、G、B 分量，总共有 4096 种可能的颜色，而 `32^3` 则意味着使用 32768 种颜色。
  >   - 对于 HDR 色彩分级模式，`16^3` 的 LUT 尺寸几乎不可用，建议的最小尺寸为 `32^3`。这是因为 HDR 内容通常具有更丰富的色彩信息和亮度范围，因此需要更大的 LUT 来正确映射这些信息。
  > - **Log Encoding**：
  >   - “lut being encoded in log” 指的是 LUT 中的数据采用对数编码。这种编码方法在处理高动态范围图像时非常有用，因为它可以更有效地表示极端亮度差异，在低光范围内提供更多细节，同时减少高光过曝的风险。
  > - **1D Shaper LUT**：
  >   - 注释中提到的 1D Shaper LUT 是一种额外的 LUT，通常用于先对输入颜色进行预处理，以便其更好地适配 3D LUT 的要求。这种方法可以进一步改善颜色映射的效果，但为了保持简单，当前实现没有使用。
  >
  > ### 总结
  >
  > LUT 在颜色分级中扮演着重要角色，能够帮助开发者以高效的方式实现复杂的颜色调整。选择合适的 LUT 大小对于确保 HDR 图像的视觉质量至关重要，较大的 LUT 能够提供更精确的颜色映射，从而获得更好的最终效果。





## 2.核心——UniversalRenderpipeline

参考：

【1】https://zhuanlan.zhihu.com/p/555310238

【2】https://www.zhihu.com/collection/703766200

从Render函数开始看：

```c#
Render()
	BeginContextRendering(renderContext, cameras);  //【1】
	SetupPerFrameShaderConstants(); //[2]
	SortCameras()
	foreach camera in cameras:
		if gameCam then //这种对应游戏中的Camera
            RenderCameraStack(ScriptableRenderContext context, Camera baseCamera) //[3]
        else: //这种对应比如Scene窗口中的Camera
			BeginCameraRendering()
			UpdateVolumeFramework()
			RenderSingleCamera()
			EndCameraRendering()
    EndContextRendering
```

- 【1】参考https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Rendering.RenderPipelineManager-beginContextRendering.html，其实就是回调了所有绑定beginContextRendering事件的函数；
- 【2】设置了一些Shader中的常量；
- 【3】对于游戏中的相机（不是Scene窗口中的相机），调用RenderCameraStack。这个概念可以参考：https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/cameras.html，在URP 文档介绍部分中会进行整理。





# URP 文档介绍

# 1.Cameras

参考：https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/cameras.html

以下记录文档中值得注意的内容。

