#include <iostream>
using namespace std;

template<typename T> class AddFloatOrMulInt{
    static T Do(T a, T b){
        return T(0); // 在这个例子里面一般形式里面是什么内容不重要，因为用不上
        // 这里就随便给个0吧。
    }
};

template<> class AddFloatOrMulInt<float>{
public:
    static float Do(float a, float b){
        return a+b;
    }
};

template<> class AddFloatOrMulInt<int>{
public:
    static int Do(int a, int b){
        return a*b;
    }
};

//第二个例子，编译器期间执行的函数，模板元编程的开始
template<typename T> class TypeToID{
public:
    static int const ID = -1;
};

template<> class TypeToID<float>{
public:
    static int const ID = 1;
};

template<> class TypeToID<void*>{
public:
    static int const ID = 0x401d;
};

int main(){
    cout<<AddFloatOrMulInt<float>::Do(3.14, 2.718)<<endl; //5.858
    cout<<AddFloatOrMulInt<int>::Do(3, 6)<<endl; //18

    cout<<TypeToID<float>::ID<<endl; //1  这里透露出了一个非常重要的信号，希望你已经能察觉出来了： TypeToID 如同是一个函数。这个函数只能在编译期间执行。它输入一个类型，输出一个ID。
    cout << "ID of uint8_t: " << TypeToID<void*>::ID << endl;

    //来看看double
    cout<<TypeToID<double>::ID<<endl; //-1。TypeToID的类模板“原型”的ID是值就是-1。通过这个例子可以知道，当模板实例化时提供的模板参数不能匹配到任何的特化形式的时候，它就会去匹配类模板的“原型”形式。
    return 0;
}