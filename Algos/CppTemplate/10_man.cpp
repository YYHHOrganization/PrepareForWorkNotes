#include <iostream>
using namespace std;

struct X {
    typedef float type;
};

struct Y {
    typedef float type2;
};

template <typename T, typename U>
void foo(T t, typename U::type u) {
    // ...
}

template <typename T, typename U>
void foo(T t, typename U::type2 u) {
  // ...
} 
void callFoo() {
    foo<int, X>(5, 5.0); // T == int, typename U::type == X::type == float
    foo<int, Y>( 1, 1.0 ); // ???
}

int main(){
    callFoo();
    return 0;
}