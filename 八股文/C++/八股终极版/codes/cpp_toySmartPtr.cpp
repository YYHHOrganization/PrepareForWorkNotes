#include <iostream>
#include <memory>
using namespace std;

template<typename T>
class SharedPtr {
public:
    int* counter;
    int* weakref;
    T* resource;

    SharedPtr(T* resc = nullptr) {
        cout << __PRETTY_FUNCTION__ << endl;
        counter = new int(1);
        weakref = new int(0);
        resource = resc;
    }

    SharedPtr(const SharedPtr& rhs) {
        cout << __PRETTY_FUNCTION__ << endl;
        resource = rhs.resource;
        counter = rhs.counter;
        ++*counter;
    }

    SharedPtr& operator=(const SharedPtr& rhs) {
        cout << __PRETTY_FUNCTION__ << endl;
        --*counter;
        if (*counter == 0) {
            delete counter;
            delete resource;
        }

        resource = rhs.resource;
        counter = rhs.counter;
        ++*counter;
    }

    ~SharedPtr() {
        cout << __PRETTY_FUNCTION__ << endl;
        --*counter;
        if (*counter == 0) {
            delete counter;
            delete resource;
        }
    }

    int use_count() {
        return *counter;
    }
};

template<typename T>
class WeakPtr {
public:
    T* resource;

    WeakPtr(T* resc = nullptr) {
        cout << __PRETTY_FUNCTION__ << endl;
        resource = resc;
    }

    WeakPtr& operator=(SharedPtr<T>& ptr) {
        cout << __PRETTY_FUNCTION__ << endl;
        resource = ptr.resource;
        ++*ptr.weakref;  // 赋值时引用计数counter不变，改变弱引用计数weakref
    }

    ~WeakPtr() {
        cout << __PRETTY_FUNCTION__ << endl;
    }
};

class Son;

class Father {
public:
    SharedPtr<Son> son_;
    Father() {
        cout << __PRETTY_FUNCTION__ << endl;
    }
    ~Father() {
        cout << __PRETTY_FUNCTION__ << endl;
    }
};

class Son {
public:
    WeakPtr<Father> father_;  // 将SharedPtr改为WeakPtr
    Son() {
        cout << __PRETTY_FUNCTION__ << endl;
    }
    ~Son() {
        cout << __PRETTY_FUNCTION__ << endl;
    }
};

int main()
{
    auto son_ = new Son();  // 创建一个Son对象，返回指向Son对象的指针son_
    auto father_ = new Father();  // 创建一个Father对象，返回指向Father对象的指针father_
    SharedPtr<Son> son(son_);  // 调用SharedPtr构造函数：son.counter=1, son.weakref=0
    SharedPtr<Father> father(father_);  // 调用SharedPtr构造函数：father.counter=1, father.weakref=0
    son.resource->father_ = father;  // 调用WeakPtr赋值函数：father.counter=1, father.weakref=1
    father.resource->son_ = son;  // 调用SharedPtr赋值函数：son.counter=2, son.weakref=0
    cout << "son: " << son.use_count() << endl;
    cout << "father: " << father.use_count() << endl;
    return 0;
}