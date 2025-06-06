# C++ 面经合集

这篇笔记记录所有牛客和其他地方见到的C++面经题目，由于内容非常多，因此比较基础的部分不会给出完全详细的解答，但会给出参考的链接。对于一些题目来说，会给出可执行的代码以方便理解。



# 一、关键词相关

## 1.C++中static和const的区别

### （1）static关键字

【参考资料】《游戏引擎架构》P111、[static静态局部变量初始化问题 - 不想写代码的DBA - 博客园](https://www.cnblogs.com/novice-dxx/p/7094690.html)

static即静态的意思，可以对变量和函数进行修饰。分三种情况：

- （1）当用于文件作用域的时候（即在.h/.cpp文件中直接修饰变量和函数），static意味着这些变量和函数只在本文件可见，其他文件是看不到也无法使用的，可以避免重定义的问题。
- （2）当用于函数作用域时，即作为局部静态变量时，意味着这个变量是全局的，只会进行一次初始化，不会在每次调用时进行重置，但只在这个函数内可见。
- （3）当用于类的声明时，即静态数据成员和静态成员函数，static表示这些数据和函数是所有类对象共享的一种属性，而非每个类对象独有。
  - static变量在类的声明中不占用内存，**因此必须在.cpp文件中定义类静态变量以分配内存。**文件域的静态变量和类的[静态成员变量](https://zhida.zhihu.com/search?content_id=180938976&content_type=Article&match_order=1&q=静态成员变量&zhida_source=entity)在main执行之前的静态初始化过程中分配内存并初始化；局部静态变量在第一次使用时分配内存并初始化。

> 这篇也值得看一下：[C++中static变量的初始化_static 变量初始化-CSDN博客](https://blog.csdn.net/qq_34139994/article/details/105157313)，有一些关于初始化时机的问题。渲染器中有遇到过类的static成员需要在外面初始化的问题。



### （2）const关键字

这里提及三件事：（1）**const的作用？** （2）**指针常量与常量指针** （3）**const重载问题**

【参考资料】《C++ Primer 第五版》2.4节。

#### （a）const的基本知识点

- const对象一旦创建后其值就不能改变，因此const对象必须初始化。
- 默认情况下，const对象只对文件内有效。默认当多个文件中出现了同名的const变量时，等同于在不同文件中分别定义了独立变量；如果想要跨文件共享，在const变量的声明和定义前都加`extern`关键字即可。
- 以下代码会有问题么？答案在C++ Primer p55页，是非法的

```c++
double dval = 3.14;
const int& val = dval;
int& val2 = val; //非法行为，C++的实现是用了一个temp值

//C++内部实现
int tmp = dval;
const int& val = tmp;
int& val2 = val;

//以下的代码也是不行的:
int a = 3;
const int& b=a;
int& c = b;
```

- const修饰符用来定义常量，具有不可变性。在类中，被const修饰的成员函数，不能修改类中的数据成员；



#### （b）指针和const

以下是一个常量指针（指向常量的指针，不能改变指向对象的值，但是可以改变指向）的例子：

```c++
const double pi = 3.14;
const double* p = &pi; //常量const 指针*， 所以是常量指针，回忆一下解释p是什么的时候我们会从右往左解释，p is a pointer which point to const

//*p = 5.0; //非法
const double e = 2.71828;
p = &e; //ok
```



而以下则是一个指针常量（指针本身是常量，指向不能改，但指向的对象可以改）

```c++
int pi = 3.14;
//int* const p; //Error,必须要初始化
int* const q = &pi; //中文读：指针 常量，英文意思从右往左看
*q = 3.15; //ok  
```

> 总结：**指针常量指的是该指针本身是一个常量，不能被修改，但是指针指向的对象可以被修改，常量指针指的是这个指针指向的对象是一个常量，不能被修改，但是指针本身可以被修改。**
>
> 这涉及到一个顶层const和底层const的概念：顶层const，本身是const，底层const，指向的对象是const；



##### 顶层const与底层const

指针本身是一个对象，它又可以指向另一个对象，这其实是两个相互独立的问题。这就引出了顶层const与底层const的概念。顶层const意味着指针本身是const，而底层const则表示指针所指向的对象是const。更一般地，**顶层const可以表示任意的对象是常量（包括指针、类、基本数据类型等）**，底层const则与指针或引用的基本类型部分有关。指针既可以是顶层const也可以是底层const，来看下面这个例子：
```c++
int i = 0;
int* const p1 = &i; //指针是顶层const
const int c1 = 42; //顶层const,基本数据类型
const int *p2 = &c1; //底层const
const int* const p3 = p2; //靠右的const是顶层const,靠左的const是底层const
const int& r = c1; //底层const,声明引用的const都是底层const
```

当执行对象的拷贝操作时，常量是顶层const和底层const具有明显的差异。其中顶层const并不会有什么影响：

```c++
 i = c1; //没有问题, c1是顶层const,对此操作无影响
 p2 = p3; //没有问题,p2和p3指向的对象类型相同,p3顶层const的部分不影响
```

执行拷贝操作并不会改变被拷贝对象的值，因此被拷入拷出的对象是否为常量都不影响。**但注意，在拷贝的过程中，拷入和拷出的对象必须具备相同的底层const资格。一般来说，非常量可以转换为常量，而反过来则不行。**来看下面这个例子：

```c++
//int *p = p3; //Error,p3包含底层const的定义,而p则没有
p2 = p3; //没有问题,p2是底层const,而p3也有底层const的定义
p2 = &i; //正确,int* 可以转换为const int*
//int &r = c1; //Error,c1不具备底层const的含义
const int &r2 = i; //可以
```

> 吐槽：C++。。。



#### （c）const成员函数重载问题

- const修饰的函数可以重载。
- const成员函数既不能改变类内的数据成员，也无法调用非const的成员函数；
- const类对象只能调用const成员函数，非const对象无论是否是const成员函数都能调用，**但是如果有重载的非const函数，非const对象会优先调用重载后的非const函数。**

> 这部分剩下的遇到题再整理吧。



### （3）二者联系

[C++ static、const 和 static const 类型成员变量声明以及初始化 | 菜鸟教程](https://www.runoob.com/w3cnote/cpp-static-const.html)

一个结论：

- **`static` 对象**：
  - 存放在静态存储区。
  - 在程序启动时初始化。
    - 注：函数内的 `static` 变量采用了懒汉式初始化（Lazy Initialization），即只有在第一次被访问时才会进行初始化。这种特性使得函数内部的 `static` 变量具有延迟加载的优点。
    - C++11 及以后的标准保证了对函数内 `static` 变量的初始化是线程安全的，即多线程环境下，多个线程不会竞态地初始化同一个 `static` 变量。（游戏开发对多线程暂时是不是不需要了解这么多？有被问到或者复习到了再说吧）
- **`const` 对象**：
  - 可以存放在静态存储区或栈上，具体取决于它的定义上下文。
  - 全局和静态 `const` 对象在程序启动时初始化，局部 `const` 对象在其作用域内初始化。



## 2.new/delete、malloc/free

Q：C++和C分别使用什么函数来做内存的分配和释放？有什么区别，能否混用？

可以参考的链接：[C++中new申请的内存， 可以用free释放吗？_new一个数组用free来释放-CSDN博客](https://blog.csdn.net/Dream_xun/article/details/50347139)

> C使用malloc/free，C++使用new/delete，前者是C语言中的库函数，后者是C++语言的运算符，对于自定义对象，malloc/free只进行分配内存和释放内存，无法调用其构造函数和析构函数，只有new/delete能做到，完成对象的空间分配和初始化，以及对象的销毁和释放空间，**不能混用**，具体区别如下：
>
> （1）new分配内存空间无需指定分配内存大小，malloc需要；
>
> （2）new返回类型指针，类型安全，malloc返回void*，再强制转换成所需要的类型；
>
> （3）new是从自由存储区获得内存，malloc从堆中获取内存；
>
> （4）**对于类对象，new会调用构造函数和析构函数，malloc不会（核心）**。

其他可能的考点：

- C++中的自由存储区：通过new和delete分配和释放空间的内存，具体实现可能是堆或者内存池。
  - 补充：堆是C和操作系统的术语，自由存储区是C++的术语，指的是通过new和delete动态分配和释放对象的抽象概念；基本上C++也会用堆区实现自由存储，但程序员可以通过重载操作符，改用其他内存实现自由存储，比如全局变量做的对象池。
- ==todo:C++ 重载new运算符（能否重载delete？）自由存储区创建的demo，后面整理到其他部分.==



# 二、常见基础问题

## 1.面向对象三大特征

[面向对象的三大基本特征，五大基本原则 - 风之之 - 博客园](https://www.cnblogs.com/fzz9/p/8973315.html)

这里对访问修饰符的复习可以看这里：[C++ 类访问修饰符 | 菜鸟教程](https://www.runoob.com/cplusplus/cpp-class-access-modifiers.html)。这个链接中关于继承的访问修饰符有一些说明，可以复习的时候看。

> 这里补充一下关于protected访问修饰符的概念：**protected（受保护）**成员变量或函数与私有成员十分相似，但有一点不同，protected（受保护）成员在派生类（即子类）中是可访问的。看下面这个例子理解protected的作用：
> ```c++
> #include <iostream>
> using namespace std;
> 
> class Rectangle
> {
>  protected:
>      double w,h;
>  public:
>      Rectangle(double w, double h): w(w), h(h){}
>      virtual void print()
>      {
>          cout<< " Rectangle "<<endl;
>          cout<<w<< " "<<h<<endl;
>      }
> };
> 
> class Square: Rectangle //注意：默认的是private继承，此时父类的protected变量在子类会降级为private，这样继承自Square的类就无法再访问w和h变量了
> {
> public:
>  // Square 类的构造函数应确保通过 Rectangle 的构造函数初始化宽度和高度。直接赋值w(r),h(r)是错误的,
>  // 因为派生类需要通过调用基类的构造函数来正确地初始化基类部分。只有在基类的构造函数被调用后，基类的成员变量才会被正确地构造。
>  Square(double r): Rectangle(r,r){}
>  virtual void print() override //使用 override 明确表示覆盖基类虚函数
>  {
>      cout<< " Square "<<endl;
>      cout<<w<< " "<<h<<endl;
>  }
> };
> 
> int main()
> {
>  Rectangle r(3.5, 1.5);
>  r.print(); //这么调用是无法找到r的private和protected的变量的,但在类中的代码可以直接访问protected变量,private依旧不可访问
>  Square s(5);
>  s.print();
>  return 0;
> }
> ```

注：类外不能访问private和protected成员。



## 2.C++中，`this`指针可否赋值？可否取地址？是否占用空间？

先看这里关于`this`的介绍：[C++ 中的 this 指针 | 菜鸟教程](https://www.runoob.com/cplusplus/cpp-this-pointer.html)。

- （1）`this`指针不能够直接赋值。不能够修改`this`指针指向的对象；

- （2）不能直接用`&`进行取地址操作，**但可以通过取值获取。**

  - > - 当你尝试使用`&this`时，实际上你是在试图获取`this`指针本身的地址。然而，`this`已经是一个指针，不再是一个可以取得地址的对象。可以将其视为以下情况：
    >   - `this` 本身是一个指针，因此没有必要再对它取地址。
    >   - 使用 `&this` 在语法上会引起混淆，因为 `this` 的类型是一个指针，取地址的结果会是一个指向指针的指针，这并不是我们通常想要的。
    >   - 实际上在类中，`&this`是会报错的，如果要返回指针指向对象的地址，用`return this;`即可。同时回忆一下，返回值为`MyClass&`类型的函数，可以返回`return *this`

- （3）`this`指针不占用内存，this相当于非静态成员函数的一个隐函的参数,不占对象的空间。它跟对象之间没有包含关系,只是当前调用函数的对象被它指向而已。所有成员函数的参数,不管是不是隐含的,都不会占用对象的空间,只会占用参数传递时的栈空间,或者直接占用一个寄存器。



## 3.enum class 的好处/和enum相比较

可以参考的链接：[C++新特性——枚举类（enum class），以及与传统枚举的区别_c++的class enum是什么类型-CSDN博客](https://blog.csdn.net/2302_80272644/article/details/141310484)

传统的 enum 定义在 C++ 中是这样的：

```c++
enum TraversalType {
    Preorder,
    Inorder,
    Postorder
};
```

在这种情况下，Preorder、Inorder 和 Postorder 都是全局作用域中的常量，可以直接使用 Preorder 来引用。如果不同的 enum 类型中有相同名字的枚举值，就会产生冲突。例如，如果你在另一个地方定义了相同名称的 enum，就可能会有名字冲突问题。

**而enum class 解决了传统 enum 的一些问题，主要是：**

- 作用域：enum class 中定义的枚举值不再是全局作用域，而是属于枚举类的作用域。要引用时，需要使用枚举类型名作为前缀。
- 强类型检查：enum class 是强类型的，不能隐式转换为整数，也不能与整数直接比较。这增加了类型安全性。

在使用`enum class`的时候，使用方法为：

```c++
enum class TraversalType {
    Preorder,
    Inorder,
    Postorder
};
//使用方法：if (type == TraversalType::Preorder)
```



# 三、重要专题部分

> 由于篇幅限制，这一部分的一些专题会被整理进笔记文件夹的单独md文件中，这里会给出对应的md文档名，方便复习。



## 1.虚函数/虚函数表专题

见`C++虚表相关.md`，在八股文/C++文件夹当中。以下是一些常见题目：

- 什么是多态？C++的多态是如何实现的？
- 虚函数的实现机制是什么？
- 虚函数调用是在编译时确定还是运行时确定的？如何确定调用哪个函数？
- 虚函数是存在类中还是类对象中（即是否共享虚表）？
- **在(基类的)构造函数和析构函数中调用虚函数会怎么样**？
- 子类的构造函数中能调用虚函数么？
- 内联函数可以是虚函数么？
- 析构函数可以是虚函数么？&虚析构函数



## 2.类的存储/C++的内存布局

**Q：c++中类对象的内存模型(布局)是怎么样的？**

答：一般遵循以下几点原则：

（1）如果是有虚函数的话，虚函数表的指针始终存放在内存空间的头部；

（2）除了虚函数之外，内存空间会按照类的[继承顺序](https://zhida.zhihu.com/search?content_id=180938976&content_type=Article&match_order=1&q=继承顺序&zhida_source=entity)(父类到子类)和字段的声明顺序布局；

（3）如果有多继承，每个包含虚函数的父类都会有自己的虚函数表，并且按照继承顺序布局(虚表指针+字段）；如果子类重写父类虚函数，都会在每一个相应的虚函数表中更新相应地址；如果子类有自己的新定义的虚函数或者非虚成员函数，也会加到第一个虚函数表的后面；

（4）如果有钻石继承，并采用了虚继承，则内存空间排列顺序为：各个父类(包含虚表)、子类、公共基类(最上方的父类，包含虚表)，并且各个父类不再拷贝公共基类中的数据成员。

可以参考的链接：[C++对象内存布局解析-CSDN博客](https://blog.csdn.net/u012658346/article/details/50775742)，以及[C++内存模型 - MrYun - 博客园](https://www.cnblogs.com/yunlambert/p/9876491.html)。



下面，我们用几个例子来看看C++的内存布局。首先是最简单的内存对齐问题（我是64位机器）：

```c++
#include <iostream>
using namespace std;

class C1
{
public:
    int a;
    char b;
    long long c; //long long 占8个字节
};

class C2
{
public:
    int a;
    long long c;
    char b;
};

int main()
{
    cout<<sizeof(C1)<<endl; //16
    cout<<sizeof(C2)<<endl; //24
}
```

这里不再详细展开说明了，具体的字节对齐规则主要有如下三点（[C++对象内存布局解析-CSDN博客](https://blog.csdn.net/u012658346/article/details/50775742)这篇里面有例子，介绍的不错）：

1) 结构体变量的首地址能够被其最宽基本类型成员的大小所整除；
2) 结构体每个成员相对于结构体首地址的偏移量都是成员大小的整数倍，eg：char型起始地址能被1整除、short型起始地址能被2整除、int型起始地址能被4整除；
3) 结构体的总大小为结构体最宽基本类型成员大小的整数倍。


当C++中一个对象没有继承自其它任何父类，且没有虚函数时，由于类中定义的方法都在方法区，并不在类所在内存中，因此该类型的大小为：**各字段的大小之和+字节对齐**，与C语言中的结构体的内存占用情况完全相同。



那么，有虚函数的时候会怎么样呢？

> 有虚函数 = sizeof(vfptr)+各字段大小之和+内存对齐
>
> - 当该类型中含有虚函数时，则还要考虑虚函数表指针vfptr的大小；当一个类中定义了虚函数时，根据C++对象模型可知，该类型的对象就会产生一个虚函数表vtbl，所有定义的虚函数都会依次排放在该虚函数表中，同时在对象的起始位置分配一个虚函数指针vfptr指向vtbl。在32位机器上，指针为4字节（64位机器上是8字节），因此当一个类函数虚函数时，它对应的对象所占内存大小为：sizeof(vfptr)+各字段大小之和+内存对齐。

比如说下面这个类：

```c++
class C1
{
public:
    int a;
    char b;
    long long c; //long long 占8个字节
    virtual void hello(){}
}; //24字节，比之前的16字节多了8字节的虚表指针
```



现在，我们的C2继承于C1,此时的`sizeof(C2)`结果是什么呢？

```c++
class C2:public C1
{
public:
    int d;
}; //32 = C2的虚表指针8(vptr) + 8:int4 + char1+ padding3 + 8:longlong8 + 8:int4+padding4 = 32
```

> **也就是说，此时对应下面这两种情况的（2）情况（（1）情况比较简单，就不再举例子了）：**
>
> 1）简单直接继承（父类、子类都没有虚函数）
> 这种情况比较简单，父类、子类都没有虚函数，则都没有虚函数表，子类在内存中各成员变量根据其继承和声明顺序依次放在后面，先父类后子类。则子类大小为：**父类各字段大小之和+子类各字段大小之和+字节对齐**
>
> 2）有虚函数（父类或子类中有虚函数）
> 当父类有虚函数表时，则父类中会有一个vfptr指针指向父类虚函数对应的虚表。当一个子类继承自含有虚函数的父类时，就会继承父类的虚函数，因此子类中也会有vfptr指针指向虚函数表。当子类重写了虚函数时，虚表中对应的虚函数就会被子类重写的函数覆盖。此时子类大小就为：sizeof(vfptr) + 父类各字段大小之和 + 子类各字段大小之和+字节对齐。
>
> **注意：经过测试，如果父类变量都是private并且继承也是private的情况，理论上子类无法访问到父类的private对象，但实际上并不会影响内存布局，实操是这样的。**



接下来，是不建议用但C++提供支持的多继承问题，这里怕考也整理一下（==没有验证，有被考到再说吧==）：

（1）当所有的父类都没有虚函数时，这种情况比较简单，子类所占内存的大小为：**所有父类所有字段之和+子类所有字段之和+字节对齐**

```c++
#include <iostream>
using namespace std;

class C1 {
    int a;
    char b;
    long long c; //long long 占8个字节
};

class C2 {
    int d;
    char e;
};

class C: public C1, public C2 {
    int f;
};

int main()
{
    cout<<sizeof(C1)<<endl; //16
    cout<<sizeof(C2)<<endl; //8
    cout<<sizeof(C)<<endl; //32
}
```

（2）父类有虚函数：当一个父类有虚函数时，表明那个父类存在虚函数表，因此在那个父类的结构中会包含一个虚函数指针vfptr。**而当多个父类中定义了虚函数时，则那些父类中都会包含一个vfptr，并且有虚函数的父类会在没有虚函数父类的前面。当子类重写了那些虚函数时，就会在第一个定义了该虚函数的父类的虚函数表中覆盖父类定义的虚函数，当子类增加了新的虚函数时，也会将新增的虚函数增加至那个虚函数表中。**

这个看[C++对象内存布局解析-CSDN博客](https://blog.csdn.net/u012658346/article/details/50775742)这篇文章最下面即可。

> 多继承+虚函数还有一些疑问，但先不管了，再研究就钻牛角尖了。



## ==3.虚继承（还没整理）==

先贴个链接提供参考：[虚继承详解：原理、使用及注意事项-CSDN博客](https://blog.csdn.net/weixin_61857742/article/details/127344922)



# 四、STL专题（单独拿出来）

> 这里面的题也是比较多，而且水也比较深，所以单独拿出来。前面几个小节是对单独的STL容器的总结，后面则是一些整体上的和算法上的总结。关于STL在《C++ Primer》中的重点介绍，参考`C++PrimerSTL相关.md`

## 1.STL各种容器的底层实现？

- （1）**vector**，底层是一块具有连续内存的数组，vector的核心在于其长度自动可变。vector的数据结构主要由三个迭代器(指针)来完成：指向首元素的start，指向尾元素的finish和指向内存末端的end_of_storage。vector的扩容机制是：当目前可用的空间不足时，分配目前空间的两倍或者目前空间加上所需的新空间大小（取较大值），容量的扩张必须经过“重新配置、元素移动、释放原空间”等过程。

- （2）list，底层是一个**循环双向链表**，链表结点和链表分开独立定义的，**结点包含pre、next指针和data数据**。

  - 补充：`forward_list`：单链表

- （3）deque（读deck），双向队列，由分段连续空间构成，每段连续空间是一个缓冲区，由一个中控器来控制。它必须维护一个map指针（中控器指针），还要维护start和finish两个迭代器，指向第一个缓冲区，和最后一个缓冲区。deque可以在前端或后端进行扩容，这些指针和迭代器用来控制分段缓冲区之间的跳转。

  - **关于deque原理的更多细节，可以看这篇：[C++面试八股文：std::deque用过吗？ - 知乎](https://zhuanlan.zhihu.com/p/639761354)**
  - 上面这篇文章里有一个错误，`deque`查找的时间复杂度是O(1)！（想想看，支持查找的话，O(1)绝对够了，通过内部的map找chunk，再通过chunk找对应索引的元素）
  - ==个人理解==，每个chunk内部会有`start`和`end`指针，在头插的时候，如果第一个chunk的`start`前面有空位则直接放在空位，否则如果end后还有空间，就会把第一个chunk内的整体后移再把新元素插入首位置。由于每个chunk的大小是固定的，所以头插可以算作是O（1）复杂度。

- （4）stack和queue，栈和队列。它们都是由deque作为底层容器实现的，他们是一种容器适配器，修改了deque的接口，具有自己独特的性质（此二者也可以用list作为底层实现）；stack是deque封住了头端的开口，先进后出，queue是deque封住了尾端的开口，先进先出。

  - > 适配器（Adaptor）的介绍（来自《C++ Primer》p9.6）.除了顺序容器外，标准库定义了三个顺序容器适配器：`stack`，`queue`和`priority_queue`。适配器是标准库中的一个通用概念。容器，迭代器和函数都具备适配器。**本质上，一个适配器是一种机制，能使某种事物的行为看起来像另一种事物。**一个容器适配器接受一种已有的容器类型，使其行为看起来像一种不同的类型。

- （5）priority_queue，优先队列。是由以vector作为底层容器，以heap作为处理规则，heap的本质是一个完全二叉树。

  - 完全二叉树：除了最后一层之外，完全二叉树的每一层都必须是满的。这意味着每一层的节点数都达到了该层的最大可能数量。在最后一层，节点可以没有填满，但一定是从左到右放的。**关于堆排序的代码，会单独在后面进行整理。**

- （6）set和**map。**底层都是由红黑树实现的。红黑树是一种二叉搜索树，但是它多了一个颜色的属性。

  - 二叉搜索树：查找的时间复杂度为O(logn)

  - **红黑树的性质如下：（==更多内容放别的地方整理吧，还没看，可整理B树，B+树， 2-3树，2-3-4树和红黑树相关==）**

    - 1）每个结点非红即黑；
    - 2）根节点是黑的；
    - 3）如果一个结点是红色的，那么它的子节点就是黑色的（也就是不能出现连续的红节点）；
    - 4）任一结点到树尾端（NULL）的路径上含有的黑色结点个数必须相同。**通过以上定义的限制，红黑树确保没有一条路径会比其他路径多出两倍以上；**因此，红黑树是一种弱平衡二叉树，相对于严格要求平衡的平衡二叉树来说，它的旋转次数少，所以对于插入、删除操作较多的情况下，通常使用红黑树。
    - 5）叶子节点一定是黑的（NIL）

  - 补充：平衡二叉树(AVL)和红黑树的区别：AVL 树是高度平衡的，频繁的插入和删除，会引起频繁的rebalance（旋转操作），导致效率下降；**红黑树不是高度平衡的，算是一种折中，插入最多两次旋转，删除最多三次旋转。**注：**关于AVL树的更多细节，在后面也会进行介绍。**

  - 平衡二叉树的概念：对于每个节点，左子树和右子树的高度差（通常称为平衡因子）不能超过一定的值。对于多种平衡二叉树，这个值通常为 1。**AVL 树**是一种自平衡的二叉搜索树，每个节点都维护一个平衡因子（左子树高度减去右子树高度），并在插入或删除节点后进行旋转调整以保持平衡。**平衡二叉树搜索、插入、删除的复杂度是O（logn）**。

    - 例题：[平衡二叉树_平衡二叉树例题-CSDN博客](https://blog.csdn.net/zhenzhu2882/article/details/124024156)
    - 其他参考链接：[平衡二叉树 —— 如何优雅的进行旋转 - 知乎](https://zhuanlan.zhihu.com/p/438604092)，这个链接讲的不错。平衡二叉树的插入操作所带来的平衡操作是递归进行的，在找到插入位置之后，会从插入位置的父节点开始往上递归做平衡旋转操作。
    - 关于平衡二叉树的删除补充（上述链接讲的不太好理解）
    
    > 首先，需要像在普通二叉搜索树中一样找到并删除要删除的节点。删除的基本步骤如下：
    >
    > - **查找**：根据二叉搜索树性质找到要删除的节点。
    > - 删除：
    >   - 如果要删除的节点是叶子节点（没有子节点），直接将其移除。
    >   - 如果要删除的节点有一个子节点，将要删除的节点替换为其唯一的子节点。
    >   - 如果要删除的节点有两个子节点，找到它的后继节点（右子树中的最小值或左子树中的最大值），用后继节点的值替换要删除的节点，然后删除后继节点。
    >     - 当左右子树都有时，根据左右子树的平衡性分情况讨论：如果左子树的高度更高，则从左子树选择最大值替换根结点，并且递归删除左子树对应结点；如果右子树更高，则从右子树选择最小值替换根结点，并且递归删除右子树对应结点；**如果理解不好的话可以画两种情况的平衡二叉树来辅助理解。**
    

- （7）multiset和multimap：底层依旧是使用红黑树来实现的，但允许多个相同元素的存在。比如对multiset而言，在插入时，所有插入都会成功，无论元素是否已存在。而对multimap来说，多个相同的键可以对应不同的值。插入相同的键会添加新的值，而不是覆盖旧的值（普通的map会覆盖旧的值）。

- （8）unordered_map和unordered_set：底层实现基于哈希表，通过哈希函数将键映射到哈希表的某个位置。对于冲突通常使用**链地址法（Separate Chaining）**来解决哈希冲突，即在同一个哈希桶中存储多个元素（使用链表或红黑树）。

  - 平均插入、删除、查找操作的时间复杂度为O（1），最差的情况可能退化到O（n），并且具备无序性：元素存储顺序与插入顺序无关，取决于哈希函数的结果。
  - 关于哈希冲突的解决方案在后面的题目里有。




## 2.**STL各种容器的查找、删除和插入的时间复杂度（性能比较）**？

【参考资料】：[C++STL各种容器的性能比较](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/zl1991/p/4691316.html)、[【C++】STL各容器的实现，时间复杂度，适用情况分析_Y先森0.0-CSDN博客](https://link.zhihu.com/?target=https%3A//blog.csdn.net/qq_39382769/article/details/102441699)

- （1）vector，vector支持随机访问(通过下标），时间复杂度是O(1)；如果是无序vector查找的时间复杂度是O(n)，如果是有序vector，采用二分查找则是O(log n)；对于插入操作，在尾部插入最快，中部次之，头部最慢，删除同理。vector占用的内存较大，由于二倍扩容机制可能会导致内存的浪费，内存不足时扩容的拷贝也会造成较大性能开销；
- （2）list由于底层是链表，不支持随机访问，只能通过扫描的方式查找，复杂度为O(n)，但是插入和删除的速度快，只需要调整指针的指向。有一种说法是链表每次插入和删除都需要分配和释放内存，会造成较大的性能开销，所以如果频繁地插入和删除，list性能并不好（动态内存分配和释放会对性能造成影响，特别是在频繁操作时）。**原则是：选择哪种容器，应该根据实际需求来。**list不会造成内存的浪费，占用内存较小；
- （3）deque支持随机访问，但性能比vector要低（占据空间更大）；支持双端扩容，因此在头部和尾部插入和删除元素很快，为O(1)，但是在中间插入和删除元素很慢；
- （4）set和map，底层基于红黑树实现，增删查改的时间复杂度近似O(log n)。
- （5）unordered_set和unordered_map，底层是基于哈希表实现的，是无序的。理论上增删查改的时间复杂度是O(1)（最差时间复杂度O(n))，实际上数据的分布是否均匀会极大影响容器的性能。



## 3.STL怎么做内存管理的，Allocator次级分配器的原理，内存池的优势和劣势？

【参考链接】[《STL源码剖析》提炼总结：空间配置器(allocator) - 知乎](https://zhuanlan.zhihu.com/p/34725232)，当然前置文章：[《STL源码剖析》提炼总结：概览 - 知乎](https://zhuanlan.zhihu.com/p/31505598)这篇也可以看看。

（1）为了提升内存管理的效率，减少申请小内存造成的内存碎片问题，SGI STL采用了两级配置器，当分配的空间大小超过128B时，会使用第一级空间配置器，直接使用malloc()、realloc()、free()函数进行内存空间的分配和释放。当分配的空间大小小于128B时，将使用第二级空间配置器，采用了内存池技术，通过空闲链表来管理内存。

（2）次级配置器的内存池管理技术：每次配置一大块内存，并维护对应的自由链表(free list)。若下次再有相同大小的内存配置，就直接从自由链表中拔出。如果客户端释还小额区块，就由配置器回收到自由链表中；配置器共要维护16个自由链表，存放在一个数组里，分别管理大小为8-128B不等的内存块。分配空间的时候，首先根据所需空间的大小（调整为8B的倍数）找到对应的自由链表中相应大小的链表，并从链表中拔出第一个可用的区块；回收的时候也是一样的步骤，先找到对应的自由链表，并插到第一个区块的位置。

（3）优势：避免内存碎片(这里应该指的是外部碎片)，不需要频繁从用户态切换到内核态，性能高效；劣势：仍然会造成一定的内存浪费，比如申请120B就必须分配128B（内部碎片）。

下图应该会方便加深对次级分配器的理解：

![image-20250129124031800](C++%20%E9%9D%A2%E7%BB%8F%E5%90%88%E9%9B%86.assets/image-20250129124031800.png)

> 补充：**内部碎片与外部碎片**：
>
> - [内存碎片是什么？ - 知乎](https://zhuanlan.zhihu.com/p/589406667)，暂时看一下前面关于内部碎片和外部碎片的介绍和例子即可。



## 4. STL容器的push_back和emplace_back的区别？

【参考资料】《C++ Primer》P308、[C++11使用emplace_back代替push_back_华秋实的专栏-CSDN博客](https://link.zhihu.com/?target=https%3A//blog.csdn.net/yockie/article/details/52674366)

答：emplace/emplace_back函数使用传递来的参数直接在容器管理的内存空间中构造元素（只调用了构造函数）；push_back会创建一个局部临时对象，并将其压入容器中（可能调用拷贝构造函数或移动构造函数）。具体在笔记合集的`C++PrimerSTL相关.md`这篇里面有。



## 5. **STL的排序用到了哪种算法，具体如何执行**？

【参考链接】[知无涯之std::sort源码剖析](https://feihu.me/blog/2014/sgi-std-sort/)。里面涉及STL的极致优化部分，

答：快速排序、插入排序和堆排序；当数据量很大的时候用快排，划分区段比较小的时候用插入排序，当划分有导致最坏情况的倾向的时候使用堆排序。

更多细节可以看下上述参考链接。

**这个链接也推荐看一下**：[(99+ 封私信 / 53 条消息) 自己写的排序会比C#自带的排序快吗？ - 知乎](https://www.zhihu.com/question/472808760/answer/2093452888)，写的很不错。



## 6.什么是哈希表？**哈希表的长度为什么要是质数？如何处理冲突？哈希表怎么删除一个元素**？

【参考资料】[图文并茂详解数据结构之哈希表 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/144296454)

（1）哈希表是一种根据关键码值直接访问数据的数据结构，它通过把关键码值映射到表中的一个位置来访问元素，以加快查找的速度。这个映射函数叫做哈希函数；

（2）哈希表的长度使用质数，可以降低发生冲突的概率，使哈希后的数据更加均匀，如果使用合数，可能会导致很多数据集中分布到一个点上，造成冲突；

（3）解决冲突的办法有开放定址法和拉链法，开放定址法包括线性测探、平方测探法；

（4）线性测探法并不会真正的删除一个元素，而是做一个标记，否则可能会导致正常的查找出错（[利用线性探测法解决hash冲突 - 寻觅beyond - 博客园 (cnblogs.com)](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/-beyond/p/7726347.html)）

> Java中的hashmap就是基于哈希表结构+数组+链表+红黑树来实现的。C++ STL中的哈希表应该是链地址法做的。



## 7.`vector`的扩容机制具体是怎样的?

> 在C++中，`std::vector` 在扩容时，会尝试调用元素的**移动构造函数**（如果存在且不抛出异常），否则会调用**拷贝构造函数**。具体过程如下：
>
> ### 1. **扩容过程**
> 当 `std::vector` 的容量不足以容纳新元素时，它会执行以下步骤：
> 1. 分配一块更大的内存空间。
> 2. 将现有元素从旧内存空间迁移到新内存空间。
> 3. 释放旧内存空间。
>
> 在迁移元素时，`std::vector` 会优先使用移动语义（调用移动构造函数）来转移元素，因为移动语义通常比拷贝语义更高效。如果移动构造函数不可用或不安全（例如可能抛出异常），则会回退到拷贝构造函数。
>
> ---
>
> ### 2. **调用移动构造函数的条件**
> `std::vector` 在扩容时会调用移动构造函数，前提是：
>
> - 元素的类型具有 **noexcept 移动构造函数**（即移动构造函数不会抛出异常）。
> - 如果移动构造函数可能抛出异常，`std::vector` 会优先使用拷贝构造函数，以确保强异常安全性。
>
> ---
>
> ### 3. **调用拷贝构造函数的条件**
> 如果以下条件之一满足，`std::vector` 会调用拷贝构造函数：
> - 元素的类型没有移动构造函数。
> - 移动构造函数可能抛出异常（即没有标记为 `noexcept`）。
> - 元素的类型是普通旧数据类型（POD，如 `int`、`double` 等），这些类型没有移动语义。
>
> ---
>
> ### 4. **具体过程**
> 以下是 `std::vector` 扩容的具体过程：
> 1. **分配新内存**：
>    - 分配一块比当前容量更大的内存空间（通常是当前容量的 2 倍）。
> 2. **迁移元素**：
>    - 如果元素类型支持 `noexcept` 移动构造函数，则调用移动构造函数将元素从旧内存移动到新内存。
>    - 如果不支持移动语义或移动构造函数可能抛出异常，则调用拷贝构造函数将元素从旧内存复制到新内存。
> 3. **销毁旧元素**：
>    - 在旧内存空间中调用元素的析构函数。
> 4. **释放旧内存**：
>    - 释放旧内存空间。
>
> ---
>
> ### 5. **示例代码**
> 以下是一个示例，展示了 `std::vector` 扩容时调用移动构造函数和拷贝构造函数的行为：
>
> ```cpp
> #include <iostream>
> #include <vector>
> 
> class MyClass {
> public:
>     MyClass() { std::cout << "Constructor\n"; }
>     MyClass(const MyClass&) { std::cout << "Copy Constructor\n"; }
>     MyClass(MyClass&&) noexcept { std::cout << "Move Constructor\n"; }
>     ~MyClass() { std::cout << "Destructor\n"; }
> };
> 
> int main() {
>     std::vector<MyClass> vec;
>     vec.reserve(1); // 预分配空间，避免初始扩容干扰
> 
>     std::cout << "Adding first element:\n";
>     vec.push_back(MyClass()); // 添加第一个元素
> 
>     std::cout << "\nAdding second element (triggering resize):\n";
>     vec.push_back(MyClass()); // 添加第二个元素，触发扩容
> 
>     return 0;
> }
> ```
>
> **输出**：
> ```
> Adding first element:
> Constructor
> Move Constructor
> Destructor
> 
> Adding second element (triggering resize):
> Constructor
> Move Constructor
> Move Constructor
> Destructor
> Destructor
> Destructor
> Destructor
> ```
>
> **解释**：
> 1. 第一次 `push_back` 时，`MyClass` 对象被构造，然后通过移动构造函数移动到 `vector` 中。
> 2. 第二次 `push_back` 时，`vector` 扩容，调用移动构造函数将旧元素迁移到新内存空间，然后新元素也被移动到新内存空间。
> 3. 最后，旧内存空间中的对象被销毁。
>
> ---
>
> ### 6. **如何控制行为**
> - **确保移动构造函数是 `noexcept`**：
>   如果你的类有移动构造函数，请确保它标记为 `noexcept`，以便 `std::vector` 优先使用移动语义。
>   ```cpp
>   MyClass(MyClass&&) noexcept { ... }
>   ```
>
> - **禁用移动语义**：
>   如果你不希望 `std::vector` 使用移动语义，可以删除移动构造函数：
>   ```cpp
>   MyClass(MyClass&&) = delete;
>   ```
>
> - **禁用拷贝语义**：
>   如果你不希望 `std::vector` 使用拷贝语义，可以删除拷贝构造函数：
>   ```cpp
>   MyClass(const MyClass&) = delete;
>   ```
>
> ---
>
> ### 7. **总结**
> - `std::vector` 在扩容时，优先调用移动构造函数（如果可用且不抛出异常）。
> - 如果移动构造函数不可用或可能抛出异常，则调用拷贝构造函数。
> - **通过确保移动构造函数是 `noexcept`，可以优化 `std::vector` 的性能。**



## 其他杂项题目

- （1）熟悉 STL 源码吗？
  - 有看过《STL源码剖析》（作者：侯捷）的一部分，但时间有限还没有读完
- （2）`vector` 插入元素发生了什么？
  - 这道题目可以答一下`vector`中的三个指针，当`end`到达`end_of_storage`就会触发扩容机制。
  - 还可以往`push_back`和`emplace_back`的区别这个方向去靠。
- （3）



## 补充：各种排序算法的原理和时间复杂度

【参考资料】：[八大常用排序算法详细分析](https://link.zhihu.com/?target=https%3A//blog.csdn.net/yuxin6866/article/details/52771739)，笔记也有一篇专门讲排序算法的：`排序算法专题.md`

![img](C++%20%E9%9D%A2%E7%BB%8F%E5%90%88%E9%9B%86.assets/20161009171515225.jpeg)

（1）**快排**：一轮划分，选择一个基准值，小于该基准值的元素放到左边，大于的放在右边，此时该基准值在整个序列中的位置就确定了，接着递归地对左边子序列和右边子序列进行划分。时间复杂度$O(nlogn)$，最坏的时间复杂度是$o(n^2)$；**快排是不稳定的排序。**

（2）堆排序：利用完全二叉树性质构造的一个一维数组，用数组下标代表结点，则一个结点的左孩子下标为`2i+1`,右孩子为`2i+2`，一个结点的父节点为`(i-1)/2`。堆排序的思想就是，构造一个最大堆或者最小堆，以最大堆为例，那么最大的值就是根节点，把这个最大值和最后一个结点交换，然后在从前`n-1`个结点中构造一个最大堆，再重复上述的操作，即**每次将现有序列的最大值放在现有数组的最后一位，最后就会形成一个有序数组；求升序用最大堆，降序用最小堆。时间复杂度$O(nlogn)$**；

（3）冒泡排序：从前往后两两比较，逆序则交换，不断重复直到有序；时间复杂度$O(n^2)$，最好情况$O(n)$；

（4）插入排序，类似打牌，从第二个元素开始，把每个元素插入前面有序的序列中；时间复杂度$O(n^2)$，最好情况$O(n)$；

（5）选择排序，每次选择待排序列中的最小值和未排序列中的首元素交换；时间复杂度$O(n^2)$；

（6）归并排序，将整个序列划分成最小的>=2的等长序列，排序后再合并，再排序再合并，最后合成一个完整序列。时间复杂度$O(nlogn)$。

（7）希尔排序，是插入排序的改进版，取一个步长划分为多个子序列进行排序，再合并(如135一个序列，246一个序列），时间复杂度$O(n^{1.3})$，最好$O(n)$，最坏$O(n^2)$；

（8）桶排序，将数组分到有限数量的桶里。每个桶再个别排序，最后依次把各个桶中的记录列出来记得到有序序列。桶排序的平均时间复杂度为线性的$O(N+C)$，其中$C=N*(logN-logM)$，$M$为桶的数量。最好的情况下为$O(N)$。



## 其他链接

【1】 [c++ std::vector 底层实现机制 - 知乎](https://zhuanlan.zhihu.com/p/499411093)

【2】[C++面试八股文：std::vector了解吗？ - 知乎](https://zhuanlan.zhihu.com/p/639103620)



# 五、C++ 新特性专题

## 1.lambda表达式（==还未整理完，只整理了最基础的==）

参考文章：[(99+ 封私信 / 29 条消息) C++ lambda - 搜索结果 - 知乎](https://www.zhihu.com/search?type=content&q=C%2B%2B lambda)

C++标准中关于lambda表达式的几种构造说明如下：

![image-20250127102736832](C++%20%E9%9D%A2%E7%BB%8F%E5%90%88%E9%9B%86.assets/image-20250127102736832.png)



1. `captures`：对应的中文含义就是捕获的意思，用来描述哪些变量将被闭包捕获。这里的捕获就是闭包持有这些外部变量的信息（可能是外部变量的值，也可能是外部变量的引用）

2. `params`：用来定义函数对象的形参，和普通函数的形参一致

3. `specs`：由`specifiers`、`exception`、`trailing-return-type`描述符组成的序列

4. 1. `specifiers`：在C++17标准中以及之前可以指定为`mutable`、`constexpr`中二者中的一个或多个组成的序列。其中`mutable`作用是允许函数体内对以值捕获而来的变量进行修改；`constexpr`是用来制定该函数是否支持const表达式
   2. `exception`：在C++17标准以及之前标准（当然需要C++11及以上，因为`lambda`是在C++11标准才引入的）可以指定一个`noexcept`用来制定该函数对象的调用时`noexcept`的
   3. `trailing-return-type`：用来以以`->ret`的形式对`lambda`的返回值类型进行显示声明。如果不进行声明，则`lambda`表达式的返回值将通过函数体的返回语句进行类型自动推导，就和普通[函数模板](https://zhida.zhihu.com/search?content_id=217615458&content_type=Article&match_order=1&q=函数模板&zhida_source=entity)返回值用`auto`进行声明的效果是一致的



1. `body`：函数体，用来写具体的函数实现的
2. `requires`：在C++20的标准中可用，在此不讨论



有了上文的一些基础之后，我们可以直接看一些lambda表达式的例子。首先先来看一个最基本的例子：

```c++
#include <iostream>
using namespace std;
int main()
{
    int num = 114514;
    auto add_num = [num](int a){return num+a;};
    num = 1919810;
    cout<<add_num(1)<<endl; //114515,因为是值传递
}
```

实际上，在使用STL的过程中我们用过仿函数，以下是一个仿函数实现同样功能的示例：

```c++
#include <iostream>
#include <string>
using namespace std;

class add_num
{
public:
    add_num(int num):num(num){}
    int operator()(int a) const { return num+a; }
private:
   int num;
};

int main()
{
    int num = 114514;
    add_num a(num);
    num = 1919810;
    std::cout << a(2) << std::endl; //对应的输出：114516，也是值传递
    return 0;
}
```

用cppinsights查看lambda表达式的编译器认识的版本（图怎么截都有点不太清楚，可以去cppinsights里面跑一下看看，和上面是类似的）：

![image-20250127104701041](C++%20%E9%9D%A2%E7%BB%8F%E5%90%88%E9%9B%86.assets/image-20250127104701041.png)



**引用捕获**

看完了值捕获，来看一个引用捕获的例子：

```c++
int main()
{
    int num = 114514;
    auto change_num = [&num](int a){num = a;}; //引用捕获
    change_num(1919810);
    cout<<num<<endl; //1919810
}
```

不难想到，此时编译器会这样优化：

![image-20250127105134382](C++%20%E9%9D%A2%E7%BB%8F%E5%90%88%E9%9B%86.assets/image-20250127105134382.png)

与刚才的不同是，这时生成的lambda类中的private变量num变成了引用类型。这样当外界修改了num的值之后，lambda表达式通过引用捕获的num也会得到修改。



**刷Leetcode背包问题时遇到的lambda表达式解析**

在刷Leetcode的时候，看到动规的记忆化搜索有这样的题目（0-1背包：目标和）

```c++
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int s = reduce(nums.begin(), nums.end()) - abs(target);
        if (s < 0 || s % 2) {
            return 0;
        }
        int m = s / 2; // 背包容量

        int n = nums.size();
        vector memo(n, vector<int>(m + 1, -1)); // -1 表示没有计算过
        auto dfs = [&](this auto&& dfs, int i, int c) -> int {
            if (i < 0) {
                return c == 0;
            }
            int& res = memo[i][c]; // 注意这里是引用
            if (res != -1) { // 之前计算过
                return res;
            }
            if (c < nums[i]) {
                return res = dfs(i - 1, c); // 只能不选
            }
            return res = dfs(i - 1, c) + dfs(i - 1, c - nums[i]); // 不选 + 选
        };
        return dfs(n - 1, m);
    }
};

作者：灵茶山艾府
链接：https://leetcode.cn/problems/target-sum/solutions/2119041/jiao-ni-yi-bu-bu-si-kao-dong-tai-gui-hua-s1cx/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

以下是对这个lambda表达式的解析：

> ```c++
> auto dfs = [&](this auto&& dfs, int i, int c) -> int {
>     // 函数体
> };
> ```
>
> - 首先来看`[&]`，这表示**以引用方式捕获外部作用域中的所有变量。**这意味着在 lambda 内部对这些变量的任何修改都将反映在外部作用域中。
> - `this`: 在这里，`this` 被捕获是为了能够访问当前对象的成员和方法。在 C++ 的类成员函数内部，`this` 指针指向当前对象。通过捕获 `this`，lambda 表达式可以调用类的其他成员（包括数据成员和其他成员函数）。
> - `auto&& dfs`: 这是一个递归的捕获，也就是说，`dfs` 在 lambda 内部被定义为自身的一部分，以便于递归调用。在 C++ 中，`auto&&` 是一种完美转发（perfect forwarding）技术，允许捕获并保留传入参数的类型（左值或右值）。
> - `-> int`: 这指定了 lambda 表达式的返回类型为 `int`，与函数的目的相符，即计算特定条件下的可能组合数。

剩下的逻辑就和背包问题本身有关了，这篇文档不再介绍。在调用`dfs`函数的时候不需要显式把dfs作为参数传进去了。



# 杂项

## 1.C++ 编译器调试时看到的地址是物理地址还是逻辑地址?

是**逻辑地址**。这里就需要我们复习一下物理地址和逻辑地址的区别：

> ### 1. 逻辑地址（虚拟地址）
>
> - **定义**：逻辑地址是程序中使用的地址，由编程语言和操作系统提供给应用程序。这些地址是相对于进程的地址空间而言的。
> - 特性：
>   - 每个进程都有自己的逻辑地址空间，**因此同一地址在不同进程中可以指向不同的物理内存位置**。
>   - 操作系统通过内存管理单元（MMU）将逻辑地址转换为物理地址。
>
> ### 2. 物理地址
>
> - **定义**：物理地址是实际存在于计算机硬件（RAM）中的地址。
> - 特性：
>   - 物理地址直接对应于内存芯片上的具体位置。
>   - 程序无法直接访问或看到物理地址，除非在一些特权模式下（例如操作系统内核）。
>
> ### 调试过程中的地址
>
> - 当你在调试器中查看变量、函数或数据结构的地址时，你看到的是逻辑地址。这是因为大多数现代操作系统都采用了虚拟内存技术，允许每个进程在自己的逻辑地址空间中运行，从而避免了不同进程之间的内存冲突。操作系统会负责将这个逻辑地址映射到物理内存中某个物理地址，但这个映射过程对用户和程序员是透明的。



# 总参考链接：

【1】[【游戏开发面经汇总】- 计算机基础篇 - 知乎](https://zhuanlan.zhihu.com/p/417640759)

