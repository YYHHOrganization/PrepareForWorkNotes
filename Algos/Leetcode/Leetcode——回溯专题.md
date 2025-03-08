# Leetcode——回溯专题

对应[分享丨【题单】链表、二叉树与回溯（前后指针/快慢指针/DFS/BFS/直径/LCA/一般树）- 讨论 - 力扣（LeetCode）](https://leetcode.cn/discuss/post/3142882/fen-xiang-gun-ti-dan-lian-biao-er-cha-sh-6srp/)这里的第四大专题：回溯。

# 一、入门回溯

## 1.[17. 电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)

```c++
class Solution {
public:
    string numbers[10] = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    string path;
    vector<string> res;
    void dfs(string digits, int i) //i表示哪个字母
    {
        int n = digits.size();
        if(i==n)
        {
            res.push_back(path);
            return;
        }
        for(char c: numbers[digits[i]-'0'])
        {
            path[i] = c;
            dfs(digits, i+1); //反正后面还会覆盖,不用pop_back(如果前面是push_back就要记得后面pop_back)
        }
    }
    vector<string> letterCombinations(string digits) {
        int n = digits.size();
        if(n==0) return res;
        path.resize(n);
        dfs(digits,0);
        return res;
    }
};
```

### 时间与空间复杂度的探讨：

- 时间复杂度：$O(n4^n)$，其中$4^n$来源于最多一个按下的数字对应4个字母，n则表示一共有n个按下的数字。而前面的n则是`res.push_back`的时间复杂度，所以总的是$O(n4^n)$
- 空间复杂度：$O(n)$

> 注：`dfs(i)`应当理解为枚举`>=i`的情况，因为除了枚举`i`以外，还要递归处理后面的部分。



# 二、子集型回溯

有「**选或不选**」和「**枚举选哪个**」两种写法。

也可以用**二进制枚举**做。

## 1.[78. 子集](https://leetcode.cn/problems/subsets/)

> 给你一个整数数组 `nums` ，数组中的元素 **互不相同** 。返回该数组所有可能的子集（幂集）。
>
> 解集 **不能** 包含重复的子集。你可以按 **任意顺序** 返回解集。
>
>  
>
> **示例 1：**
>
> ```
> 输入：nums = [1,2,3]
> 输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
> ```
>
> **示例 2：**
>
> ```
> 输入：nums = [0]
> 输出：[[],[0]]
> ```

### （1）从「**选或不选**」的角度

每个值既可以选，也可以不选，对应两波dfs：

- `dfs(nums, i+1);`表示不选，直接枚举下一个值的选择情况；
- 先push再`dfs(nums, i+1)`表示选，然后枚举下一个值得选择情况，在dfs之后要记得`pop_back()`，恢复现场。

```c++
class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void dfs(vector<int>& nums, int i) //每个数都可以选或者不选,当前枚举到了第i个
    {
        int n = nums.size();
        if(i==n) //枚举完了整个数组
        {
            res.push_back(path);
            return;
        }
        dfs(nums, i+1); //1.不选
        //2.选
        path.push_back(nums[i]);
        dfs(nums, i+1);
        path.pop_back();
    }
    vector<vector<int>> subsets(vector<int>& nums) {
        //1.选或者不选的角度来解题
        dfs(nums, 0);
        return res;
    }
};
```



### 时间与空间复杂度的探讨

- 每个数字都可以选或者不选，时间复杂度为$O(2^n)$。本身将path加入到最后的答案当中还有$O(n)$的复杂度，因此最终的时间复杂度为$O(n2^n)$。
- 空间复杂度：$O(n)$，返回值的空间忽略不计；



### （2）答案的视角（枚举选哪个）

这种角度思考本题，相当于每次进`dfs`函数时都一定会产生一个结果，需要我们自己判断为了产生答案需要让什么样的数进入dfs。此时答案如下：

```c++
class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void dfs(vector<int>& nums, int i)
    {
        int n = nums.size();
        res.push_back(path); //每次进来都会是一个答案
        for(int j=i;j<n;j++)
        {
            path.push_back(nums[j]);
            dfs(nums, j+1); //在下一轮回溯中，如果i==n，这个循环就不会进来了，所以不用额外判断
            path.pop_back();
        }
    }
    vector<vector<int>> subsets(vector<int>& nums) {
        dfs(nums, 0);
        return res;
    }
};
```

> 判断逻辑：每次放完一个数之后，只有大于其的数可以放到后面（防止重复），而每次进dfs函数所产生的解都是合法的。



## 2.[131. 分割回文串](https://leetcode.cn/problems/palindrome-partitioning/)

> 给你一个字符串 `s`，请你将 `s` 分割成一些 子串，使每个子串都是 **回文串** 。返回 `s` 所有可能的分割方案。
>
>  
>
> **示例 1：**
>
> ```
> 输入：s = "aab"
> 输出：[["a","a","b"],["aa","b"]]
> ```
>
> **示例 2：**
>
> ```
> 输入：s = "a"
> 输出：[["a"]]
> ```
>
>  
>
> **提示：**
>
> - `1 <= s.length <= 16`
> - `s` 仅由小写英文字母组成



### （1）答案的视角（枚举选哪个）

可以用“枚举选哪个”的思路来做，对后面的字符串进行切割判断是否为回文串。代码如下：

```c++
class Solution {
public:
    vector<vector<string>> res;
    vector<string> path;
    bool isValid(string& s)
    {
        int l = 0, r = (int)s.size()-1;
        while(l<=r)
        {
            if(s[l]!=s[r]) return false;
            l++, r--;
        }
        return true;
    }
    void dfs(string s, int idx) //从idx开始划分（可以理解为加分隔符），第一次传入的时候是dfs(s,0)
    {
        int n = s.size();
        if(n==idx)
        {
            res.push_back(path);
            return;
        }
        for(int i=idx;i<n;i++)
        {
            string t = s.substr(idx, i-idx+1);
            if(isValid(t))
            {
                path.push_back(t);
                dfs(s, i+1);
                path.pop_back();
            }
        }
    }
    vector<vector<string>> partition(string s) {
        dfs(s, 0);
        return res;
    }
};
```

> 对于这道题目来说，下标索引还是有写错的可能的，需要注意。



### （2）从「**选或不选**」的角度（精力有限先不看了）

> 对于本题来说，从「**选或不选**」的角度没有那么直观，因此更多还是掌握上面的那种算法。
>
> 比如对于字符串"aba" ，我们在处理的时候，想象着在字符之间有可以选择是否“插入”逗号的位置。当i指向第一个a时，“不选逗号”就是想象a和b之间没有逗号，尝试看"ab" 能不能组成回文子串；“选逗号”就是想象a后面有个逗号，把第一个a单独作为一个回文子串拿出来。
>
> 而对于最后一个字符，因为后面没有其他字符了，所以也就不存在“不选逗号，让它和后面字符组成更长子串”这种情况了，这就是  (i < n - 1) 起作用的地方。

假设每对相邻字符之间有个逗号，那么就看每个逗号是选还是不选。

也可以理解成：是否要把 `s[i] `当成分割出的子串的最后一个字符。注意` s[n−1]` 一定是最后一个字符，一定要选。

此时对应的代码如下：

```c++
class Solution {
public:
    vector<vector<string>> res;
    vector<string> path;
    bool isValid(string& s, int left, int right)
    {
        while(left<=right)
        {
            if(s[left]!=s[right]) return false;
            left++, right--;
        }
        return true;
    }
    void dfs(string s, int i, int start) //i为下一个“逗号”的位置，start为当前字符的起始位置
    {
        int n = s.size();
        if(i==n)
        {
            res.push_back(path);
            return;
        }
        //在当前位置不加逗号，和后面组成字符串（但最后一个没办法和后面组成字符串）
        if(i<n-1)
        {
            dfs(s, i+1, start);
        }
        if(isValid(s, start, i)) //可以构成回文串，继续往后访问
        {
            path.push_back(s.substr(start, i-start+1));
            dfs(s, i+1, i+1); //往后继续访问
            path.pop_back();
        }

    }
    vector<vector<string>> partition(string s) {
        dfs(s, 0, 0);
        return res;
    }
};
```



### （3）时间空间复杂度分析

- 时间复杂度：$O(n2^n)$，答案长度最多为逗号子集的个数（模拟我们用逗号来分割字符串），与上一道题目是类似的；
- 空间复杂度：$O(n)$



# 三、组合型回溯