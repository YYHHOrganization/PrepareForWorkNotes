# string 字符串 用法 小知识点



#### erase

错误❌写法：

```C++
stk.erase(stk.back()); //❌错误
```

因为

`stk.erase` 函数的参数应该是一个迭代器或索引，而不是字符本身。

应该改为`stk.pop_back();` 或 `stk.erase(stk.size() - 1)`

而

`stk.back()` 返回 `char` 类型





#### reverse(str.begin(),str.end());

返回void



#### substr

substr函数的形式为s.substr(pos, n)，

string a = s.substr(0,5);

https://blog.csdn.net/liuweiyuxiang/article/details/83687868