# Leetcode——滑动窗口与双指针专题

> 秋招一轮刷题：暂定阈值为1700，难度在1700以上的先放一放，抓紧把1700以下的专题刷完。

可以参考：[分享丨【题单】滑动窗口与双指针（定长/不定长/单序列/双序列/三指针/分组循环） - 力扣（LeetCode）](https://leetcode.cn/circle/discuss/0viNMK/)

# 一、定长滑动窗口

基础套路（[1343. 大小为 K 且平均值大于等于阈值的子数组数目 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/description/)）：

```c++
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        int n=arr.size();
        int res=0;
        int sum=0;
        int thresholdSum = threshold*k;
        for(int i=0;i<n;i++)
        {
            //1、inset
            sum+=arr[i];//假设k是3个 inset步骤 从2加到3
            if(i<k-1)continue;//判断下标是否小于2(是否小于3个元素)
            //2、update
            if(sum>=thresholdSum)res+=1;//判断一下总的sum,因为现在是3个元素
            //3、delete
            sum-=arr[i-k+1];//扣掉一个元素 回到2个元素

        }
        return res;
    }
};
```



## 1.[大小为 K 且平均值大于等于阈值的子数组数目](https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/)

经典套路题，直接给出代码：

```c++
class Solution {
public:
    int numOfSubarrays(vector<int>& arr, int k, int threshold) {
        int target = k * threshold;
        int sum = 0;
        int cnt = 0;
        for(int i=0;i<arr.size();i++){
            sum+=arr[i]; //1.inset
            if(i<k-1) continue;
            //2.update
            if(sum>=target){
                cnt++;
            }
            //3.delete
            sum -= arr[i-k+1];
        }
        return cnt;
    }
};
```



## 2.[1052. 爱生气的书店老板](https://leetcode.cn/problems/grumpy-bookstore-owner/)

一道定长滑动窗口的变形题，**定长滑动窗口题目，一定要想明白窗口里面要维护什么**。

```c++
class Solution {
public:
    int maxSatisfied(vector<int>& customers, vector<int>& grumpy, int minutes) {
        //1.计算完全不使用技巧,能让多少顾客满意 sum
        //2.维护使用技巧可以让区间内新增满意顾客的数量,即为滑动窗口维护的值
        int sum = 0;
        int newSatisfiedSum = 0;
        int maxSatisfied = 0;
        for(int i=0;i<customers.size();i++){
            //1.inset
            sum += customers[i] * (grumpy[i]==0);
            newSatisfiedSum += (grumpy[i]==1) * customers[i]; //这样,如果老板生气了,可以矫正回来,认为是新增满意顾客的数量
            if(i<minutes-1) continue;
            //2.update
            maxSatisfied = max(maxSatisfied, newSatisfiedSum);
            //3.delete
            newSatisfiedSum -= (grumpy[i-minutes+1]==1) * customers[i-minutes+1];
        }
        return maxSatisfied + sum;
    }
};
```



## 3.[2461. 长度为 K 子数组中的最大和](https://leetcode.cn/problems/maximum-sum-of-distinct-subarrays-with-length-k/)

主要是要思考“子数组中的所有元素 **各不相同**”要怎么用代码来表示。这道题的代码如下：

```c++
class Solution {
public:
    long long maximumSubarraySum(vector<int>& nums, int k) {
        long long sum = 0;
        unordered_map<int, int> umap; //key:数字, value:出现频率
        long long res = 0;
        for(int i=0;i<nums.size();i++){
            //1.inset
            sum += nums[i];
            umap[nums[i]]++;
            if(i<k-1) continue;
            //2.update
            if(umap.size()==k){
                res = max(res, sum);
            }
            //3.delete
            umap[nums[i-k+1]]--;
            sum-=nums[i-k+1];
            if(umap[nums[i-k+1]]==0) umap.erase(nums[i-k+1]);
        }
        return res;
    }
};
```



## 4.[1423. 可获得的最大点数](https://leetcode.cn/problems/maximum-points-you-can-obtain-from-cards/)

这道题目的启示是：如果转换解决问题的思路为改变窗口的大小，则需要注意**窗口大小为0的情况**。这种求和问题也可以直接用C++的`accumulate`函数加快写代码的效率，这里给出这种做法：

```c++
class Solution {
public:
    int maxScore(vector<int>& cardPoints, int k) {
        //用求和函数加快计算
        int n = cardPoints.size();
        int sum = accumulate(cardPoints.begin(), cardPoints.end(), 0); //别忘了最后一个参数
        if(n==k) return sum; //注意特殊情况判断
        int tmpSum = accumulate(cardPoints.begin(), cardPoints.begin()+n-k, 0); //前n-k个值之和
        int res = tmpSum;
        //求解窗口大小为n-k的最小点数
        for(int i=n-k;i<n;i++){
            tmpSum += (cardPoints[i] - cardPoints[i-(n-k)]); //一次更新两端
            res = min(res, tmpSum);
        }
        return sum - res;
    }
};
```



## 5.（简单题）[1652. 拆炸弹](https://leetcode.cn/problems/defuse-the-bomb/)

利用定长滑动窗口的做法，考虑用$O(n)$的复杂度解决这道题目。这种算是模拟题，可以画一下图推导一下下标索引，**千万不要硬着头皮想。**本题的难点就在于索引值的判定，代码如下：

```c++
class Solution {
public:
    vector<int> decrypt(vector<int>& code, int k) {
        int sum = 0;
        int n = code.size();
        vector<int> res(n);
        //考虑时间复杂度为O(n)的做法
        if(k<0){
            k=-k;
            //先计算第一个数替换的值
            for(int i=n-1;i>n-k-1;i--){
                sum+=code[i];
            }
            res[0] = sum;
            //此时用前面k个数字之和替换
            for(int i=1;i<code.size();i++){
                sum += (code[i-1]-code[(i-k+n-1)%n]); //取余运算
                res[i] = sum;
            }
        } else if(k>0){
            //从后往前算
            for(int i=0;i<k;i++) sum+=code[i];
            res[n-1]=sum;
            for(int i=n-2;i>=0;i--){
                sum += (code[i+1]-code[(i+k+1)%n]);
                res[i] = sum;
            }
        }
        return res;
    }
};
```



## 6.[1461. 检查一个字符串是否包含所有长度为 K 的二进制子串](https://leetcode.cn/problems/check-if-a-string-contains-all-binary-codes-of-size-k/)

通过这道题目，可以先来复习一下C++中`string`的`substr`函数用法。用这种方法来做可以秒掉这道题：

```c++
class Solution {
public:
    bool hasAllCodes(string s, int k) {
        int n = s.size();
        if((n-k+1)<(1<<k)) return false; //此时子串数量少于长度为k的二进制字符串数量
        unordered_set<string> us;
        for(int i=0;i<n-k+1;i++){
            string sub = s.substr(i, k);
            us.insert(std::move(sub));
        }
        return (us.size()==(1<<k));
    }
};
```

如果要用滑动窗口来做，可以考虑在窗口移动的时候，窗口内的值的变化情况。此时考察的就是一些位运算了，方法2的代码如下：

```c++
class Solution {
public:
    bool hasAllCodes(string s, int k) {
        int n = s.size();
        unordered_set<int> us;
        int sum = 0;
        for(int i=0;i<n;i++){
            //1.inset
            int in = s[i]-'0';
            sum = ((sum<<1) | in);
            if(i<k-1) continue;
            //2.update
            us.insert(sum);
            //3.delete
            int out = s[i-k+1]-'0';
            sum -= (out<<(k-1));
        }
        return (us.size()==(1<<k));
    }
};
```



## 7.[2269. 找到一个数字的 K 美丽值 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-k-beauty-of-a-number/)
