#include <iostream>
#include <string>

// 修饰全局变量
static int globalVar = 42; // 全局静态变量，只能在当前文件中访问

// 静态成员变量的声明
class MyClass {
public:
    static int staticMember; // 声明静态成员变量
    
    MyClass() {
        // 构造函数
    }
    
    // 静态成员函数
    static void staticFunction() {
        std::cout << "Static member function called. Static member value: " << staticMember << std::endl;
    }
};

// 初始化静态成员变量
int MyClass::staticMember = 0;

// 普通函数
void normalFunction() {
    // 修饰局部静态变量
    static int localStaticVar = 0; // 首次调用时初始化
    localStaticVar++;
    std::cout << "Local static variable value: " << localStaticVar << std::endl;
}

int main() {
    std::cout << "Global static variable: " << globalVar << std::endl;

    // 调用普通函数多次，观察局部静态变量的变化
    for (int i = 0; i < 5; ++i) {
        normalFunction();
    }

    // 使用类的静态成员
    MyClass obj1;
    MyClass::staticMember = 10; // 修改静态成员变量
    MyClass::staticFunction();  // 调用静态成员函数

    MyClass obj2; // 创建另一个对象
    MyClass::staticFunction();  // 再次调用静态成员函数，查看静态成员的值

    return 0;
}
