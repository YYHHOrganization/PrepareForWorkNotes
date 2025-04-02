#include <iostream>

using namespace std;

class Base {
public:
    // 非虚析构函数
    virtual ~Base() {
        cout << "Base destructor called." << endl;
    }
};

class Derived : public Base {
public:
    ~Derived() {
        cout << "Derived destructor called." << endl;
    }
};

int main() {
    Base* basePtr = new Derived(); // 创建派生类对象并用基类指针指向它
    delete basePtr; // 使用基类指针删除对象
    return 0;
}
