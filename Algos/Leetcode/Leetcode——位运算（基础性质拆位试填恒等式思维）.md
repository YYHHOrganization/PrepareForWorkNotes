# Leetcode——位运算（基础/性质/拆位/试填/恒等式/思维）

### 注意点

#### 1、==括号== ！一定要加！！解决优先级错误问题



推荐先阅读：[从集合论到位运算，常见位运算技巧分类总结！](https://leetcode.cn/circle/discuss/CaOJ45/)

## 一、基础题

### [3370. 仅含置位位的最小整数](https://leetcode.cn/problems/smallest-number-with-all-set-bits/) 1199

给你一个正整数 `n`。

返回 **大于等于** `n` 且二进制表示仅包含 **置位** 位的 **最小** 整数 `x` 。

**置位** 位指的是二进制表示中值为 `1` 的位。

**示例 1：**

**输入：** n = 5

**输出：** 7

**解释：**

7 的二进制表示是 `"111"`。



#### 法1：  不推荐 O(n)

```C++
class Solution {
public:
    int smallestNumber(int n) 
    {
        //101
        //111

        //1010
        //1111
        //寻找>这个数字的二进制，-1就是了

        //取出n第一位是k位，这个1<<(k+1)-1;
        int k=0;
        while(n)
        {
            k++;
            n=n>>1;
        }
        return (1<<(k))-1;

    }
};
```

#### 法2： O(1)

![image-20250228175115378](assets/image-20250228175115378.png)

```C++
class Solution {
public:
    int smallestNumber(int n) 
    {
        return (1<<(bit_width((unsigned)n)))-1;
    }
};
```

或者__lg  

```C++
        return (1<<(__lg(n)+1))-1;
```

或者 log2  

```C++
return (1<<  ((int)log2(n)+1) )   -1;
```

>        //1010=10 。log2n = 3
>        //1111 .1<<(3+1)-1
>        //寻找>这个数字的二进制，-1就是了



deepseek关于这三个函数的说法：（未校准 不知道对不对）

>在 C++ 中，`log2`、`__lg()` 和 `bit_width` 的实现涉及不同层次的优化和硬件特性，以下是它们的典型实现方式：
>
>---
>
>### 1. **数学函数 `std::log2`**
>**作用**：计算浮点数的以 2 为底的对数。
>
>#### 实现方式：
>- **硬件指令**：现代 CPU 可能直接提供 `FYL2X`（x86）或类似指令计算对数，编译器会生成相关指令。
>- **软件近似**：若无硬件支持，数学库（如 glibc 或 Intel MKL）会使用多项式逼近或查表法：
>  1. 将浮点数 `x` 分解为指数 `e` 和尾数 `m`（IEEE 754 格式）：`x = 2^e * (1 + m)`。
>  2. 计算 `log2(x) = e + log2(1 + m)`，其中 `log2(1 + m)` 用多项式（如泰勒展开）近似。
>- **边界处理**：需处理负数、0、NaN 和无穷大，例如 `log2(0)` 返回 `-inf`。
>
>---
>
>### 2. **编译器内置函数 `__lg()`**
>**作用**：快速计算整数 `n` 的最高有效位位置（即 `floor(log2(n))`）。
>
>#### 实现方式：
>- **硬件指令**：
>  - x86 使用 `BSR`（Bit Scan Reverse）指令直接获取最高位位置。
>  - ARM 使用 `CLZ`（Count Leading Zeros）指令，结果转换为 `31 - CLZ(n)`。
>- **软件回退**（无指令支持时）：
>  ```cpp
>  int __lg(uint32_t n) {
>    if (n == 0) return -1; // 未定义行为通常要求 n > 0
>    int pos = 0;
>    while (n >>= 1) pos++;
>    return pos;
>  }
>  ```
>- **优化技巧**：二分查找或分块判断（如先判断高 16 位是否有 1）。
>
>---
>
>### 3. **C++20 标准函数 `std::bit_width`**
>**作用**：返回表示无符号整数所需的最小位数（例如 `0b10011` 需要 5 位）。
>
>#### 实现方式：
>- **直接关联**：对于非零数，`bit_width(n) = __lg(n) + 1`。
>- **零值处理**：若 `n = 0`，返回 0。
>- **编译器优化**：
>  ```cpp
>  int bit_width(uint32_t n) {
>    return (n == 0) ? 0 : (32 - __builtin_clz(n));
>  }
>  ```
>  其中 `__builtin_clz` 计算前导零数目（例如 `0b0010` 的 `CLZ` 为 30，`32-30=2`）。
>
>---
>
>### **关键差异与总结**
>| 函数        | 输入类型   | 目的                             | 底层依赖                 |
>| ----------- | ---------- | -------------------------------- | ------------------------ |
>| `std::log2` | 浮点数     | 精确计算以2为底的对数            | 硬件指令或数学库近似     |
>| `__lg()`    | 整数       | 快速获取最高位位置（log2下取整） | BSR/CLZ 指令或位操作循环 |
>| `bit_width` | 无符号整数 | 最小表示位数（log2上取整+1）     | `__lg()` 或 CLZ 指令变换 |
>
>实际实现因编译器和平台而异，例如：
>- GCC/Clang 的 `__lg(x)` 直接映射为 `31 - __builtin_clz(x)`。
>- MSVC 可能用 `_BitScanReverse` 实现类似逻辑。



### [3226. 使两个整数相等的位更改次数](https://leetcode.cn/problems/number-of-bit-changes-to-make-two-integers-equal/)

给你两个正整数 `n` 和 `k`。

你可以选择 `n` 的 **二进制表示** 中任意一个值为 1 的位，并将其改为 0。

返回使得 `n` 等于 `k` 所需要的更改次数。如果无法实现，返回 -1。

**示例 1：**

**输入：** n = 13, k = 4

**输出：** 2

**解释：**
最初，`n` 和 `k` 的二进制表示分别为 `n = (1101)2` 和 `k = (0100)2`，

我们可以改变 `n` 的第一位和第四位。结果整数为 `n = (*0*10*0*)2 = k`。



#### 解析

https://leetcode.cn/problems/number-of-bit-changes-to-make-two-integers-equal/solutions/2851739/o1-wei-yun-suan-zuo-fa-pythonjavacgo-by-3lg19/

1  首先需要求是否是**子集**

> 从集合的角度理解，每次操作相当于去掉集合 n 中的一个元素。
>
>要能把 n 变成 k，k 必须是 n 的**子集**。如果不是，返回 −1。

如何求子集:

https://leetcode.cn/circle/discuss/CaOJ45/

![image-20250301095558901](assets/image-20250301095558901.png)

>![image-20250301100630498](assets/image-20250301100630498.png)
>
>如果 *k* 去掉 *n* 中所有元素后，变成了空集，那么 *k* 就是 *n* 的子集。
>
>写成代码，如果 `(k & ~n) == 0`，那么 *k* 就是 *n* 的子集。



2  其次 求n⊕k 的二进制中的 1 的个数

>如果 k 是 n 的子集，答案为从 n 中去掉 k 后的集合大小，即 n⊕k 的二进制中的 1 的个数。(只有当k是0,n是1的保留了下来)
>
>注：也可以计算 n−k 的二进制中的 1 的个数。



#### 法1:

如果 *n* 和 *k* 的交集是 *k*，那么 *k* 就是 *n* 的子集。

交集就是位运算中的 AND（`&`）。![image-20250301100419727](assets/image-20250301100419727.png)

```C++
class Solution {
public:
    int minChanges(int n, int k) 
    {
        //1101 A
        //0100 B
        //0100 A&B
        //1001 A^B
        if((n&k)==k)//判断是子集
        {
            return __builtin_popcount(n^k);//异或后的1的个数
        }
        else
        {
            return -1;
        }
    }
};
```

或者直接写

```C++
return ((n&k)==k)?__builtin_popcount(n^k):-1;
```



#### 法2

如果 *n* 和 *k* 的并集是 *n*，那么 *k* 就是 *n* 的子集。

并集就是位运算中的 OR（`|`）。![image-20250301100506502](assets/image-20250301100506502.png)

```C++
class Solution {
public:
    int minChanges(int n, int k) {
        return ((n|k)==n)?__builtin_popcount(n^k):-1;
    }
};
```



#### 法3

如果 *k* 去掉 *n* 中所有元素后，变成了空集，那么 *k* 就是 *n* 的子集。

写成代码，如果 `(k & ~n) == 0`，那么 *k* 就是 *n* 的子集。

```C++
class Solution {
public:
    int minChanges(int n, int k) {
        return ((k&(~n))==0)?__builtin_popcount(n^k):-1;
    }
};
```

OR

```C++
return (k&(~n))?-1:__builtin_popcount(n^k);
```



#### 法 不用看： 不推荐 自己想的非最优的O(n)解法

```C++
class Solution {
public:
    int minChanges(int n, int k) 
    {
        if(n<k)return -1;
        
        int nt=n,kt=k;
        int res=0;
        while(nt)
        {
            if(!(nt&1))//括号！！因为不知道哪个更优先！&和!应该是一个优先级的）
            {
                if(kt&1)  return -1;//k有一位是1 而n是0  无法变化过去
            }
            else  //(nt末==1)
            {
                if(!(kt&1))res++;
            }
            nt=nt>>1;//赋值 不能只写nt>>1 这并不会真的移动它
            kt=kt>>1;
            // cout<<nt<<endl;
        }
        return res;
    }
};
```



### [1356. 根据数字二进制下 1 的数目排序](https://leetcode.cn/problems/sort-integers-by-the-number-of-1-bits/)

给你一个整数数组 `arr` 。请你将数组中的元素按照其二进制表示中数字 **1** 的数目升序排序。

如果存在多个数字二进制中 **1** 的数目相同，则必须将它们按照数值大小升序排列。

请你返回排序后的数组。

**示例 1：**

```
输入：arr = [0,1,2,3,4,5,6,7,8]
输出：[0,1,2,4,8,3,5,6,7]
解释：[0] 是唯一一个有 0 个 1 的数。
[1,2,4,8] 都有 1 个 1 。
[3,5,6] 有 2 个 1 。
[7] 有 3 个 1 。
按照 1 的个数排序得到的结果数组为 [0,1,2,4,8,3,5,6,7]
```

ME 100%
```C++
class Solution {
public:
    static bool cmp(int a , int b)  //static！
    {   
        int aBitCount = __builtin_popcount(a);
        int bBitCount = __builtin_popcount(b);
        if(aBitCount<bBitCount)return true;
        else if(aBitCount==bBitCount)
        {
            return a<b;
        }
        return false;
    }
    vector<int> sortByBits(vector<int>& arr) 
    {
        sort(arr.begin(),arr.end(),cmp);
        return arr;
    }
};
```

用lambda表达式

```C++
class Solution {
public:
    vector<int> sortByBits(vector<int>& arr) 
    {
        // sort(arr.begin(),arr.end(),cmp);
        sort(arr.begin(),arr.end(),
        [&](int a,int b) 
        {
            int aBitCount = __builtin_popcount(a);
            int bBitCount = __builtin_popcount(b);
            if(aBitCount<bBitCount)return true;
            else if(aBitCount==bBitCount)
            {
                return a<b;
            }
            return false;
        }
        );
        return arr;
    }
};
```

>lambda表达式
>
>`[捕获列表](参数列表) -> 返回类型 { 函数体 }`
>
>`[&]` 表示以引用方式捕获外部变量



### [461. 汉明距离](https://leetcode.cn/problems/hamming-distance/)

两个整数之间的 [汉明距离](https://baike.baidu.com/item/汉明距离) 指的是这两个数字对应二进制位不同的位置的数目。

给你两个整数 `x` 和 `y`，计算并返回它们之间的汉明距离。

**示例 1：**

```
输入：x = 1, y = 4
输出：2
解释：
1   (0 0 0 1)
4   (0 1 0 0)
       ↑   ↑
上面的箭头指出了对应二进制位不同的位置。
```

#### 法1：调用接口

```C++
class Solution {
public:
    int hammingDistance(int x, int y) 
    {
        return __builtin_popcount(x^y);
    }
};
```

#### 法2： 自己造轮子 实现数1的个数

```C++
class Solution {
public:
    int hammingDistance(int x, int y) 
    {
        //return __builtin_popcount(x^y);
        //自己造轮子
        int s=x^y;
        int res=0;
        while(s)
        {
            s=s&(s-1);
            res++;
        }
        return res;
    }
};
```



### [2220. 转换数字的最少位翻转次数](https://leetcode.cn/problems/minimum-bit-flips-to-convert-number/)

一次 **位翻转** 定义为将数字 `x` 二进制中的一个位进行 **翻转** 操作，即将 `0` 变成 `1` ，或者将 `1` 变成 `0` 。

- 比方说，`x = 7` ，二进制表示为 `111` ，我们可以选择任意一个位（包含没有显示的前导 0 ）并进行翻转。比方说我们可以翻转最右边一位得到 `110` ，或者翻转右边起第二位得到 `101` ，或者翻转右边起第五位（这一位是前导 0 ）得到 `10111` 等等。

给你两个整数 `start` 和 `goal` ，请你返回将 `start` 转变成 `goal` 的 **最少位翻转** 次数。

 

**示例 1：**

```
输入：start = 10, goal = 7
输出：3
解释：10 和 7 的二进制表示分别为 1010 和 0111 。我们可以通过 3 步将 10 转变成 7 ：
- 翻转右边起第一位得到：1010 -> 1011 。
- 翻转右边起第三位：1011 -> 1111 。
- 翻转右边起第四位：1111 -> 0111 。
我们无法在 3 步内将 10 转变成 7 。所以我们返回 3 。
```

同上题 EASY
```C++
class Solution {
public:
    int minBitFlips(int start, int goal) 
    {
        return __builtin_popcount(start^goal);
    }
};
```





###  [476. 数字的补数](https://leetcode.cn/problems/number-complement/)

对整数的二进制表示取反（`0` 变 `1` ，`1` 变 `0`）后，再转换为十进制表示，可以得到这个整数的补数。

- 例如，整数 `5` 的二进制表示是 `"101"` ，取反后得到 `"010"` ，再转回十进制表示得到补数 `2` 。

给你一个整数 `num` ，输出它的补数。

**示例 1：**

```
输入：num = 5
输出：2
解释：5 的二进制表示为 101（没有前导零位），其补数为 010。所以你需要输出 2 。
```



####  法1：O1

```C++
class Solution {
public:
    int findComplement(int num) {
        // int bitwid = bit_width((unsigned(num)));
        // int a= 1<<bitwid;
        // return a-num-1;
        int bitwid = bit_width((unsigned(num)));
        long long a= 1<<bitwid;//int的话2147483647这个不行
        return a-num-1;
    }
};

```

或者

```C++
class Solution {
public:
    int findComplement(int num) {
        return pow(2,((int)log2(num)+1))-num-1;
    }
};

链接：https://leetcode.cn/problems/number-complement/solutions/3062785/cyi-xing-dai-ma-by-heuristic-agnesi21v-t4pi/
```



#### 法2：On

```C++
class Solution {
public:
    int findComplement(int num) {
        int res=0;
        int count=0;
        while(num)
        {
            int add=0;
            if(!(num&1))add = 1<<count;
            res+=add;
            count++;
            
            num=num>>1;         // 1
        }
        return res;
    }
};
```

