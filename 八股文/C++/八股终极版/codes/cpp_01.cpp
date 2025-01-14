#include <iostream>

int main() {
    int a[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    
    // 声明一个指向数组的指针
    int (*p)[10] = &a;

    // 打印数组的首元素
    std::cout << "a[0]: " << a[0] << std::endl;           // 输出 0
    std::cout << "*p: " << (*p)[0] << std::endl;         // 输出 0

    // 地址计算
    std::cout << "Address of a: " << &a << std::endl;     // 输出数组a的地址
    std::cout << "Address of a + 1: " << (&a + 1) << std::endl; // 输出a尾元素后一个元素的地址

    // 指针转换
    int *intPtr = (int *)p;
    std::cout << "intPtr points to: " << *intPtr << std::endl; // 输出 0, 即 a[0]

    //p+1
    // 打印 p 和 p + 1 的值
    std::cout << "Address of p: " << p << std::endl;            // 输出数组a的地址
    std::cout << "Address of p + 1: " << (p + 1) << std::endl; // 输出a尾元素后一个元素的地址

    return 0;
}
