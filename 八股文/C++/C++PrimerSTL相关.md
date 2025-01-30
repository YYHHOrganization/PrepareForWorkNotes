# C++PrimerSTL相关

# 第九章 顺序容器

![image-20250127205749690](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250127205749690.png)

- `forward_list`和`array`是C++ 11中新增的。`forward_list`没有size操作（毕竟保存或计算其大小会比手写链表带来额外的开销）。
- 通常，使用`vector`是最好的选择，除非有很好的理由选择其他容器。其他的一些选择的准则可以参考p293。
- p294：对容器可以保存的元素类型的限制。如果容器中存的类没有默认构造函数，则需要提供一个元素初始化器（比如显式指定元素初始值）。



## 9.2.1 迭代器

`iterator`：注意`forward_list`的迭代器不支持`--`运算符。迭代器的范围是`begin`和`end`，但`end`是在尾元素之后的位置。换句话说，元素范围是左闭右开区间：`[begin, end)`。

一个用`begin`和`end`遍历`vector`的例子：
```c++
#include <iostream>
#include <vector>

int main() {
    // 创建一个 std::vector 并初始化一些整数
    std::vector<int> vec = {10, 20, 30, 40, 50};

    // 使用迭代器遍历 vector
    std::cout << "Using iterator to traverse the vector:" << std::endl;
    
    // 使用 begin() 和 end() 方法获取迭代器
    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
        std::cout << *it << " "; // 输出当前迭代器指向的元素
    }
    
    std::cout << std::endl;

    // 另一种方式，使用 const_iterator 遍历（如果不想修改元素）
    std::cout << "Using const_iterator to traverse the vector:" << std::endl;
    
    for (std::vector<int>::const_iterator it = vec.cbegin(); it != vec.cend(); ++it) {
        std::cout << *it << " "; // 输出当前迭代器指向的元素
    }

    std::cout << std::endl;

    return 0;
}
```

- 当不需要写访问时，可以使用`cbegin`和`cend`。



## 9.2.4 容器定义和初始化

### （1）关于array

在C++中，我们不能对内置数组类型做拷贝或对象赋值操作，但对于`array`来说是可以的，来看下面这个例子：

```c++
int a[3] = {1,2,3};
//int b[3] = a; //Error
array<int, 3> arr1{1,2,3};
array<int, 3> arr2 = arr1; //OK
```



## 9.2.5 赋值和swap

![image-20250127212156470](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250127212156470.png)



也就是说，`c={a,b,d}`这种赋值对于`array`来说是不适用的。其他的一些操作如下：

- 两个容器的交换：`swap(c1, c2)`或者`c1.swap(c2)`。swap通常比从c2向c1拷贝元素快得多。马上会有更多介绍。



### （1）assign（仅顺序容器）

在 C++ STL 中，`assign` 是一个成员函数，常用于将新的内容分配给容器元素。它可以用于多个容器，如 `std::vector`、`std::list` 等。`assign` 函数通常有几种重载形式，可以用来从另一个容器复制元素、从指定范围填充或者直接用特定值填充。

比如来看下面这个例子：

```c++
#include <iostream>
#include <vector>

int main() {
    // 创建一个 std::vector 并初始化一些整数
    std::vector<int> vec = {1, 2, 3, 4, 5};

    std::cout << "Original vector elements: ";
    for (const auto& elem : vec) {
        std::cout << elem << " "; // 输出原始元素
    }
    std::cout << std::endl;

    // 使用 assign 从另一个 vector 赋值
    std::vector<int> otherVec = {10, 20, 30};
    vec.assign(otherVec.begin(), otherVec.end()); // 赋值为其他 vector 的元素

    std::cout << "After assign from other vector: ";
    for (const auto& elem : vec) {
        std::cout << elem << " "; // 输出修改后的元素
    }
    std::cout << std::endl;

    // 使用 assign 填充相同的值
    vec.assign(5, 100); // 将所有元素赋值为 100

    std::cout << "After assigning 5 elements with value 100: ";
    for (const auto& elem : vec) {
        std::cout << elem << " "; // 输出修改后的元素
    }
    std::cout << std::endl;

    return 0;
}
```

输出结果为：

> Original vector elements: 1 2 3 4 5
> After assign from other vector: 10 20 30
> After assigning 5 elements with value 100: 100 100 100 100 100 



### （2）swap

调用`swap`时，元素本身并没有交换，`swap`只是交换了两个容器的内部数据结构，示例如下：
```c++
vector<int> a(10);
vector<int> b(20);
swap(a, b);
cout << a.size()<<" "<<b.size()<<endl; //20 10
```

除`array`外，`swap`不对任何元素进行拷贝、删除或插入操作，因此可以在常数时间内完成。

![image-20250127213815414](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250127213815414.png)

也就是说，`swap`有两个特殊情况：`string`和`array`。==这里《C++ Primer》讲的不是很清晰，如有需要后面再做学习总结。==



## 9.2.6 容器大小操作

可以直接比两个容器的大小，跟字符串比较的准则有点像。注意，只能用同类型的容器才能放在一起比，比如`vector<int>`和`vector<int>`。直接看例子吧：

```c++
vector<int> a{1,2,5};
vector<int> b{1,2};
vector<int> c{1,2,4,4};

cout<<(a<b)<<endl; //0
cout<<(a<c)<<endl; //0
cout<<(b<c)<<endl; //1
```

- 注：只有当容器的元素类型定义了相应的比较运算符时，我们才可以使用关系运算符来比较两个容器。容器相等运算是通过元素的`==`来实现的，而其他关系运算符则是通过元素的`<`运算实现。



## 9.3 顺序容器操作

![image-20250127215347079](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250127215347079.png)

在使用以上操作的时候，一定要注意性能。比如，在`vector`或`string`的尾部以外的任何位置，或者是`deque`的首尾之外的任何位置添加元素，都需要移动元素。并且，向`vector`或`string`添加元素可能引起整个对象存储空间的重新分配。

### （1）push_back

除`array`和`forward_list`之外，每个顺序容器都支持`push_back`。注意：**容器元素是拷贝。（p306）**。当我们将一个对象放入容器时，容器会调用该对象的拷贝构造函数，创建一个新的对象副本。这意味着容器中的每个元素都是其原始对象的一个独立副本。

看下面这个例子：

```c++
#include <iostream>
#include <vector>

class MyClass {
public:
    int value;

    MyClass(int v) : value(v) {}
    
    // 拷贝构造函数
    MyClass(const MyClass& other) : value(other.value) {
        std::cout << "Copy constructor called for value: " << value << std::endl;
    }
};

int main() {
    std::vector<MyClass> vec;

    MyClass obj1(10);
    vec.push_back(obj1); // 调用拷贝构造函数
    obj1.value = 1000;
    std::cout << "Original object value: " << obj1.value << std::endl;

    std::cout << "Vector first element value: " << vec[0].value << std::endl;

    return 0;
}
//++++++++输出++++++++
Copy constructor called for value: 10
Original object value: 1000
Vector first element value: 10
```



### （2）push_front

这里有需要看p306页即可。

注意，`deque`和`vector`一样提供了随机访问元素的能力，但其有`vector`不支持的`push_front`操作。`deque`保证在容器首尾插入和删除元素是常数时间的，但首位之外的位置会很耗时。



### （3）其他：insert

- 在容器中的指定位置添加元素：p307
  - `mlist.insert(iter,"begin")`，会插入到`iter`表示的迭代器之前。这就意味着如果iter指向了容器的`begin()`,那么就相当于`push_front()`。
- 插入范围内元素：p307：
  - 注：[1191. K 次串联后最大子数组之和 - 力扣（LeetCode）](https://leetcode.cn/problems/k-concatenation-maximum-sum/description/)这道题目题解里用了`vec.insert(vec.end(), vec.begin(), vec.end())`也没什么问题，《C++ Primer》建议不要写这种：`a.insert(a.begin(),a.begin(), a.end());`，不过运行下来也没什么问题，先不细究了。

以上两种情况的`insert`返回指向第一个新加入的元素的迭代器。如果范围为空，不插入任何元素，`insert`将会把第一个参数返回。通过这个小技巧，可以实现把用户输入的每个单词头插到list当中，实现翻转操作，代码如下：

```c++
int main() {
    int n;
    cin>>n;
    list<string> words;
    auto iter = words.begin();
    string s;
    while(n--)
    {
        cin>>s;
        iter = words.insert(iter, s); //思考：这是一直头插
    }
    for(string s: words) cout<<s<<endl;
    return 0;
}
```



### ==（4）emplace操作（emplace_back&push_back）==

直接看这篇吧：[C++中push_back和emplace_back的区别 - 知乎](https://zhuanlan.zhihu.com/p/213853588)

这篇比较清晰，省流看这篇：[C++ 中 push_back 和 emplace_back 的区别 - 知乎](https://zhuanlan.zhihu.com/p/464737089)

> 答案：
>
> 1. **功能**：
>
> - **`push_back`**：
>   - 将一个已有的对象（或值）复制/移动到容器的末尾。
>   - 对于传入的参数，如果是右值，会调用移动构造；如果是左值，则会调用拷贝构造。
> - **`emplace_back`**：
>   - 直接在容器内部构造一个新对象，而不是先创建一个对象再拷贝或移动。
>   - 可以接受多个参数并根据这些参数调用对应的构造函数，这样更加高效。
>
> 2. **性能**：
>
> - **`push_back`**：
>   - 在某些情况下，会导致不必要的拷贝或移动构造。如果对象较大或者拷贝开销较高，性能可能受影响。
> - **`emplace_back`**：
>   - 通过直接在容器中构造对象，可以避免拷贝或移动，从而提高性能，尤其是在处理大型对象时。

现在我们来写一个对比，来看看这两个的区别：

```c++
#include<iostream>
#include<vector>
using namespace std;

class GenshinVersion
{
    public:
        //构造函数
        GenshinVersion(float version): version(version) {cout<<"constructor"<<endl;}
        //拷贝构造函数
        GenshinVersion(const GenshinVersion& g): version(g.version){cout<<"copy constructor"<<endl;}
        //移动构造函数,不能有const,因为会修改传入的g
        GenshinVersion(GenshinVersion&& g): version(g.version){cout<<"move constructor"<<endl;}
  
        float version;
};

int main()
{
    vector<GenshinVersion> genshinVersion;
    genshinVersion.reserve(10); //预先分配一下内存,不然可能会因为空间分配不足而发生重新分配
    cout<<"==========push_back============"<<endl;
    genshinVersion.push_back(5.4);
    cout<<"==========emplace_back============"<<endl;
    genshinVersion.emplace_back(5.4);
    return 0;
}
```

输出的结果为：

```c++
==========push_back============
constructor
move constructor
==========emplace_back============
constructor
```

还是比较清晰的：

> 1. **`push_back(5.4)`**:
>
>    - 当你调用`push_back(5.4)`时，会进行以下步骤：
>      - 5.4 会通过 `GenshinVersion` 的构造函数转换为一个新对象，此时会打印 `"constructor"`。
>      - 然后，由于 `std::vector` 需要管理内存，当插入新的对象时，它可能会触发拷贝或移动构造。由于 `vector` 可能在内部重新分配内存以容纳新元素，因此它需要使用拷贝构造函数将当前对象（包括自动生成的对象）复制到新的内存中。这将导致打印 `"move constructor"`，因为 `vector` 对象会被转移到新的位置。(C++11后的`push_back`也可以接收右值了，因此调用移动构造函数即可)
>
>    因此，这部分的输出是：
>
>    ```c++
>    constructor
>    move constructor
>    ```
>
> 2. **`emplace_back(5.4)`**:
>
>    - 调用`emplace_back(5.4)`时，会:
>      - 在 `vector` 内部直接**原地**构造一个 `GenshinVersion` 对象，同样会调用构造函数并打印 `"constructor"`。
>      - 在此情况下，不会有拷贝或移动构造函数的调用，因为 `emplace_back` 是直接在容器内构造对象，避免了不必要的拷贝。
>
>    这部分的输出是：
>
>    ```c++
>    constructor
>    ```

如果构造函数有多个元素，可以用`genshinVersion.emplace_back(5.5, 1)`这种方式来构造，`emplace_back`依旧会原地构造。



注意，可以试试注释掉`genshinVersion.reserve(10);`这句，在我的编译器下输出结果变成了：

```c++
==========push_back============
constructor
move constructor
==========emplace_back============
constructor
copy constructor
```

此时`emplace_back`并没有起到很好的优化作用，推测是当 `std::vector` 的容量不足以容纳新元素时，会触发内存的重新分配。在这种情况下，原有的元素需要被移动或拷贝到新的内存位置。如果发生了重新分配，所有现有的元素都会被拷贝到新的位置，这时会调用拷贝构造函数。所以`emplace_back`会调用到拷贝构造函数。

**实际测试下，把`push_back`和`emplace_back`的东西改成`std::move(GenshinVersion(5.4))`或者`GenshinVersion(5.4)`的话，两者的调用就是一样的了，都会调构造函数和移动构造函数。这是因为`GenshinVersion(5.4)`本身肯定会调用一次构造函数。**

个人理解，`emplace_back`的一个优化是当这样调用时：

```c++
genshinVersion.push_back(5.4);
genshinVersion.emplace_back(5.4);
```

`emplace_back`会倾向于原地构造，可能会减少一次移动构造的过程，从而带来性能上的优化。



注意：类中构造函数要传入多个参数时，可以这么调用：

```c++
cout<<"==========push_back============"<<endl;
genshinVersion.push_back({5.4, 60000000}); //push_back的版本不能写(5.4, 60000000)
cout<<"==========emplace_back============"<<endl;
genshinVersion.emplace_back(5.4, 60000000);
```

此时输出的结果为（依旧可以看到`emplace_back`带来的性能优化）：

```c++
==========push_back============
constructor
move constructor
==========emplace_back============
constructor
```



## 9.3.2 访问元素

包括`array`在内的每个顺序容器都有`front`成员函数，除了`forward_list`之外都有`back`成员函数，这两个分别会返回首元素和尾元素的引用。

![image-20250128133521237](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250128133521237.png)

另外，在容器中访问元素的成员函数（`front`，`back`和`at`）返回的都是引用。如果容器是`const`对象则返回的是`const`引用，否则是普通引用，可以用来修改容器元素的值。来看下面这个例子：

```c++
vector<int> a{1,2,3};
int b = a.back();
b = 10; //此时并不会改变容器中的值
for(int x: a) cout<<x<<endl;  // 1 2 3

cout<<"========ref==========="<<endl;
int& c = a.back();
c = 114514;
for(int x: a) cout<<x<<endl; // 1 2 114514
```

如果要使用`auto`来改变元素值的话，记得也要写作`auto& c = a.back();`（需要引用）。



**下标操作和安全的随机访问**

![image-20250128134018182](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250128134018182.png)

比如下面的代码：

```c
vector<int> a{1,2,3};
cout<<a[4]<<endl;
cout<<a.at(4)<<endl;
```

在gcc编译器下的输出结果为：

> 0
> terminate called after throwing an instance of 'std::out_of_range'
>   what():  vector::_M_range_check: __n (which is 4) >= this->size() (which is 3)



## 9.3.3 删除元素

这里看第p311页开始即可。下面举两个关于`erase`的例子，首先是删除`list`当中的所有奇数元素：

```c++
list<int> a{1,2,3,4,5,6,7,8,9,10};
auto iter = a.begin();
while(iter!=a.end())
{
    if(*iter % 2 == 1)
        iter = a.erase(iter); //返回指向待删除元素后面的位置(回忆迭代器的左闭右开)
    else ++iter;
}
```

如果是删除多个元素，就会删到`iter1`开始到`iter2`指向位置之前的元素，并且在删除之后`iter1==iter2`。其实为了理解这个看以下代码就好：

```c++
auto iter2 = a.begin();
iter2 = a.erase(a.begin(), a.end()); //相当于a.clear()
assert(iter2==a.end());
```



### 特殊的`forward_list`删除元素

回忆一下正常的单链表删除某个位置的元素，理论上要把前一个节点链接到下一个节点，但实际上在单链表中我们不太好找到待删除的节点的前一个节点，因此在一个`forward_list`中添加或删除元素是通过改变给定元素之后的元素来完成的。对应到接口就是`insert_after`和`erase_after`。如下图：

![image-20250128153300014](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250128153300014.png)

如果是在`forward_list`当中删除所有奇数的元素，代码这样写：

```c++
forward_list<int> a{1,2,3,4,5,6,7,8,9,10};
auto pre = a.before_begin();
auto cur = a.begin();
while(cur!=a.end())
{
    if(*cur%2==1) cur = a.erase_after(pre); //删除pre之后的元素，也就是删除当前cur所指的元素，返回值是被删元素之后的位置
    else 
    {
        pre = cur;
        ++cur;
    }
}
for(auto x:a) cout<<x<<endl;
```



## 9.3.5 改变容器大小

`array`并不支持`resize`。来看例子体会`resize`的用法（p314 9.3.5节）：

```c++
list<int> ilist(10, 5); //10个5
print(ilist); //5 5 5 5 5 5 5 5 5 5

ilist.resize(15); //将5个0添加到ilist的末尾
print(ilist); //5 5 5 5 5 5 5 5 5 5 0 0 0 0 0

ilist.resize(25, -1); //在ilist的末尾+10个-1
print(ilist); //5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1

ilist.resize(5); //删除后15个值,只保留前5个
print(ilist); //5 5 5 5 5

ilist.resize(3, -2); //结果是555, -2会被忽略掉
print(ilist);// 5 5 5
```

![image-20250128154912131](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250128154912131.png)

如果调用了`resize`会向容器中添加新的元素，且为类类型，需要保证提供初始化或者是有默认构造函数。



## 9.3.6 容器操作可能会导致迭代器失效

p315。有需要再看。最重要的其实就是**当向容器中添加元素或者删除元素时，有可能会导致迭代器失效。要保证每次改变容器操作之后都能正确定位到迭代器。**比如《C++ Primer》p316页有这样的示例：

![image-20250128155611218](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250128155611218.png)

> 注：**C#**: 使用 `foreach` 遍历时不允许在循环内修改集合（如插入或删除），否则将抛出异常。在做项目的时候有遇到过这个问题，一种解决方案是复制出来一个修改，再赋值回去。

C++这种边删边遍历其实危险挺大的，个人感觉少用为妙。

> 注：p316：**不要缓存end返回的迭代器。**如果在一个循环中插入/删除`deque`,`string`或者`vector`中的元素，不要缓存`end`返回的迭代器，每次需要的时候应该重新计算一次`end`，防止迭代器失效问题。



## 9.4 `vector`对象是如何增长的

> 在 C++ 中，`std::vector` 是一个动态数组，它可以在运行时调整其大小。当向 `vector` 中添加元素时（例如通过调用 `push_back` 或 `emplace_back`），如果当前容量不足以容纳新元素，`vector` 会自动进行扩展。下面是 `std::vector` 在增长时的一些关键点：
>
> ### 1. **容量和大小**
>
> - **大小 (size)**: `size()` 返回当前存储的元素数量。
> - **容量 (capacity)**: `capacity()` 返回当前分配的内存大小，以便容纳元素。
>
> ### 2. **增长策略**
>
> 当容量不足以新增一个元素时，`std::vector` 会执行以下操作：
>
> 1. **分配新的内存块**:
>    - 通常会将容量扩大一倍（具体实现可能有所不同）。这意味着，如果当前容量为 `N`，在需要扩展时，会增加到大约 `2 * N` 的容量。这种策略旨在减少频繁的内存分配和拷贝操作，提高性能。
> 2. **移动现有元素**:
>    - 将现有的元素从旧的内存位置拷贝或移动到新的内存位置。这一步涉及对每个元素的拷贝构造或移动构造。
> 3. **释放旧的内存**:
>    - 一旦所有元素都被移动到新的内存位置，会释放原来的内存块。

注：`reserve`并不改变容器中元素的数量，它仅影响`vector`预先分配多大的内存空间。只有当需要的内存空间超过当前容量时，`reserve`调用才会改变`vector`的容量。如果需求大小大于当前容量，`reserve`至少分配与需求一样大的内存空间（可能更大）。如果需求大小<=当前容量，则`reserve`什么都不做，自然肯定不会把分配的内存回收掉。因此，在调用`reserve`之后，`capacity`不会小于传递给`reserve`的参数。

**`reserve`要和`resize`做好区分。`resize`无法改变容器预留的内存空间。`resize`**只会改变容器中的元素数目，而不会改变容器容量。`C++11`提供了`shrink_to_fit`函数来退回不需要的内存空间，但编译器有可能会忽略这个请求。



- p318：`capacity`与`size`值得看一下，以下给一个例子：

```c++
int main() {
    std::vector<int> vec;
    
    std::cout << "Initial size: " << vec.size() << ", capacity: " << vec.capacity() << std::endl;

    for (int i = 0; i < 20; ++i) {
        vec.push_back(i);
        std::cout << "After adding " << i << ": size = " << vec.size() << ", capacity = " << vec.capacity() << std::endl;
    }

    return 0;
}
```

输出结果为：

```c++
Initial size: 0, capacity: 0
After adding 0: size = 1, capacity = 1 
After adding 1: size = 2, capacity = 2 
After adding 2: size = 3, capacity = 4 
After adding 3: size = 4, capacity = 4 
After adding 4: size = 5, capacity = 8 
After adding 5: size = 6, capacity = 8 
After adding 6: size = 7, capacity = 8 
After adding 7: size = 8, capacity = 8 
After adding 8: size = 9, capacity = 16
After adding 9: size = 10, capacity = 16
After adding 10: size = 11, capacity = 16
After adding 11: size = 12, capacity = 16
After adding 12: size = 13, capacity = 16
After adding 13: size = 14, capacity = 16
After adding 14: size = 15, capacity = 16
After adding 15: size = 16, capacity = 16
After adding 16: size = 17, capacity = 32
After adding 17: size = 18, capacity = 32
After adding 18: size = 19, capacity = 32
After adding 19: size = 20, capacity = 32
```

看起来，在本地的gcc编译器上，是每次扩充两倍的`capacity`。更多的细节会在面经当中进行整理。原则上，只有当insert相关操作时`size`与`capacity`相等，或者调用`resize`或`reserve`时给定的大小超过当前的`capacity`，才会重新分配容器的内存空间。



## 9.5 额外的string操作

有需要直接看p320页吧。这里给出一些关键词，忘了可以看看：

- 构造`string`的其他方法：p321
- `s.substr(pos, n)`:返回一个string，包含s从`pos`开始的n个字符的拷贝，默认`n`是`s.size()-pos`，即拷贝从`pos`开始的所有字符；
- p322 9.5.2：改变`string`的其他方法：
  - `insert`&`erase`
  - `append`&`replace`

![image-20250128163323159](C++PrimerSTL%E7%9B%B8%E5%85%B3.assets/image-20250128163323159.png)



## 9.5.3 `string`搜索操作

先看到这，后面再做整理。p325
