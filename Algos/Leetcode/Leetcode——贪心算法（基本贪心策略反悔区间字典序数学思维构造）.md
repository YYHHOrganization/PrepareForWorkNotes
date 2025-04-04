# 贪心算法（基本贪心策略/反悔/区间/字典序/数学/思维/构造）

链接：https://leetcode.cn/discuss/post/g6KTKL/

前言
为方便大家练习，我把比较套路的贪心题目放在前面，更灵活的思维题和构造题放在后面。每个小节的题目均按照从易到难的顺序排列。

**如果做题时没有思路，推荐看看本文第五章的「思考清单」。**

# 一、贪心策略
有两种**基本贪心策略**：

从**最小/最大**开始贪心，优先考虑最小/最大的数，从小到大/从大到小贪心。在此基础上，衍生出了**反悔贪心**。
从**最左/最右**开始贪心，思考第一个数/最后一个数的贪心策略，把 n 个数的原问题转换成 n−1 个数（或更少）的子问题。

## §1.1 从最小/最大开始贪心
优先考虑最小/最大的数，从小到大/从大到小贪心。

如果答案与数组元素顺序无关，一般需要**排序**。排序后，可以遍历计算。



### [3074. 重新分装苹果](https://leetcode.cn/problems/apple-redistribution-into-boxes/)

给你一个长度为 `n` 的数组 `apple` 和另一个长度为 `m` 的数组 `capacity` 。

一共有 `n` 个包裹，其中第 `i` 个包裹中装着 `apple[i]` 个苹果。同时，还有 `m` 个箱子，第 `i` 个箱子的容量为 `capacity[i]` 个苹果。

请你选择一些箱子来将这 `n` 个包裹中的苹果重新分装到箱子中，返回你需要选择的箱子的 **最小** 数量。

**注意**，同一个包裹中的苹果可以分装到不同的箱子中。

**示例 1：**

```
输入：apple = [1,3,2], capacity = [4,3,1,5,2]
输出：2
解释：使用容量为 4 和 5 的箱子。
总容量大于或等于苹果的总数，所以可以完成重新分装。
```



返回需要选择的箱子的 **最小** 数量。

```C++
class Solution {
public:
    int minimumBoxes(vector<int>& apple, vector<int>& capacity) {
        //n 包裹  放apple[i] 个苹果
        //sumApple
        //m 箱子  放capacity[i] 个苹果
        //排序 先用大箱子 装 
        sort(capacity.begin(),capacity.end(),greater<int>{});
        int appleSum = reduce(apple.begin(),apple.end());
        int res=0;
        while(appleSum>0)
        {
            appleSum-=capacity[res];
            res++;
        }
        return res;
    }
};
```



### [2279. 装满石头的背包的最大数量](https://leetcode.cn/problems/maximum-bags-with-full-capacity-of-rocks/)

现有编号从 `0` 到 `n - 1` 的 `n` 个背包。给你两个下标从 **0** 开始的整数数组 `capacity` 和 `rocks` 。第 `i` 个背包最大可以装 `capacity[i]` 块石头，当前已经装了 `rocks[i]` 块石头。另给你一个整数 `additionalRocks` ，表示你可以放置的额外石头数量，石头可以往 **任意** 背包中放置。

请你将额外的石头放入一些背包中，并返回放置后装满石头的背包的 **最大** 数量*。*

**示例 1：**

```
输入：capacity = [2,3,4,5], rocks = [1,2,4,4], additionalRocks = 2
输出：3
解释：
1 块石头放入背包 0 ，1 块石头放入背包 1 。
每个背包中的石头总数是 [2,3,4,4] 。
背包 0 、背包 1 和 背包 2 都装满石头。
总计 3 个背包装满石头，所以返回 3 。
可以证明不存在超过 3 个背包装满石头的情况。
注意，可能存在其他放置石头的方案同样能够得到 3 这个结果。
```



```C++
class Solution {
public:
    int maximumBags(vector<int>& capacity, vector<int>& rocks, int additionalRocks) {
        int n = capacity.size();
        //剩余容量
        for(int i=0;i<n;i++) 
            capacity[i]-=rocks[i];
        sort(capacity.begin(),capacity.end()); // 剩余容量从小到大排序
        int i=0;
        while(i<n&&additionalRocks>=capacity[i])
        {
            additionalRocks-=capacity[i++];
        }
        return i;
    }
};
```



### [1833. 雪糕的最大数量 ](https://leetcode.cn/problems/maximum-ice-cream-bars/) 同上题（有一种计数排序的做法，但还没看，先用贪心吧）

```C++
class Solution {
public:
    int maxIceCream(vector<int>& costs, int coins) 
    {
        sort(costs.begin(),costs.end());
        int i=0;
        while(i<costs.size()&& coins>=costs[i])
        {
            coins-=costs[i++];
        }
        return i;
    }
};
```



### [1005. K 次取反后最大化的数组和](https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations/)

给你一个整数数组 `nums` 和一个整数 `k` ，按以下方法修改该数组：

- 选择某个下标 `i` 并将 `nums[i]` 替换为 `-nums[i]` 。

重复这个过程恰好 `k` 次。可以多次选择同一个下标 `i` 。

以这种方式修改数组后，返回数组 **可能的最大和** 。

**示例 1：**

```
输入：nums = [4,2,3], k = 1
输出：5
解释：选择下标 1 ，nums 变为 [4,-2,3] 。
```



这个做法排序了，复杂度应该会高  有更快的 有O(n+C)的 但是官方代码写得很烂，暂时不想看

```C++
class Solution {
public:
    int largestSumAfterKNegations(vector<int>& nums, int k) {
        //1、尽量让负的为正
        //2、如果负的都是正的了，然后还多了n次
        //n偶数，不变 翻同一个值
        //n奇数，翻一次绝对值最小的

        sort(nums.begin(),nums.end());
        int i=0;
        for(i=0;i<nums.size();i++)
        {
            if(nums[i]<0&&k>0)
            {
                nums[i]=-nums[i];
                k--;
            }
            else
            {
                break;
            }
        }
        int sum = reduce(nums.begin(),nums.end());
        if(k>0)
        {
            //表示可以翻偶数次某个数，最后翻回原值
            if(k%2==0)
            {
                return sum;
            }
            else
            {
                int minNum = *min_element(nums.begin(),nums.end());
                sum-=2*minNum;
            }
        }
        return sum;

    }
};
```



### [1481. 不同整数的最少数目](https://leetcode.cn/problems/least-number-of-unique-integers-after-k-removals/)

给你一个整数数组 `arr` 和一个整数 `k` 。现需要从数组中恰好移除 `k` 个元素，请找出移除后数组中不同整数的最少数目。

**示例 1：**

```
输入：arr = [5,5,4], k = 1
输出：1
解释：移除 1 个 4 ，数组中只剩下 5 一种整数。
```

```C++
class Solution {
public:
    int findLeastNumOfUniqueInts(vector<int>& arr, int k) {
        //尽量把出现频率低的移除
        unordered_map<int,int> umap;
        int n=arr.size();
        for(int i=0;i<n;i++)
        {
            umap[arr[i]]++;
        }
        //排序
        vector<pair<int,int>> vec(umap.begin(),umap.end());
        sort(vec.begin(),vec.end(),[](const auto& a,const auto& b){return a.second<b.second;});
        int i=0;
        for(auto &[_,s]:vec)
        {
            if(k>=s)
            {
                k-=s;
                i++;
            }
            else
            {
                break;
            }
        }
        return vec.size()-i;
    }
};
```



### [1403. 非递增顺序的最小子序列](https://leetcode.cn/problems/minimum-subsequence-in-non-increasing-order/)

给你一个数组 `nums`，请你从中抽取一个子序列，满足该子序列的元素之和 **严格** 大于未包含在该子序列中的各元素之和。

如果存在多个解决方案，只需返回 **长度最小** 的子序列。如果仍然有多个解决方案，则返回 **元素之和最大** 的子序列。

与子数组不同的地方在于，「数组的子序列」不强调元素在原数组中的连续性，也就是说，它可以通过从数组中分离一些（也可能不分离）元素得到。

**注意**，题目数据保证满足所有约束条件的解决方案是 **唯一** 的。同时，返回的答案应当按 **非递增顺序** 排列。

**示例 1：**

```
输入：nums = [4,3,10,9,8]
输出：[10,9] 
解释：子序列 [10,9] 和 [10,8] 是最小的、满足元素之和大于其他各元素之和的子序列。但是 [10,9] 的元素之和最大。 
```



解答

```C++
class Solution {
public:
    vector<int> minSubsequence(vector<int>& nums) 
    {
        //sort
        sort(nums.begin(),nums.end(),greater<int>{});
        //presum
        //presum>total-presum 的第一个 即2pres>total  的第一个值
        int n=nums.size();
        vector<int> presum(n);
        partial_sum(nums.begin(),nums.end(),presum.begin());
        int totalSum = presum[n-1];
        int idx = upper_bound(presum.begin(),presum.end(),0.5*totalSum)-presum.begin();
        return vector<int>(nums.begin(),nums.begin()+idx+1);
    }
};
```



### [3010. 将数组分成最小总代价的子数组 I](https://leetcode.cn/problems/divide-an-array-into-subarrays-with-minimum-cost-i/)

给你一个长度为 `n` 的整数数组 `nums` 。

一个数组的 **代价** 是它的 **第一个** 元素。比方说，`[1,2,3]` 的代价是 `1` ，`[3,4,1]` 的代价是 `3` 。

你需要将 `nums` 分成 `3` 个 **连续且没有交集** 的子数组。

请你返回这些子数组的 **最小** 代价 **总和** 。

**示例 1：**

```
输入：nums = [1,2,3,12]
输出：6
解释：最佳分割成 3 个子数组的方案是：[1] ，[2] 和 [3,12] ，总代价为 1 + 2 + 3 = 6 。
其他得到 3 个子数组的方案是：
- [1] ，[2,3] 和 [12] ，总代价是 1 + 2 + 12 = 15 。
- [1,2] ，[3] 和 [12] ，总代价是 1 + 3 + 12 = 16 。
```



```C++
class Solution {
public:
    int minimumCost(vector<int>& nums) 
    {
        //第一个一定要选 ， 找到除了第一个以外，最小的2个数字， top2问题 
        nth_element(nums.begin()+1,nums.begin()+2,nums.end()); //回忆nth_element这个接口,可以参考https://www.geeksforgeeks.org/stdnth_element-in-cpp/
        return nums[0]+nums[1]+nums[2];

        //10 3 1 1 
        //10之后找到两个最小的数字
    }
};
```

O（n）寻找最小和次小

```C++
class Solution {
public:
    int minimumCost(vector<int>& nums) 
    {
        //第一个一定要选 ， 找到除了第一个最小的2个数字， top2问题 
        //维护最小值和次小值
        int fi=INT_MAX,se = INT_MAX;
        for(int i=1;i<nums.size();i++)//fron 1
        {
            if(nums[i]<fi)
            {
                se=fi;
                fi=nums[i];
            }
            else if(nums[i]<se)
            {
                se = nums[i];
            }
        }
        return nums[0]+fi+se;
    }
};
```



### [1338. 数组大小减半](https://leetcode.cn/problems/reduce-array-size-to-the-half/)

```c++
typedef pair<int, int> PII;
struct compare
{
    bool operator()(const PII& a, const PII& b)
    {
        return a.second > b.second;
    }
};
class Solution {
public:
    int minSetSize(vector<int>& arr) {
        //放到哈希表里,然后排序
        unordered_map<int, int> umap;
        int total = arr.size();
        for(int i=0;i<total;i++)
        {
            umap[arr[i]]++;
        }
        vector<PII> vec(umap.begin(), umap.end());
        sort(vec.begin(), vec.end(), compare());
        int cnt = 0;
        int sum = 0;
        for(auto& p: vec)
        {
            sum += p.second;
            cnt++;
            if(sum>=total/2) break;
        }
        return cnt;
    }
};
```



### [1710. 卡车上的最大单元数](https://leetcode.cn/problems/maximum-units-on-a-truck/)

```c++
class Solution {
public:
    static bool compare(vector<int>& a, vector<int>& b) //注意得是static
    {
        return a[1] > b[1];
    }
    int maximumUnits(vector<vector<int>>& boxTypes, int truckSize) {
        //把boxTypes数组按照numberOfUnitsPerBox从大到小排序,然后计算即可
        sort(boxTypes.begin(), boxTypes.end(), compare);
        int sum = 0;
        int cnt = 0;
        int n = boxTypes.size();
        for(int i=0;i<n;i++)
        {
            if(sum + boxTypes[i][0] > truckSize)
            {
                cnt += (truckSize - sum) * boxTypes[i][1] ; //剩下的都装当前的箱子种类
                break;
            }
            else
            {
                sum += boxTypes[i][0];
                cnt += boxTypes[i][1] * boxTypes[i][0];
            }
        }
        return cnt;
    }
};
```



### [3075. 幸福值最大化的选择方案](https://leetcode.cn/problems/maximize-happiness-of-selected-children/)
给你一个长度为 `n` 的数组 `happiness` ，以及一个 **正整数** `k` 。

`n` 个孩子站成一队，其中第 `i` 个孩子的 **幸福值** 是 `happiness[i]` 。你计划组织 `k` 轮筛选从这 `n` 个孩子中选出 `k` 个孩子。

在每一轮选择一个孩子时，所有 **尚未** 被选中的孩子的 **幸福值** 将减少 `1` 。注意，幸福值 **不能** 变成负数，且只有在它是正数的情况下才会减少。

选择 `k` 个孩子，并使你选中的孩子幸福值之和最大，返回你能够得到的 **最大值** 。

**示例 1：**

```
输入：happiness = [1,2,3], k = 2
输出：4
解释：按以下方式选择 2 个孩子：
- 选择幸福值为 3 的孩子。剩余孩子的幸福值变为 [0,1] 。
- 选择幸福值为 1 的孩子。剩余孩子的幸福值变为 [0] 。注意幸福值不能小于 0 。
所选孩子的幸福值之和为 3 + 1 = 4 。
```
代码：

> [划分型 DP 的套路【力扣周赛 388】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Xr421J77b/?vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99),证明在这个视频的前4分钟。

```c++
class Solution {
public:
    long long maximumHappinessSum(vector<int>& happiness, int k) {
        //选择最大的k个数,第i个数happiness[i]做处理:max(happiness[i] - i, 0);结果累加到最终值上去(当然也可以在for循环里提前剪枝)
        long long res = 0;
        //注意,本题只能用排序来做,不能优化为快速选择,因为前k个值都要求有序递减,快速选择无法保证这一点
        sort(happiness.begin(), happiness.end(), greater<int>());
        for(int i=0;i<k;i++)
        {
            res += (long long)max(happiness[i] - i, 0);
        }
        return res;
    }
};
```



### [2554. 从一个范围内选择最多整数 I](https://leetcode.cn/problems/maximum-number-of-integers-to-choose-from-a-range-i/)

> 给你一个整数数组 `banned` 和两个整数 `n` 和 `maxSum` 。你需要按照以下规则选择一些整数：
>
> - 被选择整数的范围是 `[1, n]` 。
> - 每个整数 **至多** 选择 **一次** 。
> - 被选择整数不能在数组 `banned` 中。
> - 被选择整数的和不超过 `maxSum` 。
>
> 请你返回按照上述规则 **最多** 可以选择的整数数目。

用哈希即可。不要想着对`banned`数组排序什么的，复杂度又高，又不好写（写的很不好看）。最终代码如下：

```c++
class Solution {
public:
    int maxCount(vector<int>& banned, int n, int maxSum) {
        unordered_set<int> uset;
        int sz = banned.size();
        for(int i=0;i<sz;i++)
        {
            if(!uset.contains(banned[i]))
                uset.insert(banned[i]);
        }
        int curSum = 0;
        for(int cur=1;cur<=n;cur++) //用for循环+continue/break是比较好写的，如果用while的话感觉不是特别好写，以后可以优先选for循环的写法。
        {
            if(uset.contains(cur)) continue;
            if(curSum + cur > maxSum) break;
            else
            {
                curSum += cur;
                cnt++;
            }
        }
        return cnt;
    }
};
```



### [2126. 摧毁小行星](https://leetcode.cn/problems/destroying-asteroids/)

注意可能出现的越界问题：

```c++
class Solution {
public:
    bool asteroidsDestroyed(int mass, vector<int>& asteroids) {
        //按照从小到大的顺序与小行星碰撞,假设碰撞a和b都是合法的,那肯定是先撞小的那个更稳妥一些
        int n = asteroids.size();
        sort(asteroids.begin(), asteroids.end());
        long long curSum = mass;
        int index = 0; //从0开始撞
        for( ;index<n;index++)
        {
            if(curSum>=asteroids[index])
            {
                curSum += (long long)asteroids[index];
            }
            else break;
        }
        return (index==n);

    }
};
```



### [2587. 重排数组以得到最大前缀分数](https://leetcode.cn/problems/rearrange-array-to-maximize-prefix-score/)

> 给你一个下标从 **0** 开始的整数数组 `nums` 。你可以将 `nums` 中的元素按 **任意顺序** 重排（包括给定顺序）。
>
> 令 `prefix` 为一个数组，它包含了 `nums` 重新排列后的前缀和。换句话说，`prefix[i]` 是 `nums` 重新排列后下标从 `0` 到 `i` 的元素之和。`nums` 的 **分数** 是 `prefix` 数组中正整数的个数。
>
> 返回可以得到的最大分数。

贪心思路的基本证明:

对于一个负数来说，它后面的前缀和都会把这个负数加进去。

由于要统计的是正数前缀和，那么把负数尽量放在后面，能统计到尽量多的正数前缀和。

同时，绝对值小的负数应该排在负数的前面，尽量在前缀和减为负数前还能多统计一些正数。

```c++
class Solution {
public:
    int maxScore(vector<int>& nums) {
        sort(nums.begin(), nums.end(), greater<int>());
        int n = nums.size();
        int cnt = 0;
        long long sum = 0;
        for(int i=0;i<n;i++)
        {
            if(sum + nums[i] > 0)
            {
                cnt++;
                sum += nums[i];
            }
            else break;
        }
        return cnt;
    }
};
```



### [976. 三角形的最大周长](https://leetcode.cn/problems/largest-perimeter-triangle/)

> 给定由一些正数（代表长度）组成的数组 `nums` ，返回 *由其中三个长度组成的、**面积不为零**的三角形的最大周长* 。如果不能形成任何面积不为零的三角形，返回 `0`。

这道题如果从大到小排序完，然后三轮for循环找结果的话会爆超出时间限制，所以需要对算法进行优化。实际上，只要一轮for循环就可以解决了，代码和注释如下：

```c++
class Solution {
public:
    int largestPerimeter(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        //对于nums[i]来说,如果nums[i-1]+nums[i-2]<nums[i],那么前面的更不可能了,直接枚举下一个i即可
        //否则,nums[i] + nums[i-1] + nums[i-2]就是要求解的值
        for(int i=n-1;i>=2;i--)
        {
            if(nums[i-1] + nums[i-2] <= nums[i]) continue;
            return nums[i] + nums[i-1] + nums[i-2];
        }
        return 0;
    }
};
```



### [1561. 你可以获得的最大硬币数目](https://leetcode.cn/problems/maximum-number-of-coins-you-can-get/)

> 有 3n 堆数目不一的硬币，你和你的朋友们打算按以下方式分硬币：
>
> - 每一轮中，你将会选出 **任意** 3 堆硬币（不一定连续）。
> - Alice 将会取走硬币数量最多的那一堆。
> - 你将会取走硬币数量第二多的那一堆。
> - Bob 将会取走最后一堆。
> - 重复这个过程，直到没有更多硬币。
>
> 给你一个整数数组 `piles` ，其中 `piles[i]` 是第 `i` 堆中硬币的数目。
>
> 返回你可以获得的最大硬币数目。

代码如下：
```c++
class Solution {
public:
    int maxCoins(vector<int>& piles) {
        //让Bob亏麻了,同时不让Alice赢太多
        sort(piles.begin(), piles.end());
        int n = piles.size();
        int ans = 0;
        int left = 0, right = n - 2;
        while(left < right)
        {
            ans += piles[right];
            right -= 2;
            left++;
        }
        return ans;
    }
};
```



### [3462. 提取至多 K 个元素的最大总和](https://leetcode.cn/problems/maximum-sum-with-at-most-k-elements/)

> 给你一个大小为 `n x m` 的二维矩阵 `grid` ，以及一个长度为 `n` 的整数数组 `limits` ，和一个整数 `k` 。你的目标是从矩阵 `grid` 中提取出 **至多** `k` 个元素，并计算这些元素的最大总和，提取时需满足以下限制**：**
>
> - 从 `grid` 的第 `i` 行提取的元素数量不超过 `limits[i]` 。
>
> 返回最大总和。

```c++
class Solution {
public:
    long long maxSum(vector<vector<int>>& grid, vector<int>& limits, int k) {
        //grid没有负数,因此肯定是选满k个最好
        //每一行取limit这么多大的数(快速选择),然后在这里面取topk即可
        int n = grid.size();
        int m = grid[0].size();
        int sum = accumulate(limits.begin(), limits.end(), 0);
        vector<int> candidates(sum, 0);
        int index = 0;
        for(int row = 0;row < n;row++)
        {
            nth_element(grid[row].begin(), grid[row].begin() + limits[row] - 1, grid[row].end(), greater<int>());
            for(int i=0;i<limits[row];i++)
            {
                candidates[index++] = grid[row][i];
            }
        }
        sort(candidates.begin(), candidates.end(), greater<int>());
        long long ans = 0;
        for(int i=0;i<k;i++)
        {
            ans += (long long)candidates[i];
        }
        return ans;
    }
};
```



### [3301. 高度互不相同的最大塔高和](https://leetcode.cn/problems/maximize-the-total-height-of-unique-towers/)

> 给你一个数组 `maximumHeight` ，其中 `maximumHeight[i]` 表示第 `i` 座塔可以达到的 **最大** 高度。
>
> 你的任务是给每一座塔分别设置一个高度，使得：
>
> 1. 第 `i` 座塔的高度是一个正整数，且不超过 `maximumHeight[i]` 。
> 2. 所有塔的高度互不相同。
>
> 请你返回设置完所有塔的高度后，可以达到的 **最大** 总高度。如果没有合法的设置，返回 `-1` 。

```c++
class Solution {
public:
    long long maximumTotalSum(vector<int>& maximumHeight) {
        sort(maximumHeight.begin(), maximumHeight.end());
        int mx = maximumHeight.back();
        int n = maximumHeight.size();

        int start = mx; //一开始分配的数
        long long ans = 0;
        //优先满足大的,不然后面只能越来越小,非常不划算
        int index = n-1;
        for(;index>=0;index--)
        {
            start = min(maximumHeight[index], start); 
            if(start<=0) break;
            ans += (long long)start;
            start--; //每次start-1,保证下一次分配的时候一定比现在少1
        }
        if(index>=0) return -1; //分配不完,无法达成要求
        return ans;
    }
};
```



### ==补充困难题：[1840. 最高建筑高度](https://leetcode.cn/problems/maximum-building-height/)==

> 有点难了，后面再来做吧。





## §1.2 单序列配对

同上，从最小/最大的元素开始贪心。



### [2144. 打折购买糖果的最小开销](https://leetcode.cn/problems/minimum-cost-of-buying-candies-with-discount/) 1261

一家商店正在打折销售糖果。每购买 **两个** 糖果，商店会 **免费** 送一个糖果。

免费送的糖果唯一的限制是：它的价格需要小于等于购买的两个糖果价格的 **较小值** 。

- 比方说，总共有 `4` 个糖果，价格分别为 `1` ，`2` ，`3` 和 `4` ，一位顾客买了价格为 `2` 和 `3` 的糖果，那么他可以免费获得价格为 `1` 的糖果，但不能获得价格为 `4` 的糖果。

给你一个下标从 **0** 开始的整数数组 `cost` ，其中 `cost[i]` 表示第 `i` 个糖果的价格，请你返回获得 **所有** 糖果的 **最小** 总开销。

**示例 1：**

```
输入：cost = [1,2,3]
输出：5
解释：我们购买价格为 2 和 3 的糖果，然后免费获得价格为 1 的糖果。
总开销为 2 + 3 = 5 。这是开销最小的 唯一 方案。
注意，我们不能购买价格为 1 和 3 的糖果，并免费获得价格为 2 的糖果。
这是因为免费糖果的价格必须小于等于购买的 2 个糖果价格的较小值。
```



M1

3个打包卖

```C++
class Solution {
public:
    int minimumCost(vector<int>& cost) {
        sort(cost.begin(),cost.end(),greater<int>{});
        int res=0;
        int n = cost.size();
        for(int i=0;i<n;i++)
        {
            if(i%3!=2)res+=cost[i];
        }
        return res;
    }
};
```



M2: M

```C++
class Solution {
public:
    int minimumCost(vector<int>& cost) {
        //最大 第二大的一定会买
        //排序后一定可以送第三大的糖 
        //继续上述步骤 
        sort(cost.begin(),cost.end(),greater<int>{});
        //9 7 7 5 2 2 1 1
        int res=0;
        int n = cost.size();
        for(int i=0;i<n;)
        {
            if(i<n)
            {
                res+= cost[i];
                i++;
            }
            if(i<n)
            {
                res+= cost[i];
                i++;
            }
            if(i<n)
            {
                i++;
            }
        }
        return res;
    }
};
```



### [561. 数组拆分 ](https://leetcode.cn/problems/array-partition/)约 1300

给定长度为 `2n` 的整数数组 `nums` ，你的任务是将这些数分成 `n` 对, 例如 `(a1, b1), (a2, b2), ..., (an, bn)` ，使得从 `1` 到 `n` 的 `min(ai, bi)` 总和最大。

返回该 **最大总和** 。

**示例 1：**

```
输入：nums = [1,4,3,2]
输出：4
解释：所有可能的分法（忽略元素顺序）为：
1. (1, 4), (2, 3) -> min(1, 4) + min(2, 3) = 1 + 2 = 3
2. (1, 3), (2, 4) -> min(1, 3) + min(2, 4) = 1 + 2 = 3
3. (1, 2), (3, 4) -> min(1, 2) + min(3, 4) = 1 + 3 = 4
所以最大总和为 4
```

```C++
class Solution {
public:
    int arrayPairSum(vector<int>& nums) {
        // 大的数字和大的数字放一起
        sort(nums.begin(),nums.end(),greater<int>());
        int n =nums.size();
        int res=0;
        for(int i=1;i<n;i+=2)
        {
            res+=nums[i];
        }
        return res;
    }
};
```

OR(题目说了长度是2n)

```C++
class Solution {
public:
    int arrayPairSum(vector<int>& nums) {
        // 大的数字和大的数字放一起
        sort(nums.begin(),nums.end());
        int n =nums.size();
        int res=0;
        for(int i=0;i<n;i+=2)
        {
            res+=nums[i];
        }
        return res;
    }
};
```

证明：

https://leetcode.cn/problems/array-partition/solutions/5534/minshu-dui-bi-shi-you-xu-shu-lie-shang-xiang-lin-y/

<img src="assets/image-20250330204319874.png" alt="image-20250330204319874" style="zoom: 67%;" />

![image-20250330204348220](assets/image-20250330204348220.png)

![image-20250330204410088](assets/image-20250330204410088.png)

### [1877. 数组中最大数对和的最小值](https://leetcode.cn/problems/minimize-maximum-pair-sum-in-array/)

一个数对 `(a,b)` 的 **数对和** 等于 `a + b` 。**最大数对和** 是一个数对数组中最大的 **数对和** 。

- 比方说，如果我们有数对 `(1,5)` ，`(2,3)` 和 `(4,4)`，**最大数对和** 为 `max(1+5, 2+3, 4+4) = max(6, 5, 8) = 8` 。

给你一个长度为 **偶数** `n` 的数组 `nums` ，请你将 `nums` 中的元素分成 `n / 2` 个数对，使得：

- `nums` 中每个元素 **恰好** 在 **一个** 数对中，且
- **最大数对和** 的值 **最小** 。

请你在最优数对划分的方案下，返回最小的 **最大数对和** 。

**示例 1：**

```
输入：nums = [3,5,2,3]
输出：7
解释：数组中的元素可以分为数对 (3,3) 和 (5,2) 。
最大数对和为 max(3+3, 5+2) = max(6, 7) = 7 。
```



```C++
class Solution {
public:
    int minPairSum(vector<int>& nums) 
    {
        //尽量平均
        //最大和最小放一起
        sort(nums.begin(),nums.end());
        int n= nums.size();
        int res=0;
        for(int i=0;i<n/2;i++)
        {
            res = max(res,nums[i]+nums[n-i-1]);
        }
        return res;
    }
};
```



最大数对和的最小值，贪心解的正确性证明：

https://leetcode.cn/problems/minimize-maximum-pair-sum-in-array/solutions/885704/gong-shui-san-xie-noxiang-xin-ke-xue-xi-ru29y

![image-20250330211656395](assets/image-20250330211656395.png)

![image-20250330211715475](assets/image-20250330211715475.png)

![image-20250330211725870](assets/image-20250330211725870.png)

知道了上面的证明“非对称方式”不会比“对称方式”更优，那么我们首先对于第一步来说，比如我们取最小元素和其他东西配对，只有当另一个值取到最大元素（对称）的时候，结果最小（最优）

那么去掉这两个元素，继续取剩下数组中的最大和最小元素配对即可。



### [881. 救生艇](https://leetcode.cn/problems/boats-to-save-people/) 1530 经典题

给定数组 `people` 。`people[i]`表示第 `i` 个人的体重 ，**船的数量不限**，每艘船可以承载的最大重量为 `limit`。

每艘船最多可同时载两人，但条件是这些人的重量之和最多为 `limit`。

返回 *承载所有人所需的最小船数* 。

**示例 1：**

```
输入：people = [1,2], limit = 3
输出：1
解释：1 艘船载 (1, 2)
```



https://leetcode.cn/problems/boats-to-save-people/solutions/2828004/jian-ji-yi-dong-de-tu-shi-tui-dao-fu-duo-g02g/

```C++
class Solution {
public:
    int numRescueBoats(vector<int>& people, int limit) {
        int n = people.size();
        int cnt=0;
        int l=0,r=n-1;
        sort(people.begin(),people.end());
        while(l<=r)
        {
            if(people[l]+people[r]<=limit)
            {
                cnt++;
                l++;
                r--;
            }
            else
            {
                cnt++;
                r--;
            }
        }
        return cnt;
    }
};
```



### [2592. 最大化数组的伟大值](https://leetcode.cn/problems/maximize-greatness-of-an-array/)

给你一个下标从 0 开始的整数数组 `nums` 。你需要将 `nums` 重新排列成一个新的数组 `perm` 。

定义 `nums` 的 **伟大值** 为满足 `0 <= i < nums.length` 且 `perm[i] > nums[i]` 的下标数目。

请你返回重新排列 `nums` 后的 **最大** 伟大值。

 

**示例 1：**

```
输入：nums = [1,3,5,2,1,3,1]
输出：4
解释：一个最优安排方案为 perm = [2,5,1,3,3,1,1] 。
在下标为 0, 1, 3 和 4 处，都有 perm[i] > nums[i] 。因此我们返回 4 。
```

思路:田忌赛马:

```C++
class Solution {
public:
    int maximizeGreatness(vector<int>& nums) {
        //1 1 1 2 3 3 5 nums
        sort(nums.begin(),nums.end());
        int n =nums.size();
        int f=n-2;
        int k=n-1;
        int cnt=0;
        for(;k>=0&&f>=0;)
        {
            if(nums[k]>nums[f])
            {
                cnt++;
                k--;
                f--;
            }
            else
            {
                f--;
            }
        }
        return cnt;
    }
};
```



### [2576. 求出最多标记下标](https://leetcode.cn/problems/find-the-maximum-number-of-marked-indices/)（看答案） :cat:

给你一个下标从 **0** 开始的整数数组 `nums` 。

一开始，所有下标都没有被标记。你可以执行以下操作任意次：

- 选择两个 **互不相同且未标记** 的下标 `i` 和 `j` ，满足 `2 * nums[i] <= nums[j]` ，标记下标 `i` 和 `j` 。

请你执行上述操作任意次，返回 `nums` 中最多可以标记的下标数目。

**示例 1：**

```C++
输入：nums = [3,5,2,4]
输出：2
解释：第一次操作中，选择 i = 2 和 j = 1 ，操作可以执行的原因是 2 * nums[2] <= nums[1] ，标记下标 2 和 1 。
没有其他更多可执行的操作，所以答案为 2 。
```



#### M1 :二分

在二分专题中

假如最终有 K对匹配的数对，就一定是左边最小的 K个数与右边最大的K 个数进行匹配。

![image-20250401000437309](assets/image-20250401000437309.png)

m:左边1区间中的红色，需要和右边2区间中的红色匹配（`int left = 0, right = n-k;`）

反证，如果与橙色（更小），那么一定能与红色。

​			如果与绿色（更大），那么右边2区间内不足k个，不是我们要的答案。

#### M2 :贪心

https://leetcode.cn/problems/find-the-maximum-number-of-marked-indices/solutions/2914153/tan-xin-pai-xu-shuang-zhi-zhen-tui-dao-z-bqx3/

**结论**：假如最终有 K对匹配的数对，就一定是左边最小的 K个数与右边最大的K 个数进行匹配。

由方法一的匹配方式可知，我们需要用 nums 左半部分中的数，去匹配 nums 右半部分中的数。

在 nums 的右半部分中，找到第一个满足 2⋅nums[0]≤nums[j] 的 j，那么 nums[1] 只能匹配右半部分中的下标大于 j 的数，依此类推。

这可以用同向双指针实现。

```C++
class Solution {
public:
    int maxNumOfMarkedIndices(vector<int>& nums) {
        sort(nums.begin(),nums.end());
        int n = nums.size();
        int i=0;
        for(int j=(n+1)/2;j<n;j++)
        {
            if(nums[i]*2<=nums[j])// 找到一个匹配
            {
                i++;
            }
        }
        return 2*i;
    }
};
```



## §1.3 双序列配对

同上，从最小/最大的元素开始贪心。

### （1）[455. 分发饼干](https://leetcode.cn/problems/assign-cookies/)

假设你是一位很棒的家长，想要给你的孩子们一些小饼干。但是，每个孩子最多只能给一块饼干。

对每个孩子 `i`，都有一个胃口值 `g[i]`，这是能让孩子们满足胃口的饼干的最小尺寸；并且每块饼干 `j`，都有一个尺寸 `s[j]` 。如果 `s[j] >= g[i]`，我们可以将这个饼干 `j` 分配给孩子 `i` ，这个孩子会得到满足。你的目标是满足尽可能多的孩子，并输出这个最大数值。

**示例 1:**

```C++
输入: g = [1,2,3], s = [1,1]
输出: 1
解释: 
你有三个孩子和两块小饼干，3 个孩子的胃口值分别是：1,2,3。
虽然你有两块小饼干，由于他们的尺寸都是 1，你只能让胃口值是 1 的孩子满足。
所以你应该输出 1。
```



从小到大排序

优先将小的饼干分给小胃口的孩子，孩子不够吃，再看看更大的饼干行不行

```C++
class Solution {
public:
    int findContentChildren(vector<int>& ch, vector<int>& co) {
        sort(ch.begin(), ch.end());
        int chn = ch.size();
        sort(co.begin(), co.end());
        int con = co.size();
        int chi = 0, coo = 0;
        for (; chi < chn && coo < con;)
        {
            if (co[coo] >= ch[chi])
            {
                coo++;
                chi++;
            }
            else
            {
                coo++;//看更大的cookie饼干能否满足孩子
            }
        }
        return chi;//返回可满足的孩子数量
    }
};
```



从大到小排序

优先将最大的饼干分给胃口最大的孩子，孩子不够吃，再给次大胃口的孩子

```C++
class Solution {
public:
    int findContentChildren(vector<int>& ch, vector<int>& co) {
        sort(ch.begin(), ch.end(), greater<int>());
        int chn = ch.size();
        sort(co.begin(), co.end(), greater<int>());
        int con = co.size();
        int chi = 0, coo = 0;
        for (; chi < chn && coo < con;)
        {
            if (co[coo] >= ch[chi])
            {
                coo++;
                chi++;
            }
            else
            {
                chi++;//看这个饼干 能否满足胃口更小的孩子能否 
            }
        }
        return coo;//返回可满足孩子的饼干数量
    }
};

```

