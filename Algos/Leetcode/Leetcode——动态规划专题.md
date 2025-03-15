# Leetcode——动态规划专题

> 这篇文档会聚焦于“动态规划”本身，因此每道题目只会整理动态规划的版本，帮助复习的时候形成完整的体系。为方便理解，部分题目在一轮做的时候不会考虑太多空间优化的问题，除非dp达到了三维再考虑或者是题目很好找到如何优化。`一轮做题的重点在于，把dp写好，空间的压缩与优化可以放到后面来解决。`



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



#　四、经典线性 DP

## 1.最长公共子序列（LCS）

一般定义 `f[i][j] `表示对 (`s[:i],t[:j]`) 的求解结果。



### (1)[1143. 最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/)

> 给定两个字符串 `text1` 和 `text2`，返回这两个字符串的最长 **公共子序列** 的长度。如果不存在 **公共子序列** ，返回 `0` 。
>
> 一个字符串的 **子序列** 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。
>
> - 例如，`"ace"` 是 `"abcde"` 的子序列，但 `"aec"` 不是 `"abcde"` 的子序列。
>
> 两个字符串的 **公共子序列** 是这两个字符串所共同拥有的子序列。
>
>  
>
> **示例 1：**
>
> ```
> 输入：text1 = "abcde", text2 = "ace" 
> 输出：3  
> 解释：最长公共子序列是 "ace" ，它的长度为 3 。
> ```
>
> **示例 2：**
>
> ```
> 输入：text1 = "abc", text2 = "abc"
> 输出：3
> 解释：最长公共子序列是 "abc" ，它的长度为 3 。
> ```
>
> **示例 3：**
>
> ```
> 输入：text1 = "abc", text2 = "def"
> 输出：0
> 解释：两个字符串没有公共子序列，返回 0 。
> ```
>
>  
>
> **提示：**
>
> - `1 <= text1.length, text2.length <= 1000`
> - `text1` 和 `text2` 仅由小写英文字符组成。

这道题目推荐看Leetcode的官方题解：[1143. 最长公共子序列 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-common-subsequence/solutions/696763/zui-chang-gong-gong-zi-xu-lie-by-leetcod-y7u0/)。

用下面一张图来辅助理解：

<img src="assets/1617411822-KhEKGw-image.png" alt="image.png" style="zoom:67%;" />

本题可以在推导状态转移方程的时候认为`dp[i][j]`是s的截止到索引为`i`的字符串和t的截止到索引为`j`的字符串的最长公共子序列的长度。此时有：

```c++
dp[i][j] = dp[i-1][j-1] + 1 if s[i]==t[j];
		 = max(dp[i-1][j], dp[i][j-1]) if s[i]!=t[j];
边界条件：dp[-1][x]，dp[x][-1]的结果都为0，意味着不构成最长公共子序列（最长公共子序列长度为0）。此时返回的结果为dp[m-1][n-1]。
```

> 思考：为什么在状态转移方程的时候，不需要都考虑`max(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`的情况呢？
>
> 在最长公共子序列问题中，状态转移方程的正确性可以通过以下分析严格证明：
>
> ---
>
> ### **关键证明思路**
> **当 `s[i] ≠ t[j]` 时，`dp[i-1][j-1] ≤ max(dp[i-1][j], dp[i][j-1])`**，因此无需显式考虑 `dp[i-1][j-1]`。
>
> ---
>
> ### **证明步骤**
>
> 1. **状态定义**  
>    `dp[i][j]` 表示字符串 `s` 的前 `i` 个字符和 `t` 的前 `j` 个字符的最长公共子序列（LCS）长度。
>
> 2. **单调性**  
>    根据定义，状态转移满足以下单调性：  
>    - `dp[i][j] ≥ dp[i-1][j]`（新增 `s[i]` 后，LCS 不会变短）。  
>    - `dp[i][j] ≥ dp[i][j-1]`（新增 `t[j]` 后，LCS 不会变短）。  
>
>    因此，对任意 `i, j` 有：  
>    ```  
>    dp[i][j] ≥ dp[i-1][j]  
>    dp[i][j] ≥ dp[i][j-1]  
>    ```
>
> 3. **推导 `dp[i-1][j-1]` 的上界**  
>    由单调性可知：  
>    ```  
>    dp[i-1][j] ≥ dp[i-1][j-1]  
>    dp[i][j-1] ≥ dp[i-1][j-1]  
>    ```
>    因此：  
>    ```  
>    max(dp[i-1][j], dp[i][j-1]) ≥ dp[i-1][j-1]  
>    ```
>    **当 `s[i] ≠ t[j]` 时，`dp[i][j]` 只需取 `max(dp[i-1][j], dp[i][j-1])`，因为 `dp[i-1][j-1]` 已被覆盖。**
>
> ---
>
> ### **反证法验证**
> **假设存在 `dp[i-1][j-1] > max(dp[i-1][j], dp[i][j-1])`：**  
> 根据单调性：  
> - `dp[i-1][j] ≥ dp[i-1][j-1]` → 矛盾。  
> - `dp[i][j-1] ≥ dp[i-1][j-1]` → 矛盾。  
>
> 因此，假设不成立，说明 `dp[i-1][j-1]` 不可能超过 `max(dp[i-1][j], dp[i][j-1])`。
>
> ---
>
> ### **实例验证**
> 以 `s = "abcde"`, `t = "ace"` 为例：
>
> |      | a    | c    | e     |
> | ---- | ---- | ---- | ----- |
> | a    | 1    | 1    | 1     |
> | b    | 1    | 1    | 1     |
> | c    | 1    | 2    | 2     |
> | d    | 1    | 2    | 2     |
> | e    | 1    | 2    | **3** |
>
> 当计算 `dp[3][2]`（即 `s[3] = 'd'`, `t[2] = 'c'`）时：  
> - `s[3] ≠ t[2]`，故 `dp[3][2] = max(dp[2][2]=2, dp[3][1}=1) = 2`。  
> - 若强行考虑 `dp[2][1}=1`，结果仍为 `2`，未影响正确性。
>
> ---
>
> ### **结论**
> 在 `s[i] ≠ t[j]` 时，`max(dp[i-1][j], dp[i][j-1])` **隐含了 `dp[i-1][j-1]` 的上界**，因此无需显式比较 `dp[i-1][j-1]`。原状态转移方程已完备。

另一侧的证明如下：

> 在最长公共子序列（LCS）问题中，当 `s[i] == t[j]` 时，状态转移方程只需取 `dp[i-1][j-1] + 1`，而无需比较 `dp[i-1][j]` 或 `dp[i][j-1]`。以下是严格的证明：
>
> ---
>
> ### **关键结论**
> **当 `s[i] == t[j]` 时，`dp[i][j] = dp[i-1][j-1] + 1` 已隐含了 `dp[i][j] ≥ max(dp[i-1][j], dp[i][j-1])`，因此无需额外比较。**
>
> ---
>
> ### **反证**
>
> 假设存在 `dp[i][j] < max(dp[i-1][j], dp[i][j-1])`，则会导致矛盾：
> - 若 `max(dp[i-1][j], dp[i][j-1]) = dp[i-1][j]`，则 `dp[i][j] < dp[i-1][j]`，违反单调性 `dp[i][j] ≥ dp[i-1][j]`。
> - 同理，若 `max(dp[i-1][j], dp[i][j-1]) = dp[i][j-1]`，则违反 `dp[i][j] ≥ dp[i][j-1]`。
>
> ---
>
> ### **实例分析**
> 以 `s = "abcde"` 和 `t = "ace"` 为例：
> - 当计算 `dp[3][3]`（即 `s[3] = 'd'` 和 `t[3] = 'e'`）时：
>   - `s[3] != t[3]`，故 `dp[3][3] = max(dp[2][3], dp[3][2])`。
> - 当计算 `dp[5][3]`（即 `s[5] = 'e'` 和 `t[3] = 'e'`）时：
>   - `s[5] == t[3]`，故 `dp[5][3] = dp[4][2] + 1 = 2 + 1 = 3`。
>   - 此时 `dp[4][3] = 2` 和 `dp[5][2] = 2`，显然 `3 ≥ max(2, 2)`，验证了结论。
>
> ---
>
> ### **总结**
> 当 `s[i] == t[j]` 时，**当前字符必须属于 LCS**，因此只需在 `dp[i-1][j-1]` 的基础上加 1。由于动态规划的单调性保证了 `dp[i-1][j-1] + 1` 必然大于等于 `dp[i-1][j]` 和 `dp[i][j-1]`，因此无需额外比较。



同样，我们在写代码的时候为了防止越界，给`dp`的两个维度各加1。最终代码如下：

```c++
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int m = text1.size();
        int n = text2.size();
        vector<vector<int>> dp(m+1, vector<int>(n+1));
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                if(text1[i]==text2[j])
                {
                    dp[i+1][j+1] = dp[i][j] + 1;
                }
                else
                {
                    dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j]);
                }
            }
        }
        return dp[m][n];
    }
};
```



### （2）[583. 两个字符串的删除操作](https://leetcode.cn/problems/delete-operation-for-two-strings/)

> 给定两个单词 `word1` 和 `word2` ，返回使得 `word1` 和 `word2` **相同**所需的**最小步数**。
>
> **每步** 可以删除任意一个字符串中的一个字符。
>
>  
>
> **示例 1：**
>
> ```
> 输入: word1 = "sea", word2 = "eat"
> 输出: 2
> 解释: 第一步将 "sea" 变为 "ea" ，第二步将 "eat "变为 "ea"
> ```
>
> **示例  2:**
>
> ```
> 输入：word1 = "leetcode", word2 = "etco"
> 输出：4
> ```
>
>  
>
> **提示：**
>
> - `1 <= word1.length, word2.length <= 500`
> - `word1` 和 `word2` 只包含小写英文字母

与前面那道题目类似，`dp[i][j]`表示截止到word1的索引`i`和word2的索引`j`，转换为相同的最小步数，先不考虑边界条件，此时的状态转移方程为：

```c++
dp[i][j] = dp[i-1][j-1] if word1[i]==word2[j]
    	 = min(dp[i-1][j], dp[i][j-1]) + 1 if word1[i]!=word2[j] //dp[i-1][j]相当于删除word1的一个字符，而dp[i][j-1]则相当于给word1加一个和word2[j]一样的字符，然后再统一消除掉
```

考虑边界条件，`dp[-1][j]`的结果应该为j+1（对应移位后`dp[0][j+1]=j+1`），同理`dp[i][-1]`的结果应该为`i+1`(对应移位后`dp[i+1][0]=i+1`)。（思考一下对应不合法的情况），在代码实现上需要把dp数组的每个维度的size+1，这跟之前的题目是保持一致的。最终代码如下：

```c++
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size();
        int n = word2.size();
        vector<vector<int>> dp(m+1, vector<int>(n+1));
        for(int i=1;i<=m;i++) //初始化边界条件,下同
        {
            dp[i][0] = i;
        }
        for(int j=1;j<=n;j++)
        {
            dp[0][j] = j;
        }
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                if(word1[i]==word2[j])
                {
                    dp[i+1][j+1] = dp[i][j];
                }
                else
                {
                    dp[i+1][j+1] = min(dp[i][j+1], dp[i+1][j]) + 1;
                }
            }
        }
        return dp[m][n];
    }
};
```

如果这道题目要考虑空间优化，压缩为一维的dp，则需要做如下的考虑：

- 我们把第一维去掉的话，每遍历一行要首先给0索引位置赋值，与前面的对齐；
- dp的更新逻辑基于左上角，左侧和上方。左侧和上方问题不大，但左上角需要额外的变量来进行记录。我们可以维护一个pre值来记录更新前的左上角值，==尝试了一下，不太会写空间优化，不过问题不大，重点是理解二维的思路，没有卡空间复杂度不一定需要优化这个。==



### （3）[712. 两个字符串的最小ASCII删除和](https://leetcode.cn/problems/minimum-ascii-delete-sum-for-two-strings/)

> 给定两个字符串`s1` 和 `s2`，返回 *使两个字符串相等所需删除字符的 **ASCII** 值的最小和* 。

代码如下：

```c++
class Solution {
public:
    int minimumDeleteSum(string s1, string s2) {
        //跟前面的题类似
        //dp[i][j] = dp[i-1][j-1] if s1[i]==s2[j]
        //dp[i][j] = min(dp[i-1][j]+s1[i], dp[i][j-1]+s2[j]);
        //边界条件:dp[-1][j]等于前缀和,同理dp[i][-1]也相当于前缀和
        int m = s1.size();
        int n = s2.size();
        vector<vector<int>> dp(m+1, vector<int>(n+1));
        for(int i=1;i<=m;i++)
        {
            dp[i][0] = dp[i-1][0] + s1[i-1];
        }
        for(int j=1;j<=n;j++)
        {
            dp[0][j] = dp[0][j-1] + s2[j-1];
        }
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                if(s1[i]==s2[j])
                {
                    dp[i+1][j+1] = dp[i][j]; //相等的时候，什么都不用删，如果非得删掉字符的话肯定比不删的结果要大，而题目要最小的，因此不用考虑删除的情况
                }
                else
                {
                    dp[i+1][j+1] = min(dp[i][j+1]+s1[i], dp[i+1][j]+s2[j]); //此时考虑左上角的点就相当于两个都删掉一个字符，类似于前面的题目，得到的结果一定不会小于只删除一个字符的结果，因此不用考虑进来了
                }
            }
        }
        return dp[m][n];
    }
};
```



### （4）[72. 编辑距离](https://leetcode.cn/problems/edit-distance/)

> 给你两个单词 `word1` 和 `word2`， *请返回将 `word1` 转换成 `word2` 所使用的最少操作数* 。
>
> 你可以对一个单词进行如下三种操作：
>
> - 插入一个字符
> - 删除一个字符
> - 替换一个字符
>
>  
>
> **示例 1：**
>
> ```
> 输入：word1 = "horse", word2 = "ros"
> 输出：3
> 解释：
> horse -> rorse (将 'h' 替换为 'r')
> rorse -> rose (删除 'r')
> rose -> ros (删除 'e')
> ```
>
> **示例 2：**
>
> ```
> 输入：word1 = "intention", word2 = "execution"
> 输出：5
> 解释：
> intention -> inention (删除 't')
> inention -> enention (将 'i' 替换为 'e')
> enention -> exention (将 'n' 替换为 'x')
> exention -> exection (将 'n' 替换为 'c')
> exection -> execution (插入 'u')
> ```
>
>  
>
> **提示：**
>
> - `0 <= word1.length, word2.length <= 500`
> - `word1` 和 `word2` 由小写英文字母组成

本题也是类似，代码如下：

```c++
class Solution {
public:
    int minDistance(string word1, string word2) {
        //word1转为word2,可以修改,删除word1一个字符,或者插入一个字符(相当于word2删除一个字符)
        //dp[i][j] = dp[i-1][j-1] if word1[i]==word2[j]
        //dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1 //dp[i-1][j-1]相当于修改成字符一样的(多了编辑,可以从编辑转换得到,要加这个逻辑判断)
        //dp[-1][j] = j+1=>(dp[0][j+1]=j+1), dp[i][-1] = i+1->(dp[i+1][0]=i+1)
        //其实想不太好可以排除什么情况的话可以都写上,应该也能过
        int m = word1.size();
        int n = word2.size();
        vector<vector<int>> dp(m+1, vector<int>(n+1));
        for(int i=1;i<=m;i++) dp[i][0] = i;
        for(int j=1;j<=n;j++) dp[0][j] = j;
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                if(word1[i]==word2[j]) dp[i+1][j+1] = dp[i][j];
                else
                {
                    dp[i+1][j+1] = min({dp[i][j+1], dp[i+1][j], dp[i][j]}) + 1;
                }
            }
        }
        return dp[m][n];
    }
};
```

借助本题，提及一下这种题目的空间优化写法。首先，本题可以使用滚动数组来做，但此时就需要注意`dp[i][0]`的赋值问题，每一行在遍历的时候赋值`dp[i%m][0]=i`即可。使用滚动数组之后的代码如下（滚动数组的方法基本上是一比一翻译，需要注意//（1）这个地方）：

```c++
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size();
        int n = word2.size();
        vector<vector<int>> dp(2, vector<int>(n+1));
        for(int j=1;j<=n;j++) dp[0][j] = j;
        for(int i=0;i<m;i++)
        {
            dp[(i+1)%2][0] = i+1; //注意这里，使用dp推导出来的式子：dp[i][-1] = i+1->(dp[i+1][0]=i+1)，这里的i是从0开始的，跟这里的循环从0开始能对上
            for(int j=0;j<n;j++)
            {
                if(word1[i]==word2[j]) dp[(i+1)%2][j+1] = dp[i%2][j];
                else
                {
                    dp[(i+1)%2][j+1] = min({dp[i%2][j+1], dp[(i+1)%2][j], dp[i%2][j]}) + 1;
                }
            }
        }
        return dp[m%2][n];
    }
};
```

进一步地，思考能否用一维的数组来解决本题？可以看到外层for循环一开始就会覆盖掉`dp[i+1][0]`的值，而使用一维的话会导致后面的`dp[i%2][j]`的结果被错误的更新，因此需要每次进外层的for循环就保存当前的`dp[i%2][j]`的值，即保存`pre = dp[j]`（一维的情况）。降维之后的代码如下：

```c++
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size();
        int n = word2.size();
        vector<int> dp(n+1);
        for(int j=1;j<=n;j++) dp[j] = j;
        for(int i=0;i<m;i++)
        {
            int pre = dp[0];
            //dp[(i+1)%2][0] = i+1;
            dp[0] = i+1;
            for(int j=0;j<n;j++)
            {
                int tmp = dp[j+1]; //保存上一行下次要改的值,不然会被覆盖掉
                if(word1[i]==word2[j]) //dp[(i+1)%2][j+1] = dp[i%2][j];
                    dp[j+1] = pre;
                else
                {
                    //dp[(i+1)%2][j+1] = min({dp[i%2][j+1], dp[(i+1)%2][j], dp[i%2][j]}) + 1;
                    dp[j+1] = min({dp[j+1], dp[j], pre})+1;
                }
                pre = tmp;
            }
        }
        return dp[n];
    }
};
```

> 个人理解，掌握滚动数组的方法应该是够了，基本上不可能被卡空间，而优化为一维并不简单，可能改坏掉，因此最多用滚动数组优化即可。
