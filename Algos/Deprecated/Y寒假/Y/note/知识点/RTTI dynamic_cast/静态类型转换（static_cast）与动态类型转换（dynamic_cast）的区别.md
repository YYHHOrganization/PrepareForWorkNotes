### 静态类型转换（`static_cast`）与动态类型转换（`dynamic_cast`）的区别

| **特性**         | `static_cast`                            | `dynamic_cast`                    |
| ---------------- | ---------------------------------------- | --------------------------------- |
| **检查时机**     | 编译时                                   | 运行时（依赖 RTTI）               |
| **安全性**       | 不安全（可能未定义行为）                 | 安全（返回 `nullptr` 或抛出异常） |
| **适用场景**     | 相关类型转换（如数值、继承体系向上转换） | 多态类型的向下转换（基类→派生类） |
| **多态类型要求** | 不需要                                   | 必须（基类至少有一个虚函数）      |
| **性能**         | 零开销                                   | 运行时类型检查开销                |

---

### **`dynamic_cast` 的异常/错误场景**
1. **指针转换失败** → 返回 `nullptr`。
2. **引用转换失败** → 抛出 `std::bad_cast` 异常。

---

### **C++ 代码示例（VS2019 兼容）**

```cpp
#include <iostream>
#include <typeinfo> // 包含异常类型

class Base {
public:
    virtual ~Base() {} // 必须有多态性（虚函数）
};

class Derived : public Base {};
class Unrelated {};

int main() {
    // ------------------------- 示例1：指针转换 -------------------------
    Base* basePtr = new Derived; // 基类指针指向派生类对象

    // 正确：向下转换（安全）
    Derived* derivedPtr = dynamic_cast<Derived*>(basePtr);
    if (derivedPtr) {
        std::cout << "dynamic_cast 成功：Derived*" << std::endl;
    }

    // 错误：尝试转换为不相关的类
    Unrelated* unrelatedPtr = dynamic_cast<Unrelated*>(basePtr);
    if (!unrelatedPtr) {
        std::cout << "dynamic_cast 失败：返回 nullptr" << std::endl;
    }

    // ------------------------- 示例2：引用转换 -------------------------
    try {
        Base& baseRef = *basePtr; 
        Derived& derivedRef = dynamic_cast<Derived&>(baseRef); // 成功
        std::cout << "引用转换成功" << std::endl;

        // 尝试错误转换（引用必须捕获异常）
        Unrelated& unrelatedRef = dynamic_cast<Unrelated&>(baseRef);
    } catch (const std::bad_cast& e) {
        std::cout << "引用转换失败：" << e.what() << std::endl;
    }

    // ------------------------- 示例3：static_cast 风险 -------------------------
    Base* invalidBase = new Base; // 基类指针指向基类对象

    // 错误使用 static_cast 向下转换（未定义行为！）
    Derived* badDerived = static_cast<Derived*>(invalidBase);
    // 此处可能崩溃或数据损坏

    delete basePtr;
    delete invalidBase;
    return 0;
}
```

---

### **输出结果**
```text
dynamic_cast 成功：Derived*
dynamic_cast 失败：返回 nullptr
引用转换成功
引用转换失败：Bad cast
```

---

### **关键解释**
1. **`dynamic_cast` 必须用于多态类型**（基类有虚函数），否则编译失败。
2. **指针转换失败返回 `nullptr`**：需手动检查结果。
3. **引用转换失败抛出异常**：必须用 `try-catch` 捕获。
4. **`static_cast` 不安全**：它不会检查实际类型，直接按程序员意图转换，可能导致未定义行为。

---

### **何时使用 `dynamic_cast`？**
- 当需要将基类指针/引用安全地转换为派生类时。
- 需确保代码在多态类型上操作（基类有虚函数）。

---

### **注意事项**
- **性能**：频繁使用 `dynamic_cast` 可能影响性能（涉及 RTTI 查找）。
- **设计问题**：过度依赖类型转换可能暗示设计缺陷（考虑使用虚函数替代）。