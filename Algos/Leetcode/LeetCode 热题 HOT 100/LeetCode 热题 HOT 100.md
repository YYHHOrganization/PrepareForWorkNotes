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
        // return dp[nums.size()-1];//不对 可能是中间的比较多 因为dp[i]代表的是以i为结尾的最长的 不一定是他 记住了吗
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





具体见题解：https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/?envType=problem-list-v2&envId=2cktkvj

 ![image-20250303213413576](assets/image-20250303213413576.png)

会把状态一步步返回上去，

如果没找到，返回的就是null

1、找到了 会进入【1】，返回最近公共祖先

2、节点p/q是另一个q/p的祖先节点，返回【2】


 ```C++
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if(root==NULL)return NULL;
        if(root==p||root==q)return root;//【2】
        TreeNode* left=lowestCommonAncestor(root->left,p,q); 
        TreeNode* right=lowestCommonAncestor(root->right,p,q); 
        if(left==NULL)return right;//保证其会取非空的，即有结果是祖先的那个
        else if(right==NULL)return left;//保证其会取非空的
        else return root;//【1】//左右子树都找到p和q了，那就说明p和q分别在左右两个子树上，所以此时的最近公共祖先就是root

    }
};
 ```



## 链表

### 7.Leetcode 160 相交链表  大厂笔记 :notebook:

//第二次看答案了

编写一个程序，找到两个单链表相交的起始节点。

**本题思路比较独特,需要仔细思考并记住这类题目的做法**

[160. 相交链表（双指针，清晰图解） - 相交链表 - 力扣（LeetCode） (leetcode-cn.com)](https://leetcode-cn.com/problems/intersection-of-two-linked-lists/solution/intersection-of-two-linked-lists-shuang-zhi-zhen-l/)



25/3/3

如果是环形的 

1、如果相遇之前个数不一样，第二轮遇到

<img src="assets/image-20250303235254966.png" alt="image-20250303235254966" style="zoom: 80%;" />

2、个数一样 第一轮会遇到 不会进 pa==nullptr?

![image-20250303235418711](assets/image-20250303235418711.png)

如果非环形，个数一样，一起遍历完一起为null  ； 个数不一样 第二轮一起为null

```C++
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode *pa  =headA,*pb = headB;
        //如果是环形的 1、如果相遇之前个数不一样，第二轮遇到 2、个数一样 第一轮会遇到
        while(pa!=pb)
        {
            pa = pa==nullptr?headB:pa->next;
            pb = pb==nullptr?headA:pb->next;
        }
        return pa;
    }
};
```







### [234. 回文链表](https://leetcode.cn/problems/palindrome-linked-list/) 简单

给你一个单链表的头节点 `head` ，请你判断该链表是否为回文链表。如果是，返回 `true` ；否则，返回 `false` 。

 

**示例 1：**

![img](assets/pal1linked-list.jpg)

```
输入：head = [1,2,2,1]
输出：true
```

**示例 2：**

![img](assets/pal2linked-list.jpg)

```
输入：head = [1,2]
输出：false
```

 

**提示：**

- 链表中节点数目在范围`[1, 105]` 内
- `0 <= Node.val <= 9`



```C++
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
class Solution 
{
public:
    bool isPalindrome(ListNode* head) 
    {
        vector<int> huiwen;
        ListNode * p = head;
        while(p!=nullptr)
        {
            huiwen.push_back(p->val);
            p=p->next;
        }
        int n = huiwen.size();
        for(int i=0;i<n/2;i++)
        {
            if(huiwen[i]!=huiwen[n-i-1])return false;
        }
        return true;
    }
};
```



M2

O(1) 空间做法：寻找中间节点+反转链表

使用**快慢指针**在一次遍历中找到中间：慢指针一次走一步，快指针一次走两步，快慢指针同时出发。当快指针移动到链表的末尾时，慢指针恰好到链表的中间。通过慢指针将链表分为两部分。



有时间尝试一下



