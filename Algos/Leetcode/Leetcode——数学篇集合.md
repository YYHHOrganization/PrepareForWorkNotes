# Leetcode——数学篇集合

# 一、取模运算基础

首先，先看一下这篇：[分享丨模运算的世界：当加减乘除遇上取模（模运算恒等式/费马小定理/组合数） - 力扣（LeetCode）](https://leetcode.cn/circle/discuss/mDfnkW/)

这里列举一下学习这篇文章的时候刷的题目和关键的知识点。



**前言**
某些题目，由于要计算的答案非常大（超出 64 位整数的范围），会要求把答案对 10 ^9 +7 取模。如果没有处理得当的话，**会 WA（错误）或者 TLE（超时）**。

例如计算一堆数字的乘积，如果没有及时取模，乘法会**溢出**（例如计算结果超出 C++ 中 long long 的最大值），从而得到**和预期不符的答案**（因此如果**WA（答案错误）**是有可能因为超出范围导致的）。对于 Python 来说，虽然没有溢出的问题，但大整数（big integer）之间的运算并不是 O(1) 的，可能会导致 TLE。



如何正确地取模呢？

## 1.基本取余运算

如果数非常大的时候，往往要对结果取余，对于加法和乘法，有如下规律：
$$
(a+b)\,\mathrm{mod}\, m=((a\,\mathrm{mod}\,m)+(b\,\mathrm{mod}\,m))\mathrm{mod}\,m \\(a\cdot b)\,\mathrm{mod}\,m=((a\,\mathrm{mod}\,m)\cdot(b\,\mathrm{mod}\,m))\mathrm{mod}\,m
$$


注意，如果涉及到幂运算，指数是不能随意取模的。如果指数在 64 位整数的范围内，可以用**快速幂**计算。如果指数超出 64 位整数的范围，可以使用**欧拉降幂公式**。以下进行总结。

> 同余定理：[同余 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/同餘)



### （1）快速幂计算

经典题目：[50. Pow(x, n) - 力扣（LeetCode）](https://leetcode.cn/problems/powx-n/)

> 下面题解中的Power函数即为快速幂的板子，需要记下来。
>
> <img src="assets/1728623430-RNGDEK-lc50-3-c-1745305380878-1.png" alt="lc50-3-c.png" style="zoom: 17%;" />

```c++
class Solution {
public:
    double Power(double x, long long n)
    {
        //快速幂
        double res = 1.0;
        while(n) // 从低到高枚举 n 的每个比特位
        {
            if(n&1) // 这个比特位是 1
            {
                res*=x;// 把 x 乘到 ans 中
            }
            x*=x;// x 自身平方
            n>>=1;// 继续枚举下一个比特位
        }
        return res;
    }
    double myPow(double x, int n) {
        if(x<=1e-6 && x>=-1e-6) return 0; //此时认为x=0  （这题也可以不需要这句话）
        long long p = n; //如果不是ll，n=-2147483648的时候 ，p=-p 会溢出
        if(p==0) return 1;
        if(p<0)
        {
            p = -p;
            x = 1.0 / x;
        }
        return Power(x, p);
    }
};
```



### （2）[372. 超级次方 - 力扣（LeetCode）](https://leetcode.cn/problems/super-pow/description/)

首先我们先利用快速幂的思想+代码再做一下这道题目：[372. 超级次方 - 力扣（LeetCode）](https://leetcode.cn/problems/super-pow/description/)，以下给出快速幂的做法代码：

<img src="assets/image-20250422154459127.png" alt="image-20250422154459127" style="zoom: 80%;" />

```c++
class Solution {
public:
    const int MOD = 1337;
    int Pow(int x, int n)
    {
        //在快速幂的时候求MOD
        long long res = 1.0;
        while(n)
        {
            if(n&1) res = (res%MOD) * (x%MOD)%MOD ;
            x = (x%MOD) * (x%MOD) %MOD;
            n>>=1;
        }
        return res;
    }
    int superPow(int a, vector<int>& b) {
        long long res = 1;
        for(int i = b.size()-1;i>=0;i--)
        {
            res = (res %MOD * Pow(a, b[i])%MOD)%MOD;
            a = Pow(a, 10);
        }
        return res;
    }
};
```

少加一些MOD:

```C++
class Solution {
public:
    const int MOD = 1337;
    int Power(int x,long long n)
    {
        int ans=1;
        while(n)
        {
            if(n&1)
            {
                ans =((long long)ans* x)%MOD;
            }
            x=((long long)x*x)%MOD;
            n>>=1;
        }
        return ans;
    }
    int superPow(int a, vector<int>& b) {
        // 10
        // a^(b1*1000 + b2*100 + b3*10 +b4)
        //a^(b1*1000) * a^(b2*100) * a^(b3*10) * a^(b4)
        //加上取模：a^(b1*1000)%MOD * a^(b2*100)%MOD * a^(b3*10)%MOD * a^(b4)%MOD
        //a^(b1*1000) = (a^1000)^b1
        int bn = b.size();
        int ans=1;
        for(int i=bn-1;i>=0;i--)
        {
            ans = (long long)ans * Power(a,b[i]) %MOD;
            a = Power(a,10);
        }
        return ans;
    }
};
```



**接下来我们来介绍欧拉降幂公式。**==这个有空再看吧，估计记不住==，给一个参考链接：

> [【力扣·每日一题】372. 超级次方(欧拉降幂 快速幂)_mb62cff40cc1a13的技术博客_51CTO博客](https://blog.51cto.com/u_15718710/5473326)



### （3）同余

首先引入同余（congruence modulo）的概念。

两个整数 x 和 y，如果 $(x-y)\,mod\,m==0$ ，则称 x 与 y 关于模 m 同余，记作  $x \equiv y \pmod{m}$  

>三条线强调“模意义下的等价关系” , 强调 \( x \) 和 \( y \) 在模 \( m \) 意义下属于同一等价类
>
>其实也就是 $x\,mod\,m==y\,mod\,m$

注意：(a%m - b%m != (a-b)%m) ! 反例：` m=3 a=6 b=2`

> 只有在a%m - b%m == (a-b)%m == 0的时候才是成立的，即为同余定理。



## 2.取余运算进阶

### （1）负数情况的处理

如果计算过程中有减法，可能会产生负数，取余运算时处理不当也会导致 WA。如何正确处理这种情况呢？

如果发现**加法取余的过程中可能会出现负数（$x\,mod\,m<0$），可以用下面的式子：**
$$
(x\,mod\,m + m)\,mod\,m
$$
这样无论$x$是否为负数，运算结果都会落在区间 `[0,m−1] `中。



m：在C++中，对负数取模我们推荐这么写：

```C++
// 调整 x 的余数为非负数，再与 y 的余数比较
((x % m + m) % m) == (y % m)
```



### （2）除法的处理

看这篇：[分享丨模运算的世界：当加减乘除遇上取模（模运算恒等式/费马小定理/组合数） - 力扣（LeetCode）](https://leetcode.cn/circle/discuss/mDfnkW/)中的除法取模部分，写的很好。



先说结论，如果$p$是一个质数，$a$是$b$的倍数且$b$和$p$互质$(b$不是$p$的倍数),那么有

$$
\large \frac ab\bmod p=(a\cdot b^{p-2})\bmod p
$$
上式中$a$和$b$可以是很大的数，例如$a=100!,b=50!50!$ 。

由于$10^9+7$是一个质数，所以上式可用于要求对$10^9+7$取模的题目。如果推导出了包含除法的式子，可以用上式转换成乘法，
并用快速幂计算 $b^{p-2}$ mod $p$。



## 3.总结

```c++
MOD = 1_000_000_007

// 加
(a + b) % MOD

// 减
((a - b)%MOD + MOD) % MOD  //这个应该会比较稳妥一些

// 把任意整数 a 取模到 [0,MOD-1] 中，无论 a 是正是负
(a % MOD + MOD) % MOD

// 乘（注意使用 64 位整数）long long
a * b % MOD

// 多个数相乘，要步步取模，防止溢出
a * b % MOD * c % MOD

// 除（MOD 是质数且 b 不是 MOD 的倍数）
a * qpow(b, MOD - 2, MOD) % MOD
```

其中qpow 为**快速幂**算法。



容易遇到的坑：

k是任何数字，i>0,以下有什么问题

```C++
(i-k+26)%26+26  
```

上面还是可能是负数或者超过26

其实应该是:

```C++
((i-k)%26+26)%26
```



## 补充：组合数板子

<img src="assets/image-20250422161618999.png" alt="image-20250422161618999" style="zoom: 67%;" />

看一下这道题目：[62. 不同路径 - 力扣（LeetCode）](https://leetcode.cn/problems/unique-paths/description/)。

题解：**https://leetcode.cn/problems/unique-paths/solutions/3062432/liang-chong-fang-fa-dong-tai-gui-hua-zu-o5k32/**

一种做法是使用dp，但这里我们关注组合数的方法。板子如下：

```c++
const int MOD = 1'000'000'007;
const int MX = 100'001; // 根据题目数据范围修改

long long F[MX]; // F[i] = i!
long long INV_F[MX]; // INV_F[i] = i!^-1

long long pow(long long x, int n) {
    long long res = 1;
    for (; n; n /= 2) {
        if (n % 2) {
            res = res * x % MOD;
        }
        x = x * x % MOD;
    }
    return res;
}

auto init = [] {
    F[0] = 1;
    for (int i = 1; i < MX; i++) {
        F[i] = F[i - 1] * i % MOD;
    }

    INV_F[MX - 1] = pow(F[MX - 1], MOD - 2); // ① 👇
    for (int i = MX - 1; i; i--) {
        INV_F[i - 1] = INV_F[i] * i % MOD; //②
    }
    return 0;
}();

// 从 n 个数中选 m 个数的方案数
long long comb(int n, int m) {
    return m < 0 || m > n ? 0 : F[n] * INV_F[m] % MOD * INV_F[n - m] % MOD;
}

class Solution {
public:
    int solve(vector<int>& nums) {
        // 预处理的逻辑写在 class 外面，这样只会初始化一次
    }
};
```

>①
>$$
>\large \frac 1{(m!)}\bmod p=(1\cdot {(m!)}^{p-2})\bmod p
>$$
>
>②
>$$
>\large \frac 1{(m-1)!} = \large \frac m{(m)!}
>$$



放到这道题里，我们不需要那么大的数值范围，可以简化为[C++组合数的计算(3种方法实现)_c++求组合数-CSDN博客](https://blog.csdn.net/m0_37149062/article/details/122522676)这个链接里面的做法（边乘边除，推导略）。此时这道题就可以秒杀了（感觉记一下这种求组合数的方法平时可能够用了）：

![image-20250422164238652](assets/image-20250422164238652.png)

```c++
class Solution {
public:
    typedef long long ll;
    ll C(int n,int m)
    {
      ll res=1;
      for(int i=1;i<=m;i++)
      {
        res = res * (n-m+i)/i;// 注意一定要先乘再除//res*((n-m+i)/i)❌：会出现浮点数，不可以加括号
      }  
      return res;
    }
    int uniquePaths(int m, int n) {
        //C(m+n-2, m-1);
        return C(m+n-2, m-1);
    }
};
```



## 补充题目

【1】[3379. 转换数组](https://leetcode.cn/problems/transformed-array/)：

【2】[2961. 双模幂运算](https://leetcode.cn/problems/double-modular-exponentiation/)

【3】[2550. 猴子碰撞的方法数](https://leetcode.cn/problems/count-collisions-of-monkeys-on-a-polygon/)

- 这题有个坑人情况，需要注意（注意可能会出现负数的情况）



### [3379. 转换数组](https://leetcode.cn/problems/transformed-array/)

>题目意思是： nums[i] =k 表示移动k，找到 nums[i+k]（循环）, 放入res数组

给你一个整数数组 `nums`，它表示一个循环数组。请你遵循以下规则创建一个大小 **相同** 的新数组 `result` ：

对于每个下标 `i`（其中 `0 <= i < nums.length`），独立执行以下操作：

- 如果 `nums[i] > 0`：从下标 `i` 开始，向 **右** 移动 `nums[i]` 步，在循环数组中落脚的下标对应的值赋给 `result[i]`。
- 如果 `nums[i] < 0`：从下标 `i` 开始，向 **左** 移动 `abs(nums[i])` 步，在循环数组中落脚的下标对应的值赋给 `result[i]`。
- 如果 `nums[i] == 0`：将 `nums[i]` 的值赋给 `result[i]`。

返回新数组 `result`。

**注意：**由于 `nums` 是循环数组，向右移动超过最后一个元素时将回到开头，向左移动超过第一个元素时将回到末尾。

**示例 1：**

**输入：** nums = [3,-2,1,1]

**输出：** [1,1,1,3]

**解释：**

- 对于 `nums[0]` 等于 3，向右移动 3 步到 `nums[3]`，因此 `result[0]` 为 1。
- 对于 `nums[1]` 等于 -2，向左移动 2 步到 `nums[3]`，因此 `result[1]` 为 1。
- 对于 `nums[2]` 等于 1，向右移动 1 步到 `nums[3]`，因此 `result[2]` 为 1。
- 对于 `nums[3]` 等于 1，向右移动 1 步到 `nums[0]`，因此 `result[3]` 为 3。

```C++
class Solution {
public:
    //  3 -2 1 1
    //  1  1 1 3
    vector<int> constructTransformedArray(vector<int>& nums) {
        int n = nums.size();
        vector<int> res(n,0);
        for(int i=0;i<n;i++)
        {
            res[i] = nums[((i+nums[i])%n+n)%n];
        }
        return res;
    }
};
```



# 二、数论

## 1.判断质数

[3115. 质数的最大距离 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-prime-difference/description/)

这是一道算是板子的题目，先来写一个基础的判断质数的函数：

```c++
bool isPrime(int n)
{
    for(int i=2;i<=sqrt(n);i++)
    {
        if(n%i==0) return false;
    }
    return n>=2;
}
```

接下来，使用素数筛来改善一下，以下是本题的核心代码：

![image-20250121213033029](Leetcode%E2%80%94%E2%80%94%E6%95%B0%E5%AD%A6%E7%AF%87%E9%9B%86%E5%90%88.assets/image-20250121213033029.png)

```c++
vector<int> primes;
void init()
{
    isPrime.resize(MAX+1,1);
    isPrime[0]=0;
    isPrime[1]=0;
    for(int i=2;i<=MAX;i++)
    {
        if(isPrime[i])
        {
            primes.push_back(i); //同时，这个逻辑还可以判断质数
            for(int j=i;j<=MAX/i;j++)  //这样做是为了防止溢出
                isPrime[i*j]=0; //相当于这些都不是质数
        }  
    }
}
```



相似题目：[2761. 和等于目标值的质数对 - 力扣（LeetCode）](https://leetcode.cn/problems/prime-pairs-with-target-sum/description/)，这题比较容易写错（写错了好几次。。。）。



## §1.6 最大公约数（GCD）

### [365. 水壶问题](https://leetcode.cn/problems/water-and-jug-problem/)

https://leetcode.cn/problems/water-and-jug-problem/description/

有两个水壶，容量分别为 `x` 和 `y` 升。水的供应是无限的。确定是否有可能使用这两个壶准确得到 `target` 升。

你可以：

- 装满任意一个水壶
- 清空任意一个水壶
- 将水从一个水壶倒入另一个水壶，直到接水壶已满，或倒水壶已空。

 

**示例 1:** 

```
输入: x = 3,y = 5,target = 4
输出: true
解释：
按照以下步骤操作，以达到总共 4 升水：
1. 装满 5 升的水壶(0, 5)。
2. 把 5 升的水壶倒进 3 升的水壶，留下 2 升(3, 2)。
3. 倒空 3 升的水壶(0, 2)。
4. 把 2 升水从 5 升的水壶转移到 3 升的水壶(2, 0)。
5. 再次加满 5 升的水壶(2, 5)。
6. 从 5 升的水壶向 3 升的水壶倒水直到 3 升的水壶倒满。5 升的水壶里留下了 4 升水(3, 4)。
7. 倒空 3 升的水壶。现在，5 升的水壶里正好有 4 升水(0, 4)。
参考：来自著名的 "Die Hard"
```



#### 方法1：DFS

```C++
using PII = pair<int,int>;
class Solution {
public:
    bool canMeasureWater(int x, int y, int target) {
        stack<PII> stk;
        stk.emplace(0,0);
        auto hashFunc = [](const PII& a)
        {
            return hash<int>()(a.first)^hash<int>()(a.second);
        };
        unordered_set<PII,decltype(hashFunc)> seen(0,hashFunc);
        while(!stk.empty())
        {
            if(seen.count(stk.top()))//如果已经重复回来了。
            {
                stk.pop();
                continue;
            }
            seen.emplace(stk.top());
            auto [remain_x,remain_y] = stk.top();
            stk.pop();
            if(remain_x==target||remain_y==target||remain_x+remain_y==target)return true;
            stk.emplace(x,remain_y); // 把 X 壶灌满。
            stk.emplace(remain_x,y); // 把 Y 壶灌满。
            stk.emplace(0,remain_y); // 把 X 壶倒空。
            stk.emplace(remain_x,0); // 把 Y 壶倒空。
            //x倒空：remain_x//y-remain_y 倒满y需要的  
            //  if remain_x小 x'=0 
            //  else          x' = remain_x - (y-remain_y); //y-remain_y y中还能放的水
            // 把 X 壶的水灌进 Y 壶，直至灌满或倒空。
            stk.emplace(remain_x-min(remain_x,y-remain_y),remain_y+min(remain_x,y-remain_y));
            // 把 Y 壶的水灌进 X 壶，直至灌满或倒空。
            stk.emplace(remain_x+min(remain_y,x-remain_x),remain_y-min(remain_y,x-remain_x));
        }
        return false;
    }
};
```



语法

>1. **Lambda 表达式定义哈希函数**：
>
>   ```cpp
>   auto hash_function = [](const PII& o) 
>   {
>       return hash<int>()(o.first) ^ hash<int>()(o.second);
>   };
>   ```
>
>   - `auto` 推导变量类型为 lambda 的闭包类型。
>   - Lambda 接受 `const PII&` 参数，计算其 `first` 和 `second` 的哈希值异或结果。
>   - `hash<int>()(o.first)` 调用标准库的 `hash<int>` 生成哈希值。
>
>2. **声明 `unordered_set` 并指定哈希类型**：
>
>   ```cpp
>   unordered_set<PII, decltype(hash_function)> seen(0, hash_function);
>   ```
>
>   - `decltype(hash_function)` 获取 lambda 的类型作为模板参数，确保 `unordered_set` 使用自定义哈希。
>     - **`decltype`的作用**：获取Lambda的类型，因为Lambda的类型是匿名且编译器生成的，无法直接写出
>   - 模板参数：`PII` 是元素类型，`decltype(hash_function)` 是哈希函数类型。
>
>3. **构造函数参数**：
>
>   - `0`：初始桶（bucket）数量。
>   - `hash_function`：传入自定义哈希函数对象。由于 lambda 闭包类型不可默认构造，必须显式传递实例。

解释

>### 1. **为什么需要自定义哈希函数？**
>
>- **标准库限制**：C++标准库未提供`std::pair<int, int>`的默认哈希函数，因此直接使用`unordered_set<PII>`会编译失败。
>- **手动提供哈希逻辑**：通过定义`hash_function`，明确告诉容器如何计算`PII`对象的哈希值，使其能正确存储和查找元素。
>
>### 2. **与C#的`Equals`和`GetHashCode`的关系**
>
>- 等价性：C++的unordered_set需要两个组件：哈希函数（类似GetHashCode）和相等比较（类似Equals）。
>  - **哈希函数**：必须显式提供（如代码中的`hash_function`）。
>  - **相等比较**：默认使用`operator==`，而`std::pair`已实现`==`，因此无需额外编写。
>- **C#对比**：在C#中，若将对象用作字典键，必须同时重写`Equals`和`GetHashCode`，确保逻辑一致。C++的机制类似，但语法和实现方式不同。



#### 方法二：数学

https://leetcode.cn/problems/water-and-jug-problem/solutions/161010/shui-hu-wen-ti-by-leetcode-solution/

1. **操作分析**：每次操作（装满或倒空）会导致总水量变化为 \(x\) 或 \(y\) 的整数倍。倒水操作不影响总水量，仅改变水的分布。
2. **贝祖（裴蜀）定理**：方程 \(ax + by = z\) 有解当且仅当 \(z\) 是 \(x\) 和 \(y\) 的最大公约数（gcd）的倍数。
3. **实际约束**：总水量 \(z\) 必须满足$ 0 \leq z \leq x + y$，因为无法获得超过两壶总容量的水或负水量。

解题步骤

1. **特殊情况处理**：
   - 若 \(z = 0\)，直接返回 `True`（无需操作）。
   - 若 \(x + y < z\)，返回 `False`（超出容量总和）。
   - 若 \(x\) 或 \(y\) 为0，则只有当 \(z\) 等于另一容器的容量或0时才可能。
2. **计算最大公约数**：使用欧几里得算法计算 \(x\) 和 \(y\) 的 gcd。
3. **判断条件**：检查 \(z\) 是否是 gcd 的倍数且满足容量约束。

```C++
class Solution {
public:
    bool canMeasureWater(int x, int y, int target) {
        if(target==0)return true;
        if(target>x+y)return false;
        if(x==0||y==0)return target==0||x+y==target;
        return target % gcd(x,y) ==0;
    }
};
```



如果想自己写gcd：

答: 是辗转相除法 用于求**最大公约数**

递归写法

```C++
int gcd(int a, int b){
    if (a%b == 0) {
        return b;
    }
    return gcd(b, a%b);
}
```

非递归写法：

```C++
int gcd(int a, int b){
    int temp = a;
    while(a%b != 0){
        a = b;
        b = temp%b;
        temp = a;
    }
    return b;
}
```

简单写法：

```C++
int gcd(int a, int b)
{
    return b == 0 ? a : gcd(b, a % b);
}
```



# 组合数学专题

可以参考这个视频系列来学习：[NOIP初赛讲解——组合数学_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1PE411y76n/?spm_id_from=333.337.search-card.all.click&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)

## 1.基础知识

### (1)加法原理与乘法原理

> 在组合数学中，**加法原理**和**乘法原理**是计算事件可能性的基础规则，具体解释如下：
>
> ---
>
> ### **1. 加法原理（互斥事件的“或”关系）**
> - **定义**：若完成某任务有若干**互斥**的方式（任选一种即可），则总方法数为各方式方法数之和。
> - **公式**：总方法数 = $A + B + C + \dots$
> - **例子**：  
>   - 从北京到上海，可以坐飞机（5个航班）或高铁（3个车次）。总共有 \(5 + 3 = 8\) 种选择。
>   - 书架上有4本数学书和6本小说，选一本书阅读的方法数是 \(4 + 6 = 10\) 种。
>
> ---
>
> ### **2. 乘法原理（独立步骤的“且”关系）**
> - **定义**：若完成某任务需要**多个独立步骤**（所有步骤依次完成），则总方法数为各步骤方法数的乘积。
> - **公式**：总方法数 = $A \times B \times C \times \dots$
> - **例子**：  
>   - 穿衣服时，有3件上衣和4条裤子，总搭配方式为 $3 \times 4 = 12$种。
>   - 从A城到B城有2条路，B城到C城有3条路，从A到C的路径数为$2 \times 3 = 6$ 种。
>
> ---
>
> ### **关键区别**
> - **加法原理**：事件之间**互斥**（只能选一种）。
> - **乘法原理**：步骤之间**独立**（需依次完成所有步骤）。
>
> ---
>
> ### **算法竞赛中的典型应用**
> - **加法原理**：分类讨论不同情况（如动态规划中的状态转移）。
> - **乘法原理**：排列组合问题（如路径计数、排列数计算）。
>
> **示例题**：  
> 从1~100中选一个数，要求是3的倍数 **或** 5的倍数，共有多少种选择？  
> - **加法原理**：3的倍数有33个，5的倍数有20个，但需扣除重复（15的倍数，共6个）。  
>   总数为 \(33 + 20 - 6 = 47\) 种（结合容斥原理）。
>
> ---
>
> 掌握这两个原理，能高效解决大部分组合计数问题！



### (2)排列数与组合数

![image-20250327221816916](assets/image-20250327221816916.png)

![image-20250327221829602](assets/image-20250327221829602.png)

> 其中组合数的公式其实是可以从排列数当中推导而来，只不过在其基础上再除了一个m!.



### (3)常用的恒等式

#### （a）恒等式1

组合数有一个基本的递推式(**很重要，算是杨辉三角的基础。**)：
$$
C(n, m) = C(n-1,m) + C(n-1,m-1)
$$

> 组合数学中，组合数 $C(n, m) = C(n-1, m) + C(n-1, m-1)$ 的证明及与杨辉三角的关系可形象解释如下：
>
> ------
>
> ### **1. 形象证明：是否包含某个特定元素**
>
> 假设从 $n$ 个元素中选 $m$ 个，我们可以固定其中一个元素（例如第一个元素），将所有情况分为两类：
>
> - **包含该元素**：需从剩下的 $n-1$ 个元素中再选 $m-1$ 个，对应 $C(n-1, m-1)$。
> - **不包含该元素**：需从剩下的 $n-1$ 个元素中选全部 $m$ 个，对应 $C(n-1, m)$。
>
> **总方法数** = 包含该元素的方法数 + 不包含该元素的方法数，即：
>
> $C(n, m) = C(n-1, m) + C(n-1, m-1) $
>
> #### **示例验证**
>
> 当 $n=5, m=3$ 时：
>
> $C(5,3) = C(4,3) + C(4,2) = 4 + 6 = 10 $
>
> 直接计算 $C(5,3) = \frac{5!}{3!2!} = 10$，结果一致。
>
> ------
>
> ### **2. 与杨辉三角的关系**
>
> 杨辉三角的构造规则是：**每个数等于它上方左右两数之和**。
>
> - 第 $n$ 行第 $m$ 列的数值对应组合数 $C(n, m)$。
> - 递推公式 $C(n, m) = C(n-1, m) + C(n-1, m-1)$ 正是杨辉三角的生成规则。
>
> #### **示例：杨辉三角前5行**
>
> ```
> 1         (n=0)
> 1 1       (n=1)
> 1 2 1     (n=2)
> 1 3 3 1   (n=3)
> 1 4 6 4 1 (n=4)
> ```
>
> - 例如，第4行（$n=4$）的数值对应：
>   $C(4,0)=1, \, C(4,1)=4, \, C(4,2)=6, \, C(4,3)=4, \, C(4,4)=1$。
>
> ------
>
> ### **3. 数学归纳法补充证明**
>
> - **基础情况**：当 $n=1$，$C(1,0)=1$，$C(1,1)=1$，满足递推关系。
>
> - **归纳假设**：假设对 $n=k$ 成立，即 $C(k, m) = C(k-1, m) + C(k-1, m-1)$。
>
> - 归纳步骤：对 n=k+1n=k+1n=k+1，根据定义：
>
>   $C(k+1, m) = \frac{(k+1)!}{m!(k+1-m)!} = \frac{k!}{m!(k-m)!} \cdot \frac{k+1}{k+1-m} + \frac{k!}{(m-1)!(k+1-m)!} $
>
>   化简后仍满足递推关系。
>
> ------
>
> ### **总结**
>
> - **核心思想**：分类讨论是否包含特定元素，穷尽所有可能性。
>- **杨辉三角**：组合数的递推关系直接对应其生成规则，两者本质一致。
> 
>该原理是动态规划、二项式定理等算法的理论基础，也是组合数学的核心公式之一。



#### （b）恒等式2

$$
C(n,0)+C(n,1)+C(n,2)+...+C(n,n) = 2^n
$$

证明思路比较重要：“两边算”。左右两边都可以看作是从n个数里面做任意多的选择：

- 左侧：选0个数，选1个数，选2个数。。。。选n个数的总的方案数
- 右侧：每个数都可以选，或者不选，总的方案数

这样的话，等号成立就很好理解了。



### 例题

- 6人站成一排，求：

  - 1. 甲不在排头，乙不在排尾的排列数；

    > 优先考虑特殊位置。比较好的做法是画方块法。分为乙在排头和乙不在排头两种情况：
    >
    > - 乙在排头：5!
    > - 乙不在排头：`4（乙的位置）X 4(甲的位置) X 4！（剩下的人）`
    >
    > 加一起即可。也可以用容斥原理来做：6！-5！-5！+4！（总的方案数-甲在排头-乙在排尾+甲在排头且乙在排尾）

  - 2. 甲不在排头，乙不在排尾，并且甲乙不相邻的排列数；

    > 分类讨论：
    >
    > - 甲在排尾，乙在排头：4！
    > - 甲在排尾，乙不在排头：3X4！
    > - 甲不在排尾，乙在排头：3X4!（对称的）
    > - 甲不在排尾，乙不在排头：4（甲的选择）X 乙的选择——（甲在2：2X4！ + 甲在3：4! +甲在4：4！+甲在5：2X4！）

也就是说，分情况讨论的情况使用加法原理。



## 2.捆绑与插空法

