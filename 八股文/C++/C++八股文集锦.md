# C++八股文集锦

Linux下编译运行cpp程序的方法：

```shell
haohan@ming-3090x4:~/CppTest$ g++ 01_test.cpp
haohan@ming-3090x4:~/CppTest$ ./a.out
```

# 一、基础问题

## 1.指针和引用的区别

见01_test.cpp



## 2.关于const

见02_const.cpp

```c++
const int *ref = &temp; // ref is a pointer to a constant integer
int const *ref2 = &temp; // ref2 is a pointer to a constant integer
```

以上的这两个指针，不能通过`*ref = 10`来修改其指向的对象的值，但可以改变指针的指向。



以下的这个指针可以改变指向对象的值，但不能改变指向的对象：

```c++
int *const p = &temp3; // p is a constant pointer to an integer
*p = 114514;
cout << "temp3 = " << temp3 << endl;
cout << *p << endl;
//p = &temp4; // Error
```

**回忆：其实这种就是从右往左读就可以了。**



## 3.关于static

static 关键字主要⽤于控制变ᰁ和函数的⽣命周期、作⽤域以及访问权限。重点记住下面几个应用场景：

- 静态变量：见03_static_1.cpp文件
- 静态函数/类静态成员函数：见03_static_2.cpp文件
- 类中静态成员变量：见03_static_2.cpp文件



## 4.关于constexpr 和const

```c++
constexpr int *p = nullptr; //可能是学的还是太少，感觉这种语法没什么用
```

其他可以看04_constexpr.cpp文件。



## 5.前置++和后置++

这里以游戏开发为例，介绍一下自定义类++的重载运算符用法。（相关代码在05_testPlayer.cpp文件中）

```c++
#include <iostream>
#include <string>
using namespace std;

class Player
{
private:
    int level;
    string name;
public:
    //构造函数
    Player(int level, string name)
    {
        this->level = level;
        this->name = name;
    }
    
    // 输出玩家信息
    void display() const 
    {
        std::cout << "Player: " << name << ", Level: " << level << std::endl;
    }

    //重载++运算符
    // 前置自增运算符重载
    Player& operator++() 
    {
        ++level; // 增加等级
        return *this; // 返回自身的引用
    }

    // 后置自增运算符重载
    const Player operator++(int) 
    {
        Player temp = *this; // 保存修改前的对象
        ++level; // 增加等级
        return temp; // 返回修改前的对象
    }
};

int main()
{
    Player player(1, "Tom");
    player.display();
    ++player;
    player.display();
    player++;
    player.display();

    return 0;
}
```

有几个注意事项：

- 后置自增运算符不返回引用，原因是其创建了一个临时对象，在函数执行之后销毁了，所以引用是不行的；
- 为什么后置自增运算符返回的是const呢？为了防止用户写出`i++++`这样的代码，因为它与内置类型行为不⼀致；⽆法获得你所期望的结果，因为第⼀次返回的是旧值，而不是原对象，调用两次后置++，结果只累加了⼀次，所以我们必须⼿动禁⽌其合法化，就要在前⾯加上const。

> 这里具体说明一下，比如上面的代码`const Player operator++(int) `中去掉const，会导致可以写出`player++++`这种代码，但其实最终结果只会++一次，虽然重载++函数调用了两次。（不知道为啥？没人会考这种东西吧。。。主要也是要防止用户写出++++这种逆天的代码）

- 对于自定义类来说，自增最好使用前置++符号，不会创建临时对象，进⽽不会带来构造和析构⽽造成的格外开销。



### 6.std::atomic

Q：a++ 和 int a = b 在C++中是否是线程安全的？

> 不是。

这个关键字后面有需求的话再看吧，暂时不太用看。



## 7.函数指针的使用

见09_func.cpp文件

```c++
#include<iostream>
using namespace std;

int add(int a, int b){
    return a+b;
}

int substract(int a,int b){
    return a-b;
}

int main(){
    int(*oper)(int, int); //定义⼀个函数指针，指向⼀个接受两个int参数、返回int的函数
    oper = &add;
    cout<<oper(3,6)<<endl;  //9
    oper = &substract;
    cout<<oper(3,6)<<endl;  //-3
    cout<<(*oper)(3,6)<<endl; //这样也可以
    return 0;
}
```

C++中函数指针的使用场景有：

- 回调函数： 函数指针常⽤于实现回调机制，允许将函数的地址传递给其他函数，以便在适当的时候调⽤
- 函数指针数组： 可以使⽤函数指针数组实现类似于状态机的逻辑，根据不同的输⼊调⽤不同的函数
- 动态加载库： 函数指针可⽤于在运⾏时动态加载库中的函数，实现动态链接库的调⽤；
- 多态实现： 在C++中，虚函数和函数指针结合使⽤，可以实现类似于多态的效果。 
- 函数指针作为参数： 可以将函数指针作为参数传递给其他函数，实现⼀种可插拔的函数⾏为。 
- 实现函数映射表： 在⼀些需要根据某些条件调⽤不同函数的情况下，可以使⽤函数指针来实现函数映射表



## 8.struct和class的区别



## 9.C++强制类型转换

关键字：static_cast、dynamic_cast、reinterpret_cast和 const_cast

对应demo：`10_cast.cpp`

### （1）static_cast

**没有运⾏时类型检查来保证转换的安全性**。因此上行转换是安全的（派生类指针或引用转换为基类），但是下行转换（基类指针或引用转换为派生类）则是不安全的（因为没有动态类型检查）。

常见使用：

- ⽤于基本数据类型之间的转换，如把int转换成char。
- 把任何类型的表达式转换成void类型。



### （2）dynamic_cast

下行转换的时候，dynamic_cast具有类型检查（信息在虚函数中）的功能，⽐static_cast更安全。转换后必须是类的指针、引用或者void*，基类要有虚函数，可以交叉转换。 dynamic本身只能⽤于存在虚函数的⽗⼦关系的强制类型转换；对于指针，转换失败则返回nullptr，对于引用，转换失败会抛出异常。



### （3）reinterpret_cast

可以将整型转换为指针，也可以把指针转换为数组；可以在指针和引用⾥进行肆⽆忌惮的转换，平台移植性比较差。 



### （4）const_cast

常量指针转换为⾮常量指针，并且仍然指向原来的对象。常量引⽤被转换为⾮常量引⽤，并且仍然指向原来的对象。去掉类型的const或volatile属性（[C/C++ 中 volatile 关键字详解 | 菜鸟教程 (runoob.com)](https://www.runoob.com/w3cnote/c-volatile-keyword.html)）。



主要应该就是看static_cast和dynamic_cast这两个，示例demo如下：

```c++
#include <iostream>
using namespace std;

// 定义父类
class Mihoyo {
public:
    // 虚函数
    virtual void print() {
        cout << "This is the Base class." << endl;
    }
};

// 定义子类
class Genshin : public Mihoyo {
public:
    // 重写虚函数
    void print() override {
        cout << "This is the Derived class." << endl;
    }
};

int main() {
    // 创建子类对象
    Genshin genshinImpact;

    // 使用父类指针指向子类对象
    Mihoyo* hoyo = &genshinImpact;

    // 调用 print 函数，实际调用的是子类的实现
    hoyo->print(); // 输出: This is the Derived class.

    //dynamic_cast 强制转换
    Mihoyo* basePtr = &genshinImpact; //父类指针指向子类对象
    Genshin* derivedPtr = dynamic_cast<Genshin*>(basePtr); //强制下行转换
    if (derivedPtr == nullptr) {
        cout << "basePtr cannot be down-casted to Derived* type" << endl;
    } else {
        cout << "basePtr has been down-casted to Derived* type" << endl;
    }

    // 创建父类对象
    //Mihoyo baseObj;

    // 使用子类指针指向父类对象是非法的
    // Derived* derivedPtr = &baseObj; // 这行代码会引发编译错误

    return 0;
}

```



## 10.C++内存管理

主要关键词（图找参考资料即可，代码随想录C++八股文合集）：

- 堆
- 栈
- 全局（静态）区
- 常量区
- 代码区



## 11.【关键】关于内存泄漏的一个点

**没有将基类的析构函数定义为虚函数**，会导致内存泄漏，为什么？

> 当你创建一个基类指针并让它指向一个派生类对象时，你可以通过基类指针来操作该对象。如果基类的析构函数不是虚函数，则在删除基类指针时，仅会调用基类的析构函数，而不会调用派生类的析构函数。

这个例子可以看11_virtualDestructor.cpp这个案例：

```c++
#include <iostream>

using namespace std;

class Base {
public:
    // 非虚析构函数
    ~Base() {
        cout << "Base destructor called." << endl;
    }
};

class Derived : public Base {
public:
    ~Derived() {
        cout << "Derived destructor called." << endl;
    }
};

int main() {
    Base* basePtr = new Derived(); // 创建派生类对象并用基类指针指向它
    delete basePtr; // 使用基类指针删除对象
    return 0;
}

```

此时父类指针指向子类对象，删除指针的时候会调用父类的析构函数，但是因为父类的析构函数不是虚函数，因此不会调用子类的，输出就是一句`Base destructor called.`，造成内存泄漏；

修改：
```c++
//只需要改父类的析构函数为虚函数即可
virtual ~Base() {
    cout << "Base destructor called." << endl;
}
```

在这种情况下，`delete basePtr` 调用时，先调用 `Derived` 的析构函数，再调用 `Base` 的析构函数，确保所有资源都得到了正确释放，避免了内存泄漏。

> 补充：
>
> ### 1. 多态性和虚函数
>
> C++ 中的虚函数机制允许程序根据实际对象类型（而不是指针或引用的类型）来选择要调用的函数。这种行为称为运行时多态性。
>
> - 当你将一个函数声明为虚函数时，C++ 会在每个对象中维护一个指向虚函数表（vtable）的指针。虚函数表是一个指针数组，其中包含该类的所有虚函数的地址。
> - 当通过基类指针或引用调用虚函数时，程序会查找该对象的虚函数表，以确定应该调用哪个版本的函数（即基类或派生类的实现）。
>
> ### 2. 虚析构函数的工作原理
>
> 当父类的析构函数被声明为虚函数时，删除一个基类指针所指向的派生类对象时，会发生以下情况：
>
> 1. **对象的销毁过程**：
>    - 当你使用 `delete` 操作符删除一个基类指针指向的对象时，C++ 首先会查找该对象的 vtable。
>    - 如果这个对象是派生类的实例，vtable 会指向派生类的析构函数。
> 2. **调用析构函数**：
>    - C++ 将首先调用派生类的析构函数，确保派生类的资源（如动态分配的内存、打开的文件等）得到释放。
>    - 随后，基类的析构函数被调用，处理基类的清理工作。
>
> 这样一来，所有与派生类和基类相关的资源都能够正确释放，从而避免了内存泄漏和资源泄露。



## 12.构造函数和析构函数能被定义成虚函数么？

析构函数应当被定义为虚函数，理由11题里面有。

**构造函数不需要，没有意义。**虚函数调⽤是在部分信息下完成⼯作的机制，允许我们只知道接⼝⽽不知道对象的确 切类型。 要创建⼀个对象，你需要知道对象的完整信息。 特别是，你需要知道你想要创建的确切类型。 因此，构 造函数不应该被定义为虚函数



## 13.智能指针

没啥可多说的，记住这几个智能指针的基本之后，多用就完了。



## 14.new/malloc，以及delete/free



## 15.野指针/悬浮指针

具体案例见12_badPointer.cpp文件。

### （1）野指针

野指针的诞生情况：

```c++
#include <iostream>
using namespace std;

int* func(){
    int x = 10;
    return &x;  //2.情况2：返回局部变量的指针；此时如果使用返回的指针，可能会出现未定义问题
}

void func2(int* ptr){
    delete ptr;
}

int main(){
    int *p = new int(4);
    delete p;
    p = nullptr; //1.情况1，没写这句，p指针变成了野指针

    int *ptr = new int(114514);
    func2(ptr); //3.情况3：在 func2 函数中 ptr 被释放，但在 main 函数中仍然可⽤，成为野指针
    //注意，在 func2 函数中不要释放调⽤⽅传递的指针
    //cout<<*ptr<<endl; //未定义行为

}
```

类似于情况1，现在完全可以使用智能指针当中的`unique_ptr`来做，自动管理生命周期。

针对情况3，解决方案是可以避免在函数内释放调⽤⽅传递的指针，或者通过引⽤传递指针：

```c++
void func3(int*& ptr){
    //ptr 是引用，所以在函数内部释放 ptr 不会影响 main 函数中的 ptr
    delete ptr;
    ptr = nullptr;
}

int *ptr2 = new int(1919810);
func3(ptr2); //这是可以的
```



### （2）悬浮指针

悬浮指针是指向已经被销毁的对象的引⽤。当函数返回⼀个局部变ᰁ的引⽤，⽽调⽤者使⽤该引⽤时，就可能产⽣ 悬浮引⽤。访问悬浮引⽤会导致未定义⾏为，因为引⽤指向的对象已经被销毁，数据不再有效。

> **这部分更多地等需要背八股的时候再背就来得及。**



## 16.内存对齐

可以看看这个：[C++内存对齐 | ZHXILIN'S BLOG](https://zhxilin.github.io/post/tech_stack/1_programming_language/modern_cpp/language_base/memory_alignment/)

（这个还没看完）