#include <iostream>
#include <cstdint>
using namespace std;

template <int i> class A 
{
public:
    void foo(int)
    {
    }
};

template <uint8_t a, typename b, void* c> class B {};
template <bool flag, void (*a)()> class C {};
template <void (A<3>::*a)(int)> class D {};

template <int i> int Add(int a)	// 当然也能用于函数模板
{
    return a + i;
}

//template <float a> class E {}; // ERROR: 别闹！早说过只能是整数类型的啦！

void foo(){
    A<5> a;  //没问题的
    B<7, A<5>, nullptr>	b; // 模板参数可以是一个无符号八位整数，可以是模板生成的类；可以是一个指针。
    C<false, &foo> c;      // 模板参数可以是一个bool类型的常量，甚至可以是一个函数指针。
    D<&A<3>::foo> d;       // 丧心病狂啊！它还能是一个成员函数指针！
    int x = Add<3>(5);     // x == 8。因为整型模板参数无法从函数参数获得，所以只能是手工指定
}

int main(){

    return 0;
}