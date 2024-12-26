# C++ 虚表相关

参考链接：https://www.zhihu.com/question/389546003/answer/1194780618

# 一、回顾：如何用C语言模拟一个面向对象的类？

回顾一下C语言纯POD的结构体（struct）：

> POD是指Plain Old Data（普通旧数据）的缩写。具体来说，POD主要指的是那些不包含任何C++特有的复杂性（如虚函数、构造函数等）的数据类型或结构体。

C语言实现一个类似面向对象的类，可以这么写：

```c
#include<stdio.h>
typedef struct Hilichurl
{
    int name;
    int age;
    int weight;
    void (*desc)(struct Hilichurl*);
} Hilichurl;

//obj中各个字段的值不一定被初始化过，通常还会在类内定义一个类似构造函数的函数指针，这里简化
void profile(Hilichurl* obj)
{
    printf("Name: %d\n", obj->name);
    printf("Age: %d\n", obj->age);
    printf("Weight: %d\n", obj->weight);
}

int main()
{
    Hilichurl h;
    h.name = "Hilichurl1";
    h.age = 10;
    h.weight = 100;
    h.desc = profile;

    h.desc(&h); //类似于调用类函数
    return 0;
}
```

想达到面向对象中**数据和操作封装到一起**的效果，只能给struct里面添加函数指针，然后给函数指针赋值。但这样会带来很大的内存开销，因为此时每个实例化的对象中都会有一个8字节的函数指针（64位机器），如果是N个对象，每个对象有M个函数，这样会造成`N*M*8`字节的额外空间开销。

往往在C语言中不会在struct中定义函数指针，而是放在外面（方法二）：

```c
#include<stdio.h>
typedef struct Hilichurl
{
    int name;
    int age;
    int weight;
} Hilichurl;

//obj中各个字段的值不一定被初始化过，通常还会在类内定义一个类似构造函数的函数指针，这里简化
void desc(Hilichurl* obj)
{
    printf("Name: %d\n", obj->name);
    printf("Age: %d\n", obj->age);
    printf("Weight: %d\n", obj->weight);
}

int main()
{
    Hilichurl h;
    h.name = "Hilichurl1";
    h.age = 10;
    h.weight = 100;

    desc(&h); //直接调用函数指针
    return 0;
}
```

> Redis中AE相关的代码实现，便是如此。Redis暂时领域不太相关，先不管了。



## 1.对应的C++代码

如果在C++中实现上面的功能，代码我们比较熟了，如下：

```c++
#include <iostream>
using namespace std;

class Hilichurl
{
public:
    int name;
    int age;
    int weight;
    void desc()
    {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "Weight: " << weight << endl;
    }
};

int main()
{
    Hilichurl h;
    h.name = 1;
    h.age = 10;
    h.weight = 100;

    h.desc();
    return 0;
}
```

看起来，调用方式是`h.desc();`，那么实际上在C++中这相当于上面C语言版本的哪种实现方式呢？**其实相当于方法二**。C++编译器实际会帮你生成一个类似上例中C语言写法二的形式（这也算是C++ zero overhead指导方针的一个体现），但实际上C++由于支持重载，会存在命名崩坏（暂时不用细究了），但原理是差不多的。

**所以实际上，C++中对类的封装只是对程序员而言的，编译器编译后依然是面向过程的代码。编译器帮你给成员函数增加一个额外的类指针参数，运行期间传入对象实际的指针。**类的数据（[成员变量）](https://zhida.zhihu.com/search?content_id=247303351&content_type=Answer&match_order=1&q=成员变量）&zhida_source=entity)和操作（成员函数）其实还是分离的**。**

每个函数都有地址（指针），不管是全局函数还是成员函数在编译之后几乎类似。

在类不含有虚函数的情况下，编译器在编译期间就会把函数的地址确定下来，运行期间直接去调用这个地址的函数即可。**这种函数调用方式也就是所谓的『静态绑定』（static binding）。**

> 补充知识：在C++中，普通函数和类成员函数通常会放在内存的代码段（text segment）区域。代码段是存放程序执行代码的区域，通常是只读的，以防止程序在运行时意外修改其指令。
>
> 具体来说：
>
> - **普通函数**：这些函数的机器代码会被存储在代码段中。
> - **类成员函数**：这些函数也是以机器代码的形式存储在代码段中，尽管它们与类的实例相关联，但它们的实现仍然是独立于任何特定对象的。
>
> 总结来说，普通函数和类成员函数都位于内存的代码段区域。



# 二、虚函数的用法

虚函数的出现其实就是为了实现面向对象三个特性之一的『多态』（[polymorphism](https://zhida.zhihu.com/search?content_id=247303351&content_type=Answer&match_order=1&q=polymorphism&zhida_source=entity)）。来看一个例子：

```c++
#include<iostream>
#include<string>
using namespace std;

class Monster
{
public:
    Monster(string name, int id, int hp) : name(name), id(id), hp(hp) {}
    virtual void desc()
    {
        cout << "Name: " << name << endl;
        cout << "ID: " << id << endl;
        cout << "HP: " << hp << endl;
    }
    string name;
    int id;
    int hp;
};

class Hilichurl : public Monster
{
public:
    Hilichurl(string name, int id, int hp, int atk) : Monster(name, id, hp), atk(atk) {}
    void desc()
    {
        cout << "Name: " << name << endl;
        cout << "ID: " << id << endl;
        cout << "HP: " << hp << endl;
        cout << "ATK: " << atk << endl;
    }
    int atk;
};

int main()
{
    Monster m("Monster1", 1, 100);
    Hilichurl h("Hilichurl1", 2, 100, 10);

    m.desc();
    h.desc();
    return 0;
}
```

在main函数中，我们创建了一个父类的对象和一个子类的对象，并调用他们的desc函数，这个结果是显然的：父类调用父类的desc函数，子类调用子类重写的desc函数。现在我们把main函数改为：

```c++
Hilichurl h("Hilichurl1", 1, 100, 10);
Monster* m = &h; //父类指针指向子类对象
m->desc(); //调用子类的desc

Monster& m2 = h; //父类引用指向子类对象
m2.desc(); //调用子类的desc
```

此时用父类指针指向子类对象，最终调用desc函数的时候调用的是子类的。这个现象称之为『**动态绑定**』（dynamic binding）或者『**延迟绑定**』（lazy binding）。**如果把父类中的virtual关键字去掉，则这个代码最终将调用父类的函数desc，而非子类的desc。**

这是为什么呢？指针实际指向的还是子类对象的内存空间，可是为什么不能调用到子类的desc？这个就是前面提到的：**类的数据（成员变量）和操作（成员函数）其实是分离的**。仅从对象的内存布局来看，只能看到成员变量，看不到成员函数。因为调用哪个函数是编译期间就确定了的，编译期间只能识别父类的desc。**现在已经对多态有了一个基本的认知，那么多态在C++当中是如何实现的呢？**



## 1.虚表

具体如何实现C++的多态是由编译器厂商来决定的，但主流做法一般都使用虚表指针来做，而且应该也是现在实现多态的最常见做法。我们先给父类再添加一个虚函数，然后子类重写这个虚函数，代码修改为：

```c++
#include<iostream>
#include<string>
using namespace std;

class Monster
{
public:
    Monster(string name, int id, int hp) : name(name), id(id), hp(hp) {}
    virtual void desc()
    {
        cout << "Name: " << name << endl;
        cout << "ID: " << id << endl;
        cout << "HP: " << hp << endl;
    }

    virtual void attack()
    {
        cout<<"Monster attack!"<<endl;
    }
    string name;
    int id;
    int hp;
};

class Hilichurl : public Monster
{
public:
    Hilichurl(string name, int id, int hp, int atk) : Monster(name, id, hp), atk(atk) {}
    void desc()
    {
        cout << "Name: " << name << endl;
        cout << "ID: " << id << endl;
        cout << "HP: " << hp << endl;
        cout << "ATK: " << atk << endl;
    }

    void attack()
    {
        cout<<"Hilichurl attack!"<<endl;
    }

    int atk;
};

int main()
{
    Hilichurl h("Hilichurl1", 1, 100, 10);
    h.desc();
    Monster* m = &h; //父类指针指向子类对象
    m->desc(); //调用子类的desc

    Monster& m2 = h; //父类引用指向子类对象
    m2.desc(); //调用子类的desc
    return 0;
}
```

此时，main函数应该会打印Hilichurl的信息三次，因为不管是h，m还是m2调用到的都是子类（前面的知识点已经学过了）。

 

### （1）g++输出内存布局

首先来看一下g++的版本：

```shell
g++ -V  # gcc -V也可以
```

![image-20241225164505561](./assets/image-20241225164505561.png)

然后可以dump出来cpp文件的内存布局：

```shell
g++ -fdump-lang-class Cpp_PolyMorphism.cpp
```

搜索dump出来的文件（以.class结尾）中的内容，可以看到下面的关键信息：

```cpp
Vtable for Monster
Monster::_ZTV7Monster: 4 entries
0     (int (*)(...))0
8     (int (*)(...))(& _ZTI7Monster)
16    (int (*)(...))Monster::desc
24    (int (*)(...))Monster::attack
    
Vtable for Hilichurl
Hilichurl::_ZTV9Hilichurl: 4 entries
0     (int (*)(...))0
8     (int (*)(...))(& _ZTI9Hilichurl)
16    (int (*)(...))Hilichurl::desc
24    (int (*)(...))Hilichurl::attack

Class Monster
   size=48 align=8
   base size=48 base align=8
Monster (0x0x6695f60) 0
    vptr=((& Monster::_ZTV7Monster) + 16)

Class Hilichurl
   size=56 align=8
   base size=52 base align=8
Hilichurl (0x0x669b3a8) 0
    vptr=((& Hilichurl::_ZTV9Hilichurl) + 16)
Monster (0x0x66e56c0) 0
      primary-for Hilichurl (0x0x669b3a8)
```

以下是GPT-4o的解释：

> ### 1. **Vtable（虚拟表）** 的解释
>
> C++ 中使用虚函数时，为了支持多态性，编译器为每个类生成一个虚表（vtable），该表包含了指向虚函数的指针。虚表在每个类的对象中存储了指向函数的指针，这样在运行时可以根据对象的实际类型来调用对应的函数。
>
> #### `Vtable for Monster`:
>
> ```
> Vtable for Monster
> Monster::_ZTV7Monster: 4 entries
> 0     (int (*)(...))0
> 8     (int (*)(...))(& _ZTI7Monster)
> 16    (int (*)(...))Monster::desc
> 24    (int (*)(...))Monster::attack
> ```
>
> - `Monster::_ZTV7Monster`：这是 `Monster` 类的虚拟表。
> - 4 entries：这个虚拟表有 4 个条目，表示该类有 4 个虚函数。
>   - 第 1 个条目是 `0`，通常表示指向虚继承或空的指针，`Monster` 类并没有虚继承或需要其他特殊处理的虚函数。
>   - 第 2 个条目 `(& _ZTI7Monster)` 是指向类型信息（`type_info`）的指针，用于运行时类型识别（RTTI）。
>   - 第 3 个条目是 `Monster::desc`，指向 `Monster` 类的 `desc` 函数（虚函数）。
>   - 第 4 个条目是 `Monster::attack`，指向 `Monster` 类的 `attack` 函数（虚函数）。
>
> #### `Vtable for Hilichurl`:
>
> ```
> Vtable for Hilichurl
> Hilichurl::_ZTV9Hilichurl: 4 entries
> 0     (int (*)(...))0
> 8     (int (*)(...))(& _ZTI9Hilichurl)
> 16    (int (*)(...))Hilichurl::desc
> 24    (int (*)(...))Hilichurl::attack
> ```
>
> - `Hilichurl::_ZTV9Hilichurl` 是 `Hilichurl` 类的虚拟表。
> - 与Monster类类似，Hilichurl类也有 4 个条目。
>   - 这其中 `Hilichurl::desc` 和 `Hilichurl::attack` 分别是 `Hilichurl` 类重写的虚函数。
>   - 和 `Monster` 一样，前两条记录与类型信息和虚继承相关。
>
> ### 2. **类的内存布局**
>
> #### `Class Monster`:
>
> ```
> Class Monster
>    size=48 align=8
>    base size=48 base align=8
> Monster (0x0x6695f60) 0
>     vptr=((& Monster::_ZTV7Monster) + 16)
> ```
>
> - `size=48`：`Monster` 类的对象大小是 48 字节。
> - `align=8`：类对象的对齐要求是 8 字节。
> - `base size=48`：`Monster` 类的基础部分大小为 48 字节，说明它的成员（如 `name`、`id` 和 `hp`）加上虚函数表指针的总大小为 48 字节。
> - `vptr=((& Monster::_ZTV7Monster) + 16)`：虚函数表指针（vptr）指向 `Monster::_ZTV7Monster` 表的地址，偏移量是 16 字节。这意味着虚函数表指针的位置是在 `Monster` 类对象的内存布局中的某个地方。
>
> #### `Class Hilichurl`:
>
> ```
> Class Hilichurl
>    size=56 align=8
>    base size=52 base align=8
> Hilichurl (0x0x669b3a8) 0
>     vptr=((& Hilichurl::_ZTV9Hilichurl) + 16)
> Monster (0x0x66e56c0) 0
>       primary-for Hilichurl (0x0x669b3a8)
> ```
>
> - `size=56`：`Hilichurl` 类对象的大小是 56 字节，比 `Monster` 类大。
> - `base size=52`：`Hilichurl` 类的基础部分（继承自 `Monster`）占用 52 字节。
>   - **看起来Monster占用48字节，为什么Hilichurl占用52字节呢**？应该是因为子类有自己的对象，引发编译器做内存对齐的时候会有所更新，但应该不是本节虚表相关的重点内容。
> - `vptr=((& Hilichurl::_ZTV9Hilichurl) + 16)`：`Hilichurl` 类对象的虚函数表指针指向 `Hilichurl::_ZTV9Hilichurl` 表，偏移量同样是 16 字节。
>
> `Hilichurl` 类相对于 `Monster` 类多了一个成员变量 `atk`，所以它的大小比 `Monster` 多了 8 字节。
>
> #### `primary-for Hilichurl`:
>
> ```
> primary-for Hilichurl (0x0x669b3a8)
> ```
>
> 这表明 `Hilichurl` 类继承自 `Monster`，并且在内存中存储 `Hilichurl` 对象时，父类 `Monster` 对象的内存会嵌套在其中（==此处存疑==）。
>
> ### 3. **总结**
>
> - `vtable` 机制支持了运行时的多态性，通过虚函数表来实现。
> - `Monster` 类和 `Hilichurl` 类的虚函数表指针分别指向对应类的虚拟表。
> - `Monster` 类的对象大小为 48 字节，`Hilichurl` 类的对象大小为 56 字节，多出来的 8 字节是因为 `Hilichurl` 类新增了成员变量 `atk`。
> - 在继承体系中，`Hilichurl` 类会包含一个指向父类 `Monster` 的虚函数表指针。

继续上文的知识介绍，**也就是说在含有虚函数的类编译期间，编译器会自动给这种类在起始位置追加一个虚表指针**，（称之为：vptr）。**vptr指向一个虚表（称之为：vtable 或 vtbl）**，虚表中存储了实际的函数地址。

vptr指向的并不是虚表的表头，而是直接指向的虚函数的位置，看上面dump出来的结果，vptr指向的是Hilichurl的vtable + 16个字节的位置，也就是虚表的地址。

剩下的部分看这里吧：参考链接：https://www.zhihu.com/question/389546003/answer/1194780618，不太好描述。

