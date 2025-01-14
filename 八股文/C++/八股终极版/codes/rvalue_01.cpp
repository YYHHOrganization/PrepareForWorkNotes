#include <iostream>
using namespace std;

int main()
{
    int a = 5; // a是个左值
    int &ref_a_left = a; // 左值引用指向左值
    int &&ref_a_right = std::move(a); // 通过std::move将左值转化为右值，可以被右值引用指向
 
    cout << a << endl; // 打印结果：5
    ref_a_right += 10;
    cout << a << endl; // 打印结果:15
    return 0;
}