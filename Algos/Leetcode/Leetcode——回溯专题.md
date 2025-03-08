# Leetcode——回溯专题

对应[分享丨【题单】链表、二叉树与回溯（前后指针/快慢指针/DFS/BFS/直径/LCA/一般树）- 讨论 - 力扣（LeetCode）](https://leetcode.cn/discuss/post/3142882/fen-xiang-gun-ti-dan-lian-biao-er-cha-sh-6srp/)这里的第四大专题：回溯。

# 一、入门回溯

## 1.[17. 电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/)

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
>  
>
> **示例 1：**
>
> ```
> 输入：nums = [1,2,3]
> 输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
> ```
>
> **示例 2：**
>
> ```
> 输入：nums = [0]
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
>  
>
> **示例 1：**
>
> ```
> 输入：s = "aab"
> 输出：[["a","a","b"],["aa","b"]]
> ```
>
> **示例 2：**
>
> ```
> 输入：s = "a"
> 输出：[["a"]]
> ```
>
>  
>
> **提示：**
>
> - `1 <= s.length <= 16`
> - `s` 仅由小写英文字母组成



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
            if(isalpha(s[i]))
            {
                path[i] = tolower(s[i]);
                dfs(i+1);
                path[i] = toupper(s[i]);
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



## 4.[LCP 51. 烹饪料理](https://leetcode.cn/problems/UEcfPD/)

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
            dfs(i+1, value,curY);
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



## 6.[1239. 串联字符串的最大长度](https://leetcode.cn/problems/maximum-length-of-a-concatenated-string-with-unique-characters/)

> 给定一个字符串数组 `arr`，字符串 `s` 是将 `arr` 的含有 **不同字母** 的 **子序列** 字符串 **连接** 所得的字符串。
>
> 请返回所有可行解 `s` 中最长长度。
>
> **子序列** 是一种可以从另一个数组派生而来的数组，通过删除某些元素或不删除元素而不改变其余元素的顺序。
>
>  
>
> **示例 1：**
>
> ```
> 输入：arr = ["un","iq","ue"]
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
> 输入：arr = ["cha","r","act","ers"]
> 输出：6
> 解释：可能的解答有 "chaers" 和 "acters"。
> ```
>
> **示例 3：**
>
> ```
> 输入：arr = ["abcdefghijklmnopqrstuvwxyz"]
> 输出：26
> ```
>
>  
>
> **提示：**
>
> - `1 <= arr.length <= 16`
> - `1 <= arr[i].length <= 26`
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



## 7.（特殊，可以重复选）[39. 组合总和](https://leetcode.cn/problems/combination-sum/)

> 给你一个 **无重复元素** 的整数数组 `candidates` 和一个目标整数 `target` ，找出 `candidates` 中可以使数字和为目标数 `target` 的 所有 **不同组合** ，并以列表形式返回。你可以按 **任意顺序** 返回这些组合。
>
> `candidates` 中的 **同一个** 数字可以 **无限制重复被选取** 。如果至少一个数字的被选数量不同，则两种组合是不同的。 
>
> 对于给定的输入，保证和为 `target` 的不同组合数少于 `150` 个。
>
>  
>
> **示例 1：**
>
> ```
> 输入：candidates = [2,3,6,7], target = 7
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
> 输入: candidates = [2,3,5], target = 8
> 输出: [[2,2,2,2],[2,3,3],[3,5]]
> ```
>
> **示例 3：**
>
> ```
> 输入: candidates = [2], target = 1
> 输出: []
> ```
>
>  
>
> **提示：**
>
> - `1 <= candidates.length <= 30`
> - `2 <= candidates[i] <= 40`
> - `candidates` 的所有元素 **互不相同**
> - `1 <= target <= 40`

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



# 三、划分型回溯

把分割线（逗号）看成是可以「选或不选」的东西，本质在一定程度上是子集型回溯。前面的题目「分割回文串」即可以理解为划分型回溯的题目。这部分整理一下其他题：

## 1.[2698. 求一个整数的惩罚数](https://leetcode.cn/problems/find-the-punishment-number-of-an-integer/)（看题解）

> 给你一个正整数 `n` ，请你返回 `n` 的 **惩罚数** 。
>
> `n` 的 **惩罚数** 定义为所有满足以下条件 `i` 的数的平方和：
>
> - `1 <= i <= n`
> - `i * i` 的十进制表示的字符串可以分割成若干连续子字符串，且这些子字符串对应的整数值之和等于 `i` 。

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



## 2.[1593. 拆分字符串使唯一子字符串的数目最大](https://leetcode.cn/problems/split-a-string-into-the-max-number-of-unique-substrings/)

> 给你一个字符串 `s` ，请你拆分该字符串，并返回拆分后唯一子字符串的最大数目。
>
> 字符串 `s` 拆分后可以得到若干 **非空子字符串** ，这些子字符串连接后应当能够还原为原字符串。但是拆分出来的每个子字符串都必须是 **唯一的** 。
>
> 注意：**子字符串** 是字符串中的一个连续字符序列。
>
>  
>
> **示例 1：**
>
> ```
> 输入：s = "ababccc"
> 输出：5
> 解释：一种最大拆分方法为 ['a', 'b', 'ab', 'c', 'cc'] 。像 ['a', 'b', 'a', 'b', 'c', 'cc'] 这样拆分不满足题目要求，因为其中的 'a' 和 'b' 都出现了不止一次。
> ```
>
> **示例 2：**
>
> ```
> 输入：s = "aba"
> 输出：2
> 解释：一种最大拆分方法为 ['a', 'ba'] 。
> ```
>
> **示例 3：**
>
> ```
> 输入：s = "aa"
> 输出：1
> 解释：无法进一步拆分字符串。
> ```
>
>  
>
> **提示：**
>
> - `1 <= s.length <= 16`
> - `s` 仅包含小写英文字母

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
                    dfs(i+1); //枚举下一位
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

```c++
```







# 四、组合型回溯