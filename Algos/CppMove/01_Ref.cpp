#include <iostream>
#include <vector>
using namespace std;

int main(){
    int a = 5;
    int &ref = a;
    //int &ref2 = 5; // 编译错误,5是右值，没有地址
    const int &ref2 = 5; // 编译通过
    vector<int> intVec;
    intVec.push_back(5);  //可以阅读一下vector的push_back函数，左值版本是有const的

    int&& rRef = 5; // 右值引用
    //int &&rRef2 = a; // 编译错误，a是左值
    rRef = 6; // 右值引用可以修改值
    
    int &&rRef3 = std::move(a); // std::move可以将左值转换为右值
    cout<<a<<endl; // 5,实际上a里还是有值的，实际上move就是强制把左值转换为了右值，
    return 0;
}