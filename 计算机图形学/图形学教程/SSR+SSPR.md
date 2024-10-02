# SSR+SSPR



# 一、SSR基础

参考文章：https://zhuanlan.zhihu.com/p/650035462



# 二、SSPR

一些知识点的介绍：

## 1.关于贴图格式

> 在 Unity 中，`RenderTextureFormat.ARGB32` 和 `RenderTextureFormat.ARGBHalf` 是两种不同的渲染纹理格式，它们主要用于处理图像数据的存储方式。
>
> ### RenderTextureFormat.ARGB32
>
> - **描述**：这是一个 32 位的纹理格式，每个像素包含四个通道：A（Alpha）、R（Red）、G（Green）、B（Blue），每个通道占用 8 位。
> - **位深度**：每个颜色通道使用 8 位，因此总共提供了 256 种可能的值（0-255），可以表示的颜色范围较小。
> - **HDR**：不支持 HDR（高动态范围），适合普通的色彩渲染。
>
> ### RenderTextureFormat.ARGBHalf
>
> - **描述**：这是一个 64 位的纹理格式，同样包含四个通道：A、R、G、B，但每个通道占用 16 位。
> - **位深度**：每个颜色通道使用 16 位，可以表示的值范围大大增加，支持更丰富的颜色和亮度信息。
> - **HDR**：支持 HDR，这使得它可以处理更高的亮度值，非常适合于需要高动态范围的场景，如光照效果和后处理特效等。
>
> ### 精度对比
>
> - **精度更高**：`RenderTextureFormat.ARGBHalf` 的精度更高，因为它的每个通道都使用 16 位，而 `RenderTextureFormat.ARGB32` 只使用 8 位。这使得 `ARGBHalf` 能够更精确地表示颜色和亮度信息，尤其是在涉及到光照计算或高动态范围渲染时。
>
> ### 总结
>
> - `RenderTextureFormat.ARGB32`：32 位，8 位每通道，不支持 HDR。
> - `RenderTextureFormat.ARGBHalf`：64 位，16 位每通道，支持 HDR，因此在处理高亮度和细节时表现更佳。



> 在 Unity 中，`RenderTextureFormat.RFloat` 和 `RenderTextureFormat.RInt` 是两种特定的渲染纹理格式，主要用于处理单通道（即只包含一个通道）数据。它们分别用于存储浮点数和整数值。
>
> ### RenderTextureFormat.RFloat
>
> - **描述**：这是一个单通道的渲染纹理格式，每个像素仅包含一个通道，用于表示浮点数值。
>
> - **位深度**：每个像素使用 32 位（4 字节），能够存储范围非常广泛的浮点数值。这使得它非常适合需要高精度的计算，比如物理模拟、光照信息等。
>
> - 使用场景
>
>   ：
>
>   - 可以用于存储深度信息或浮动值，例如，不同的物理量（如速度、温度等）。
>   - 在某些后处理效果中也可能用来存储亮度或其他需要高动态范围的信息。
>
> ### RenderTextureFormat.RInt
>
> - **描述**：这是一个单通道的渲染纹理格式，每个像素同样仅包含一个通道，用于表示整数值。
>
> - **位深度**：每个像素使用 32 位（4 字节），可以存储带符号的整数值，范围通常是从 -2,147,483,648 到 2,147,483,647。
>
> - 使用场景
>
>   ：
>
>   - 常用于离散数据，例如索引、标识符或者其他需要整数表示的情况。
>   - 也可以用于一些特定的后处理效果，特别是那些需要对像素进行分类或计数的操作。
>
> ### 总结
>
> - **RenderTextureFormat.RFloat**：用于存储浮点数值，具有高精度，适合需要细致计算的场合。
> - **RenderTextureFormat.RInt**：用于存储整数值，适合对数据进行分类、标识或计数的情况。
>
> 这两种格式都提供了灵活性，使得开发者可以根据具体的需求选择合适的数据表示方式。



> ### 说明
>
> - **PC (DirectX)**：指的是在 PC 平台上使用 DirectX 图形 API 的环境。
> - **RenderTextureFormat.RInt + InterlockedMin()**：表示可以使用 `RInt` 格式的渲染纹理，并结合 `InterlockedMin()` 函数来进行线程安全的最小值计算。
> - **Non-Mobile path**：表明这个特性或功能适用于非移动平台（即桌面和控制台等平台），而不适用于移动设备。
>
> ### 为什么选择 RInt 而不是 RFloat？
>
> 1. **整数操作**：使用 `RenderTextureFormat.RInt` 可以直接存储整数数据，这对于某些计算（如计数、索引、标识符等）更为高效。在这种情况下，整数格式比浮点格式更合适，因为整数计算通常比浮点计算涉及的资源要少，并且执行速度可能更快。
> 2. **线程安全**：`InterlockedMin()` 是一个原子操作，确保在多线程环境中安全地更新值。当你需要并发地对一个值进行修改时，使用整数类型的渲染纹理格式与原子操作相结合，可以避免竞争条件和数据不一致的问题。
> 3. **内存占用和性能**：对于整数数据，使用 `RInt` 格式可能在内存占用方面更具优势，并且可以提高性能，特别是在不需要高精度的情况下。相比之下，`RFloat` 虽然提供更广泛的数值范围和精度，但如果没有必要，使用它可能会浪费资源。
>
> ### RFloat 的使用情况
>
> 尽管注释中没有直接提到 `RFloat`，但这并不意味着 `RFloat` 在 PC 平台上不可用。开发者仍然可以选择使用 `RenderTextureFormat.RFloat`，尤其是在需要高动态范围或者更复杂计算（如物理模拟、光照等）的场景中。
>
> ### 总结
>
> - **使用 `RInt` 的原因**：高效的整数操作、线程安全的原子操作、内存占用低、更好的性能。
> - **`RFloat` 的可用性**：虽然没有特别推荐，但在需要高精度的情况下仍然可以使用。





> 在 Unity 的计算着色器 (Compute Shader) 中，您提供的代码片段主要用于定义纹理属性并将其传递给计算着色器。以下是对每一部分的详细解释：
>
> ### 代码解析
>
> ```c#
> static readonly int _SSPR_ColorRT_pid = Shader.PropertyToID("_MobileSSPR_ColorRT");
> static readonly int _SSPR_PackedDataRT_pid = Shader.PropertyToID("_MobileSSPR_PackedDataRT");
> static readonly int _SSPR_PosWSyRT_pid = Shader.PropertyToID("_MobileSSPR_PosWSyRT");
> ```
>
> 1. **Shader.PropertyToID**：
>
>    - `PropertyToID` 是一个静态方法，用于将字符串形式的属性名转换为整数 ID。这种转换使得在访问这些属性时更加高效，因为使用整数 ID 可以减少字符串查找的开销。
>    - 在这里，创建了三个属性 ID，分别针对不同的纹理。
>
> 2. **RenderTargetIdentifier**：
>
>    ```c#
>    RenderTargetIdentifier _SSPR_ColorRT_rti = new RenderTargetIdentifier(_SSPR_ColorRT_pid);
>    RenderTargetIdentifier _SSPR_PackedDataRT_rti = new RenderTargetIdentifier(_SSPR_PackedDataRT_pid);
>    RenderTargetIdentifier _SSPR_PosWSyRT_rti = new RenderTargetIdentifier(_SSPR_PosWSyRT_pid);
>    ```
>
>    - `RenderTargetIdentifier` 是一个结构体，用于标识渲染目标。在这里，它们被用来引用之前定义的纹理属性，通过它们的 ID。
>    - 这使得后续的渲染操作能够方便地使用这些纹理。
>
> ### SetComputeTextureParam 方法
>
> ```c#
> 复制代码cb.SetComputeTextureParam(cs, kernel_NonMobilePathClear, "ColorRT", _SSPR_ColorRT_rti);
> ```
>
> 1. **cb**：命令缓冲区（Command Buffer），用于存储要发送给 GPU 的渲染指令。
> 2. SetComputeTextureParam：
>    - 这个方法用于将指定的纹理（在这里是 `_SSPR_ColorRT_rti`）设置为计算着色器中的一个参数。
> 3. **cs**：计算着色器的实例。
> 4. **kernel_NonMobilePathClear**：指定要使用的核函数，可以理解为计算着色器中的某个特定计算任务。
> 5. **"ColorRT"**：这是计算着色器中定义的纹理参数名称。计算着色器可以通过这个名称访问传入的纹理。
>
> ### 整体意义
>
> - 这行代码的目的是将名为 `"ColorRT"` 的计算着色器参数与对应的纹理 `_SSPR_ColorRT_rti` 绑定起来。
> - 在计算着色器执行时，程序会从这个纹理读取数据，以进行相关计算或处理。
>
> ### 应用场景
>
> 这些步骤通常用于图形处理、后处理效果、物理模拟等场景，确保计算着色器能够有效利用 GPU 的并行计算能力，并处理复杂的图像或数据。





> //Non-Mobile path will use this RT: single 32bits RInt RT, split first 16bits for GetReflectionColorFromID's y, last 16bits for GetReflectionColorFromID's x //y put in first 16 bits because we want to sort by InterlockedMin(), allowing only "closer to reflection plane candidate" to write to HashRT 翻译并解释一下这段是什么意思
>
> 
>
> 
>
> 2024/10/2 18:41:42
>
> 这段注释的意思是：
>
> ### 翻译
>
> ```
> // 非移动路径将使用这个渲染目标（RT）：单个 32 位的 RInt 渲染目标，将前 16 位分配给 GetReflectionColorFromID 的 y 值，把后 16 位分配给 GetReflectionColorFromID 的 x 值。
> // 将 y 放在前 16 位是因为我们希望通过 InterlockedMin() 进行排序，只允许“更靠近反射平面的候选者”写入 HashRT。
> ```
>
> ### 解释
>
> 1. **Non-Mobile path**：
>    - 指的是适用于桌面或控制台等非移动平台的图形渲染路径。这种路径通常能够利用更强大的硬件性能，支持更复杂的操作。
> 2. **RT (Render Target)**：
>    - 渲染目标是一个可以被 GPU 写入的纹理或缓冲区。在这里提到的 **32 位的 RInt RT** 表示每个像素由一个 32 位的整数表示。
> 3. **分割 32 位数据**：
>    - 该 32 位整数被分为两个部分：
>      - **前 16 位**用于存储 `GetReflectionColorFromID` 函数的 y 值。
>      - **后 16 位**用于存储同一函数的 x 值。
> 4. **InterlockedMin()**：
>    - 这是一个原子操作，用于确保在多线程环境中安全地更新值。这里的目的是对可能的反射候选者进行排序，只有距离反射平面最近的候选者能够写入这个渲染目标（HashRT）。
> 5. **排序目的**：
>    - 通过将 y 值放在前 16 位，可以利用 InterlockedMin() 确保只让更接近反射平面的值写入 HashRT。这意味着，如果有多个候选者，它们的 y 值会被比较，只有最小的（即最近的）y 值会被保存，从而避免覆盖在反射平面较远的候选者。
>
> ### 总结
>
> 这段注释描述了如何在计算着色器中有效管理和处理反射信息，通过将数据分为两部分并使用原子操作来确保正确的写入顺序，从而优化反射效果的计算。这种方法在需要同时处理多个候选者时，可以提高渲染效率和结果的准确性。





## 2.关于ZFight的解决方案

### 中文翻译

```
////////////////////////////////////////////////////////////////////////////////////////////////////
// 将“原始RT位置ID.xy和alpha”写入“12位yID、12位xID、8位alpha”哈希，在“反射RT位置”处
////////////////////////////////////////////////////////////////////////////////////////////////////
/*
参考: http://remi-genin.fr/blog/screen-space-plane-indexed-reflection-in-ghost-recon-wildlands/#hash-resolve-jump
读取-写入时最大化访问投影哈希UAV

// 来自上面网站的示例代码，“哈希解决”部分
uint projectionHash = SrcPosPixel.y << 16 | SrcPosPixel.x; 
InterlockedMax(ProjectionHashUAV[ReflPosPixel], projectionHash, dontCare);
*/

 // ghost recon wildlands方法使用16位y，16位x编码
 // 但在我们的实现中，16位过于浪费，因为我们不需要一个65536*65536的RT
 // 相反，我们为淡出alpha信息保存8位，结果是：
 // -前12位用于id.y (0~4095)
 // -接着12位用于id.x (0~4095)
 // -最后8位用于alpha (0~255)
```

### 解释

这段代码注释描述了一种用于图形渲染的哈希存储方案，具体是在反射相关的渲染技术中。这种技术源自《幽灵行动：荒野》（Ghost Recon Wildlands），主要用于处理屏幕空间中的平面索引反射。以下是对每个部分的详细解释：

1. **目标**：
   - 将原始渲染目标（RT）的位置 ID 和 alpha 值以特定格式编码，并存储在反射位置的哈希表中。
2. **编码形式**：
   - 使用 32 位来存储信息，其中：
     - 前 12 位用于 y 轴 ID（范围 0 到 4095）
     - 接下来的 12 位用于 x 轴 ID（范围 0 到 4095）
     - 最后 8 位用于 alpha 值（范围 0 到 255）
3. **效率考虑**：
   - 原文指出，虽然《幽灵行动：荒野》中使用了 16 位 y 和 16 位 x 编码，但在他们的实现中，16 位的精度是多余的，因为 RT 的分辨率不需要达到 65536 x 65536。因此，他们采用了更紧凑的格式，以节省内存并提高性能。
4. **哈希更新**：
   - 代码提到使用 `InterlockedMax` 函数来确保在并发访问时能够安全地更新哈希值。这意味着如果多个线程同时尝试写入同一位置，它们将不会造成数据竞争，最终只会保留最大的哈希值。

### 总结

这段代码的核心思想是为图形渲染中的反射信息提供一种高效的存储机制，通过合理编码来减少所需的位数，同时保持足够的信息以满足需求。

> note：alpha值用于记录一些与边界有关的信息，具体地可以看代码，我的理解是越靠近屏幕的边缘就越有一种淡化的效果，可以让视觉效果更理想。



## 3.hash的计算方法

> 在这段代码中，`hash` 是通过将三个不同的值打包到一个 `uint`（32 位无符号整数）中来计算的。我们可以逐步分析这个过程：
>
> ### 变量解释
>
> 1. **`fadeoutAlphaInt`**：
>    - 这是将 `fadeoutAlpha`（一个在 0 到 1 范围内的浮点数）乘以 255 来得到的结果。这样做是为了将其转换为一个在 0 到 255 范围内的整数，这个整数可以用 8 位表示。
> 2. **`id.y` 和 `id.x`**：
>    - 假设 `id.y` 和 `id.x` 是用于标识某个对象或像素的整数值。根据上下文，它们可能分别表示 y 和 x 轴上的某些位置 ID。
>
> ### `hash` 的计算
>
> ```
> cpp复制代码uint hash = id.y << 20 | id.x << 8 | fadeoutAlphaInt;
> ```
>
> #### 打包步骤：
>
> 1. **移位操作**：
>    - id.y << 20：将id.y左移 20 位，使其位于hash的高位部分。
>      - 这意味着 `id.y` 在最终的 `hash` 中占据了从第 21 位到第 32 位的位置（共 12 位）。
>    - id.x << 8：将id.x左移 8 位，使其位于中间部分。
>      - 这意味着 `id.x` 在 `hash` 中占据了从第 9 位到第 20 位的位置（共 12 位）。
>    - fadeoutAlphaInt：直接放置在低位部分。
>      - 这意味着 `fadeoutAlphaInt` 在 `hash` 中占据了从第 1 位到第 8 位的位置（共 8 位）。
> 2. **按位 OR 操作**：
>    - 使用按位 OR (`|`) 将这三个值组合在一起，从而形成一个唯一的 `hash` 值。
>    - 由于每个值的位数和位置都不重叠，因此它们可以安全地组合成一个 32 位的整数。
>
> ### 示例
>
> 假设：
>
> - `id.y = 5`（在二进制表示为 `0000 0000 0000 0101`）
> - `id.x = 3`（在二进制表示为 `0000 0000 0000 0011`）
> - `fadeoutAlphaInt = 200`（在二进制表示为 `11001000`）
>
> 那么计算过程如下：
>
> 1. `id.y << 20`:
>    - `0000 0000 0000 0101` 移动 20 位 -> `0101 0000 0000 0000 0000 0000 0000 0000`
> 2. `id.x << 8`:
>    - `0000 0000 0000 0011` 移动 8 位 -> `0000 0000 0000 0000 0011 0000 0000 0000`
> 3. `fadeoutAlphaInt`:
>    - `11001000` -> `0000 0000 0000 0000 0000 0000 1100 1000`
>
> 最后，组合这些值：
>
> ```
> plaintext复制代码hash = (01 0100 0000 0000 0000 0000 0000 0000) // id.y shifted
>       | (00 0000 0000 0000 0011 0000 0000 0000) // id.x shifted
>       | (00 0000 0000 0000 0000 0000 1100 1000) // fadeoutAlphaInt
> ```
>
> ### 总结
>
> 这种打包方式允许将多个数据点存储在一个单一的整数中，节省空间并提高数据处理效率。在图形编程中，尤其是在处理纹理映射、光照和反射等方面，这种方法可以有效地管理大量信息。



## 4.不断完善算法的中间结果图

如果只是完成了最基础的原理部分，那么渲染得到的结果如下：

![image-20241002200916282](./assets/image-20241002200916282.png)

可以看到，有很多断掉的地方，而且反射的部分有很多洞，这就是接下来要解决的问题。



### （1）FillHoles

使用最基础的步骤，会出现反射空洞的情况。这是因为们对翻转后的世界坐标进行透视投影变换，导致因为其近大远小的特性，像素会被偏移，也就导致我们最后的存在反射纹理中的纹理索引不对了（比如一个像素本该映射到(233, 233)索引的，可能会被映射到(233, 232)，导致(233, 233)这个索引处的纹理颜色一直为空，也就导致了空洞的出现）。参考文章：https://zhuanlan.zhihu.com/p/651134124

一种缓解的方法是取得周围的有效像素去填补空洞。这里看最终项目当中的Compute Shader的kernel即可。





### （2）边缘缺失——解决方案：边缘拉伸

首先来看一下FillHoles之后的效果：

![image-20241002202228783](./assets/image-20241002202228783.png)

可以看到好了一些，不过由于角色的组成比较复杂，深度图获取不到的区域（比如脖子下方那里）在SSPR的时候信息就会丢失。这里根据那篇[Screen Space Planar Reflections in Ghost Recon Wildlands](https://link.zhihu.com/?target=https%3A//remi-genin.github.io/posts/screen-space-planar-reflections-in-ghost-recon-wildlands/)的做法，将边缘的UV进行拉伸。主要还是看代码