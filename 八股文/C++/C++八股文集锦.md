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



