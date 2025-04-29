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

