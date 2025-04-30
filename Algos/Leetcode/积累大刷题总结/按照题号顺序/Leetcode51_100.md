## [51. N 皇后](https://leetcode.cn/problems/n-queens/)

> 按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。
>
> **n 皇后问题** 研究的是如何将 `n` 个皇后放置在 `n×n` 的棋盘上，并且使皇后彼此之间不能相互攻击。
>
> 给你一个整数 `n` ，返回所有不同的 **n 皇后问题** 的解决方案。
>
> 每一种解法包含一个不同的 **n 皇后问题** 的棋子放置方案，该方案中 `'Q'` 和 `'.'` 分别代表了皇后和空位。

本题注意斜对角线的判断逻辑，即`abs(r1-r2)==abs(c1-c2)`,则在斜对角线上，此时不是合法的放置方案。

```c++
class Solution {
public:
    bool isValid(vector<int>& cols, int curRow, int curCol)
    {
        int n = cols.size();
        for(int r=0;r<curRow;r++) //判断之前的就行,后面的行不需要判断
        {
            //1.不能同列
            if(cols[r]==curCol) return false;
            //2.不能对角线
            if(abs(r-curRow)==abs(cols[r]-curCol)) return false;
        }
        return true;
    }
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> res;
        vector<int> cols(n, -1); //一开始都没选择
        auto dfs=[&](this auto&& dfs, int curRow)
        {
            if(curRow==n) //说明到了最后,还原出来一种可行解,放入最终结果中
            {
                // cout<<"=============="<<endl;
                // for(int c:cols) cout<<c<<" ";
                // cout<<endl;
                vector<string> path(n);
                for(int r=0;r<n;r++) //还原每一行
                {
                    path[r] = string(cols[r],'.') + 'Q' + string(n-cols[r]-1,'.');
                }
                res.push_back(path);
                return;
            }
            //开始遍历八皇后问题,找哪一列可以作为新的一行选择的列
            for(int curCol=0;curCol<n;curCol++)
            {
                if(isValid(cols, curRow, curCol)) //传入当前行和当前列
                {
                    cols[curRow] = curCol;
                    dfs(curRow+1);
                    //不用还原,因为后面会被覆盖掉.
                }
            }
        };
        dfs(0);
        return res;
    }
};
```



## [52. N 皇后 II](https://leetcode.cn/problems/n-queens-ii/)

> **n 皇后问题** 研究的是如何将 `n` 个皇后放置在 `n × n` 的棋盘上，并且使皇后彼此之间不能相互攻击。
>
> 给你一个整数 `n` ，返回 **n 皇后问题** 不同的解决方案的数量。

代码跟上一题基本差不多，甚至比上一题还简单：

```c++
class Solution {
public:
    vector<int> cols;
    int n;
    bool isValid(int curRow, int curCol)
    {
        for(int r=0;r<curRow;r++) //遍历到当前Row即可
        {
            if(curCol==cols[r]) return false;
            if(abs(curCol-cols[r])==abs(curRow-r))
            {
                return false; //对应对角线的情况
            }
        }
        return true;
    }
    int totalNQueens(int n) {
        int cnt = 0;
        this->n = n;
        cols.resize(n, -1); //每一行都放在了哪一列
        auto dfs = [&](this auto&& dfs, int curRow)
        {
            if(curRow==n) //找到一组合理的解
            {
                cnt++; //本题只需要cnt++,实际上也可以打印具体的放置方案
                return;
            }
            //看哪一列可以放
            for(int curCol=0;curCol<n;curCol++)
            {
                if(isValid(curRow, curCol))
                {
                    cols[curRow] = curCol;
                    dfs(curRow + 1); //可以遍历下一行,本行是合法的
                    //不用赋值回来,后面会覆盖
                }
            }
        };
        dfs(0);
        return cnt;
    }
};
```



## [53. 最大子数组和](https://leetcode.cn/problems/maximum-subarray/)

> 给你一个整数数组 `nums` ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
>
> **子数组**是数组中的一个连续部分。

DP类题目，代码如下：
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



## [54. 螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/)

> 给你一个 `m` 行 `n` 列的矩阵 `matrix` ，请按照 **顺时针螺旋顺序** ，返回矩阵中的所有元素。

模拟题，需要小心可能存在的边界情况：

```c++
class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        int l=0,r=matrix[0].size()-1, t=0, b=matrix.size()-1;
        vector<int> res;
        while(l<=r && t<=b)
        {
            for(int i=l;i<=r;i++) res.push_back(matrix[t][i]);
            t++;
            if(l>r || t>b) break;
            for(int i=t;i<=b;i++) res.push_back(matrix[i][r]);
            r--;
            if(l>r || t>b) break;
            for(int i=r;i>=l;i--) res.push_back(matrix[b][i]);
            b--;
            if(l>r || t>b) break;
            for(int i=b;i>=t;i--) res.push_back(matrix[i][l]);
            l++;
        }
        return res;
    }
};
```



## [55. 跳跃游戏](https://leetcode.cn/problems/jump-game/)

> 给你一个非负整数数组 `nums` ，你最初位于数组的 **第一个下标** 。数组中的每个元素代表你在该位置可以跳跃的最大长度。
>
> 判断你是否能够到达最后一个下标，如果可以，返回 `true` ；否则，返回 `false` 。

本题可以用类似于贪心的做法来做。到每一个位置的时候，都更新最右能跳多远。如果遍历到的当前下标超过了计算出的能跳的最远的下标，则表示无法到达最后一格下标，return false即可。

代码如下：

```c++
class Solution {
public:
    bool canJump(vector<int>& nums) {
        int mx = 0;
        for(int i=0;i<nums.size();i++)
        {
            if(i>mx) return false;
            mx = max(mx, i+nums[i]);
        }
        return true;
    }
};
```



## [56. 合并区间](https://leetcode.cn/problems/merge-intervals/)

> 以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [starti, endi]` 。请你合并所有重叠的区间，并返回 *一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间* 。

### （1）方法1：差分

在之前的学习中，这道题目可以用差分来做，但要注意`[1，2]，[3，4]`是不能合并的，因此可以先把所有的值*2，最后再/2来解决问题。使用差分来做这道题目，代码如下：

```c++
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        map<int,int> diff;
        int n=intervals.size();
        for(int i=0;i<n;i++)
        {
            int left = intervals[i][0],right = intervals[i][1];
            diff[left*2]++;
            diff[right*2+1]--; //差分的过程
        }
        int s=0;
        int l=0;
        bool flag=false;
        vector<vector<int>> res;
        for(auto &[k,v]:diff)
        {
            s+=v;
            if(flag==false&& s>0) //注意下面的判断过程
            {
                l=k;
                flag=true;
            }
            else if(flag==true&&s==0)
            {
                res.push_back({l/2,k/2});
                flag=false;
            }
        }
        return res;

    }
};
```



### （2）方法2：贪心

按照左端点进行排序。以示例 1 为例，我们有 [1,3],[2,6],[8,10],[15,18] 这四个区间。

为方便合并，把区间按照左端点从小到大排序（示例 1 已经按照左端点排序了）。排序的理由会在下面的合并过程中说明。

排序后，我们就知道了第一个合并区间的左端点，即 `intervals[0][0]=1`。

第一个合并区间的右端点是多少？目前只知道其 `≥intervals[0][1]=3`，但具体是多少现在还不确定，得向右遍历。

具体算法如下：

- 把 intervals[0] 加入答案。注意，答案的最后一个区间表示当前正在合并的区间。
- 遍历到 intervals[1]=[2,6]，由于左端点 2 不超过当前合并区间的右端点 3，可以合并。由于右端点 6>3，那么更新当前合并区间的右端点为 6。
  - 注意，由于我们已经按照左端点排序，所以 intervals[1] 的左端点 2 必然大于等于合并区间的左端点，所以无需更新当前合并区间的左端点。
- 遍历到 intervals[2]=[8,10]，由于左端点 8 大于当前合并区间的右端点 6，无法合并（两个区间不相交）。再次利用区间按照左端点排序的性质，更后面的区间的左端点也大于 6，无法与当前合并区间相交，所以当前合并区间 [1,6] 就固定下来了，把新的合并区间 [8,10] 加入答案。
- 遍历到 intervals[3]=[15,18]，由于左端点 15 大于当前合并区间的右端点 10，无法合并（两个区间不相交），我们找到了一个新的合并区间 [15,18] 加入答案。

上述算法同时说明，按照左端点排序后，合并的区间一定是 intervals 中的连续子数组。

上述算法的代码如下：

```c++
class Solution {
public:
    static bool compare(const vector<int>& v1, const vector<int>& v2)
    {
        return v1[0] < v2[0]; //排序第一个数
    }
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), compare);
        int n = intervals.size();
        vector<vector<int>> res;
        res.emplace_back(intervals[0]);
        for(int i=1;i<n;i++) //往后遍历
        {
            int curRight = res.back()[1];
            if(intervals[i][0]>curRight)
            {
                res.emplace_back(intervals[i]);
            }
            else res.back()[1] = max(intervals[i][1], res.back()[1]);  //更新右端点的最大值
        }
        return res;
    }
};
```



## [57. 插入区间](https://leetcode.cn/problems/insert-interval/)

> 给你一个 **无重叠的** *，*按照区间起始端点排序的区间列表 `intervals`，其中 `intervals[i] = [starti, endi]` 表示第 `i` 个区间的开始和结束，并且 `intervals` 按照 `starti` 升序排列。同样给定一个区间 `newInterval = [start, end]` 表示另一个区间的开始和结束。
>
> 在 `intervals` 中插入区间 `newInterval`，使得 `intervals` 依然按照 `starti` 升序排列，且区间之间不重叠（如果有必要的话，可以合并区间）。
>
> 返回插入之后的 `intervals`。
>
> **注意** 你不需要原地修改 `intervals`。你可以创建一个新数组然后返回它。

```c++
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        // 先按照start的位置插入到合适的地方,然后再用上一题的做法做合并
        // 二分找第一个>=newInterval的位置,即为插入的位置
        int n = intervals.size();
        int left = 0, right = n - 1;
        while(left<=right)
        {
            int mid = left + ((right-left)>>1);
            if(intervals[mid][0]<newInterval[0])
            {
                left = mid + 1; //left一定往合法的地方走,最后的left一定是第一个合法的位置
            }
            else right = mid - 1;
        }
        intervals.insert(intervals.begin()+left, newInterval);
        //与上一题一样,开始合并区间
        vector<vector<int>> res;
        res.emplace_back(intervals[0]);
        for(int i=1;i<n+1;i++)
        {
            int curRight = res.back()[1];
            if(intervals[i][0]>curRight) //来的左端点比当前最远右端点还要大
            {
                res.emplace_back(intervals[i]);
            }
            else res.back()[1] = max(res.back()[1], intervals[i][1]);
        }
        return res;
    }
};
```



## [58. 最后一个单词的长度](https://leetcode.cn/problems/length-of-last-word/)

> 给你一个字符串 `s`，由若干单词组成，单词前后用一些空格字符隔开。返回字符串中 **最后一个** 单词的长度。
>
> **单词** 是指仅由字母组成、不包含任何空格字符的最大子字符串。

```c++
class Solution {
public:
    int lengthOfLastWord(string s) {
        //从最后往前遍历，从第一个不是空格的字符开始，到另一个是空格的字符结束
        int n = s.size();
        int index = n-1;
        while(index>=0 && s[index]==' ') index--;
        if(index<0) return 0;
        int len = 0;
        while(index>=0)
        {
            if(s[index]==' ') break;
            len++;
            index--;
        }
        return len;
    }
};
```



### (1) C++ 库函数

```c++
class Solution {
public:
    int lengthOfLastWord(string s) {
        int i = s.find_last_not_of(' '); //最后一个不是空格的索引
        int j = s.find_last_of(' ', i); //最后一个是空格的索引,从i开始往前
        return i-j;
    }
};
```



## [59. 螺旋矩阵 II](https://leetcode.cn/problems/spiral-matrix-ii/)

> 给你一个正整数 `n` ，生成一个包含 `1` 到 `n2` 所有元素，且元素按顺时针顺序螺旋排列的 `n x n` 正方形矩阵 `matrix` 。

这道题的要点在于**如何把解决问题的代码写的比较优雅。**可以参考下面的代码。

```c++
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        int dirs[4][2] = {{0,1},{1,0},{0,-1},{-1,0}};
        vector<vector<int>> grid(n, vector<int>(n, 0)); //默认是0
        int d = 0; //0：右，1：下，2：左，3：上
        int curX = 0, curY = 0;
        for(int index=1;index<=n*n;index++)
        {
            //到达边界，或者已经填数了，需要转向d=(d+1)%4;
            grid[curX][curY] = index;
            int nxtX = curX + dirs[d][0];
            int nxtY = curY + dirs[d][1];
            if(nxtX<0 || nxtX>=n || nxtY<0 || nxtY>=n || grid[nxtX][nxtY])
            {
                //说明其实是要转向的，现在不能走了
                d = (d+1) % 4;
            }
            curX += dirs[d][0];
            curY += dirs[d][1]; //此时不会越界，因为一定能放得下n^2这么多数
        }
        return grid;
    }
};
```



## [60. 排列序列](https://leetcode.cn/problems/permutation-sequence/)

> 给出集合 `[1,2,3,...,n]`，其所有元素共有 `n!` 种排列。
>
> 按大小顺序列出所有排列情况，并一一标记，当 `n = 3` 时, 所有排列如下：
>
> 1. `"123"`
> 2. `"132"`
> 3. `"213"`
> 4. `"231"`
> 5. `"312"`
> 6. `"321"`
>
> 给定 `n` 和 `k`，返回第 `k` 个排列。

### （1）我的方法——回溯爆搜

```c++
class Solution {
public:
    string res;
    string getPermutation(int n, int k) {
        //正常排列，用回溯的方法来做
        vector<int> used(n+1, 0); //记录使用的情况
        int index = 0; //=k的时候返回结果
        string path;
        auto dfs = [&](this auto&& dfs, int i) -> int
        {
            if(i==n)
            {
                index++;
                if(index==k)
                {
                    res = path;
                    return -1; //表示找到了第k个解，return -1
                }
                return 0;
            }
            for(int idx=1;idx<=n;idx++)
            {
                if(!used[idx])
                {
                    used[idx] = 1;
                    path.push_back('0'+idx);
                    int res = dfs(i+1);
                    if(res==-1) return -1;
                    used[idx] = 0;
                    path.pop_back();
                }
            }
            return 0;
        };
        dfs(0);
        return res;
    }
};
```



### （2）数学方法——康托展开与逆康托展开

参考链接如下：[康托展开与逆康托展开-CSDN博客](https://blog.csdn.net/wbin233/article/details/72998375)

> ### **康托展开（Cantor Expansion）与逆康托展开（Inverse Cantor Expansion）**
>
> 康托展开是一种将排列（permutation）映射到一个唯一整数（排名）的双射方法，逆康托展开则是从排名恢复原排列的过程。它们在排列的字典序排名、组合数学和算法竞赛中有广泛应用。
>
> ---
>
> ## **1. 康托展开（Cantor Expansion）**
> ### **定义**
> 给定一个排列 $P = [a_1, a_2, \ldots, a_n] $，康托展开计算其在所有排列中的字典序排名（从0开始）。
>
> ### **公式**
> 康托展开的计算公式为：
> $$
> \text{rank} = \sum_{i=1}^{n} (d_i \times (n-i)!)
> $$
> 其中：
> - $d_i$ 表示在 $a_i$ 右侧比 $a_i $ 小的数字的个数（即逆序数）。
> - $(n-i)!$ 是阶乘，表示剩余数字的排列数。
>
> ### **计算步骤**
> 1. 初始化 `rank = 0`。
> 2. 对于每个 $ a_i $（从左到右）：
>    - 计算 $d_i=$ 当前未使用的数字中比 $a_i$ 小的数字的个数。
>    - 累加 $d_i \times (n-i)!$ 到 `rank`。
>    - 标记 $a_i$ 为已使用。
> 3. 最终 `rank` 即为该排列的字典序排名。
>
> ### **示例**
> 计算排列 `[3, 1, 4, 2]` 的康托展开：
> 1. $a_1 = 3 $，未使用数字 `{1,2,3,4}`，比 `3` 小的有 `1,2` → $d_1 = 2$，贡献$ 2 \times 3! = 12$。
> 2. $a_2 = 1$，未使用数字 `{1,2,4}`，比 `1` 小的无 → $d_2 = 0$，贡献 $0 \times 2! = 0$。
> 3. $a_3 = 4$，未使用数字 `{2,4}`，比 `4` 小的有 `2` → $d_3 = 1$，贡献 $ 1 \times 1! = 1 $。
> 4. $a_4 = 2$，未使用数字 `{2}`，比 `2` 小的无 → $d_4 = 0$，贡献 $ 0 \times 0! = 0$。
> 5. 最终 `rank = 12 + 0 + 1 + 0 = 13`。
>
> ---
>
> ## **2. 逆康托展开（Inverse Cantor Expansion）**
> ### **定义**
> 给定排名 `rank` 和排列长度 `n`，逆康托展开恢复原排列。
>
> ### **公式**
> 1. 初始化未使用数字列表 `nums = [1, 2, ..., n]`。
> 2. 对于每个位置 \( i \)（从1到n）：
>    - 计算 $k = \text{rank} / (n-i)!$，得到当前数字在未使用数字中的索引。
>    - 取 `nums[k]` 作为当前数字，并从 `nums` 中移除。
>    - 更新 `rank = rank % (n-i)!`。
>
> ### **示例**
> 给定 `rank = 13`，`n = 4`，恢复排列：
> 1. 未使用数字 `[1,2,3,4]`：
>    - \( k = 13 / 3! = 2 \)，取 `nums[2] = 3`，剩余 `[1,2,4]`。
>    - `rank = 13 % 6 = 1`。
> 2. 未使用数字 `[1,2,4]`：
>    - \( k = 1 / 2! = 0 \)，取 `nums[0] = 1`，剩余 `[2,4]`。
>    - `rank = 1 % 2 = 1`。
> 3. 未使用数字 `[2,4]`：
>    - \( k = 1 / 1! = 1 \)，取 `nums[1] = 4`，剩余 `[2]`。
>    - `rank = 1 % 1 = 0`。
> 4. 未使用数字 `[2]`：
>    - \( k = 0 / 0! = 0 \)，取 `nums[0] = 2`。
> 5. 最终排列 `[3,1,4,2]`。
>
> ---
>
> ## **3. C++ 代码实现**
> ### **(1) 康托展开**
> ```cpp
> #include <vector>
> #include <algorithm>
> using namespace std;
> 
> int factorial(int n) {
>     int res = 1;
>     for (int i = 2; i <= n; i++) res *= i;
>     return res;
> }
> 
> int cantorExpansion(vector<int>& perm) {
>     int n = perm.size();
>     int rank = 0;
>     vector<bool> used(n + 1, false); // 标记数字是否已使用
>     
>     for (int i = 0; i < n; i++) 	{
>         int cnt = 0;
>         for (int j = 1; j < perm[i]; j++) {
>             if (!used[j]) cnt++;
>         }
>         rank += cnt * factorial(n - i - 1);
>         used[perm[i]] = true;
>     }
>     return rank;
> }
> ```
>
> ### **(2) 逆康托展开**
> ```cpp
> vector<int> inverseCantorExpansion(int rank, int n) {
>     vector<int> nums(n);
>     for (int i = 0; i < n; i++) nums[i] = i + 1; //nums[2] = 3
>     vector<int> perm;
>     
>     for (int i = 0; i < n; i++) {
>         int fact = factorial(n - i - 1);
>         int k = rank / fact;
>         perm.push_back(nums[k]);
>         nums.erase(nums.begin() + k);
>         rank %= fact;
>     }
>     return perm;
> }
> ```
>
> ---
>
> ## **4. 力扣（LeetCode）相关题目**
> ### **(1) [60. 排列序列](https://leetcode.cn/problems/permutation-sequence/)**
> - **题目**：给定 `n` 和 `k`，返回第 `k` 个排列（1-based）。
> - **解法**：直接使用逆康托展开。
>
> ### **(2) [46. 全排列](https://leetcode.cn/problems/permutations/)**
> - **题目**：生成所有排列。
> - **相关**：康托展开可用于唯一标识排列。
>
> ---
>
> ## **5. 总结**
> - **康托展开**：排列 → 排名（字典序）。
> - **逆康托展开**：排名 → 排列。
> - **应用**：排列排名、组合数学、搜索优化。
> - **力扣题目**：60（直接应用）、31、46（相关）。
>
> 你可以直接复制上述公式和代码到 Typora 中使用！

## [61. 旋转链表](https://leetcode.cn/problems/rotate-list/)

> 给你一个链表的头节点 `head` ，旋转链表，将链表每个节点向右移动 `k` 个位置。

思路：将链表首尾相连，并在合适的位置将链表断开。

```c++
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* rotateRight(ListNode* head, int k) {
        //首尾相连,顺便记录一下链表的长度
        int cnt = 1;
        if(head==nullptr) return nullptr;
        ListNode* p = head;
        while(p && p->next) //最后会走到最后一个节点
        {
            cnt++;
            p = p->next;
        }
        p->next = head;
        //走n-k%n个节点
        int x = cnt - k%cnt; //这个值不会超过n了
        while(x-1)
        {
            head = head->next;
            x--;
        }
        ListNode* newHead = head->next;
        head->next = nullptr;
        return newHead;
    }
};
```



## [62. 不同路径](https://leetcode.cn/problems/unique-paths/)

> 一个机器人位于一个 `m x n` 网格的左上角 （起始点在下图中标记为 “Start” ）。
>
> 机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。
>
> 问总共有多少条不同的路径？

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



## [63. 不同路径 II](https://leetcode.cn/problems/unique-paths-ii/)

> 给定一个 `m x n` 的整数数组 `grid`。一个机器人初始位于 **左上角**（即 `grid[0][0]`）。机器人尝试移动到 **右下角**（即 `grid[m - 1][n - 1]`）。机器人每次只能向下或者向右移动一步。
>
> 网格中的障碍物和空位置分别用 `1` 和 `0` 来表示。机器人的移动路径中不能包含 **任何** 有障碍物的方格。
>
> 返回机器人能够到达右下角的不同路径数量。
>
> 测试用例保证答案小于等于 `2 * 109`。

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



## [64. 最小路径和](https://leetcode.cn/problems/minimum-path-sum/)

> 给定一个包含非负整数的 `*m* x *n*` 网格 `grid` ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。
>
> **说明：**每次只能向下或者向右移动一步。
>
>  
>
> **示例 1：**
>
> ![img](assets/minpath.jpg)
>
> ```
> 输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
> 输出：7
> 解释：因为路径 1→3→1→1→1 的总和最小。
> ```

以前做这种题目的时候，往往会对第一行和第一列进行特殊的赋值。但实际上可以多开一维，然后用0x3f的常用做法来做这道题目。代码如下：
```c++
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        vector<vector<int>> dp(m+1, vector<int>(n+1, 0x3f3f3f)); //初值比较大，取min不会过来
        //dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j];
        //dp[-1][x] = dp[x][-1] = INT_MAX, dp[0][0] = grid[0][0](思考DFS，这是最小的合理子问题，所以要单独赋值)
        dp[1][1] = grid[0][0]; //相当于给左上角单独赋值
        for(int i=0;i<m;i++)
        {
            for(int j=0;j<n;j++)
            {
                if(i==0 && j==0) continue; //左上角已经赋值完毕了，所以continue掉
                dp[i+1][j+1] = min(dp[i][j+1], dp[i+1][j]) + grid[i][j];
            }
        }
        return dp[m][n];
    }
};
```



## [66. 加一](https://leetcode.cn/problems/plus-one/)

> 给定一个由 **整数** 组成的 **非空** 数组所表示的非负整数，在该数的基础上加一。
>
> 最高位数字存放在数组的首位， 数组中每个元素只存储**单个**数字。
>
> 你可以假设除了整数 0 之外，这个整数不会以零开头。

```c++
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        vector<int> res;
        int n = digits.size();
        int flag = 0; //是否进位
        digits[n-1] += 1; //+1
        for(int i=n-1;i>=0;i--)
        {
            int digit = (digits[i] + flag);
            flag = 0;
            if(digit>=10)
            {
                digit-=10;
                flag = 1;
            }
            res.emplace_back(digit);
        }
        if(flag) res.emplace_back(flag);
        reverse(res.begin(), res.end());
        return res;
    }
};
```



### （1）额外题目——两个数相加 [989. 数组形式的整数加法](https://leetcode.cn/problems/add-to-array-form-of-integer/)

> 整数的 **数组形式** `num` 是按照从左到右的顺序表示其数字的数组。
>
> - 例如，对于 `num = 1321` ，数组形式是 `[1,3,2,1]` 。
>
> 给定 `num` ，整数的 **数组形式** ，和整数 `k` ，返回 *整数 `num + k` 的 **数组形式*** 。

代码跟上一题差不多，但相当于两个整数相加，而不是简单的+1，代码如下：
```c++
class Solution {
public:
    vector<int> addToArrayForm(vector<int>& num, int k) {
        vector<int> res;
        int n=num.size();
        int flag=0; //是否会进位
        for(int i=n-1;i>=0;i--)
        {
            int number = num[i] + k%10 + flag; //k%10表示k的最后一位
            if(number>=10)
            {
                number-=10;
                flag=1;
            } else flag=0;
            res.push_back(number);
            k/=10; //如果k位数更少,不用担心,k后面一直是0,不影响
        }

        while(k) //k更长
        {
            int number = k%10+flag;
            if(number>=10)
            {
                number-=10;
                flag=1;
            } else flag=0;
            res.push_back(number);
            k/=10;
        }
        if(flag==1) res.push_back(1);
        reverse(res.begin(), res.end());
        return res;
    }
};
```



## [67. 二进制求和](https://leetcode.cn/problems/add-binary/)

> 给你两个二进制字符串 `a` 和 `b` ，以二进制字符串的形式返回它们的和。

### （1）我的做法——比较冗长

还是直接模拟：

```c++
class Solution {
public:
    string addBinary(string a, string b) {
        //跟正常的整数加法类似，0+0 =0 ，0+1 = 1， 1+1 = 0（同时进位）
        string res;
        int m = a.size(), n = b.size();
        int index1 = m-1, index2 = n-1;
        int flag = 0; //是否进位
        while(index1>=0 && index2>=0) 
        {
            int x1 = a[index1] - '0';
            int x2 = b[index2] - '0';
            int sum = x1 + x2 + flag;
            flag = 0;
            if(sum > 1)
            {
                sum -= 2;
                flag = 1;
            }
            res.push_back('0' + sum);
            index1--, index2--;
        }
        //有可能index1>=0，有可能index2>=0
        while(index1>=0)
        {
            int x1 = a[index1] - '0';
            int sum = x1 + flag;
            flag = 0;
            if(sum > 1)
            {
                sum -= 2;
                flag = 1;
            }
            res.push_back('0' + sum);
            index1--;
        }
        while(index2>=0)
        {
            int x1 = b[index2] - '0';
            int sum = x1 + flag;
            flag = 0;
            if(sum > 1)
            {
                sum -= 2;
                flag = 1;
            }
            res.push_back('0' + sum);
            index2--;
        }
        if(flag) res.push_back('1');
        reverse(res.begin(), res.end());
        return res;
    }
};
```



### （2）简便一些的写法

实际上，我们只需要把短的字符串的前面补0，就不需要进行`有可能index1>=0，有可能index2>=0`的特判了，代码如下：
```c++
class Solution {
public:
    string addBinary(string a, string b) {
        //跟正常的整数加法类似，0+0 =0 ，0+1 = 1， 1+1 = 0（同时进位）
        string res;
        int m = a.size(), n = b.size();
        int diff = m - n;
        string tmp;
        for(int i=0;i<abs(diff);i++)
        {
            tmp += '0';
        }
        if(diff>0) //a比b长，b前面补0
        {
            tmp.append(b);
            b = tmp;
        }
        else
        {
            tmp.append(a);
            a = tmp;
        }
        int index = max(n, m) - 1;
        int flag = 0; //是否进位

        while(index>=0) 
        {
            int x1 = a[index] - '0';
            int x2 = b[index] - '0';
            int sum = x1 + x2 + flag;
            flag = 0;
            if(sum > 1)
            {
                sum -= 2;
                flag = 1;
            }
            res.push_back('0' + sum);
            index--;
        }
        if(flag) res.push_back('1');
        reverse(res.begin(), res.end());
        return res;
    }
};
```



Y ： 补零

```C++
class Solution {
public:
    string addBinary(string a, string b) {
        int an = a.size();
        int bn = b.size();
        if(an<bn)
        {
            a = string(bn-an,'0')+a;//cout<<a<<endl;
        }
        else
        {
            b = string(an-bn,'0')+b;//cout<<b<<endl;
        }
        int carry = 0;
        for(int i=max(an,bn)-1;i>=0;i--)
        {
            int t = (a[i]-'0')+(b[i]-'0')+carry;
            a[i] = (t%2+'0');
            carry = t/2;
        }
        if(carry==1)
        {
            a = "1"+a;
        }
        return a;
    }
};
```

