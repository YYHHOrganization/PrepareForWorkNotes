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

## 1.前缀和基础

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



## 2.前缀和与哈希表

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
        umap[sum]--;
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



###  2588. 统计美丽子数组数目 1697

###  525. 连续数组

###  面试题 17.05. 字母与数字 同 525 题

###  3026. 最大好子数组和 1817

