#include <iostream>
using namespace std;

template <typename T>
class RemovePointer
{
public:
    typedef T Result;  // 如果放进来的不是一个指针，那么它就是我们要的结果。
};

template <typename T>
class RemovePointer<T*>	// 祖传牛皮藓，专治各类指针
{
public:
public:
    // 如果是传进来的是一个指针，我们就剥夺一层，直到指针形式不存在为止。
    // 例如 RemovePointer<int**>，Result 是 RemovePointer<int*>::Result，
    // 而 RemovePointer<int*>::Result 又是 int，最终就变成了我们想要的 int，其它也是类似。
    typedef typename RemovePointer<T>::Result Result;
};

void Foo()
{
    RemovePointer<float****>::Result x = 5.0f; // 用RemovePointer后，那个Result就是把float*的指针处理掉以后的结果：float啦。
    std::cout << x << std::endl;  //5
}

int main(){
    Foo();
    return 0;
}