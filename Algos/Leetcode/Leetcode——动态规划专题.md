# Leetcode——动态规划专题

> 这篇文档会聚焦于“动态规划”本身，因此每道题目只会整理动态规划的版本，帮助复习的时候形成完整的体系。



# 一、入门dp

## 1.爬楼梯

### （1）[377. 组合总和 Ⅳ](https://leetcode.cn/problems/combination-sum-iv/)

> 给你一个由 **不同** 整数组成的数组 `nums` ，和一个目标整数 `target` 。请你从 `nums` 中找出并返回总和为 `target` 的元素组合的个数。
>
> 题目数据保证答案符合 32 位整数范围。

用`dp[target]`表示能组成总和为`target`的元素的个数，那么`dp[target]`即为最终所求。而`dp[target]`应该是所有`dp[target-nums[i]]`的累加和。同时`dp[0]`被设置成了1，因为如果`target`本身就在`nums`数组当中，那么其本身也是一种元素组合方案。

代码如下：

```c++
class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        vector<long long> dp(target+1);
        dp[0]=1;
        for(int i=1;i<=target;i++)
        {
            for(int j=0;j<nums.size();j++)
            {
                if(i-nums[j]>=0 && (dp[i]<=INT_MAX-dp[i-nums[j]])) //右边这个算是trick,防止中间结果爆掉.因为最后结果不会爆,所以中间结果爆了的话一定不会用到中间结果
                {
                    dp[i] += dp[i-nums[j]];
                }
            }
        }
        return dp[target];
    }
};
```



### （2）[2466. 统计构造好字符串的方案数](https://leetcode.cn/problems/count-ways-to-build-good-strings/)

这种统计方案数的dp题，如果中间的范围会非常大，可以提前取`MOD`，因为模运算可以线性相加，所以为了防止越界可以在中间就对dp数组进行取模运算。

```c++
class Solution {
public:
    int countGoodStrings(int low, int high, int zero, int one) {
        //依旧是两种情况加在一起,同时dp[0]=1;
        const int MOD = 1e9+7;
        vector<long long> dp(high+1);
        dp[0] = 1;
        long long cnt = 0;
        for(int i=0;i<=high;i++)
        {
            if(i-zero>=0) dp[i] = (dp[i] + (dp[i-zero])%MOD)%MOD;
            if(i-one>=0) dp[i] = (dp[i] + (dp[i-one])%MOD)%MOD;
            if(i>=low)
            {
                cnt = (cnt + dp[i]%MOD)%MOD;
            }
        }
        return cnt;
    }
};
```



### （3）[2266. 统计打字方案数](https://leetcode.cn/problems/count-number-of-texts/)

这道题是之前做的了，直接给出题解（跟前面题类似，相当于222可能是由前面+222，22+2，2+22得来的）：

```c++
class Solution {
public:
    const int MOD = 1e9+7;
    int countTexts(string pressedKeys) {
        //dp[i]表示截止到**长度为i的字符串的时候,总的方案数**
        int n = pressedKeys.size();
        vector<long long> dp(n+1, 0);
        //跟前面一样,dp[0]=1,这样有助于计算中间过程;
        dp[0]=1;
        for(int i=1;i<=n;i++)
        {
            dp[i] = dp[i-1]; //至少有dp[i-1]种可能性（在前面的基础上额外按了一次当前字符）
            //有可能是由dp[i-2]过渡而来,但要求1.i>=2  2.nums[i-1]和nums[i-2]相同 ,比如22的情况（这轮按了两次当前字符）
            if(i>=2 && pressedKeys[i-1]==pressedKeys[i-2]) dp[i]+=dp[i-2]%MOD;
            //有可能是由dp[i-3]过渡而来,但要求1.i>=3 2.nums[i-1],nums[i-2],nums[i-3]都得相同（这轮按了三次当前字符）
            if(i>=3 && pressedKeys[i-1]==pressedKeys[i-2] && pressedKeys[i-2]==pressedKeys[i-3]) dp[i]+=dp[i-3]%MOD;
            //对于按下7或者9的情况,还有可能是四个
            int digit = pressedKeys[i-1]-'0';
            if(digit==7 || digit==9)
            {
                if(i>=4)
                {
                    if(pressedKeys[i-1]==pressedKeys[i-2] && pressedKeys[i-2]==pressedKeys[i-3] && pressedKeys[i-3]==pressedKeys[i-4]) //这轮按了4次当前字符
                    dp[i] += dp[i-4]%MOD;
                }
            }
            dp[i]=dp[i]%MOD;
        }
        return dp[n];
    }
};
```



## 2.打家劫舍

### （1）[198. 打家劫舍](https://leetcode.cn/problems/house-robber/)

> 你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警**。
>
> 给定一个代表每个房屋存放金额的非负整数数组，计算你 **不触动警报装置的情况下** ，一夜之内能够偷窃到的最高金额。
>
>  
>
> **示例 1：**
>
> ```
> 输入：[1,2,3,1]
> 输出：4
> 解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
>      偷窃到的最高金额 = 1 + 3 = 4 。
> ```
>
> **示例 2：**
>
> ```
> 输入：[2,7,9,3,1]
> 输出：12
> 解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
>      偷窃到的最高金额 = 2 + 9 + 1 = 12 。
> ```
>
>  
>
> **提示：**
>
> - `1 <= nums.length <= 100`
> - `0 <= nums[i] <= 400`

每间房屋都可以选择“偷”或者“不偷”。如果偷，问题转换为了`i-2`的问题；如果不偷，问题转换为了`i-1`的问题。本题相当于从最后一个房子开始思考，因此有状态转移方程：

> f(i) = max(f(i-1), f(i-2)+nums[i]); -> f(i+2) = max(f(i+1), f(i)+nums[i]); 

这样，遍历还是从0~n-1，但是`dp`数组初始化长度为`n+2`，并且都初始化成0即可。代码如下：

```c++
class Solution {
public:
    int rob(vector<int>& nums) {
        //f(i+2) = max(f(i+1), f(i)+nums[i]); 
        int n = nums.size();
        vector<int> dp(n+2);
        for(int i=0;i<n;i++)
        {
            dp[i+2] = max(dp[i+1], dp[i]+nums[i]);
        }
        return dp[n+1];
    }
};
```

