#include <iostream>
using namespace std;

template<typename SrcT, typename DstT>
DstT c_style_cast(SrcT src){
    return (DstT)src;
}

template<typename DstT, typename SrcT>
DstT c_style_cast_right(SrcT src){
    return (DstT)src;
}

int main(){
    int v = 0;
    double d = c_style_cast<int, double>(v);  //这样是没问题的
    //double e = c_style_cast<double>(d);  //这样不行，dstT无法推导出来

    //只不过在部分推导、部分指定的情况下，编译器对模板参数的顺序是有限制的：先写需要指定的模板参数，再把能推导出来的模板参数放在后面。
    //针对本例子，dstT是需要指定的，而srcT是可以推导出来的
    double e = c_style_cast_right<double>(d);  //这样是没问题的,形象地说，DstT会先把你指定的参数吃掉，剩下的就交给编译器从函数参数列表中推导啦。
    cout << e << endl;
    return 0;
}