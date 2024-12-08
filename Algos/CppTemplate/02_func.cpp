#include <iostream>
using namespace std;

template<typename T> T Add(T a, T b) {
    return a+b;
}

template<typename T> T GetValue(int a){
    return static_cast<T>(a);
}

int main(){
    int a = 3, b = 6;
    cout << Add<int>(a, b) << endl; //9
    cout << Add(5.01, 7.01)<<endl;  //12.02,此时编译器会自动推导出模板参数类型
    
    //float c = GetValue(a); //错误，无法根据返回值自动推导出模板参数类型
    float c = GetValue<float>(a); //正确
    cout << c << endl; //3.0

    return 0;

}