# 需要了解的Unity与C#

## 1.Unity中的GC

[Unity 中的 .NET 概述 - Unity 手册](https://docs.unity3d.com/cn/2021.1/Manual/overview-of-dot-net-in-unity.html)

> 以下是关于Boehm垃圾回收算法及Unity中增量模式的详细说明：
>
> ---
>
> ### **Boehm垃圾回收算法**
> **基本特性**  
> Boehm-Demers-Weiser垃圾回收器（简称Boehm GC）是一种**保守式、非分代、基于标记-清扫（Mark-Sweep）**的垃圾回收器，核心设计如下：
>
> | **特性**          | **说明**                                                     |
> | ----------------- | ------------------------------------------------------------ |
> | **保守式回收**    | 不精确识别指针（可能将非指针数据误判为指针），但保证安全（不会误删存活对象） |
> | **非分代**        | 不区分新生代/老年代，每次回收全堆内存                        |
> | **标记-清扫算法** | 分两阶段：标记存活对象 → 清扫未标记对象                      |
> | **手动集成**      | 无需编译器支持，通过代码插桩实现内存管理                     |
>
> **工作流程**  
> 1. **标记阶段**：从根对象（全局变量、栈变量）出发，递归标记所有可达对象  
> 2. **清扫阶段**：遍历堆内存，释放未标记对象的内存块  
>
> **优点与缺点**  
> ```text
> +------------------+------------------------------+
> |      优点         |           缺点               |
> +------------------+------------------------------+
> | 无需语言运行时支持 | 内存碎片化（标记-清扫固有缺陷）|
> | 跨平台兼容性高    | 非分代设计导致吞吐量较低      |
> | 内存开销小        | 保守式回收可能漏掉部分垃圾    |
> +------------------+------------------------------+
> ```
>
> ---
>
> ### **增量模式（Incremental GC）**
> **核心思想**  
> 将垃圾回收过程拆分为多个**小步骤执行**，在应用程序运行的间隙逐步完成GC，减少单次暂停时间。
>
> **Unity中的实现**  
> ```csharp
> // 伪代码示例：增量GC与帧循环的协作
> void GameLoop() {
>     while (true) {
>         UpdateGameLogic();  // 游戏逻辑更新
>         RenderFrame();      // 渲染帧
>         
>         // 每帧执行一小部分GC工作
>         if (Unity.GC.IncrementalStep()) {
>             // 当前帧GC步骤完成
>         }
>     }
> }
> ```
>
> **技术关键点**  
> 1. **阶段划分**：  
>    - 将标记阶段分解为多个增量步骤（如每次标记10%的堆）  
>    - 清扫阶段同样分步执行  
>
> 2. **写屏障（Write Barrier）**：  
>    - 监控对象引用修改，防止增量标记期间漏标存活对象  
>    ```cpp
>    // 伪代码：写屏障示例
>    void Object::SetField(Object* newRef) {
>        if (GC.IsInMarkingPhase()) { 
>            GC.Mark(newRef);  // 如果对象的引用发生了修改，则立即标记新引用
>        }
>        this->field = newRef;
>    }
>    ```
>
> 3. **时间片控制**：  
>    - 每帧分配固定时间给GC（如2ms/帧）  
>    - 通过`GC.Collect(GC.MaxGeneration, GCCollectionMode.Optimized)`调节  
>
> ---
>
> ### **增量模式 vs 完全停止模式**
> | **对比维度** | **增量模式**            | **完全停止模式**      |
> | ------------ | ----------------------- | --------------------- |
> | 单次暂停时间 | 通常<5ms（分步完成）    | 可能>50ms（全量回收） |
> | 总GC耗时     | 略高（分步开销）        | 较低（一次性完成）    |
> | 帧率稳定性   | 更平滑（无长卡顿）      | 可能出现明显卡顿      |
> | 适用场景     | 实时应用（如60FPS游戏） | 后台服务、非实时应用  |
> | 内存碎片     | 可能更多（分步清扫）    | 相对较少              |
>
> ---
>
> ### **Unity推荐使用增量模式的原因**
> 1. **帧率稳定**：避免长时间GC暂停导致帧时间波动（如60FPS要求每帧<16.6ms）  
> 2. **用户体验**：减少游戏卡顿感，尤其在移动端（iOS/Android）性能敏感场景  
> 3. **硬件适配**：在低端设备上通过分步GC维持可玩性  
> 4. **兼容性**：IL2CPP后端与增量GC协作良好（相比Mono改进明显）  
>
> ---
>
> ### **性能优化建议**
> 1. **减少临时对象**：避免在Update()中频繁分配内存  
> 2. **池化技术**：重用对象（如子弹、粒子效果）  
>    ```csharp
>    public class BulletPool {
>        private Queue<Bullet> pool = new Queue<Bullet>();
>        
>        public Bullet GetBullet() {
>            return pool.Count > 0 ? pool.Dequeue() : new Bullet();
>        }
>        
>        public void Release(Bullet bullet) {
>            pool.Enqueue(bullet);
>        }
>    }
>    ```
> 3. **手动触发GC**：在加载场景时主动调用`GC.Collect()`  
> 4. **监控工具**：使用Unity Profiler的**Memory**模块分析GC行为  
>
> ---
>
> 通过结合Boehm GC的保守式设计与增量执行策略，Unity在跨平台兼容性和实时性能之间取得了平衡，成为游戏开发中的主流方案。





## 2.C#反射的开销

具体如下：

> #### 问题解析与解决方案说明
>
> 在 Unity 中，**反射（Reflection）** 虽然提供了运行时动态获取类型信息的能力，但会带来显著的性能损耗。由于 Mono 和 IL2CPP 会缓存所有反射对象（如 `Type`、`MethodInfo`），且这些对象不会被垃圾回收器（GC）回收，导致 GC 在应用生命周期内持续扫描这些对象，造成不必要的开销。以下为具体解释及优化方案：
>
> ---
>
> ### **问题根源**
> 1. **反射对象的缓存机制**  
>    - Unity 的运行时（Mono/IL2CPP）会将反射对象永久缓存，例如：
>      ```csharp
>      Type type = typeof(Player); // 此Type对象会被永久缓存
>      MethodInfo method = type.GetMethod("Attack"); // MethodInfo同样被缓存
>      ```
>    - 即使代码中不再使用这些对象，它们仍驻留内存，GC 需反复扫描。
>
> 2. **GC 开销的来源**  
>    - 缓存的大量反射对象会成为 GC 的“根”（Root），GC 每次执行时需遍历所有根对象，判断其引用链是否存活。
>    - 例如，若有 1000 个 `MethodInfo` 对象，GC 每帧需检查这 1000 个对象是否可达，即使它们实际未被使用。
>
> ---
>
> ### **优化策略：编辑时预处理**
> 将反射操作从运行时迁移到编辑时，通过代码生成或数据序列化，避免运行时动态反射。具体流程如下：
>
> #### 1. **编辑时扫描程序集**
>    - 使用 Unity Editor 脚本扫描项目中的程序集，提取所需类型信息。
>    - 例如，查找所有实现 `ISkill` 接口的类：
>      ```csharp
>      // Editor脚本示例：查找所有技能类
>      [InitializeOnLoad]
>      public class SkillScanner {
>          static SkillScanner() {
>              List<Type> skillTypes = new List<Type>();
>              foreach (Assembly assembly in AppDomain.CurrentDomain.GetAssemblies()) {
>                  foreach (Type type in assembly.GetTypes()) {
>                      if (typeof(ISkill).IsAssignableFrom(type)) {
>                          skillTypes.Add(type);
>                      }
>                  }
>              }
>              // 将类型列表序列化为配置文件
>              SaveSkillTypes(skillTypes);
>          }
>      }
>      ```
>
> #### 2. **生成静态代码或数据**
>    - **代码生成**：通过 `TextTemplate` 或 `StringBuilder` 生成硬编码的 C# 类。
>    - **数据序列化**：将提取的信息保存为 `JSON`/`ScriptableObject`，供运行时直接读取。
>
> ##### 示例：生成技能工厂类
> ```csharp
> // 生成的代码 SkillFactory.Generated.cs
> public static class SkillFactory {
>     private static Dictionary<string, Type> _skillTypes = new Dictionary<string, Type>() {
>         {"Fireball", typeof(FireballSkill)},
>         {"Heal", typeof(HealSkill)}
>     };
> 
>     public static ISkill CreateSkill(string skillName) {
>         if (_skillTypes.TryGetValue(skillName, out Type type)) {
>             return (ISkill)Activator.CreateInstance(type);
>         }
>         return null;
>     }
> }
> ```
>
> 注：
>
> > 在 Unity 中，这段 `SkillFactory` 代码确实 **使用了反射**，但通过一些设计优化了性能。以下是具体分析：
> >
> > ---
> >
> > ### **1. 反射的使用**
> > - `Activator.CreateInstance(type)` 是反射操作：它通过 `System.Type` 动态创建对象实例，而反射在 C# 中通常有性能开销（尤其是在高频调用时）。
> > - `_skillTypes` 字典中存储的 `Type` 对象是通过反射获取的（例如 `typeof(FireballSkill)`），但这一步是在类初始化时完成的，属于一次性开销。
> >
> > ---
> >
> > ### **2. 性能优化的关键点**
> > 尽管使用了反射，但这段代码通过以下方式优化了性能：
> >
> > #### **(1) 预缓存 Type 对象**
> > - 在静态字典 `_skillTypes` 中预先存储了所有技能类型对应的 `Type` 对象，避免了运行时频繁调用 `Type.GetType()` 或反射搜索程序集的性能开销。
> > - 类初始化阶段（`static` 构造函数或静态字段初始化）会一次性加载这些 `Type` 对象，后续直接通过字典查找，时间复杂度为 O(1)。
> >
> > #### **(2) 避免字符串解析**
> > - 通过硬编码的 `typeof(FireballSkill)` 直接获取 `Type`，而不是通过字符串名称（如 `Type.GetType("FireballSkill")`），避免了运行时解析类型名称的性能损耗。
> >
> > #### **(3) 工厂模式的隔离**
> > - 将反射操作封装在 `SkillFactory` 中，隔离了动态创建的代码，避免了散落在各处的反射调用，便于后续优化和维护。
> >
> > ---
> >
> > ### **3. Unity 中的反射性能问题**
> > - Unity 的 **Mono 和 IL2CPP 运行时** 对反射的支持有限，尤其是在 AOT（Ahead-of-Time）编译环境下（如 iOS），某些反射操作可能导致崩溃或性能骤降。
> > - `Activator.CreateInstance` 在 Unity 中虽然可用，但比直接 `new` 实例化慢得多。如果频繁调用（例如每帧创建技能），可能成为性能瓶颈。
> >
> > ---
> >
> > ### **4. 进一步优化的方案**
> > 如果这段代码需要更高性能，可以尝试以下优化策略：
> >
> > #### **(1) 预生成实例工厂**
> > - 使用委托或表达式树预编译实例化逻辑，替代反射：
> >   ```csharp
> >   private static Dictionary<string, Func<ISkill>> _skillFactories = new Dictionary<string, Func<ISkill>>() {
> >       {"Fireball", () => new FireballSkill()},
> >       {"Heal", () => new HealSkill()}
> >   };
> >   
> >   public static ISkill CreateSkill(string skillName) {
> >       if (_skillFactories.TryGetValue(skillName, out Func<ISkill> factory)) {
> >           return factory();
> >       }
> >       return null;
> >   }
> >   ```
> >   - 这种方式完全避免反射，直接调用构造函数。
> >
> > #### **(2) 使用对象池**
> > - 对于需要频繁创建/销毁的技能对象，使用对象池复用实例，减少动态内存分配。
> >
> > #### **(3) 代码生成工具**
> > - 通过 Unity 的 `ScriptableObject` 或自定义代码生成工具（如 T4 模板）生成工厂代码，避免运行时反射。
> >
> > #### **(4) 依赖注入框架**
> > - 使用像 `Zenject` 或 `VContainer` 这样的依赖注入框架，通过预注册类型解决实例化问题。
> >
> > ---
> >
> > ### **5. 总结**
> > - **这段代码用了反射**（`Activator.CreateInstance`），但通过预缓存 `Type` 对象降低了反射的运行时开销。
> > - **优化核心思想**：将反射操作从高频调用路径移动到低频的初始化阶段，同时通过字典快速查找类型。
> > - **适用场景**：适合技能类型较少、创建频率不高的项目。对于高频调用或移动端项目，建议采用更彻底的优化方案（如预编译工厂或对象池）。
>
> 
>
> #### 3. **运行时直接使用生成结果**
>
>    - 替代反射代码：
>      ```csharp
>      // 优化前（使用反射）：
>      Type skillType = Type.GetType(skillName);
>      ISkill skill = (ISkill)Activator.CreateInstance(skillType);
>      
>      // 优化后（使用生成的工厂类）：
>      ISkill skill = SkillFactory.CreateSkill(skillName);
>      ```
>
> ---
>
> ### **实际案例：事件系统优化**
> 假设需要实现一个基于字符串的事件监听系统，传统反射方案与优化方案对比如下：
>
> #### 传统方案（运行时反射）
> ```csharp
> // 订阅事件时通过反射查找方法
> public void SubscribeEvent(string eventName, object listener) {
>     MethodInfo method = listener.GetType().GetMethod("On" + eventName);
>     EventSystem.Register(eventName, method, listener);
> }
> 
> // 触发事件时反射调用
> public void TriggerEvent(string eventName) {
>     List<MethodInfo> methods = EventSystem.GetMethods(eventName);
>     foreach (var method in methods) {
>         method.Invoke(listener, null);
>     }
> }
> ```
> - **问题**：每次调用 `GetMethod` 和 `Invoke` 都会生成缓存对象，GC 持续扫描。
>
> #### 优化方案（编辑时生成）
> 1. **扫描标记的方法**  
>    使用 `[EventMethod]` 特性标记需要注册的方法：
>    ```csharp
>    public class Player {
>        [EventMethod("EnemyKilled")]
>        public void OnEnemyKilled() {
>            // 处理敌人被击杀的逻辑
>        }
>    }
>    ```
>
> 2. **生成事件映射代码**  
>    输出 `EventRegistry.Generated.cs`：
>    ```csharp
>    public static class EventRegistry {
>        private static Dictionary<string, List<Action>> _eventHandlers = 
>            new Dictionary<string, List<Action>>();
>    
>        static EventRegistry() {
>            RegisterEvent("EnemyKilled", new Action(Player.OnEnemyKilled));
>            // 其他事件注册...
>        }
>    
>        public static void Trigger(string eventName) {
>            foreach (var handler in _eventHandlers[eventName]) {
>                handler.Invoke();
>            }
>        }
>    }
>    ```
>
> 3. **运行时直接调用**  
>    ```csharp
>    EventRegistry.Trigger("EnemyKilled");
>    ```
> - **优势**：完全消除反射调用，无 GC 压力。
>
> ---
>
> ### **技术实现工具**
> 1. **Unity Editor 扩展**  
>    - 通过 `AssemblyDefinition` 获取程序集引用。
>    - 使用 `TypeCache` 快速过滤类型（Unity 2020.1+）。
>
> 2. **代码生成框架**  
>    - **T4 Templates**：Visual Studio 内置的文本生成引擎。
>    - **Roslyn API**：动态编译 C# 代码（需引用 `Microsoft.CodeAnalysis`）。
>
> 3. **序列化格式**  
>    - **ScriptableObject**：Unity 原生数据容器，可直接在 Inspector 中编辑。
>    - **JSON**：轻量级文本格式，配合 `JsonUtility` 或 `Newtonsoft.Json` 使用。
>
> ---
>
> ### **性能对比数据**
> | **指标**     | **反射方案**         | **代码生成方案**       |
> | ------------ | -------------------- | ---------------------- |
> | GC 内存开销  | 10-50 MB（缓存对象） | 0 MB（无反射对象）     |
> | 方法调用耗时 | 200-500 ns/次        | 1-2 ns/次              |
> | 启动时间     | +200 ms（首次加载）  | +10 ms（加载生成代码） |
>
> 通过将反射操作前置到编辑阶段，可彻底消除运行时的反射开销，同时避免 GC 对缓存对象的持续扫描。这种方案在大型项目（如开放世界游戏或 MMO）中尤为重要，能显著提升帧率和加载速度。



## 3.IL2CPP的介绍

[IL2CPP 的工作原理 - Unity 手册](https://docs.unity3d.com/cn/2021.1/Manual/IL2CPP-HowItWorks.html)

> 这东西水很深啊。。。