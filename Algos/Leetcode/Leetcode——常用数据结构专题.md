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



### （7）[1014. 最佳观光组合](https://leetcode.cn/problems/best-sightseeing-pair/)