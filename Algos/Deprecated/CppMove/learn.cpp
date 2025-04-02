#include <iostream>
#include <vector>
using namespace std;

class A
{
public:
    int a;
    A(int a1): a(a1) {}
    A() 
    {
        cout << "Default constructor" << endl;
    }
    //拷贝构造函数
    A(const A& a1)
    {
        cout << "Copy constructor" << endl;
    }

    //重载赋值运算符
    A& operator=(const A& a1)
    {
        cout << "Copy assignment operator" << endl;
        return *this;
    }
};

void func1(const A& val) //引用
{
    cout << "Lvalue ref" << endl;
    //val.a = 10;
}

void func(A&& a) //右值引用
{
    cout << "Rvalue ref" << endl;
}

class Array {
public:
    Array(int size) : size_(size) {
        data_ = new int[size_];
    }
     
    // 深拷贝构造
    Array(const Array& temp_array) {
        cout << "Copy constructor" << endl;
        size_ = temp_array.size_;
        data_ = new int[size_];
        for (int i = 0; i < size_; i ++) {
            data_[i] = temp_array.data_[i];
        }
    }

    Array(Array&& temp_array) {
        data_ = temp_array.data_;
        size_ = temp_array.size_;
        // 为防止temp_array析构时delete data，提前置空其data_      
        temp_array.data_ = nullptr;
    }
     
    // 深拷贝赋值
    Array& operator=(const Array& temp_array) {
        delete[] data_;
 
        size_ = temp_array.size_;
        data_ = new int[size_];
        for (int i = 0; i < size_; i ++) {
            data_[i] = temp_array.data_[i];
        }
    }

    ~Array() {
        delete[] data_;
    }
 
public:
    int *data_;
    int size_;
};

int main()
{
    int a = 3; 
    int &b = a;

    const int &c = 3;
    vector<A> vec;
    A a1;
    vec.push_back(a1);
    vec.emplace_back(a1);

    int&& m = 10;
    cout << &m << endl;

    Array array(10);
    vector<Array*> vecArray;
    Array array3 = std::move(array);

    return 0;
}