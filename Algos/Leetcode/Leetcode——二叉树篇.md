# Leetcode——二叉树篇

# 一、视频中的热门题目

## 1.[104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)

> 重点在于能够想到将原问题变为左右子树可以解决的子问题，先“递”，在计算到正确答案或者是触发边界的时候再“归”，回到根节点即可计算出正确的答案。

### （1）方法1：左右深度最大值+1

```c++
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if(root==nullptr) return 0;
        return max(maxDepth(root->left), maxDepth(root->right))+1;
    }
};
```



### （2）方法2：递归时深度+1，记录最大深度

```c++
class Solution {
public:
    int res = 0;
    void dfs(TreeNode* root, int cnt)
    {
        if(root==nullptr) return;
        cnt+=1;
        res = max(res, cnt);
        dfs(root->left, cnt);
        dfs(root->right, cnt);
    }
    int maxDepth(TreeNode* root) {
        dfs(root, 0);
        return res;
    }
};
```



## 2.对应作业题

### （1）[112. 路径总和](https://leetcode.cn/problems/path-sum/)

> 给你二叉树的根节点 `root` 和一个表示目标和的整数 `targetSum` 。判断该树中是否存在 **根节点到叶子节点** 的路径，这条路径上所有节点值相加等于目标和 `targetSum` 。如果存在，返回 `true` ；否则，返回 `false` 。
>
> **叶子节点** 是指没有子节点的节点。

这道题不要理解错误，是到了叶子节点才会去算，而不是中间就算。

```c++
class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) {
        if(root==nullptr) return false;
        int target = targetSum - root->val;
        if(root->left==nullptr && root->right==nullptr) //叶子节点
        {
            return target == 0;
        }
        return hasPathSum(root->left, target) || hasPathSum(root->right, target);
    }
};
```



### （2）[129. 求根节点到叶节点数字之和](https://leetcode.cn/problems/sum-root-to-leaf-numbers/)

> 给你一个二叉树的根节点 `root` ，树中每个节点都存放有一个 `0` 到 `9` 之间的数字。
>
> 每条从根节点到叶节点的路径都代表一个数字：
>
> - 例如，从根节点到叶节点的路径 `1 -> 2 -> 3` 表示数字 `123` 。
>
> 计算从根节点到叶节点生成的 **所有数字之和** 。
>
> **叶节点** 是指没有子节点的节点。

```c++
class Solution {
public:
    int dfs(TreeNode* root, int curSum)
    {
        if(root==nullptr) return 0;
        int x = curSum * 10 + root->val; //截止到当前分支目前节点的总和
        if(root->left==nullptr && root->right==nullptr) //叶子节点
        {
            return x;
        }
        return dfs(root->left, x) + dfs(root->right, x); //还没到叶子节点或者遍历到空,继续往下遍历
    }
    int sumNumbers(TreeNode* root) {
        //=从当前开始左分支的总和+右分支的总和
        return dfs(root, 0);
    }
};
```

