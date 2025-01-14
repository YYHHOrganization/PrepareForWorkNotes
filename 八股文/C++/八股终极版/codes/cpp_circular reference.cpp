#include <iostream>
#include <memory>
using namespace std;

class Son;

class Father {
public:
    shared_ptr<Son> son_;
    Father() {
        cout << __FUNCTION__ << endl;
    }
    ~Father() {
        cout << __FUNCTION__ << endl;
    }
};

class Son {
public:
    shared_ptr<Father> father_;
    Son() {
        cout << __FUNCTION__ << endl;
    }
    ~Son() {
        cout << __FUNCTION__ << endl;
    }
};

int main()
{
    auto son = make_shared<Son>();
    auto father = make_shared<Father>();
    son->father_ = father;
    father->son_ = son;
    cout << "son: " << son.use_count() << endl;
    cout << "father: " << father.use_count() << endl;
    return 0;
}