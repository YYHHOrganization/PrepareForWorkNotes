#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main(){
    vector<string> stringVec;
    string str = "Genshin";
    stringVec.push_back(str); //调用拷贝构造函数
    cout << "str: " << str << endl; //str: Genshin
    stringVec.push_back(std::move(str)); //调用移动构造函数
    cout << "str: " << str << endl; //str: 无内容，因为内容已经被移动了，str变成了空字符串

    string str2 = "Impact";
    stringVec.emplace_back(str2); //str2是左值，调用拷贝构造函数，怎么调用的呢？
    stringVec.emplace_back("Honkai");
    cout << "str2: " << str2 << endl; //str2: Impact
    stringVec.emplace_back(std::move(str2));
    cout << "str2: " << str2 << endl; //str2: 无内容，因为内容已经被移动了，str2变成了空字符串
    return 0;
}