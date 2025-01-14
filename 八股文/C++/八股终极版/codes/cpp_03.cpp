#include <iostream>
#include <cstring> // 包含 strcpy、sprintf 和 memcpy 函数

// 使用 strcpy 复制字符串
void useStrcpy() {
    const char* source = "Hello, World!";
    char destination[50]; // 确保目标数组足够大以容纳源字符串

    strcpy(destination, source); // 复制字符串
    std::cout << "Using strcpy: Copied String: " << destination << std::endl;
}

// 使用 sprintf 格式化字符串并输出
void useSprintf() {
    char buffer[100];
    int value = 42;

    sprintf(buffer, "The answer is %d", value); // 格式化字符串并保存到 buffer
    std::cout << "Using sprintf: Formatted String: " << buffer << std::endl;
}

// 使用 memcpy 复制内存内容
void useMemcpy() {
    const char source[] = "Goodbye, World!";
    char destination[50];

    memcpy(destination, source, strlen(source) + 1); // 复制字节，包括空字符
    std::cout << "Using memcpy: Copied Memory: " << destination << std::endl;
}

int main() {
    std::cout << "Demonstrating strcpy, sprintf, and memcpy:" << std::endl;

    useStrcpy();   // 展示 strcpy 的用法
    useSprintf();  // 展示 sprintf 的用法
    useMemcpy();   // 展示 memcpy 的用法

    return 0;
}
