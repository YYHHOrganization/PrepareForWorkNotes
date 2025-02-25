# Leetcode——二分算法专题

参考：[分享丨【题单】二分算法（二分答案/最小化最大值/最大化最小值/第K小） - 力扣（LeetCode）](https://leetcode.cn/circle/discuss/SqopEo/)

# 一、基础

## 1.[34. 在排序数组中查找元素的第一个和最后一个位置 - 力扣（LeetCode）](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/description/)

一道算是板子题的题目，需要记住对应的写法：

```c++
class Solution {
public:
    int lower_bound(vector<int>& nums, int target){ //求解第一个>=target的索引
        int left = 0, right = nums.size()-1;
        while(left<=right){ //记住:左闭右闭的写法
            int mid = ((left+right)>>1); //本题不会越界
            if(nums[mid]<target){
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return left; 
    }
    vector<int> searchRange(vector<int>& nums, int target) {
        //求解第一个>=target的值,作为左边界
        int lower = lower_bound(nums, target);
        if(lower==nums.size() || nums[lower]>target){
            //此时不用再算右边界了
            return {-1,-1};
        }
        //此时一定有右边界,因为至少有一个数相等,计算最后一个<=target的数,等同于第一个>target的数索引-1,等同于第一个>=(target+1)的数索引-1
        int upper = lower_bound(nums, target+1)-1;
        return {lower, upper};
    }
};
```



## 2.[35. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/)

一道非常常规的板子题：

```c++
class Solution {
public:
    int lower_bound(vector<int>& nums, int target){
        int left = 0, right = nums.size()-1;
        while(left<=right){
            int mid = left + ((right-left)>>1);
            if(nums[mid]<target){
                left = mid+1;
            } else right = mid-1;
        }
        return left;
    }
    int searchInsert(vector<int>& nums, int target) {
        //找到第一个>=target的值
        int index = lower_bound(nums, target); //放入到第一个>=target的位置
        return index; 
    }
};
```



## 3.[2529. 正整数和负整数的最大计数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-count-of-positive-integer-and-negative-integer/description/)

```c++
class Solution {
public:
    int lower_bound(vector<int>& nums, int target){
        int left = 0, right = nums.size()-1;
        while(left<=right){
            int mid = left+ ((right-left)>>1);
            if(nums[mid]<target){
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }
    int maximumCount(vector<int>& nums) {
        //找到最后一个<0的索引,以及第一个>0的索引
        int negIndex = lower_bound(nums, 0) - 1; //第一个>=0的索引-1
        int posIndex = lower_bound(nums, 1); //第一个>=1的索引
        int n = nums.size();
        return max(negIndex+1, n-posIndex);
    }
};
```



# 二、进阶

部分题目需要先排序，然后在有序数组上二分查找。

## 1.[2300. 咒语和药水的成功对数](https://leetcode.cn/problems/successful-pairs-of-spells-and-potions/)

对于二分的题目来说，千万不要不要忘了sort！！

```c++
class Solution {
public:
    int lower_bound(vector<int>& potions, long long target){
        int left = 0, right = potions.size()-1;
        while(left<=right){
            int mid = left + ((right-left)>>1);
            if((long long)potions[mid]<target){
                left = mid + 1;
            } else{
                right = mid - 1;
            }
        }
        return left;
    }
    vector<int> successfulPairs(vector<int>& spells, vector<int>& potions, long long success) {
        //找到potions第一个>= ceil(success/spells[cur])的元素,该元素以及后面的都可以成功
        sort(potions.begin(), potions.end());
        int n = spells.size();
        int m = potions.size();
        vector<int> res(n);
        for(int i=0;i<n;i++){
            long long target = (success + spells[i] - 1) / spells[i]; //向上取整
            int index = lower_bound(potions, target);
            res[i] = m - index;
        }
        return res;
    }
};
```

