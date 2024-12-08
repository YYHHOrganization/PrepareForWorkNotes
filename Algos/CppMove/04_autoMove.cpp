#include <iostream>
#include <vector>
#include <utility>

class MyClass {
public:
    std::vector<int> data;

    // 没有定义任何拷贝构造函数或拷贝赋值运算符

    // 编译器将生成移动构造函数和移动赋值运算符
};

int main() {
    MyClass obj1;
    obj1.data.push_back(1);

    // 使用移动构造
    MyClass obj2 = std::move(obj1); // 调用移动构造函数

    // 使用移动赋值
    MyClass obj3;
    obj3 = std::move(obj2); // 调用移动赋值运算符

    std::cout << "obj1.data.size() = " << obj1.data.size() << std::endl; // 0
    std::cout << "obj2.data.size() = " << obj2.data.size() << std::endl; // 0
    std::cout << "obj3.data.size() = " << obj3.data.size() << std::endl; // 1

    // 可以简单看看unique_ptr的实现，它就是通过移动语义来实现资源的转移的
    std::unique_ptr<MyClass> ptr1 = std::make_unique<MyClass>();
    //std::unique_ptr<MyClass> ptr2 = ptr1;
    std::unique_ptr<MyClass> ptr2 = std::move(ptr1);

    return 0;
}