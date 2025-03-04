# Leetcode——常用数据结构专题

参考链接：[分享丨【题单】常用数据结构（前缀和/差分/栈/队列/堆/字典树/并查集/树状数组/线段树） - 力扣（LeetCode）](https://leetcode.cn/circle/discuss/mOr1u6/)

# 零、常用枚举技巧

## 1.枚举右，维护左

对于 **双变量问题**，例如两数之和$a_i+a_j=t$,可以枚举右边的$a_j$,转换为**单变量问题**，也就是在$a_j$左边找是否有$a_i=t-a_j$，这可以用哈希表维护。

这个技巧可以叫做**枚举右，维护左。**

参考[1. 两数之和 - 力扣（LeetCode）](https://leetcode.cn/problems/two-sum/solutions/2326193/dong-hua-cong-liang-shu-zhi-he-zhong-wo-0yvmj/)



### （1）[1. 两数之和](https://leetcode.cn/problems/two-sum/)

这是一道经典题目。可以枚举右（也就是让右侧的`j`变量从左到右依次遍历），然后维护左表示先看哈希表中是否有`target-nums[j]`，如果有说明记录过，直接返回`{it->second, j}`即可（哈希表的key表示值，value表示索引，`it->second`表示对应元素的索引）；否则如果找不到的话则把对应的`(nums[j],j)`放入到哈希表当中。

> 注意：不能先加入哈希表再查找，因为不能使用两次相同的元素，因此每次都是先查有没有再加入哈希表。

本题代码如下：

```c++
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> umap; //key:元素值, value:索引
        for(int j=0;j<nums.size();j++){
            int x = target - nums[j];
            auto it = umap.find(x);
            if(it!=umap.end()){
                return {it->second, j};
            }
            umap[nums[j]] = j;
        }
        return {};
    }
    
};
```



### （2）[1512. 好数对的数目](https://leetcode.cn/problems/number-of-good-pairs/)

```c++
class Solution {
public:
    int numIdenticalPairs(vector<int>& nums) {
        //哈希表维护有多少相同的数
        unordered_map<int, int> umap;
        int cnt = 0;
        for(int j=0;j<nums.size();j++){
            if(umap.count(nums[j])){
                cnt += umap[nums[j]]; //每遍历到一个新的数,和数组内所有和他相等的数都构成好数对
            }
            umap[nums[j]]++;
        }
        return cnt;
    }
};
```



### （3）[219. 存在重复元素 II](https://leetcode.cn/problems/contains-duplicate-ii/)

哈希表里存索引，取出时检查索引是否在范围内即可。代码如下：

```c++
class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        unordered_map<int, int> umap;
        for(int j=0;j<nums.size();j++){
            auto it = umap.find(nums[j]);
            if(it!=umap.end()){
                int index = umap[nums[j]];
                if(abs(index-j)<=k){
                    return true;
                }
            }
            umap[nums[j]]=j;
        }
        return false;
    }
};
```



### ==（4）[121. 买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/)==

看了一眼，感觉跟枚举右，维护左的关联性没有那么大，先不在这里做了。



### （5）[624. 数组列表中的最大距离](https://leetcode.cn/problems/maximum-distance-in-arrays/)

针对本题来说，**枚举右，维护左**的思想就在于，在每次往后遍历一个数组时，维护左侧遍历完的数组中的最小值和最大值，而最终结果一定在（当前数组最大-历史数组最小，以及历史数组最大-当前数组最小）中产生。

代码如下：

```c++
class Solution {
public:
    int maxDistance(vector<vector<int>>& arrays) {
        int minDist = INT_MAX/2, maxDist = -INT_MAX/2; //这样可以避免相减时溢出
        int result = -INT_MAX;
        for(int j=0;j<arrays.size();j++){
            result = max({result, arrays[j].back()-minDist, maxDist-arrays[j][0]}); //每个数组只能选一个,因此先计算再更新,避免重复的问题
            minDist = min(minDist, arrays[j][0]);
            maxDist = max(maxDist, arrays[j].back());
        }
        return result;
    }
};
```



Y 感觉上面那个更好

```C++
class Solution {
public:
    int maxDistance(vector<vector<int>>& arrays) 
    {
        // int minNum= INT_MAX/2;
        // int maxNum = -INT_MAX/2;
        int minNum = arrays[0][0];
        int maxNum = arrays[0].back();
        int res=0;
        for(int i=1;i<arrays.size();i++)
        {
            res = max({res,abs(arrays[i][0]-maxNum),abs(arrays[i].back()-minNum)});
            minNum = min(minNum,arrays[i][0]);
            maxNum = max(maxNum,arrays[i].back());
        }
        return res;
    }
};
```



### （6）[2815. 数组中的最大数对和](https://leetcode.cn/problems/max-pair-sum-in-an-array/)

```c++
class Solution {
public:
    int maxSum(vector<int>& nums) {
        int num[10]={0}; //记录每个数位对应的最大值
        int res = -1;
        for(int j=0;j<nums.size();j++){
            //开始拆解某个数,更新所有的为可能的最大值
            int x = nums[j];
            int m = 0; //记录最大的数位
            while(x){
                int a = x % 10;
                x /= 10;
                m = max(m, a);
            }
            if(num[m]!=0) res = max(res, nums[j]+num[m]); //num[m]如果是0表示"哈希表"里没东西,因为nums[i]>=1
            num[m] = max(num[m], nums[j]);
        } 
        return res;
    }
};
```



### （7）[1014. 最佳观光组合](https://leetcode.cn/problems/best-sightseeing-pair/)（※）

这道题目如果想要写出复杂度比较低的写法，有一定的难度。本题的要点在于，因为我们要计算的是`values[i] + values[j] + i - j`，可以维护`j`左侧的最大的`values[i]+i`项。每次移动`j`的时候，都先拿出记录的当前最大的`values[i]+i`项，然后判断是否当前是更好的观光组合，之后更新最大的`values[i]+i`项。（更新要放在查询之后，防止拿出了当前的索引值，出现重复）。此时代码如下：

```c++
class Solution {
public:
    int maxScoreSightseeingPair(vector<int>& values) {
        int maxV = -INT_MAX; //维护values[i]+i的最大值
        int res = -INT_MAX;
        for(int j=0;j<values.size();j++){
            int sum = maxV + values[j] - j;
            res = max(res, sum);
            maxV = max(maxV, values[j] + j); //更新values[i]+i的最大值
        }
        return res;
    }
};
```



### （8）[1814. 统计一个数组中好对子的数目](https://leetcode.cn/problems/count-nice-pairs-in-an-array/)

- `nums[i] + rev(nums[j]) == nums[j] + rev(nums[i])`转为计算``nums[i] -rev(nums[i]) == nums[j] - rev(nums[j])``

所以，提前先遍历一遍数组，然后计算一下`nums[i] -rev(nums[i])`的值，然后就转换为了前面学过的题目。

```c++
class Solution {
public:
    const int MOD = 1e9+7;
    int countNicePairs(vector<int>& nums) {
        //对数组进行预处理
        int n = nums.size();
        vector<long long> process(n);
        for(int i=0;i<nums.size();i++){
            int x = nums[i];
            //翻转x
            long long sum = 0;
            while(x){
                int a = x%10;
                sum*=10;
                sum+=a;
                x/=10;
            }
            process[i] = (long long)nums[i] - sum;
        }

        //用哈希存这个值,计算总的cnt
        int cnt = 0;
        unordered_map<long long, int> umap; //存每个值出现的次数
        for(int i=0;i<n;i++){
            cnt = (cnt + umap[process[i]])%MOD;
            umap[process[i]]++;
        }
        return cnt;
    }
};
```



# 一、前缀和

## §1.1.前缀和基础

首先，推荐阅读这一篇：[303. 区域和检索 - 数组不可变 - 力扣（LeetCode）](https://leetcode.cn/problems/range-sum-query-immutable/solutions/2693498/qian-zhui-he-ji-qi-kuo-zhan-fu-ti-dan-py-vaar/)

要点是记住：

- `s[0]=0`，以及计算`left`到`right`索引对应的数组和，可以用`s[right+1]-s[left]`。

具体写法，直接看本题板子题即可：

```c++
class NumArray {
public:
    vector<int> s;
    NumArray(vector<int>& nums) {
        int n = nums.size();
        s.resize(n+1);
        for(int i=0;i<n;i++){
            s[i+1] = s[i] + nums[i]; //注:s[0]=0
        }
    }
    
    int sumRange(int left, int right) {
        return s[right+1] - s[left];
    }
};

/**
 * Your NumArray object will be instantiated and called as such:
 * NumArray* obj = new NumArray(nums);
 * int param_1 = obj->sumRange(left,right);
 */
```

vector.resize 与 vector.reserve的区别  ： https://blog.csdn.net/JMW1407/article/details/108785448



### （1）[3427. 变长子数组求和](https://leetcode.cn/problems/sum-of-variable-length-subarrays/)

前缀和的最简单应用。

```c++
class Solution {
public:
    int subarraySum(vector<int>& nums) {
        int n = nums.size();
        int res = 0;
        vector<int> s(n+1);
        for(int i=0;i<n;i++) s[i+1] = s[i] + nums[i]; //前缀和
        for(int i=0;i<n;i++){
            int start = max(0, i-nums[i]);
            res += (s[i+1]-s[start]);
        }
        return res;
    }
};
```



### （2）[2559. 统计范围内的元音字符串数](https://leetcode.cn/problems/count-vowel-strings-in-ranges/)

```c++
class Solution {
public:
    bool isVowel(char& c){
        return c=='a' || c=='e' || c=='i' || c=='o' || c=='u';
    }
    bool isValid(string& s){
        return (isVowel(s[0]) && isVowel(s.back()));
    }
    vector<int> vowelStrings(vector<string>& words, vector<vector<int>>& queries) {
        int n = words.size();
        vector<int> s(n+1); //默认s[0]=0,前缀和
        for(int i=0;i<n;i++){
            s[i+1] = s[i] + (int)(isValid(words[i]));
        }
        //开始查询
        int m = queries.size();
        vector<int> res(m);
        for(int i=0;i<m;i++){
            res[i] = (s[queries[i][1]+1]-s[queries[i][0]]);
        }
        return res;
    }
};
```



### （3）[3152. 特殊数组 II](https://leetcode.cn/problems/special-array-ii/)（第一遍看了提示）

这道题的要点在于，可以让符合条件的在前缀和中用0表示，不符合条件的会+1上去，这样如果查询区间`s[right]-s[left]==0`则证明区间内都是0，也就是都符合要求。**针对这种题目可以变通考虑前缀和的下标开始位置，以及计算前缀和的公式，不要硬背诵板子。**

本题代码如下：

```c++
class Solution {
public:
    vector<bool> isArraySpecial(vector<int>& nums, vector<vector<int>>& queries) {
        int n = nums.size();
        int m = queries.size();
        vector<bool> res(m);
        vector<int> s(n);
        for(int i=1;i<n;i++){ //s[i]表示0~i的不相等情况
            s[i] = s[i-1] + (nums[i]%2==nums[i-1]%2); //不相等时是0,不会增加s[i],否则相等时是1,会增加s[i] 
        }
        for(int i=0;i<queries.size();i++){
            res[i] = (s[queries[i][1]]==s[queries[i][0]]);
        }
        return res;
    }
};
```



### （4）[1749. 任意子数组和的绝对值的最大值](https://leetcode.cn/problems/maximum-absolute-sum-of-any-subarray/)（想了一下直接看答案前缀和做法）

[1749. 任意子数组和的绝对值的最大值 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-absolute-sum-of-any-subarray/solutions/2372374/ren-yi-zi-shu-zu-he-de-jue-dui-zhi-de-zu-qerr/)，这个题解的思路确实很妙。C++中前缀和函数说明：[C++ STL partial_sum 函数说明 - 简书](https://www.jianshu.com/p/e68a11d5b316)

```c++
class Solution {
public:
    int maxAbsoluteSum(vector<int>& nums) {
        int n = nums.size();
        vector<int> s(n+1);
        partial_sum(nums.begin(), nums.end(), s.begin()+1); //注意,填一个0在前缀和开头是有必要的
        // for(int x:s){
        //     cout<<x<<" ";
        // }
        auto p = minmax_element(s.begin(), s.end());
        return *p.second - *p.first;
    }
};
```

之所以要填一个0在前缀和的开头，是因为可能会存在以下的序列：

![image-20250224193947519](Leetcode%E2%80%94%E2%80%94%E5%B8%B8%E7%94%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%93%E9%A2%98.assets/image-20250224193947519.png)

注意看标准输出，打印了前缀和中的元素，此时都是负的值，最大值应该是什么都不选。此时如果开头的0不在前缀和数组当中，会得到错误的结果。

> 可以理解为，添加一个0在前缀和开头，有助于解决查询区间`left=0`的问题。



常规写法:(如果忘记上面语法)

```C++
class Solution {
public:
    int maxAbsoluteSum(vector<int>& nums) {
        int n= nums.size();
        vector<int> preSum(n+1);
        int maxPresum=0;//防止max也是负的
        int minPresum=0;//方式min也是正的
        for(int i=0;i<n;i++)
        {
            preSum[i+1]=preSum[i]+nums[i];
            maxPresum = max(maxPresum,preSum[i+1]);
            minPresum = min(minPresum,preSum[i+1]);
        }
        return abs(maxPresum-minPresum);
    }
};
```





### （5）[2389. 和有限的最长子序列](https://leetcode.cn/problems/longest-subsequence-with-limited-sum/)（看答案）

注意本题是子序列，并不要求必须连续，可以删掉中间的。因为是求和所以可以对数组进行排序，并不影响结果。于是就可以前缀和+二分来做这道题了，代码如下：

```c++
class Solution {
public:
    vector<int> answerQueries(vector<int>& nums, vector<int>& queries) {
        //贪心:既然子序列要尽量长,就要选一些最小的数
        sort(nums.begin(), nums.end());
        //原地计算前缀和,本题不会做区间前缀和查询,因此不一定需要s[0]=0
        partial_sum(nums.begin(), nums.end(), nums.begin());
        vector<int> res(queries.size());
        for(int i=0;i<queries.size();i++){
            int x = queries[i];
            int len = ranges::upper_bound(nums, x) - nums.begin();
            res[i] = len;
        }
        return res;
    }
};
```

补充知识：[【C++】 详解 lower_bound 和 upper_bound 函数（看不懂来捶我！！！）_lowerbound和upperbound比较函数-CSDN博客](https://blog.csdn.net/weixin_45031801/article/details/137544229)

- 前提是有序的情况下，**lower_bound** **返回指向第一个值不小于 val 的位置，也就是返回第一个大于等于val值的位置。**（通过二分查找）
- 前提是有序的情况下，`upper_bound`返回第一个>target的值。所以像本题要求解最后一个<=target的值，可以用`upper_bound`的返回索引值-1来实现。

Y

```C++
class Solution {
public:
    vector<int> answerQueries(vector<int>& nums, vector<int>& queries) 
    {
        sort(nums.begin(),nums.end());
        //[1,2,4,5]
        //presum:[1,3,3,7,12]
        //二分
        int n=nums.size();
        vector<int> presum(n);
        partial_sum(nums.begin(),nums.end(),presum.begin());
        int qn=queries.size();
        vector<int> res(qn);
        for(int i=0;i<qn;i++)
        {
            //最后一个<=x的 第一个>x的-1
            auto a = upper_bound(presum.begin(),presum.end(),queries[i]);
            
            res[i]=(a-presum.begin());//end = a-1 (第一个>x的-1),res = end+1(数量)
        }
        return res;

    }
};
```



### ==（6）[3361. 两个字符串的切换距离](https://leetcode.cn/problems/shift-distance-between-two-strings/)==（题解太少，先放着）



### ==（7）[2055. 蜡烛之间的盘子](https://leetcode.cn/problems/plates-between-candles/)（看答案，这题暂时超纲了，水平太拉了，明天再试试）==

> 这道题目有比较大的思维难度。和接雨水那道题的思路有共同之处，推荐看这篇题解：[2055. 蜡烛之间的盘子 - 力扣（LeetCode）](https://leetcode.cn/problems/plates-between-candles/solutions/1320763/qian-zhui-he-xiang-xi-zhu-shi-qu-jin-shu-6v3k/)。思路挺绝的。
>
> 补充：为什么能想到前缀和呢？
>
> - 这道题目的第一个能想到的点是，维护每个点的左侧最近的蜡烛和右侧最近的蜡烛所在的索引，这就好像接雨水那道题目。
> - 接着，就是前缀和的思路了。用前缀和统计累加的盘子总数。对于查询的区间，只有区间左端点右侧最近的蜡烛，到右端点左侧最近的蜡烛之间的盘子是有效的，而计算这些盘子的总数就要用到前缀和。

（用时非常久，>45分钟）需要注意的问题：**前缀和依赖于什么进行更新呢？**验证前缀和的结果可以去题解那个链接里面看。

思考，什么时候前缀和不需要声明成+1的形式呢？==是不是在`nums[0]=0`的时候就可以正常用`s[right]-s[left]`了？（存疑）==



```C++
			"**|**|***|"
			"*	*  | * * | * * * | "
stopNum :	 0  0  0 0 0 2 2 2 2 5  ////存从左到右数 每个蜡烛（栏杆）能拦住多少盘子（猪）
Leftmin :	-1 -1  2 2 2 5 5 5 5 9 //存每个idx左边距离自己最近的蜡烛坐标
Rightmin:	 2  2  2 5 5 5 9 9 9 9 ////存每个idx右边距离自己最近的蜡烛坐标
```



```C++
class Solution {
public:
    vector<int> platesBetweenCandles(string s, vector<vector<int>>& queries) 
    {
        int n=s.size();
        vector<int> stopNum(n);//存从左到右数 每个蜡烛（栏杆）能拦住多少盘子（猪）
        int idx=0;
        int stopN=0;
        int NewStopNum=0;
        bool flagBeginStop=false;
        for(int i=0;i<n;i++)
        {
            if(s[i]=='|')
            {
                flagBeginStop = true;
            }
            if(flagBeginStop==true)
            {
                if(s[i]=='|')
                    NewStopNum =stopN;
                else stopN++;//=='*'
                stopNum[i]=NewStopNum;
            }
        }
        // for(int i=0;i<n;i++)
        // {
        //     cout<<stopNum[i]<<" ";
        // }
        // cout<<endl;
        vector<int> Leftmin(n);//存每个idx左边距离自己最近的蜡烛坐标
        int curIdx=-1;
        for(int i=0;i<n;i++)
        {
            if(s[i]=='|')curIdx = i;
            Leftmin[i]=curIdx;
        }
        // for(int i=0;i<n;i++)
        // {
        //     cout<<Leftmin[i]<<" ";
        // }
        // cout<<endl;
        vector<int> Rightmin(n);//存每个idx右边距离自己最近的蜡烛坐标
        curIdx=-1;
        for(int i=n-1;i>=0;i--)
        {
            if(s[i]=='|')curIdx = i;
            Rightmin[i]=curIdx;
        }
        // for(int i=0;i<n;i++)
        // {
        //     cout<<Rightmin[i]<<" ";
        // }
        int l=0,r=0;
        int qn=queries.size();
        vector<int> res(qn);
        for(int i=0;i<qn;i++)
        {
            l = queries[i][0];
            r = queries[i][1];
            //找到距离l右边最近的蜡烛
            int lr = Rightmin[l];
            int rl = Leftmin[r];
            if(lr==-1||rl==-1)res[i] = 0;
            else res[i] = max(0,stopNum[rl]-stopNum[lr]);
        }
        return res;
    }
};
```



### （8）[1523. 在区间范围内统计奇数数目](https://leetcode.cn/problems/count-odd-numbers-in-an-interval-range/)

依旧直接看了答案。定义`pre(x)`表示`[0，x]`之间的奇数的数目，容易得知该值是`(n+1)/2`个。因此，`[left,right]`区间内的奇数数目应该是`pre(right)-pre(left-1)`，之所以`-1`是因为要包括left在内。**启示是在做前缀和的题目是，一定要懂得灵活变通，不一定要写统一的板子，能搞清楚数组区间和前缀和的区间关系即可。**

代码如下：

```c++
class Solution {
public:
    int pre(int n){
        //统计[0,n]之间有多少奇数
        return (n+1)/2;
    }
    int countOdds(int low, int high) {
        //看见奇数+1,偶数维持不变
        return pre(high) - pre(low-1);
    }
};
```



## §1.2.前缀和与哈希表

通常要用到「枚举右，维护左」的技巧。

### （1）[560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)

乍一看，这题好像可以用滑动窗口来做。但注意，**数组当中可能有负数。这意味着当窗口右指针向右移动是，我们不能保证窗口中的和是递增的，因此滑动窗口方法不可用。**
（可以记为， 数组不是单调的话，不要用滑动窗口，考虑用前缀和）

题解：https://leetcode.cn/problems/subarray-sum-equals-k/solutions/2781031/qian-zhui-he-ha-xi-biao-cong-liang-ci-bi-4mwr/

前缀和**不**增加一位的写法：

```C++
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) 
    {
        //nums = [1,2,3], k = 3
        //presum = [1,3,6]
        //pre[i]-pre[j]=k
        //遍历i  找j 即pre[i]-k存不存在
        unordered_map<int,int> umap;
        int n=nums.size();
        vector<int> presum(n);
        partial_sum(nums.begin(),nums.end(),presum.begin());
        int cnt=0;
        umap[0]=1;//不增加一位的话需要将0手动加进来
        for(int i=0;i<n;i++)
        {
            int target = presum[i]-k;
            auto it = umap.find(target);
            if(it!=umap.end())
            {
                //find!
                cnt+=umap[target];
            }
            umap[presum[i]]++;
        }
        return cnt;
    }
};
```

问：为什么要把 0 也加到哈希表中？

答：举个最简单的例子，nums=[1], k=1。如果不把0加到哈希表中，按照我们的算法，没法算出这里有 1 个符合要求的子数组。也可以这样理解，要想把任意子数组都表示成两个前缀和的差，必须添加 0，否则当子数组是前缀时，没法减去一个数，具体见 前缀和及其扩展 中的讲解。



前缀和增加一位的写法：

```C++
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) 
    {
        //nums = [1,2,3], k = 3
        //presum = [1,3,6]
        //pre[i]-pre[j]=k
        //遍历i  找j 即pre[i]-k存不存在
        unordered_map<int,int> umap;
        int n=nums.size();
        vector<int> presum(n+1);
        partial_sum(nums.begin(),nums.end(),presum.begin()+1);
        int cnt=0;
        // umap[0]=1;
        for(int i=0;i<n+1;i++)
        {
            int target = presum[i]-k;
            auto it = umap.find(target);
            if(it!=umap.end())
            {
                //find!
                cnt+=umap[target];
            }
            umap[presum[i]]++;
        }
        return cnt;
    }
};
```



### [1524. 和为奇数的子数组数目](https://leetcode.cn/problems/number-of-sub-arrays-with-odd-sum/)

```C++
class Solution {
public:
    int numOfSubarrays(vector<int>& arr) 
    {
        //[1,3,5]
        //presum [1,4,9]
        //(presum[i]-presum[j])%2==1
        //遍历i ，求j
        //if presum[i] 1 cnt+=j0 num
        //if presum[i] 0 j1
        const int MOD=1e9+7;
        int oddPreSumNum=0;
        int evenPreSumNum=1;//加入0
        int n=arr.size();
        vector<int> presum(n);
        partial_sum(arr.begin(),arr.end(),presum.begin());
        int cnt=0;
        for(int i=0;i<n;i++)
        {
            if(presum[i]%2==0)
            {
                cnt=(cnt+oddPreSumNum)%MOD;
                evenPreSumNum++;
            }
            else
            {
                cnt=(cnt+evenPreSumNum)%MOD;
                oddPreSumNum++;
            }
        }
        return cnt%MOD;
    }
};
```



###  974. 和可被 K 整除的子数组 1676
https://leetcode.cn/problems/subarray-sums-divisible-by-k/

判断子数组的和能否被 k 整除就等价于判断 `(P[j]−P[i−1])mod k==0`，根据 **同余定理**，只要 `P[j]mod k==P[i−1]mod k`，就可以保证上面的等式成立。

作者：力扣官方题解
链接：https://leetcode.cn/problems/subarray-sums-divisible-by-k/solutions/187947/he-ke-bei-k-zheng-chu-de-zi-shu-zu-by-leetcode-sol/

在这道题目中，我们需要计算和可被 \( k \) 整除的子数组的数量。为了实现这一点，我们使用了前缀和（prefix sum）和同余定理。

```C++
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) 
    {
        //presum i -presum j %k ==0
        //presum i %k = presum j %k [同余定理]
        int n=nums.size();
        vector<int> presum(n+1);
        unordered_map<int,int> modkpresum;
        modkpresum[0]=1;/////
        for(int i=0;i<n;i++)
        {
            presum[i+1]=presum[i]+nums[i];
            // // 注意 C++ 取模的特殊性，当被除数为负数时取模结果为负数，需要纠正
            int modulus = ((presum[i+1]%k)+k)%k;
            modkpresum[modulus]++;
        }
        int cnt=0;
        //写法1：比较不简洁
        // for(auto it = modkpresum.begin();it!=modkpresum.end();it++)
        // {
        //     int num = (*it).second;
        //     cnt+=(num*(num-1))/2; //it返回的是
        // }
        //写法2：比较推荐
        for(auto [x,cx]:modkpresum)
        {
            cnt += cx*(cx-1)/2;
        }
        return cnt;
    }
};
```



简化写法:优化前缀和数组

```C++
class Solution {
public:
    int subarraysDivByK(vector<int>& nums, int k) 
    {
        int n=nums.size();
        unordered_map<int,int> umap;
        int sum=0;
        umap[0]=1;//因为ps[i]-0 %k==0 就是k的倍数 要考虑
        for(int i=0;i<n;i++)
        {
            sum+=nums[i];
            int modu = (sum%k+k)%k;//余数
            umap[modu]++;
        }
        int res=0;
        for(auto [x,cx]:umap)
        {
            res+=cx*(cx-1)/2;
        }
        return res;
    }
};
```



###### 解释 `modkpresum[0] = 1;`

1. **初始化 `modkpresum[0] = 1` 的原因**：
   - 当我们计算前缀和时，如果某个前缀和本身就能被 \( k \) 整除（即 `presum[i] % k == 0`），那么从数组的开始到这个位置的子数组也是一个有效的子数组。
   - 为了能够统计这些情况，我们需要在 `modkpresum` 中初始化 `0` 的计数为 `1`。这表示在开始时（即没有任何元素时），前缀和为 `0`，并且这个前缀和是可以被 \( k \) 整除的。

###### 具体例子

假设我们有一个数组 `nums = [4, 5, 0, -2, -3, 1]` 和 \( k = 5 \)。

- 在计算前缀和时，假设我们在某个位置 \( i \) 计算得到的前缀和 `presum[i]` 是 \( 5 \)（例如，前四个元素的和）。那么：
  - `presum[4] % 5 == 0`，这意味着从数组开始到位置 \( 4 \) 的子数组是一个有效的子数组。
- 如果没有初始化 `modkpresum[0]` 为 `1`，那么我们无法统计从数组开始到某个位置的子数组，因为我们没有记录前缀和为 `0` 的情况。

###### 总结

因此，`modkpresum[0] = 1;` 是为了确保我们能够正确统计那些从数组开始到某个位置的子数组的数量，这些子数组的和可以被 \( k \) 整除。



###  [523. 连续的子数组和](https://leetcode.cn/problems/continuous-subarray-sum/)

这题只需要返回是否存在, 那么umap中也可以仅仅存上一次mod是这个的idx 但是如果要返回个数估计还得存余数mod同的个数

```C++
class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) {
        int m = nums.size();
        if (m < 2) 
        {
            return false;
        }
        unordered_map<int, int> mp;
        mp[0] = -1;
        int remainder = 0;
        for (int i = 0; i < m; i++) 
        {
            remainder = (remainder + nums[i]) % k;
            if (mp.count(remainder)) 
            {
                int prevIndex = mp[remainder];
                if (i - prevIndex >= 2) 
                {
                    return true;
                }
                //不更新 保留最远
            }
            else
            {
                mp[remainder] = i;
            }
        }
        return false;
    }
};

作者：力扣官方题解
链接：https://leetcode.cn/problems/continuous-subarray-sum/solutions/807930/lian-xu-de-zi-shu-zu-he-by-leetcode-solu-rdzi/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```



```C++
class Solution {
public:
    bool checkSubarraySum(vector<int>& nums, int k) 
    {

        int n=nums.size();
        unordered_map<int,int> umap;
        vector<int> presum(n+1);
        // umap[0]=1;//因为ps[i]-0 %k==0 就是k的倍数 要考虑
        int keepLastmodu=0;//上一次的余数

        for(int i=0;i<n;i++)
        {
            presum[i+1]=presum[i]+nums[i];
            // int modu = (presum[i+1]%k+k)%k;//余数
            int modu = presum[i+1]%k;//余数.题目保证为正数
            //if(umap.contains(modu))res+=umap[modu];
            if(umap.contains(modu))return true;
            
            //umap[modu]++;
            umap[keepLastmodu]++;//上一次的余数，保证不会扣上次的 即让个数大于2
            keepLastmodu = modu;
        }
       
        return false;
    }
};
```



如果要返回**个数**  (不一定对.未验证)

```C++
class Solution {
public:
    int checkSubarraySum(vector<int>& nums, int k) 
    {

        int n=nums.size();
        unordered_map<int,int> umap;
        vector<int> presum(n+1);
        // umap[0]=1;//因为ps[i]-0 %k==0 就是k的倍数 要考虑
        int keepLastmodu=0;//上一次的余数
        int res=0;
        for(int i=0;i<n;i++)
        {
            
            presum[i+1]=presum[i]+nums[i];
            // int modu = (presum[i+1]%k+k)%k;//余数
            int modu = presum[i+1]%k;//余数.题目保证为正数
            if(umap.contains(modu))res+=umap[modu];
            
            //umap[modu]++;
            umap[keepLastmodu]++;//上一次的余数，保证不会扣上次的 即让个数大于2
            keepLastmodu = modu;
        }
       
        return res;
    }
};
```





###  [437. 路径总和 III](https://leetcode.cn/problems/path-sum-iii/) :call_me_hand:

> **注意，如果题目可能会有大数，可以考虑无脑用long long，不然可能会有一些测试用例卡掉，反正long long也就占一些额外的内存消耗，不太可能因为用long long导致超时或者超内存限制的。**

```C++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    unordered_map<long long,int> umap{{0,1}};
    int res=0;
    void dfs(TreeNode* node , long long sum,int targetSum)
    {
        if(node ==nullptr)return ;
        sum+=node->val;
        if(umap.contains(sum -targetSum))res+=umap[sum-targetSum]; 
        umap[sum]++;
        dfs(node->left,sum,targetSum);
        dfs(node->right,sum,targetSum);
        umap[sum]--;//在这里pop
    }
    int pathSum(TreeNode* root, int targetSum) 
    {
        //每个叶子节点到根节点，维护前缀和 vec vec
        //只看一条链。 枚举右，维护左。 对于i，寻找map中是否有VAL[i]-target的值，+=map[VAL[i]-target]
        //每次新加入节点 看是否有 结合回溯来做

        dfs(root,0,targetSum);
        return res;
    }
};
```



>问：为什么要把 0 加到哈希表中？
>
>答：这里的 0 相当于前缀和数组中的 s[0]=0。举个最简单的例子，根节点值为 1，targetSum=1。如果不把 0 加到哈希表中，按照我们的算法，没法算出这里有 1 条符合要求的路径。也可以这样理解，要想把任意路径和都表示成两个前缀和的差，必须添加一个 0，否则当路径是前缀时（从根节点开始的路径），没法减去一个数，具体见 前缀和及其扩展 中的讲解。
>
>作者：灵茶山艾府
>链接：https://leetcode.cn/problems/path-sum-iii/
>来源：力扣（LeetCode）
>著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



这题尝试过用迭代方法  做不出来 遂罢,尝试的过程在以下文件,以后可以进一步讨论

D:\PGPostgraduate\githubNotePrepareForWork\PrepareForWorkNotes\2025寒假\Y\学习记录等.md



###  [2588. 统计美丽子数组数目](https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/)  :custard:



```C++
class Solution {
public:
    long long beautifulSubarrays(vector<int>& nums) 
    {
        //0110
        //0011
        //0001
        //都是1->0
        //都是0->0
        //1 0->1
        //统计1的个数，如果每一位1的个数都是偶数就可以变成0=>亦或操作

        // vector<int> pre  前面的数组所有数字总的在每一位是偶数还是奇数
        //前缀和
        //每次变化奇偶性就行
        int n = nums.size();
        vector<int> preOddEven(n+1);
        long long res=0;
        unordered_map<int,int> umap(n);//存储每个^之后的数字 这个数字表示的是每个位上有多少奇偶
        umap[0]=1;
        for(int i=0;i<n;i++)
        {
            //0011 计算与前缀1100的^ =>1111   0011^ 0101 =  0110
            preOddEven[i+1]=preOddEven[i]^nums[i];//将第一个数字加入，并没有加0
            if(umap.contains(preOddEven[i+1]))res+=umap[preOddEven[i+1]];
            umap[preOddEven[i+1]]++;
        }
        return res;
    }
};
```

>https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/solutions/2163133/tao-lu-qian-zhui-he-ha-xi-biao-pythonjav-3fna/
>
>对于二进制中第 *i* 位，数组中所有元素第 *i* 位为 1 的数目为偶数，则此时满足数组中所有元素第 *i* 位的异或和一定为 0。
>
>```
>   //presumi 1101
>        //presumj 1101
>        //每一位1的个数奇偶性一样
>        //都是奇数 减完之后子数组一定是偶数个1
>```
>
>

优化”前缀和“数组位单个值

```C++
class Solution {
public:
    long long beautifulSubarrays(vector<int>& nums) 
    {
        int n = nums.size();
        // vector<int> preOddEven(n+1);
        int preOddEven=0;
        long long res=0;
        unordered_map<int,int> umap(n);
        umap[0]=1;
        for(int i=0;i<n;i++)
        {
            preOddEven=preOddEven^nums[i];//将第一个数字加入，并没有加0
            if(umap.contains(preOddEven))res+=umap[preOddEven];
            umap[preOddEven]++;
        } 
        return res;
    }
};
```



###  [525. 连续数组](https://leetcode.cn/problems/contiguous-array/) :call_me_hand:

给定一个二进制数组 `nums` , 找到含有相同数量的 `0` 和 `1` 的最长连续子数组，并返回该子数组的长度。

**示例 1:**

```
输入: nums = [0,1]
输出: 2
说明: [0, 1] 是具有相同数量 0 和 1 的最长连续子数组。
```

**示例 2:**

```
输入: nums = [0,1,0]
输出: 2
说明: [0, 1] (或 [1, 0]) 是具有相同数量0和1的最长连续子数组。
```

 

![5de8577a0b96cb4a525764aeb4e5657.png](assets/1622652955-LSHXCI-5de8577a0b96cb4a525764aeb4e5657.png)

```C++
class Solution {
public:
    int findMaxLength(vector<int>& nums) 
    {
        //相同数量
        int n=nums.size();
        unordered_map<int,int> umap(n);
        umap[0]=-1;
        int cur = 0;
        int maxLen = 0;
        // [0,1]
        // [-1,0]
        for(int i=0;i<n;i++)
        {
            if(nums[i]==0)cur--;
            else cur++;
            if(umap.contains(cur))
            {
                maxLen = max(maxLen,i-umap[cur]);//-umap[cur]+1错误 因为其实是前缀和相减
            }
            else 
            {
                umap[cur] = i;
            }
        }
        return maxLen;
        
    }
};
```

是不是做过一个类似的题目 在滑动窗口那里？



###  [面试题 17.05. 字母与数字](https://leetcode.cn/problems/find-longest-subarray-lcci/) 同 525 题

同上题

给定一个放有字母和数字的数组，找到最长的子数组，且包含的字母和数字的个数相同。

返回该子数组，若存在多个最长子数组，返回左端点下标值最小的子数组。若不存在这样的数组，返回一个空数组。

**示例 1：**

```
输入：["A","1","B","C","D","2","3","4","E","5","F","G","6","7","H","I","J","K","L","M"]

输出：["A","1","B","C","D","2","3","4","E","5","F","G","6","7"]
```

**示例 2：**

```
输入：["A","A"]

输出：[]
```

```C++
class Solution {
public:
    vector<string> findLongestSubarray(vector<string>& array) 
    {
        int n=array.size();
        unordered_map<int,int> umap(n);// <cur,idx>
        umap[0] = -1;//到时会做 -(-1) 相当于+1  否则会缺一位
        int cur=0;
        int start=0;
        int maxLen=0;
        int maxLenStart=0;
        //字母-- 数字++
        for(int i=0;i<n;i++)
        {
            string str = array[i];
            if(str[0]>='0'&&str[0]<='9')cur++;
            else cur--;
            if(umap.contains(cur))
            {
                start = umap[cur];
                int len = i-start;
                if(len>maxLen)
                {
                    maxLen=len;
                    maxLenStart = start+1;//+1!!!!!! //因为其实是要从它的下一个开始
                }
            }
            else
                umap[cur]=i;
        }
        return vector<string>(array.begin()+maxLenStart,array.begin()+maxLenStart+maxLen);
    }
};
```



## §1.3.距离和



### [1685. 有序数组中差绝对值之和](https://leetcode.cn/problems/sum-of-absolute-differences-in-a-sorted-array/)

给你一个 **非递减** 有序整数数组 `nums` 。

请你建立并返回一个整数数组 `result`，它跟 `nums` 长度相同，且`result[i]` 等于 `nums[i]` 与数组中所有其他元素差的绝对值之和。

换句话说， `result[i]` 等于 `sum(|nums[i]-nums[j]|)` ，其中 `0 <= j < nums.length` 且 `j != i` （下标从 0 开始）。

**示例 1：**

```
输入：nums = [2,3,5]
输出：[4,3,5]
解释：假设数组下标从 0 开始，那么
result[0] = |2-2| + |2-3| + |2-5| = 0 + 1 + 3 = 4，
result[1] = |3-2| + |3-3| + |3-5| = 1 + 0 + 2 = 3，
result[2] = |5-2| + |5-3| + |5-5| = 3 + 2 + 0 = 5。
```

**示例 2：**

```
输入：nums = [1,4,6,8,10]
输出：[24,15,13,15,21]
```

```C++
class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) 
    {
        int n=nums.size();
        vector<int> presum(n+1);
        partial_sum(nums.begin(),nums.end(),presum.begin()+1);
        vector<int> res(n);
        for(int i=0;i<n;i++)
        {
            res[i] = ( i*nums[i]-presum[i] )+(presum[n]-presum[i+1]-(n-i-1)*nums[i]);
        }
        return res;
    }
};
```



### [2602. 使数组元素全部相等的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-all-array-elements-equal/) :sparkles:

给你一个正整数数组 `nums` 。

同时给你一个长度为 `m` 的整数数组 `queries` 。第 `i` 个查询中，你需要将 `nums` 中所有元素变成 `queries[i]` 。你可以执行以下操作 **任意** 次：

- 将数组里一个元素 **增大** 或者 **减小** `1` 。

请你返回一个长度为 `m` 的数组 `answer` ，其中 `answer[i]`是将 `nums` 中所有元素变成 `queries[i]` 的 **最少** 操作次数。

**注意**，每次查询后，数组变回最开始的值。

 

**示例 1：**

```
输入：nums = [3,1,6,8], queries = [1,5]
输出：[14,10]
解释：第一个查询，我们可以执行以下操作：
- 将 nums[0] 减小 2 次，nums = [1,1,6,8] 。
- 将 nums[2] 减小 5 次，nums = [1,1,1,8] 。
- 将 nums[3] 减小 7 次，nums = [1,1,1,1] 。
第一个查询的总操作次数为 2 + 5 + 7 = 14 。
第二个查询，我们可以执行以下操作：
- 将 nums[0] 增大 2 次，nums = [5,1,6,8] 。
- 将 nums[1] 增大 4 次，nums = [5,5,6,8] 。
- 将 nums[2] 减小 1 次，nums = [5,5,5,8] 。
- 将 nums[3] 减小 3 次，nums = [5,5,5,5] 。
第二个查询的总操作次数为 2 + 4 + 1 + 3 = 10 。
```

最好使用以下这个presum补开头一个0的写法（加一位）

```C++
class Solution {
public:
    vector<long long> minOperations(vector<int>& nums, vector<int>& queries) 
    {
        int n=nums.size();
        sort(nums.begin(),nums.end() );
        vector<long long> preSum(n+1);
        //partial_sum(nums.begin(),nums.end(),preSum.begin());//一个是ll 一个是int 赋值的时候还是会越界 还是自己写吧
        for(int i=0;i<n;i++)preSum[i+1]=preSum[i]+nums[i];
        int qn = queries.size();
        vector<long long > res(qn);
        for(int i=0;i<qn;i++)
        {
            //寻找第一个>=Qi的值
            auto low = lower_bound(nums.begin(),nums.end(),queries[i]);//这个也可以
            long long index = low-nums.begin();
            long long ans = (long long)queries[i]*(index)-preSum[index];// 左边
            ans+= preSum[n]-preSum[index]-queries[i]*(n-index);//右边
            res[i]=ans;
        }
        return res;
    }
};
```



presum没增加一个

```C++
class Solution {
public:
    vector<long long> minOperations(vector<int>& nums, vector<int>& queries) 
    {
        // 3 1 6 8
        // -3>0 -1>1  3-2 
        int n=nums.size();
        sort(nums.begin(),nums.end() );
        vector<long long> preSum(n);
        //partial_sum(nums.begin(),nums.end(),preSum.begin());//一个是ll 一个是int 赋值的时候还是会越界 还是自己写吧
        preSum[0] = nums[0];
        for(int i=1;i<n;i++)preSum[i]=preSum[i-1]+nums[i];
        int qn = queries.size();
        vector<long long > res(qn);
        for(int i=0;i<qn;i++)
        {
            //寻找第一个>=Qi的值
            auto low = lower_bound(nums.begin(),nums.end(),queries[i]);//这个也可以
            long long index = low-nums.begin();
            long long ans=0;
            // 处理左边和：index为0时，leftSum=0
            long long leftSum = (index > 0) ? preSum[index - 1] : 0;
            ans = (long long)queries[i]*(index)-leftSum;
            long long totalSum = preSum.empty()?0:preSum.back();
            long long rightSum = totalSum - leftSum;
            ans+=rightSum- (long long)queries[i]*(n-index);

            res[i]=ans;
        }
        return res;
    }
};
```



<img src="assets/1723433422-AjGlKo-DBDE2F9C-5F12-48b9-A1B0-4360A6CA3987.png" alt="DBDE2F9C-5F12-48b9-A1B0-4360A6CA3987.png" style="zoom:33%;" />



### [2615. 等值距离和](https://leetcode.cn/problems/sum-of-distances/)

给你一个下标从 **0** 开始的整数数组 `nums` 。现有一个长度等于 `nums.length` 的数组 `arr` 。对于满足 `nums[j] == nums[i]` 且 `j != i` 的所有 `j` ，`arr[i]` 等于所有 `|i - j|` 之和。如果不存在这样的 `j` ，则令 `arr[i]` 等于 `0` 。

返回数组 `arr` *。*

**示例 1：**

```
输入：nums = [1,3,1,1,2]
输出：[5,0,3,4,0]
解释：
i = 0 ，nums[0] == nums[2] 且 nums[0] == nums[3] 。因此，arr[0] = |0 - 2| + |0 - 3| = 5 。 
i = 1 ，arr[1] = 0 因为不存在值等于 3 的其他下标。
i = 2 ，nums[2] == nums[0] 且 nums[2] == nums[3] 。因此，arr[2] = |2 - 0| + |2 - 3| = 3 。
i = 3 ，nums[3] == nums[0] 且 nums[3] == nums[2] 。因此，arr[3] = |3 - 0| + |3 - 2| = 4 。 
i = 4 ，arr[4] = 0 因为不存在值等于 2 的其他下标。
```

**示例 2：**

```
输入：nums = [0,5,3]
输出：[0,0,0]
解释：因为 nums 中的元素互不相同，对于所有 i ，都有 arr[i] = 0 。
```



##### 相同元素分组+前缀和

```C++
class Solution {
public:
    vector<long long> distance(vector<int>& nums) 
    {
        //1-vector<int> 0,2,3,7,8
        //0:
        int n=nums.size();
        vector<long long> res(n);
        unordered_map<int,vector<int>> umap;//存储index
        for(int i=0;i<n;i++)
        {
            umap[nums[i]].push_back(i);
        }

        //存储对于每个x来说的前缀和
        // unordered_map<int,vector<int>> preumap;
        //for(auto [x, v]:umap)
        for(auto &[x,v]:umap)//x是一样的值，v[i]:idx 引用更好
        {
            //求前缀和
            int m=v.size();
            vector<long long> presum(m+1);
            for(int i=0;i<m;i++)presum[i+1]=presum[i]+v[i];
            // preumap[x]=presum;

            for(int i=0;i<m;i++)
            {
                long long target = v[i];
                long long left = target*i-presum[i];
                // long long right = presum[m]-presum[i+1]-(m-i-1)*target;//这个也行 无非就i是包不包含自己而已 
                long long right = presum[m]-presum[i]-(m-i)*target;
                res[target] = left+right;
            }
        }
        return res;

    }
};
```



## §1.4 前缀异或和

推荐先阅读：[从集合论到位运算，常见位运算技巧分类总结！](https://leetcode.cn/circle/discuss/CaOJ45/)



### [1177. 构建回文串检测](https://leetcode.cn/problems/can-make-palindrome-from-substring/)  1848  :call_me_hand:

给你一个字符串 `s`，请你对 `s` 的子串进行检测。

每次检测，待检子串都可以表示为 `queries[i] = [left, right, k]`。我们可以 **重新排列** 子串 `s[left], ..., s[right]`，并从中选择 **最多** `k` 项替换成任何小写英文字母。 

如果在上述检测过程中，子串可以变成回文形式的字符串，那么检测结果为 `true`，否则结果为 `false`。

返回答案数组 `answer[]`，其中 `answer[i]` 是第 `i` 个待检子串 `queries[i]` 的检测结果。

注意：在替换时，子串中的每个字母都必须作为 **独立的** 项进行计数，也就是说，如果 `s[left..right] = "aaa"` 且 `k = 2`，我们只能替换其中的两个字母。（另外，任何检测都不会修改原始字符串 `s`，可以认为每次检测都是独立的）

 

**示例：**

```
输入：s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]
输出：[true,false,false,true,true]
解释：
queries[0] : 子串 = "d"，回文。
queries[1] : 子串 = "bc"，不是回文。
queries[2] : 子串 = "abcd"，只替换 1 个字符是变不成回文串的。
queries[3] : 子串 = "abcd"，可以变成回文的 "abba"。 也可以变成 "baab"，先重新排序变成 "bacd"，然后把 "cd" 替换为 "ab"。
queries[4] : 子串 = "abcda"，可以变成回文的 "abcba"。
```

**提示：**

- `1 <= s.length, queries.length <= 10^5`
- `0 <= queries[i][0] <= queries[i][1] < s.length`
- `0 <= queries[i][2] <= s.length`
- `s` 中只有小写英文字母





![image-20250227135756695](assets/image-20250227135756695.png)

#### 三、算法（优化前）

https://leetcode.cn/problems/can-make-palindrome-from-substring/solutions/2309725/yi-bu-bu-you-hua-cong-qian-zhui-he-dao-q-yh5p/

![image-20250227002134586](assets/image-20250227002134586.png)

```C++
class Solution {
public:
    vector<bool> canMakePaliQueries(string s, vector<vector<int>>& queries) 
    {
        int n=s.size();
        vector<array<int,26>> sum(n+1);
        //sum[i][0] 表示前i个字母前缀中a的个数
        //用途：sum 的每个元素（如 sum[i]）存储字符串 s 前 i 个字符中各字母（a-z）的出现次数
        for(int i=0;i<n;i++)
        {
            sum[i+1]=sum[i];
            sum[i+1][s[i]-'a']++;
        }
        int qn = queries.size();
        vector<bool> res(qn);
        for(int i=0;i<qn;i++)
        {
            int left = queries[i][0],right = queries[i][1],k=queries[i][2];
            int m=0;//m 种字母出现奇数次
            for(int j=0;j<26;j++)
            {
                m+=((sum[right+1][j]-sum[left][j])%2==1);
            }
            res[i] = (m/2 <=k);
        }
        return res;

    }
};
```



>------
>
>用户代码中的 `vector<array<int, 26>>` 表示一个向量，每个元素是一个固定大小为26的 `int` 数组：
>
>```
>cpp复制代码vector<std::array<int, 26>> sum(n + 1);
>```
>
>- **用途**：`sum` 的每个元素（如 `sum[i]`）存储
>
>###  **`std::array` 的语法**
>
>`std::array` 是固定大小的数组容器，声明时需要指定 **元素类型** 和 **固定大小**：
>
>```
>cpp复制代码#include <array>
>
>// 定义一个包含26个int元素的数组
>std::array<int, 26> arr;
>```
>
>- **模板参数**：`<int, 26>` 表示元素类型为 `int`，数组大小为26。
>- **性能**：与原生数组性能相同，但更安全（如边界检查）且支持STL操作[1](https://www.cnblogs.com/huaweiyun/p/14060524.html)[3](https://blog.csdn.net/weixin_59141600/article/details/126898379)[7](https://cloud.tencent.com/developer/article/1518723)。
>
>### **为什么用 `std::array` 而不是 `vector`？**
>
>- **固定大小**：当元素数量已知且不变（如26个字母）时，`std::array` 更高效（无动态内存分配）[1](https://www.cnblogs.com/huaweiyun/p/14060524.html)[7](https://cloud.tencent.com/developer/article/1518723)。
>- **内存局部性**：所有元素存储在连续内存中，访问速度更快[1](https://www.cnblogs.com/huaweiyun/p/14060524.html)[7](https://cloud.tencent.com/developer/article/1518723)。



接下来的优化在：https://leetcode.cn/problems/can-make-palindrome-from-substring/solutions/2309725/yi-bu-bu-you-hua-cong-qian-zhui-he-dao-q-yh5p/ 中 



#### 四、一步步优化
由于只关心每种字母出现次数的奇偶性，所以不需要在前缀和中存储每种字母的出现次数，只需要保存每种字母出现次数的奇偶性。

为方便计算，用 0 表示出现偶数次，用 1 表示出现奇数次。

注意只有奇数减偶数，或者偶数减奇数，才能得到奇数。所以如果相减的结果不为 0（或者说相减的两个数不相等），就表示出现了奇数次。

```C++
class Solution {
public:
    vector<bool> canMakePaliQueries(string s, vector<vector<int>>& queries) 
    {
        int n=s.size();
        vector<array<int,26>> sum(n+1);
        //sum[i][0] 表示前i个字母前缀中a的个数
        //用途：sum 的每个元素（如 sum[i]）存储字符串 s 前 i 个字符中各字母（a-z）的出现次数
        for(int i=0;i<n;i++)
        {
            sum[i+1]=sum[i];
            sum[i+1][s[i]-'a']++;
            sum[i+1][s[i]-'a']%=2;
        }
        int qn = queries.size();
        vector<bool> res(qn);
        for(int i=0;i<qn;i++)
        {
            int left = queries[i][0],right = queries[i][1],k=queries[i][2];
            int m=0;//m 种字母出现奇数次
            for(int j=0;j<26;j++)
            {
                // m+=((sum[right+1][j]-sum[left][j])%2==1);
                m+=(sum[right+1][j]!=sum[left][j]);
            }
            res[i] = (m/2 <=k);
        }
        return res;

    }
};
```



由于异或运算满足 1 和 0 的结果是 1，而 0 和 0，以及 1 和 1 的结果都是 0，所以可以用异或替换上面的减法。

```C++
class Solution {
public:
    vector<bool> canMakePaliQueries(string s, vector<vector<int>>& queries) 
    {
        int n=s.size();
        vector<array<int,26>> sum(n+1);
        //sum[i][0] 表示前i个字母前缀中a的个数
        //用途：sum 的每个元素（如 sum[i]）存储字符串 s 前 i 个字符中各字母（a-z）的出现次数
        for(int i=0;i<n;i++)
        {
            sum[i+1]=sum[i];
            // sum[i+1][s[i]-'a']++;//【改】
            sum[i+1][s[i]-'a']^=1;// // 奇数变偶数，偶数变奇数【改】（这一个字母+1 会出现奇变偶 偶变奇）
        }
        int qn = queries.size();
        vector<bool> res(qn);
        for(int i=0;i<qn;i++)
        {
            int left = queries[i][0],right = queries[i][1],k=queries[i][2];
            int m=0;//m 种字母出现奇数次
            for(int j=0;j<26;j++)
            {
                // m+=((sum[right+1][j]-sum[left][j])%2==1);
                m+=(sum[right+1][j]^sum[left][j]);//【改】
            }
            res[i] = (m/2 <=k);
        }
        return res;

    }
};
```



由于长为 26 的数组中只存储 0 和 1，可以压缩到一个二进制数中，二进制数从低到高第 i 个比特存储着 0 和 1 的信息。

例如二进制 10010 表示 b 和 e 出现奇数次，其余字母出现偶数次。

在计算前缀和时（准确地说是异或前缀和）：

修改 a 出现次数的奇偶性，可以异或二进制 1；
修改 b 出现次数的奇偶性，可以异或二进制 10；
修改 c 出现次数的奇偶性，可以异或二进制 100；
依此类推。
此外，由于异或可以「并行计算」，对前缀和中的两个二进制数直接异或，便得到了子串中每种字母出现次数的奇偶性。再计算这个二进制数中的 1 的个数，便得到了 m。

例如 10010⊕01110=11100，说明有 3 种字母出现奇数次.

>这里不理解的话可以看题目[2588. 统计美丽子数组数目](https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/)  :custard:  跟那个有点像
>
>对于二进制中第 *i* 位，数组中所有元素第 *i* 位为 1 的数目为偶数，则此时满足数组中所有元素第 *i* 位的异或和一定为 0。
>
>```
>   //presumi 1101
>   //presumj 1101
>   //每一位1的个数奇偶性一样
>   //都是奇数 减完之后子数组一定是偶数个1
>```
>

```C++
class Solution {
public:
    vector<bool> canMakePaliQueries(string s, vector<vector<int>>& queries) 
    {
        int n=s.size();
        // vector<array<int,26>> sum(n+1);
        vector<int> sum(n+1);//最大是2^24 没超过2^32//【改】
        //sum[i][0] 表示前i个字母前缀中a的个数
        //用途：sum 的每个元素（如 sum[i]）存储字符串 s 前 i 个字符中各字母（a-z）的出现次数
        for(int i=0;i<n;i++)
        {
            sum[i+1]=sum[i];
            // sum[i+1][s[i]-'a']^=1;
            int bit = 1<<(s[i]-'a');//【改】
            sum[i+1]^=bit;//// 该比特对应字母的奇偶性：奇数变偶数，偶数变奇数//【改】
        }
        int qn = queries.size();
        vector<bool> res(qn);
        for(int i=0;i<qn;i++)
        {
            int left = queries[i][0],right = queries[i][1],k=queries[i][2];
            int m=0;//m 种字母出现奇数次
            m=__builtin_popcount(sum[right+1]^sum[left]);//【改】

            res[i] = (m/2 <=k);
        }
        return res;

    }
};
```





## §1.5 其他一维前缀和

### [1310. 子数组异或查询](https://leetcode.cn/problems/xor-queries-of-a-subarray/)

有一个正整数数组 `arr`，现给你一个对应的查询数组 `queries`，其中 `queries[i] = [Li, Ri]`。

对于每个查询 `i`，请你计算从 `Li` 到 `Ri` 的 **XOR** 值（即 `arr[Li] **xor** arr[Li+1] **xor** ... **xor** arr[Ri]`）作为本次查询的结果。

并返回一个包含给定查询 `queries` 所有结果的数组。

**示例 1：**

```
输入：arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]
输出：[2,7,14,8] 
解释：
数组中元素的二进制表示形式是：
1 = 0001 
3 = 0011 
4 = 0100 
8 = 1000 
查询的 XOR 值为：
[0,1] = 1 xor 3 = 2 
[1,2] = 3 xor 4 = 7 
[0,3] = 1 xor 3 xor 4 xor 8 = 14 
[3,3] = 8
```



```C++
class Solution {
public:
    vector<int> xorQueries(vector<int>& arr, vector<vector<int>>& queries) {
        //1 1101
        //2 1110 - 0011
        //3 0001 - 0010
        //4 1010 - 1000
        //5 1111 - 0111

        //3 0001 
        //4 1010 - 1011 = pre4^pre2 

        int n = arr.size();
        vector<int> presum(n+1);
        for(int i=0;i<n;i++)
        {
            presum[i+1] = presum[i]^arr[i];
        }
        int qn = queries.size();
        vector<int> res(qn);
        for(int i=0;i<qn;i++)
        {
            int left = queries[i][0],right = queries[i][1];
            int ans = presum[right+1]^presum[left];
            res[i]=ans;
        }
        return res;

    }
};
```



这个算是前缀异或和吧

和题目[1177. 构建回文串检测](https://leetcode.cn/problems/can-make-palindrome-from-substring/)  1848 以及题目[2588. 统计美丽子数组数目](https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/)  :custard: 相关

![image-20250227141132234](assets/image-20250227141132234.png)





### [2438. 二的幂数组中查询范围内的乘积](https://leetcode.cn/problems/range-product-queries-of-powers/)

[2438. 二的幂数组中查询范围内的乘积](https://leetcode.cn/problems/range-product-queries-of-powers/)

给你一个正整数 `n` ，你需要找到一个下标从 **0** 开始的数组 `powers` ，它包含 **最少** 数目的 `2` 的幂，且它们的和为 `n` 。`powers` 数组是 **非递减** 顺序的。根据前面描述，构造 `powers` 数组的方法是唯一的。

同时给你一个下标从 **0** 开始的二维整数数组 `queries` ，其中 `queries[i] = [lefti, righti]` ，其中 `queries[i]` 表示请你求出满足 `lefti <= j <= righti` 的所有 `powers[j]` 的乘积。

请你返回一个数组 `answers` ，长度与 `queries` 的长度相同，其中 `answers[i]`是第 `i` 个查询的答案。由于查询的结果可能非常大，请你将每个 `answers[i]` 都对 `109 + 7` **取余** 。

 

**示例 1：**

```
输入：n = 15, queries = [[0,1],[2,2],[0,3]]
输出：[2,4,64]
解释：
对于 n = 15 ，得到 powers = [1,2,4,8] 。没法得到元素数目更少的数组。
第 1 个查询的答案：powers[0] * powers[1] = 1 * 2 = 2 。
第 2 个查询的答案：powers[2] = 4 。
第 3 个查询的答案：powers[0] * powers[1] * powers[2] * powers[3] = 1 * 2 * 4 * 8 = 64 。
每个答案对 109 + 7 得到的结果都相同，所以返回 [2,4,64] 。
```



要解决这个问题，我们需要处理大数指数运算时的溢出问题。直接使用位移操作会导致溢出，尤其是在处理非常大的指数时。正确的做法是使用快速幂算法，并在每一步计算中取模，以避免溢出并确保结果正确。

关于快速幂请看https://leetcode.cn/problems/powx-n/solutions/2858114/tu-jie-yi-zhang-tu-miao-dong-kuai-su-mi-ykp3i/

<img src="assets/1728623430-RNGDEK-lc50-3-c.png" alt="lc50-3-c.png" style="zoom: 25%;" />

```C++
class Solution {
public:
    long long mod_pow(long long x, long long n, long long mod) 
    {
        long long ans=1;
        while (n) // 从低到高枚举 n 的每个比特位
        { 
            if (n & 1) // 这个比特位是 1
            { 
                ans = (ans*x%mod)%mod; // 把 x 乘到 ans 中
            }
            x = (x*x%mod)%mod; // x 自身平方
            n >>= 1; // 继续枚举下一个比特位
        }
        return ans%mod;
    }
    vector<int> productQueries(int n, vector<vector<int>>& queries) 
    {
        //01111 1248
        //1 2 4 8 16 
        //0 1 2 3 4 次方
        //数字取出来 存一个前缀积
        const int MOD=1e9+7;
        int m = n;
        vector<long long> nums;
        vector<long long> presum;
        presum.push_back(0);
        for(int i=0;m;i++)
        {
            if(m&1)
            {
                nums.push_back(i); //cout<<i<<" ";
                presum.push_back(presum.back()+i);
            }
            m=m>>1;
        }
        int qn = queries.size();
        vector<int> res(qn);
        for(int i=0;i<qn;i++)
        {
            int left = queries[i][0],right = queries[i][1];
            long long diff = presum[right+1]-presum[left];
            //res[i] = (1<<diff)%MOD;
            res[i]=static_cast<int>(mod_pow(2, diff, MOD));
        }

        return res;
        
    }
};
```



## §1.6 二维前缀和

[【图解】一张图秒懂二维前缀和！](https://leetcode.cn/problems/range-sum-query-2d-immutable/solution/tu-jie-yi-zhang-tu-miao-dong-er-wei-qian-84qp/)

<img src="https://pic.leetcode.cn/1692152740-dSPisw-matrix-sum.png" alt="matrix-sum.png" style="zoom: 40%;" />‘





### [304. 二维区域和检索 - 矩阵不可变](https://leetcode.cn/problems/range-sum-query-2d-immutable/) 【板子】

给定一个二维矩阵 `matrix`，以下类型的多个请求：

- 计算其子矩形范围内元素的总和，该子矩阵的 **左上角** 为 `(row1, col1)` ，**右下角** 为 `(row2, col2)` 。

实现 `NumMatrix` 类：

- `NumMatrix(int[][] matrix)` 给定整数矩阵 `matrix` 进行初始化
- `int sumRegion(int row1, int col1, int row2, int col2)` 返回 **左上角** `(row1, col1)` 、**右下角** `(row2, col2)` 所描述的子矩阵的元素 **总和** 。

**示例 1：**

![img](assets/1626332422-wUpUHT-image.png)

```
输入: 
["NumMatrix","sumRegion","sumRegion","sumRegion"]
[[[[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]],[2,1,4,3],[1,1,2,2],[1,2,2,4]]
输出: 
[null, 8, 11, 12]
```

解答
原因看上上面那个图

```C++
class NumMatrix {
public:
    vector<vector<int>> sum;
    NumMatrix(vector<vector<int>>& matrix) 
    {
        int m=matrix.size(),n=matrix[0].size();
        sum.resize(m+1,vector<int>(n+1,0));
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                sum[i+1][j+1] = sum[i][j+1]+sum[i+1][j]-sum[i][j]+matrix[i][j];
            }
        }
    }
    
    int sumRegion(int row1, int col1, int row2, int col2) 
    {
        return sum[row2+1][col2+1]-sum[row2+1][col1]-sum[row1][col2+1]+sum[row1][col1];
    }
};

/**
 * Your NumMatrix object will be instantiated and called as such:
 * NumMatrix* obj = new NumMatrix(matrix);
 * int param_1 = obj->sumRegion(row1,col1,row2,col2);
 */
```



### [1314. 矩阵区域和](https://leetcode.cn/problems/matrix-block-sum/)

给你一个 `m x n` 的矩阵 `mat` 和一个整数 `k` ，请你返回一个矩阵 `answer` ，其中每个 `answer[i][j]` 是所有满足下述条件的元素 `mat[r][c]` 的和： 

- `i - k <= r <= i + k, `
- `j - k <= c <= j + k` 且
- `(r, c)` 在矩阵内。

**示例 1：**

```
输入：mat = [[1,2,3],[4,5,6],[7,8,9]], k = 1
输出：[[12,21,16],[27,45,33],[24,39,28]]
```
ans

```C++
class Solution {
public:
    vector<vector<int>> matrixBlockSum(vector<vector<int>>& mat, int k) 
    {
        //build presum
        int m=mat.size(),n=mat[0].size();
        vector<vector<int>> presum(m+1,vector<int>(n+1,0));
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                presum[i+1][j+1] = presum[i][j+1]+presum[i+1][j]-presum[i][j]+mat[i][j];
                //[1,2,3]
                //[4,5,6]
                //[7,8,9]
                //cout<<"presum[i+1][j+1]:i+1:"<<i+1<<" j+1:"<<j+1<<" : **"<<presum[i+1][j+1]<<"  /";
            }
            //cout<<endl;
        }
        vector<vector<int>> ans(m,vector<int>(n,0));
         for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                int xmin = max(0,i-k);
                int ymin = max(0,j-k);
                int xmax = min(i+k,m-1);//m！！！
                int ymax = min(j+k,n-1);//n！！！

                ans[i][j] =
                 presum[xmax+1][ymax+1] - presum[xmax+1][ymin]-presum[xmin][ymax+1]+presum[xmin][ymin];
            }
        }
        return ans;
    }
};
```





### [3070. 元素和小于等于 k 的子矩阵的数目](https://leetcode.cn/problems/count-submatrices-with-top-left-element-and-sum-less-than-k/)

给你一个下标从 **0** 开始的整数矩阵 `grid` 和一个整数 `k`。

返回包含 `grid` 左上角元素、元素和小于或等于 `k` 的 **子矩阵**的数目。

**示例 1：**

![img](assets/example1.png)

```
输入：grid = [[7,6,3],[6,6,1]], k = 18
输出：4
解释：如上图所示，只有 4 个子矩阵满足：包含 grid 的左上角元素，并且元素和小于或等于 18 。
```

ans:
```c++
class Solution {
public:
    int countSubmatrices(vector<vector<int>>& grid, int k) 
    {
        int m= grid.size(),n=grid[0].size();
        vector<vector<int>> sum(m+1,vector<int>(n+1,0));
        int res=0;
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                sum[i+1][j+1] = sum[i][j+1]+sum[i+1][j]-sum[i][j]+grid[i][j];
                if(sum[i+1][j+1]<=k)res++;
            }
        }
        return res;
    }
};
```





### [1738. 找出第 K 大的异或坐标值](https://leetcode.cn/problems/find-kth-largest-xor-coordinate-value/) :eyes:

给你一个二维矩阵 `matrix` 和一个整数 `k` ，矩阵大小为 `m x n` 由非负整数组成。

矩阵中坐标 `(a, b)` 的 **目标值** 可以通过对所有元素 `matrix[i][j]` 执行异或运算得到，其中 `i` 和 `j` 满足 `0 <= i <= a < m` 且 `0 <= j <= b < n`（**下标从 0 开始计数**）。

请你找出 `matrix` 的所有坐标中第 `k` 大的目标值（**`k` 的值从 1 开始计数**）。

**示例 1：**

```
输入：matrix = [[5,2],[1,6]], k = 1
输出：7
解释：坐标 (0,1) 的目标值是 5 XOR 2 = 7 ，为最大的目标值。
```



解析：

下图给出了该二维前缀和递推式的可视化展示。

<img src="assets/1-1740733863865-8.png" alt="fig1" style="zoom:40%;" />

<img src="assets/image-20250228171135184.png" alt="image-20250228171135184" style="zoom: 80%;" />



$\color{red}{\huge快速选择算法nth\_element}$

在C++中，可以使用std::nth_element函数来实现快速选择算法。

std::nth_element函数用于将第n个元素放置在已排序序列中的正确位置上，并将该位置左边的元素都小于该元素，右边的元素都大于该元素。

https://www.acwing.com/blog/content/37043/

https://leetcode.cn/circle/discuss/AL5nP8/

函数原型如下：

```C++
template <class RandomAccessIterator>
//注意 返回void！！  
void nth_element(RandomAccessIterator first, RandomAccessIterator nth, RandomAccessIterator last);

template <class RandomAccessIterator, class Compare>
void nth_element(RandomAccessIterator first, RandomAccessIterator nth, RandomAccessIterator last, Compare comp);
```

参数说明：

- first：指向要排序的序列的起始位置的迭代器。
- nth：指向要选择的元素的位置的迭代器。
- last：指向要排序的序列的末尾位置的迭代器。
- comp：可选参数，用于指定比较函数的谓词。



##### 代码

```C++
class Solution {
public:
    int kthLargestValue(vector<vector<int>>& matrix, int k) 
    {
        int m = matrix.size(),n=matrix[0].size();
        vector<vector<int>> sum(m+1,vector<int>(n+1));
        vector<int> res(n*m);
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                sum[i+1][j+1]= sum[i+1][j]^sum[i][j+1]^sum[i][j]^matrix[i][j];
                res[i*n+j] = sum[i+1][j+1];
            }
        }
        //----法2：【推荐】快速选择
        nth_element(res.begin(),res.begin()+k-1,res.end(),greater<int>());//greater<int>() 注意这个写法！！
        return res[k-1];//！！

        //----法1：sort 排序
        // sort(res.begin(),res.end());
        // //01234    //3  //5  //5-3=2
        // return res[n*m-k];

        //----法1.2：sort 排序2
        // sort(res.begin(),res.end(),greater<int>());
        // return res[k-1];
        
        
    }
};
```



### [3212. 统计 X 和 Y 频数相等的子矩阵数量](https://leetcode.cn/problems/count-submatrices-with-equal-frequency-of-x-and-y/)

给你一个二维字符矩阵 `grid`，其中 `grid[i][j]` 可能是 `'X'`、`'Y'` 或 `'.'`，返回满足以下条件的子矩阵数量：

- 包含 `grid[0][0]`
- `'X'` 和 `'Y'` 的频数相等。
- 至少包含一个 `'X'`。

**示例 1：**

**输入：** grid = [["X","Y","."],["Y",".","."]]

**输出：** 3

**解释：**

**<img src="assets/examplems.png" alt="img" style="zoom: 67%;" />**

##### 代码
```C++
class Solution {
public:
    int numberOfSubmatrices(vector<vector<char>>& grid) 
    {
        //前缀和中 存储xy的个数
        int m=grid.size(),n=grid[0].size();
        vector<vector<pair<int,int>>> sum(m+1,vector<pair<int,int>>(n+1,{0,0}));
        int res=0;
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                char gridc = (grid[i][j]);
                sum[i+1][j+1].first = 
                    sum[i+1][j].first + sum[i][j+1].first -sum[i][j].first + (gridc=='X');
                sum[i+1][j+1].second = 
                    sum[i+1][j].second + sum[i][j+1].second -sum[i][j].second + (gridc=='Y');
                if(sum[i+1][j+1].first>=1 && sum[i+1][j+1].first == sum[i+1][j+1].second)
                {
                    res++;
                }
            }
        }
        return res;
    }
};
```



# 二、差分

### §2.1 一维差分（扫描线）

>差分即存储**变化值**。

### （1）[1094. 拼车](https://leetcode.cn/problems/car-pooling/)

一种最为基础的差分写法（自己看完原理写的）：

> 创建一个长为 1001 的差分数组，这可以保证 *d* 数组不会下标越界。

```c++
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        //差分数组,离米小游的题目又近了一些
        //写法1:直接把长度定为1001,这样一定不会超
        vector<int> d(1001);
        //一开始都是0,意味着每一段都没有乘客
        for(int i=0;i<trips.size();i++){
            int start = trips[i][1];
            int end = trips[i][2];
            int p = trips[i][0]; //乘客数量
            d[start]+=p;
            d[end]-=p; //end对应的站不算,因为乘客下车了
        }
        int start = 0;
        //可以靠差分数组还原原来的数组
        for(int i=0;i<1001;i++){
            start+=d[i];
            if(start>capacity) return false;
        }
        return true;
    }
};
```



第二种写法是利用平衡树（C++ 中的 `map`，Java 中的 `TreeMap`）代替差分数组，因为我们只需要考虑在`from_i`到`to_i`这部分的乘客数，其余位置的乘客数是保持不变的，无需考虑。平衡树可以保证我们是从小到大遍历这些位置的。当然，如果你不想用平衡树的话，也可以用哈希表，把哈希表的 key 取出来排序，就可以从小到大遍历这些位置了。

此时第二种写法的代码如下（可能是因为map的原因，这种写法会慢一些，感觉看数据量吧，比如这题`trip`的大小只有1000其实直接可以开一个定长vector来解决）：

```c++
class Solution {
public:
    bool carPooling(vector<vector<int>>& trips, int capacity) {
        map<int, int> d; //差分数组,但只用存对应区间即可,中间不会发生变化
        for(auto trip: trips){
            int num = trip[0], start = trip[1], end=trip[2];
            d[start]+=num;
            d[end]-=num;
        }
        int s = 0;
        for(auto [k, v]: d){ //只有在k所在的索引位置，才会产生值的变动，所以map的话这么遍历是没问题的
            s+=v;
            if(s>capacity) return false;
        }
        return true;
    }
};
```



### （2）[2848. 与车相交的点](https://leetcode.cn/problems/points-that-intersect-with-cars/)

```c++
class Solution {
public:
    int numberOfPoints(vector<vector<int>>& nums) {
        //一开始都是0,用差分做,返回哪些不是0
        vector<int> d(102);
        int maxLength = 0; //统计到这里就可以了
        int cnt = 0;
        for(int i=0;i<nums.size();i++){
            d[nums[i][0]]++;
            d[nums[i][1]+1]--; //注意这个+1!! 因为最后一个是包含的
            maxLength = max(maxLength, nums[i][1]);
        }
        int s = 0;
        for(int i=0;i<maxLength+1;i++){
            s+=d[i];
            cnt += (s!=0);
        }
        return cnt;
    }
};
```



### （3）[1893. 检查是否区域内所有整数都被覆盖](https://leetcode.cn/problems/check-if-all-the-integers-in-a-range-are-covered/)

```c++
class Solution {
public:
    bool isCovered(vector<vector<int>>& ranges, int left, int right) {
        //正常覆盖即可
        vector<int> diff(55);
        for(auto& range: ranges){
            int l = range[0], r = range[1];
            diff[l]++;
            diff[r+1]--;
        }
        int s = 0;
        for(int i=0;i<51;i++){
            s+=diff[i];
            if(i>=left && i<=right){
                if(s==0) return false;
            }
        }
        return true;
    }
};
```



### （4）[1854. 人口最多的年份](https://leetcode.cn/problems/maximum-population-year/)

依旧是简单题：

```c++
class Solution {
public:
    int maximumPopulation(vector<vector<int>>& logs) {
        //计算一下人口数,这个数据量可以用map来记录
        map<int, int> diff;
        for(auto& log: logs){
            int left = log[0], right = log[1];
            diff[left]++;
            diff[right]--;
        }
        int s = 0;
        int max_year = -1;
        int max = -1;
        for(auto [k,v]: diff){
            s+=v;
            if(s>max){
                max = s;
                max_year = k;
            }
        }
        return max_year;
    }
};
```



### （5）[2960. 统计已测试设备](https://leetcode.cn/problems/count-tested-devices-after-test-operations/)

本题的难点在于如何将其转换到差分的思想上去。注意思考问题的时候不要硬往什么板子上靠，可以从原理上来理解。

- 记res为累计每个设备需要下降的电量数。x为每个设备输入的电量数。当`x-res>0`时，说明当前的设备是要被检测的，于是`res+=1`，最后返回`res`值即为要检测的设备数。

代码如下：

```c++
class Solution {
public:
    int countTestedDevices(vector<int>& batteryPercentages) {
        int res = 0;
        for(int i=0;i<batteryPercentages.size();i++){
            if(batteryPercentages[i]-res>0) res++; //>0才会去测试该设备
        }
        return res;
    }
};
```



### （6）[1109. 航班预订统计](https://leetcode.cn/problems/corporate-flight-bookings/)

算是经典差分题目了，返回的也算是还原后的数组。代码如下：

```c++
class Solution {
public:
    vector<int> corpFlightBookings(vector<vector<int>>& bookings, int n) {
        vector<int> diff(n+1);
        for(auto& booking: bookings){
            int left = booking[0]-1, right = booking[1]-1, num = booking[2]; //diff数组是从0开始编号的
            diff[left]+=num;
            diff[right+1]-=num;
        }
        vector<int> res(n);
        int s = 0;
        for(int i=0;i<n;i++){
            s+=diff[i];
            res[i] = s;
        }
        return res;
    }
};
```



### （7）[3355. 零数组变换 I](https://leetcode.cn/problems/zero-array-transformation-i/)

依旧是最基础的差分数组做法：

```c++
class Solution {
public:
    bool isZeroArray(vector<int>& nums, vector<vector<int>>& queries) {
        //可-1可不-1的情况下,-1,如果最后<=0即可
        int n = nums.size();
        vector<int> diff(n+1);  //最后一位其实并不重要,可以理解为只是为了防止越界
        diff[0] = nums[0];
        //差分数组要算出来
        for(int i=1;i<n;i++){
            diff[i] = nums[i]-nums[i-1];
        }
        for(auto& q: queries){
            int left = q[0], right = q[1];
            diff[left]--;
            diff[right+1]++;
        }
        //还原回nums,同时看是否都能<=0
        int s = 0;
        for(int i=0;i<n;i++){
            s+=diff[i];
            if(s>0) return false;
        }
        return true;
    }
};
```



### （8）[56. 合并区间](https://leetcode.cn/problems/merge-intervals/)（值得再做一遍差分做法）

这道题目的难点在于如何正确地写好要输出的内容，根据基础差分板子可以求出每个值是否被覆盖，而求解最后区间的时候，可以对差分数组求前缀和，以还原原数组，看区间覆盖情况（把连续 >0 的段当作合并后的区间）。

- 技巧：考虑`[1,4],[5,6]`这个用例，如果只是按差分数组前缀和>0来判断的话，会得到`[1,6]`，不过按照题目的要求来答案应该是`[1,4],[5,6]`，解决方案是可以把索引全部*2，这样原来相邻的索引就不会被考虑进来了。代码如下：

```c++
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        //中间的不会变,可以考虑用map实现
        map<int, int> diff;
        for(auto& interval: intervals){
            int left = interval[0], right = interval[1];
            diff[left*2]++;
            diff[right*2+1]--; // ！！！不可是diff[(right+1)*2]--;  见👇
        }
        vector<vector<int>> res;
        int s = 0; //>0说明有被覆盖
        int start = -1;
        for(auto [k,v]: diff){
            s+=v;
            if(s>0 && start==-1){
                start = k;
            } else if(s==0 && start!=-1){
                res.push_back({start/2, k/2});
                start = -1;
            }
        }
        return res;
    }
};
```

>👇
>
>`diff[right*2+1]--; // ！！！不可是diff[(right+1)*2]--;  `
>
>因为其实是把right存在夹缝之中 本来是
>
>| | | | | |
>
>|.|.|.|.|.|. *2之后
>
>而`right*2+1`会将right存储在夹缝 “.” 中，如果写成`(right+1)*2` 就还是存在 “|” 中，就实际上就变成重叠了



### （9）[732. 我的日程安排表 III](https://leetcode.cn/problems/my-calendar-iii/)（差分数组法）

不妨先用差分数组的想法来做这道题，可以做，但问题在于每次插入一个新的区间时，都要遍历一遍整个数组找覆盖最多的值，**而这大概就是后面线段树所要优化的地方。**

先用差分数组来做一下这道题目：

```c++
class MyCalendarThree {
public:
    map<int, int> diff;
    MyCalendarThree() {
        
    }
    
    int book(int startTime, int endTime) {
        diff[startTime]++;
        diff[endTime]--; //左闭右开区间,所以右边是endTime   //注意这个时间指的是结束了
        int res = 0;
        int s = 0;
        for(auto& [k, v]: diff){ 
            s += v;
            res = max(res, s);
        }
        return res;
    }
};

/**
 * Your MyCalendarThree object will be instantiated and called as such:
 * MyCalendarThree* obj = new MyCalendarThree();
 * int param_1 = obj->book(startTime,endTime);
 */
```



### （10）[2406. 将区间分为最少组数](https://leetcode.cn/problems/divide-intervals-into-minimum-number-of-groups/)

这个思路一下子没想到，其实**最多被覆盖数就是需要的区间数**，如果按照上下车来理解的话，就是最多在车上的人的人数。**思路的转换还是比较巧的。**

> 这个是会议室模型，只要任意时刻至多有 x 个会议室在同时使用，那么就至多需要 x 个会议室。

代码如下：

```c++
class Solution {
public:
    int minGroups(vector<vector<int>>& intervals) {
        map<int, int> diff;
        for(auto& interval:intervals){
            int left = interval[0], right = interval[1];
            diff[left]++;
            diff[right+1]--;
        }
        int res = 0;
        int s = 0;
        for(auto& [k, v]: diff){
            s += v;
            res = max(res, s);
        }
        return res;
    }
};
```



### （11）[2381. 字母移位 II](https://leetcode.cn/problems/shifting-letters-ii/)

> 补充：C++当中的对负数取模运算。
>
> 在C++中，取余运算符`%`的结果满足以下规则：
> **余数的符号与被除数（左操作数）相同，且绝对值小于除数（右操作数）的绝对值**。
>
> ### **示例分析：`-2 % 3`**
>
> 1. **计算过程**：
>    - 被除数为 `-2`，除数为 `3`。
>    - 商向零取整：`-2 / 3 = 0`（整数除法）。
>    - 余数公式：`余数 = 被除数 - 商 * 除数`
>      `余数 = -2 - (0 * 3) = -2`。
> 2. **结果验证**：
>    - 余数符号与被除数 `-2` 一致（负）。
>    - 余数绝对值 `2` 小于除数绝对值 `3`。
>
> ### **C++取余规则总结**
>
> | **表达式** | **余数符号**   | **余数值** | **验证公式**           |
> | ---------- | -------------- | ---------- | ---------------------- |
> | `-2 % 3`   | 同被除数（负） | `-2`       | `-2 = 0 * 3 + (-2)`    |
> | `2 % -3`   | 同被除数（正） | `2`        | `2 = 0 * (-3) + 2`     |
> | `-5 % 3`   | 负             | `-2`       | `-5 = (-1) * 3 + (-2)` |
> | `5 % -3`   | 正             | `2`        | `5 = (-1) * (-3) + 2`  |
>
> ### **对比数学模运算**
>
> 数学中模运算余数通常非负，例如：
>
> - 数学上 `-2 mod 3 = 1`（因为 `-2 = (-1)*3 + 1`）。
>   但在C++中，`%`运算符是取余（非数学模运算），结果符号由被除数决定。

本题的代码如下：

```c++
class Solution {
public:
    string shiftingLetters(string s, vector<vector<int>>& shifts) {
        //其实需要计算差分并还原字符串即可,
        int n = s.size();
        vector<int> diff(n+1);
        diff[0] = s[0]-'a';
        for(int i=1;i<n;i++){
            diff[i] = s[i]-s[i-1];
        }
        for(auto& shift: shifts){
            int left = shift[0], right =shift[1], num = ((shift[2]==1)?1:-1);
            diff[left]+=num;
            diff[right+1]-=num; //值可能会越界,但这个问题后面再考虑
        }
        string res;
        int sum = 0;
        for(int i=0;i<n;i++){
            sum += diff[i];
            //cout<<diff[i]<<" "<<sum<<" "<<(sum%26+26)%26<<endl;
            res.push_back('a'+((sum%26+26)%26)); //根据经验，不管正的负的，写成这样都能够正确取余运算。
        }
        return res;
    }
};
```



Y

```C++
class Solution {
public:
    string shiftingLetters(string s, vector<vector<int>>& shifts) 
    {
        // map<int,int> diff;
        vector<int> diff(50010,0);
        for(int i=0;i<shifts.size();i++)
        {
            int left = shifts[i][0],right = shifts[i][1],move = shifts[i][2];
            if(move==1)
            {
                diff[left]++;
                diff[right+1]--;//一定要注意+1的问题！！！！
            }
            else
            {
                diff[left]--;
                diff[right+1]++;
            }
        }
        int sSum=0;
        for(int i=0;i<s.size();i++)
        {
            sSum+=diff[i];
            s[i] = ((s[i]-'a'+sSum)%26+26)%26 +'a';
        }
        return s;
    }
};
```



### ==（12）[3453. 分割正方形 I](https://leetcode.cn/problems/separate-squares-i/)（这题只有两个赞，先不做了）==



## §2.2 二维差分

推荐先读一下这篇：[2132. 用邮票贴满网格图 - 力扣（LeetCode）](https://leetcode.cn/problems/stamping-the-grid/solutions/1199642/wu-nao-zuo-fa-er-wei-qian-zhui-he-er-wei-zwiu/)

二维差分和二维前缀和有一些像，重点是能够画出下面这张图：

![image-20250302134239576](Leetcode%E2%80%94%E2%80%94%E5%B8%B8%E7%94%A8%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%93%E9%A2%98.assets/image-20250302134239576.png)



### （1）[2536. 子矩阵元素加 1](https://leetcode.cn/problems/increment-submatrices-by-one/)

**算是板子题。**既涉及到了差分数组的更新，又涉及到了如何用二维差分数组还原出原来的数组（**计算原数组的时候使用二维前缀和来做**）。代码如下：

```c++
class Solution {
public:
    vector<vector<int>> rangeAddQueries(int n, vector<vector<int>>& queries) {
        vector<vector<int>> diff(n+2, vector<int>(n+2)); //差分外面多一圈,前缀和里面多一圈,不如直接把大小设置为n+2,计算完前缀和之后,取中间n*n即为最终结果
        for(auto& q: queries){
            int r1 = q[0]+1, c1 = q[1]+1, r2=q[2]+1, c2=q[3]+1;
            diff[r1][c1]+=1;
            diff[r2+1][c1]-=1;
            diff[r1][c2+1]-=1;
            diff[r2+1][c2+1]+=1;
        }
        //还原原来的数组
        for(int i=1;i<=n;i++){
            for(int j=1;j<=n;j++){
                //二维前缀和，注意这里是+=，相当于diff[i][j] = diff[i][j-1]+diff[i-1][j]-diff[i-1][j-1]+diff[i][j];
                diff[i][j] += diff[i][j-1]+diff[i-1][j]-diff[i-1][j-1];
            }
        }
        //移除外面0那一圈,保留中间n*n的取余,即为答案
        diff.pop_back();
        diff.erase(diff.begin());
        for(auto& row:diff){
            row.pop_back();
            row.erase(row.begin());
        }
        return diff;
    }
};
```



# 三、栈

## ==1.[1441. 用栈操作构建数组](https://leetcode.cn/problems/build-an-array-with-stack-operations/)==

这题先不做了，有点意义不明，且难度也比较低。



## 2.[844. 比较含退格的字符串](https://leetcode.cn/problems/backspace-string-compare/)

可以直接用两个栈作比较，如下：
```c++
class Solution {
public:
    bool backspaceCompare(string s, string t) {
        //用两个栈来比较s和t中的内容
        stack<char> stks;
        stack<char> stkt;
        for(int i=0;i<s.size();i++)
        {
            if(s[i]=='#')
            {
                if(!stks.empty()) stks.pop();
            }
            else stks.push(s[i]);
        }

        for(int i=0;i<t.size();i++)
        {
            if(t[i]=='#')
            {
                if(!stkt.empty()) stkt.pop();
            }
            else stkt.push(t[i]);
        }

        //从栈顶开始比较两个栈中的内容是否一致
        if(stks.empty()&&stkt.empty()) return true;
        while(!stks.empty() && !stkt.empty())
        {
            char c1 = stks.top(), c2 = stkt.top();
            if(c1!=c2) return false;
            stks.pop(); 
            stkt.pop();
        }
        return (stks.empty()&&stkt.empty());
    }
};
```

不过这种做法比较麻烦，实际上可以直接在字符串上做操作，来模拟一个栈，这样还更好比较。代码如下：

```c++
class Solution {
public:
    string build(string s)
    {
        //返回做了#退格处理之后的结果
        string res;
        for(int i=0;i<s.size();i++)
        {
            if(s[i]=='#'&&!res.empty()) res.pop_back();
            else if(s[i]!='#') res.push_back(s[i]);
        }
        return res;
    }
    bool backspaceCompare(string s, string t) {
        return build(s)==build(t);
    }
};
```



## 3.[682. 棒球比赛](https://leetcode.cn/problems/baseball-game/)

直接用栈模拟应该没问题，也可以用`vector`去计算操作，不过复杂度是一样的，就不额外尝试了。

```c++
class Solution {
public:
    int calPoints(vector<string>& operations) {
        //"C,D,+"其实都不需要特意入栈,只要操作之后把结果入栈即可
        stack<int> scores;
        for(string& s: operations)
        {
            if(s=="C")
            {
                scores.pop();
            }
            else if(s=="D")
            {
                int num = scores.top();
                scores.push(num*2);
            }
            else if(s=="+")
            {
                int num = scores.top();
                scores.pop();
                int num2 = scores.top();
                scores.push(num);
                scores.push(num+num2);
            }
            else
            {
                scores.push(stoi(s));
            }
        }
        //把栈里的值加在一起
        int sum = 0;
        while(!scores.empty())
        {
            sum+=scores.top();
            scores.pop();
        }
        return sum;
    }
};
```



## 4.[2390. 从字符串中移除星号](https://leetcode.cn/problems/removing-stars-from-a-string/)

```c++
class Solution {
public:
    string removeStars(string s) {
        //*其实就是退格符
        string res;
        for(int i=0;i<s.size();i++)
        {
            if(s[i]=='*')
            {
                if(!res.empty()) res.pop_back();
            } 
            else
            {
                res.push_back(s[i]);
            }
        }
        return res;
    }
};
```

Y 

```C++
class Solution {
public:
    string removeStars(string s) 
    {
        vector<char> res;
        for(int i=0;i<s.size();i++)
        {
            if(s[i]=='*'&&!res.empty())
            {
                res.pop_back();
            }
            else
            {
                res.push_back(s[i]);
            }
        }
        return string(res.begin(),res.end());
    }
};
```



## 5.[1472. 设计浏览器历史记录](https://leetcode.cn/problems/design-browser-history/)

**这道题目有一定的模拟题的性质，需要仔细考虑。**用数组模拟一个栈即可，每次push进来都放到数组后面，后退 `steps` 步或前进 `steps` 步都仅仅会修改当前的索引值，而`visit`操作则会一直删除数组后面的元素，直到`visit`指定的url。代码如下：

> 写的时候，要注意在`back`和`forward`的时候，别忘了更新现在`cur`的值。

```c++
class BrowserHistory {
public:
    vector<string> histories;
    int cur = 0; //当前浏览的网页是histories[cur]
    BrowserHistory(string homepage) {
        histories.push_back(homepage);
    }
    
    void visit(string url) {
        //当前为最新浏览网页,后面的都不要了
        cur++;
        histories.resize(cur);//！！！！！！！！！！！！！！！！！！
        histories.push_back(url);
    }
    
    string back(int steps) {
        int index = max(0, cur-steps);
        //记得把cur移动过去,下面函数也是类似
        cur = index;
        return histories[cur];
    }
    
    string forward(int steps) {
        int n = histories.size(); 
        int index = min(cur+steps, n-1); //直接min(cur+steps, histories.size()-1)是会报错的,因为histories.size()不是int类型,更多见https://cplusplus.com/reference/vector/vector/size/
        cur = index;
        return histories[cur];
    }
};

/**
 * Your BrowserHistory object will be instantiated and called as such:
 * BrowserHistory* obj = new BrowserHistory(homepage);
 * obj->visit(url);
 * string param_2 = obj->back(steps);
 * string param_3 = obj->forward(steps);
 */
```



## 6.[946. 验证栈序列](https://leetcode.cn/problems/validate-stack-sequences/)

这道题目也算是一道小模拟题，但可能会经常做错（H本人）。每次都先按照入栈序列push进来，再按照出栈序列看看能不能出栈，最后返回栈是否为空即可。

```c++
class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        //即便是popped和pushed对应,popped对应的索引也不会越界
        stack<int> stk;
        int n = pushed.size();
        for(int i=0, j=0;i<n;i++)
        {
            stk.push(pushed[i]); //固定一定把pushed对应的值放入栈
            while(!stk.empty()&&stk.top()==popped[j]) //!!!!!记得判断!stk.empty()
            {
                stk.pop();
                j++; //j不会越界,因为题目说了popped.length==pushed.length
            }
        }
        return stk.empty();
    }
};
```



## 7.[3412. 计算字符串的镜像分数](https://leetcode.cn/problems/find-mirror-score-of-a-string/)

想了一下，直接看答案了hhh。需要体会一下栈的思想。本题对每个字母维护一个栈，还是非常巧妙的。

```c++
class Solution {
public:
    long long calculateScore(string s) {
        //镜像表示字母表中索引相加为26
        //暴力做的话复杂度是O(n^2),注意是距离最近的,考虑用栈
        vector<stack<int>> alphaStk(26);
        //1.如果镜像的栈为空,则放入当前字母栈;否则从镜像栈里弹出一个元素,计算分数并累加
        long long score = 0;
        for(int i=0;i<s.size();i++)
        {
            int index = s[i] - 'a';
            int mirror = 25-index;
            if(!alphaStk[mirror].empty())
            {
                int t = alphaStk[mirror].top();
                alphaStk[mirror].pop();
                score+=(long long)(i-t);
            }
            else
            {
                alphaStk[index].push(i); //把当前索引放入对应字母栈中
            }
        }
        return score;
    }
};
```



## 8.[71. 简化路径](https://leetcode.cn/problems/simplify-path/)（难点：写出干净清晰的代码）

感觉上应该能做，但自己写了一些感觉有点埋汰，就来看看优质代码怎么写。以下代码感觉还是比较优雅的：

> 题意抽象为如下，就会简单很多：
>
> 给你一组由 `/` 隔开的字符串（忽略空串和 `.`），请你从左到右遍历这些字符串，依次删除每个 `..` 及其左侧的字符串（模拟返回上一级目录）。
>
> **解决思路：**
>
> 把 path 用 / 分割，得到一个字符串列表。
>
> 遍历字符串列表的同时，用栈维护遍历过的字符串：
>
> - 如果当前字符串是空串或者 `.`，什么也不做（跳过）。
> - 如果当前字符串不是 `..`，那么把字符串入栈。
> - 否则弹出栈顶字符串（前提是栈不为空），模拟返回上一级目录。
>
> 最后把栈中字符串用 / 拼接起来（最前面也要有个 /）。
>
> 补充知识：
>
> - C++中的`istringstream`：[C++ istringstream用法详解_天选打工仔 inurl:csdn-CSDN博客](https://blog.csdn.net/weixin_41028555/article/details/136907277)
> - C++中的`getline`：[C++中getline()的用法-CSDN博客](https://blog.csdn.net/weixin_44480968/article/details/104282535#:~:text=getline是C++标准库函数；它有两种形式，一种是头文件< istream)

优雅！

```c++
class Solution {
public:
    string simplifyPath(string path) {
        vector<string> stk;
        istringstream ss(path);
        string s; //接收每个子字符串
        while(getline(ss, s, '/')) //以/间隔
        {
            if(s.empty() || s==".") {continue;} //只有一个.,此时忽略掉即可
            else if(s=="..")
            {
                if(!stk.empty()) stk.pop_back();
            }
            else
            {
                stk.push_back(s);
            }
        }
        string result;
        result+="/";
        for(int i=0;i<stk.size();i++)
        {
            result+=stk[i];
            if(i<stk.size()-1) result+="/";
        }
        return result;
    }
};
```

> ```cpp
>  vector<string> names = split(path, '/');也可以
> ```



## 9.[3170. 删除星号以后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-minimum-string-after-removing-stars/)

> 要点在于贪心的思路：每次要删除的时候，我们总是**尽量删除索引大的下标**，这样可以让剩下的字符串的字典序尽可能小。

```c++
class Solution {
public:
    string clearStars(string s) {
        vector<vector<int>> stk(26);
        for(int i=0;i<s.size();i++)
        {
            if(s[i]=='*')
            {
                for(int j=0;j<26;j++)
                {
                    if(!stk[j].empty())
                    {
                        stk[j].pop_back();
                        break;
                    }
                }
            }
            else
            {
                stk[s[i]-'a'].push_back(i);
            }
        }
        vector<int> index;
        for(int i=0;i<26;i++)
        {
            index.insert(index.end(), stk[i].begin(), stk[i].end());
        }
        sort(index.begin(), index.end());
        string res;
        for(int i=0;i<index.size();i++)
        {
            res.push_back(s[index[i]]);
        }
        return res;

    }
};
```

