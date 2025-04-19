# Leetcode——回溯专题

对应[分享丨【题单】链表、二叉树与回溯（前后指针/快慢指针/DFS/BFS/直径/LCA/一般树）- 讨论 - 力扣（LeetCode）](https://leetcode.cn/discuss/post/3142882/fen-xiang-gun-ti-dan-lian-biao-er-cha-sh-6srp/)这里的第四大专题：回溯。

本质是搜索树上的 DFS。

推荐先完成 **§2.7** 节。先理解二叉树上的回溯，再来学习一般情况下的回溯。

# 一、入门回溯

## 1.[17. 电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)

给定一个仅包含数字 `2-9` 的字符串，返回所有它能表示的字母组合。答案可以按 **任意顺序** 返回。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。

![img](assets/200px-telephone-keypad2svg.png)

**示例 1：**

```
输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

```c++
class Solution {
public:
    string numbers[10] = {"","","abc","def","ghi","jkl","mno","pqrs","tuv","wxyz"};
    string path;
    vector<string> res;
    void dfs(string digits, int i) //i表示哪个字母
    {
        int n = digits.size();
        if(i==n)
        {
            res.push_back(path);
            return;
        }
        for(char c: numbers[digits[i]-'0'])
        {
            path[i] = c;
            dfs(digits, i+1); //反正后面还会覆盖,不用pop_back(如果前面是push_back就要记得后面pop_back)
        }
    }
    vector<string> letterCombinations(string digits) {
        int n = digits.size();
        if(n==0) return res;
        path.resize(n);
        dfs(digits,0);
        return res;
    }
};
```

### 时间与空间复杂度的探讨：

- 时间复杂度：$O(n4^n)$，其中$4^n$来源于最多一个按下的数字对应4个字母，n则表示一共有n个按下的数字。而前面的n则是`res.push_back`的时间复杂度，所以总的是$O(n4^n)$
- 空间复杂度：$O(n)$

> 注：`dfs(i)`应当理解为枚举`>=i`的情况，因为除了枚举`i`以外，还要递归处理后面的部分。



# 二、子集型回溯

有「**选或不选**」和「**枚举选哪个**」两种写法。

也可以用**二进制枚举**做。

## 1.[78. 子集](https://leetcode.cn/problems/subsets/)

> 给你一个整数数组 `nums` ，数组中的元素 **互不相同** 。返回该数组所有可能的子集（幂集）。
>
> 解集 **不能** 包含重复的子集。你可以按 **任意顺序** 返回解集。
>
>  **示例 1：**
>
> ```
>输入：nums = [1,2,3]
> 输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
> ```
> 
> **示例 2：**
>
> ```
>输入：nums = [0]
> 输出：[[],[0]]
> ```

### （1）从「**选或不选**」的角度

每个值既可以选，也可以不选，对应两波dfs：

- `dfs(nums, i+1);`表示不选，直接枚举下一个值的选择情况；
- 先push再`dfs(nums, i+1)`表示选，然后枚举下一个值得选择情况，在dfs之后要记得`pop_back()`，恢复现场。

```c++
class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void dfs(vector<int>& nums, int i) //每个数都可以选或者不选,当前枚举到了第i个
    {
        int n = nums.size();
        if(i==n) //枚举完了整个数组
        {
            res.push_back(path);
            return;
        }
        dfs(nums, i+1); //1.不选
        //2.选
        path.push_back(nums[i]);
        dfs(nums, i+1);
        path.pop_back();
    }
    vector<vector<int>> subsets(vector<int>& nums) {
        //1.选或者不选的角度来解题
        dfs(nums, 0);
        return res;
    }
};
```



### 时间与空间复杂度的探讨

- 每个数字都可以选或者不选，时间复杂度为$O(2^n)$。本身将path加入到最后的答案当中还有$O(n)$的复杂度，因此最终的时间复杂度为$O(n2^n)$。
- 空间复杂度：$O(n)$，返回值的空间忽略不计；



### （2）答案的视角（枚举选哪个）

这种角度思考本题，相当于每次进`dfs`函数时都一定会产生一个结果，需要我们自己判断为了产生答案需要让什么样的数进入dfs。此时答案如下：

```c++
class Solution {
public:
    vector<vector<int>> res;
    vector<int> path;
    void dfs(vector<int>& nums, int i)
    {
        int n = nums.size();
        res.push_back(path); //每次进来都会是一个答案
        for(int j=i;j<n;j++)
        {
            path.push_back(nums[j]);
            dfs(nums, j+1); //在下一轮回溯中，如果i==n，这个循环就不会进来了，所以不用额外判断
            path.pop_back();
        }
    }
    vector<vector<int>> subsets(vector<int>& nums) {
        dfs(nums, 0);
        return res;
    }
};
```

> 判断逻辑：每次放完一个数之后，只有大于其的数可以放到后面（防止重复），而每次进dfs函数所产生的解都是合法的。



## 2.[131. 分割回文串](https://leetcode.cn/problems/palindrome-partitioning/)

> 给你一个字符串 `s`，请你将 `s` 分割成一些 子串，使每个子串都是 **回文串** 。返回 `s` 所有可能的分割方案。
>
>  **示例 1：**
>
> ```
>输入：s = "aab"
> 输出：[["a","a","b"],["aa","b"]]
> ```
> 
> **示例 2：**
>
> ```
>输入：s = "a"
> 输出：[["a"]]
> ```
> 
> **提示：**
>
>  - `1 <= s.length <= 16`
>- `s` 仅由小写英文字母组成



### （1）答案的视角（枚举选哪个）

可以用“枚举选哪个”的思路来做，对后面的字符串进行切割判断是否为回文串。代码如下：

```c++
class Solution {
public:
    vector<vector<string>> res;
    vector<string> path;
    bool isValid(string& s)
    {
        int l = 0, r = (int)s.size()-1;
        while(l<=r)
        {
            if(s[l]!=s[r]) return false;
            l++, r--;
        }
        return true;
    }
    void dfs(string s, int idx) //从idx开始划分（可以理解为加分隔符），第一次传入的时候是dfs(s,0)
    {
        int n = s.size();
        if(n==idx)
        {
            res.push_back(path);
            return;
        }
        for(int i=idx;i<n;i++)
        {
            string t = s.substr(idx, i-idx+1);
            if(isValid(t))
            {
                path.push_back(t);
                dfs(s, i+1);
                path.pop_back();
            }
        }
    }
    vector<vector<string>> partition(string s) {
        dfs(s, 0);
        return res;
    }
};
```

> 对于这道题目来说，下标索引还是有写错的可能的，需要注意。



### （2）从「**选或不选**」的角度（精力有限先不看了）

> 对于本题来说，从「**选或不选**」的角度没有那么直观，因此更多还是掌握上面的那种算法。
>
> 比如对于字符串"aba" ，我们在处理的时候，想象着在字符之间有可以选择是否“插入”逗号的位置。当i指向第一个a时，“不选逗号”就是想象a和b之间没有逗号，尝试看"ab" 能不能组成回文子串；“选逗号”就是想象a后面有个逗号，把第一个a单独作为一个回文子串拿出来。
>
> 而对于最后一个字符，因为后面没有其他字符了，所以也就不存在“不选逗号，让它和后面字符组成更长子串”这种情况了，这就是  (i < n - 1) 起作用的地方。

假设每对相邻字符之间有个逗号，那么就看每个逗号是选还是不选。

也可以理解成：是否要把 `s[i] `当成分割出的子串的最后一个字符。注意` s[n−1]` 一定是最后一个字符，一定要选。

此时对应的代码如下：

```c++
class Solution {
public:
    vector<vector<string>> res;
    vector<string> path;
    bool isValid(string& s, int left, int right)
    {
        while(left<=right)
        {
            if(s[left]!=s[right]) return false;
            left++, right--;
        }
        return true;
    }
    void dfs(string s, int i, int start) //i为下一个“逗号”的位置(认为逗号是紧挨着每个字符的)，start为当前字符的起始位置
    {
        int n = s.size();
        if(i==n)
        {
            res.push_back(path);
            return;
        }
        //在当前位置不加逗号，和后面组成字符串（但最后一个没办法和后面组成字符串）
        if(i<n-1)
        {
            dfs(s, i+1, start);
        }
        if(isValid(s, start, i)) //可以构成回文串，继续往后访问
        {
            path.push_back(s.substr(start, i-start+1));
            dfs(s, i+1, i+1); //往后继续访问
            path.pop_back();
        }

    }
    vector<vector<string>> partition(string s) {
        dfs(s, 0, 0);
        return res;
    }
};
```



### （3）时间空间复杂度分析

- 时间复杂度：$O(n2^n)$，答案长度最多为逗号子集的个数（模拟我们用逗号来分割字符串），与上一道题目是类似的；
- 空间复杂度：$O(n)$



## 3.[784. 字母大小写全排列](https://leetcode.cn/problems/letter-case-permutation/)

> 给定一个字符串 `s` ，通过将字符串 `s` 中的每个字母转变大小写，我们可以获得一个新的字符串。
>
> 返回 *所有可能得到的字符串集合* 。以 **任意顺序** 返回输出。

也就是说，每个字母都有“变”与“不变”两种情况，其实也就是每个字母都可以大写和小写。于是思路就是`选或不选`的思路。代码如下：

```c++
class Solution {
public:
    vector<string> letterCasePermutation(string s) {
        //每个字符都可以选或者不选
        vector<string> res;
        int n = s.size();
        string path(n, 0);
        auto dfs = [&](this auto&& dfs, int i) //i表示遍历到了哪个字符
        {
            if(i==n)
            {
                res.push_back(path);
                return;
            }
            if(isalpha(s[i])) // 注意这个库函数！！
            {
                path[i] = tolower(s[i]);//
                dfs(i+1);
                path[i] = toupper(s[i]);//
                dfs(i+1);
            } 
            else //不是字母,直接递归下一个即可
            {
                path[i]=s[i];
                dfs(i+1); 
            }
        };
        dfs(0);
        return res;
    }
};
```

- 时间复杂度：$O(n2^n)$



## 4.[LCP 51. 烹饪料理 ](https://leetcode.cn/problems/UEcfPD/):cat:

> 欢迎各位勇者来到力扣城，城内设有烹饪锅供勇者制作料理，为自己恢复状态。
>
> 勇者背包内共有编号为 `0 ~ 4` 的五种食材，其中 `materials[j]` 表示第 `j` 种食材的数量。通过这些食材可以制作若干料理，`cookbooks[i][j]` 表示制作第 `i` 种料理需要第 `j` 种食材的数量，而 `attribute[i] = [x,y]` 表示第 `i` 道料理的美味度 `x` 和饱腹感 `y`。
>
> 在饱腹感不小于 `limit` 的情况下，请返回勇者可获得的最大美味度。如果无法满足饱腹感要求，则返回 `-1`。
>
> **注意：**
>
> - 每种料理只能制作一次。
>
> **示例 1：**
>
> > 输入：`materials = [3,2,4,1,2]` `cookbooks = [[1,1,0,1,2],[2,1,4,0,0],[3,2,4,1,0]]` `attribute = [[3,2],[2,4],[7,6]]` `limit = 5`
> >
> > 输出：`7`
> >
> > 解释： 食材数量可以满足以下两种方案： 方案一：制作料理 0 和料理 1，可获得饱腹感 2+4、美味度 3+2 方案二：仅制作料理 2， 可饱腹感为 6、美味度为 7 因此在满足饱腹感的要求下，可获得最高美味度 7
>
> **示例 2：**
>
> > 输入：`materials = [10,10,10,10,10]` `cookbooks = [[1,1,1,1,1],[3,3,3,3,3],[10,10,10,10,10]]` `attribute = [[5,5],[6,6],[10,10]]` `limit = 1`
> >
> > 输出：`11`
> >
> > 解释：通过制作料理 0 和 1，可满足饱腹感，并获得最高美味度 11
>
> **提示：**
>
> - `materials.length == 5`
> - `1 <= cookbooks.length == attribute.length <= 8`
> - `cookbooks[i].length == 5`
> - `attribute[i].length == 2`
> - `0 <= materials[i], cookbooks[i][j], attribute[i][j] <= 20`
> - `1 <= limit <= 100`

这道回溯题目可以用”选或不选“的思路来做。一定要注意写好处理判断的逻辑，剩下的交给回溯本身来进行即可，这种类型题目很有可能会出在米小游里面。

```c++
class Solution {
public:
    int perfectMenu(vector<int>& materials, vector<vector<int>>& cookbooks, vector<vector<int>>& attribute, int limit) {
        int res = -1; 
        //每种料理都可以"选"或者"不选"
        int n = cookbooks.size(); //这么多种料理
        auto dfs = [&](this auto&& dfs, int i, int value, int curY) //i表示当前待选择是否烹饪的是第i个,value则表示现在总的美味度,curY则表示当前的饱腹感
        {
            if(i==n)
            {
                if(curY>=limit) //饱腹感是合格的
                {
                    res = max(res, value); //记录最大的美味度
                }
                return;
            }
            //不选当前料理,继续遍历
            dfs(i+1, value,curY);//！！！！
            //选当前料理,需要看当前料理能不能烹饪
            bool flag = true; //一开始认为能烹饪
            for(int idx=0;idx<materials.size();idx++) //食材不够了,不能烹饪
            {
                if(materials[idx]-cookbooks[i][idx]<0)
                {
                    flag = false;
                    break;
                }
            }
            if(flag)
            {
                for(int idx=0;idx<materials.size();idx++)
                {
                    materials[idx]-=cookbooks[i][idx];
                }
                dfs(i+1, value+attribute[i][0], curY+attribute[i][1]);
                //复原现场
                for(int idx=0;idx<materials.size();idx++)
                {
                    materials[idx]+=cookbooks[i][idx];
                }
            }
        };
        dfs(0, 0, 0);
        return res;
    }
};
```



## 5.[2397. 被列覆盖的最多行数](https://leetcode.cn/problems/maximum-rows-covered-by-columns/)

> 不看图的话这题不太好理解，复习的时候直接去链接里面看吧。
>
> 任选 `numSelect` 个列，把这些列里的 1 全变成 0，问这样做最多能使多少行变成全 0

解题思路（看m和n的数据范围，应该可以纯暴力回溯，==注意本题有二进制枚举和Gosper‘s Hack的更快更好解法，但慢慢来吧，本题数据可以用回溯来做。更具体可以参考[2397. 被列覆盖的最多行数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-rows-covered-by-columns/solutions/1798794/by-endlesscheng-dvxe/)==）：

- 每一列都处于”选或不选“的状态。但由于最终必须要选择numSelect个不同列，因此还需要记录一下选择到了哪一列以及已经选择的列数，并依此作为边界判断条件。

现在问题就转换为了，如何获知几行的1被全覆盖了呢？应该可以用一个哈希来存储所有选中的列，然后在选择到最后一列的时候判断每一行的情况。代码如下：
```c++
class Solution {
public:
    int maximumRows(vector<vector<int>>& matrix, int numSelect) {
        int res = 0;
        unordered_set<int> us; //记录已经选择的列
        int m = matrix.size();
        int n = matrix[0].size(); //m是行,n是列
        auto dfs=[&](this auto&& dfs, int i) //假设先完全不考虑剪枝,纯暴力应该也能过
        {
            if(i==n) //遍历到了最后,开始检查
            {
                int cnt = 0;
                for(int r=0;r<m;r++)
                {
                    bool flag = true;
                    for(int c=0;c<n;c++)
                    {
                        if(matrix[r][c]==1)
                        {
                            if(!us.contains(c)) 
                            {
                                flag = false;
                                break;
                            }
                        }
                    }
                    if(flag) cnt+=1; //此时相当于所有的1都在选的列当中
                }
                res = max(res, cnt);
                return;
            }
            //不选:此时已经选的个数为us.size()个,总的为numSelect个,已经遍历到了第i个,总共n列
            //不选的情况会麻烦一点,假设从现在列开始后面都选,总的选择数大于numSelect,才可以选择不选
            if((us.size()+(n-i))>numSelect)
            {
                dfs(i+1); 
            }
    
            //选:只要当前选择个数还没到numSelect个,就可以选
            if(us.size()<numSelect)
            {
                us.insert(i);
                dfs(i+1);
                us.erase(i);
            }
        };
        dfs(0);
        return res;
    }
};
```

Y 下面这个没怎么剪枝不用看 看下下面的位运算

```C++
class Solution {
public:
    int maximumRows(vector<vector<int>>& matrix, int numSelect) {
        //1不能出现在没被覆盖的列上，这行才算能被覆盖
        //回溯
        //选/不选
        int maxRows=0;
        //unordered_map<int,int> path;
        unordered_set<int> path;
        int m = matrix.size();
        int n = matrix[0].size();
        // vector<int> path(n,0);
        
        auto dfs = [&](this auto&& dfs,int start)
        {
            if(path.size()==numSelect)//**
            {
                int rows=m;
                for(int i=0;i<m;i++)
                {
                    for(int j=0;j<n;j++)
                    {
                        if(path.find(j)==path.end()&&matrix[i][j]==1) 
                        {
                            rows--;
                            break;
                        }
                    }
                }
                maxRows = max(maxRows,rows);
                return;
            }
            if(start==n)return;
            
            //不选
            dfs(start+1);
            //选
            // path[start]=1;
            path.insert(start);
            dfs(start+1);
            // path[start]=0;
            path.erase(start);
        };
        dfs(0);
        return maxRows;
    }
};
```

#### 位运算优化
##### 回溯

```C++
class Solution {
public:
    int maximumRows(vector<vector<int>>& matrix, int numSelect) {
        //1不能出现在没被覆盖的列上，这行才算能被覆盖
        //回溯
        //选/不选
        int maxRows=0;
        int m = matrix.size();
        int n = matrix[0].size();
        vector<int> mask(m,0);
        //注意 这里位的排列次序 从低到高是从右到左的！！！即011表示的是110
        //不过没有关系 只要保证path计算也是这样就可
         for (int i = 0; i < m; i++) 
         {
            for (int j = 0; j < n; j++) 
                mask[i] |= matrix[i][j] << j;         
        }
        auto dfs = [&](this auto&& dfs,int start,int path)
        {
            if(__builtin_popcount(path)==numSelect)
            {
                int rows=0;
                for(int i=0;i<m;i++)
                {
                    rows+=((path&mask[i])==mask[i]);//括号括括号！
                }
                maxRows = max(maxRows,rows);
                return;
            }
            
            if(start==n)return;
            
            //不选
            dfs(start+1,path);
            //选
            path|=(1<<start);
            dfs(start+1,path);
            path&=(0<<start);
        };
        dfs(0,0);
        return maxRows;
    }
};
```

##### 枚举

当然了 ，这题实际上可以枚举做，枚举 {0,1,2,⋯,*n*−1} 的所有大小为 *numSelect* 的子集 *subset*，表示我们所选的列。

```C++
class Solution {
public:
    int maximumRows(vector<vector<int>> &mat, int numSelect) {
        int m = mat.size(), n = mat[0].size();
        vector<int> mask(m);
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                mask[i] |= mat[i][j] << j;
            }
        }

        int ans = 0;
        for (int subset = 0; subset < (1 << n); subset++) {
            if (__builtin_popcount(subset) == numSelect) {
                int covered_rows = 0;
                for (int row : mask) {
                    if ((row & subset) == row) {
                        covered_rows++;
                    }
                }
                ans = max(ans, covered_rows);
            }
        }
        return ans;
    }
};
```



## 6.[1239. 串联字符串的最大长度](https://leetcode.cn/problems/maximum-length-of-a-concatenated-string-with-unique-characters/)

> 给定一个字符串数组 `arr`，字符串 `s` 是将 `arr` 的含有 **不同字母** 的 **子序列** 字符串 **连接** 所得的字符串。
>
> 请返回所有可行解 `s` 中最长长度。
>
> **子序列** 是一种可以从另一个数组派生而来的数组，通过删除某些元素或不删除元素而不改变其余元素的顺序。
>
>  **示例 1：**
>
> ```
>输入：arr = ["un","iq","ue"]
> 输出：4
> 解释：所有可能的串联组合是：
> - ""
> - "un"
> - "iq"
> - "ue"
> - "uniq" ("un" + "iq")
> - "ique" ("iq" + "ue")
> 最大长度为 4。
> ```
> 
> **示例 2：**
>
> ```
>输入：arr = ["cha","r","act","ers"]
> 输出：6
> 解释：可能的解答有 "chaers" 和 "acters"。
> ```
> 
> **示例 3：**
>
> ```
>输入：arr = ["abcdefghijklmnopqrstuvwxyz"]
> 输出：26
> ```
> 
> **提示：**
>
>  - `1 <= arr.length <= 16`
>- `1 <= arr[i].length <= 26`
> - `arr[i]` 中只含有小写英文字母

本题依旧可以用”选或不选“的思路来做。不选的话，就跳转到下一个，选的话则必须保证没有重复字母。

- 如何保证没有重复字母呢？可以开一个26维的array来做，并依此来判断（应该也可以简化为位运算？但不熟练的话还是先不这么激进了）。

代码如下（代码写的比较冗长，但确实可以完成需求，而且时间空间运行效率也还不错，因此有优化后面再来补充吧）：
```c++
class Solution {
public:
    int maxLength(vector<string>& arr) {
        array<int, 26> alphas;
        int n = arr.size();
        int cnt = 0;
        int res = 0;
        //提前存一下哪些本身有重复字符
        vector<bool> isValid(n);
        for(int i=0;i<n;i++)
        {
            int temp[26]={0}; //必须显式初始化为0,美好C++
            isValid[i]=true;
            for(int j=0;j<(int)arr[i].size();j++)
            {
                if(temp[arr[i][j]-'a']>0)
                {
                    isValid[i]=false;
                    break;
                }
                temp[arr[i][j]-'a']++;
            }
        }

        auto dfs=[&](this auto&& dfs, int i) //遍历到第i个字符串了
        {
            if(i==n)
            {
                res = max(res, cnt);
                return;
            }
            //不选,直接进下一个
            dfs(i+1);
            //选,则需要保证字母没有
            bool flag = isValid[i];
            if(!flag) return;
            for(int idx = 0;idx<(int)arr[i].size();idx++)
            {
                if(alphas[arr[i][idx]-'a']!=0)
                {
                    flag = false;
                    break;
                }
            }
            if(flag) //当然,自身有重复字符肯定不行,flag=false
            {
                //放进去
                for(int idx = 0;idx<(int)arr[i].size();idx++)
                {
                    alphas[arr[i][idx]-'a']=1;
                }
                cnt += (int)arr[i].size();
                dfs(i+1);
                for(int idx = 0;idx<(int)arr[i].size();idx++)
                {
                    alphas[arr[i][idx]-'a']=0;
                }
                cnt -= (int)arr[i].size();
            }
        };
        dfs(0);
        return res;
    }
};
```

Y 还可以用位运算优化 后面再说吧

```C++
class Solution {
public:
    int maxLength(vector<string>& arr) {
        //回溯 选/不选
        //存储umap
        int maxLen =0; 
        int n=arr.size();
        vector<array<int,26> > vec(n,array<int,26>{0});
        vector<bool> isValid(n,false);

        for(int i=0;i<n;i++)
        {
            bool flag=false;
            for(int j=0;j<arr[i].size();j++)
            {
                int id = arr[i][j]-'a';
                if( vec[i][id]>0) 
                {
                    flag = true;
                }
                vec[i][id]++;
            }
            if(flag==false)isValid[i]=true;

        }
        array<int,26> patharr;
        auto dfs = [&](this auto &&dfs,int start,int len)
        {
            if(start==n)
            {
                maxLen = max(maxLen,len);
                return;
            }
            //不选
            dfs(start+1,len);
            //选
            if(!isValid[start])return;
            for(int i=0;i<26;i++)
            {
                if(patharr[i]>0&&vec[start][i]>0)return;
            }
            //可选
            for(int i=0;i<arr[start].size();i++)patharr[arr[start][i]-'a']++;
            dfs(start+1,len+arr[start].size());
            for(int i=0;i<arr[start].size();i++)patharr[arr[start][i]-'a']--;
        };
        dfs(0,0);
        return maxLen;
    }
};
```



## 7.（特殊，可以重复选）[39. 组合总和](https://leetcode.cn/problems/combination-sum/) :eyes:

> 给你一个 **无重复元素** 的整数数组 `candidates` 和一个目标整数 `target` ，找出 `candidates` 中可以使数字和为目标数 `target` 的 所有 **不同组合** ，并以列表形式返回。你可以按 **任意顺序** 返回这些组合。
>
> `candidates` 中的 **同一个** 数字可以 **无限制重复被选取** 。如果至少一个数字的被选数量不同，则两种组合是不同的。 
>
> 对于给定的输入，保证和为 `target` 的不同组合数少于 `150` 个。
>
>  **示例 1：**
>
> ```
>输入：candidates = [2,3,6,7], target = 7
> 输出：[[2,2,3],[7]]
> 解释：
> 2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
> 7 也是一个候选， 7 = 7 。
> 仅有这两种组合。
> ```
> 
> **示例 2：**
>
> ```
>输入: candidates = [2,3,5], target = 8
> 输出: [[2,2,2,2],[2,3,3],[3,5]]
> ```
> 
> **示例 3：**
>
> ```
>输入: candidates = [2], target = 1
> 输出: []
> ```
> 
> **提示：**
>
>  - `1 <= candidates.length <= 30`
>- `2 <= candidates[i] <= 40`
> - `candidates` 的所有元素 **互不相同**
>- `1 <= target <= 40`

本题也可以类比用”选或不选“的思路，只不过此时选的话继续进入`dfs(i)`，表示下一轮可以继续选择当前值。注意某些条件触发则无法递归（比如target-candidates[i]<0则return）。本题代码如下：

```c++
class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
       vector<vector<int>> res;
       vector<int> path;
       int n = candidates.size();
       auto dfs = [&](this auto&& dfs,int i,int curTarget) //i表示当前的值,curTarget表示当前剩下的值
       {
            if(curTarget==0) //考虑到了最后一个值了
            {
                res.push_back(path);
                return;
            }
            if(i==n || curTarget<0) return;
            //不选
            dfs(i+1, curTarget);
            //选
            path.push_back(candidates[i]);
            dfs(i, curTarget-candidates[i]); //可以重复选,dfs不再是i+1,而是i
            path.pop_back();
       };
       dfs(0, target);
       return res;
    }
};
```

可以考虑进行剪枝优化，既然回溯的复杂度比较高，而`candidates`中的数又会频繁使用，因此可以提前把`candidates`中的数进行排序，如果`curTarget<candidates[i]`，说明后面的更不可能能满足题意了，直接return即可。只需要改一句（当然前面要排序）：

```c++
if(i==n || curTarget<candidates[i]) return;
```

实测这样的话可以提速不少。



没看出排序剪枝快多少嘤嘤

```C++
class Solution {
public:
    vector<vector<int> > res;
    vector<int> path;
    
    void dfs(vector<int>& candidates, int target,int start,int sum)
    {
        if(sum==target)
        {
            res.push_back(path);
            return;
        }
        if(start==candidates.size())return;
        if(sum>target||candidates[start]>target)return;//剪枝 //排序剪枝
        //不选
        dfs(candidates,target,start+1,sum);
        //选 
        //选自己
        sum+=candidates[start];
        path.push_back(candidates[start]);
        dfs(candidates,target,start,sum);
        //选下一个
        //dfs(candidates,target,start+1,sum);//这个不要写！不然会重复 因为实际上已经包含在了选选选然后不选里面！！！
        path.pop_back();

    }
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        sort(candidates.begin(),candidates.end());
        dfs(candidates,target,0,0);
        return res;
    }
};
```



# 三、划分型回溯

把分割线（逗号）看成是可以「选或不选」的东西，本质在一定程度上是子集型回溯。前面的题目「分割回文串」即可以理解为划分型回溯的题目。这部分整理一下其他题：

## 1.[2698. 求一个整数的惩罚数](https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/)（看题解） :cat:

> 给你一个正整数 `n` ，请你返回 `n` 的 **惩罚数** 。
>
> `n` 的 **惩罚数** 定义为所有满足以下条件 `i` 的数的平方和：
>
> - `1 <= i <= n`
> - `i * i` 的十进制表示的字符串可以分割成若干连续子字符串，且这些子字符串对应的整数值之和等于 `i` 。
> - **示例 1：**
>
>   ```
>   输入：n = 10
>   输出：182
>   解释：总共有 3 个范围在 [1, 10] 的整数 i 满足要求：
>   - 1 ，因为 1 * 1 = 1
>   - 9 ，因为 9 * 9 = 81 ，且 81 可以分割成 8 + 1 。
>   - 10 ，因为 10 * 10 = 100 ，且 100 可以分割成 10 + 0 。
>   因此，10 的惩罚数为 1 + 81 + 100 = 182
>   ```

这种题在考场上可以这样，先计算出范围内所有符合题意的数，如果不多的话直接打表，可以防止超时。对于本题来说，”选或不选“的做法没有那么直观，我们就直接在当前切割位置往后枚举各个切割位置来计算了。

```c++
class Solution {
public:
    bool dfs(string s, int target, int curSum, int start) //n是i*i, target是目标值(为i), start是当前分割到的位置,curSum是目前的累计值
    {
        int n = s.size();
        if(start==n) //分割类的题目,必须分割完,因此需要等start==n才能下结论
        {
            return (curSum==target);
        }
        int x = 0; //计算当前分割产生的新值
        for(int i=start;i<n;i++)
        {
            x = x*10 + s[i]-'0';
            bool r = dfs(s, target, curSum+x, i+1); //查看每种切割方式是否会带来true
            if(r) return true; //找到一种,则这个数符合要求
        }
        return false;
    }
    int init(int n)
    {
        //计算出符合要求的值,即i * i 的十进制表示的字符串可以分割成若干连续子字符串，且这些子字符串对应的整数值之和等于i 。
        //i预处理到1000即可,复杂度应该算可以接受
        vector<int> preSum(1001);
        for(int i=1;i<=1000;i++)
        {
            bool isValid = dfs(to_string(i*i), i, 0, 0);
            preSum[i] = preSum[i-1] + (isValid ? i*i:0); //计算前缀和
        }
        //for(int r:res) cout<<r<<endl;
        return preSum[n];
    }
    int punishmentNumber(int n) {
        return init(n);
    }
};
```

感觉划分型回溯掌握的并不是太好，还需要多做一些题目加深理解。



Y：不好的用例👇以下这个写法较**慢** 应该是因为用的字符串 用数字会快，不过下面的错误值得记住不要再犯

```C++
class Solution {
public:
    bool isValid(int a)
    {
        //i * i 的十进制表示的字符串可以分割成若干连续子字符串，且这些子字符串对应的整数值之和等于 i
        auto dfs = [&](this auto&& dfs,int target,string str,int start)->bool
        {
            if(target<0)return false;
            if(start==str.size())
            {
                if(target==0)return true;
                return false;
            }
            //1296   1 2/29/296
            for(int i=start;i<str.size();i++)
            {
                //string subs = str.substr(i,i-start+1);//!错误❌ ！是从start开始不是i！！！！！
                string subs = str.substr(start,i-start+1);
                int newtarget = target-stoi(subs);
                //target-=stoi(subs);//!错误❌ 因为target被剪掉了会影响后面的 要么new新的要么直接放进去
                if(dfs(newtarget,str,i+1))return true;
            }
            return false;
        };
        return dfs(a,to_string(a*a),0);
    }
    int punishmentNumber(int n) 
    {
        //遍历1-n 寻找所有数字是不是 符合的数
        //是就加起来
        int res=0;
        for(int i=1;i<=n;i++)
        {
            if(isValid(i))
            {
                res+=i*i;
            }
        }
        return res;
    }
};
```

改为整数，会快一些

```C++
for(int i=start;i<str.size();i++)
{
    //string subs = str.substr(start,i-start+1);
    //int newtarget = target-stoi(subs);
    x=x*10+(str[i]-'0');
    if(dfs(target-x,str,i+1))return true;//找到一个即可
}
return false;
```

但是更快有可能要预存储  如果输入多个数字啥的 算前缀和 

https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/ 没看

```C++
int PRE_SUM[1001];

int init = []() {
    for (int i = 1; i <= 1000; i++) 
    {
        string s = to_string(i * i);
        int n = s.length();
        function<bool(int, int)> dfs = [&](int p, int sum) -> bool 
        {
            if (p == n) // 递归终点
            { 
                return sum == i; // i 符合要求
            }
            int x = 0;
            for (int j = p; j < n; j++) // 枚举分割出从 s[p] 到 s[j] 的子串
            { 
                x = x * 10 + s[j] - '0'; // 子串对应的整数值
                if (dfs(j + 1, sum + x)) 
                {
                    return true;
                }
            }
            return false;
        };
        PRE_SUM[i] = PRE_SUM[i - 1] + (dfs(0, 0) ? i * i : 0);
    }
    return 0;
}();

class Solution {
public:
    int punishmentNumber(int n) 
    {
        return PRE_SUM[n];
    }
};

```



## 2.[1593. 拆分字符串使唯一子字符串的数目最大](https://leetcode.cn/problems/split-a-string-into-the-max-number-of-unique-substrings/)

> 给你一个字符串 `s` ，请你拆分该字符串，并返回拆分后唯一子字符串的最大数目。
>
> 字符串 `s` 拆分后可以得到若干 **非空子字符串** ，这些子字符串连接后应当能够还原为原字符串。但是拆分出来的每个子字符串都必须是 **唯一的** 。
>
> 注意：**子字符串** 是字符串中的一个连续字符序列。
>
>  **示例 1：**
>
> ```
>输入：s = "ababccc"
> 输出：5
> 解释：一种最大拆分方法为 ['a', 'b', 'ab', 'c', 'cc'] 。像 ['a', 'b', 'a', 'b', 'c', 'cc'] 这样拆分不满足题目要求，因为其中的 'a' 和 'b' 都出现了不止一次。
> ```
> 
> **示例 2：**
>
> ```
>输入：s = "aba"
> 输出：2
> 解释：一种最大拆分方法为 ['a', 'ba'] 。
> ```
> 
> **示例 3：**
>
> ```
>输入：s = "aa"
> 输出：1
> 解释：无法进一步拆分字符串。
> ```
> 
> **提示：**
>
>  - `1 <= s.length <= 16`
>- `s` 仅包含小写英文字母

依旧相当于对字符串做划分，不过每次划分的结果会被保存在哈希表当中，在dfs之后不要忘了恢复现场。代码如下：

```c++
class Solution {
public:
    int maxUniqueSplit(string s) {
        int res = 0;
        unordered_set<string> us;
        int n = s.size();
        auto dfs = [&](this auto&& dfs, int start) //start为开始枚举切割的位置
        {
            if(start==n)
            {
                res = max(res, (int)us.size()); //已经撑到最后了,表明是一个合理的字符串,此时哈希表里的都是拆出来的结果,作比较即可
                return;
            }
            for(int i=start;i<n;i++) //可以枚举切割
            {
                string t = s.substr(start, i-start+1); //划分出来的字符串
                if(!us.contains(t))
                {
                    us.insert(t);
                    dfs(i+1); //枚举下一位【⚠】我们已经将start->i的字符串放进来了，接下来要从i+1开始而不是start+1！！
                    us.erase(t);
                }
            }
        };
        dfs(0);
        return res;
    }
};
```



## 3.[1849. 将字符串拆分为递减的连续值](https://leetcode.cn/problems/splitting-a-string-into-descending-consecutive-values/)（看题解）

> 给你一个仅由数字组成的字符串 `s` 。
>
> 请你判断能否将 `s` 拆分成两个或者多个 **非空子字符串** ，使子字符串的 **数值** 按 **降序** 排列，且每两个 **相邻子字符串** 的数值之 **差** 等于 `1` 。
>
> - 例如，字符串 `s = "0090089"` 可以拆分成 `["0090", "089"]` ，数值为 `[90,89]` 。这些数值满足按降序排列，且相邻值相差 `1` ，这种拆分方法可行。
> - 另一个例子中，字符串 `s = "001"` 可以拆分成 `["0", "01"]`、`["00", "1"]` 或 `["0", "0", "1"]` 。然而，所有这些拆分方法都不可行，因为对应数值分别是 `[0,1]`、`[0,1]` 和 `[0,0,1]` ，都不满足按降序排列的要求。
>
> 如果可以按要求拆分 `s` ，返回 `true` ；否则，返回 `false` 。
>
> **子字符串** 是字符串中的一个连续字符序列。

这种划分型的题目不太好用”选或不选“的思路来做，因此可以直接遍历枚举划分位置来完成这道题。代码如下：

> 不知道第一个是什么怎么办？其实只要对第一个字符串进行枚举就可以了。这样后面的就可以有一个对应的初值，代码就会变得很好写。`这道题的坑人点实在是太多，注意unsigned long long完全可以包住19位的数。`参考[数据类型范围 | Microsoft Learn](https://learn.microsoft.com/zh-cn/cpp/cpp/data-type-ranges?view=msvc-170)

```c++
class Solution {
public:
    bool splitString(string s) {
        //去除前导0
        int i = 0;
        int n = s.size();
        for(i=0;i<n;i++)
        {
            if(s[i]!='0') break;
        }

        //lastNum是上次划分得到的值,start是当前开始划分的位置
        auto dfs = [&](this auto&& dfs, int start, unsigned long long lastNum)->bool
        {   
            if(start==n) return true;
            //可剪枝:如果lastNum是0,则看一下后面的是不是都是0,是的话return true(相当于后面的0都归到一起),不是的话return false
            if(lastNum==0)
            {
                for(int idx=start;idx<n;idx++)
                {
                    if(s[idx]!='0') return false;
                }
                return true;
            }
            for(int idx=start;idx<n;idx++)
            {
                unsigned long long curNum = stoull(s.substr(start, idx-start+1));
                if(curNum==lastNum-1)
                {
                    bool res = dfs(idx+1, curNum);
                    if(res) return true;
                }
            }
            return false;
        };

        for(int j=i; j<n-1;j++) //此时i指向第一个非0的字符,但还是有可能越界,比如999999999999这种数,unsigned long long的范围是0~18446744073709551615,是20位,因为在枚举的时候会至少划分两段,因此至多是19位,可以被unsigned long long 涵盖住,所以使用unsigned long long是可以的
        {
            unsigned long long first = stoull(s.substr(i, j-i+1));
            bool res = dfs(j+1, first); //从j+1开始遍历
            if(res) return true;
        }
        return false;
    }
};
```

Y 

以下未剪枝 剪枝看上面

>以下两种写法不等价
>```C++
>//return dfs(j+1,num);//❌不可以这么写！它和下面的不等价！这个是false也会返回 直接结束了不判断后面
>if(dfs(j+1,num))return true;//这个是只有true才返回 
>```

```c++
class Solution {
public:
    bool splitString(string s) {
        //先拆第一个
        //先把前导0去掉
        int is=0;
        int n=s.size();
        for(is=0;is<n&&s[is]=='0';is++);
        bool flag=false;

        auto dfs = [&](this auto&& dfs,int i,unsigned long long lastNum)->bool
        {
            if(i==n)
            {
                return true;
            }
            // for(int j=0;j<n;j++)//错误
             for(int j=i;j<n;j++)
            {
                string subs = s.substr(i,j-i+1);
                unsigned long long num = stoull(subs);
                if(num==lastNum-1)
                {
                    //return dfs(j+1,num);//❌不可以这么写！它和下面的不等价！这个是false也会返回 直接结束了不判断后面
                    if(dfs(j+1,num))return true;//这个是只有true才返回 
                }
            }
            return false;
        };

        for(int i=is;i<n-1;i++)//至少要留一个字母 因为要被拆至少2个
        {
            string str = s.substr(is,i-is+1);
            unsigned long long num = stoull(str);
            if(dfs(i+1,num))return true;
        }
        
    
        return false;
    }
};
```

## ==4.[306. 累加数](https://leetcode.cn/problems/additive-number/)==

> **累加数** 是一个字符串，组成它的数字可以形成累加序列。
>
> 一个有效的 **累加序列** 必须 **至少** 包含 3 个数。除了最开始的两个数以外，序列中的每个后续数字必须是它之前两个数字之和。
>
> 给你一个只包含数字 `'0'-'9'` 的字符串，编写一个算法来判断给定输入是否是 **累加数** 。如果是，返回 `true` ；否则，返回 `false` 。
>
> **说明：**累加序列里的数，除数字 0 之外，**不会** 以 0 开头，所以不会出现 `1, 2, 03` 或者 `1, 02, 3` 的情况。
>
>  **示例 1：**
>
> ```
>输入："112358"
> 输出：true 
> 解释：累加序列为: 1, 1, 2, 3, 5, 8 。1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8
> ```
> 
> **示例 2：**
>
> ```
>输入："199100199"
> 输出：true 
> 解释：累加序列为: 1, 99, 100, 199。1 + 99 = 100, 99 + 100 = 199
> ```
> 
> - `num` 仅由数字（`0` - `9`）组成

这道题目算是上一题的进阶版本，



# 四、组合型回溯

有个数上的约束。也算作子集型回溯。

## 1.[77. 组合](https://leetcode.cn/problems/combinations/)

> 给定两个整数 `n` 和 `k`，返回范围 `[1, n]` 中所有可能的 `k` 个数的组合。
>
> 你可以按 **任何顺序** 返回答案。
>
>  **示例 1：**
>
> ```
>输入：n = 4, k = 2
> 输出：
> [
> [2,4],
> [3,4],
>   [2,3],
>   [1,2],
>   [1,3],
>   [1,4],
>   ]
>   ```
> 
> **示例 2：**
>
> ```
>输入：n = 1, k = 1
> 输出：[[1]]
> ```
> 
> **提示：**
>
>  - `1 <= n <= 20`
>- `1 <= k <= n`

这算是一道经典题目，在遍历枚举的时候，我们可以从后往前遍历，这样在剪枝的时候会更方便一些。

![image-20250309124438299](Leetcode%E2%80%94%E2%80%94%E5%9B%9E%E6%BA%AF%E4%B8%93%E9%A2%98.assets/image-20250309124438299.png)

举个例子，假设n=5，k=3，path.size()=1，那么还需要选择两个数(d=k-path.size())，此时如果当前的数i<d，则没办法再选择了，因此只有`i>=d`的才会继续走dfs的逻辑，这就是剪枝。

回溯结束的条件是“path.size()==k”。

本题代码如下（通过倒序的遍历，剪枝就变得很容易思考了，并且从代码角度也更容易写一些）：
```c++
class Solution {
public:
    vector<vector<int>> combine(int n, int k) {
        vector<vector<int>> res;
        vector<int> path;
        //从后往前遍历
        auto dfs = [&](this auto&& dfs, int start) 
        {
            int d=k-path.size();
            if(d==0)
            {
                res.push_back(path);
                return;
            }
            for(int i=start;i>=d;i--)
            {
                path.push_back(i);
                dfs(i-1);
                path.pop_back();
            }
        };
        dfs(n);
        return res;
    }
};
```



### （1）时间与空间复杂度分析

- 时间复杂度：分析回溯问题的时间复杂度，有一个通用公式：**路径长度**×**搜索树的叶子数**。对于本题来说，路径长度为k，搜索树的叶子数为$C(n,k)$，因此总的时间复杂度为$O(k*C(n,k))$。
- 空间复杂度：$O(k)$，返回值不计入。



## 2.[216. 组合总和 III](https://leetcode.cn/problems/combination-sum-iii/)

> 找出所有相加之和为 `n` 的 `k` 个数的组合，且满足下列条件：
>
> - 只使用数字1到9
> - 每个数字 **最多使用一次** 
>
> 返回 *所有可能的有效组合的列表* 。该列表不能包含相同的组合两次，组合可以以任何顺序返回。
>
> 2 <= k <= 9
> 1 <= n <= 60
>
> **示例 1:**
>
> ```
>输入: k = 3, n = 7
> 输出: [[1,2,4]]
> 解释:
> 1 + 2 + 4 = 7
> 没有其他符合的组合了。
> ```
> 
> **示例 2:**
>
> ```
>输入: k = 3, n = 9
> 输出: [[1,2,6], [1,3,5], [2,3,4]]
> 解释:
> 1 + 2 + 6 = 9
> 1 + 3 + 5 = 9
> 2 + 3 + 4 = 9
> 没有其他符合的组合了。
> ```
> 
> **示例 3:**
>
> ```
>输入: k = 4, n = 1
> 输出: []
> 解释: 不存在有效的组合。
> 在[1,9]范围内使用4个不同的数字，我们可以得到的最小和是1+2+3+4 = 10，因为10 > 1，没有有效的组合。
> ```

与上一题类似，依然是从9到1倒序遍历（每个数只能用一次），同时在dfs当中传入一个target参数。如果`path.size()==k&&target==0`时，认为找到了一组符合条件的数。以下分析剪枝条件：

- （1）依旧是如果`i<(k-path.size())`，说明剩下的数凑不到k个了，此时return即可；
- （2）由于每个数都只能用一次，所以如果剩下的数加在一起都不如target大，则直接return掉，剩下的数应该是1+2+...+i=(1+i)*i/2,用这个值还可以进行一波剪枝。

最终代码如下：

```c++
class Solution {
public:
    vector<vector<int>> combinationSum3(int k, int n) {
        vector<vector<int>> res;
        vector<int> path;
        auto dfs = [&](this auto&& dfs, int start, int target)
        {
            int d = k - path.size();
            if(d==0)
            {
                if(target==0)
                {
                    res.push_back(path);
                }
                return;
            }
            //用等差数列通项公式提前剪枝
            if(((1+start)*start/2)<target) return;
            for(int i=start;i>=d;i--)
            {
                path.push_back(i);
                dfs(i-1, target-i);
                path.pop_back();
            }
        };
        dfs(9,n);
        return res;
    }
};
```



## 3.[22. 括号生成](https://leetcode.cn/problems/generate-parentheses/)

> 数字 `n` 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 **有效的** 括号组合。
>
>  **示例 1：**
>
> ```
>输入：n = 3
> 输出：["((()))","(()())","(())()","()(())","()()()"]
> ```
> 
> **示例 2：**
>
> ```
>输入：n = 1
> 输出：["()"]
> ```
> 
> **提示：**
>
>  - `1 <= n <= 8`

本质上，这道题目相当于从2*n个位置当中，选择n个位置放左括号，选择n个位置放右括号，如果`path.size()==2*n`则认为找到了一组正确的解。但左右括号是有一定的限制的，dfs中传入起始左括号和右括号的个数，有如下情况（类似“选或不选”）：

- 如果剩余左括号数>0，则可以放左括号
- 如果剩余右括号数>0，且剩余左括号少于剩余右括号（说明现在序列里已经有的左括号更多），则可以放右括号；否则不能放右括号（不能是`(()))`这种）

代码如下：
```c++
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> res;
        int m = n*2; //总的长度
        string path(m,0);
        auto dfs = [&](this auto&& dfs, int leftCount, int rightCount, int start)
        {
            if(start==m)
            {
                if(leftCount==0 && rightCount==0)
                    res.push_back(path);
                return;
            }
            //1.加入左括号
            if(leftCount>0)
            {
                path[start] = '(';
                dfs(leftCount-1, rightCount, start+1); //不用恢复现场,因为会被后面的情况覆盖掉
            }
            if(rightCount>0 && leftCount<rightCount)
            {
                path[start] = ')';
                dfs(leftCount, rightCount-1, start+1);
            }
        };
        dfs(n, n, 0);
        return res;
    }
};
```



# 五、排列型回溯

部分题目也可以用状压 DP 做。

## 1.[46. 全排列](https://leetcode.cn/problems/permutations/)

> 给定一个不含重复数字的数组 `nums` ，返回其 *所有可能的全排列* 。你可以 **按任意顺序** 返回答案。
>
>  **示例 1：**
>
> ```
>输入：nums = [1,2,3]
> 输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
> ```
> 

对于排列的题目，我们需要记录哪些数被使用，并记得在dfs之后恢复现场。本题代码如下：

```c++
class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<vector<int>> res;
        int n = nums.size();
        vector<int> path(n); 
        unordered_set<int> used_set; //使用过的数
        auto dfs = [&](this auto&& dfs, int start)
        {
            if(start==n)
            {
                res.push_back(path);
                return;
            }
            for(int i=0;i<nums.size();i++)
            {
                if(!used_set.contains(nums[i])) //没有被使用过,可以进行递归
                {
                    path[start] = nums[i];
                    used_set.insert(nums[i]);
                    dfs(start+1);
                    used_set.erase(nums[i]);
                }
            }
        };
        dfs(0);
        return res;
    }
};
```

其实也不一定要用unordered_set，对于本题而言开一个长度为n的visited数组也能够到达预期。



### （1）时间空间复杂度分析

![image-20250309135803287](Leetcode%E2%80%94%E2%80%94%E5%9B%9E%E6%BA%AF%E4%B8%93%E9%A2%98.assets/image-20250309135803287.png)



## 2.[51. N 皇后](https://leetcode.cn/problems/n-queens/)

>按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。
>
>**n 皇后问题** 研究的是如何将 `n` 个皇后放置在 `n×n` 的棋盘上，并且使皇后彼此之间不能相互攻击。
>
>给你一个整数 `n` ，返回所有不同的 **n 皇后问题** 的解决方案。
>
>每一种解法包含一个不同的 **n 皇后问题** 的棋子放置方案，该方案中 `'Q'` 和 `'.'` 分别代表了皇后和空位。
>
>**示例 1：**
>
><img src="assets/queens.jpg" alt="img" style="zoom:33%;" />
>
>```
>输入：n = 4
>输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
>解释：如上图所示，4 皇后问题存在两个不同的解法。
>```

- （1）可以用一个`col[n]`数组存储每一行对应选择的列，这样的话行本身就不用再额外判断了。
- （2）在dfs的参数中加一个start，表示当前回溯到了第几行，当start==n的时候，利用col数组复原当前棋盘的样子，加入到res当中；
- （3）判断不在同一行可以自动判断，不在同一列的话只要col[n]前面没有当前选择的列即可，重点是判断是否在斜对角线：



对于某一个皇后(r,c)来说，其两条对角线中的元素满足(假设这些元素是(R,C))：`abs(r-R)==abs(c-C)`，用这条就可以判断N皇后的位置是否斜对角线合法。（务必记住这个结论，现场推导很可能不靠谱）

总的代码如下：

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

