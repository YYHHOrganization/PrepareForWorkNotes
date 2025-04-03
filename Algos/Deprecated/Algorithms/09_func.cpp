#include<iostream>
using namespace std;

int add(int a, int b){
    return a+b;
}

int substract(int a,int b){
    return a-b;
}

int main(){
    int(*oper)(int, int); //定义⼀个函数指针，指向⼀个接受两个int参数、返回int的函数
    oper = &add;
    cout<<oper(3,6)<<endl;  //9
    oper = &substract;
    cout<<oper(3,6)<<endl;  //-3
    cout<<(*oper)(3,6)<<endl; //这样也可以
    return 0;
}