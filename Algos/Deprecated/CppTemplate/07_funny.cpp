#include <iostream>
using namespace std;

template<typename T> class TypeToID{
public:
    static int const ID = -1;
};

template<> class TypeToID<float>{
public:
    static int const ID = 114514;
};

template<typename T> class TypeToID<T*>{  // 我要对所有的指针类型特化，所以这里就写T*
public:
    typedef T SameAsT;
    static const int ID = 0x000008;
};

void printID(){
    cout << "ID of float*: " << TypeToID<float*>::ID << endl;  //8
    cout << "ID of int*: " << TypeToID<int*>::ID << endl;  //8
    cout << "ID of float*: " << TypeToID<TypeToID<float*>::SameAsT>::ID << endl; //此时推导出的类型是float，因为匹配的float*对应T*
}

int main() {
    printID();
    return 0;
}