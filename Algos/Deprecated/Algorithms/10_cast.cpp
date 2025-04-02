#include <iostream>
using namespace std;

// 定义父类
class Mihoyo {
public:
    // 虚函数
    virtual void print() {
        cout << "This is the Base class." << endl;
    }
};

// 定义子类
class Genshin : public Mihoyo {
public:
    // 重写虚函数
    void print() override {
        cout << "This is the Derived class." << endl;
    }
};

int main() {
    // 创建子类对象
    Genshin genshinImpact;

    // 使用父类指针指向子类对象
    Mihoyo* hoyo = &genshinImpact;

    // 调用 print 函数，实际调用的是子类的实现
    hoyo->print(); // 输出: This is the Derived class.

    //dynamic_cast 强制转换
    Mihoyo* basePtr = &genshinImpact; //父类指针指向子类对象
    Genshin* derivedPtr = dynamic_cast<Genshin*>(basePtr); //强制下行转换
    if (derivedPtr == nullptr) {
        cout << "basePtr cannot be down-casted to Derived* type" << endl;
    } else {
        cout << "basePtr has been down-casted to Derived* type" << endl;
    }

    // 创建父类对象
    //Mihoyo baseObj;

    // 使用子类指针指向父类对象是非法的
    // Derived* derivedPtr = &baseObj; // 这行代码会引发编译错误

    return 0;
}
