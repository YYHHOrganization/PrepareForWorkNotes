#include <iostream>
#include <vector>
#include <string>
#include <memory>
using namespace std;
//可以去cpp insights网站查看模板实例化的结果

template<typename T> class Blob
{
public:
    typedef T value_type;
    typedef typename vector<T>::size_type size_type;
    Blob();
    Blob(initializer_list<T> il);
    size_type size() const { return data->size(); }
    bool empty() const { return data->empty(); }
    void push_back(const T &t) { data->push_back(t); }
    void push_back(T &&t) { data->push_back(std::move(t)); }
    void pop_back();
    T& back();
    T& operator[](size_type i);
private:
    shared_ptr<vector<T>> data;
    void check(size_type i, const string &msg) const;
};

template<typename T>
Blob<T>::Blob(): data(make_shared<vector<T>>()) {}

template<typename T>
Blob<T>::Blob(initializer_list<T> il): data(make_shared<vector<T>>(il)) {}

template<typename T>
void Blob<T>::check(size_type i, const string &msg) const
{
    if(i >= data->size())
        throw out_of_range(msg);
}

template<typename T>
T& Blob<T>::back()
{
    check(0, "back on empty Blob");
    return data->back(); //vector的方法，返回最后一个元素
}

template<typename T>
T& Blob<T>::operator[](size_type i)
{
    check(i, "subscript out of range");
    return (*data)[i];
}

template<typename T>
void Blob<T>::pop_back()
{
    check(0, "pop_back on empty Blob");
    data->pop_back();
}

template<typename T> class BlobPtr
{
public:
    BlobPtr(): curr(0) {}
    BlobPtr(Blob<T> &a, size_t sz = 0): wptr(a.data), curr(sz) {}
    T& operator*() const
    {
        auto p = check(curr, "dereference past end");
        return (*p)[curr];
    }
    BlobPtr& operator++();
    BlobPtr& operator--();
    BlobPtr operator++(int); //后置递增
    BlobPtr operator--(int); //后置递减
private:
    shared_ptr<vector<T>> check(size_t i, const string &msg) const
    {
        auto ret = wptr.lock();
        if(!ret)
            throw runtime_error("unbound BlobPtr");
        if(i >= ret->size() || i < 0)
            throw out_of_range(msg);
        return ret;
    }
    weak_ptr<vector<T>> wptr; //指向Blob中的vector
    size_t curr; //数组中的当前位置
};

template<typename T>
BlobPtr<T>& BlobPtr<T>::operator++()  //前置++
{
    check(curr, "increment past end of BlobPtr");
    ++curr;
    return *this;
}

template<typename T>
BlobPtr<T>& BlobPtr<T>::operator--()  //前置--
{
    --curr;
    check(curr, "decrement past begin of BlobPtr");
    return *this;
}

template<typename T>
BlobPtr<T> BlobPtr<T>::operator++(int)  //后置++
{
    BlobPtr ret = *this;
    ++*this;
    return ret;
}

template<typename T>
BlobPtr<T> BlobPtr<T>::operator--(int)  //后置--
{
    BlobPtr ret = *this;
    --*this;
    return ret;
}

int main()
{
    Blob<int> ia;
    Blob<int> ia2 = {0, 1, 2, 3, 4, 5};
    cout << ia.size() << endl; //0
    cout << ia2.size() << endl; //6
    for(int i=0;i<ia2.size();i++)
    {
        cout << ia2[i] << " ";
    }
    Blob<string> sa = {"hi", "mom", "!"};
    return 0;
}