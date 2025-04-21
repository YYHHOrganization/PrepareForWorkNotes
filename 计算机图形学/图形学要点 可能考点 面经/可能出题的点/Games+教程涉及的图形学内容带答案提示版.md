# 一、渲染——基础篇

## 1.线性代数基础篇+空间变换

> 本节需要复习的内容：
>
> - （1）图形学教程的空间变换篇；
> - （2）《入门精要》中的shader里面的空间变换；

### （1）游戏业务：巡逻的敌人

在《原神》中，有一些巡逻的西风骑士团NPC，玩家需要靠躲避NPC的视野来拿到天空之琴，每个NPC有一个forward方向，视野的范围（张角），和判定距离。同时需要有一个可视化的灯光范围，提示玩家避开这个范围。这个业务逻辑怎么做呢？

回答：

> 在《原神》类NPC视野检测与可视化实现方案：  
>
> ### **1. 视野检测逻辑（核心算法）**  
> - **点乘 + 距离判断**：  
>   - 用 `Vector3.Dot(NPC.forward, (playerPos - NPC.position).normalized)` 计算夹角余弦值，若大于 `cos(视野张角/2)` 则角度有效。  
>   - 同时检查玩家距离是否在 `判定距离` 内。  
>   - **优化**：可预计算 `cos(θ)` 避免重复调用 `Mathf.Cos`。  
>
> ### **2. 可视化方案（Unity实现）**  
> - **Spot Light**：  
>   - 直接绑定 `Spot Light` 到NPC，调整 `angle` 和 `range` 匹配视野参数，但需注意性能（多NPC时需烘焙或动态控制）。  
> - **Mesh投影（更优）**：  
>   - 动态生成扇形Mesh（`MeshFilter` + `MeshRenderer`），用半透明材质显示视野范围，性能更可控。  
>
> ### **3. 代码逻辑（伪代码）**  
> ```csharp
> bool IsPlayerInSight(NPC npc, Player player) {
>     Vector3 dirToPlayer = (player.pos - npc.pos).normalized;
>     float dot = Vector3.Dot(npc.forward, dirToPlayer);
>     float cosHalfAngle = Mathf.Cos(npc.fovAngle * 0.5f * Mathf.Deg2Rad);
>     return dot >= cosHalfAngle && Vector3.Distance(npc.pos, player.pos) <= npc.viewDistance;
> }
> ```
>
> ### **4. 优化点**  
> - **性能**：对非活跃NPC降低检测频率（如 `Coroutine` 分帧检测）。  
> - **扩展性**：用 `ScriptableObject` 配置视野参数（角度、距离）。  
>
> **总结**：点乘判断 + 动态Mesh可视化是平衡性能与效果的最佳实践。

- 另外，点乘也可以用来判断两个向量是同向/异向，应该比较好理解，就不展开了。**根据最后的值还可以知道两个向量靠的有多近。**



### （2）叉乘在图形学中有什么应用？

- 判断b向量在a向量的左侧/右侧
- 判断点是否在三角形内部；



### （3）补充：换坐标系的投影

核心是以下的逻辑：假设把向量$p$投影到uvw坐标系下，则可以表示为：
$$
\vec{p} = (\vec{p} · \vec{u})\vec{u} + (\vec{p} · \vec{v})\vec{v} + (\vec{p} · \vec{w})\vec{w}
$$


### （4）矩阵的基本性质

- (AB)C = A(BC)
- A(B+C) = AB + AC
- (A+B)C = AC + BC



### （5）空间变换的相关题目

> 图形学教程——空间变换中记录的非常详细了，这里就只整理题目，需要的去那里看。

#### （a）需要能推导的矩阵

- 平移、旋转、缩放矩阵、shear矩阵
- MVP矩阵，视口变换矩阵



#### （b）需要能说出推导过程的矩阵

- 绕任意轴旋转的矩阵怎么推导？注意任意轴可能过原点或者不过原点。（`有难度，需要不断复习`）



## 2.四元数相关的题目

