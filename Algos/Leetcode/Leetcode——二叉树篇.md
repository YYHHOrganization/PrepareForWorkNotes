# Leetcode——二叉树篇

> 本系列Leetcode总结篇基本参考[分享丨【算法题单】链表、二叉树与回溯（前后指针/快慢指针/DFS/BFS/直径/LCA/一般树）- 讨论 - 力扣（LeetCode）](https://leetcode.cn/discuss/post/3142882/fen-xiang-gun-ti-dan-lian-biao-er-cha-sh-6srp/),仅用作个人准备秋招总结,无商用的情况。

![DFS BFS](assets/1724824379-UOsXIV-dfsbfsnew-c.png)

**学习递归，从二叉树开始。**

带着问题去做下面的题目：

- 一般来说，DFS 的递归边界是空节点。在什么情况下，要额外把叶子节点作为递归边界？
- 在什么情况下，DFS 需要有返回值？什么情况下不需要有返回值？
- 在什么情况下，题目更适合用自顶向下的方法解决？什么情况下更适合用自底向上的方法解决？

## 1.遍历二叉树

### （1）[872. 叶子相似的树](https://leetcode.cn/problems/leaf-similar-trees/)

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    void dfs(TreeNode* root, vector<int>& leafs)
    {
        if(root==nullptr) return;
        if(root->left==root->right) //叶子结点
        {
            leafs.push_back(root->val);
            return;
        }
        dfs(root->left, leafs);
        dfs(root->right, leafs);
    }
    bool leafSimilar(TreeNode* root1, TreeNode* root2) {
        //前序遍历两棵树，叶子节点记录下来，然后比较是否一样
        vector<int> leaf1;
        vector<int> leaf2;
        dfs(root1, leaf1);
        dfs(root2, leaf2);
        return leaf1==leaf2;
    }
};
```



### （2）[LCP 44. 开幕式焰火](https://leetcode.cn/problems/sZ59z6/)

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    vector<int> vals;
    void dfs(TreeNode* root)
    {
        if(root==NULL) return;
        vals[root->val] += 1; //前序遍历
        dfs(root->left);
        dfs(root->right);
    }
    int numColor(TreeNode* root) {
        //前序遍历，记录有多少个不同的值即可
        vals.resize(1001);
        dfs(root);
        int ans = 0;
        for(int val: vals)
        {
            if(val!=0) ans++;
        }
        return ans;
    }
};
```

或者用`unordered_set<int> s;`



### （3）[404. 左叶子之和](https://leetcode.cn/problems/sum-of-left-leaves/)（==可以复习==）

> 给定二叉树的根节点 `root` ，返回所有左叶子之和。

本题直接判断是否是左叶子比较麻烦，简单起见可以在if语句中判断当前结点的左节点是否是叶子结点，是的话就累加sum到最终结果当中。代码如下：
```c++
class Solution {
public:
    int sum = 0;
    void dfs(TreeNode* root) 
    {
        if(root==nullptr) return;
        //判断当前结点是否有左孩子，且左孩子是否为叶子节点
        //依旧是前序遍历顺序：根，左，右
        if(root->left && root->left->left==nullptr && root->left->right==nullptr)
        {
            sum += root->left->val; 
        }
        dfs(root->left);
        dfs(root->right);
    }
    int sumOfLeftLeaves(TreeNode* root) {
        dfs(root);
        return sum;
    }
};
```



### （4）[671. 二叉树中第二小的节点](https://leetcode.cn/problems/second-minimum-node-in-a-binary-tree/)

> 给定一个非空特殊的二叉树，每个节点都是正数，并且每个节点的子节点数量只能为 `2` 或 `0`。如果一个节点有两个子节点的话，那么该节点的值等于两个子节点中较小的一个。
>
> 更正式地说，即 `root.val = min(root.left.val, root.right.val)` 总成立。
>
> 给出这样的一个二叉树，你需要输出所有节点中的 **第二小的值** 。
>
> 如果第二小的值不存在的话，输出 -1 **。**

#### （a）我的做法

两次DFS，时间复杂度会高一些，代码如下：
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    unordered_set<int> uset;
    int update(TreeNode* root) //更新二叉树所有节点的值
    {
        if(root==nullptr) return 0;
        if(root->left==root->right) return root->val;
        int v = min(update(root->left), update(root->right));
        root->val = v;
        return v;
    }
    void dfs(TreeNode* root)
    {
        if(root==nullptr) return;
        //根，左，右
        uset.insert(root->val);
        dfs(root->left);
        dfs(root->right);
    }
    int findSecondMinimumValue(TreeNode* root) {
        update(root);
        dfs(root);
        vector<int> res(uset.begin(), uset.end());
        if((int)res.size()<2) return -1;
        nth_element(res.begin(), res.begin()+1, res.end());
        return res[1];
    }
};
```



#### （a.y）记录 最小值 和 次小值

```C++
class Solution {
public:
    long long min1=(long long)INT_MAX+1,min2 = (long long)INT_MAX+1;
    void dfs(TreeNode* root)
    {
        if(root==nullptr)return ;
        int v = root->val;
        if(v<min1)
        {
            min2 = min1;
            min1 = v;
        }
        else if(v!=min1&&v<min2) min2 = v;
        dfs(root->left); 
        dfs(root->right);
    }
    int findSecondMinimumValue(TreeNode* root) {
         min1=(long long)INT_MAX+1,min2 = (long long)INT_MAX+1;
        dfs(root);
        return min2>INT_MAX?-1:min2;
    }
};
```



#### （b）简单一些的做法

经过题意的理解，对于二叉树中的任意节点 *x*，*x* 的值不大于以 *x* 为根的子树中所有节点的值。同理，根节点应该是整棵树最小的值。因此，问题转换为了求解严格比根节点值大的最小的值。

代码如下：
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    long long mn = (long long)INT_MAX + 5;
    long long ans = (long long)INT_MAX + 5; //结果,注意本题的数据范围
    void dfs(TreeNode* root)
    {
        if(root==nullptr) return;
        long long x = root->val;
        if(x>mn && x<ans) //更新ans的值
        {
            ans = x;
        }
        dfs(root->left);
        dfs(root->right);
    }
    int findSecondMinimumValue(TreeNode* root) {
        //结点数量>=1，一定有根
        mn = (long long)root->val;
        dfs(root);
        if(ans==(long long)INT_MAX+5) return -1;
        return ans;
    }
};
```



## 2.自顶向下DFS

在「递」的过程中维护值。

> 有些题目自顶向下和自底向上都可以做。有些题目也可以用 BFS 做。

### （1）[111. 二叉树的最小深度](https://leetcode.cn/problems/minimum-depth-of-binary-tree/)

> 给定一个二叉树，找出其最小深度。
>
> 最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
>
> **说明：**叶子节点是指没有子节点的节点。

注意这道题目和“二叉树的最大深度”之间的差别：
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int dfs(TreeNode* root)
    {
        if(root==nullptr) return 0;
        //注意本题和最大深度的差别:有可能只有左孩子或者右孩子,此时直接取min会得到0,但实际上应该是仅有的那边孩子的深度+1
        if(root->left && !root->right) return dfs(root->left)+1;
        else if(root->right && !root->left) return dfs(root->right)+1;
        //有两个子节点或者没有子节点,都可以走下面这个逻辑
        return min(dfs(root->left), dfs(root->right))+1;
    }
    int minDepth(TreeNode* root) {
        int res = dfs(root);
        return res;
    }
};
```



### （2）[1457. 二叉树中的伪回文路径](https://leetcode.cn/problems/pseudo-palindromic-paths-in-a-binary-tree/)

> 给你一棵二叉树，每个节点的值为 1 到 9 。我们称二叉树中的一条路径是 「**伪回文**」的，当它满足：路径经过的所有节点值的排列中，存在一个回文序列。
>
> 请你返回从根到叶子节点的所有路径中 **伪回文** 路径的数目。

要点在于理解“伪回文路径”的特点：1~9的数字里，最多有一个数是奇数个。由于结点的值范围是1到9，因此可以使用二进制来压缩。代码如下：
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int cnt = 0;
    void dfs(TreeNode* root, int base) //base做二进制压缩
    {
        if(root==nullptr) return; //判断逻辑不能写在这里,不然左右孩子都为空会进两次
        int x = root->val;
        base ^= (1<<x);
        if(root->left==nullptr && root->right==nullptr)
        {
            if((base & (base - 1)) == 0) //1~9每个数最多不超过一个(二进制压缩)，表示最多只有一个1
            {
                cnt++;
            }
            return;
        }
        dfs(root->left, base);
        dfs(root->right, base);
        //不需要在dfs之后把base的值改回去，因为是值传递的
    }
    int pseudoPalindromicPaths (TreeNode* root) {
        dfs(root, 0);
        return cnt;
    }
};
```



### （3）[1315. 祖父节点值为偶数的节点和](https://leetcode.cn/problems/sum-of-nodes-with-even-valued-grandparent/)

> 给你一棵二叉树，请你返回满足以下条件的所有节点的值之和：
>
> - 该节点的祖父节点的值为偶数。（一个节点的祖父节点是指该节点的父节点的父节点。）
>
> 如果不存在祖父节点值为偶数的节点，那么返回 `0` 。

```c++
class Solution {
public:
    int ans = 0;
    void dfs(TreeNode* root, TreeNode* father, TreeNode* grandfather)
    {
        if(root==nullptr) return;
        if(grandfather!=nullptr && (grandfather->val%2==0))
        {
            ans += root->val;
        }
        dfs(root->left, root, father);
        dfs(root->right, root, father);
    }
    int sumEvenGrandparent(TreeNode* root) {
        dfs(root, nullptr, nullptr);
        return ans;
    }
};
```



### （4）[988. 从叶结点开始的最小字符串](https://leetcode.cn/problems/smallest-string-starting-from-leaf/)

> 给定一颗根结点为 `root` 的二叉树，树中的每一个结点都有一个 `[0, 25]` 范围内的值，分别代表字母 `'a'` 到 `'z'`。
>
> 返回 ***按字典序最小** 的字符串，该字符串从这棵树的一个叶结点开始，到根结点结束*。
>
> > 注**：**字符串中任何较短的前缀在 **字典序上** 都是 **较小** 的：
> >
> > - 例如，在字典序上 `"ab"` 比 `"aba"` 要小。叶结点是指没有子结点的结点。 
>
> 节点的叶节点是没有子节点的节点。

没什么特别好的优化方法，暴力出奇迹：
```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<string> vec;
    void dfs(TreeNode* root, string res)
    {
        if(root==nullptr) return;
        res += ('a'+root->val);
        if(root->left==root->right)
        {
            string t = res;
            reverse(t.begin(), t.end());
            vec.push_back(t);
        } 
        dfs(root->left, res);
        dfs(root->right, res);
    }
    string smallestFromLeaf(TreeNode* root) {
        //找字典序最小并不意味着找逆序字典序最大, 反例:421<431 124<134
        //暴力做法:找到所有的,反转并排序
        dfs(root, "");
        string ans = *min_element(vec.begin(), vec.end());
        return ans;
    }
};
```



### （5）[1022. 从根到叶的二进制数之和](https://leetcode.cn/problems/sum-of-root-to-leaf-binary-numbers/)

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int ans = 0;
    void dfs(TreeNode* root, int sum)
    {
        if(root==nullptr) return;
        sum = sum * 2 + root->val;
        if(root->left==root->right) 
        {
            ans += sum;
        }
        dfs(root->left, sum);
        dfs(root->right, sum);
    }
    int sumRootToLeaf(TreeNode* root) {
        dfs(root, 0);
        return ans;
    }
};
```



### （6）[623. 在二叉树中增加一行](https://leetcode.cn/problems/add-one-row-to-tree/)

> 给定一个二叉树的根 `root` 和两个整数 `val` 和 `depth` ，在给定的深度 `depth` 处添加一个值为 `val` 的节点行。
>
> 注意，根节点 `root` 位于深度 `1` 。
>
> 加法规则如下:
>
> - 给定整数 `depth`，对于深度为 `depth - 1` 的每个非空树节点 `cur` ，创建两个值为 `val` 的树节点作为 `cur` 的左子树根和右子树根。
> - `cur` 原来的左子树应该是新的左子树根的左子树。
> - `cur` 原来的右子树应该是新的右子树根的右子树。
> - 如果 `depth == 1 `意味着 `depth - 1` 根本没有深度，那么创建一个树节点，值 `val `作为整个原始树的新根，而原始树就是新根的左子树。
> - **示例 1:**
>
>   <img src="assets/addrow-tree.jpg" alt="img" style="zoom:67%;" />
>
>   ```
>   输入: root = [4,2,6,3,1,5], val = 1, depth = 2
>   输出: [4,1,1,2,null,null,6,3,1,5]
>   ```

我写的代码：
```c++
class Solution {
public:
    TreeNode* dfs(TreeNode* root, int val, int depth) //返回值为root
    {
        //1 <= depth <= the depth of tree + 1,对于树的深度来说,1表示根节点
        if(root==nullptr) return nullptr;
        TreeNode* left = root->left;
        TreeNode* right = root->right;
        depth--;
        if(depth==0)
        {
            TreeNode* newRoot = new TreeNode(val);
            newRoot->left = root;
            return newRoot; //需要注意如果不显式地返回新的root的话，root更改指向是带不出去的，因为指针是复制传递的，没有用引用
        }
        else if(depth==1)
        {
            TreeNode* l = new TreeNode(val);
            TreeNode* r = new TreeNode(val);
            root->left = l;
            root->right = r;
            l->left = left;
            r->right = right; //这些其实可以用Leetcode为本题提供的代码中的构造函数简化一下，这里就不写了
            return root;
        }
        dfs(root->left, val, depth);
        dfs(root->right, val, depth);
        return root;
    }
    TreeNode* addOneRow(TreeNode* root, int val, int depth) {
        TreeNode* newRoot = dfs(root, val, depth);
        return newRoot;
    }
};
```

> 本题也可以用二叉树的层序遍历来做。

层序遍历：

```C++
class Solution {
public:
    TreeNode* addOneRow(TreeNode* root, int val, int depth) {
        int curDepth = 0;
        //用层序
        queue<TreeNode* > que;
        que.emplace(root);
        if(depth==1)
        {
            TreeNode* newNode = new TreeNode(val);
            newNode->left = root;
            return newNode;
        }
        while(!que.empty())
        {
            curDepth++;
            int sz = que.size();
            for(int i=0;i<sz;i++)
            {
                TreeNode *node = que.front();
                // cout<<"curnode"<<node->val<<endl;
                que.pop();
                TreeNode* left = node->left;  
                TreeNode* right = node->right;
                if(curDepth == depth-1)
                {
                    TreeNode* newl = new TreeNode(val);
                    newl->left = left;
                    TreeNode* newr = new TreeNode(val);
                    newr->right = right;
                    node->left = newl; 
                    node->right =newr;
                }
                if(left) que.push(left);
                if(right)que.push(right);
            }
        }
        return root;
    }
};
```





### ==（7）[1372. 二叉树中的最长交错路径](https://leetcode.cn/problems/longest-zigzag-path-in-a-binary-tree/)（值得复习一下）==

> 给你一棵以 `root` 为根的二叉树，二叉树中的交错路径定义如下：
>
> - 选择二叉树中 **任意** 节点和一个方向（左或者右）。
> - 如果前进方向为右，那么移动到当前节点的的右子节点，否则移动到它的左子节点。
> - 改变前进方向：左变右或者右变左。
> - 重复第二步和第三步，直到你在树中无法继续移动。
>
> 交错路径的长度定义为：**访问过的节点数目 - 1**（单个节点的路径长度为 0 ）。
>
> 请你返回给定树中最长 **交错路径** 的长度。

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int ans = 0;
    int dfs(TreeNode* root, bool turnLeft) //turnLeft表示是否往左走
    {
        if(root==nullptr) return 0;
        //看一下从当前点直接出发,往左走和往右走的结果
        int left = dfs(root->left, false);
        int right = dfs(root->right, true);
        ans = max(ans, max(left, right)); //单个节点的路径长度为0,这里不用+1
        //根据当前步的指示决定采用哪个值作为递归的返回值
        int len = 0;
        if(turnLeft) len = left + 1;
        else len = right + 1; //相当于后序遍历：左，右，根，结果要返回上去了，此时要+1（说明多了一层）
        return len;
    }
    int longestZigZag(TreeNode* root) {
        dfs(root, true);
        dfs(root, false);
        return ans;
    }
};
```

> 其他做法也值得学习一下，可以参考力扣的官方题解（还没看完）。



### ==（8）[971. 翻转二叉树以匹配先序遍历](https://leetcode.cn/problems/flip-binary-tree-to-match-preorder-traversal/)（还没做）==

> 给你一棵二叉树的根节点 `root` ，树中有 `n` 个节点，每个节点都有一个不同于其他节点且处于 `1` 到 `n` 之间的值。
>
> 另给你一个由 `n` 个值组成的行程序列 `voyage` ，表示 **预期** 的二叉树 [**先序遍历**](https://baike.baidu.com/item/先序遍历/6442839?fr=aladdin) 结果。
>
> 通过交换节点的左右子树，可以 **翻转** 该二叉树中的任意节点。例，翻转节点 1 的效果如下：
>
> ![img](assets/fliptree.jpg)
>
> 请翻转 **最少** 的树中节点，使二叉树的 **先序遍历** 与预期的遍历行程 `voyage` **相匹配** 。 
>
> 如果可以，则返回 **翻转的** 所有节点的值的列表。你可以按任何顺序返回答案。如果不能，则返回列表 `[-1]`。





## 3.自底向上DFS

### （1）[1379. 找出克隆二叉树中的相同节点](https://leetcode.cn/problems/find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree/)

```c++
class Solution {
public:
    TreeNode* dfs(TreeNode* p, TreeNode* q, TreeNode* target) //本题保证target不会是nullptr
    {
        if(p==NULL || q==NULL) return NULL;
        if(p==target)
        {
            return q;
        }
        TreeNode* left = dfs(p->left, q->left, target);
        TreeNode* right = dfs(p->right, q->right, target);
        if(!left) return right;
        else return left; //非NULL的结果应该就是要求的
    }
    TreeNode* getTargetCopy(TreeNode* original, TreeNode* cloned, TreeNode* target) {
        return dfs(original, cloned, target);
    }
};
```



### （2）[563. 二叉树的坡度](https://leetcode.cn/problems/binary-tree-tilt/)

> 给你一个二叉树的根节点 `root` ，计算并返回 **整个树** 的坡度 。
>
> 一个树的 **节点的坡度** 定义即为，该节点左子树的节点之和和右子树节点之和的 **差的绝对值** 。如果没有左子树的话，左子树的节点之和为 0 ；没有右子树的话也是一样。空结点的坡度是 0 。
>
> **整个树** 的坡度就是其所有节点的坡度之和。

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int ans = 0;
    int dfs(TreeNode* root) //返回值为以当前节点为根节点的子树和
    {
        if(root==nullptr) return 0;
        int left = dfs(root->left); //左子树之和
        int right = dfs(root->right); //右子树之和
        ans += abs(left - right);
        return left + right + root->val;
    }
    int findTilt(TreeNode* root) {
        dfs(root);
        return ans;
    }
};
```



### （3）[606. 根据二叉树创建字符串](https://leetcode.cn/problems/construct-string-from-binary-tree/)

> 给你二叉树的根节点 `root` ，请你采用前序遍历的方式，将二叉树转化为一个由括号和整数组成的字符串，返回构造出的字符串。
>
> 空节点使用一对空括号对 `"()"` 表示，转化后需要省略所有不影响字符串与原始二叉树之间的一对一映射关系的空括号对。

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    string tree2str(TreeNode* root) {
        //算是一道DFS的模拟题,正常前序遍历
        //如果是nullptr,返回""
        //如果是叶子节点(没有左右孩子),则直接返回to_string(root->val);
        //否则如果有左孩子没有右孩子,则返回v(dfs(v->left))
        //如果没有左孩子,有右孩子,则返回v()(dfs(v->right))
        //否则,左右孩子都有,返回v(dfs(v->left))(dfs(v->right))
        //其实情况可以有一定的合并，这里为了方便理解直接都写了。
        if(root==nullptr) return "";
        if(root->left==root->right) return to_string(root->val);//即if(!root->left&&!root->right)
        if(root->left && !root->right)
        {
            return to_string(root->val) + "(" + tree2str(root->left) + ")";
        }
        if(!root->left && root->right)
        {
            return to_string(root->val) + "()(" + tree2str(root->right) + ")";
        }
        if(root->left && root->right)
        {
            return to_string(root->val) + "(" + tree2str(root->left) + ")(" + tree2str(root->right) + ")";
        }
        return "";
    }
};
```



### （4）[2265. 统计值等于子树平均值的节点数](https://leetcode.cn/problems/count-nodes-equal-to-average-of-subtree/)

> 给你一棵二叉树的根节点 `root` ，找出并返回满足要求的节点数，要求节点的值等于其 **子树** 中值的 **平均值** 。
>
> **注意：**
>
> - `n` 个元素的平均值可以由 `n` 个元素 **求和** 然后再除以 `n` ，并 **向下舍入** 到最近的整数。
> - `root` 的 **子树** 由 `root` 和它的所有后代组成。





# 一、视频中的热门题目

对应视频:[如何灵活运用递归？【基础算法精讲 10】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV18M411z7bb/?vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99&spm_id_from=333.788.videopod.sections)

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

### 时间空间复杂度分析

本题时空复杂度都是O(n)。

- 时间复杂度：每个节点都会入栈一次，出栈一次，所以是O(n)；
- 空间复杂度：O(n)，最差的情况退化为类似于链表，此时空间复杂度O(n)；

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

Y

```C++
class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) 
    {
        if(root==nullptr)return false;
        if(!root->left&&!root->right)
        {
            if(targetSum-root->val==0)return true;
            return false;
        }
        return hasPathSum(root->left,targetSum-root->val)||hasPathSum(root->right,targetSum-root->val);
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

Y

```C++
class Solution {
public:
    
    int sumNumbers(TreeNode* root) {
        // int path=0;
        int res=0;
        auto dfs = [&](this auto &&dfs,TreeNode* root,int path)
        {
            if(root==nullptr)return;
            path=path*10+root->val;
            if(!root->left&&!root->right)
            {
                res+=path;
                return;
            }
            dfs(root->left,path);
            dfs(root->right,path);
        };
        dfs(root,0);
        return res;
    }
};
```



### (3)[1448. 统计二叉树中好节点的数目](https://leetcode.cn/problems/count-good-nodes-in-binary-tree/)

> 给你一棵根为 `root` 的二叉树，请你返回二叉树中好节点的数目。
>
> 「好节点」X 定义为：从根到该节点 X 所经过的节点中，没有任何节点的值大于 X 的值。

要点还是想好各种情况，把问题分解好，然后可以写逻辑了。

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int dfs(TreeNode* root, int cnt, int maxValue)
    {
        //注意想好递归拆解问题的逻辑,就可以写代码了,将问题拆解为左子树中好节点的数目+右子树中好节点的数目+根是否为好节点?
        //1.递归结束条件:
        if(root==nullptr) return 0;
        int flag = 0;
        if(maxValue<=root->val) //没有任何节点的值大于 X 的值,意味着X是最大值,也就是其他节点中的最大值也要<=X
        {
            maxValue = root->val; //最大值更新
            flag = 1; //当前根节点本身也是好节点
        }
        cnt+=(flag + dfs(root->left, cnt, maxValue) + dfs(root->right, cnt, maxValue));
        return cnt;
    }
    int goodNodes(TreeNode* root) {
        int res = dfs(root, 0, INT_MIN); //一开始设置为INT_MIN,是因为根节点一定是好节点
        return res;
    }
};
```
Y
```C++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int goodNodes(TreeNode* root) 
    {
        int maxNum=INT_MIN;
        int num=0;
        auto dfs = [&](this auto&& dfs,TreeNode* root, int maxNum)
        {
            if(root==nullptr)return;
            if(root->val>=maxNum)
            {
                num++;
                maxNum = root->val;
            }
            dfs(root->left,maxNum);
            dfs(root->right,maxNum);
        };
        dfs(root,maxNum);
        return num;
    }
};
```


## 3.二叉树相同、对称、平衡等

### （1）[100. 相同的树](https://leetcode.cn/problems/same-tree/)

> 给你两棵二叉树的根节点 `p` 和 `q` ，编写一个函数来检验这两棵树是否相同。
>
> 如果两个树在结构上相同，并且节点具有相同的值，则认为它们是相同的。

递归思路：需要根节点相同，且左右子树都是相同的树。

```c++
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        //左或右可能为空
        if(p==nullptr || q==nullptr)
        {
            return p==q; //只有都为空时return true
        }
        return (p->val == q->val) && isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};
```

Y

```C++
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) 
    {
        if(p==nullptr&&q==nullptr)return true;
        if(p&&q)return (p->val==q->val)&&isSameTree(p->left,q->left)&&isSameTree(p->right,q->right);
        return false;
    }
};
```



### （2）[101. 对称二叉树](https://leetcode.cn/problems/symmetric-tree/)

> 给你一个二叉树的根节点 `root` ， 检查它是否轴对称。

轴对称二叉树，可以认为是当前左子树`p`,右子树`q`两个节点的值相等，且左子树的左子树`==`右子树的右子树，且左子树的右子树`==`右子树的左子树。如果`p，q`有一个为空，则只能是`p==q`的时候才返回true，否则返回false。代码如下：

```c++
class Solution {
public:
    bool dfs(TreeNode* p, TreeNode* q)
    {
        if(p==nullptr || q==nullptr) return p==q;
        return (p->val==q->val) && dfs(p->left, q->right) && dfs(p->right, q->left);
    }
    bool isSymmetric(TreeNode* root) {
        if(root==nullptr) return true;
        return dfs(root->left, root->right);
    }
};
```





### （3）[110. 平衡二叉树](https://leetcode.cn/problems/balanced-binary-tree/)

平衡二叉树要求左右子树的高度差相差不超过1。这道题的关键在于返回值怎么设计，其实我们可以让递归函数返回树的高度，如果树已经不平衡了则返回-1，如果判断返回值为-1则会一路`return`上去，从而达到需求。因此本题的一种写法如下：
```c++
class Solution {
public:
    int get_height(TreeNode* root)
    {
        if(root==nullptr) return 0;
        int left_height = get_height(root->left);
        if(left_height==-1) return -1;
        int right_height = get_height(root->right);
        if(right_height==-1 || abs(left_height-right_height)>1) 
        {
            return -1;
        }
        return max(left_height, right_height) + 1;
    }
    bool isBalanced(TreeNode* root) {
        //平衡二叉树:左右子树高度差不超过1,要点:求子树高度
        return get_height(root)!=-1;
    }
};
```

Y

```C++
class Solution {
public:
    int Balance(TreeNode* root)
    {
        if(root==nullptr)return 0;
        int lh = Balance(root->left);
        int rh = Balance(root->right);
        if(lh==-1||rh==-1)return -1;
        if(abs(lh-rh)>1)return -1;
        return max(lh,rh)+1;
    }
    bool isBalanced(TreeNode* root) 
    {
        if(Balance(root)==-1)return false;
        return true;
    }
};
```

​	

### （4）[199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/) :cat:

> 给定一个二叉树的 **根节点** `root`，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。

假设先不考虑层序遍历。一种方法是先遍历右子树，再遍历左子树。但产生了两个问题：

- （1）怎么把答案记录下来？
- （2）怎么判断一个节点是否需要记录到答案当中？

可以在递归的时候传一个深度值进去。如果当前深度<记录数组中的元素个数，说明这一层已经找到最右侧的元素了，此时不做记录；否则如果==记录数组中的元素个数，则考虑计入。

代码如下：
```c++
class Solution {
public:
    vector<int> res;
    void dfs(TreeNode* root, int depth)
    {
        if(root==nullptr) return;
        if(depth==res.size()) //！！
        {
            res.emplace_back(root->val);
        }
        dfs(root->right, depth+1); //！！先右再左
        dfs(root->left, depth+1);
    }
    vector<int> rightSideView(TreeNode* root) {
        dfs(root, 0);
        return res;
    }
};
```

> 每次优先遍历右节点而非左节点，实际上保证了“某一层第一次被访问的节点一定在这一层的最右边”，因此只需要能够判断某一层是不是被第一次访问就行，怎么判断？加一个depth参数就可以。拿着`depth`参数和答案`res`数组的`size`作比较，就知道是不是第一次被记录了。



>深度是从上到下数的，而高度是从下往上数。不同题目适用不同的解法
>
><img src="assets/1523448-20190716212515612-1703079491.png" alt="img" style="zoom:50%;" />



#### （a）层序遍历的方法

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        //层序遍历
        queue<TreeNode*> que;
        vector<int> ans;
        if(root==nullptr) return ans; //注意根节点直接为空的情况
        que.push(root);
        
        while(!que.empty())
        {
            int sz = que.size();
            for(int i=0;i<sz;i++)
            {
                TreeNode* cur = que.front();
                if(i==sz-1) ans.push_back(cur->val);
                que.pop();
                if(cur->left) que.push(cur->left);
                if(cur->right) que.push(cur->right); 
            }
        }
        return ans;
    }
};
```





## 4.对应作业题

### （1）[965. 单值二叉树](https://leetcode.cn/problems/univalued-binary-tree/)

> 如果二叉树每个节点都具有相同的值，那么该二叉树就是*单值*二叉树。
>
> 只有给定的树是单值二叉树时，才返回 `true`；否则返回 `false`。

思路：如果当前节点为空，返回true；否则需要当前节点`==value`且左子树`==value`且右子树`==value`。代码如下：
```c++
class Solution {
public:
    bool dfs(TreeNode* root, int target)
    {
        if(root==nullptr) return true;
        bool flag = (root->val==target);
        return flag && dfs(root->left, target) && dfs(root->right, target);
    }
    bool isUnivalTree(TreeNode* root) {
        //一定有至少1个节点
        return dfs(root, root->val);
    }
};
```



### （2）[951. 翻转等价二叉树](https://leetcode.cn/problems/flip-equivalent-binary-trees/) :eye:

> 我们可以为二叉树 **T** 定义一个 **翻转操作** ，如下所示：选择任意节点，然后交换它的左子树和右子树。
>
> 只要经过一定次数的翻转操作后，能使 **X** 等于 **Y**，我们就称二叉树 **X** *翻转 等价* 于二叉树 **Y**。
>
> 这些树由根节点 `root1` 和 `root2` 给出。如果两个二叉树是否是*翻转 等价* 的函数，则返回 `true` ，否则返回 `false` 。

只要思考好可能的各种情况，答案应该就呼之欲出了。对于`bool flipEquiv(TreeNode* root1, TreeNode* root2)`提供的两个根节点而言，其实**相当于可翻可不翻**：

- （1）如果不翻，则`flipEquiv(root1->left, root2->left) && flipEquiv(root1->right, root2->right);`
- （2）如果翻，则`flipEquiv(root1->left, root2->right) && flipEquiv(root1->right, root2->left);`

因此，可以写出如下的代码：

```c++
class Solution {
public:
    bool flipEquiv(TreeNode* root1, TreeNode* root2) {
        if(root1==nullptr || root2==nullptr) return root1==root2;
        if(root1->val!=root2->val) return false; //相等的时候未必是true,但至少false是一定不等的，可以提前返回
        bool flag1 = flipEquiv(root1->left, root2->left) && flipEquiv(root1->right, root2->right);
        bool flag2 = flipEquiv(root1->left, root2->right) && flipEquiv(root1->right, root2->left);
        return flag1 || flag2;
    }
};
```



### （3）[226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/)

> 给你一棵二叉树的根节点 `root` ，翻转这棵二叉树，并返回其根节点。

相当于先翻转左右节点，再递归进入左右节点翻转。注意当根节点为空时return即可，不为空时进行翻转。代码如下：

```c++
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root==nullptr) return root;
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};
```



### （4）[617. 合并二叉树](https://leetcode.cn/problems/merge-two-binary-trees/)

> 给你两棵二叉树： `root1` 和 `root2` 。
>
> 想象一下，当你将其中一棵覆盖到另一棵之上时，两棵树上的一些节点将会重叠（而另一些不会）。你需要将这两棵树合并成一棵新二叉树。合并的规则是：如果两个节点重叠，那么将这两个节点的值相加作为合并后节点的新值；否则，**不为** null 的节点将直接作为新二叉树的节点。
>
> 返回合并后的二叉树。
>
> **注意:** 合并过程必须从两个树的根节点开始。

不妨思考合并的逻辑，将`root2`合并到`root1`上，并最终返回`root1`。

- 如果`root1`和`root2`都为空，则return，表示后面不会再合并了；
- 如果有一者为空，则为另一者，return另一者；
- 若都不为空，则加在一起。

递归处理`root1`的左右节点（因为`root1`为合并之后的结果），并返回`root1`。

代码如下（这属于先处理当前的节点的合并问题，再递归处理左右节点，根左右）：

```c++
class Solution {
public:
    TreeNode* mergeTrees(TreeNode* root1, TreeNode* root2) {
        if(root1==nullptr && root2==nullptr) return root1;
        if(root1==nullptr) return root2;
        if(root2==nullptr) return root1;
        root1->val = root1->val + root2->val;
        root1->left = mergeTrees(root1->left, root2->left);
        root1->right = mergeTrees(root1->right, root2->right);
        return root1;
    }
};
```

如果做了二叉树的公共祖先那道题，可能这题就没有那么难以理解了。



另一种做法，使用指针的引用才不会错误：

```c++
class Solution {
public:
    TreeNode* mergeTrees(TreeNode*& root1, TreeNode*& root2) {//得改成引用才行
        if(root1==nullptr&&root2==nullptr)return nullptr;
        if(root1&&root2)
        {
            int val = root1->val+root2->val;
            root1->val =val;
            mergeTrees(root1->left,root2->left);
            mergeTrees(root1->right,root2->right);
            //root2->val =val;
        }
        else if(root2) //无root1,有root2
        {
            root1 = root2;
        }
        return root1;
    }
};
```



### （5）[2331. 计算布尔二叉树的值](https://leetcode.cn/problems/evaluate-boolean-binary-tree/)

> 给你一棵 **完整二叉树** 的根，这棵树有以下特征：
>
> - **叶子节点** 要么值为 `0` 要么值为 `1` ，其中 `0` 表示 `False` ，`1` 表示 `True` 。
> - **非叶子节点** 要么值为 `2` 要么值为 `3` ，其中 `2` 表示逻辑或 `OR` ，`3` 表示逻辑与 `AND` 。
>
> **计算** 一个节点的值方式如下：
>
> - 如果节点是个叶子节点，那么节点的 **值** 为它本身，即 `True` 或者 `False` 。
> - 否则，**计算** 两个孩子的节点值，然后将该节点的运算符对两个孩子值进行 **运算** 。
>
> 返回根节点 `root` 的布尔运算值。
>
> **完整二叉树** 是每个节点有 `0` 个或者 `2` 个孩子的二叉树。
>
> **叶子节点** 是没有孩子的节点。

依旧是考虑题目怎么分治，以及各种情况。

- 如果当前节点为叶子节点，则return 自己的值；
- 如果当前节点不为叶子节点，那一定是有左右两个孩子（题目规定），此时如果自己是AND，则为两个孩子求&&;否则如果自己是OR，则为两个孩子求||；

题目规定这棵树的节点数至少为1。其实已经考虑完所有的情况了，就可以开始写代码了：

```c++
class Solution {
public:
    bool evaluateTree(TreeNode* root) {
        if(root->left==nullptr && root->right==nullptr)  //是叶子节点
        {
            return (bool)root->val; //这种情况下,根据题意,root本身是不会为空的
        }
        if(root->val==2) //逻辑OR
        {
            return evaluateTree(root->left) || evaluateTree(root->right);
        }
        else return evaluateTree(root->left) && evaluateTree(root->right);
    }
};
```



### (6)[508. 出现次数最多的子树元素和](https://leetcode.cn/problems/most-frequent-subtree-sum/)

> 给你一个二叉树的根结点 `root` ，请返回出现次数最多的子树元素和。如果有多个元素出现的次数相同，返回所有出现次数最多的子树元素和（不限顺序）。
>
> 一个结点的 **「子树元素和」** 定义为以该结点为根的二叉树上所有结点的元素之和（包括结点本身）。

对于每个和，我们用哈希表存储值和出现的次数即可，最后再依据频率来排序即可拿到结果。于是现在问题转换到了如何计算结果，那其实就是根+左孩子值+右孩子值。如果为空，则return即可。如果是叶子节点，则直接return 当前值。

- 如果当前节点并非空，则也需要记录一下当前的sum值放入哈希表中统计频率。

因此，可以写出下面的代码：

```c++
class Solution {
public:
    unordered_map<int, int> umap;
    int dfs(TreeNode* root)
    {
        if(root==nullptr) return 0;
        // if(root->left==nullptr && root->right==nullptr) return root->val;
        int sum = root->val + dfs(root->left) + dfs(root->right);
        umap[sum]++;
        return sum;
    }
    static bool cmp(const pair<int, int>& a, const pair<int, int>& b)
    {
        return a.second>b.second;
    }
    vector<int> findFrequentTreeSum(TreeNode* root) {
        dfs(root);
        vector<pair<int, int>> tmp(umap.begin(), umap.end()); 
        sort(tmp.begin(), tmp.end(), cmp);
        vector<int> res;
        int value = tmp[0].second;
        for(int i=0;i<tmp.size();i++)
        {
            if(tmp[i].second==value)
            {
                res.emplace_back(tmp[i].first);
            }
            else break;
        }
        return res;
    }
```

其实根本不用排序（因为只要找最大值），为了让复杂度更低，其实只需要在递归的时候维护一个最大值，然后遍历哈希表，记录value为最大值的key即可，修改后的代码如下：

```c++
class Solution {
public:
    unordered_map<int, int> umap;
    int maxFreq = 0;
    int dfs(TreeNode* root)
    {
        if(root==nullptr) return 0;
        // if(root->left==nullptr && root->right==nullptr) return root->val;
        int sum = root->val + dfs(root->left) + dfs(root->right);
        umap[sum]++;
        maxFreq = max(maxFreq, umap[sum]);
        return sum;
    }
    vector<int> findFrequentTreeSum(TreeNode* root) {
        dfs(root);
        vector<int> res;
        for(auto& [k, v]: umap)
        {
            if(v==maxFreq) res.emplace_back(k);
        }
        return res;
    }
};
```



### （7）[1026. 节点与其祖先之间的最大差值](https://leetcode.cn/problems/maximum-difference-between-node-and-ancestor/)

> 给定二叉树的根节点 `root`，找出存在于 **不同** 节点 `A` 和 `B` 之间的最大值 `V`，其中 `V = |A.val - B.val|`，且 `A` 是 `B` 的祖先。
>
> （如果 A 的任何子节点之一为 B，或者 A 的任何子节点是 B 的祖先，那么我们认为 A 是 B 的祖先）

我们可以找出所有的节点对，并记录他们的V值，最后只要排序即可。于是问题转换为了如何判断是一个合理的子孙对？

依旧是思考如何拆解为递归的问题。一个根节点和其左孩子和右孩子分别构成节点对（前提是存在），然后递归即可。

```C++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    int res;
    void dfs(TreeNode* root,int mn,int mx)
    {
        if(root == nullptr)return;
        mn = min(root->val,mn);
        mx = max(root->val,mx);
        res = max(res,mx-mn);
        dfs(root->left,mn,mx);
        dfs(root->right,mn,mx);
    }
    int maxAncestorDiff(TreeNode* root) {
        res =  INT_MIN;
        dfs(root,INT_MAX,INT_MIN);
        return res;
    }
};
```

