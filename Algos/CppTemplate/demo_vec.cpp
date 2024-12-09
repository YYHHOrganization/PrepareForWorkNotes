#include<iostream>
using namespace std;

template<typename T, int dim>
class vec
{
public:
    T* data = new T[dim];
    vec()
    {
        for (int i = 0; i < dim; i++)
        {
            data[i] = 0;
        }
    }
    vec(initializer_list<T> list)
    {
        int i = 0;
        for (auto &e : list)
        {
            data[i] = e;
            i++;
        }
    }

    // 拷贝构造函数
    vec(const vec &v)
    {
        for (int i = 0; i < dim; i++)
        {
            data[i] = v.data[i];
        }
    }

    // 移动构造函数
    vec(vec &&v)
    {
        data = v.data;
        v.data = nullptr;
    }

    //重载赋值，移动语义
    vec& operator=(vec &&v)
    {
        data = v.data;
        v.data = nullptr;
        return *this;
    }

    vec& operator=(const vec &v)
    {
        for (int i = 0; i < dim; i++)
        {
            data[i] = v.data[i];
        }
        return *this;
    }
    
    //重载+
    vec operator+(const vec &v)
    {
        vec res;
        for (int i = 0; i < dim; i++)
        {
            res.data[i] = data[i] + v.data[i];
        }
        return res;
    }

    void print()
    {
        if(data == nullptr)
        {
            cout<<"data is nullptr"<<endl;
            return;
        }
        for (int i = 0; i < dim; i++)
        {
            cout << data[i] << " ";
        }
        cout << endl;
    }

    vec cross(const vec &v)
    {
        cout << "cross" << endl;
        return vec();
    }
 
};

//特化vec2和vec3的cross函数
template<> vec<int, 2> vec<int, 2>::cross(const vec<int, 2> &v)
{
    cout << "cross2" << endl;
    return vec<int, 2>();
}

template<> vec<int, 3> vec<int, 3>::cross(const vec<int, 3> &v)
{
    cout << "cross3" << endl;
    return vec<int, 3>();
}

int main()
{
    vec<int, 3> v1{1, 2, 3};
    vec<float, 4> v2{1.0, 2.0, 3.0, 4.0};
    vec<int, 3> v3 = v1 + v1;
    vec<int, 3> v4{114514,114514,1919810};
    cout<<"深拷贝"<<endl;
    v3 = v4;
    v4.print();
    cout<<"浅拷贝"<<endl;
    v3 = std::move(v4);
    v4.print();

    v3.print();

    cout << "=============" <<endl;
    vec<int, 4> v5;
    vec<int, 4> v6;
    v5.cross(v6);
    return 0;
}