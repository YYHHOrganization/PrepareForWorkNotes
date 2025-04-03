#include <iostream>
using namespace std;

int* func(){
    int x = 10;
    return &x;  //2.情况2：返回局部变量的指针；此时如果使用返回的指针，可能会出现未定义问题
}

void func2(int* ptr){
    delete ptr;
}

void func3(int*& ptr){
    //ptr 是引用，所以在函数内部释放 ptr 不会影响 main 函数中的 ptr
    delete ptr;
    ptr = nullptr;
}

int main(){
    int *p = new int(4);
    delete p;
    p = nullptr; //1.情况1，没写这句，p指针变成了野指针

    int *ptr = new int(114514);
    func2(ptr); //3.情况3：在 func2 函数中 ptr 被释放，但在 main 函数中仍然可⽤，成为ᰀ指针
    //注意，在 func2 函数中不要释放调⽤⽅传递的指针
    //cout<<*ptr<<endl; //未定义行为
    int *ptr2 = new int(1919810);
    func3(ptr2); //这是可以的
}