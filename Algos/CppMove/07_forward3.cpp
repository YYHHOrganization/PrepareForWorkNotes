#include <iostream>
#include <utility>

void process(int& x) {
    std::cout << "Left Value: " << x << std::endl;
}

void process(int&& x) {
    std::cout << "Right Value: " << x << std::endl;
}

template <typename T>
void wrapper(T&& arg) {
    // 使用 std::forward 将 arg 的值类别转发到 process
    process(std::forward<T>(arg));
}

int main() {
    int a = 10;
    wrapper(a);          // 调用左值版本
    wrapper(20);        // 调用右值版本
}