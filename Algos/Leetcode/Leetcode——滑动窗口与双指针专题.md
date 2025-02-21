# Leetcode——滑动窗口与双指针专题

> 秋招一轮刷题：暂定阈值为1700，难度在1700以上的先放一放，抓紧把1700以下的专题刷完。

可以参考：[分享丨【题单】滑动窗口与双指针（定长/不定长/单序列/双序列/三指针/分组循环） - 力扣（LeetCode）](https://leetcode.cn/circle/discuss/0viNMK/)

**定长滑动窗口**

- [x] 定长子串中元音的最大数目 1263
- [x] 子数组最大平均数 I
- [x] 大小为 K 且平均值大于等于阈值的子数组数目 1317
- [x] 半径为 k 的子数组平均值 1358
- [x] 得到 K 个黑块的最少涂色次数 1360
- [x] 爱生气的书店老板 1418
- [x] 几乎唯一子数组的最大和 1546
- [x] 长度为 K 子数组中的最大和 1553
- [x] 可获得的最大点数 1574
- [x] 拆炸弹 做到 O(n)
- [ ] 健身计划评估（会员题）
- [ ] 长度为 K 的无重复字符子串（会员题）
- [ ] 每个子数组的数字种类数（会员题）
- [ ] 最少交换次数来组合所有的 1（会员题）
- [ ] 分享 K 个糖果后独特口味的数量（会员题）
- [x] 检查一个字符串是否包含所有长度为 K 的二进制子串 1504
- [ ] 最少交换次数来组合所有的 1 II 1748
- [ ] 子串的最大出现次数 1748
- [ ] 滑动子数组的美丽值 1786
- [ ] 使二进制字符串字符交替的最少反转次数 2006
- [ ] 字符串的排列
- [ ] 找到字符串中所有字母异位词
- [ ] 串联所有单词的子串
- [ ] 查找给定哈希值的子串 2063
- [ ] 统计完全子字符串 2449
- [ ] 子串能表示从 1 到 N 数字的二进制串 做到 O(∣s∣)
- [ ] K 个关闭的灯泡（会员题）做到 O(n)
- [ ] 等计数子串的数量（会员题）
- [ ] 子数组的最大频率分数（会员题）
- [x] [2269. 找到一个数字的 K 美丽值](https://leetcode.cn/problems/find-the-k-beauty-of-a-number/) 1280
- [x] [1984. 学生分数的最小差值](https://leetcode.cn/problems/minimum-difference-between-highest-and-lowest-of-k-scores/) 1306
- [ ] [220. 存在重复元素 III](https://leetcode.cn/problems/contains-duplicate-iii/)



**不定长滑动窗口**

§2.1 求最长/最大

- [x] 无重复字符的最长子串
- [x] 每个字符最多出现两次的最长子字符串 1329
- [x] 删掉一个元素以后全为 1 的最长子数组 1423
- [ ] 尽可能使字符串相等 1497
- [ ] 找到最长的半重复子字符串 1502
- [ ] 水果成篮 1516
- [ ] 删除子数组的最大得分 1529
- [ ] 最多 K 个重复元素的最长子数组 1535
- [ ] 数组的最大美丽值 1638
- [ ] 考试的最大困扰度 1643
- [ ] 最大连续 1 的个数 III 1656
- [ ] 

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

这道题目本身并不难，难点在于对C++字符串相关接口的熟练应用。一个是`tostring(num)`接口，一个是`stoi(s)`接口。虽然本题用滑动窗口法的话不一定能用上这俩接口，但还是要记住的。本题代码如下：

```c++
class Solution {
public:
    int divisorSubstrings(int num, int k) {
        int sum = 0; //维护窗口内的值
        string s = to_string(num);
        int cnt = 0;
        for(int i=0;i<s.size();i++){
            //1.inset
            int in = s[i]-'0';
            sum = sum * 10 + in;
            if(i<k-1) continue;
            //2.update
            if(sum!=0 && num%sum==0) cnt++; //注意题意:0不能整除任何值
            //3.delete
            int out = s[i-k+1]-'0';
            sum -= out * pow(10, k-1);
        }
        return cnt;
    }
};
```

枚举所有长度为`k`的子串，可以用以下`string`中的接口：

```c++
for (int i = 0; i <= n - k; ++i) {
    // 枚举所有长度为 k 的子串
    int tmp = stoi(s.substr(i, k));
    if (tmp && num % tmp == 0) {
        ++res;
    }
}
```



## 8.[1984. 学生分数的最小差值](https://leetcode.cn/problems/minimum-difference-between-highest-and-lowest-of-k-scores/)

可以简化运算，这里为了保持三部曲写的麻烦一点，但非常好理解：

```c++
class Solution {
public:
    int minimumDifference(vector<int>& nums, int k) {
        //思路很清晰,排序后定长滑动窗口
        sort(nums.begin(), nums.end());
        int res = INT_MAX;
        for(int i=0;i<nums.size();i++){
            //1.inset
            if(i<k-1) continue;
            //2.update
            res = min(res, nums[i]-nums[i-k+1]);
            //3.delete
        }
        return res;
    }
};
```



## ==9.[220. 存在重复元素 III](https://leetcode.cn/problems/contains-duplicate-iii/)（困难，还没做）==





# 二、不定长滑动窗口

## 1.求最长/最大

一般题目都有「至多」的要求。

- 与定长滑动窗口套路是类似的，在外层`for`循环中维护r指针，如果不满足要求则移动`l`指针直到满足要求为止。

### （1）[3. 无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/)

代码如下：

```c++
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_map<char, int> umap; //存储每个字符出现的次数
        int res = 0;
        int l=0;
        for(int r=0;r<s.size();r++){
            umap[s[r]]++;
            while(umap[s[r]]>1){
                umap[s[l]]--;
                l++;
            }
            if(l<=r) res = max(res, r-l+1);
        }
        return res;
    }
};
```



### （2）[3090. 每个字符最多出现两次的最长子字符串](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/)

跟上一题比较类似，代码如下：

```c++
class Solution {
public:
    int maximumLengthSubstring(string s) {
       int l=0;
       int res = 0;
       unordered_map<char, int> umap; //key:字符 value:出现次数
       for(int r=0;r<s.size();r++){
            umap[s[r]]++;
            while(umap[s[r]]>2){
                umap[s[l]]--;
                l++;
            }
            if(l<=r) res = max(res, r-l+1);
       } 
        return res;
    }
};
```



### （3）[1493. 删掉一个元素以后全为 1 的最长子数组](https://leetcode.cn/problems/longest-subarray-of-1s-after-deleting-one-element/)

题解如下（也可以用动规做，但暂时还没看，这里只整理滑动窗口的解法：）

```c++
class Solution {
public:
    int longestSubarray(vector<int>& nums) {
        //一个0没事,一旦出现两个零就要缩到一个零,维护窗口内最多一个0时的最大值
        int zeroCnt = 0; //记录窗口内0的个数
        int res = 0;
        int j = 0;
        for(int i=0;i<nums.size();i++){
            if(nums[i]==0){
                if(zeroCnt<2) zeroCnt++;
                if(zeroCnt==2){
                    while(nums[j]!=0){ //让窗口内最多只能有一个0
                        j++;
                    }
                    j++; //++之后指到了不是0的位置
                    zeroCnt--;
                }
            }
            if(j<=i) res = max(res, i-j+1);
        }
        return res-1; //不得不删除一个元素,即使没有0
    }
};
```

