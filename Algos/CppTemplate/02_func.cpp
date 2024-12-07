#include <iostream>
using namespace std;

template<typename T> T Add(T a, T b) {
    return a+b;
}

int main(){
    int a = 3, b = 6;
    cout << Add<int>(a, b) << endl; //9
}