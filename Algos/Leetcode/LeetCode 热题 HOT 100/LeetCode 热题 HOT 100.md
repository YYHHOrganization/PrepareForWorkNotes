#  LeetCode 热题 HOT 100



## 二分 :red_circle:

### [300. 最长递增子序列 ](https://leetcode-cn.com/problems/longest-increasing-subsequence/)  记录在“大厂”那个笔记中 :red_circle:

难度中等

给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。

**子序列** 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的子序列。

**示例 1：**

```C++
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
```

**示例 2：**

```C++
输入：nums = [0,1,0,3,2,3]
输出：4
```

**示例 3：**

```C++
输入：nums = [7,7,7,7,7,7,7]
输出：1
```

 

**提示：**

- `1 <= nums.length <= 2500`
- `-104 <= nums[i] <= 104`

 

**进阶：**

- 你能将算法的时间复杂度降低到 `O(n log(n))` 吗?

（M如果是选出所有递增序列的话可以用回溯，查一下递增序列即可）



**解法总结**

维护tail数组  每次来一个数字就二分查找其存在这个tail数组的哪里，并存入



##### 解法1：动态规划法

[300. 最长递增子序列（动态规划 + 二分查找，清晰图解） - 最长递增子序列 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/zui-chang-shang-sheng-zi-xu-lie-dong-tai-gui-hua-2/)



![image-20220312160621680](assets/image-20220312160621680.png)

```C++
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> dp(nums.size(),1);
        int resmax=0;//
        for(int i=0;i<nums.size();i++)
        {
            for(int j=0;j<i;j++)
            {
                if(nums[j]<nums[i]) dp[i]=max(dp[i],dp[j]+1);
            }
            resmax=max(resmax,dp[i]);
        }
        // vector<int>::iterator it=dp.begin();
        // for(;it!=dp.end();it++)cout<<" "<<*it;
        // return dp[nums.size()-1];//不对 可能是中间的比较多 因为dp[i]代表的是以i为结尾的最长的 不一定是他 记住了吗 记住了!
        return resmax;
    }
};
```

##### 解法2：动态规划+二分查找

https://leetcode.cn/problems/longest-increasing-subsequence/solutions/24173/zui-chang-shang-sheng-zi-xu-lie-dong-tai-gui-hua-2/?envType=problem-list-v2&envId=2cktkvj

<img src="assets/6808e0f2ef1ba669aaf93252c3262b5442e0ab5689bec16ada3af29866e11e64-Picture8.png" alt="img" style="zoom:33%;" />

<img src="assets/c8f6a8543a627e2a2d07e1b6d8b3f142e0b8844fd639acb553a9654d564f4a8b-Picture9.png" alt="img" style="zoom:33%;" />

![image-20220312163453274](assets/image-20220312163453274.png)

![image-20220312163513503](assets/image-20220312163513503.png)

比如序列是78912345，前三个遍历完以后tail是789，这时候遍历到1，就得把1放到合适的位置，于是在tail二分查找1的位置，变成了189（如果序列在此时结束，因为res不变，所以依旧输出3），再遍历到2成为129，然后是123直到12345 这题难理解的核心不在于算法难，而在于在于官方给的例子太拉了，遇不到这个算法真正要解决的问题，即没有我例子中1要代替7的过程，

精妙之处就在于： 遍历nums拿出来的比我当前tail尾部更小的数，我遇见了就把它换进来，要是后续不能让这些稍小（相较于tail数组的尾部）的变成更长的子序列，那就超不过原先的，我也没有任何损失，但如果长度能超过之前的这些，我前面已经替换完了，随时准备着和你后面的组成更长的，只需要你来加到尾部就ok了。 更通俗点说，在一样长的最长子序列里面，我永远是所有元素最小的那个子序列，后面随便给我来一个元素，它可能跟我组成更长的，而不可能跟你组更长的，如果它跟我都不能组，跟你则更不可能组了，因为我最后一个元素比你小呀！



相当于 更新子序列了吧

（思路：构建tails 每次去更新就行了

25/05/03

```C++
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) 
    {
        int n = nums.size();
        vector<int> tail;
        //41078523
        //478  找到第一个  >=5的：7-> 458 
        for(int i=0;i<n;i++)
        {
            if(tail.empty()||nums[i]>tail.back())tail.push_back(nums[i]);
            else
            {
                //严格递增 所以>= 不能放两个
                //upper_bound寻找第一个>5的 但是如果是5555 那么 t：5 既不会进上面的push 下面的也会找超出
                //而题目需要严格递增 所以如果是一样的数字 应该覆盖 所以应该寻找tail中第一个>=5的 覆盖
                //int index = upper_bound(tail.begin(),tail.end(),nums[i])-tail.begin();
                int index = lower_bound(tail.begin(),tail.end(),nums[i])-tail.begin();
                tail[index] = nums[i];
            };
        }
        return tail.size();
    }
};
```

> **深入理解本题的贪心策略:**
>
> ### 分步解释与证明
>
> 要理解该贪心算法的正确性，需明确以下几点：
>
> ---
>
> #### **1. 维护数组 `res` 的性质**
> - **`res` 是递增序列**：每次插入或替换操作均保证 `res` 严格递增。
> - **`res[i]` 表示长度为 `i+1` 的递增子序列的最小可能末尾元素**  
>   例如，若当前 `res = [2, 5, 7]`，则：
>   - 长度为1的递增子序列最小末尾是2；
>   - 长度为2的最小末尾是5；
>   - 长度为3的最小末尾是7。
>
> ---
>
> #### **2. 关键操作的解释**
> - **当 `nums[i] > res.back()`**  
>   直接追加到 `res`，因为当前元素能扩展最长子序列。
>   
> - **当 `nums[i] ≤ res.back()`**  
>   用 `lower_bound` 找到第一个 `≥ nums[i]` 的位置 `j`，替换 `res[j]` 为 `nums[i]`。  
>   **目的**：更新长度为 `j+1` 的子序列的末尾为更小的值，以便未来可能形成更长的子序列。(这地方有一些贪心的意味)
>
> ---
>
> #### **3. 正确性证明（数学归纳法）**
> **归纳基础**：初始时 `res` 为空，显然长度为0时成立。
>
> **归纳假设**：假设处理前 `k` 个元素后，`res` 满足：
> - `res` 递增；
> - `res[i]` 是前 `k` 个元素中长度为 `i+1` 的递增子序列的最小末尾。
>
> **归纳步骤**：处理第 `k+1` 个元素 `x = nums[k]`。
>
> - **情况1：`x > res.back()`**  
>   追加 `x` 到 `res`，此时新长度 `L+1`。由于 `x` 可接在长度为 `L` 的子序列后，形成更长的子序列，且 `x` 是该长度的最小末尾（因为之前无法形成更长的子序列）。
>
> - **情况2：`x ≤ res.back()`**  
>   找到 `j` 使得 `res[j]` 是第一个 `≥ x` 的元素，替换 `res[j] = x`。  
>   **为何可行**：  
>   - 存在一个长度为 `j` 的子序列，其末尾 `< x`（由 `res` 的递增性保证），因此可将 `x` 接在其后，形成长度为 `j+1` 的子序列，且末尾更小（优化了原 `res[j]`）。
>
> **结论**：处理完所有元素后，`res` 的长度即为最长递增子序列的长度。
>
> ---
>
> #### **4. 示例分析**
> 以数组 `[3, 0, 1, 2, 6, 4, 5]` 为例：
>
> | 步骤 | 当前元素 | res 操作                 | res 数组     | 解释                     |
> | ---- | -------- | ------------------------ | ------------ | ------------------------ |
> | 1    | 3        | 直接追加                 | [3]          | 初始长度为1              |
> | 2    | 0        | 替换3 → 0                | [0]          | 0是更小的长度为1的末尾   |
> | 3    | 1        | 替换res[1]（越界，追加） | [0, 1]       | 1 > 0，扩展长度为2       |
> | 4    | 2        | 替换1 → 2                | [0, 2]       | 替换后长度为2的末尾更小  |
> | 5    | 6        | 直接追加                 | [0, 2, 6]    | 6 > 2，扩展长度为3       |
> | 6    | 4        | 替换6 → 4                | [0, 2, 4]    | 4 < 6，优化长度为3的末尾 |
> | 7    | 5        | 替换res[3]（越界，追加） | [0, 2, 4, 5] | 5 > 4，扩展长度为4       |
>
> 最终 `res` 长度为4，对应最长递增子序列 `[0,1,2,5]` 或 `[0,2,4,5]`。
>
> ---
>
> #### **5. 算法优势**
> - **时间复杂度**：O(n log n)，优于动态规划的 O(n²)。
> - **空间复杂度**：O(n)，仅需维护数组 `res`。
>
> ---
>
> ### **总结**
> 该算法通过维护不同长度递增子序列的最小末尾元素，确保后续元素能高效地扩展更长序列。虽然 `res` 并非真实的最长子序列，但其长度正确反映了最长递增子序列的长度。贪心策略的核心在于通过替换优化末尾元素，为未来扩展保留最大可能性。



## 二叉树 :red_circle:


### [剑指 Offer 68 - II. 二叉树的最近公共祖先](https://leetcode-cn.com/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/)   记录在“大厂”那个笔记中 :red_circle:

难度简单393收藏分享切换为英文接收动态反馈

给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

[百度百科](https://baike.baidu.com/item/最近公共祖先/8918834?fr=aladdin)中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（**一个节点也可以是它自己的祖先**）。”

例如，给定如下二叉树: root = [3,5,1,6,2,0,8,null,null,7,4]

![img](assets/binarytree.png)

 

**示例 1:**

```
输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出: 3
解释: 节点 5 和节点 1 的最近公共祖先是节点 3。
```

**示例 2:**

```
输入: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出: 5
解释: 节点 5 和节点 4 的最近公共祖先是节点 5。因为根据定义最近公共祖先节点可以为节点本身。
```

 ```C++
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if(root==NULL)return NULL;
        if(root==p||root==q)return root;
        TreeNode* left=lowestCommonAncestor(root->left,p,q); 
        TreeNode* right=lowestCommonAncestor(root->right,p,q); 
        if(left==NULL)return right;
        else if(right==NULL)return left;
        else return root;

    }
};
 ```



解析版：

```C++
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if(root == null) return null; // 如果树为空，直接返回null
        if(root == p || root == q) return root; // 如果 p和q中有等于 root的，那么它们的最近公共祖先即为root（一个节点也可以是它自己的祖先）
        TreeNode left = lowestCommonAncestor(root.left, p, q); // 递归遍历左子树，只要在左子树中找到了p或q，则先找到谁就返回谁
        TreeNode right = lowestCommonAncestor(root.right, p, q); // 递归遍历右子树，只要在右子树中找到了p或q，则先找到谁就返回谁
        if(left == null) return right; // 如果在左子树中 p和 q都找不到，则 p和 q一定都在右子树中，右子树中先遍历到的那个就是最近公共祖先（一个节点也可以是它自己的祖先）
        else if(right == null) return left; // 否则，如果 left不为空，在左子树中有找到节点（p或q），这时候要再判断一下右子树中的情况，如果在右子树中，p和q都找不到，则 p和q一定都在左子树中，左子树中先遍历到的那个就是最近公共祖先（一个节点也可以是它自己的祖先）
        else return root; //否则，当 left和 right均不为空时，说明 p、q节点分别在 root异侧, 最近公共祖先即为 root
    }
}
```

