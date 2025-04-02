# 字符串与字符数组 C++——C风格&string

https://blog.csdn.net/ksws0292756/article/details/79432329



## 第一关：初识C语言字符串

请问以下输出是？：

```C++
int main()
{
	char  a[] = { 'g', 'e', 'n' };
	int b[] = { 1,2,3 };
	cout << sizeof(a) << endl;//打印结果：
	cout << a << endl;//打印结果：
	cout << b << endl;//打印结果：

	char  a2[] = { 'g', 'e', 'n','\0'};
	cout << sizeof(a2) << endl;//打印结果：
	cout << a2 << endl;//打印结果：

	char  a3[] = { "gen"};
	cout << sizeof(a3) << endl;//打印结果：
	cout << a3 << endl;//打印结果：

	char  a4[] = "gen";

	cout << &a <<" "<<&a2 <<" "<<&a3<< " " << &a4<<endl;//地址一样吗

	return 0;
}
```



答案：

```c++
int main()
{
	char  a[] = { 'g', 'e', 'n' };
	int b[] = { 1,2,3 };
	cout << sizeof(a) << endl;//打印结果：3
	cout << a << endl;//打印结果：gen烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫?
	cout << b << endl;//打印结果：地址0000007D8F4FF548

	char  a2[] = { 'g', 'e', 'n','\0'};
	cout << sizeof(a2) << endl;//打印结果：4
	cout << a2 << endl;//打印结果：gen

	char  a3[] = { "gen"};//等于char  a3[] = "gen";
	cout << sizeof(a3) << endl;//打印结果：4
	cout << a3 << endl;//打印结果：gen

	char  a4[] = "gen";

	cout << &a <<" "<<&a2 <<" "<<&a3<< " " << &a4<<endl;//地址都不一样！

	return 0;
}
```



## 第二关：了解C语言字符串

理解对char*数组的sizeof和cout操作：

```c++
char greeting[] = "Hello\0";
cout << sizeof(greeting) << endl; //输出：7
cout << greeting << endl; //输出： Hello

char beautifulCpp[] = "Hello\0H";
cout << sizeof(beautifulCpp) << endl; //输出：8
cout << beautifulCpp << endl; //输出： Hello

char beautifulCpp2[] = "Hello";
beautifulCpp2[3] = 0;
cout << sizeof(beautifulCpp2) << endl; //输出：6
cout << beautifulCpp2 << endl; //输出： Hel
```



以下：

```c++
char s1[] = "march7th";
char s2[] = "dan";
strcpy(s1, s2); //这个操作前后s1的地址不变
cout << s1 << endl;//dan 应该是因为\0也复制了
cout << sizeof(s1) << endl;//9
cout << s1 + 1 << endl;//an
cout << s1[5] << endl; //7
s1[3] = 's';
cout << s1 << endl; //dansh7th
cout << *s1 << endl; //d
// 	cout << **s1 << endl; //error
s1[8] = 's';
s1[9] = 't';
s1[10] = '\0';
cout<<s1<<endl;//dansh7thst,C++默认不做越界检查
```







## 【2】以下程序的输出结果为（）

```c++
#include<iostream>
#include<string>
using namespace std;
void print(const char** str) {
    ++str;
    cout << *str << endl;
}
int main() {
    static const char* arr[] = { "hello", "world", "c++" };
    const char** ptr = arr;
    print(ptr);
    return 0;
}
```

- [ ] hello
- [ ] world
- [ ] 字符w的起始地址
- [ ] 字符e

> 提示：
>
> 可以把 `*ptr`当作一个整体，指向一个char* 的字符串，然后注意下面这些情况：
>
> ```
> *ptr = arr[0] = "hello"
> (*ptr)[1] = arr[0][1] = 'e'
> (*ptr + 1) = arr[0][1:] = "ello"
> *(ptr + 1) = arr[1] = "world"
> ```

<details>   <summary>点我查看答案</summary>   选择B </details>







3、

const char* 

char  a[] = “string”

char b[] = {"string"}

char  a[] = {'s', 't', 'r'}

A ab 内存分配地址相同

B b在栈上 / 堆上？

> 出题：
>
> - (1)`char  a[] = {'s', 't', 'r'}`,cout它会有问题么？



最后一个字符是\0吗 

a大小？

