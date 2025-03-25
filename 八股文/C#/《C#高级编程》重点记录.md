# 《C#高级编程》重点记录

阅读的是第11版。

# 第一章 .NET应用程序和工具

## 1 .NET Core和.Net Framework的联系

| **对比维度**   | **.NET Framework**             | **.NET Core**                                         | **联系与说明**                                               |
| -------------- | ------------------------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| **跨平台支持** | 仅Windows                      | Windows/Linux/macOS                                   | .NET 5+统一了二者，但历史项目仍需区分                        |
| **开源协议**   | 部分组件开源                   | 完全开源（MIT协议）                                   | 两者共享部分开源组件（如Roslyn编译器）                       |
| **部署模式**   | 需系统全局安装                 | 支持独立部署（自带运行时）                            | Core的独立部署包大小约50-150MB（含运行时）                   |
| **应用场景**   | WinForms/WPF/ASP.NET Web Forms | [ASP.NET](http://asp.net/) Core/微服务/跨平台控制台   | Core 3.0+支持Windows桌面应用                                 |
| **版本更新**   | 已停止大版本更新（最新4.8）    | 持续迭代（[现为.NET](http://xn--siq162g.net/) 6/7/8） | Framework建议仅维护旧项目，[新项目首选.NET](http://xn--efvt79a52s2wh0mb.net/) 6+ |
| **性能优化**   | 传统优化，适合单体应用         | 高性能（低延迟GC、SIMD指令）                          | Core的Kestrel比Framework的IIS吞吐量高5倍+                    |
| **依赖注入**   | 需第三方库（如Unity）          | 内置DI容器                                            | Core的DI支持构造函数注入、生命周期管理                       |
| **微服务支持** | 有限（需配合WCF）              | 原生支持（gRPC/Dapr）                                 | Core的微服务启动时间<100ms（Framework通常>1s）               |
| **CLI工具链**  | 依赖Visual Studio              | 完整跨平台CLI（dotnet命令）                           | Core支持`dotnet build`/`dotnet run`独立编译运行              |
| **Docker适配** | 镜像体积大（基于Windows镜像）  | 轻量镜像（Alpine镜像约100MB）                         | Core的Alpine镜像启动内存消耗<50MB                            |

总之就是现在能用.Net Core就用，Framework主要用于维护老项目。



## 2.IL & CLR

参考p 13 1.3.6节，公共语言运行库。在其他笔记里也有整理，这里可以重点看一下Unity的：

[Unity 中的 .NET 概述 - Unity 手册](https://docs.unity3d.com/cn/2021.1/Manual/overview-of-dot-net-in-unity.html)



# 第二章 核心C#

## 1.预定义的引用类型

C#支持两种预定义的引用类型：object和string。以下重点介绍一下：

> ### **C# 预定义引用类型 `object` 和 `string` 详解**
>
> ---
>
> ### **一、`object` 类型**
> #### **1. 基本概念**
> - **所有类型的基类**：在 C# 中，`object`（`System.Object`）是所有类型的根类型，无论是值类型（如 `int`、`struct`）还是引用类型（如 `string`、`class`），都隐式继承自 `object`。
> - **统一类型系统**：通过 `object`，值类型和引用类型可以在统一类型系统中操作（例如装箱和拆箱）。
>
> #### **2. `object` 提供的基本方法**
> `object` 类型定义了以下核心方法，所有类型默认继承这些方法：
>
> | 方法              | 作用                                                         |
> | ----------------- | ------------------------------------------------------------ |
> | **`Equals`**      | 比较两个对象是否相等。默认实现为引用相等（比较内存地址）。   |
> | **`GetHashCode`** | 返回对象的哈希码，用于哈希表（如 `Dictionary`）中的快速查找。默认实现与对象地址相关。 |
> | **`ToString`**    | 返回对象的字符串表示。默认返回类型全名（如 `"System.Object"`）。 |
> | **`GetType`**     | 返回对象的运行时类型信息（`Type` 对象）。不可被重写。        |
> | **`Finalize`**    | 析构方法，由垃圾回收器调用，用于清理非托管资源。             |
>
> #### **3. 其他重要内容**
> - **方法重写**：  
>   - 自定义类型通常需要重写 `Equals` 和 `GetHashCode`，以提供逻辑相等性（而非引用相等）。  
>   - 示例：两个 `Person` 对象在 `ID` 相同时应被视为相等，需重写 `Equals` 和 `GetHashCode`。
>   ```csharp
>   public class Person {
>       public int ID { get; set; }
>       public override bool Equals(object obj) => obj is Person p && p.ID == ID;
>       public override int GetHashCode() => ID.GetHashCode();
>   }
>   ```
>
> - **装箱与拆箱**：  
>   - **装箱**：将值类型转换为 `object` 时，值类型会被复制到堆中，产生性能开销。  
>   - **拆箱**：将 `object` 转换回值类型时，需显式类型转换，若类型不匹配会抛出 `InvalidCastException`。  
>   ```csharp
>   int num = 42;
>   object boxed = num;      // 装箱（堆分配）
>   int unboxed = (int)boxed; // 拆箱
>   ```
>
> - **类型检查**：  
>   - `is` 运算符：检查对象是否为指定类型（如 `if (obj is string)`）。  
>   - `as` 运算符：安全类型转换（失败返回 `null`）。  
>
> ---
>
> ### **二、`string` 类型**
> #### **1. 引用类型与堆分配**
> - **引用类型**：`string` 是引用类型，字符串数据存储在堆中，变量存储的是对堆内存的引用。  
> - **字符串赋值**：赋值时仅复制引用，而非实际数据。  
>   ```csharp
>   string a = "Hello";
>   string b = a;  // a 和 b 指向同一块堆内存
>   ```
>
> #### **2. 修改字符串的问题**
> - **不可变性**：`string` 是不可变的（Immutable），任何“修改”操作都会创建新字符串对象。  
>   - **示例**：字符串拼接会产生新对象。  
>   ```csharp
>   string s = "Hello";
>   s += " World"; // 创建新对象，s 指向新内存地址，原 "Hello" 仍存在于堆中。
>   ```
>   - **性能问题**：频繁修改字符串（如循环拼接）会导致大量临时对象，影响性能。建议使用 `StringBuilder`。
>
> - **实现原理**：  
>   - **不可变性机制**：`string` 的内部字符数组（`private readonly char[]`）在创建后无法修改。  
>   - **运算符重载**：`+` 运算符被重载为 `String.Concat`，每次拼接返回新对象。  
>
> #### **3. 其他重要内容**
> - **字符串驻留（Interning）**：  
>   - 编译器会将相同的字符串字面量指向同一内存位置，节省内存。  
>   ```csharp
>   string a = "Hello";
>   string b = "Hello";
>   bool isSame = object.ReferenceEquals(a, b); // true（驻留优化）
>   ```
>   - 可通过 `string.Intern` 手动驻留字符串。
>
> - **字符串比较**：  
>   - `==` 运算符被重载为值比较（比较内容，而非引用）。  
>   ```csharp
>   string a = "Hello";
>   string b = new string("Hello".ToCharArray());
>   bool isEqual = (a == b); // true（内容相同）
>   bool isRefEqual = object.ReferenceEquals(a, b); // false（不同引用）
>   ```
>
> - **特殊行为**：  
>   - 空字符串 `""` 和 `null` 是不同的概念。  
>   - 使用 `string.Empty` 表示空字符串，避免 `null` 引用异常。
>
> ---
>
> ### **总结**
> - **`object`**：作为类型系统的根，提供基础方法，需关注装箱/拆箱和类型安全。  
> - **`string`**：不可变的引用类型，通过驻留和运算符重载优化使用，需注意性能问题。



## 2.C#和C++ 的switch语句的不同

> **C++与C#的`switch`语句区别：**
>
> 1. **类型支持**  
>    - **C++**：仅支持整型（`int`、`char`等）和枚举类型。  
>    - **C#**：支持整型、枚举、字符串、`null`及模式匹配（C# 7.0+可匹配类型，如`case int i`）。
>
> 2. **执行流程控制**  
>    - **C++**：允许`case`穿透（无`break`会继续执行后续`case`代码）。  
>    - **C#**：强制每个`case`必须用`break`、`return`或`goto`显式终止，否则编译报错（防止意外穿透）。
>
> 3. **特殊处理**  
>    - **C#**：支持`case null`，可检测空引用；支持范围匹配（如`case > 10`）。  
>    - **C++**：仅支持常量值匹配，无空值或范围判断。
>
> **示例对比：**  
> ```c++
> // C++：允许穿透，类型受限
> switch (n) {
>     case 1: /* ... */ break;
>     case 2: /* 无break，继续执行case 3 */ 
>     case 3: /* ... */ break;
> }
> ```
>
> ```csharp
> // C#：禁止穿透，支持字符串和模式
> switch (s) {
>     case "A": break;  // 必须显式终止
>     case null: break; // 处理空值
>     case int i when i > 10: break; // 条件匹配
> }
> ```



## 3.集合概念初探

`foreach`可以用来遍历集合中的每一项。从技术上来看，要使用集合对象，必须支持`IEnumerable`接口。集合的例子有C#数组，System.collection名称空间里面的集合类，以及用于定义的集合类。

- 注意：`foreach`不能改变集合中各项的值，会编译失败。如果要改的话使用for循环来做。