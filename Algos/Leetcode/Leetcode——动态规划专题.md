# Leetcode——动态规划专题

> 这篇文档会聚焦于“动态规划”本身，因此每道题目只会整理动态规划的版本，帮助复习的时候形成完整的体系。为方便理解，部分题目在一轮做的时候不会考虑太多空间优化的问题，除非dp达到了三维再考虑或者是题目很好找到如何优化。`一轮做题的重点在于，把dp写好，空间的压缩与优化可以放到后面来解决。`

DP题单:[分享丨【题单】动态规划（入门/背包/状态机/划分/区间/状压/数位/树形/数据结构优化）- 讨论 - 力扣（LeetCode）](https://leetcode.cn/discuss/post/3581838/fen-xiang-gun-ti-dan-dong-tai-gui-hua-ru-007o/)

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

给你整数 `zero` ，`one` ，`low` 和 `high` ，我们从空字符串开始构造一个字符串，每一步执行下面操作中的一种：

- 将 `'0'` 在字符串末尾添加 `zero` 次。
- 将 `'1'` 在字符串末尾添加 `one` 次。

以上操作可以执行任意次。

如果通过以上过程得到一个 **长度** 在 `low` 和 `high` 之间（包含上下边界）的字符串，那么这个字符串我们称为 **好** 字符串。

请你返回满足以上要求的 **不同** 好字符串数目。由于答案可能很大，请将结果对 `109 + 7` **取余** 后返回。

**示例 1：**

```C++
输入：low = 3, high = 3, zero = 1, one = 1
输出：8
解释：
一个可能的好字符串是 "011" 。
可以这样构造得到："" -> "0" -> "01" -> "011" 。
从 "000" 到 "111" 之间所有的二进制字符串都是好字符串。
```



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

Alice 在给 Bob 用手机打字。数字到字母的 **对应** 如下图所示。

<img src="assets/1722224025-gsUAIv-image.png" alt="img" style="zoom: 25%;" />

为了 **打出** 一个字母，Alice 需要 **按** 对应字母 `i` 次，`i` 是该字母在这个按键上所处的位置。

- 比方说，为了按出字母 `'s'` ，Alice 需要按 `'7'` 四次。类似的， Alice 需要按 `'5'` 两次得到字母 `'k'` 。
- 注意，数字 `'0'` 和 `'1'` 不映射到任何字母，所以 Alice **不** 使用它们。

但是，由于传输的错误，Bob 没有收到 Alice 打字的字母信息，反而收到了 **按键的字符串信息** 。

- 比方说，Alice 发出的信息为 `"bob"` ，Bob 将收到字符串 `"2266622"` 。

给你一个字符串 `pressedKeys` ，表示 Bob 收到的字符串，请你返回 Alice **总共可能发出多少种文字信息** 。

由于答案可能很大，将它对 `109 + 7` **取余** 后返回。

**示例 1：**

```C++
输入：pressedKeys = "22233"
输出：8
解释：
Alice 可能发出的文字信息包括：
"aaadd", "abdd", "badd", "cdd", "aaae", "abe", "bae" 和 "ce" 。
由于总共有 8 种可能的信息，所以我们返回 8 。
```



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



### （2）[740. 删除并获得点数](https://leetcode.cn/problems/delete-and-earn/)

> 给你一个整数数组 `nums` ，你可以对它进行一些操作。
>
> 每次操作中，选择任意一个 `nums[i]` ，删除它并获得 `nums[i]` 的点数。之后，你必须删除 **所有** 等于 `nums[i] - 1` 和 `nums[i] + 1` 的元素。
>
> 开始你拥有 `0` 个点数。返回你能通过这些操作获得的最大点数。

依旧是打家劫舍的类型题，“选”或者“不选”当前的值，这题有一种构造想法确实是很巧妙。参考[740. 删除并获得点数 - 力扣（LeetCode）](https://leetcode.cn/problems/delete-and-earn/solutions/3061028/zhi-yu-da-jia-jie-she-pythonjavaccgojsru-e5gg/)，可以转化为纯打家劫舍题目。代码如下：
```c++
class Solution {
public:
    int deleteAndEarn(vector<int>& nums) {
        //比如示例2:[2,2,3,3,3,4],删除3之后,所有的2和所有的4都会被删掉,意味着可以构造vec数组,其第i位vec[i]保存nums中=i的数的和,于是对vec数组进行打家劫舍即可得到最后的结果 [0,0,4,9,4]
        int mx = ranges::max(nums);
        vector<int> vec(mx+1, 0);
        for(int num:nums)
        {
            vec[num] += num;
        }
        int n = vec.size();
        //开始打家劫舍 dp[i]表示截止到第i个元素的最大点数 dp[i] = max(dp[i-1], dp[i-2]+vec[i])
        //打家劫舍还可以优化到常数复杂度，但感觉暂时没什么太大必要，代码清晰易读为当前的重点
        vector<int> dp(n+2, 0);
        for(int i=0;i<n;i++)
        {
            dp[i+2] = max(dp[i+1], dp[i]+vec[i]);
        }
        return dp[n+1];
    }
};
```



### ==（3）[2320. 统计放置房子的方式数](https://leetcode.cn/problems/count-number-of-ways-to-place-houses/)==

> 大概重温了一下当时的做法，有时间再重新做一下。



### （4）[213. 打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/)

与前面的打家劫舍相比，本题的所有房屋呈现环形分布，意味着最后一间房间连着第一间房间。

简单的做法是直接分类讨论：偷最后一间（此时第一间就不能偷了，从第二间开始算，相当于打家劫舍的子问题），或者不偷最后一间（此时第一间可以偷）。代码如下：

```c++
class Solution {
public:
    int robRange(vector<int>& nums, int left, int right) //偷的范围考虑
    {
        //left到right范围内做打家劫舍,返回右边界,此时用几个滚动变量会容易一些
        //dp[i] = max(dp[i-1], dp[i-2]+nums[i]);
        int f0 = 0, f1 = 0, f=0; //对应dp[i-2],dp[i-1]
        for(int i=left;i<=right;i++)
        {
            f = max(f1, f0 + nums[i]);
            f0 = f1;
            f1 = f;
        }
        return f; //相当于返回dp[n-1]
    }
    int rob(vector<int>& nums) {
        int n = nums.size();
        int last = nums[n-1];
        //偷最后一间,或者不偷最后一间,偷的话右侧考虑到n-3,因为偷最后一间,那么倒数第二间一定不能偷,此时最右侧只需要考虑到倒数第三间即可
        return max(robRange(nums, 1, n-3)+last, robRange(nums, 0, n-2));
    }
};
```



### （5）[3186. 施咒的最大总伤害](https://leetcode.cn/problems/maximum-total-damage-with-spell-casting/)

> 一个魔法师有许多不同的咒语。
>
> 给你一个数组 `power` ，其中每个元素表示一个咒语的伤害值，可能会有多个咒语有相同的伤害值。
>
> 已知魔法师使用伤害值为 `power[i]` 的咒语时，他们就 **不能** 使用伤害为 `power[i] - 2` ，`power[i] - 1` ，`power[i] + 1` 或者 `power[i] + 2` 的咒语。
>
> 每个咒语最多只能被使用 **一次** 。
>
> 请你返回这个魔法师可以达到的伤害值之和的 **最大值** 。

本题算是第（2）题：删除并获得点数的进阶版本。代码如下：

```c++
class Solution {
public:
    long long maximumTotalDamage(vector<int>& power) {
        sort(power.begin(), power.end());
        unordered_map<int, int> umap; //key:技能伤害值,value:个数
        //去重,顺便记录个数
        vector<int> nums;
        for(int p: power)
        {
            if(umap.count(p)==0)
            {
                nums.emplace_back(p);
            }
            umap[p]++;
        }
        int n = nums.size();
        vector<long long> dp(n, 0); //dp[i]表示考虑到nums[i],所能造成的最大释咒伤害值
        int k = 2; //本题k=2,其实k也可以替换为别的值
        dp[0] = (long long)nums[0] * umap[nums[0]];
        for(int i=1;i<n;i++)
        {
            //当前咒语释放,或者不释放，use表示释放
            long long use = 0;
            use += (long long)nums[i] * umap[nums[i]]; //释放当前咒语的伤害值

            //删除前面的不能用的咒语,找到最后一个<nums[i]-2的数
            int j = i;
            while(j>=0 && nums[j]>=nums[i]-k) j--;
            if(j>=0) use+=dp[j];
            dp[i] = max(dp[i-1], use); //不释放的话就是dp[i-1]可以过来
        }
        return dp[n-1];
    }
};
```



### （6）思维扩展：[2140. 解决智力问题](https://leetcode.cn/problems/solving-questions-with-brainpower/)

> 给你一个下标从 **0** 开始的二维整数数组 `questions` ，其中 `questions[i] = [pointsi, brainpoweri]` 。
>
> 这个数组表示一场考试里的一系列题目，你需要 **按顺序** （也就是从问题 `0` 开始依次解决），针对每个问题选择 **解决** 或者 **跳过** 操作。解决问题 `i` 将让你 **获得** `pointsi` 的分数，但是你将 **无法** 解决接下来的 `brainpoweri` 个问题（即只能跳过接下来的 `brainpoweri` 个问题）。如果你跳过问题 `i` ，你可以对下一个问题决定使用哪种操作。
>
> - 比方说，给你 
>
>   ```
>   questions = [[3, 2], [4, 3], [4, 4], [2, 5]]：
>   ```
>
>   - 如果问题 `0` 被解决了， 那么你可以获得 `3` 分，但你不能解决问题 `1` 和 `2` 。
>   - 如果你跳过问题 `0` ，且解决问题 `1` ，你将获得 `4` 分但是不能解决问题 `2` 和 `3` 。
>
> 请你返回这场考试里你能获得的 **最高** 分数。



#### （a）自己尝试——错误，踩坑，初见杀



先尝试写一下状态转移方程，假设`dp[i]`表示考虑到第`i`个问题（`i`的下标从0开始），则有做这道题或者不做这道题两种方案：

```c++
dp[i] = max(dp[i-1], dp[j]+questions[i].first) //不做这道题，或者做这道题（注意，如果j到-1了，说明都不能从前面的状态转移过来，这个时候其实也是可以做当前题的）
```

只不过在做这道题的时候，需要找截止到前面允许做这道题的索引，即对于符合要求的j来说，需要满足`questions[j].second < i - j`。有没有可能是再之前的状态转移过来的呢？有可能，但由于每个`dp`数组中的元素都在维护最大值，因此`dp[j]`本身就应该已经包括前面状态最大值的考量了。

本题代码如下：（转化为`dp[i+1]=max(dp[i],dp[j+1]+questions[i].first)`,`j`依旧是从`i`开始往前遍历，找最靠右的那个符合`questions[j].second < i - j`条件的）
```c++
class Solution {
public:
    long long mostPoints(vector<vector<int>>& questions) {
        int n = questions.size();
        vector<long long> dp(n+1, 0);
        for(int i=0;i<n;i++)
        {
            int j = i-1;
            while(j>=0 && questions[j][1] >= i-j) j--; //还不能转移过来,继续往前走
            dp[i+1] = max(dp[i], dp[j+1]+questions[i][0]); //极限情况,j=-1,那么其实也可以做这道题
        }
        return dp[n];
    }
};
```

> 慢着！这道题目使用上面的解答并不能过掉所有的案例！那么问题出在哪里呢？可以参考这一篇：[2140. 解决智力问题 - 力扣（LeetCode）](https://leetcode.cn/problems/solving-questions-with-brainpower/solutions/2360782/you-guan-guan-fang-jie-da-fang-fa-1zhong-rfqu/)。因为当遍历到第j个元素时，某个**小于j的已选元素k**的"脑力恢复期"可能**仍未结束**，因此不能只考虑选择j所造成的"脑力恢复期"。**这个题在这一点上还是比较坑的，第一次很容易踩坑，因此把踩坑过程也记录下来。**



#### （b）正确的做法

从后往前推

```c++
class Solution {
public:
    long long mostPoints(vector<vector<int>>& questions) {
        //dp[i]表示[i, n-1]这个区间的最大值
        //dp[i] = max(dp[i+1], dp[i+questions[i][1]+1]+questions[i][0])
        int n = questions.size();
        vector<long long> dp(n+1, 0);
        //dp[n-1] = questions[n-1][0];
        for(int i=n-1;i>=0;i--)
        {
            dp[i] = dp[i+1]; //不做题
            if(i+questions[i][1]+1<n)
            {
                dp[i] = max(dp[i], dp[i+questions[i][1]+1]+(long long)questions[i][0]); //做题
            }
            else
            {
                dp[i] = max((long long)questions[i][0],dp[i]);
            }
        }
        return dp[0];
    }
};
```

一个简便一些的做法：

```c++
class Solution {
public:
    long long mostPoints(vector<vector<int>>& questions) {
        int n = questions.size();
        vector<long long> f(n + 1);
        for (int i = n - 1; i >= 0; i--) {
            int j = min(i + questions[i][1] + 1, n);
            f[i] = max(f[i + 1], f[j] + questions[i][0]); //不做当前题,或者做当前题,做当前题就一定有当前题的分数,但转移的时候不一定能从有效值转移过来
        }
        return f[0];
    }
};

作者：灵茶山艾府
链接：https://leetcode.cn/problems/solving-questions-with-brainpower/solutions/1213919/dao-xu-dp-by-endlesscheng-2qkc/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```



正序解法中，`f[i]` 应该是表示在**能选择 i 处的前提**下 `[0,i]` 内可以获得的最大分数。此时正序遍历是0(n^2)，我们尝试了会超时。



## 3.最大子数组和（最大子段和）——==未整理完==

有两种做法：

- 定义状态 `f[i]` 表示以 `a[i]` 结尾的最大子数组和，不和 `i` 左边拼起来就是 `f[i]=a[i]`，和`i` 左边拼起来就是 `f[i]=f[i−1]+a[i]`，取最大值就得到了状态转移方程 `f[i]=max(f[i−1],0)+a[i]`，答案为 max(f)(因为不确定最大值是以哪个索引为结尾的，所以要维护中间过程中的max值)。这个做法也叫做 `Kadane` 算法。
- 用前缀和解决。

### （1）[53. 最大子数组和](https://leetcode.cn/problems/maximum-subarray/)——DP法

算是一个正常的板子题，代码如下：
```c++
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int n = nums.size();
        int res = nums[0];
        //vector<int> dp(n+1, 0);
        //dp[i] = max(dp[i-1]+nums[i], nums[i])
        int cur = 0;
        for(int i=0;i<n;i++)
        {
            //dp[i+1] = max(dp[i]+nums[i], nums[i]);
            cur = max(cur, 0) + nums[i];
            res = max(res, cur);
            //res = max(res, dp[i+1]);
        }
        return res;
    }
};
```



### （2）[1749. 任意子数组和的绝对值的最大值](https://leetcode.cn/problems/maximum-absolute-sum-of-any-subarray/)

代码如下：

```c++
class Solution {
public:
    int maxAbsoluteSum(vector<int>& nums) {
        int res=0, minSum=0, maxSum=0; //子数组有可能是空的,所以初始化为0即可; 如果类似于53题子数组不能为空,则或许需要初始化为INT_MIN/INT_MAX(看需求)
        for(const int& num: nums)
        {
            minSum = min(minSum, 0) + num;
            maxSum = max(maxSum, 0) + num;
            res = max(res, max(-minSum, maxSum));
        }
        return res;
    }
};
```



### （3）



# 二、网格图DP

对于一些二维 DP（例如背包、最长公共子序列），如果把 DP 矩阵画出来，其实状态转移可以视作在网格图上的移动。所以在学习相对更抽象的二维 DP 之前，做一些形象的网格图 DP 会让后续的学习更轻松（比如 0-1 背包的空间优化写法为什么要倒序遍历）。

### 1.基础

### （1）[64. 最小路径和](https://leetcode.cn/problems/minimum-path-sum/)

```c++
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        //dp[i][j]表示左上角到[i,j]位置的最小数字总和
        int m = grid.size();
        int n = grid[0].size();
        vector<vector<int>> dp(m, vector<int>(n,0));
        dp[0][0] = grid[0][0];
        for(int i=1;i<m;i++) dp[i][0] = dp[i-1][0] + grid[i][0];
        for(int j=1;j<n;j++) dp[0][j] = dp[0][j-1] + grid[0][j];
        for(int i=1;i<m;i++)
        {
            for(int j=1;j<n;j++)
            {
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j];
            }
        }
        return dp[m-1][n-1];
    }
};
```



### （2）不同路径

```c++
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> dp(m, vector<int>(n));
        //初始化第一行和第一列
        for(int i=0;i<m;i++) dp[i][0]=1; //第一列
        //第一行 
        for(int i=0;i<n;i++) dp[0][i]=1;
        for(int i=1;i<m;i++)
        {
            for(int j=1;j<n;j++)
                dp[i][j] = dp[i-1][j]+dp[i][j-1];
        }
        return dp[m-1][n-1];
    }
};
```



### （3）[63. 不同路径 II](https://leetcode.cn/problems/unique-paths-ii/)

也是从左上角走到右下角，但区别在于本题中有障碍物，需要做障碍物的对应判断。

> 本题的要点是在于dp数组初始值的设定，注意考虑好左上角是障碍物的情况，此时第一行和第一列应该都是0.因此赋值逻辑应该写作把第一行和第一列截止到第一个障碍物之前的都设置为`dp[0][0]`（务必注意！每次都写错，不能赋值为1，否则左上角即为障碍物的情况考虑不到）

```c++
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        int m = obstacleGrid.size();
        int n = obstacleGrid[0].size();
        vector<vector<int>> dp(m, vector<int>(n, 0));
        //赋值初值
        dp[0][0] = ((obstacleGrid[0][0]==1)? 0:1);
        //第一列与第一行
        for(int i=1;i<m && obstacleGrid[i][0]==0;i++) dp[i][0] = dp[0][0]; //没有遇到障碍物,则有1条路径,否则障碍物及后面的都是0条路径,**务必注意边界测试用例:左上角是障碍物的情况**
        for(int j=1;j<n && obstacleGrid[0][j]==0;j++) dp[0][j] = dp[0][0];
        for(int i=1;i<m;i++)
        {
            for(int j=1;j<n;j++)
            {
                if(obstacleGrid[i][j]==1) dp[i][j] = 0; //有障碍物,过不去
                else
                {
                    dp[i][j] = dp[i-1][j] + dp[i][j-1];
                }
            }
        }
        return dp[m-1][n-1];
    }
};
```



### （4）[120. 三角形最小路径和](https://leetcode.cn/problems/triangle/)

> 心得体会：这种二维网格图的dp题，遇到`i-1`，`j-1`不太好像前面的题一样整体把dp数组往右移一位（边界条件会有一点麻烦），所以一般就用`dp[i][j]`来表示与原数组`grid[i][j]`有关的信息，然后手动管理好可能会越界的情况。

```c++
class Solution {
public:
    int minimumTotal(vector<vector<int>>& triangle) {
        int n = triangle.size();
        vector<vector<int>> dp(n, vector<int>(n));
        dp[0][0]=triangle[0][0];
        if(n==1) return triangle[0][0];
        for(int i=1;i<n;i++)
        {
            //最左侧
            dp[i][0] = dp[i-1][0]+triangle[i][0];
            for(int j=1;j<i;j++)
            {
                dp[i][j]=min(dp[i-1][j-1],dp[i-1][j])+triangle[i][j];
            }
            //最右侧
            dp[i][i] = dp[i-1][i-1]+triangle[i][i];
        }
        //最后一行看看谁最小
        int res = INT_MAX;
        for(int i=0;i<n;i++)
        {
            res=min(res, dp[n-1][i]);
        }
        return res;
    }
};
```



### （5）[2684. 矩阵中移动的最大次数](https://leetcode.cn/problems/maximum-number-of-moves-in-a-grid/)（整理一个DFS做法，有需要再看）

这道题目用dp做有一点邪门，在提交记录当中可以看到，这里补充一种DFS的做法，有需要可以复习一下。

```c++
class Solution {
public:
    int dirs[3][2] = {0,1,1,1,-1,1}; //r,c: 右,右下,或者右上
    int maxMoves(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        //ans是最大移动的步数
        int ans = 0;
        auto dfs = [&](this auto&& dfs, int x, int y)
        {
            ans = max(ans, y); //从第一列开始走,y=1即为移动1步,依次类推
            if(ans==n-1) return; //走到最右侧了,return
            //往严格大的地方走
            for(int d=0;d<3;d++)
            {
                int curX = x + dirs[d][0];
                int curY = y + dirs[d][1];
                if(curX>=m || curX<0 ) continue;
                if(grid[curX][curY]>grid[x][y])
                {
                    dfs(curX, curY); 
                }
            }
            grid[x][y] = 0; //用这个来充当visited数组,后面不会再遍历到了,因为这个节点后面的路径已经探索完了,没必要再探索（跟那些岛屿问题是一样的）
        };
        //第一列都试试
        for(int i=0;i<m;i++)
        {
            dfs(i, 0);
        }
        return ans;
    }
};
```



### （6）[3418. 机器人可以获得的最大金币数](https://leetcode.cn/problems/maximum-amount-of-money-robot-can-earn/)

依旧是从左上角出发，到达右下角。网格中的每个单元格包含一个值 `coins[i][j]`：

- 如果 `coins[i][j] >= 0`，机器人可以获得该单元格的金币。
- 如果 `coins[i][j] < 0`，机器人会遇到一个强盗，强盗会抢走该单元格数值的 **绝对值** 的金币。

不过对于本题而言，机器人有一项特殊能力，可以在行程中 **最多感化** 2个单元格的强盗，从而防止这些单元格的金币被抢走。

**注意：**机器人的总金币数可以是负数。

返回机器人在路径上可以获得的 **最大金币数** 。



这道题目可以给`dp`数组加一维，`dp[i][j][k]`表示到达网格下标为（i，j）的位置时，使用了k次技能后所能获得的最多金币。于是状态转移方程就变成了：

```c++
dp[i][j][k] = max(dp[i-1][j][k]+coins[i][j], dp[i][j-1][k]+coins[i][j]); //对每个k都要赋值一下(k=0,1,2)，相当于当前格没有感化强盗，需要吃金币/吃伤害
if(coins[i][j]<0) //有强盗，也可以选择在当前格感化强盗
{
	dp[i][j][k] = max(dp[i][j][k], dp[i-1][j][k-1], dp[i][j-1][k-1]); //当前格使用了技能，从k-1次技能转移过来，但也得是从左侧或者上侧过来的
}
```

注意到不合法的状态应该是`dp(-1,j,k)`以及`dp(i,-1,k)`（其中k的合法性比较好做，就不提了），本题要求max，则可以用-inf来表示不合法的状态，这样再取max的时候就不会取到-inf了。

- `dp[0,0,0] = coins[0,0]`；表示使用了0次技能，那获得的金币数就是coins[0,0]本身；
- if k>0， `dp[0,0,0] = max(coins[0,0], 0);`,意味着此时感化了强盗，会让负的金币数变成0,正的金币就不动(相当于没有效果)。

在写代码的时候，依旧可以给i和j都加一维，因为初始化为-inf所以边界条件也有了（注意，由于本题可能有负值的强盗，所以初始化为-inf可能会越界，可以改为-0x3f3f3f）。最终代码如下：

```c++
class Solution {
public:
    int maximumAmount(vector<vector<int>>& coins) {
        int m = coins.size();
        int n = coins[0].size();
        vector<vector<array<int, 3>>> dp(m+1, vector<array<int, 3>>(n+1, array<int,3>{-0x3f3f3f, -0x3f3f3f, -0x3f3f3f}));
        //dp[0][0][k]的赋值
        dp[1][1] = {coins[0][0], max(0, coins[0][0]), max(0,coins[0][0])};
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                int x = coins[i][j];
                //k最多为2,直接写逻辑就行
                if(i==0 && j==0) continue; //前面赋值了,这里可以稍微特判一下
                dp[i+1][j+1][0] = max(dp[i][j+1][0], dp[i+1][j][0]) + x;
                dp[i+1][j+1][1] = max({dp[i][j+1][1] + x, dp[i+1][j][1] + x, dp[i][j+1][0], dp[i+1][j][0]});
                dp[i+1][j+1][2] = max({dp[i][j+1][2] + x, dp[i+1][j][2] + x, dp[i][j+1][1], dp[i+1][j][1]});
            }
        }
        //return max({dp[m][n][0], dp[m][n][1], dp[m][n][2]}); 
        return dp[m][n][2]; //感化了两次，效果一定>=感化1次或者0次
    }
};
```



### （7）[1594. 矩阵的最大非负积](https://leetcode.cn/problems/maximum-non-negative-product-in-a-matrix/)

在前面的题目中，有遇到过求最大绝对值的题目，思路是维护一个最大值和一个最小值，当遇到负数的时候交换最大值和最小值（对本题来说，不要交换dp，而是在状态转移方程的时候交换逻辑），本题也可以用类似的思路来做。最终代码如下：
```c++
class Solution {
public:
    const int MOD = 1e9+7;
    int maxProductPath(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        vector dp(m, vector<array<long long, 2>>(n, array<long long, 2>{})); //存最大值与最小值,array第一个数存最大值,第二个数存最小值
        dp[0][0] = {grid[0][0], grid[0][0]};
        //第一行和第一列没得选,只有一种结果
        for(int i=1;i<m;i++)
        {
            dp[i][0] = {dp[i-1][0][0] * grid[i][0], dp[i-1][0][1] * grid[i][0]};
        }
        for(int j=1;j<n;j++)
        {
            dp[0][j] = {dp[0][j-1][0]*grid[0][j], dp[0][j-1][1]*grid[0][j]};
        }
        for(int i=1;i<m;i++)
        {
            for(int j=1;j<n;j++)
            {
                int cur = grid[i][j];
                if(cur>0) //正常维护即可
                {
                    dp[i][j][0] = max(dp[i-1][j][0]*cur, dp[i][j-1][0]*cur);
                    dp[i][j][1] = min(dp[i-1][j][1]*cur, dp[i][j-1][1]*cur);
                }
                else //反着维护,最大值由之前的最小值得到,最小值由之前的最大值得到
                {
                    dp[i][j][0] = max(dp[i-1][j][1]*cur, dp[i][j-1][1]*cur); //这题找了半天有个坑,因为有负数的乘法操作,所以cur要乘在里面,不能max(a,b)*cur,会起不到对应的作用
                    dp[i][j][1] = min(dp[i-1][j][0]*cur, dp[i][j-1][0]*cur);
                }
            }
        }
        // for(int i=0;i<m;i++)
        // {
        //     for(int j=0;j<n;j++)
        //         cout<<i<<" "<<j<<" "<<dp[i][j][0]<<" "<<dp[i][j][1]<<endl;
        // }
        long long res = dp[m-1][n-1][0]%MOD; //最大值
        if(res<0) return -1;
        return res;

    }
};
```



## 以下为现阶段困难题部分

### （8）[1301. 最大得分的路径数目 ](https://leetcode.cn/problems/number-of-paths-with-max-score/):cat:

> 给你一个正方形字符数组 `board` ，你从数组最右下方的字符 `'S'` 出发。
>
> 你的目标是到达数组最左上角的字符 `'E'` ，数组剩余的部分为数字字符 `1, 2, ..., 9` 或者障碍 `'X'`。在每一步移动中，你可以向上、向左或者左上方移动，可以移动的前提是到达的格子没有障碍。
>
> 一条路径的 「得分」 定义为：路径上所有数字的和。
>
> 请你返回一个列表，包含两个整数：第一个整数是 「得分」 的最大值，第二个整数是得到最大得分的方案数，请把结果对 **`10^9 + 7`** **取余**。
>
> 如果没有任何路径可以到达终点，请返回 `[0, 0]` 。
>
>  
>
> **示例 1：**
>
> ```
> 输入：board = ["E23","2X2","12S"]
> 输出：[7,1]
> ```
>
> **示例 2：**
>
> ```
> 输入：board = ["E12","1X1","21S"]
> 输出：[4,2]
> ```
>
> **示例 3：**
>
> ```
> 输入：board = ["E11","XXX","11S"]
> 输出：[0,0]
> ```
>
>  
>
> **提示：**
>
> - `2 <= board.length == board[i].length <= 100`

本题是比较有难度的，需要用一个pair维护最大分数以及方案数，具体的注释写在了下面的代码中：

```c++
class Solution {
public:
    using PII = pair<int, int>;
    const int MOD = 1e9+7;
    int n = 0;
    void update(vector<vector<PII>>& dp, int curx, int cury, int oldx, int oldy)
    {
        //正常更新逻辑,cur是当前的ij,而old则是考虑的转移过来的状态
        if(oldx>=n ||oldy>=n || oldx<0 || oldy<0) return;
        if(dp[oldx][oldy].first > dp[curx][cury].first) //这个状态的值更大
        {
            dp[curx][cury] = dp[oldx][oldy];
        }
        else if(dp[oldx][oldy].first==dp[curx][cury].first) //相等的情况,
        {
            dp[curx][cury].second  += dp[oldx][oldy].second;
        }
        if(dp[curx][cury].second>MOD)
        {
            dp[curx][cury].second-=MOD;
        }
    }
    vector<int> pathsWithMaxScore(vector<string>& board) {
        //在dp数组中存放一个PII,表示最大值值和方案数
        //注意本题是从右下角,向上,左,左上方移动,因此有:(假设我们只考虑最大值)
        //dp[i][j] = max({dp[i+1][j], dp[i][j+1], dp[i+1][j+1]}) + board[i][j] - '0'; (特判一下'X'的时候应该是-1),然后再找一下从哪个状态过来的,记录一下方案数(如果是相等的,加入之前的,如果之前的更大,则替换为之前的方案数,否则不做处理)
        n = board[0].size();
        vector dp(n, vector<PII>(n, {-1,0})); //初始值按照{-1, 0}来赋值就可以了(表示一开始都没得走)
        //常见的套路：赋值右下角那个值，因为是S所以一定0分，有一个方案。
        dp[n-1][n-1] = {0, 1}; 
        //开始状态转移
        for(int i=n-1;i>=0;i--)
        {
            for(int j=n-1;j>=0;j--)
            {
                if(i==n-1 && j==n-1) continue;
                //默认情况针对障碍物,不是障碍物的话update一下
                if(board[i][j]!='X')
                {
                    update(dp, i, j, i+1, j);
                    update(dp, i, j, i, j+1);
                    update(dp, i, j, i+1, j+1);
                    if(dp[i][j].first!=-1)  //注意,这句需要加,也就是board[i][j]!='X'的时候dp[i][j].first为-1也是不行的,说明别的状态转移不过来,比如中间的XXXX拦住了,此时从下面应该推不上来才对
                    {
                        if(board[i][j]!='E') //非目的地,加上分数
                        {
                            dp[i][j].first += (board[i][j] - '0'); //有分数,把当前的分数加上
                        }
                    }
                }
            }
        }
        if(dp[0][0].first==-1) return {0,0};
        else return {dp[0][0].first, dp[0][0].second};
    }
};
```



### （9）[2435. 矩阵中和能被 K 整除的路径](https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/) :cat:

> 给你一个下标从 **0** 开始的 `m x n` 整数矩阵 `grid` 和一个整数 `k` 。你从起点 `(0, 0)` 出发，每一步只能往 **下** 或者往 **右** ，你想要到达终点 `(m - 1, n - 1)` 。
>
> 请你返回路径和能被 `k` 整除的路径数目，由于答案可能很大，返回答案对 `10^9 + 7` **取余** 的结果。

参考题解：[2435. 矩阵中和能被 K 整除的路径 - 力扣（LeetCode）](https://leetcode.cn/problems/paths-in-matrix-whose-sum-is-divisible-by-k/solutions/1878910/dong-tai-gui-hua-pythonjavacgo-by-endles-94wq/)

需要多做一点题来熟悉套路。本题可以把路径和模k的结果作为一个扩展维度。

![image-20250326214438859](assets/image-20250326214438859.png)

注意这个套路，以后可能会用得到：

```c++
class Solution {
public:
    int numberOfPaths(vector<vector<int>>& grid, int k) {
        //多一个维度(第三个维度)表示路径和%k对应的余数代表的路径数目
        //dp[i][j][(v+grid[i][j])%k] = (dp[i-1][j][v] + dp[i][j-1][v])%mod; v的范围是0到k(统统遍历一遍!),防止越界将下标+1
        //dp[0][0][grid[0][0]%k] = 1;
        const int MOD = 1e9+7;
        int m = grid.size();
        int n = grid[0].size();
        int dp[m+1][n+1][k];
        memset(dp, 0, sizeof(dp));//这题是方案数 所以初始化为0
        dp[1][1][grid[0][0]%k] = 1;//除了左上角初始值为1
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                if(i==0 && j==0) continue; //之前赋完值了,不管
                for(int v=0;v<k;v++)
                {
                    dp[i+1][j+1][(v+grid[i][j])%k] = (dp[i][j+1][v] + dp[i+1][j][v])%MOD;
                }
            }
        }
        return dp[m][n][0]; //能够被k整除
    }
};
```

易错点：

>```C++
>1 方案数初始化为0才是对的
>2 第二维初始化需要写为vector<vector<int>>...而不是vector<int>...
>//vector<vector<vector<int>>> dp(m+1,vector<int>(n+1,vector<int>(k,-0x3f3f3f)));
>vector<vector<vector<int>>> dp(m+1,vector<vector<int>>(n+1,vector<int>(k,0)));
>```



### （10）[174. 地下城游戏](https://leetcode.cn/problems/dungeon-game/)

省流：左上角为起点，右下角为终点，骑士只能往右或者往下走，初始健康值为x，每一格（包括起点和终点）可能为正数表示加血，负数表示扣血，如果血量<=0立刻死亡。问：能够到达右下角且不死亡的最小的初始健康值x是多少？

可以看一下这个视频：[大巧不工，动态规划的正确打开方式。力扣 174，地下城游戏_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Jex9e6EUf/?spm_id_from=333.337.search-card.all.click&vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)

> 补充：关于本题左上角到右下角DP不满足“无后效性”的说明：[174. 地下城游戏 - 力扣（LeetCode）](https://leetcode.cn/problems/dungeon-game/solutions/326171/di-xia-cheng-you-xi-by-leetcode-solution/)
>
> 另一种比较好记的说法：
>
> - 从左上到右下是错误的说的通俗易懂点就是如果`dungeon[i][j]`为负数,那走到这一格子就是一个扣血的过程,如果当前剩余血量扣掉之后是负的,那肯定不行,所以有可能前一步多剩点血可能是好事,也有可能初始血量得加点才死不了。**这样的话就很难做出合理的决策了。**因此可以考虑从右下角往左上角推，并保证推导每一步的合法性（**相当于考虑每一步骑士不死所需要的最少血量**）。

**最终解法（看这个！）**:

- 令`dp[i][j]`表示从(i,j)到终点所需的最少血量，可以发现右下角是最小的子问题，而左上是一个比较麻烦的问题，因此我们从右下角转移到左上角（`dp[0][0]`是要求解的终极问题）。
- 在右下角时，`dp[m-1][n-1] = max(1, 1-dungeon[m-1][n-1])`,如果这个格子是怪比较好理解，至少需要` 1-dungeon[m-1][n-1]`这么多的血才够扣。如果这个格子是回血包，那`1-dungeon[m-1][n-1]<1`，但至少得保证为1才是合理状态（不然就死了）。**也就是说这个状态说明至少需要1的血**. 注意是有"**1- dun...**" ,因为至少需要维持1血 
- 接着是状态转移方程：
  - `dp[i][j] = max(1, min(dp[i+1][j]-dungeon[i][j], dp[i][j+1]-dungeon[i][j])`;后两者取min是因为要尽量小的血量（因为一定能保证结果合法，所以选少的那个做状态转移是合适的）
  - 可以设置**边界值**为0x3f3f3f，意味着**血量无穷**，在状态转移**求min**的时候右边界和下边界一定会从合法的那边转过来。(**求最小**)

> 出发的血量是无法确定的，想要确定就要枚举（二分），但结束时的血量是可以确定的（>=1，因为从右下推到左上，可以认为往右或者往下走的状态本来就已经通过max(1，xxx）约束强制只考虑合法的情况了，就省了枚举的步骤，所以从结束倒推更快。

最终代码如下：
```c++
class Solution {
public:
    int calculateMinimumHP(vector<vector<int>>& dungeon) {
        int m = dungeon.size();
        int n = dungeon[0].size();
        vector<vector<int>> dp(m+1, vector<int>(n+1, 0x3f3f3f));
        dp[m-1][n-1] = max(1, 1-dungeon[m-1][n-1]);
        for(int i=m-1;i>=0;i--)
        {
            for(int j=n-1;j>=0;j--)
            {
                if(i==m-1 && j==n-1) continue;
                dp[i][j] = max(1, min(dp[i][j+1]-dungeon[i][j], dp[i+1][j]-dungeon[i][j]));
            }
        }
        return dp[0][0];
    }
};
```



### ==（11）[329. 矩阵中的最长递增路径](https://leetcode.cn/problems/longest-increasing-path-in-a-matrix/)==

> 给定一个 `m x n` 整数矩阵 `matrix` ，找出其中 **最长递增路径** 的长度。
>
> 对于每个单元格，你可以往上，下，左，右四个方向移动。 你 **不能** 在 **对角线** 方向上移动或移动到 **边界外**（即不允许环绕）。





# 三、背包专题

## 1.0-1背包

### （1）纯板子

先来看一道纯板子题：[P1048 [NOIP2005 普及组\] 采药 - 洛谷 | 计算机科学教育新生态](https://www.luogu.com.cn/problem/P1048)

```C++
#include<iostream>
#include<vector>
using namespace std;
int main()
{
    int t,m;
    cin>>t>>m;
    vector<int> v(m,0);//花费时间 / 重量
    vector<int> w(m,0); // 价值
    for(int i=0;i<m;i++)
    {
        cin>>v[i]>>w[i];
    }
    vector<vector<int>> dp(m+1,vector<int>(t+1,0));
    dp[0][0] = 0;
    for(int i=0;i<m;i++)
    {
        for(int j=0;j<=t;j++)
        {
            if(j-v[i]>=0)
                dp[i+1][j] =  max(dp[i][j],dp[i][j-v[i]]+w[i]);
            else
                dp[i+1][j] = dp[i][j];
        }
    }
    cout<<dp[m][t]<<endl;
    return 0;
}
```

优化为一维

```C++
#include<iostream>
#include<vector>
using namespace std;
int main()
{
    int t,m;
    cin>>t>>m;
    vector<int> v(m,0);//花费时间 / 重量
    vector<int> w(m,0); // 价值
    for(int i=0;i<m;i++)
    {
        cin>>v[i]>>w[i];
    }
    vector<int> dp(t+1,0);
    dp[0] = 0;
    for(int i=0;i<m;i++)
    {
        for(int j=t;j>=v[i];j--) //一维这里需要逆序
        {
            dp[j] =  max(dp[j],dp[j-v[i]]+w[i]);
        }
    }
    cout<<dp[t]<<endl;
    return 0;
}
```



这次我们来试一下记忆化搜索怎么写（用dfs+lambda表达式），后面会改成动规，练习一下：

> 注意，以下的写法需要C++ 20才能编译通过，C++ 11是不能编译通过的，感觉看看得了，也不能保证笔试的时候有C++ 20的环境。以防万一也可以把lambda表达式写成正常的dfs+数组存储，可读性也比较好，还不容易出问题。

```c++
#include<iostream>
#include<vector>
using namespace std;
const int N = 105;

int main()
{
    int t,m; //t:背包容量,m:总的物体数量
    cin>>t>>m;
    int v[N], w[N]; //v[N]存放所有物品的价值,w[N]存放所有物体的重量
    for(int i=0;i<m;i++)
    {
        cin>>w[i]>>v[i]; //索引从0开始
    }
    vector<vector<int>> mem(m, vector<int>(t+1, -1)); //用于记忆化搜索,初始化为-1
    auto dfs = [&](auto&& self, int i, int c)->int  // 返回值是当背包剩余最大容量为c时,截止到第i个物品的最大价值
    {
        if(i<0) return 0;
        auto& res = mem[i][c]; //注意是引用传递
        if(res!=-1) return res; //记忆化搜索

        //剩余容量不够了,只能不装
        if(c<w[i]) res = self(self, i-1, c);
        else res = max(self(self, i-1,c), self(self, i-1, c-w[i])+v[i]);
        return res;
    };

    int res = dfs(dfs, m-1, t);
    cout<<res<<endl;

    return 0;
}
```

>做题步骤可以是：先自己注释里写出转移方程二维dp形式以及边界写完，正式代码上直接写一维的 ，记得j是从右到左遍历



### （2）leetcode 494：目标和

[494. 目标和 - 力扣（LeetCode）](https://leetcode.cn/problems/target-sum/)

给你一个非负整数数组 `nums` 和一个整数 `target` 。

向数组中的每个整数前添加 `'+'` 或 `'-'` ，然后串联起所有整数，可以构造一个 **表达式** ：

- 例如，`nums = [2, 1]` ，可以在 `2` 之前添加 `'+'` ，在 `1` 之前添加 `'-'` ，然后串联起来得到表达式 `"+2-1"` 。

返回可以通过上述方法构造的、运算结果等于 `target` 的不同 **表达式** 的数目。

**示例 1：**

```
输入：nums = [1,1,1,1,1], target = 3
输出：5
解释：一共有 5 种方法让最终目标和为 3 。
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
```

**普通做法，开一个二维数组**

```c++
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        //1.假设所有选中的数组中要设置为正数的和为s,所有选中的数组中的要设置为负数部分的和为t
        //有: s+t = sum 且 s - t = target
        //∴ s = (sum+target)/2;
        int sum = reduce(nums.begin(), nums.end()) + target; 
        if(sum<0 || sum%2==1) return 0; //此时s不符合题意,一定找不到对应结果
        int n = nums.size();
        int s = sum / 2;
        //问题转换为找到数组中的一些数,使得总和为s的方案数

        //dp[i][j]表示考虑到索引为i-1时,和为j的总表达式的数目, return dp[n][s];
        vector<vector<int>> dp(n+1, vector<int>(s+1, 0)); //默认方案数都是0
        //初始化,dp[0][0]=1;
        dp[0][0]=1; //跟之前的题目有共同之处

        //dp[i][j] = dp[i-1][j] + dp[i-1][j-nums[i]] //没选当前这个数,或者选了当前这个数
        //防止i-1越界,可以:
        //dp[i+1][j] = dp[i][j] + dp[i][j-nums[i]];
        for(int i=0;i<nums.size();i++)
        {
            for(int j=0;j<=s;j++)
            {
                if(j<nums[i]) dp[i+1][j] = dp[i][j];
                else dp[i+1][j] = dp[i][j] + dp[i][j-nums[i]];
            }
        }
        return dp[n][s];
    }
};
```



**优化空间：**

观察可以看到，`dp[i+1][...]`是由`dp[i][...]`得到的，因此其实两个数组就够了，一种简单的写法是把所有的`dp[i][j]`换成`dp[i%2][j]`。一样可以通过本题。此时的状态转移方程代码可以写做：

```c++
for(int i=0;i<nums.size();i++)
{
    for(int j=0;j<=s;j++)
    {
        if(j<nums[i]) dp[(i+1)%2][j] = dp[i%2][j];
        else dp[(i+1)%2][j] = dp[i%2][j] + dp[i%2][j-nums[i]];
    }
}
return dp[n%2][s];
```



**再次优化，一维dp**

那么，能否用一维数组继续降维？从前往后是不行的，因为很可能用到某个`dp[i][j-nums[i]]`在前面已经被更新了，而实际上我们要的是未更新的版本，所以不能从前往后遍历，但**可以从后往前遍历。**此时代码如下：

```c++
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = reduce(nums.begin(), nums.end()) + target; 
        if(sum<0 || sum%2==1) return 0; //此时s不符合题意,一定找不到对应结果
        int n = nums.size();
        int s = sum / 2;
        vector<int> dp(s+1, 0); //默认方案数都是0
        dp[0]=1; //跟之前的题目有共同之处

        for(int i=0;i<nums.size();i++)
        {
            for(int j=s;j>=0;j--)
            {
                if(j>=nums[i]) dp[j] += dp[j-nums[i]];
            }
        }
        return dp[s];
    }
};
```

考虑数目 ，使用和+

### （3）[2915. 和为目标值的最长子序列的长度](https://leetcode.cn/problems/length-of-the-longest-subsequence-that-sums-to-target/)

```c++
class Solution {
public:
    int lengthOfLongestSubsequence(vector<int>& nums, int target) {
        //经典0-1背包
        //dp[i][j] = max(dp[i-1][j], dp[i-1][j-nums[i]]+1);
        vector<int> dp(target+1, INT_MIN);
        dp[0] = 0;
        int n = nums.size();
        for(int i=0;i<n;i++)
        {
            for(int j=target;j>=nums[i];j--)
            {
                dp[j] = max(dp[j], dp[j-nums[i]]+1); 
            }
        }
        if(dp[target]<INT_MIN/2) return -1; //这里dp[target]有可能会被更新为INT_MIN+1这种,因此不能用==INT_MIN来判断,只要足够小就说明不存在
        return dp[target];
    }
};
```

考虑最长， 使用max

### （4）[416. 分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/)

给你一个 **只包含正整数** 的 **非空** 数组 `nums` 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。

**示例 1：**

```
输入：nums = [1,5,11,5]
输出：true
解释：数组可以分割成 [1, 5, 5] 和 [11] 。
```

```c++
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        //背包问题简单变种, 算sum/2为target
        int sum = reduce(nums.begin(), nums.end());
        if(sum%2==1) return false;
        int target = sum/2;
        vector<int> dp(target+1, 0); //一开始都是false
        //看一下dp[i][j]表示考虑前i个数能否使得和=j
        dp[0] = 1; 
        int n=nums.size();
        for(int i=0;i<n;i++)
        {
            //从右往左遍历
            for(int j=target;j>=nums[i];j--)
                dp[j] = (dp[j] || dp[j-nums[i]]); //背包变种,不选当前数,或者选当前数
        }
        return (bool) dp[target];
    }
};
```

Y

```c++
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        //sum/2
        int sum = reduce(nums.begin(),nums.end());
        if(sum%2==1)return false;
        sum =sum/2;
        //dp[i][j] = dp[i-1][j]|dp[i-1][j-nums[i]]
        //dp[-1][0] = true;
        int n = nums.size();
        vector<bool> dp(sum+1,false);
        dp[0]=true;
        for(int i=0;i<n;i++)
        {
            for(int j=sum;j>=nums[i];j--)
            {
                dp[j] = dp[j]|dp[j-nums[i]];
            }
        }
        return dp[sum];
    }
};
```

考虑true/false  使用或|

### （5）[2787. 将一个数字表示成幂的和的方案数](https://leetcode.cn/problems/ways-to-express-an-integer-as-sum-of-powers/)

可以先用二维的做，再看看能否降维。

```c++
class Solution {
public:
    const int MOD = 1e9+7;
    int numberOfWays(int n, int x) {
        vector<int> dp(n+1, 0); //dp[i][j]表示考虑到正整数i时,且此时总和为j时的方案数,但可以把i省略掉
        dp[0] = 1;
        //dp[i][j] = dp[i-1][j] + dp[i-1][j-pow(i, x)]
        //-> dp[i+1][j] = dp[i][j] + dp[i][j-pow(i, x)]
        //能否降维?可以从后往前降维
        for(int i=1;i<=n;i++) //注意这里的i指的是要选的数,从1开始
        {
            for(int j=n;j>=pow(i, x);j--)
            {
                dp[j] = (dp[j]%MOD + dp[j-pow(i, x)]%MOD)%MOD; 
            }
        }
        return dp[n]%MOD;
    }
};
```

考虑数目，使用和+



### （6）[3180. 执行操作可获得的最大总奖励 I](https://leetcode.cn/problems/maximum-total-reward-using-operations-i/)

> 给你一个整数数组 `rewardValues`，长度为 `n`，代表奖励的值。
>
> 最初，你的总奖励 `x` 为 0，所有下标都是 **未标记** 的。你可以执行以下操作 **任意次** ：
>
> - 从区间 `[0, n - 1]` 中选择一个 **未标记** 的下标 `i`。
> - 如果 `rewardValues[i]` **大于** 你当前的总奖励 `x`，则将 `rewardValues[i]` 加到 `x` 上（即 `x = x + rewardValues[i]`），并 **标记** 下标 `i`。
>
> 以整数形式返回执行最优操作能够获得的 **最大** 总奖励。

本题是隐式“有顺序要求的”，所以需要一点贪心的思维，假设先考虑大的，再考虑小的，不会好过先考虑小的，再考虑大的，因此可以先对`rewardValues`数组做从小到大的排序，即可转换为0-1背包问题。令`dp[i][j]`表示考虑前i个物体的时候，获取到的总奖励值为j是否可行。最终我们要找到对于dp[n]来说，最大的为true的j是多少。

- 状态转移方程：`dp[i][j] = (dp[i-1][j] | dp[i-1][j-rewardValues[i]])`,不过这里要保证`j>=rewardValues[i] && j-rewardValues[i]<rewardValues[i]`。
- dp数组开的时候，第一维开到n+1（防止越界），第二维开到2*m即可，m是数组中的最大值（想象一下，最大的那个数一定会被选，因为如果最后选的不是最大的那个数m，则将其改成选择最大的数m会使得总奖励值更大，因此想要获得最大奖励，总要选最大的那个值m），此时选m之前的总奖励x应该<m（不然选不了），因此最大的奖励结果不会超过2m-1。无法得到比2m-1更大的和。

- 最终求解的为使得`dp[n][j]=1`的最大的j，注意到只需要遍历到2m-1即可，m是数组中的最大值。

本题代码如下：

```c++
class Solution {
public:
    int maxTotalReward(vector<int>& rewardValues) {
        //1.sort
        //1.dp[i][j]:i是考虑的数, j是使得总奖励为j是否可行 
        //使得dp[n][j]=true的最大j
        //第二维多少? 一定会包含最大的rewardValue(设为m),最大奖励值为2*m-1
        sort(rewardValues.begin(), rewardValues.end());
        int mx = rewardValues.back();
        int n = rewardValues.size();
        vector<int> dp(2*mx+1, 0);
        dp[0] = 1; //这种奖励情况是合法的,能拿到
        //接下来就是0-1背包了
        for(int i=0;i<n;i++)
        {
            for(int j=2*rewardValues[i]-1;j>=rewardValues[i];j--)
            {
                dp[j] |= dp[j-rewardValues[i]];
            }
        }
        int i = 2*mx-1;
        for( ;i>=0;i--)
        {
            if(dp[i]==1) break;
        }
        return i;
    }
};
```

>这里起始位置是 `j=2*rewardValues[i]-1;`，自动保证了` j-rewardValues[i]<rewardValues[i]`。
>
>```C++
>for(int j=2*rewardValues[i]-1;j>=rewardValues[i];j--)
>{
>    dp[j] |= dp[j-rewardValues[i]];
>}
>```

### （7）二维背包——[474. 一和零](https://leetcode.cn/problems/ones-and-zeroes/)

> 本题除了背包是二维的，还需要考虑“至多”如何体现在背包当中。对于“至多”的类型，初始值设置为当i=-1时，相当于背包中没有任何物品，对于恰好型的来说`dp[-1][0]`才是合法态，而如果是至多的话`dp[-1][j]`都是合法的（个人理解相当于没用完背包的容量，是满足“至多”属性的，没有问题）。

代码如下：

```c++
class Solution {
public:
    int findMaxForm(vector<string>& strs, int m, int n) {
        //二维背包,dp[i][j][k]表示考虑到第i个字符串str,0的个数"至多"为j,1的个数"至多"为k的最大子集的长度(最多能选几个)
        //dp[i][j][k] = max(dp[i-1][j][k], dp[i-1][j-当前字符串0的个数][k-当前字符串1的个数]+1); 当然,要保证不要越界
        //dp[-1][j][k] = 0 相当于没有物品可以选,为0
        int sz = strs.size();
        vector dp(m+1, vector<int>(n+1)); //dp[0][j][k]都是0,表示什么都没选的情况下,最大子集长度一定是0
        for(int i=0;i<sz;i++)
        {
            int zeroCnt = ranges::count(strs[i], '0');
            int oneCnt = (int)strs[i].size() - zeroCnt;
            for(int j=m;j>=zeroCnt;j--)
            {
                for(int k=n;k>=oneCnt;k--)
                {
                    dp[j][k] = max(dp[j][k], dp[j-zeroCnt][k-oneCnt]+1);
                }
            }
        }
        return dp[m][n];
    }
};
```

>**`ranges::count` 的作用**
>统计范围中某个值的出现次数。此处范围是 `strs[i]`（字符串），统计字符 `'0'` 在其中出现的次数。



### （8）[3489. 零数组变换 IV](https://leetcode.cn/problems/zero-array-transformation-iv/)

> 给你一个长度为 `n` 的整数数组 `nums` 和一个二维数组 `queries` ，其中 `queries[i] = [li, ri, vali]`。
>
> 每个 `queries[i]` 表示以下操作在 `nums` 上执行：
>
> - 从数组 `nums` 中选择范围 `[li, ri]` 内的一个下标子集。
> - 将每个选中下标处的值减去 **正好** `vali`。
>
> **零数组** 是指所有元素都等于 0 的数组。
>
> 返回使得经过前 `k` 个查询（按顺序执行）后，`nums` 转变为 **零数组** 的最小可能 **非负** 值 `k`。如果不存在这样的 `k`，返回 -1。
>
> 数组的 **子集** 是指从数组中选择的一些元素（可能为空）。
>
> 背包问题花样是真的多。

其实这道题目可以抽象为：对于nums数组的每一个元素来说，找到queries数组中哪些条目可以执行到这个元素，然后每个条目选或者不选，使得最终和为当前元素的值，于是这道题目就变成了**分割等和子集的类似题目**。需要记录让每个数都能减为0的值中的最大值，这个最大值才能做到让整个数组都减为0.

- 注意本题要特判一下0的情况，不然有的测试用例过不去（因为0本身是不用操作的）。

代码如下：

```c++
class Solution {
public:
    int minZeroArray(vector<int>& nums, vector<vector<int>>& queries) {
        int n = nums.size();
        int res = 0;
        int m = queries.size();
        for(int i=0;i<n;i++)
        {
            int x = nums[i];
            if(x==0) continue; //对于0来说,并不需要操作
            //从queries数组中找到能对当前元素进行操作的queries下标
            //dp[index][j] = dp[index-1][j] | dp[index-1][j-queries[index][2]]
            //dp[-1][0] = 1;
            vector<int> dp(x+1); //挑选一些query,使得总和为x
            dp[0] = 1;
            for(int index=0;index<m;index++) //每个query
            {
                //需要query对当前值是有效的
                if(queries[index][0]>i || queries[index][1]<i) continue;
                for(int j=x;j>=queries[index][2];j--)
                {
                    dp[j] |= dp[j-queries[index][2]];
                }
                if(dp[x]==1) //说明存在,能够分割,保存最大值,计算nums数组的下一个数是否符合
                {
                    res = max(res, index+1); //+1是因为答案要求的是前多少个，因此是索引值+1
                    break; //看nums数组的下一个数的选择情况
                }
            }
            if(dp[x]==0) return -1; //无法达成,直接提前返回
        }
        return res;
    }
};
```





------



## 2.完全背包

完全背包和0-1背包的区别在于，不再是n个物品，而是n种物品（每种物品可以无限制选择），那么此时的状态转移方程就变为：

```c++
dfs(i,c) = max(dfs(i-1,c), dfs(i, c-w[i])+v[i]); //可以继续考虑当前第i个物品
```

与0-1背包唯一的不同就是是`dfs(i, c-w[i])+v[i])`而不是`dfs(i-1, c-w[i])+v[i])`

以下是例题。

（完全背包在降维的时候，j是从左到右进行遍历的）

### （1）[322. 零钱兑换](https://leetcode.cn/problems/coin-change/)

还是先开一个正常的二维dp来做一下这道题目。题解如下：

```c++
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        //先用正常二维dp看一下, dp[i][j]表示考虑到第i-1个硬币的时候,总和为j的最少硬币个数
        int n = coins.size();
        vector<vector<int>> dp(n+1, vector<int>(amount+1, INT_MAX/2)); //都是正数,初始化为INT_MAX,表示不合法情况，也可以是0x3f3f3f
        dp[0][0] = 0; //不选硬币的时候,总和为0是合法情况,此时"最少的硬币个数"也是0
        //dp[i][j] = min(dp[i-1][j], dp[i][j-nums[i]]+1); //不选,或者选
        //dp[i+1][j] = min(dp[i][j], dp[i+1][j-nums[i]]+1);
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<=amount;j++)
            {
                if(j<coins[i]) dp[i+1][j] = dp[i][j];
                else dp[i+1][j] = min(dp[i][j], dp[i+1][j-coins[i]]+1);//注意这个是i+1
            }
        }
        int res = 0;
        if(dp[n][amount]==(INT_MAX/2)) res = -1;
        else res = dp[n][amount];
        return res;
    }
};
```

接下来，可以降维成一维的情况，注意到状态转移方程为：

```c++
if(j<coins[i]) dp[i+1][j] = dp[i][j];
else dp[i+1][j] = min(dp[i][j], dp[i+1][j-coins[i]]+1);
```

可以发现从左到右遍历并不会出现错误的覆盖问题，因为`j-coins[i]`是第`i+1`行的，本来就是要更新后的结果，所以从左往右遍历是正确的。

> 注意，二维的情况j不能从nums[i]开始更新，因为本行前面的部分初始化为非法值，不会自动更新为本行的内容，而一维的隐式自动继承上一行的值，相当于`if(j<coins[i]) dp[i+1][j] = dp[i][j];`是默认实现的。

此时代码如下：

```c++
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        //先用正常二维dp看一下, dp[i][j]表示考虑到第i-1个硬币的时候,总和为j的最少硬币个数
        int n = coins.size();
        vector<int> dp(amount+1,INT_MAX/2); //都是正数,初始化为INT_MAX,表示不合法情况
        dp[0] = 0; //不选硬币的时候,总和为0是合法情况,此时"最少的硬币个数"也是0
        //dp[i][j] = min(dp[i-1][j], dp[i][j-nums[i]]+1); //不选,或者选
        //dp[i+1][j] = min(dp[i][j], dp[i+1][j-nums[i]]+1);
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<=amount;j++)
            {
                if(j>=coins[i]) dp[j] = min(dp[j], dp[j-coins[i]]+1);
            }
        }
        int res = 0;
        if(dp[amount]==(INT_MAX/2)) res = -1;
        else res = dp[amount];
        return res;
    }
};
```

或者：`int j=coins[i]`开始也可以(相当于其他的部分取了上一次的结果，但是二维的话不可以从这个开始 必须全部赋值)

```C++
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        // dp[i][j] 表示选择到i的coins  能否凑够j的金额 的最少硬币个数
        // dp[i][j] = min(dp[i-1][j] , dp[i][j-coins[i]]);
        //dp[-1][0] = 0
        int n = coins.size();
        vector<int> dp(amount+1,0x3f3f3f);
        dp[0] = 0;
        for(int i=0;i<n;i++)
        {
            for(int j=coins[i];j<=amount;j++)
            {
                dp[j] = min(dp[j-coins[i]]+1,dp[j]);
            }
        }
        return dp[amount]==0x3f3f3f?-1:dp[amount];
    }
};
```



### （2）[518. 零钱兑换 II](https://leetcode.cn/problems/coin-change-ii/)

跟上一道题目是类似的，不过变成了求解总的方案数。代码如下：

> 注意这道题目中间结果可能会爆INT上限，在之前的题目也有遇到过这种问题，即最终求解的结果不会达到INT上限，但中间结果可能会达到。可以把dp数组设置为unigned long long来规避这个问题（比较推荐），之前还有题目会剪枝掉越界的中间结果（毕竟既然保证最终结果不越界，不可能是从中间结果推过来的），**但这样做感觉会破坏代码的鲁棒性，感觉还是先用unsigned long long看一下，不行再剪枝吧。**

```c++
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<unsigned long long> dp(amount+1, 0);
        dp[0] = 1;
        int n = coins.size();
        for(int i=0;i<n;i++)
        {
            for(int j=coins[i];j<=amount;j++)
            {
                dp[j] += dp[j-coins[i]];
            }
        }
        return dp[amount];
    }
};
```

如果不用ll：

```C++
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        //dp[i][j] 表示到i的coins 能凑齐金额为j的 组合数
        //dp[i][j] = dp[i-1][j] + dp[i][j-coins[i]]
        //dp[-1][0] = 1;
        int n = coins.size();
        vector<int> dp(amount+1,0);
        dp[0]=1;
        for(int i=0;i<n;i++)
        {
            for(int j=coins[i];j<=amount;j++)
            {
                if(dp[j]>INT_MAX-dp[j-coins[i]])break;//题目说“保证结果符合 32 位带符号整数。”那么超过的后面一定不会用，直接剪枝
                dp[j] = dp[j]+dp[j-coins[i]];
            }
        }
        return dp[amount];
    }
};
```

​	

### （3）[279. 完全平方数](https://leetcode.cn/problems/perfect-squares/)（HOT 100） :fire:

> 给你一个整数 `n` ，返回 *和为 `n` 的完全平方数的最少数量* 。
>
> **完全平方数** 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，`1`、`4`、`9` 和 `16` 都是完全平方数，而 `3` 和 `11` 不是。
>
>  
>
> **示例 1：**
>
> ```
> 输入：n = 12
> 输出：3 
> 解释：12 = 4 + 4 + 4
> ```
>
> **示例 2：**
>
> ```
> 输入：n = 13
> 输出：2
> 解释：13 = 4 + 9
> ```
>
>  
>
> **提示：**
>
> - `1 <= n <= 104`

一道HOT 100的题目，代码如下（比较符合完全背包题目的样式）：
```c++
class Solution {
public:
    int numSquares(int n) {
        //相当于背包里面都是1,4,9这样的平方数
        vector<int> dp(n+1, 0x3f3f3f);
        //dp[-1][0] = 0;
        dp[0] = 0;
        //dp[i][j] = min(dp[i-1][j], dp[i][j-nums[i]] + 1);
        int upper = sqrt(n + 1);
        for(int i=1;i<=upper;i++)
        {
            int num = i * i; //背包中的每个物品:1,4,9,...
            for(int j = num;j<=n;j++)
            {
                dp[j] = min(dp[j], dp[j-num] + 1);
            }
        }
        return dp[n];
    }
};
```

Y

```C++
class Solution {
public:
    int numSquares(int n) {
        // 1 4 9 16..
        //dp[i][j] 表示拿到i位，能凑齐结果为j的最少数量
        //dp[i][j] = min(dp[i-1][j],dp[i-1][j-i*i])
        //dp[-1][0] = 0;数量为0

        vector<int> dp(n+1,INT_MAX);
        dp[0]=0; // 数量为0
        for(int i=1;i<=sqrt(n);i++)
        {
            for(int j=i*i;j<=n;j++)
            {
                dp[j] = min(dp[j],dp[j-i*i]+1);
            }
        }
        return dp[n];

    }
};
```



### （4）[1449. 数位成本和为目标值的最大数字](https://leetcode.cn/problems/form-largest-integer-with-digits-that-add-up-to-target/)

给你一个整数数组 `cost` 和一个整数 `target` 。请你返回满足如下规则可以得到的 **最大** 整数：

- 给当前结果添加一个数位（`i + 1`）的成本为 `cost[i]` （`cost` 数组下标从 0 开始）。
- 总成本必须恰好等于 `target` 。
- 添加的数位中没有数字 0 。

由于答案可能会很大，请你以字符串形式返回。

如果按照上述要求无法得到任何整数，请你返回 "0" 。

举例：

> **示例 1：**
>
> ```
> 输入：cost = [4,3,2,5,6,7,2,5,5], target = 9
> 输出："7772"
> 解释：添加数位 '7' 的成本为 2 ，添加数位 '2' 的成本为 3 。所以 "7772" 的代价为 2*3+ 3*1 = 9 。 "977" 也是满足要求的数字，但 "7772" 是较大的数字。
>  数字     成本
>   1  ->   4
>   2  ->   3
>   3  ->   2
>   4  ->   5
>   5  ->   6
>   6  ->   7
>   7  ->   2
>   8  ->   5
>   9  ->   5
> ```
>
> **示例 2：**
>
> ```
> 输入：cost = [7,6,5,5,5,6,8,7,8], target = 12
> 输出："85"
> 解释：添加数位 '8' 的成本是 7 ，添加数位 '5' 的成本是 5 。"85" 的成本为 7 + 5 = 12 。
> ```
>
> **示例 3：**
>
> ```
> 输入：cost = [2,4,6,2,4,6,4,4,4], target = 5
> 输出："0"
> 解释：总成本是 target 的条件下，无法生成任何整数。
> ```
>
> **示例 4：**
>
> ```
> 输入：cost = [6,10,15,40,40,40,40,40,40], target = 47
> 输出："32211"
> ```

看到总成本必须恰好等于target，可以思考用背包模型来做。注意到对于构造出来的数，要先保证尽可能地“长”，在某一个长度下，则保证字典序是倒序的，即为最大值。而第一步保证结果尽可能地长，就是完全背包模型（每个值可以选无数次）。

- 本题主要的难点在于，如何根据最多选择的长度（用完全背包即可求解）构造出来这个字符串。转移方程为`dp[i+1][j] = max(dp[i][j], dp[i+1][j-cost[i]]+1)`。最后的状态为`dp[n][target]`，只要判断一下其是通过哪个状态转移过来的，即可重建出来最后的字符串（并且该字符串就是最大的，因为从最后一位开始遍历的）。

代码如下：

```c++
class Solution {
public:
    string largestNumber(vector<int>& cost, int target) {
        //成本恰好等于target:联想到背包
        //相当于选一些数,使得总和为target,且对应的数值最大.相当于选最多位的数,并且把选出来的数按照字典序从大到小排列
        int n = cost.size();
        vector<vector<int>> dp(n+1, vector<int>(target+1, -0x3f3f3f));
        dp[0][0] = 0; //唯一的合法态,长度为0,注意dp数组往后挪了一位(本来是dp[-1][0]=0),题目要求成本恰好为target,意味着背包正好装满
        for(int i=0;i<n;i++) //完全背包
        {
            for(int j=0;j<=target;j++)
            {
                if(j>=cost[i])
                    dp[i+1][j] = max(dp[i][j], dp[i+1][j-cost[i]]+1);
                else dp[i+1][j] = dp[i][j]; //别忘了对于二维来说要分类讨论!不然对于j<cost[i]的部分,就没办法得到更新了
            }
        }
        int maxLength = dp[n][target];
        //cout<<maxLength<<endl;
        //倒着推回去,看看是从哪个状态来的
        string res = "";
        int i = n; //从最后一个往前推
        int x = target;
        while(x && i>0)
        {
            if((x-cost[i-1]>=0) && dp[i][x]==dp[i][x-cost[i-1]]+1) //说明是从加某个数字转移过来的
            {
                res += to_string(i);
                x -= cost[i-1];
            }
            else i--;
        }
        if(x!=0 || res=="") return "0"; //剩余不是0,或者没有进上面的while循环,则返回"0",表示无法达成
        return res;

    }
};
```

其实看状态转移的过程，和最终复原的过程，本题依旧是可以把完全背包降维成一维的，但最近没怎么写原本二维的背包版本，导致在状态转移的时候没有分类讨论，debug了非常久（降为一维的话，不需要考虑`else dp[i+1][j] = dp[i][j]`，因为默认`dp[i+1][j]=dp[i][j]`）。这里就不贴一维的版本了，后面重复做这题的时候再补充吧。

> 注：后面可以看这个系列的背包教程：[1449. 数位成本和为目标值的最大数字 - 力扣（LeetCode）](https://leetcode.cn/problems/form-largest-integer-with-digits-that-add-up-to-target/solutions/824611/gong-shui-san-xie-fen-liang-bu-kao-lu-we-uy4y/)，可能也会有新的收获。



Y： 也可以写作上下保持一致的写法：

```C++
class Solution {
public:
    string largestNumber(vector<int>& cost, int target) {
        //dp[i][j] 表示用到i的cost ，能够凑成target 的最多位的情况
        //dp[i][j] = max(dp[i-1][j],d[i][j-cost[i]])
        //dp[-1][0] 0
        // vector<int> dp(target+1,INT_MIN);
        int n = cost.size();
        vector<vector<int>> dp(n + 1, vector<int>(target + 1, INT_MIN));
        dp[0][0] = 0;//dp[i][0]=0

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j <= target; j++)
            {
                if (j >= cost[i])
                    dp[i + 1][j] = max(dp[i][j], dp[i + 1][j - cost[i]] + 1);
                else
                    dp[i + 1][j] = dp[i][j];
            }
        }
        if (dp[n][target] <= 0)return "0";
        string res;
        int j = target;

        for (int i = n - 1; i >= 0;)
        {
            //if (dp[i + 1][j] != dp[i][j])错误
            if(j - cost[i]>=0 && dp[i + 1][j] == dp[i + 1][j - cost[i]] + 1)
            {
                j -= cost[i];
                res += to_string(i+1);
            }
            else
            {
                i--;
            }
        }
        return res;

    }
};
```



注意：

>```C++
>for (int i = n - 1; i >= 0;)
>{
>if ((j - cost[i] >= 0) && dp[i+1][j] == dp[i][j - cost[i]] + 1) //说明是从加某个数字转移过来的
>//if (dp[i + 1][j] != dp[i][j]) // 错误 ❌
>{
>   res += to_string(i+1);
>   j -= cost[i];
>}
>else i--;
>}
>```
>
>不可以写作`if (dp[i + 1][j] != dp[i][j]) // 错误 ❌`的原因是：
>
>---
>### 反例分析
>假设 `cost = [5, 5]`，`target = 5`。数字 1 和 2 的 cost 均为 5。正确结果应为 `"2"`（数字 2 更大），但你的代码会错误地生成 `"1"`。
>
>#### 动态规划过程
>1. **初始化**：`dp[0][0] = 0`，其余 `dp[0][j] = INT_MIN`。
>2. **处理数字 1（i=0）**：
>  - `j=5` 时，`dp[1][5] = dp[0][5 - 5] + 1 = 1`。
>3. **处理数字 2（i=1）**：
>  - `j=5` 时，`dp[2][5] = max(dp[1][5], dp[2][5 - 5] + 1) = max(1, 1) = 1`。
>
>#### 构造结果字符串的流程
>1. **初始状态**：`j = 5`，从数字 2（i=1）开始。
>
>2. **判断条件**：`dp[2][5] != dp[1][5]` → `1 != 1` → **False**。  即使这两个相等 并不意味着我没选择  因为这个dp我们表示的是位数 ，中间状态
>
>    打家劫舍是金钱数，只会递增， dp里都是保存最终的状态。
>  - 跳过数字 2，i 减为 0。
>3. **处理数字 1（i=0）**：
>  - `dp[1][5] != dp[0][5]` → `1 != INT_MIN` → **True**。
>  - 选择数字 1，最终结果为 `"1"`。
>
>显然，原始条件未能正确识别到数字 2 的转移路径，导致错误。
>
>---
>### 正确逻辑
>正确的判断条件应验证当前状态是否由选择当前数字转移而来，即：
>```cpp
>if (j >= cost[i] && dp[i+1][j] == dp[i][j - cost[i]] + 1)
>```
>这确保了只有当 `dp[i+1][j]` 的值是通过选择当前数字 `i+1` 达到时，才将其加入结果。
>
>
>
>1. **条件判断**：通过 `dp[i+1][j] == dp[i][j - cost[i]] + 1` 确保当前状态是通过选择当前数字转移而来。
>2. **贪心选择**：从高位到低位遍历，优先选择较大的数字以保证结果的最大性。
>
>这样修改后，代码能够正确识别转移路径并构造出符合要求的最大数字。



## 3.多重背包

物品可以重复选，有个数限制。

### 求方案数

### （1）[2585. 获得分数的方法数](https://leetcode.cn/problems/number-of-ways-to-earn-points/)

> 考试中有 `n` 种类型的题目。给你一个整数 `target` 和一个下标从 **0** 开始的二维整数数组 `types` ，其中 `types[i] = [counti, marksi] `表示第 `i` 种类型的题目有 `counti` 道，每道题目对应 `marksi` 分。
>
> 返回你在考试中恰好得到 `target` 分的方法数。由于答案可能很大，结果需要对 `109 +7` 取余。
>
> **注意**，同类型题目无法区分。
>
> - 比如说，如果有 `3` 道同类型题目，那么解答第 `1` 和第 `2` 道题目与解答第 `1` 和第 `3` 道题目或者第 `2` 和第 `3` 道题目是相同的。
>
>  
>
> **示例 1：**
>
> ```
> 输入：target = 6, types = [[6,1],[3,2],[2,3]]
> 输出：7
> 解释：要获得 6 分，你可以选择以下七种方法之一：
> - 解决 6 道第 0 种类型的题目：1 + 1 + 1 + 1 + 1 + 1 = 6
> - 解决 4 道第 0 种类型的题目和 1 道第 1 种类型的题目：1 + 1 + 1 + 1 + 2 = 6
> - 解决 2 道第 0 种类型的题目和 2 道第 1 种类型的题目：1 + 1 + 2 + 2 = 6
> - 解决 3 道第 0 种类型的题目和 1 道第 2 种类型的题目：1 + 1 + 1 + 3 = 6
> - 解决 1 道第 0 种类型的题目、1 道第 1 种类型的题目和 1 道第 2 种类型的题目：1 + 2 + 3 = 6
> - 解决 3 道第 1 种类型的题目：2 + 2 + 2 = 6
> - 解决 2 道第 2 种类型的题目：3 + 3 = 6
> ```
>
> **示例 2：**
>
> ```
> 输入：target = 5, types = [[50,1],[50,2],[50,5]]
> 输出：4
> 解释：要获得 5 分，你可以选择以下四种方法之一：
> - 解决 5 道第 0 种类型的题目：1 + 1 + 1 + 1 + 1 = 5
> - 解决 3 道第 0 种类型的题目和 1 道第 1 种类型的题目：1 + 1 + 1 + 2 = 5
> - 解决 1 道第 0 种类型的题目和 2 道第 1 种类型的题目：1 + 2 + 2 = 5
> - 解决 1 道第 2 种类型的题目：5
> ```
>
> **示例 3：**
>
> ```
> 输入：target = 18, types = [[6,1],[3,2],[2,3]]
> 输出：1
> 解释：只有回答所有题目才能获得 18 分。
> ```

本题可以算作是多重背包的板子题了，每个物品可以重复选，但是有个数限制。多重背包的介绍可以看这里：[2585. 获得分数的方法数 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-ways-to-earn-points/solutions/2148313/fen-zu-bei-bao-pythonjavacgo-by-endlessc-ludl/)。

![image-20250329154732494](assets/image-20250329154732494.png)

详细注释版本的代码如下：
```c++
class Solution {
public:
    int waysToReachTarget(int target, vector<vector<int>>& types) {
        const int MOD = 1e9+7;
        //dp[i][j]表示做i道题目,恰好得到j分的总的方案数
        //dp[-1][0] = 1;
        //dp[i][j] += dp[i-1][j-nums[i]*k] (j-nums[i]*k>=0 且k<=count), k从0开始枚举
        //降维到一维的话,k从1开始枚举即可(因为k=0相当于dp[j],上一个状态已经算完了)
        vector<int> dp(target+1);
        dp[0] = 1;
        int n = types.size();
        for(int i=0;i<n;i++)
        {
            int cnt = types[i][0];
            int score = types[i][1];
            //遍历j,按照0-1背包的思路(i依赖于上一行i-1的左侧的部分),所以j倒着遍历
            for(int j=target;j>=0;j--) 
            {
                //k需要满足题意，翻译自上面的推导过程
                for(int k=1;k<=cnt && k<=(j/score);k++)// 【这里k一定要从1开始 👇】
                {
                    dp[j] = (dp[j] + dp[j-score*k])%MOD;
                }
            }
        }
        return dp[target];
    }
};
```



>`for(int k=1;k<=cnt && k<=(j/score);k++)`
>
>1、k一定要从**1**开始
>
>否则的话 当k=0`dp[j] = (dp[j] + dp[j-score*k])%MOD;` 我们发现 它就会变成 `dp[j] = (dp[j] + dp[j]) = 2dp[j]`是错误的
>
>2、这里正反都可以
>
>因为  `dp[j-score*k]`一定会小于j ， 不论k是多少。只要从后到前计算 `dp[j]`，就不会有问题
>
>
>
>当k=1，就是0-1背包.因此写法与0-1背包其实是一样的倒序

## 4.分组背包

同一组内的物品至多/恰好选一个。

### （1）[1155. 掷骰子等于目标和的方法数](https://leetcode.cn/problems/number-of-dice-rolls-with-target-sum/)

> 这里有 `n` 个一样的骰子，每个骰子上都有 `k` 个面，分别标号为 `1` 到 `k` 。
>
> 给定三个整数 `n`、`k` 和 `target`，请返回投掷骰子的所有可能得到的结果（共有 `k^n` 种方式），使得骰子面朝上的数字总和等于 `target`。
>
> 由于答案可能很大，你需要对 `10^9 + 7` **取模**。
>
>  
>
> **示例 1：**
>
> ```
> 输入：n = 1, k = 6, target = 3
> 输出：1
> 解释：你掷了一个有 6 个面的骰子。
> 得到总和为 3 的结果的方式只有一种。
> ```
>
> **示例 2：**
>
> ```
> 输入：n = 2, k = 6, target = 7
> 输出：6
> 解释：你掷了两个骰子，每个骰子有 6 个面。
> 有 6 种方式得到总和为 7 的结果: 1+6, 2+5, 3+4, 4+3, 5+2, 6+1。
> ```
>
> **示例 3：**
>
> ```
> 输入：n = 30, k = 30, target = 500
> 输出：222616187
> 解释：返回的结果必须对 109 + 7 取模。
> ```
>
>  
>
> **提示：**
>
> - `1 <= n, k <= 30`
> - `1 <= target <= 1000`

本题相当于每个骰子是一个组，每组里面选1~k中的一个值，使得总和是target。这种叫做“分组背包”问题。具体的做法可以参考这个链接：[1155. 掷骰子等于目标和的方法数 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-dice-rolls-with-target-sum/solutions/2495836/ji-bai-100cong-ji-yi-hua-sou-suo-dao-di-421ab/)。

#### 方法1：多重背包

本题虽然更像是分组背包的问题，但也可以用多重背包来进行尝试。相当于有n种物品（表示n个骰子），每种物品的大小都是1，且必须选择1~k个（意味着每个骰子必须要roll出一个值）
```c++
class Solution {
public:
    int numRollsToTarget(int n, int k, int target) {
        //用多重背包来做,二维,相当于n种物品,每个物品价值都为1,每种物品会选择1~k个
        //dp[i][j] = sum(dp[i-1][j-m*1]),m>=1 && j-m>=0 && m<=k
        //dp[-1][0] = 1;
        const int MOD = 1e9+7;
        vector<vector<int>> dp(n+1, vector<int>(target+1, 0));
        dp[0][0] = 1;
        for(int i=0;i<n;i++)
        {
            //多重背包,j要从后往前遍历
            for(int j=target;j>=0;j--)
            {
                int sum = 0;
                for(int m=1;m<=j && m<=k; m++)
                {
                    sum = (sum + dp[i][j-m])%MOD;
                }
                dp[i+1][j] = sum;
            }
        }
        return dp[n][target]; 
    }
};
```

用多重背包来做的话，应该也可以用前缀和来进行一些优化，不过以上代码在时间复杂度上可以击败57%，暂时可以先不考虑优化问题了。



#### ==方法2：分组背包（未看完，感觉不优化的话思路跟多重背包基本一致？）==

用分组背包思考这道题的解法如下：[1155. 掷骰子等于目标和的方法数 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-dice-rolls-with-target-sum/solutions/2495836/ji-bai-100cong-ji-yi-hua-sou-suo-dao-di-421ab/)。

> 等到后面底力上来了再做相关背包的补充吧。



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

# 五、划分型 DP

## §5.1 判定能否划分
一般定义 f[i] 表示长为 i 的前缀 a[:i] 能否划分。

枚举最后一个子数组的左端点 L，从 f[L] 转移到 f[i]，并考虑 a[L:i] 是否满足要求。

### [2369. 检查数组是否存在有效划分](https://leetcode.cn/problems/check-if-there-is-a-valid-partition-for-the-array/)

给你一个下标从 **0** 开始的整数数组 `nums` ，你必须将数组划分为一个或多个 **连续** 子数组。

如果获得的这些子数组中每个都能满足下述条件 **之一** ，则可以称其为数组的一种 **有效** 划分：

1. 子数组 **恰** 由 `2` 个相等元素组成，例如，子数组 `[2,2]` 。
2. 子数组 **恰** 由 `3` 个相等元素组成，例如，子数组 `[4,4,4]` 。
3. 子数组 **恰** 由 `3` 个连续递增元素组成，并且相邻元素之间的差值为 `1` 。例如，子数组 `[3,4,5]` ，但是子数组 `[1,3,5]` 不符合要求。

如果数组 **至少** 存在一种有效划分，返回 `true` ，否则，返回 `false` 。

**示例 1：**

```
输入：nums = [4,4,4,5,6]
输出：true
解释：数组可以划分成子数组 [4,4] 和 [4,5,6] 。
这是一种有效划分，所以返回 true 。
```



https://leetcode.cn/problems/check-if-there-is-a-valid-partition-for-the-array/solutions/1728735/by-endlesscheng-8y73/

![image-20250408154935344](assets/image-20250408154935344.png)

```C++
class Solution {
public:
    //10 ++ 12+
    bool validPartition(vector<int>& nums) {
        //dp[i] |= 
        //same dp[i-2]
        //same dp[i-3]
        //递增 dp[i-3] 
        int n = nums.size();
        vector<int> dp(n+1,0);
        dp[0] = 1;
        //4 4 4 5 6 
        for(int i=1;i<n;i++)
        {
            if(nums[i]==nums[i-1])
            {
                dp[i+1] |= dp[i-1];
                if(i-2>=0)
                {
                    if(nums[i-1]==nums[i-2])
                        dp[i+1] |= dp[i-2];// dp[i] |= dp[i-3];
                }
            }
            if(i-2>=0)
            {
                if(nums[i] == nums[i-1]+1&&nums[i-1]==nums[i-2]+1)
                {
                    //dp[i]|=dp[i-3]
                    dp[i+1]|= dp[i-2];
                }
            }
        }
        return dp[n];
    }
};
```

or

```C++
class Solution {
public:
    //10 ++ 12+
    bool validPartition(vector<int>& nums) {
        //dp[i] |= 
        //same dp[i-2]
        //same dp[i-3]
        //递增 dp[i-3] 
        int n = nums.size();
        vector<int> dp(n+1,0);
        dp[0] = 1;
        //4 4 4 5 6 
        for(int i=1;i<n;i++)
        {
            if(
            (dp[i-1]&&nums[i]==nums[i-1]) ||
            (i-2>=0&& dp[i-2]&& ((nums[i-1]==nums[i-2])||
                                (nums[i] == nums[i-1]+1&&nums[i-1]==nums[i-2]+1)))
            )
            {
                dp[i+1] = 1;
            }
        }
        return dp[n];
    }
};
```

OR:

```C++
class Solution {
public:
    bool validPartition(vector<int>& nums) {
        // dp[i] 
        // nums[i] == nums[i-1]&&dp[i-2]  dp[i] = 1
        // i>=3&&nums[i-1] == nums[i-2]&&dp[i-3] dp[i]=1
        // i>=3&&nums[i]==nums[i-1]+1&&.. &&dp[i-3] dp[i]=1

        // dp[-1] = 1
        int n = nums.size();
        vector<int> dp(n+1,0);
        dp[0]=1;
        for(int i=1;i<n ;i++)
        {
            bool flag1 = (dp[i-1]&&nums[i]==nums[i-1]);
            bool flag2 = (i>=2&&dp[i-2]&&(nums[i]==nums[i-1])&&(nums[i-1]==nums[i-2]));
            bool flag3 = (i>=2&&dp[i-2]&&(nums[i]==nums[i-1]+1)&&(nums[i-1]==nums[i-2]+1));
            if(flag1||flag2||flag3)dp[i+1] = 1;
        }
        return dp[n];
    }
};
```



### [139. 单词拆分](https://leetcode.cn/problems/word-break/)

给你一个字符串 `s` 和一个字符串列表 `wordDict` 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 `s` 则返回 `true`。

**注意：**不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

 

**示例 1：**

```
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
```



https://leetcode.cn/problems/word-break/

![image-20250408162618171](assets/image-20250408162618171.png)

```C++
class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> uset(wordDict.begin(),wordDict.end());
        int max_len = ranges::max(wordDict,{},&string::length).length();
        int sn = s.size();
        int wn = wordDict.size();
        vector<int> dp(sn+1,0);
        dp[0]=1;
        for(int i=0;i<=sn;i++)
        {
            for(int j=i-1;j>=max(i-max_len,0);j--)//j-i 如果超过了最大字符 直接结束 [max!!]
            {
                if(dp[j]&&uset.contains(s.substr(j,i-j)))
                {
                    dp[i] = dp[j];
                    break; //有一个符合要求的就可以提前推出了      
                }
            }
        }
        return dp[sn];
    }
};
```

>1、`dp[i]`表示前i个，genshinImpactGood，
>
>```
>genshin I mpact G ood
>	  ( j )   ( i )
>```
>
>2、
>
>`int max_len = ranges::max(wordDict, {}, &string::length).length();` 
>
>使用了C++20的Ranges库语法，其作用是计算`wordDict`中最长字符串的长度。
>
>- **`&string::length`**：投影函数（Projection），对每个元素调用`length()`方法，取其返回值进行比较。
>
>忘了的话正常写也一样：
>
>```C++
>//int max_len = ranges::max(wordDict,{},&string::length).length();
>int max_len = 0;
>for (const auto& word : wordDict) 
>{
>   if (word.length() > max_len) 
>   {
>       max_len = word.length();
>   }
>}
>```



## §5.2 最优划分
计算最少（最多）可以划分出多少段、最优划分得分等。

一般定义 f[i] 表示长为 i 的前缀 a[:i] 在题目约束下，分割出的最少（最多）子数组个数（或者定义成分割方案数）。

枚举最后一个子数组的左端点 L，从 f[L] 转移到 f[i]，并考虑 a[L:i] 对最优解的影响。



### [132. 分割回文串 II](https://leetcode.cn/problems/palindrome-partitioning-ii/)

困难

给你一个字符串 `s`，请你将 `s` 分割成一些子串，使每个子串都是回文串。

返回符合要求的 **最少分割次数** 。

**示例 1：**

```
输入：s = "aab"
输出：1
解释：只需一次分割就可将 s 分割成 ["aa","b"] 这样两个回文子串。
```

#### 优化前

```C++
class Solution {
public:
    int minCut(string s) 
    {
        //dp[i] 最少分割次数
        //某区间是回文串，dp[i] = min(dp[i],dp[i-len]+1)
        int n = s.size();
        vector<int> dp(n+1,0);//dp[0]=0 dp[1] = 1 dp[2]=2
        ranges::iota(dp,0);
        //a a b
        auto isPalindrome = [&](int left,int right)->bool
        {
            while(left<right)
            {
                if(s[left]!=s[right])
                    return false;
                left++;
                right--;
            }
            return true;
        };
        for(int i=0;i<n;i++) // i 是右边界
        {
            for(int j=0;j<=i;j++)// j 是左边界
            {
                if(isPalindrome(j,i))// 检查 s[j:i] 是否是回文
                {
                    dp[i+1] = min(dp[i+1],dp[j]+1);// 更新 dp[i + 1]
                }
            }
        }
        return dp[n]-1;// 返回最小切割次数
    }
};

```

#### 优化后1

```C++
class Solution {
public:
    int minCut(string s) 
    {
        //dp[i] 最少分割次数
        //某区间是回文串，dp[i] = min(dp[i],dp[i-len]+1)
        int n = s.size();
        vector<int> dp(n+1,INT_MAX);//dp[0]=0 dp[1] = 1 dp[2]=2
        dp[0]=-1;
        dp[1]=0;// 单个字母 a/ b/  // 这个不用也行
        //a a b a v v a
        //a a b a v v*a+
        //a a b a v*v+a
        //a a b a*v v a+
        vector<vector<int>> isPalindrome(n,vector<int>(n,true));
        for(int l = n-2;l>=0;l--)
        {
            for(int r = l+1;r<n;r++)
            {
                isPalindrome[l][r] = (s[l]==s[r]&&isPalindrome[l+1][r-1]);
            }
        }
        for(int r=0;r<n;r++) // r 是右边界
        {
            for(int l=0;l<=r;l++)// l 是左边界
            {
                if(isPalindrome[l][r])// 检查 s[l:r] 是否是回文
                {
                    dp[r+1] = min(dp[r+1],dp[l]+1);// 更新 dp[r + 1]
                }
            }
        }
        return dp[n];// 返回最小切割次数
    }
};
```

n不加1版本：dp[i] 表示以下标i为结尾的 推荐！

https://leetcode.cn/problems/palindrome-partitioning-ii/solutions/3588633/jiao-ni-yi-bu-bu-si-kao-dpcong-ji-yi-hua-bnlb/

```C++
class Solution {
public:
    int minCut(string s) 
    {
        //dp[i] 最少分割次数
        //某区间是回文串，dp[i] = min(dp[i],dp[i-len]+1)
        int n = s.size();
        vector<int> dp(n,0);//dp[0]=0 dp[1] = 1 dp[2]=2
        //ranges::iota(dp,0);//改
        //a a b a v v a
        //a a b a v v*a+
        //a a b a v*v+a
        //a a b a*v v a+
        vector<vector<int>> isPalindrome(n,vector<int>(n,true));
        for(int l = n-2;l>=0;l--)
        {
            for(int r = l+1;r<n;r++)
            {
                isPalindrome[l][r] = (s[l]==s[r]&&isPalindrome[l+1][r-1]);
            }
        }
        for(int r=0;r<n;r++) // r 是右边界
        {
            if(isPalindrome[0][r])continue;// 已是回文串，无需分割(不加1版本需要特判 否则l<0)
            int res = INT_MAX;//改
            for(int l=1;l<=r;l++)// l 是左边界
            {
                if(isPalindrome[l][r])// 检查 s[l:r] 是否是回文
                {
                    res = min(res,dp[l-1]+1);// 更新 dp[r + 1] //改
                }
            }
            dp[r] = res;//改
        }
        return dp[n-1];// 返回最小切割次数 //改
    }
};
```





# 十、数位 DP

[数位 DP v1.0 模板讲解](https://leetcode.cn/link/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1rS4y1s721%2F%3Ft%3D19m36s)

[数位 DP v2.0 模板讲解](https://leetcode.cn/link/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1Fg4y1Q7wv%2F%3Ft%3D31m28s) 上下界数位 DP



### [2719. 统计整数数目](https://leetcode.cn/problems/count-of-integers/)

给你两个数字字符串 `num1` 和 `num2` ，以及两个整数 `max_sum` 和 `min_sum` 。如果一个整数 `x` 满足以下条件，我们称它是一个好整数：

- `num1 <= x <= num2`
- `min_sum <= digit_sum(x) <= max_sum`.

请你返回好整数的数目。答案可能很大，请返回答案对 `109 + 7` 取余后的结果。

注意，`digit_sum(x)` 表示 `x` 各位数字之和。

**示例 1：**

```c++
输入：num1 = "1", num2 = "12", min_num = 1, max_num = 8
输出：11
解释：总共有 11 个整数的数位和在 1 到 8 之间，分别是 1,2,3,4,5,6,7,8,10,11 和 12 。所以我们返回 11 。
```



把问题拆分成：

计算 ≤num 2  的好整数个数，记作 a。
计算 ≤num 1 −1 的好整数个数，记作 b。
那么答案就是 a−b。



考虑（<=nums2 的 ) ➖减去  （<=nums1的) ➕（==nums1的）



#### v1.0 

```C++
class Solution {
    const int MOD = 1e9 + 7;
    //计算 ≤numStr（上界） 的好整数个数  //好整数 min_sum <= sum(x) <= max_sum.
    int calc(string& s, int min_sum, int max_sum)
    {
        int n = s.size();
        vector<vector<int>> memo(n, vector<int>(min(9 * n, max_sum) + 1, -1));
        auto dfs = [&](this auto&& self,int i,int sum,bool is_limit)->int
        {
            if (sum > max_sum)  // 非法
                return 0;
            if (i == n)
                return sum >= min_sum ? 1 : 0;
            //返回记忆化的
            if (!is_limit && memo[i][sum] != -1)
                return memo[i][sum];
            int up = is_limit ? s[i] - '0' : 9;
            int res = 0;
            for (int d = 0; d <= up; d++)
            {
                res = (res + self(i + 1, sum + d, is_limit && d == up)) % MOD;
            }
            if (!is_limit)
                memo[i][sum] = res;
            return res;
        };
        return dfs(0, 0, true);
    }
public:
    int count(string num1, string num2, int min_sum, int max_sum) {
        int ans = calc(num2, min_sum, max_sum) - calc(num1, min_sum, max_sum) + MOD; // 避免负数
        int sum = 0;
        for (char c : num1)
        {
            sum += (c - '0');
        }
        ans += (sum >= min_sum && sum <= max_sum);
        return ans % MOD;
    }
};
```



注释版本：

1、return

2、可返回记忆化

3、继续dfs

​		3.1、up

​		...

```cpp
class Solution {
    const int MOD = 1e9 + 7;  // 模数，用于结果取模

    // 计算 ≤numStr 的好整数个数（数位和介于[min_sum, max_sum]）
    int calc(string& s, int min_sum, int max_sum) 
    {
        int n = s.size();
        // memo[i][sum] 表示处理到第i位，当前和为sum时的记忆化结果
        // 第二维大小优化：sum最多为 min(9*n, max_sum)，+1是因为包含0到该值的所有可能
        vector<vector<int>> memo(n, vector<int>(min(9 * n, max_sum) + 1, -1));
        
        // 递归函数：数位DP核心
        // 参数：当前位i，当前和sum，是否受上限约束is_limit
        auto dfs = [&](this auto&& self, int i, int sum, bool is_limit) -> int 
        {
            if (sum > max_sum) return 0;  // 当前和超过max_sum，直接剪枝
            if (i == n) return sum >= min_sum ? 1 : 0;  // 所有位处理完毕，检查sum是否≥min_sum
            
            // 若不受限且已记忆化，直接返回结果（注意：受限状态无法复用，故不记忆化）
            if (!is_limit && memo[i][sum] != -1) return memo[i][sum];
            
            int up = is_limit ? s[i] - '0' : 9;  // 当前位的最大值（受限则为s[i]，否则为9）
            int res = 0;
            for (int d = 0; d <= up; d++) // 枚举当前位的所有可能数字
            {  
                // 递归到下一位，更新sum和is_limit状态（若当前位选到上限且d==up，则下一位仍受限）
                res = (res + self(i + 1, sum + d, is_limit && d == up)) % MOD;
            }
            
            if (!is_limit) memo[i][sum] = res;  // 仅记忆化非受限状态的结果
            return res;
        };
        
        return dfs(0, 0, true);  // 从第0位开始，初始和为0，受限于上限 。 is_limit是true可以保证第一位不乱选
    }

public:
    int count(string num1, string num2, int min_sum, int max_sum) 
    {
        // 计算[num1, num2]内的好整数数 = calc(num2) - calc(num1) + (num1是否合法)
        int ans = (calc(num2, min_sum, max_sum) - calc(num1, min_sum, max_sum) + MOD) % MOD;//【 + MOD！👇】
        // 单独检查num1是否合法
        int sum = 0;
        for (char c : num1) sum += (c - '0');
        if (sum >= min_sum && sum <= max_sum) ans = (ans + 1) % MOD;
        return ans;
    }
};
```

>`int ans = (calc(num2, min_sum, max_sum) - calc(num1, min_sum, max_sum) + MOD) % MOD;//【 + MOD！👇】`
>
>注意这里一定要 **+MOD**
>
>因为calc(num2, min_sum, max_sum) 返回的是MOD返回的，
>
>所以可能会导致 `calc(num2, min_sum, max_sum) < calc(num1, min_sum, max_sum)`是负数



```c++
// 上界5555
// 14  
// 22 [14 22 可记忆化]
// 55
// 19 [55 19不可记忆化]
```



**关于 `min(9 * n, max_sum) + 1, -1)` 的解释：**

- **`min(9 * n, max_sum)`**：当前处理数字的位数为 `n`，每位最大为9，因此数位和的最大可能值为 `9 * n`。但题目要求数位和不超过 `max_sum`，因此当 `max_sum < 9 * n` 时，超过 `max_sum` 的和无意义，可直接剪枝。取两者的最小值是为了优化记忆化数组的空间，避免存储无效状态。
  
- **`+1`**：因为数位和的取值范围是 `[0, min(9 * n, max_sum)]`，共有 `min(9 * n, max_sum) + 1` 个可能值，所以需要 `+1` 来包含所有情况。

- **`-1`**：初始化记忆化数组的默认值为-1，表示该状态未被计算过。



关于语法：

>##### 三种递归lambda实现方式
>
>1 `std::function`（类型明确）
>
>```C++
>function<int(int, int, bool)> dfs = [&](int i, int sum, bool is_limit) -> int 
>{
>    // ... 递归调用直接使用 dfs(i+1, ...)
>     dfs(i+1, sum+d, ...);
>};
>return dfs(0, 0, true); // 
>```
>
>2 泛型lambda + 显式传递自身（通用模板）
>
>```C++
>auto dfs = [&](auto&& self, int i, int sum, bool is_limit) -> int 
>{
>    // 递归调用时传递 self 自身
>    self(self, i+1, sum+d, ...); // ✅
>};
>return dfs(dfs, 0, 0, true); // ✅ 初始调用仍用 dfs（见下方解释）
>```
>
>2 C++23显式对象参数（`this auto&&`）
>
>```C++
>auto dfs = [&](this auto&& self,int i,int sum,bool is_limit)->int
>{
>    self(i+1, sum+d, ...); // self
>};
>return dfs(0, 0, true); // 
>```
>
>
>
>具体涉及到auto，function等的语法可以看 D:\PGPostgraduate\githubNotePrepareForWork\PrepareForWorkNotes\Algos\Leetcode\C++ 特殊语法 C++ 新特性 刷题时候遇到的.md



#### v2.0 推荐

```C++
class Solution {
public:
    //10 ++
    int count(string num1, string num2, int min_sum, int max_sum) {
        //1001  8888
        //20 30
        //12*
        //30*
        //i,sum
        int MOD = 1e9+7;
        int n = num2.size();
        int m = num2[0]-'0'+(n-1)*9;
        num1 = string(n-num1.size(),'0')+num1;//【补前导0!!!】
        vector<vector<int>> dp(n,vector<int>(m,-1));
        auto dfs = [&](this auto&&dfs,int i,int sum,bool low_limit,bool high_limit)->int
        {
            if(sum>max_sum)return 0;
            if(i==n) return (sum>=min_sum);
            if(!high_limit&&!low_limit&&dp[i][sum]!=-1)return dp[i][sum];

            int hi = high_limit? num2[i]-'0':9;
            int lo = low_limit?num1[i]-'0':0;
            int res=0;
            for(int d=lo;d<=hi;d++)
            {
                res = (res+dfs(i+1,sum+d,low_limit&&d==lo,high_limit&&d==hi))%MOD;
            }
            if(!high_limit&&!low_limit)dp[i][sum] = res;
            return res%MOD;
        };
        return dfs(0,0,true,true);
    }
};
```



### [788. 旋转数字](https://leetcode.cn/problems/rotated-digits/)

我们称一个数 X 为好数, 如果它的每位数字逐个地被旋转 180 度后，我们仍可以得到一个有效的，且和 X 不同的数。要求每位数字都要被旋转。

如果一个数的每位数字被旋转以后仍然还是一个数字， 则这个数是有效的。0, 1, 和 8 被旋转后仍然是它们自己；2 和 5 可以互相旋转成对方（在这种情况下，它们以不同的方向旋转，换句话说，2 和 5 互为镜像）；6 和 9 同理，除了这些以外其他的数字旋转以后都不再是有效的数字。

现在我们有一个正整数 `N`, 计算从 `1` 到 `N` 中有多少个数 X 是好数？

**示例：**

```
输入: 10
输出: 4
解释: 
在[1, 10]中有四个好数： 2, 5, 6, 9。
注意 1 和 10 不是好数, 因为他们在旋转之后不变。
```



V1.0

```C++
int diffs[10]  = {0,0,1,-1,-1,1,1,-1,0,1};
                //0 1 2  3  4 5 6  7 8 9 
class Solution {
public:
    int rotatedDigits(int n) {
        // 0 1 8 （a=0）
        // 2 - 5 ， 6 - 9 （b=1）
        // 3 4 7 （c=-1）

        //有数字是b=1类  可
        //有数字是c=-1类 不可 退出

        // 1a 2b 
        // 8a 6b 其实这两后面的情况是一样的 可以记忆化搜索 
        string s = to_string(n);
        int m = s.size();
        vector<vector<int>> dp(m,vector<int>(2,-1));//有diff和没有diff的情况
        auto dfs = [&](this auto &&dfs,int i,bool has_diff,bool is_limit)->int
        {
            if(i==m) return has_diff;// 只有包含 2/5/6/9 才算一个好数
            if(!is_limit&&dp[i][has_diff]!=-1) return dp[i][has_diff];
            int up = is_limit?(s[i]-'0'):9;
            int res=0;
            for(int d=0;d<=up;d++)// 枚举要填入的数字 d
            {
                if(diffs[d]!=-1)//不是3 4 7
                {
                    res+= dfs(i+1,has_diff||diffs[d],is_limit&&d==up);//进入i+1
                }
            }
            if(!is_limit) dp[i][has_diff] = res;
            return res;
        };
        return dfs(0,false,true);//
    }
};
```

https://leetcode.cn/problems/rotated-digits/

<img src="assets/image-20250331212952884.png" alt="image-20250331212952884" style="zoom: 80%;" />

<img src="assets/image-20250331213001008.png" alt="image-20250331213001008" style="zoom:80%;" />



### [902. 最大为 N 的数字组合](https://leetcode.cn/problems/numbers-at-most-n-given-digit-set/)

给定一个按 **非递减顺序** 排列的数字数组 `digits` 。你可以用任意次数 `digits[i]` 来写的数字。例如，如果 `digits = ['1','3','5']`，我们可以写数字，如 `'13'`, `'551'`, 和 `'1351315'`。

返回 *可以生成的小于或等于给定整数 `n` 的正整数的个数* 。

**示例 1：**

```
输入：digits = ["1","3","5","7"], n = 100
输出：20
解释：
可写出的 20 个数字是：
1, 3, 5, 7, 11, 13, 15, 17, 31, 33, 35, 37, 51, 53, 55, 57, 71, 73, 75, 77.
```



增加`isNum`

```C++
class Solution {
public://10min内 自己 +1贴
    int atMostNGivenDigitSet(vector<string>& digits, int n)
    {
        string s = to_string(n);//将 n 转换成字符串 s
        int m = s.size();
        //i  , is_limit, is_num->中间不可以有看空缺的0 因为这个吧？
        vector<int> dp(m, -1);
        //定义 dp(i,isLimit,isNum) 表示构造从左往右第 i 位及其之后数位的合法方案数
        auto dfs = [&](this auto&& dfs, int i, bool is_limit, bool is_num)->int
        {
            if (i == m)return is_num;
            if (!is_limit && is_num && dp[i] != -1)return dp[i];// [is_num ]
            int res = 0;
            if (!is_num)
            {
                res = dfs(i + 1, false, false);
            }
            char up = is_limit ? s[i] : '9';
            for (int d = 0; d < digits.size(); d++)
            {
                if (digits[d][0] > up)break;
                res += dfs(i + 1, is_limit && digits[d][0] == up, true);
            }
            if (!is_limit && is_num) dp[i] = res;
            return res;
        };
        return dfs(0, true, false);
    }
};
```



链接：https://leetcode.cn/problems/numbers-at-most-n-given-digit-set/solutions/1900101/shu-wei-dp-tong-yong-mo-ban-xiang-xi-zhu-e5dg/

`isNum` 表示` i `前面的数位是否填了数字。

若为假，则当前位可以跳过（不填数字），或者要填入的数字至少为 1；

若为真，则必须填数字，且要填入的数字从 0 开始。

这样我们可以控制构造出的是一位数/两位数/三位数等等。对于本题而言，要填入的数字可直接从 `digits `中选择。

m不可以没有的原因可能包含，中间不可以有看空缺的0 ，没有isNum就没办法构造某一位不填的现象

![image-20250331215836889](assets/image-20250331215836889.png)

0X3f注释版：

```C++
class Solution {
public:
    int atMostNGivenDigitSet(vector<string> &digits, int n) {
        auto s = to_string(n);
        int m = s.length(), dp[m];
        memset(dp, -1, sizeof(dp)); // dp[i] = -1 表示 i 这个状态还没被计算出来
        function<int(int, bool, bool)> f = [&](int i, bool is_limit, bool is_num) -> int {
            if (i == m) return is_num; // 如果填了数字，则为 1 种合法方案
            if (!is_limit && is_num && dp[i] >= 0) return dp[i]; // 在不受到任何约束的情况下，返回记录的结果，避免重复运算
            int res = 0;
            if (!is_num) // 前面不填数字，那么可以跳过当前数位，也不填数字
                // is_limit 改为 false，因为没有填数字，位数都比 n 要短，自然不会受到 n 的约束
                // is_num 仍然为 false，因为没有填任何数字
                res = f(i + 1, false, false);
            char up = is_limit ? s[i] : '9'; // 根据是否受到约束，决定可以填的数字的上限
            // 注意：对于一般的题目而言，如果这里 is_num 为 false，则必须从 1 开始枚举，由于本题 digits 没有 0，所以无需处理这种情况
            for (auto &d : digits) { // 枚举要填入的数字 d
                if (d[0] > up) break; // d 超过上限，由于 digits 是有序的，后面的 d 都会超过上限，故退出循环
                // is_limit：如果当前受到 n 的约束，且填的数字等于上限，那么后面仍然会受到 n 的约束
                // is_num 为 true，因为填了数字
                res += f(i + 1, is_limit && d[0] == up, true);
            }
            if (!is_limit && is_num) dp[i] = res; // 在不受到任何约束的情况下，记录结果
            return res;
        };
        return f(0, true, false);
    }
};
```



### [1742. 盒子中小球的最大数量](https://leetcode.cn/problems/maximum-number-of-balls-in-a-box/)

你在一家生产小球的玩具厂工作，有 `n` 个小球，编号从 `lowLimit` 开始，到 `highLimit` 结束（包括 `lowLimit` 和 `highLimit` ，即 `n == highLimit - lowLimit + 1`）。另有无限数量的盒子，编号从 `1` 到 `infinity` 。

你的工作是将每个小球放入盒子中，其中盒子的编号应当等于小球编号上每位数字的和。例如，编号 `321` 的小球应当放入编号 `3 + 2 + 1 = 6` 的盒子，而编号 `10` 的小球应当放入编号 `1 + 0 = 1` 的盒子。

给你两个整数 `lowLimit` 和 `highLimit` ，返回放有最多小球的盒子中的小球数量*。*如果有多个盒子都满足放有最多小球，只需返回其中任一盒子的小球数量。

 

**示例 1：**

```
输入：lowLimit = 1, highLimit = 10
输出：2
解释：
盒子编号：1 2 3 4 5 6 7 8 9 10 11 ...
小球数量：2 1 1 1 1 1 1 1 1 0  0  ...
编号 1 的盒子放有最多小球，小球数量为 2 。
```



使用V2.0

https://leetcode.cn/problems/maximum-number-of-balls-in-a-box/solutions/3073112/san-chong-fang-fa-bao-li-mei-ju-qian-zhu-kze9/

```C++
class Solution {
public:
    int countBalls(int lowLimit, int highLimit) {
        string high_s = to_string(highLimit);
        int n = high_s.size();
        int m = high_s[0]-'0' + (n-1)*9;
        
        string low_s = to_string(lowLimit);
        low_s = string(n-low_s.size(),'0')+low_s;//!!!!
        
        vector<vector<int>> dp(n,vector<int>(m+1,-1));
        auto dfs = [&](this auto &&dfs ,int i,int sum,bool lowlimit,bool highlimit)->int
        {
            if(i==n) return sum==0;
            if(!lowlimit&&!highlimit&&dp[i][sum]!=-1)return dp[i][sum];
            int lo = lowlimit?low_s[i]-'0':0;
            int hi = highlimit?high_s[i]-'0':9;
            int res=0;
            for(int d=lo;d<=min(sum,hi);d++)//min(sum,hi)!!!
            {
                res+=dfs(i+1,sum-d,lowlimit&&d==lo,highlimit&&d==hi);
            }
            if(!lowlimit&&!highlimit)dp[i][sum] = res;
            return res;
        };

        int maxRes=0;
        for(int i=1;i<=m;i++)
        {
            maxRes = max(maxRes,dfs(0,i,true,true));
        }
        return maxRes;
    }
};
```



` low_s = string(n-low_s.size(),'0')+low_s;//!!!!`    需要补充前导0. 

比如 high 12345， low 8

这时候变成  low_s[i] 可能已经越界了，但是c++没报错而已

应该是 00008

# 十二、树形 DP

注：可能有同学觉得树形 DP 没有重复访问同一个状态（重叠子问题），并不能算作 DP，而是算作普通的递归。这么说也有一定道理，不过考虑到思维方式和 DP 是一样的自底向上，所以仍然叫做树形 DP。此外，如果是自顶向下的递归做法，是存在重叠子问题的，一般要结合记忆化搜索实现。

## §12.1 树的直径

讲解：[树形 DP：树的直径](https://leetcode.cn/link/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV17o4y187h1%2F)

### [543. 二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/)

给你一棵二叉树的根节点，返回该树的 **直径** 。

二叉树的 **直径** 是指树中任意两个节点之间最长路径的 **长度** 。这条路径可能经过也可能不经过根节点 `root` 。

两节点之间路径的 **长度** 由它们之间边数表示。

**示例 1：**

![img](assets/diamtree.jpg)

```
输入：root = [1,2,3,4,5]
输出：3
解释：3 ，取路径 [4,2,1,3] 或 [5,2,1,3] 的长度。
```



```C++
class Solution {
public:
    int s=0;
    int lenTree(TreeNode* root)
    {
        if(root == nullptr)return -1; //注意  这个必须是-1 到时会和1抵消
        int left = lenTree(root->left);
        int right= lenTree(root->right);
        int val = left+right+2;
        s = max(s,val);
        return max(left,right)+1;
    }
    int diameterOfBinaryTree(TreeNode* root) {
        lenTree(root);
        return s;
    }
};
```

或者

```C++
class Solution {
public:
    int diameterOfBinaryTree(TreeNode* root) {
        int ans = 0;
        auto dfs = [&](this auto&& dfs, TreeNode* node) -> int {
            if (node == nullptr) {
                return -1;
            }
            int l_len = dfs(node->left) + 1; // 左子树最大链长+1
            int r_len = dfs(node->right) + 1; // 右子树最大链长+1
            ans = max(ans, l_len + r_len); // 两条链拼成路径
            return max(l_len, r_len); // 当前子树最大链长
        };
        dfs(root);
        return ans;
    }
};
```



## §12.2 树上最大独立集

讲解：[树形 DP：打家劫舍III](https://leetcode.cn/link/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1vu4y1f7dn%2F)



### [337. 打家劫舍 III](https://leetcode.cn/problems/house-robber-iii/)

小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为 `root` 。

除了 `root` 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果 **两个直接相连的房子在同一天晚上被打劫** ，房屋将自动报警。

给定二叉树的 `root` 。返回 ***在不触动警报的情况下** ，小偷能够盗取的最高金额* 。

**示例 1:**

![img](assets/rob1-tree.jpg)

```
输入: root = [3,2,3,null,3,null,1]
输出: 7 
解释: 小偷一晚能够盗取的最高金额 3 + 3 + 1 = 7
```

```C++
class Solution {
    pair<int, int> dfs(TreeNode* node) {
        if (node == nullptr) { // 递归边界
            return {0, 0}; // 没有节点，怎么选都是 0
        }
        auto [l_rob, l_not_rob] = dfs(node->left); // 递归左子树
        auto [r_rob, r_not_rob] = dfs(node->right); // 递归右子树
        int rob = l_not_rob + r_not_rob + node->val; // 选
        int not_rob = max(l_rob, l_not_rob) + max(r_rob, r_not_rob); // 不选
        return {rob, not_rob};
    }

public:
    int rob(TreeNode* root) {
        auto [root_rob, root_not_rob] = dfs(root);
        return max(root_rob, root_not_rob); // 根节点选或不选的最大值
    }
};
```



```C++
class Solution {
public:
    pair<int, int> dfs(TreeNode* root)
    {
        if (root == nullptr) return { 0,0 };
        pair<int, int> pl = dfs(root->left);
        pair<int, int> pr = dfs(root->right);
        
        int choose = pl.second + pr.second + root->val;
        int noChoose = max(pl.first, pl.second) + max(pr.first, pr.second);
        
        return { choose , noChoose };
    }
    int rob(TreeNode* root) {
        pair<int,int> p =dfs(root);
        return max(p.first, p.second);
    }
};
```



