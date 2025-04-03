#include<iostream>
using namespace std;

template<typename T>
class vector{
public:
    void push_back(T const& x){  //C++ 11要求类模板的变量在调用成员函数的时候，需要看到完整的成员函数定义。
        cout<<"push_back()"<<x<<endl;
    }
    void clear(){
        cout<<"clear()"<<endl;
    };	
private:
    T* elements;
};

// 以下的函数定义也是可以的
// template <typename T>
// void vector<T>::clear()  // 函数的实现放在这里，类似于模板的偏特化
// {
//     // Function body
// }

int main(){
    vector<int> v1;
    vector<double> v2;
    v1.push_back(3);
    v2.push_back(3.14);
    //vector v3; //错误，模板类必须指定类型
}