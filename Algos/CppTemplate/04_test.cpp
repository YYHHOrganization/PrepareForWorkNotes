#include <iostream>
using namespace std;

template<typename T, int v> struct Array{
    T data[v];
};

int main(){
    Array<int, 5> a;
    
    int b = 3;
    //Array<int, b> c; //b不是编译器的常量，这样是不行的, 因为模板的匹配是在编译的时候完成的，所以实例化模板的时候所使用的参数，也必须要在编译期就能确定
    constexpr int c = 5;
    Array<int, c> d; //这样是可以的
    return 0;
}