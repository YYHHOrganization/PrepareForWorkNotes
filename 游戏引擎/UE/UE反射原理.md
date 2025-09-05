UE反射原理

**https://blog.csdn.net/hhw_hhw/article/details/139287867**

https://dev.epicgames.com/documentation/zh-cn/unreal-engine/reflection-system-in-unreal-engine

gemini排版后的内容，好像有简化：



# 【UE 反射】反射的原理是什么？如何使用机制？



---

## **目录**

*   **0. 拓展**
    *   0.1 静态类型检查
        *   0.1.1 静态类型检查的主要原理
        *   0.1.2 编译器的工作流程
        *   0.1.3 静态类型检查的优点和缺点
        *   0.1.4 示例
        *   0.1.5 C++也可以在运行时类型检查
    *   0.2 运行时动态类型检查
        *   0.2.1 主要特点
        *   0.2.2 动态类型检查的实现
        *   0.2.3 优缺点
    *   0.3 两种检查方式和反射的关系
        *   0.3.1 反射机制
        *   0.3.2 静态类型检查、动态类型检查和反射的联系
        *   0.3.3 示例对比
    *   0.4 偏移量在反射机制中的作用
*   **1. UE反射的原理**
    *   1.1 为什么UE要实现反射机制，而C++没有实现
        *   1.1.1 UE为什么要实现反射
        *   1.1.2 反射对蓝图脚本至关重要
        *   1.1.3 为什么C++没有实现反射
    *   1.2 UE是如何实现反射机制
        *   1.2.1 核心组件
        *   1.2.2 反射的实现步骤
        *   1.2.2 示例
*   **2. 使用UE反射机制**
    *   2.1 使用反射机制的前提
    *   2.2 使用反射API

---

## 0. 拓展

在开始介绍反射之前，我想先了解下不同的语言，不同的类型检查机制和反射的联系，以及偏移量在反射中的作用是什么。（这部分知识有利于反射机制的深入理解）

[官方参考文章](https://docs.unrealengine.com/5.3/en-US/unreal-engine-reflection-system/)

### 0.1 静态类型检查

静态类型检查是在 **编译时** 对程序中的所有变量和表达式进行类型检查，以确保每个操作数、变量、函数调用等的类型都是一致和兼容的。其中C、C++、Java、C#都是静态类型检查的语言。

#### 0.1.1 静态类型检查的主要原理

*   **类型声明和定义**
    在静态类型语言中，每个变量、函数参数和返回值等的类型在代码编写时就已经明确指定。这些类型信息是编译器进行类型检查的基础。
    ```cpp
    int a = 10;         // 变量a的类型是int
    double b = 20.5;    // 变量b的类型是double
    ```

*   **符号表（Symbol Table）**
    编译器在编译过程中维护一个符号表，用于存储所有变量、函数及其类型信息。符号表在语法分析阶段创建，并在语义分析阶段进行扩展和检查。

*   **类型推导**
    有些静态类型语言支持类型推导，编译器可以根据上下文自动推导出变量的类型（如C++中的`auto`关键字）。
    ```cpp
    auto x = 10;       // 编译器推导x的类型为int
    auto y = 20.5;     // 编译器推导y的类型为double
    ```

*   **类型检查**
    编译器在编译过程中对所有表达式和语句进行类型检查，以确保类型一致性。例如，变量赋值时检查类型兼容性，函数调用时检查参数类型匹配，运算符操作时检查操作数类型。
    ```cpp
    int a = 10;
    double b = 20.5;
    a = b;    // 编译器会警告或错误，类型不兼容
    
    void foo(int x) { }
    foo(b);   // 编译器会警告或错误，类型不兼容
    ```

*   **类型转换**
    静态类型语言通常支持显式类型转换和隐式类型转换。编译器在类型转换时进行检查，确保转换是合法的。
    ```cpp
    int a = 10;
    double b = static_cast<double>(a);  // 显式类型转换
    double c = a;                       // 隐式类型转换
    ```

#### 0.1.2 编译器的工作流程

1.  **词法分析（Lexical Analysis）**: 将源代码转换为一系列标记（tokens）。
2.  **语法分析（Syntax Analysis）**: 将标记组织成语法树（AST, Abstract Syntax Tree）。
3.  **语义分析（Semantic Analysis）**: 进行类型检查，建立和维护符号表。
4.  **中间代码生成（Intermediate Code Generation）**: 将语法树转换为中间表示（IR）。
5.  **优化（Optimization）**: 对中间代码进行优化。
6.  **目标代码生成（Code Generation）**: 将优化后的中间代码转换为目标机器代码。

#### 0.1.3 静态类型检查的优点和缺点

*   **优点**
    *   **提高性能**: 消除了运行时类型检查的开销，生成的代码更高效。
    *   **早期错误检测**: 类型错误在编译时被捕捉，减少了运行时错误。
    *   **代码可维护性**: 明确的类型定义提高了代码的可读性和可维护性。

*   **缺点**
    *   **灵活性较低**: 类型必须在编译时确定，减少了代码的灵活性。
    *   **开发速度较慢**: 需要显式地声明类型，增加了编码工作量。

#### 0.1.4 示例

以下是一个C++代码示例，演示了静态类型检查的基本原理：
```cpp
#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 3); // 编译时确定类型
    std::cout << "Result: " << result << std::endl;
    return 0;
}
```
通过静态类型检查，编译器可以在编译阶段发现并修正许多潜在的错误，提高程序的可靠性和性能。

#### 0.1.5 C++也可以在运行时类型检查

虽然C++主要依赖静态类型检查，但它也提供了多种机制支持运行时类型检查，如RTTI。接下来就详细介绍一下RTTI。

**RTTI（Runtime Type Information，运行时类型信息）**

RTTI是C++的一种机制，它允许程序在运行时获得类型相关的信息。

*   **RTTI基本原理**
    当一个类包含虚函数时，编译器会为它生成一个虚函数表（vtable），每个实例都有一个指向该表的指针（vptr）。RTTI信息（如`std::type_info`对象指针）也存储在虚函数表中。

*   **RTTI的实现**
    RTTI依赖于两个关键操作符：`typeid`和`dynamic_cast`。
    *   `typeid`：获取对象的类型信息。
        ```cpp
        #include <iostream>
        #include <typeinfo>
        
        class Base {
        public:
            virtual ~Base() = default;
        };
        
        class Derived : public Base {};
        
        int main() {
            Base* base = new Derived();
            std::cout << "Type of base: " << typeid(*base).name() << std::endl;
            delete base;
            return 0;
        }
        ```
    
        *   这个输出的是 Derived
    
        
    *   `dynamic_cast`：进行安全的多态类型转换。
    
        ```cpp
        #include <iostream>
        
        class Base {
        public:
            virtual ~Base() = default;
        };
        
        class Derived : public Base {
        public:
            void show() {
                std::cout << "Derived class method called" << std::endl;
            }
        };
        
        int main() {
            Base* base = new Derived();
            Derived* derived = dynamic_cast<Derived*>(base);
            if (derived) {
                derived->show();
            } else {
                std::cout << "dynamic_cast failed" << std::endl;
            }
            delete base;
            return 0;
        }
        ```
    
        *   输出 Derived class method called
    
* **RTTI的工作流程**

  1.  **编译时**: 编译器为每个包含虚函数的类生成vtable，并在其中添加指向`type_info`对象的指针。
  2.  **运行时**: `typeid`和`dynamic_cast`通过访问vtable中的类型信息来工作。

* **RTTI的限制**
  *   **性能开销**: 会增加一些运行时开销和内存占用。
  *   **仅适用于多态类**: 依赖于虚函数表，因此只适用于包含虚函数的类。
  *   **可移植性**: 不同编译器和平台对RTTI的实现可能有所不同。



好的，这是接续内容的排版：

### 0.2 运行时动态类型检查

运行时动态类型检查是在程序 **运行时** 进行类型检查，以确保操作数和表达式的类型是有效和兼容的。与静态类型检查不同，动态类型检查是在程序执行过程中进行的，这意味着类型信息在运行时确定。动态类型检查通常用于动态类型语言，如Python、JavaScript和Ruby。

#### 0.2.1 主要特点

*   **运行时确定类型**： 变量和表达式的类型在运行时确定，允许更灵活的编程方式。
*   **高灵活性**： 由于类型信息在运行时可用，可以方便地进行类型转换、动态类型检查和反射。
*   **潜在的性能开销**： 运行时类型检查增加了程序的运行时开销，可能会影响性能。
*   **延迟错误检测**： 类型错误在运行时被捕获，这可能导致运行时错误，增加调试和维护的复杂性。

#### 0.2.2 动态类型检查的实现

*   **Python**
    ```python
    def add(a, b):
        return a + b
    
    result = add(5, 3)  # 有效操作
    print(result)
    
    result = add("hello", "world")  # 有效操作，字符串拼接
    print(result)
    
    # result = add(5, "world")  # 无效操作，运行时会抛出 TypeError 异常
    # print(result)
    ```    在Python中，`add`函数可以接受任何类型的参数。如果参数类型不兼容，程序将在运行时抛出`TypeError`异常。

*   **JavaScript**
    ```javascript
    function add(a, b) {
        return a + b;
    }
    
    console.log(add(5, 3));  // 有效操作，结果是 8
    console.log(add("hello", "world"));  // 有效操作，结果是 "helloworld"
    console.log(add(5, "world"));  // 有效操作，JavaScript会进行隐式类型转换, 结果是 "5world"
    ```
    在JavaScript中，如果参数类型不兼容，例如将整数与字符串相加，JavaScript会进行隐式类型转换。

*   **Ruby**
    ```ruby
    def add(a, b)
      a + b
    end
    
    puts add(5, 3)  # 有效操作，结果是 8
    puts add("hello", "world")  # 有效操作，结果是 "helloworld"
    # puts add(5, "world")  # 无效操作，运行时会抛出 TypeError 异常
    ```
    在Ruby中，如果参数类型不兼容，程序将在运行时抛出`TypeError`异常。

#### 0.2.3 优缺点

*   **优点**
    *   **灵活性**: 允许变量在运行时改变类型，支持更多的编程模式，如鸭子类型（duck typing）。
    *   **快速开发**: 无需显式地声明类型，减少了编码工作量。
    *   **动态特性**: 支持反射、动态类型转换和动态方法调用等特性。

*   **缺点**
    *   **性能开销**: 运行时类型检查增加了额外的开销，影响了程序的执行效率。
    *   **延迟错误检测**: 类型错误在运行时捕捉，增加了调试和维护的难度。
    *   **类型安全性**: 可能会导致类型不安全的问题，增加了潜在的运行时错误。

---

### 0.3 两种检查方式和反射的关系

静态类型检查和动态类型检查都是类型系统的一部分，而反射机制则是与类型系统密切相关的高级特性。

#### 0.3.1 反射机制

*   **定义**: 反射是指程序在运行时能够检查和修改自身结构的能力，包括检查类、方法、属性等信息。
*   **特点**:
    *   **运行时类型信息**: 允许在运行时获取和操作类型信息。
    *   **动态性**: 支持动态调用方法、访问属性、创建对象等。
    *   **依赖语言支持**: 需要语言提供相应的反射API。
*   **优点**:
    *   **动态性和灵活性**：允许在运行时进行动态操作。
    *   **适用于框架和库**：如依赖注入、ORM等场景。
*   **缺点**:
    *   **性能开销**：反射操作通常比直接调用更慢。
    *   **安全性问题**：反射可能绕过类型检查，导致潜在的安全问题。
    *   **代码复杂性**：反射增加了代码的复杂性和维护难度。
*   **示例语言**: Java、C#、Python

#### 0.3.2 静态类型检查、动态类型检查和反射的联系

*   **类型系统的基础**:
    *   静态类型检查在 **编译时** 确定类型。
    *   动态类型检查在 **运行时** 确定类型。
*   **反射的实现依赖**:
    *   **静态类型语言** 通过编译时生成的元数据和运行时类型信息（RTTI）实现反射。
    *   **动态类型语言** 天然支持反射，因为类型信息在运行时就可用。
*   **灵活性和性能的权衡**:
    *   **静态类型检查** 提供了更好的性能和类型安全性，但灵活性较低。
    *   **动态类型检查** 提供了更高的灵活性，但带来了性能和类型安全性的挑战。
    *   **反射** 增加了动态性，但也带来了额外的性能开销和潜在的安全问题。

#### 0.3.3 示例对比

*   **静态类型语言中的反射（Java）**:
    ```java
    // 示例类
    class ExampleClass {
        public void exampleMethod() {
            System.out.println("Method called through reflection!");
        }
    }
    
    public class Main {
        public static void main(String[] args) throws Exception {
            // 1. 通过类名获取Class对象
            Class<?> clazz = Class.forName("ExampleClass");
    
            // 2. 创建该类的实例
            Object obj = clazz.getDeclaredConstructor().newInstance();
    
            // 3. 获取名为"exampleMethod"的方法对象
            Method method = clazz.getMethod("exampleMethod");
    
            // 4. 调用方法
            method.invoke(obj);
        }
    }
    ```

*   **动态类型语言中的反射（Python）**:
    ```python
    # 定义一个示例类
    class ExampleClass:
        def example_method(self):
            print("Method called through reflection!")
    
    # 创建ExampleClass的实例
    instance = ExampleClass()
    
    # 使用getattr函数获取实例中的example_method方法
    method = getattr(instance, "example_method")
    
    # 调用获取到的方法
    method()
    ```

---

### 0.4 偏移量在反射机制中的作用

在 Unreal Engine（UE）的反射机制中，**偏移量（offset）** 扮演着至关重要的角色。它是实现运行时动态访问和操作对象属性和方法的基础之一。

**偏移量在反射机制中的作用：**

*   **属性访问**：
    反射机制通过属性的偏移量来直接访问对象内存中的成员变量。当需要读取或修改对象的某个属性值时，UE反射系统会找到该属性的偏移量，然后直接定位到内存中的相应位置。

*   **内存布局解析**：
    偏移量帮助引擎解析和理解对象的内存布局。反射系统需要知道每个属性在对象内存中的具体位置，以便能够正确地进行读写操作。

*   **序列化和反序列化**：
    在对象的序列化（保存）和反序列化（加载）过程中，偏移量起着重要作用。通过偏移量，反射系统可以精确地读取或写入每个属性的值。

#### 实际应用

**示例：使用反射机制访问属性**

```cpp
#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "MyObject.generated.h"

UCLASS()
class UMyObject : public UObject
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "MyCategory")
    int32 MyIntProperty;
};

// 示例：使用反射访问属性
void AccessPropertyWithReflection()
{
    UMyObject* MyObject = NewObject<UMyObject>();
    MyObject->MyIntProperty = 42;

    // 获取属性的UProperty对象
    FProperty* Property = FindField<FProperty>(UMyObject::StaticClass(), "MyIntProperty");

    if (Property)
    {
        // 获取属性的偏移量
        int32 Offset = Property->GetOffset_ForInternal();

        // 通过偏移量计算属性的内存地址并访问
        int32* PropertyAddress = (int32*)((uint8*)MyObject + Offset);
        UE_LOG(LogTemp, Log, TEXT("MyIntProperty value: %d"), *PropertyAddress);
    }
}
```
在这个示例中，我们通过反射机制获取了 `MyIntProperty` 的偏移量，并使用该偏移量成功访问了属性的值。通过理解和正确使用偏移量，可以更好地利用 UE 的反射机制，实现动态属性访问和操作。

