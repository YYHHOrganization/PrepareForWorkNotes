# Leetcode——字符串（KMP/Z函数/Manacher/字符串哈希/AC自动机/后缀数组/子序列自动机）





（非题单题）

### [8. 字符串转换整数 (atoi)](https://leetcode.cn/problems/string-to-integer-atoi/)

请你来实现一个 `myAtoi(string s)` 函数，使其能将字符串转换成一个 32 位有符号整数。

函数 `myAtoi(string s)` 的算法如下：

1. **空格：**读入字符串并丢弃无用的前导空格（`" "`）
2. **符号：**检查下一个字符（假设还未到字符末尾）为 `'-'` 还是 `'+'`。如果两者都不存在，则假定结果为正。
3. **转换：**通过跳过前置零来读取该整数，直到遇到非数字字符或到达字符串的结尾。如果没有读取数字，则结果为0。
4. **舍入：**如果整数数超过 32 位有符号整数范围 `[−231, 231 − 1]` ，需要截断这个整数，使其保持在这个范围内。具体来说，小于 `−231` 的整数应该被舍入为 `−231` ，大于 `231 − 1` 的整数应该被舍入为 `231 − 1` 。

返回整数作为最终结果。

**示例 1：**

**输入：**s = "42"

**输出：**42

**解释：**加粗的字符串为已经读入的字符，插入符号是当前读取的字符。

```
带下划线线的字符是所读的内容，插入符号是当前读入位置。
第 1 步："42"（当前没有读入字符，因为没有前导空格）
         ^
第 2 步："42"（当前没有读入字符，因为这里不存在 '-' 或者 '+'）
         ^
第 3 步："42"（读入 "42"）
```



M1:

**https://leetcode.cn/problems/string-to-integer-atoi/solutions/2361399/8-zi-fu-chuan-zhuan-huan-zheng-shu-atoiq-a2e8/**

<img src="assets/1600793383-jCgsGU-Picture1.png" alt="Picture1.png" style="zoom:50%;" />

<img src="assets/1600793383-JZRYip-Picture2.png" alt="Picture2.png" style="zoom:50%;" />

使用int

```C++
class Solution {
public:
    int myAtoi(string s) {
        int n=s.size();
        int sign = 1,bndry = INT_MAX/10;//214748364;
        int i=0;
        if(n==0)return 0;
        while(s[i]==' ')if(++i>n)return 0;
        if(s[i]=='-')sign = -1;
        if(s[i]=='-'||s[i]=='+')i++;
        int res=0;
        for(;i<n;i++)
        {
            if(s[i]<'0'||s[i]>'9') break;
            if(res>bndry||(res==bndry&&s[i]>'7')) //这个是字符！
            {
                return sign==1?INT_MAX:INT_MIN;
            }
            res=res*10+(s[i]-'0');//(s[i]-'0')一定要加括号 否则res*10+s[i]有溢出风险
        }
        return sign*res;
    }
};
```



M2:

Y: 较为冗长臃肿 而且使用了long（有的题目可能不让用）

```C++
class Solution {
public:
    int myAtoi(string s) {
        int n = s.size();
        int i=0;
        int b=1;
        bool flagBeginReadNum=false;
        long long res=0;
        for(int i=0;i<n;i++)
        {
            if(flagBeginReadNum)
            {
                if(s[i]>='0'&&s[i]<='9')
                {
                    res=res*10+(s[i]-'0');
                    // cout<<"res"<< res<<endl;
                    if(res*b>INT_MAX)
                    {
                        res=INT_MAX;
                        return res;
                    }
                    else if(res*b<INT_MIN)
                    {
                        res = INT_MIN;
                        return res;
                    }
                }
                else
                {
                    return b*res;
                }
            }
            else
            {
                if(s[i]==' ')continue;
                if( s[i]=='-')
                {
                    b=-1;
                    flagBeginReadNum=true; // -***+12 这算0
                }
                else if( s[i]=='+')
                {
                    flagBeginReadNum=true; // -***+12 这算0	
                }
                else if(s[i]>='0'&&s[i]<='9')
                {
                    // cout<<"in"<<s[i]<<endl;
                    flagBeginReadNum=true;
                    res=res*10+(s[i]-'0');
                }
                //其他情况 非法字符。
                else
                {
                    return b*res;
                }
            }
        }
        return res*b;
    }
};
```







# 其他



## 链表

### [61. 旋转链表](https://leetcode.cn/problems/rotate-list/)

给你一个链表的头节点 `head` ，旋转链表，将链表每个节点向右移动 `k` 个位置。

 

**示例 1：**

![img](assets/rotate1.jpg)

```
输入：head = [1,2,3,4,5], k = 2
输出：[4,5,1,2,3]
```



这题有很多方法可以做 也都能写出

M1：快慢指针

M2：闭合为环
思路及算法

记给定链表的长度为 n，注意到当向右移动的次数 k≥n 时，我们仅需要向右移动 kmodn 次即可。因为每 n 次移动都会让链表变为原状。这样我们可以知道，新链表的最后一个节点为原链表的第 (n−1)−(kmodn) 个节点（从 0 开始计数）。

这样，我们可以先将给定的链表连接成环，然后将指定位置断开。

具体代码中，我们首先计算出链表的长度 n，并找到该链表的末尾节点，将其与头节点相连。这样就得到了闭合为环的链表。然后我们找到新链表的最后一个节点（即原链表的第 (n−1)−(kmodn) 个节点），将当前闭合为环的链表断开，即可得到我们所需要的结果。

特别地，当链表长度不大于 1，或者 k 为 n 的倍数时，新链表将与原链表相同，我们无需进行任何处理。
链接：https://leetcode.cn/problems/rotate-list/solutions/681812/xuan-zhuan-lian-biao-by-leetcode-solutio-woq1/

```C++
class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        if(k==0||head==nullptr||head->next==nullptr)return head;
        ListNode* end = head;
        int n=1;
        while(end->next)
        {
            end = end->next;
            n++;
        }
        end->next = head;//1 2 3 4 5 1 2...
        k = n-k%n;//5-5%2 = 3// 
        ListNode* p = end;
        for(int i=0;i<k;i++)
        {
            p=p->next;
        }
        ListNode* res = p->next;
        p->next = nullptr;
        return res;
    }
};	
```



## 暂无分类



### [9. 回文数](https://leetcode.cn/problems/palindrome-number/)

给你一个整数 `x` ，如果 `x` 是一个回文整数，返回 `true` ；否则，返回 `false` 。

回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

- 例如，`121` 是回文，而 `123` 不是。

**示例 1：**

```
输入：x = 121
输出：true
```



M1 推荐 不用long

链接：https://leetcode.cn/problems/palindrome-number/solutions/

```C++
class Solution 
{
public:
    bool isPalindrome(int x) 
    {
        // 特殊情况：
        // 如上所述，当 x < 0 时，x 不是回文数。
        // 同样地，如果数字的最后一位是 0，为了使该数字为回文，
        // 则其第一位数字也应该是 0
        // 只有 0 满足这一属性
        if (x < 0 || (x % 10 == 0 && x != 0)) 
        {
            return false;
        }

        int revertedNumber = 0;
        while (x > revertedNumber) 
        {
            revertedNumber = revertedNumber * 10 + x % 10;
            x /= 10;
        }

        // 当数字长度为奇数时，我们可以通过 revertedNumber/10 去除处于中位的数字。
        // 例如，当输入为 12321 时，在 while 循环的末尾我们可以得到 x = 12，revertedNumber = 123，
        // 由于处于中位的数字不影响回文（它总是与自己相等），所以我们可以简单地将其去除。
        return x == revertedNumber || x == revertedNumber / 10;
    }
};
```



M2 Y 不用看 用了long

```C++
class Solution {
public:
    bool isPalindrome(int x) {
        if(x<0) return false;
        long long tx = x;
        long long rx=0;
        while(tx)
        {
            rx=rx*10+tx%10;
            tx=tx/10;
        }
        return x == rx;
    }
};
```

