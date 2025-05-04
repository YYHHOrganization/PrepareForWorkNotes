# Effective C++学习

参考：https://www.illurin.com/articles/effective-cpp/#post-comment (主要看这个)

https://github.com/GunterMueller/Books-3/blob/master/Effective%20C%2B%2B%203rd%20ed.pdf

以下会结合原文和自己的理解对参考文章进行对应的补充。没有额外补充的条款则只记录标题,剩下的去上面的链接中看。



# 一、让自己习惯C++

## 1.视C++为一个语言联邦

C++ 拥有多种不同的编程范式，而这些范式集成在一个语言中，使得 C++ 是一门即灵活又复杂的语言：

- 传统的面向过程 C：区块，语句，预处理器，内置数据类型，数组，指针。
- 面向对象的 C with Classes：类，封装，继承，多态，动态绑定。
- 模板编程 Template C++ 和堪称黑魔法的模板元编程（TMP）。
- C++ 标准库 STL。

牢记上述的四种次语言，后面还会有更多介绍。



## 2.尽量以const, enum, inline 替换 #define

> 总结：
>
> - 对于单纯常量，最好以constexpr/const对象或enums替换#define
> - 对于形似函数的宏，最好改用inline函数替换#define。

在原书写成时 C++11 中的`constexpr`还未诞生，现在一般认为应当用`constexpr`定义编译期常量来替代大部分的`#define`宏常量定义。例如：

```c++
constexpr auto aspect_ratio = 1.653;
```

我们也可以将编译期常量定义为类的静态成员：

```c++
class GamePlayer {
public:
    static constexpr auto numTurns = 5; //注意这里用static，因为要确保该常量至多有一份实体
    int scores[numTurns];
};
```

如果老的编译器不支持上述语法，则声明写在头文件里（不赋初值），然后在实现文件中给出常量的定义。



`enum`可以用于替代整型的常量，并且在模板元编程中应用广泛（见条款 48）：以下这个叫做`enum hack`。

```c++
class GamePlayer {
public:
    enum { numTurns = 5 };
    int scores[numTurns];
};
```

其理论基础在于，一个属于枚举类型的数值可以充当int被使用。这往往是合理的：

- （1）enum hack的行为比较接近#define而不是const。例如对const常量取地址是合法的，但对#define和enum取地址则不合法。
  - 同时，虽然优秀的编译器不会为“整数型const对象”设定额外的存储空间（除非用指针或引用指向它），但并不一定保证。而enums和#define一样绝对不会导致非必要的内存分配。
- （2）enum hack同时也是模板元编程的基础技术（见条款48）.



大部分`#define`宏常量应当用内联模板函数替代：

```c++
#define CALL_WITH_MAX(a, b) f((a) > (b) ? (a) : (b))
```

以上这种宏务必注意**所有实参要加上小括号。**宏的好处是不会招致函数调用带来的额外开销，但可读性是比较差的。但即使加了括号，也会出现调用错误的情况，比如下面：

```c++
int a = 5, b = 0;
CALL_WITH_MAX(++a, b); //a会被累加两次，不满足本意
CALL_WITH_MAX(++a, b+10);
```

因此，更好的做法是把上面的宏替换为：

```c++
template<typename T>
inline void CallWithMax(const T& a, const T& b) {
    f(a > b ? a : b);
}
```



## 3.尽可能使用const

> Take Away：
>
> - （1）将某些东西声明为const可以帮助编译器检测出错误用法，const可以被施加于任何作用域内的对象，函数参数，函数返回类型，成员函数本体；
> - （2）编译器强制实施bitwise constness，但我们编写程序时应该使用conceptual constness；
> - （3）当const和non-const成员函数有实质等价的实现时，令non-const版本调用const版本可以避免代码重复。

若你想让一个常量只读，那你应该明确说出它是const常量，对于指针来说，更是如此：

```c++
char greeting[] = "Hello";
char* p = greeting;                // 指针可修改，数据可修改
const char* p = greeting;          // 指针可修改，数据不可修改
char const* p = greeting;          // 指针可修改，数据不可修改
char* const p = greeting;          // 指针不可修改，数据可修改
const char* const p = greeting;    // 指针不可修改，数据不可修改
```



对于 STL 迭代器，分清使用`const`还是`const_iterator`：

```c++
const std::vector<int>::iterator iter = vec.begin();    // 迭代器不可修改，数据可修改
std::vector<int>::const_iterator iter = vec.begin();    // 迭代器可修改，数据不可修改
```

注：

- `const std::vector<int>::iterator iter`:相当于迭代器本身是const的，表示其不得指向别的东西，但指到的东西可以改值。
- `std::vector<int>::const_iterator cIter`:迭代器可以改指向，但指向的值不能改。



面对函数声明时，**如果你不想让一个函数的结果被无意义地当作左值，请使用const返回值：**

```c++
const Rational operator*(const Rational& lhs, const Rational& rhs);
```

如果返回类型不是const，则可能会产生如下的暴行：
```c++
Rational a, b;
(a*b) = c; //在a*b的结果上调用operator =
```

所以为了避免这种奇怪的操作，需要正确地将返回值设定为const。



### （1）const成员函数

const成员函数允许我们操控const对象，这在传递常引用时显得尤为重要：

```c++
class TextBlock {
public:
    const char& operator[](std::size_t position) const {    // const对象使用的重载
        return text[position];
    }

    char& operator[](std::size_t position) {                // non-const对象使用的重载
        return text[position];
    }

private:
    std::string text;
};
```

这样，const和non-const对象都有其各自的重载版本：

```c++
void Print(const Textblock& ctb) {
    std::cout << ctb[0];            // 调用 const TextBlock::operator[]
}
```

编译器对待const对象的态度通常是 bitwise constness，而我们在编写程序时通常采用 logical constness，这就意味着，在确保客户端不会察觉的情况下，我们认为const对象中的某些成员变量应当是允许被改变的，使用关键字`mutable`来标记这些成员变量（`即有些成员变量可能总是会被更改，即使他们在const成员函数内。`）：

```c++
class CTextBlock {
public:
    std::size_t Length() const;

private:
    char* pText;
    mutable std::size_t textLength;
    mutable bool lengthIsValid;
};

std::size_t CTextBlock::Length() const {
    if (!lengthIsValid) {
        textLength = std::strlen(pText);    // 可以修改mutable成员变量
        lengthIsValid = true;               // 可以修改mutable成员变量
    }
    return textLength;
}
```



> 补充：
>
> 在 **Effective C++** 中，**bitwise constness**（位常量性）和 **logical constness**（逻辑常量性）是两种不同的 **const 成员函数** 的约束方式，它们的区别如下：
>
> ---
>
> ### **1. Bitwise Constness（位常量性）**
> - **定义**：  
>   一个成员函数是 **bitwise const** 当且仅当它 **不修改对象的任何成员变量（即不改变对象的二进制位）**。  
>   
>   - 编译器检查的是 **物理内存是否被修改**，而非逻辑行为。
>   
> - **特点**：
>   - **严格**：即使修改的是指针指向的数据或 mutable 成员，只要对象本身的二进制位不变，编译器就认为合法。
>   - **C++ 默认标准**：`const` 成员函数默认遵循 bitwise constness。
>
> - **例子**：
>   ```cpp
>   class MyClass {
>   public:
>       int* ptr;
>       int getValue() const { 
>           return *ptr;  // bitwise const（ptr 本身未修改，但可能修改 *ptr）
>       }
>   };
>   ```
>   - 虽然 `getValue()` 是 `const`，但它可能间接修改 `*ptr`，但编译器不会报错（因为 `ptr` 的地址未变）。
>
> ---
>
> ### **2. Logical Constness（逻辑常量性）**
> - **定义**：  
>   一个成员函数是 **logical const** 当且仅当它 **不修改对象的逻辑状态**（即用户可见的状态）。  
>   - 允许修改 **对用户不可见的内部状态**（如缓存、计数器等）。
>
> - **特点**：
>   - **灵活**：通过 `mutable` 关键字标记可修改的成员变量，绕过 bitwise constness 的限制。（主要是因为编译器本身是bitwise constness的）
>   - **更符合设计意图**：即使物理内存被修改，只要逻辑状态不变，就认为是常量函数。
>
> - **例子**：
>   ```cpp
>   class MyClass {
>   private:
>       mutable int cache;  // 允许在 const 函数中修改
>       bool cacheValid;
>   public:
>       int getValue() const {
>           if (!cacheValid) {
>               cache = computeValue();  // 修改 mutable 成员
>               cacheValid = true;
>           }
>           return cache;
>       }
>   };
>   ```
>   - `getValue()` 是逻辑常量，尽管修改了 `cache`，但对用户来说对象的逻辑状态未变。
>
> ---
>
> ### **3. 核心区别**
> | **特性**     | **Bitwise Constness**                | **Logical Constness**                |
> | ------------ | ------------------------------------ | ------------------------------------ |
> | **检查标准** | 不修改对象的任何物理内存（二进制位） | 不修改对象的逻辑状态（用户可见状态） |
> | **灵活性**   | 低（严格按内存是否变化判断）         | 高（允许通过 `mutable` 绕过限制）    |
> | **适用场景** | 默认行为，编译器强制检查             | 需要缓存、延迟计算等优化场景         |
> | **代码示例** | `const` 函数不直接修改成员变量       | `const` 函数可修改 `mutable` 成员    |
>
> ---
>
> ### **4. 为什么需要区分？**
> - **Bitwise constness** 是编译器的底层约束，但可能 **过于严格**（如无法实现缓存优化，比如上面示例中的cacheValid，不设置为mutable的话编译器会报错，但完全符合logical constness）。
> - **Logical constness** 是程序员的设计意图，通过 `mutable` 实现 **逻辑上的常量性**，同时保持灵活性。
>
> ---
>
> ### **总结**
> - 如果只关心 **物理内存是否被修改**，用 **bitwise constness**（默认行为）。
> - 如果需要 **逻辑上的常量性**（如缓存、调试计数），用 **logical constness**（结合 `mutable`）。  
>   ——这正是 **Effective C++ 条款 3**（尽可能用 `const`）讨论的关键点。



在重载const和non-const成员函数时，需要尽可能避免书写重复的内容，**这促使我们去进行常量性转除（指的是例如在实际内部实现时，非const函数的实现版本调用const的实现版本）**。在大部分情况下，我们应当避免转型的出现，但在此处为了减少重复代码，转型是适当的：

```c++
class TextBlock {
public:
    const char& operator[](std::size_t position) const {

        // 假设这里有非常多的代码

        return text[position];
    }

    char& operator[](std::size_t position) {
        //前面的const_cast用于去除const版本[]返回值中的const，而后面的static_cast则强制进行一次安全转型（安全，使用static_cast，将non-const对象转为const对象）
        return const_cast<char&>(static_cast<const TextBlock&>(*this)[position]);
    }

private:
    std::string text;
};
```

> 上述代码可能会有点丑，但至少“运用const成员函数实现出其non-const孪生兄弟”的技术是值得了解的。

需要注意的是，反向做法：令const版本调用non-const版本以避免重复——并不被建议，一般而言const版本的限制比non-const版本的限制更多，因此这样做会带来风险。



## 4.确定对象被使用前已先被初始化

> Take Away：
>
> - （1）为内置型对象进行手工初始化，因为C++不保证初始化他们；
> - （2）构造函数最好使用初始化列表，尽量不要在构造函数本体内使用赋值操作。初始值列表列出的成员变量，最好排列次序和他们在class中的声明次序相同；
> - （3）为免除“跨编译单元之初始化次序”问题，请以local static对象替换non-local static对象。

无初值对象在 C/C++ 中广泛存在，因此这一条款就尤为重要。在定义完一个对象后需要尽快为它赋初值：

```c++
int x = 0;
const char* text = "A C-style string";

double d;
std::cin >> d;
```

对于类中的成员变量而言，我们有两种建议的方法完成初始化工作，一种是直接在定义处赋初值（since C++11）：

```c++
class CTextBlock {
private:
    std::size_t textLength{ 0 };
    bool lengthIsValid{ false };
};
```

另一种是使用构造函数成员初始化列表：

```c++
ABEntry::ABEntry(const std::string& name, const std::string& address,
                 const std::list<PhoneNumber>& phones)
    : theName(name),
      theAddress(address),
      thePhones(phones),
      numTimesConsulted(0) {}
```

> 使用初始化列表的构造函数相比直接在构造函数内赋值来说，通常效率更高。基于赋值的那个版本首先调用default构造函数为变量设定初值，然后立刻对他们赋予新值，此时default构造函数的一切作为因此就浪费了。而使用成员初始化列表则可以规避这个问题（使用初始化列表中的初值进行拷贝构造）。

成员初始化列表也可以留空用来执行默认构造函数：

```c++
ABEntry::ABEntry()
    : theName(),
      theAddress(),
      thePhones(),
      numTimesConsulted(0) {}
```

需要注意的是，**类中成员的初始化具有次序性，而这次序与成员变量的声明次序一致，与成员初始化列表的次序无关。**基类更早于派生类被初始化。为了避免出现阅读上的不好理解，最好在使用初始化列表时，跟声明次序保持一致。

> 类中成员的初始化是可选的，但是引用类型和const类型必须初始化。



### （1）静态对象的初始化

C++ 对于定义于不同编译单元内的全局静态对象的初始化相对次序并无明确定义（C++对“定义于不同的编译单元内的non-local static对象”的初始化相对次序没有明确定义。毕竟正确决定全局静态变量初始化顺序对编译器来说是相当困难的，甚至是做不到的），因此，以下代码可能会出现使用未初始化静态对象的情况：

> 所谓编译单元，是指产出单一目标文件（object file）的那些源码。基本上它是单一源码文件加上其所包含的头文件。

```c++
// File 1
extern FileSystem tfs;

// File 2
class Directory {
public:
    Directory() {
        FileSystem disk = tfs;
    }
};

Directory tempDir;
```

在上面这个例子中，你无法确保位于不同编译单元内的`tfs`一定在`tempDir`之前初始化完成。

这个问题的一个有效解决方案是采用 **Meyers’ singleton**，将全局静态对象转化为局部静态对象（这些函数同时也是绝佳的inlining候选人，尤其如果他们被频繁调用的话，见条款30）：

```c++
FileSystem& tfs() {
    static FileSystem fs;
    return fs;
}

Directory& tempDir() {
    static Directory td;
    return td;
}
```

这个手法的基础在于：C++ 保证，函数内的局部静态对象会在**该函数被调用期间**和**首次遇上该对象之定义式**时被初始化。

当然，这种做法对于多线程来说并不具有优势，最好还是在单线程启动阶段手动调用函数完成初始化。

> 这些函数内含static对象的事实使他们在多线程系统中带有不确定性。任何一种non-const static对象（不管是local还是non-local），在多线程环境下“等待某事发生”都会有麻烦。**一种解决方案是在程序的单线程启动结点手工调用所有reference-returning函数，可以有效消除与初始化有关的“竞速形式 race conditions”**
>
> 但注意，C++ 11中以下magic static的方法已经是线程安全的了：
>
> ```c++
> Foo& getFoo() {
>     static Foo foo;  // C++11 起线程安全
>     return foo;
> }
> ```
>
> 具体如下（==但实际感觉只要记住C++ 11即可，毕竟现在不用C++ 11的系统应该没那么多了。==**C++11 已成为行业最低标准**：Unity、UE、Maya、Houdini 等主流工具均已支持。）：
>
> | **方案**               | **适用场景**                  | **线程安全性** | **备注**             |
> | ---------------------- | ----------------------------- | -------------- | -------------------- |
> | **单线程提前初始化**   | C++03 或无法使用 C++11 的情况 | ✅ 安全         | 需手动管理初始化时机 |
> | **C++11 magic static** | C++11 及以上                  | ✅ 安全         | 最简单、推荐方式     |
> | **双重检查锁定**       | C++03                         | ⚠️ 需谨慎实现   | 容易出错，不推荐     |
> | **`std::call_once`**   | C++11                         | ✅ 安全         | 比双重检查锁定更可靠 |



# 二、构造/析构/赋值运算