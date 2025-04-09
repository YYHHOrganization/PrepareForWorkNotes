# Leetcode——图论专题

[分享丨【题单】图论算法（DFS/BFS/拓扑排序/最短路/最小生成树/二分图/基环树/欧拉路径）- 讨论 - 力扣（LeetCode）](https://leetcode.cn/discuss/post/3581143/fen-xiang-gun-ti-dan-tu-lun-suan-fa-dfsb-qyux/)

# 一、基础遍历

## 1.DFS

### （1）[547. 省份数量](https://leetcode.cn/problems/number-of-provinces/)

#### （a）方法1：用DFS做，类似岛屿

> visited数组并不需要回退，类似于在遍历到的岛屿上插旗，表明来过了（这是我的地盘！）即可。

```c++
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        //方法1:DFS
        int n = isConnected.size(); //邻接矩阵
        vector<int> visited(n, 0);
        //i是开始遍历的城市,这题相当于岛屿数量
        auto dfs = [&](this auto&& dfs, int i)->void
        {
            visited[i] = 1;
            for(int j=0;j<n;j++)
            {
                if(isConnected[i][j]==1 && !visited[j])
                {
                    dfs(j);
                }
            }
        };
        int cnt = 0;
        for(int i=0;i<n;i++)
        {
            if(!visited[i])
            {
                dfs(i);
                cnt++;
            }
        }
        return cnt;
    }
};
```



#### （b）并查集的做法

> 可以写一下并查集的做法，正好能复习。

```c++
struct UnionFind
{
    vector<int> fa;
    vector<int> sz; //每个连通块的大小
    int cc;
    UnionFind(int n): fa(n), sz(n, 1), cc(n)
    {
        iota(fa.begin(), fa.end(), 0); //赋值fa[i] = i;
    }
    int find(int u)
    {
        if(fa[u]!=u)
        {
            fa[u] = find(fa[u]);
        }
        return fa[u];
    }
    bool isSame(int u, int v)
    {
        return find(u) == find(v);
    }
    void join(int from, int to)
    {
        from = find(from);
        to = find(to);
        if(from==to) return;
        fa[from] = to;
        sz[to] += sz[from];
        cc--;
    }
};
class Solution {
public:
    int findCircleNum(vector<vector<int>>& isConnected) {
        //使用并查集来做,有相邻的边就放到一起,由于是邻接矩阵,因此可以只遍历一半
        int n = isConnected.size();
        UnionFind uf(n);
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<=i;j++)
            {
                if(isConnected[i][j]==1)
                {
                    uf.join(i, j);
                }
            }
        }
        return uf.cc;
    }
};
```



### （2）[797. 所有可能的路径](https://leetcode.cn/problems/all-paths-from-source-to-target/)

> 给你一个有 `n` 个节点的 **有向无环图（DAG）**，请你找出所有从节点 `0` 到节点 `n-1` 的路径并输出（**不要求按特定顺序**）
>
>  `graph[i]` 是一个从节点 `i` 可以访问的所有节点的列表（即从节点 `i` 到节点 `graph[i][j]`存在一条有向边）。

```c++
class Solution {
public:
    vector<vector<int>> allPathsSourceTarget(vector<vector<int>>& graph) {
        //本题用DFS+回溯来做,题目给的输入是邻接表
        //有向图,没有环的话,可以不用visited数组，因为不会走回来 👍
        int n = graph.size();
        vector<int> path;
        vector<vector<int>> res;
        auto dfs = [&](this auto&& dfs, int start, int end)
        {
            if(start == end)
            {
                res.push_back(path);
                return;
            }
            for(int i = 0; i<graph[start].size(); i++)
            {
                path.push_back(graph[start][i]);
                dfs(graph[start][i], end);
                path.pop_back();
            }
        };
        path.push_back(0); //从0索引出发
        dfs(0, n-1);
        return res;
    }
};
```



### （3）[2316. 统计无向图中无法互相到达点对数](https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/)

> 给你一个整数 `n` ，表示一张 **无向图** 中有 `n` 个节点，编号为 `0` 到 `n - 1` 。同时给你一个二维整数数组 `edges` ，其中 `edges[i] = [ai, bi]` 表示节点 `ai` 和 `bi` 之间有一条 **无向** 边。
>
> 请你返回 **无法互相到达** 的不同 **点对数目** 。

这道题用并查集来做会比较方便，代码如下：
```c++
struct UnionFind
{
    vector<int> pa;
    vector<int> sz;
    int cc;
    UnionFind(int n): pa(n), sz(n, 1),cc(n)
    {
        iota(pa.begin(), pa.end(), 0);
    }
    int find(int u)
    {
        if(pa[u]!=u)
        {
            pa[u] = find(pa[u]);
        }
        return pa[u];
    }
    bool isSame(int u, int v)
    {
        return find(u) == find(v);
    }
    void join(int from, int to)
    {
        from = find(from);
        to = find(to);
        if(from==to) return;
        pa[from] = to;
        sz[to] += sz[from];
        cc--;
    }
};
class Solution {
public:
    long long countPairs(int n, vector<vector<int>>& edges) {
        //并查集比较简单,每个并查集中的点对都不能和其他集合中的相连,但全加在一起之后还要/2,因为会重复算
        int m = edges.size();
        UnionFind uf(n);
        for(int i=0;i<m;i++)
        {
            int from = edges[i][0];
            int to = edges[i][1];
            uf.join(from, to);
        }
        long long res = 0;
        //遍历每个点
        for(int i=0;i<n;i++)
        {
            int fa = uf.find(i); // 不可以直接用它自己 必须要找到其parent
            int other = n - uf.sz[fa]; //这么多与它不相连的
            res += other;
        }
        return res / 2; //每个节点对都多算了一遍,整体/2即可
    }
};
```



### （4）[2492. 两个城市间路径的最小分数](https://leetcode.cn/problems/minimum-score-of-a-path-between-two-cities/)

> 给你一个正整数 `n` ，表示总共有 `n` 个城市，城市从 `1` 到 `n` 编号。给你一个二维数组 `roads` ，其中 `roads[i] = [ai, bi, distancei]` 表示城市 `ai` 和 `bi` 之间有一条 **双向** 道路，道路距离为 `distancei` 。城市构成的图不一定是连通的。
>
> 两个城市之间一条路径的 **分数** 定义为这条路径中道路的 **最小** 距离。
>
> 城市 `1` 和城市 `n` 之间的所有路径的 **最小** 分数。
>
> **注意：**
>
> - 一条路径指的是两个城市之间的道路序列。
> - 一条路径可以 **多次** 包含同一条道路，你也可以沿着路径多次到达城市 `1` 和城市 `n` 。
> - 测试数据保证城市 `1` 和城市`n` 之间 **至少** 有一条路径。

#### （a）方法1：并查集

由于本题可以走回头路，因此可以先构建并查集，然后查每条边roads的任意一个节点是否和终点在一个并查集里，在的话说明可达，记录最小值即可。并查集的做法如下：
```c++
class Solution {
public:
    vector<int> father;
    int find(int u)
    {
        return father[u]==u? u: father[u] = find(father[u]);
    }
    bool isSame(int u, int v)
    {
        u=find(u);
        v=find(v);
        return u==v;
    }
    void join(int u, int v)
    {
        u=find(u);
        v=find(v);
        if(u==v) return;
        father[v]=u;
    }
    int minScore(int n, vector<vector<int>>& roads) {
        father.resize(n+1);
        for(int i=1;i<=n;i++) father[i] = i;
        for(int i=0;i<roads.size();i++)
        {
            join(roads[i][0], roads[i][1]);
        }
        //找最小值
        int nfather = find(n);
        int res = INT_MAX; //题目保证一定至少有一条路径
        for(int i=0;i<roads.size();i++)
        {
            int f = find(roads[i][0]); //自然,如果roads[i][0]在目标并查集中,roads[i][1]一定在目标并查集中,因此值判断一个即可
            if(f==nfather)
            {
                if(roads[i][2]<res) res=roads[i][2];
            }
        } 
        return res;
    }
};
```



**并查集 法2：**

要解决这个问题，我们需要找到城市1和城市n之间的所有路径中的最小分数，这个分数定义为路径中的道路的最小距离。我们可以使用并查集（Union-Find）数据结构来维护连通块，并在合并集合时跟踪每个连通块中的最小边权重。

方法思路

1. **并查集结构**：使用并查集来维护城市之间的连通性。每个节点维护其父节点、集合大小以及该集合中的最小边权重。
2. **合并操作**：在合并两个集合时，更新目标集合的最小边权重为原两个集合的最小边权重和当前边的权重的最小值。
3. **处理所有边**：遍历所有道路，处理每条边以更新并查集结构中的连通块信息。
4. **查找结果**：最后，找到城市1和城市n所在的连通块，其最小边权重即为答案。

```C++
class UnionFind
{
    vector<int> parent;
public:
    vector<int> sz;
    vector<int> minW;
    int cc;
    UnionFind(int n):cc(n),minW(n,INT_MAX),sz(n,1),parent(n)
    {
        ranges::iota(parent,0);
    }
    int find(int a)
    {
        if(a!=parent[a])
        {
            parent[a] = find(parent[a]);
        }
        return parent[a];
    }
    void join(int from,int to,int weight)
    {
        from =find(from);
        to = find(to);
        minW[to] = min({minW[to],weight,minW[from]});//[三者都要有]
        if(from==to)
        {
            return;
        }
        parent[from] = to;
        sz[to]+=sz[from];
        cc--;
    }
};
class Solution {
public:
    int minScore(int n, vector<vector<int>>& roads) {
        //一个集合的最小分数
        //存储
        UnionFind uf(n);
        for(int i=0;i<roads.size();i++)
        {
            uf.join(roads[i][0]-1,roads[i][1]-1,roads[i][2]);
        }
        int fa = uf.find(0);
        int minRes = uf.minW[fa];
        return minRes;
    }
};
```

>### 解释 `res.resize(n);` 的必要性
>
>1. **初始化大小**：如果 `res` 向量在使用之前没有被初始化（即没有设置大小），那么它的大小将是 `0`。在这种情况下，调用 `iota(res.begin(), res.end(), 0);` 将不会有任何效果，因为 `res.end()` 会等于 `res.begin()`，导致没有元素被填充。



#### （b）方法2：DFS

由于本题可以折返,因此答案其实就是连通块中所有边中的最小权重。注意dfs的过程中不需要设置end，也不要让start==end的时候提前退出之类的逻辑，我们需要遍历所有与1联通的最小的权重（因为题目保证从1一定能到达n），因此只需要visited数组做限制即可。

```c++
class Solution {
public:
    typedef pair<int, int> PII; // 存放每条边的to和权重
    int minScore(int n, vector<vector<int>>& roads) {
        //由于本题可以折返,因此答案其实就是连通块中所有边中的最小权重
        vector<vector<PII>> graph(n+1); //编号从1~n,所以要开n+1
        int m = roads.size();
        for(int i=0;i<m;i++)
        {
            int a = roads[i][0];
            int b = roads[i][1];
            int dist = roads[i][2];
            graph[a].emplace_back(make_pair(b, dist));
            graph[b].emplace_back(make_pair(a, dist));
        }
        vector<int> visited(n+1, 0);
        //dfs,从1出发到n,把连通块都涂成"visited"(也就是所有可达的块)
        int minRes = INT_MAX;
        auto dfs = [&](this auto&& dfs, int start) -> void
        {
            visited[start] = 1;
            //if(start==end) return;
            int sz = graph[start].size();
            for(int index=0;index<sz;index++)
            {
                minRes = min(minRes, graph[start][index].second);//【（1）】
                if(!visited[graph[start][index].first])
                    dfs(graph[start][index].first);
            }
        };
        //dfs(1, n); //注意题意是从1~n的编号
        dfs(1);
        return minRes;
    }
};
```

>### **为什么不需要回退`visited`？**
>
>` minRes = min(minRes, graph[start][index].second);//【（1）】`因为边会先更新，再判断节点是否被访问。
>
>1. **问题本质**：题目要求找到连通块中的最小边权。只要遍历所有边的最小值即可，无需关心具体路径。因为无论路径如何绕，只要连通块中存在某条边是当前最小值，最终结果一定是它。
>2. **DFS遍历的特性**：
>   - 当访问一个节点时，会处理其所有邻接边的权值。例如，节点`u`的邻接边`(u, v, w)`，无论`v`是否被访问过，都会将`w`与当前最小值比较。
>   - `visited`仅标记节点是否被访问过，防止重复遍历节点，但边的权值会在处理邻接边时被“捕获”。

注意：这题邻接矩阵好像会超出内存，需要用**邻接表**才行。如果不用visited或者visited有回退，那么会超时。综上，这题用并查集应该是更好的选择。



### （5）[3310. 移除可疑的方法](https://leetcode.cn/problems/remove-methods-from-project/)

> 你正在维护一个项目，该项目有 `n` 个方法，编号从 `0` 到 `n - 1`。
>
> 给你两个整数 `n` 和 `k`，以及一个二维整数数组 `invocations`，其中 `invocations[i] = [ai, bi]` 表示方法 `ai` 调用了方法 `bi`。
>
> 已知如果方法 `k` 存在一个已知的 bug。那么方法 `k` 以及它直接或间接调用的任何方法都被视为 **可疑方法** ，我们需要从项目中移除这些方法。
>
> 只有当一组方法没有被这组之外的任何方法调用时，这组方法才能被移除。
>
> 返回一个数组，包含移除所有 **可疑方法** 后剩下的所有方法。你可以以任意顺序返回答案。如果无法移除 **所有** 可疑方法，则 **不** 移除任何方法。

题意:k节点直接或者间接连到的节点都是可疑节点,如果可疑节点被其他节点调用(意味着有其他节点指向可疑节点的边),则不能删除可疑节点,否则可以删除可疑节点,如果有一个可疑节点不能删除,则所有的节点都不删除;否则,删除所有可疑的节点。

注意，这道题是有向图，**当看到有向图的时候基本上不能用并查集来做**，所以本题可以直接放弃并查集的做法。

> 做图论的题，代码往往都相对较长，而且过程可能会比较麻烦，考虑好再开始写代码。

本题代码如下：
```c++
class Solution {
public:
    vector<int> remainingMethods(int n, int k, vector<vector<int>>& invocations) {
        //step 0:构建图:a调用b则有一条a->b的边
        vector<vector<int>> graph(n);
        int m = invocations.size();
        for(int i=0;i<m;i++)
        {
            int from = invocations[i][0];
            int to = invocations[i][1];
            graph[from].emplace_back(to);
        }

        //step 1: 找到哪些是可疑的方法,标记为1
        vector<int> isSuspicious(n, 0); //可以充当visited了
        //vector<int> visited(n, 0); //以防万一,遍历过的不再遍历
        auto dfs = [&](this auto&& dfs, int start) -> void
        {
            //visited[start] = 1;
            isSuspicious[start] = 1;
            int sz = graph[start].size();
            for(int index=0;index<sz;index++)
            {
                int dest = graph[start][index];
                //if(!visited[dest])
                if(!isSuspicious[dest])
                {
                    dfs(dest);
                }
            }
        };
        dfs(k);
        //此时isSuspicious数组中为1的是所有可疑的方法
        //step 2:遍历invocations数组,如果[a,b]中的b对应isSuspicious[b]为1(同时isSuspicious[a]!=1),说明被非可疑方法调用了,直接返回所有的节点并break掉,最后能删除则返回所有非可疑的方法
        vector<int> res;
        for(int i=0;i<m;i++)
        {
            int from = invocations[i][0];
            int to = invocations[i][1];
            if(!isSuspicious[from] && isSuspicious[to])
            {
                res.resize(n);//一定需要有这句
                iota(res.begin(), res.end(), 0);
                return res;
            }
        }
        //没有return所有的情况,非可疑方法是我们想要的
        for(int i=0;i<n;i++)
        {
            if(!isSuspicious[i]) res.emplace_back(i);
        }
        return res;
    }
};
```



### （6）[2685. 统计完全连通分量的数量](https://leetcode.cn/problems/count-the-number-of-complete-components/)

> 给你一个整数 `n` 。现有一个包含 `n` 个顶点的 **无向** 图，顶点按从 `0` 到 `n - 1` 编号。给你一个二维整数数组 `edges` 其中 `edges[i] = [ai, bi]` 表示顶点 `ai` 和 `bi` 之间存在一条 **无向** 边。
>
> 返回图中 **完全连通分量** 的数量。
>
> 如果在子图中任意两个顶点之间都存在路径，并且子图中没有任何一个顶点与子图外部的顶点共享边，则称其为 **连通分量** 。
>
> 如果连通分量中每对节点之间都存在一条边，则称其为 **完全连通分量** 。

#### （a）方法1：DFS

用visited数组，每次都把第一次遍历到的放到一个集合里，最后看这个集合里每个节点的相连的边数是不是都是集合的size-1，如果是的话就是完全联通分量，否则不是完全联通分量。代码如下：

```c++
class Solution {
public:
    int countCompleteComponents(int n, vector<vector<int>>& edges) {
        //step 0: 先构建邻接表
        vector<vector<int>> graph(n);
        int m = edges.size();
        for(int i=0;i<m;i++)
        {
            int a = edges[i][0];
            int b = edges[i][1];
            graph[a].emplace_back(b);
            graph[b].emplace_back(a);
        }
        //step 1:开始做这道题
        int ans = 0;
        vector<int> visited(n, 0);
        //res保存的是新加进来的顶点
        auto dfs = [&](this auto&& dfs, int start, vector<int>& res) ->void 
        {
            res.emplace_back(start);
            visited[start] = 1;
            int sz = graph[start].size();
            for(int index=0;index<sz;index++)
            {
                if(!visited[graph[start][index]])
                {
                    dfs(graph[start][index], res);
                }
            }
        };  
        for(int i=0;i<n;i++)
        {
            if(!visited[i])
            {
                vector<int> subNodes; //记录这个连通块有哪些节点
                dfs(i, subNodes); //这样res就会记录这一连通块内有多少个节点
                bool flag = true;
                int total = subNodes.size();
                for(int x: subNodes)
                {
                    if(graph[x].size()!=total-1) 
                    {
                        flag = false;
                        break;
                    }
                }
                if(flag) ans++;
            }
        }
        return ans;
    }
};
```



#### （b）优化

> 题解参考：[2685. 统计完全连通分量的数量 - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-complete-components/solutions/2269255/dfs-qiu-mei-ge-lian-tong-kuai-de-dian-sh-opg4/)

实际上，上述的方法可以做一些数学上的优化，在DFS的时候，每遍历到一个点，顶点数+=1（当前顶点v），e+=v的边数，但这样会导致每条边被统计了两遍。对于完全联通分量而言，假设顶点数为n，边数为e，应该有e = (n-1) * n / 2，根据这个条件来判断即可。

<img src="assets/image-20250403183920251.png" alt="image-20250403183920251" style="zoom:80%;" />

此时依据数学来判断，会使得代码更优雅一些：

```c++
class Solution {
public:
    int countCompleteComponents(int n, vector<vector<int>>& edges) {
        //step 0: 先构建邻接表
        vector<vector<int>> graph(n);
        int m = edges.size();
        for(int i=0;i<m;i++)
        {
            int a = edges[i][0];
            int b = edges[i][1];
            graph[a].emplace_back(b);
            graph[b].emplace_back(a);
        }
        //step 1:开始做这道题
        int ans = 0;
        vector<int> visited(n, 0);
        //res保存的是新加进来的顶点
        auto dfs = [&](this auto&& dfs, int start, int& nodeCnt, int& edgeCnt) ->void 
        {
            visited[start] = 1;
            nodeCnt += 1;
            edgeCnt += (int)graph[start].size();
            int sz = graph[start].size();
            for(int index=0;index<sz;index++)
            {
                if(!visited[graph[start][index]])
                {
                    dfs(graph[start][index], nodeCnt, edgeCnt);
                }
            }
        };  
        for(int i=0;i<n;i++)
        {
            if(!visited[i])
            {
                int nodeCnt = 0;
                int edgeCnt = 0;
                dfs(i, nodeCnt, edgeCnt); 
                if(nodeCnt*(nodeCnt-1)==edgeCnt) ans++;
            }
        }
        return ans;
    }
};
```



### ==（7）[2192. 有向无环图中一个节点的所有祖先](https://leetcode.cn/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/)==（未整理完）

> 给你一个正整数 `n` ，它表示一个 **有向无环图** 中节点的数目，节点编号为 `0` 到 `n - 1` （包括两者）。
>
> 给你一个二维整数数组 `edges` ，其中 `edges[i] = [fromi, toi]` 表示图中一条从 `fromi` 到 `toi` 的单向边。
>
> 请你返回一个数组 `answer`，其中 `answer[i]`是第 `i` 个节点的所有 **祖先** ，这些祖先节点 **升序** 排序。
>
> 如果 `u` 通过一系列边，能够到达 `v` ，那么我们称节点 `u` 是节点 `v` 的 **祖先** 节点。

本题有两种基本的思路，分别是DFS和拓扑排序，详见链接中提交过的题解。



### （8）==[3387. 两天自由外汇交易后的最大货币数](https://leetcode.cn/problems/maximize-amount-after-two-days-of-conversions/)==（未整理，这题比较烦，再说吧，0x3f的题解有个视频可以看看）

这题好像在哪里整理过。（做过这题）

### （9）[924. 尽量减少恶意软件的传播](https://leetcode.cn/problems/minimize-malware-spread/)

题目的大概意思是说，找到一个连通块，需要满足连通块里最多只有一个被感染的软件（否则即使删除了，还有感染软件也会污染连通块内的软件），并且这个连通块还要尽可能地大。我们可以DFS每个被感染的且没有visited的节点，统计其能到达的节点数（如果遇到了另一个被感染的软件，则return 0，表示无法清除这个连通块的污染），找到最小值即可。



我们要找的是**只包含一个被感染节点的连通块**，并且这个连通块**越大越好**。

#### 方法1：DFS

```c++
class Solution {
public:
    typedef pair<int, int> PII;
    static bool compare(const PII& a, const PII& b)
    {
        if(a.second == b.second) return a.first<b.first;
        return a.second > b.second;
    }
    int minMalwareSpread(vector<vector<int>>& graph, vector<int>& initial) {
        //记录每个initial数组元素所能联通到的软件的数量(包括自己)
        int n = graph.size();
        //返回连通块的数量
        vector<int> visited(n, 0); 
        int m = initial.size();
        unordered_set us(initial.begin(), initial.end()); //用于快速找是否是恶意软件
        auto dfs = [&](this auto&& dfs, int cur, bool first) -> int
        {
            visited[cur] = 1;
            int cnt = 1;
            if(!first && us.contains(cur)) return 0; //不是第一次遇到恶意软件,则整个返回0
            bool hasOtherBad = false;
            for(int i=0;i<n;i++)
            {
                if(graph[cur][i]==1 && !visited[i]) //有联通的,并且没有访问过
                {
                    int res = dfs(i, false);
                    if(res == 0) hasOtherBad = true;
                    else cnt += res;
                }
            }
            if(hasOtherBad) cnt = 0;
            return cnt;
        };
        //遍历所有的initial中的元素,记录能够抵达的(包含自己)的软件的数量,放到vector里
        vector<PII> vec(m); //first:索引,second:数量
        for(int i=0;i<m;i++)
        {
            int x = initial[i];
            if(visited[x])
            {
                vec[i] = make_pair(x, 0);
                continue; //说明访问过,意味着与其他恶意软件相连了
            }
            int ans = dfs(x, true);
            vec[i] = make_pair(x, ans);
        }
        //这题表述的有问题,如果找不到最大的话就返回initial里面最小的那个值(也就是最小的索引)
        sort(vec.begin(), vec.end(), compare);
        return vec[0].first;
    }
};
```



#### 方法2：DFS+状态机

注：这篇题解里面的状态机思路值得学习一下：[924. 尽量减少恶意软件的传播 - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-malware-spread/)。

```C++
class Solution {
public:
    int minMalwareSpread(vector<vector<int>>& graph, vector<int>& initial) {
        //状态机： 无感染-1 -》 感染x -》感染大于1：-2 
        //dfs 
        int size =0;
        int maxsize=0;
        int n = graph.size();
        vector<int> visited(n,0);
        int node_id=-1;
        //存放恶意软件
        unordered_set<int> badUset(initial.begin(),initial.end());
        int resIndex=-1;
        //需要有->void  不然会错
        auto dfs = [&](this auto&& dfs,int cur)->void
        {
            visited[cur] = 1;
            size++;
            if(node_id!=-2&&badUset.contains(cur))
            {
                node_id = node_id==-1?cur:-2;
            }
            for(int i=0;i<graph[cur].size();i++)
            {
                if(graph[cur][i] && !visited[i])//【!】graph[i][j]别忘
                {
                    dfs(i);
                }
            }
        };
        for(int i=0;i<initial.size();i++)
        {
            if(visited[initial[i]])continue;//【!】这句没有会错
            node_id = -1;
            size = 0;
            dfs(initial[i]);
            if(node_id >=0)//只有一个是坏的
            {
                if(size>maxsize)
                {
                    maxsize = size;
                    resIndex = node_id;
                }
                else if(size ==maxsize)
                {
                    resIndex = min(resIndex,node_id);
                }
            }
        }
        if(resIndex == -1)
        {
            return *min_element(initial.begin(),initial.end());
        }
        return resIndex;
    }
};
```





#### 方法3：并查集

推荐做法 这题并查集好写，而dfs更容易写错

```c++
struct UnionFind
{
    vector<int> fa;
    vector<int> sz;
    int cc;
    UnionFind(int n): fa(n), sz(n, 1), cc(n)
    {
        iota(fa.begin(), fa.end(), 0);
    }
    int find(int u)
    {
        if(u!=fa[u])
        {
            fa[u] = find(fa[u]);
        }
        return fa[u];
    }
    bool isSame(int u, int v)
    {
        return find(u) == find(v);
    }
    void join(int from, int to)
    {
        from = find(from);
        to = find(to);
        if(from==to) return;
        fa[from] = to;
        sz[to] += sz[from];
        cc--;
    }
};
class Solution {
public:
    typedef pair<int, int> PII;
    int minMalwareSpread(vector<vector<int>>& graph, vector<int>& initial) {
        //用并查集应该会更加直观一些,有两个initial数组中的元素parent一样,则不考虑
        int n = graph.size();
        UnionFind uf(n);
        for(int i=0;i<n;i++) //邻接矩阵,遍历一半即可
        {
            for(int j=0;j<=i;j++)
            {
                if(graph[i][j]==1)
                    uf.join(i, j);
            }
        }
        
        int ans = n, mx = 0;
        vector<int> cnt(n);//记录块中的恶意软件个数
        for (int x : initial) 
        {
            ++cnt[uf.find(x)];
        }
        for (int x : initial) 
        {
            int root = uf.find(x);
            if (cnt[root] == 1) //一个集合里只有一个恶意软件,符合题意
            {
                int sz = uf.sz[root]; //集合里元素的数量
                if (sz > mx || (sz == mx && ans > x)) //集合里元素数量更多,或者索引值更小(initial 数组里的更小的值)
                {
                    ans = x;
                    mx = sz;
                }
            }
        }
        //ans默认是n,如果结束ans==n意味着没有被更新过
        return ans == n ? *min_element(initial.begin(), initial.end()) : ans;
    }
};
```



####　思考题：

> 如果改成移除 2 个节点呢？改成移除 *k* 个节点呢？

移除k个节点的话，可以在算出联通块的大小和被感染的个数之后采用0-1背包的作法。将连通块大小看成价值，每个块里面的感染个数是重量，而k就是背包的总重量。因为每个连通块的感染数要么全部移除，要么全部保留。



### （10）[2101. 引爆最多的炸弹](https://leetcode.cn/problems/detonate-the-maximum-bombs/)

> 给你一个炸弹列表。一个炸弹的 **爆炸范围** 定义为以炸弹为圆心的一个圆。
>
> 炸弹用一个下标从 **0** 开始的二维整数数组 `bombs` 表示，其中 `bombs[i] = [xi, yi, ri]` 。`xi` 和 `yi` 表示第 `i` 个炸弹的 X 和 Y 坐标，`ri` 表示爆炸范围的 **半径** 。
>
> 你需要选择引爆 **一个** 炸弹。当这个炸弹被引爆时，**所有** 在它爆炸范围内的炸弹都会被引爆，这些炸弹会进一步将它们爆炸范围内的其他炸弹引爆。
>
> 给你数组 `bombs` ，请你返回在引爆 **一个** 炸弹的前提下，**最多** 能引爆的炸弹数目。

！！注意，**本题不能使用并查集来做**，因为炸弹的引爆不是双向的，比如炸弹A和炸弹B之间的距离为4，炸弹A的半径为3，炸弹B的半径为4，此时只能通过B来引爆A，不能反着来，因此这道题目应该被抽象为**有向图**，而非无向图，因此不能使用并查集。

此时代码如下（难点在于不要试图用并查集做，构建图之后老老实实用DFS即可）：

```c++
class Solution {
public:
    int maximumDetonation(vector<vector<int>>& bombs) {
        //构建邻接表
        int n = bombs.size();
        vector<vector<int>> graph(n);
        for(int i=0;i<n;i++)
        {
            long long xi = bombs[i][0];
            long long yi = bombs[i][1];
            long long radius = bombs[i][2];
            for(int j=0;j<n;j++)
            {
                long long dx = (xi - bombs[j][0]);
                long long dy = (yi - bombs[j][1]);
                if(dx * dx + dy * dy <= radius * radius) //在爆炸范围内,相当于相连
                {
                    graph[i].emplace_back(j);
                }
            }
        }
        vector<int> visited(n, 0);
        auto dfs = [&](this auto&& dfs, int cur) -> int
        {
            int cnt = 1;
            visited[cur] = 1;
            int sz = graph[cur].size();
            for(int i=0;i<sz;i++)
            {
                if(!visited[graph[cur][i]])
                {
                    cnt += dfs(graph[cur][i]); 
                }
            }
            return cnt;
        };
        int res = 0;
        for(int i=0;i<n;i++)
        {
            //ranges::fill(visited, 0);
            std::fill(visited.begin(), visited.end(), 0); //没有ranges的话用这个
            int count = dfs(i);
            res = max(res, count);
        }
        return res;
    }
};
```



### （11）[207. 课程表](https://leetcode.cn/problems/course-schedule/)

这里可以学习一种新的做法，为”三色标记法“判断图中是否有环。具体可以看这篇题解：[207. 课程表 - 力扣（LeetCode）](https://leetcode.cn/problems/course-schedule/solutions/2992884/san-se-biao-ji-fa-pythonjavacgojsrust-by-pll7/)。

> 注：在有向图中，不能完成拓扑排序的唯一原因就是图中存在有向环。以下是详细的解释和论证：
>
> ### 1. **拓扑排序的定义与性质**
>    - 拓扑排序是对有向无环图（DAG）的顶点的一种线性排序，使得对于图中的每一条有向边 \((u, v)\)，\(u\) 在排序中总是位于 \(v\) 的前面。
>    - **关键性质**：拓扑排序存在的充要条件是图必须是无环的。如果图中存在环，则无法满足所有边的方向性要求，因为环中的顶点会相互依赖，无法确定线性顺序。
>
> ### 2. **为什么有环会导致拓扑排序失败？**
>    - **自洽性矛盾**：假设图中存在一个环 ($v_1 \to v_2 \to \cdots \to v_k \to v_1$。根据拓扑排序的定义：
>      - \(v_1\) 必须在 \(v_2\) 之前，
>      - \(v_2\) 必须在 \(v_3\) 之前，
>      - ……
>      - \(v_k\) 必须在 \(v_1\) 之前。
>    - 这会导致 \(v_1\) 必须同时在 \(v_1\) 之前和之后，产生矛盾，因此无法构造拓扑排序。
>
> ### 3. **其他可能情况的探讨**
>    - **非连通图**：即使图是非连通的（即由多个互不连通的DAG组成），只要每个连通分量都是无环的，仍然可以构造拓扑排序（例如按分量独立排序后拼接）。
>    - **顶点孤立或无边**：没有边的图（仅孤立顶点）或某些顶点无依赖关系时，拓扑排序仍然存在（顶点的任意顺序均满足定义）。
>    - **结论**：除了有向环之外，**不存在其他情况会导致拓扑排序失败**。拓扑排序的不可行性完全由环的存在决定。
>
> ### 4. **算法角度的验证**
>    - **Kahn算法**：基于逐步移除入度为0的顶点。如果算法结束时仍有未移除的顶点，说明剩余顶点构成环（因为它们互相依赖，入度无法降为0）。
>    - **DFS方法**：通过检测后向边（back edge）判断环的存在。若存在后向边，则无法完成拓扑排序。
>
> ### 5. **反例思考**
>    - 假设存在一种无环但有其他原因导致拓扑排序失败的情况，例如“顶点无限多”或“非良序依赖”。但在有限图中，这些情况不适用。无限图超出常规拓扑排序的讨论范围。
>
> ### 总结
> **有向图无法完成拓扑排序的唯一原因是图中存在有向环**。其他图的结构特性（如非连通性、孤立顶点等）均不影响拓扑排序的存在性。这一结论是图论中拓扑排序的核心性质之一。


因此，本题就转变为了如何在有向图中判断是否有环，具体做法可以参考上面的题解。以下是两种三色标记法的写法:

```c++
class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        //无法完成拓扑排序,只有可能是有环,用三色标记法判断是否会有环
        //step 1:根据prerequisites构建邻接表
        vector<vector<int>> graph(numCourses);
        for(auto& p: prerequisites)
        {
            int from = p[1];
            int to = p[0];
            graph[from].emplace_back(to);
        }
        //step 2:写dfs的代码,用于后面三色标记法判断是否有环
        vector<int> visited(numCourses, 0); //0表示没有访问过,-1表示正在堆栈里,-2表示结束访问
        //dfs = true 表示有环,false表示没有环
        auto dfs = [&](this auto&& dfs, int cur) -> bool
        {
            if(visited[cur]==-2) return false; //这个节点彻底访问完了,没环
            visited[cur] = -1; //正在访问
            int sz = graph[cur].size();
            bool hasCircle = false;
            for(int i=0;i<sz;i++)
            {
                int nxt = graph[cur][i];
                if(visited[nxt]==-1 || dfs(nxt)) //访问了正在访问的,
                {
                    hasCircle = true;
                }
            }
            visited[cur] = -2; //访问完毕
            return hasCircle;
        };
        //step 3:遍历所有的节点,检查是否有环
        for(int i=0;i<numCourses;i++)
        {
            if(visited[i]==0)
            {
                bool res = dfs(i);
                if(res) return false;
            }
        }
        return true;
    }
};
```
另一种:
```C++
class Solution {
public:
    //10
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        //有环则不能完成
        // 0  1  2
        // 还没访问过0  访问过为1 其周围全部访问过 为2（不用再走这条路了）
        //bi.push ai
        vector<vector<int>> adj(numCourses);
        for(int i=0;i<prerequisites.size();i++)
        {
            int a = prerequisites[i][0];
            int b = prerequisites[i][1];
            adj[b].push_back(a);
        }
        vector<int> visited(numCourses,0);
        auto dfs = [&](this auto&& dfs,int i)->bool
        {
            if(visited[i]==2)return false;
            if(visited[i]==1)return true;
            visited[i]=1;
            for(int j=0;j<adj[i].size();j++)
            {
                if(dfs(adj[i][j])==true)
                {
                    return true;
                }
            }
            visited[i]=2;
            return false;
        };
        for(int i=0;i<numCourses;i++)
        {
            if(dfs(i)==true)return false;
        }
        return true;
```




### （12）[802. 找到最终的安全状态](https://leetcode.cn/problems/find-eventual-safe-states/)

写了一版有各种问题，看一下官方的题解吧：[802. 找到最终的安全状态 - 力扣（LeetCode）](https://leetcode.cn/problems/find-eventual-safe-states/)。

> 务必注意DFS的各种情况，能否提前return之类的。

#### （a）方法1：三色标记法判断是否有环

本题代码如下：

```c++
class Solution {
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> colors(n, 0); //1表示正在访问,2表示访问过了
        //true表示有环,false表示没有环,注意在判断的过程中如果遇到了环则直接一路返回,不修改color的状态,这样后面的节点遍历到colors>0的节点就会知道是否是安全的了
        auto dfs = [&](this auto&& dfs, int cur) -> bool
        {
            if(colors[cur]>0)
            {
                return colors[cur]==1; 
            }
            colors[cur] = 1; //先认为是不安全的,或者理解成是在栈里面的
            int sz = graph[cur].size();
            for(int i=0;i<sz;i++)
            {
                if(dfs(graph[cur][i])) //说明有环
                {
                    return true; //提前返回,这里不需要全遍历完,因为会有colors数组保留节点的状态,这样一路上的节点都会被保持为1的情况,即不安全
                }
            }
            colors[cur] = 2;
            return false;
        };
        vector<int> res;
        for(int i=0;i<n;i++)
        {
            if(!dfs(i)) //说明没有环或者说已经被标记成了安全节点
            {
                res.push_back(i);
            }
        }
        return res;
    }
};
```

每次结束DFS之后,已经访问过的没环的节点会是2,在环内的节点会是1。



#### （b）方法2：逆拓扑排序

> 根据题意，**若一个节点没有出边，则该节点是安全的；若一个节点出边相连的点都是安全的，则该节点也是安全的。**
>
> 根据这一性质，我们可以将图中所有边反向，得到一个反图，然后在反图上运行拓扑排序。
>
> 具体来说，首先得到反图 rg 及其入度数组 inDeg。将所有入度为 0 的点加入队列，然后不断取出队首元素，将其出边相连的点的入度减一，若该点入度减一后为 0，则将该点加入队列，如此循环直至队列为空。循环结束后，所有入度为 0 的节点均为安全的。我们遍历入度数组，并将入度为 0 的点加入答案列表。
>

拓扑排序的话记录的是入度为0的点，因此对于反图来说正好是出度为0的点，即为所求。将反图进行拓扑排序之后，所有入度为0的点（相当于原图出度为0）即为所求。

代码如下：
```c++
class Solution {
public:
    vector<int> eventualSafeNodes(vector<vector<int>>& graph) {
        //环也可以用拓扑排序来做
        //step 1:求反图
        int n = graph.size();
        vector<vector<int>> rg(n);
        vector<int> indegrees(n, 0);
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<(int)graph[i].size();j++)
            {
                int from = graph[i][j];
                int to = i;
                rg[from].emplace_back(to);
                indegrees[to]++;
            }
        }
        queue<int> que;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==0) que.push(i);
        }
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            for(int i=0;i<rg[cur].size();i++)
            {
                indegrees[rg[cur][i]]--;
                if(indegrees[rg[cur][i]]==0) //所有入度为0的点都是不会成环的点
                {
                    que.push(rg[cur][i]);
                }
            }
        }
        vector<int> res;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==0) res.emplace_back(i);
        }
        return res;
    }
};
```



## 2.BFS基础

### （1）[3243. 新增道路查询后的最短距离 I](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-i/)

之前做这道题的代码比较怪，有点Dijkstra那个感觉，但又不是，如果要写BFS的话还是写的正统一些，如下：

```c++
class Solution {
public:
    vector<int> shortestDistanceAfterQueries(int n, vector<vector<int>>& queries) {
        //有向图,直接放弃并查集
        //BFS可以求最短路,暴力每个查询都做一次BFS.为了防止visited数组每次要刷一遍,可以认为visited[i]=step的才是本轮访问过的
        vector<int> visited(n, -1); //一开始是-1,第step轮被访问的会被刷成step
        //先建图
        vector<vector<int>> graph(n);
        for(int i=0;i<n-1;i++)
        {
            int from = i;
            int to = i+1;
            graph[from].push_back(to);
        }
        auto bfs = [&](int start, int end, int step)
        {
            //BFS,用队列来做
            queue<int> que;
            que.push(start);
            int totalStep = 0;
            while(!que.empty())
            {
                int size = que.size();
                totalStep+=1; //新走了一步
                while(size--)
                {
                    int cur = que.front();
                    que.pop();
                    int sz = graph[cur].size();
                    for(int idx = 0;idx<sz;idx++)
                    {
                        int nxt = graph[cur][idx];
                        if(nxt == end) return totalStep;
                        if(visited[nxt]!=step) 
                        {
                            visited[nxt] = step;
                            que.push(nxt);
                        }
                    }
                }
            }
            return totalStep; //根据题意,本题能够保证可达
        };
        int m = queries.size();
        vector<int> res(m);
        for(int i=0;i<m;i++)
        {
            int addFrom = queries[i][0];
            int addTo = queries[i][1];
            graph[addFrom].push_back(addTo);
            int step = bfs(0, n-1, i); //最后一个参数是step
            res[i] = step;
        }
        return res;
    }
};
```



### （2）[1129. 颜色交替的最短路径](https://leetcode.cn/problems/shortest-path-with-alternating-colors/)

以下代码写的可能比较冗长，也可以参考这篇题解：[1129. 颜色交替的最短路径 - 力扣（LeetCode）](https://leetcode.cn/problems/shortest-path-with-alternating-colors/solutions/2087881/python3javacgo-yi-ti-yi-jie-bfsqing-xi-t-ag0i/)

```c++
class Solution {
public:
    vector<int> shortestAlternatingPaths(int n, vector<vector<int>>& redEdges, vector<vector<int>>& blueEdges) {
        //建图,把红边和蓝边都放进去
        vector<vector<vector<int>>> graph(2, vector<vector<int>>(n)); //2表示红和蓝,后面一个维度则是每个顶点
        for(int i=0;i<redEdges.size();i++)
        {
            int from = redEdges[i][0];
            int to = redEdges[i][1];
            graph[0][from].push_back(to);
        }
        for(int i=0;i<blueEdges.size();i++)
        {
            int from = blueEdges[i][0];
            int to = blueEdges[i][1];
            graph[1][from].push_back(to);
        }
        //bfs
        vector<vector<int>> visited(2, vector<int>(n, 0));
        queue<pair<int, int>> que; //first是红蓝属性,second则是节点
        //把起点相关的边的放入队列中
        for(int i=0;i<graph[0][0].size();i++) //红色边
        {
            que.push(make_pair(0, graph[0][0][i])); 
        }
        for(int i=0;i<graph[1][0].size();i++)
        {
            que.push(make_pair(1, graph[1][0][i]));
        }
        visited[0][0] = 1;
        visited[1][0] = 1;
        int step = 0;
        //一开始,队列里应该有连接起点的所有红蓝边
        vector<int> res(n, 0x3f3f3f);
        res[0] = 0; //起点是0,一定可达
        while(!que.empty())
        {
            int queSize = que.size();
            step += 1;
            while(queSize--)
            {
                auto p = que.front();
                que.pop();
                int color = p.first; //颜色
                res[p.second] = min(res[p.second], step);
                for(int idx = 0; idx<graph[1-color][p.second].size();idx++)
                {
                    int nxt = graph[1-color][p.second][idx]; //下一个节点
                    if(!visited[1-color][nxt])
                    {
                        visited[1-color][nxt] = 1;
                        que.push(make_pair(1-color, nxt));
                    }
                }
            }
        }
        for(int i=0;i<n;i++)
        {
            if(res[i]==0x3f3f3f) res[i] = -1; //表明不可达
        }
        return res;
    }
};
```



Y：

```C++
class Solution {
public:
    //10 ++ 
    vector<int> shortestAlternatingPaths(int n, vector<vector<int>>& redEdges, vector<vector<int>>& blueEdges) {
        //记录 红色图 和 蓝色图
        //记录 当前节点dist 最后 从红色来 和从蓝色来 的情况
        vector<vector<int>> redAdj(n);
        vector<vector<int>> blueAdj(n);
        for(auto &v:redEdges)
        {
            //0->1
            redAdj[v[0]].emplace_back(v[1]);
        }
        for(auto &v:blueEdges)
        {
            blueAdj[v[0]].emplace_back(v[1]);
        }
        vector<int> redD(n,-1);
        vector<int> blueD(n,-1);
        queue<pair<int,int>> que;//存放当前节点 及其来的颜色 <节点index,0red 1blue>
        que.emplace(0,0);
        que.emplace(0,1);
        redD[0]=0;
        blueD[0]=0;
        int step=0;
        vector<int> ans(n,0x3f3f3f);
        while(!que.empty())
        {
            step++;
            int sz = que.size();
            for(int i=0;i<sz;i++)
            {
                auto [idx,color] = que.front();
                que.pop();
                ans[idx] = min(ans[idx],step-1);
                if(color==0)
                {
                    for(auto k:blueAdj[idx])
                    {
                        if(blueD[k]!=-1)continue;
                        blueD[k] = step;
                        que.emplace(k,1);
                    }
                }
                else
                {
                    for(auto k:redAdj[idx])
                    {
                        if(redD[k]!=-1)continue;
                        redD[k] = step;
                        que.emplace(k,0);
                    }
                }
            }
        }
       
        for(int i=0;i<n;i++)
        {
            if(ans[i]==0x3f3f3f)ans[i] = -1;
        }
        return ans;
    }
};
```



### （3）[1298. 你能从盒子里获得的最大糖果数](https://leetcode.cn/problems/maximum-candies-you-can-get-from-boxes/)

”最大“比较迷惑人，其实就是把所有能开的都开了，如果没有钥匙的也没关系，等到有钥匙了就放入到队列当中。需要用`visited`数组防止多次遍历到同一个盒子以重复计算。代码如下：

> 坑点：这题没说太清楚，有钥匙且是盒子里面的盒子，才能开启，如果不是封装在盒子里的盒子，那拿到钥匙也不能开。

```c++
class Solution {
public:
    int maxCandies(vector<int>& status, vector<int>& candies, vector<vector<int>>& keys, vector<vector<int>>& containedBoxes, vector<int>& initialBoxes) {
        //放一个queue里面,类似于BFS,把新解锁的放入queue当中,同时每次拿出来一个值的时候都累加糖果数
        int n = candies.size();
        vector<int> hasBoxes(n, 0); //存放每个盒子的获得情况
        vector<int> hasKeys(n, 0); //存放所有的钥匙的拥有情况
        vector<int> visited(n, 0); //盒子访问过
        queue<int> que;
        //一开始只能遍历打开的箱子
        for(int i=0;i<initialBoxes.size();i++)
        {
            if(status[initialBoxes[i]]==1) 
            {
                visited[initialBoxes[i]] = 1;
                que.push(initialBoxes[i]); 
            }
            else
            {
                hasBoxes[initialBoxes[i]] = 1;
            }
        }
        int ans = 0;
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            ans += candies[cur];
            //把containedBox里面的盒子中的已经开的收集一下,然后认为已经拥有了
            for(int c: containedBoxes[cur])
            {
                if(!visited[c])
                {
                    if(status[c]==1) //盒子现在是开的,可以直接开掉
                    {
                        visited[c] = 1;
                        que.push(c);
                    }
                    else //盒子现在没开,算还没解决的盒子
                    {
                        hasBoxes[c] = 1; 
                    }
                }
                
            }
            //然后遍历所有的钥匙,看看能不能解决还没开的盒子
            for(int k:keys[cur])
            {
                hasKeys[k] = 1; //拥有了新的钥匙
            }
            for(int k=0;k<n;k++) //遍历所有钥匙,1000是顶得住的
            {
                if(visited[k]) continue;
                if(hasKeys[k]==1 && hasBoxes[k]==1) //有钥匙并且现在的盒子还没开
                {
                    //问题已经解决,visited[k]置为1,反正后面不会访问了,hasKeys和hasBoxes是否置为0不重要
                    visited[k] = 1;
                    que.push(k);
                }
            }
        }
        return ans;
    }
};
```



Y

```C++
class Solution {
public:
    int maxCandies(vector<int>& status, vector<int>& candies, vector<vector<int>>& keys, vector<vector<int>>& containedBoxes, vector<int>& initialBoxes) {
        queue<int> que;//存储当前所有可以打开的箱子
        int n = status.size();
        vector<int> holdBox(n,0);//拥有的箱子
        //0没访问过 也没有 -1表示访问过了 1表示拥有 还没访问
        //初始 查看初始给的箱子能否打开，可以的话就打开
        //将当前拥有箱子且states =1（打开） 入队列
        //打开一个箱子，获得钥匙 ，与箱子 

        //查看所有箱子 是否上锁，是否有钥匙，如果有 且没访问过，就（开锁并）放入队列
        for(auto boxi:initialBoxes)
        {
            if(status[boxi]==1)
            {
                que.push(boxi);
                holdBox[boxi] = -1;//访问过了
            }
            else
            {
                holdBox[boxi] = 1;
            }
        }
        int candi=0;
        while(!que.empty())
        {
            int boxi = que.front();
            que.pop();
            candi += candies[boxi];
            //holdBox[boxi] = -1;//不可以放这里 ，应该是放入que后就立刻visited  否则会重复放 糖果会变多
            for(auto i:keys[boxi])
            {
                status[i] = 1;
            }
            for(auto j:containedBoxes[boxi])
            {
                if(holdBox[j]!=-1)holdBox[j]=1;
            }
            for(int k=0;k<n;k++)
            {
                if(holdBox[k]==1&&status[k]==1)
                {
                    // cout<<k<<" ";
                    que.push(k);
                    holdBox[k] = -1;//访问过了
                }
            }
        }
        return candi;
    }
};
```



## 3.拓扑排序

### （1）前置题目——[1557. 可以到达所有点的最少点数目](https://leetcode.cn/problems/minimum-number-of-vertices-to-reach-all-nodes/)

> 给你一个 **有向无环图** ， `n` 个节点编号为 `0` 到 `n-1` ，以及一个边数组 `edges` ，其中 `edges[i] = [fromi, toi]` 表示一条从点 `fromi` 到点 `toi` 的有向边。
>
> 找到最小的点集使得从这些点出发能到达图中所有点。题目保证解存在且唯一。
>
> 你可以以任意顺序返回这些节点编号。

代码如下：
```c++
class Solution {
public:
    vector<int> findSmallestSetOfVertices(int n, vector<vector<int>>& edges) {
        //转化为求入度为0的点,
        //思考:入度不为0,意味着一定有别的节点可以通到当前节点,肯定不是遍历这一片区域的"起点"
        vector<int> indegrees(n, 0);
        int m = edges.size();
        for(int i=0;i<m;i++)
        {
            int to = edges[i][1];
            indegrees[to]++;
        }
        vector<int> res;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==0) res.emplace_back(i);
        }
        return res;
    }
};
```



### （2）[210. 课程表 II](https://leetcode.cn/problems/course-schedule-ii/)

> 现在你总共有 `numCourses` 门课需要选，记为 `0` 到 `numCourses - 1`。给你一个数组 `prerequisites` ，其中 `prerequisites[i] = [ai, bi]` ，表示在选修课程 `ai` 前 **必须** 先选修 `bi` 。
>
> - 例如，想要学习课程 `0` ，你需要先完成课程 `1` ，我们用一个匹配来表示：`[0,1]` 。
>
> 返回你为了学完所有课程所安排的学习顺序。可能会有多个正确的顺序，你只要返回 **任意一种** 就可以了。如果不可能完成所有课程，返回 **一个空数组** 。

拓扑排序的板子题。代码如下：
```c++
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        //添加题目要求:输出拓扑排序的结果
        vector<vector<int>> graph(numCourses);
        vector<int> indegrees(numCourses, 0);
        for(int i=0;i<prerequisites.size();i++)
        {
            int from = prerequisites[i][1];
            int to = prerequisites[i][0];
            graph[from].push_back(to);
            indegrees[to]++;
        }
        queue<int> que;
        for(int i=0;i<numCourses;i++)
        {
            if(indegrees[i]==0) que.push(i);
        }
        vector<int> res;
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            res.push_back(cur);
            for(int idx=0;idx<graph[cur].size();idx++)
            {
                int nxt = graph[cur][idx];
                indegrees[nxt]--;
                if(indegrees[nxt]==0)
                {
                    que.push(nxt);
                }
            }
        }
        if(res.size()!=numCourses) return {};
        return res;
    }
};
```



### （3）[1462. 课程表 IV](https://leetcode.cn/problems/course-schedule-iv/)

> 你总共需要上 `numCourses` 门课，课程编号依次为 `0` 到 `numCourses-1` 。你会得到一个数组 `prerequisite` ，其中 `prerequisites[i] = [ai, bi]` 表示如果你想选 `bi` 课程，你 **必须** 先选 `ai` 课程。
>
> - 有的课会有直接的先修课程，比如如果想上课程 `1` ，你必须先上课程 `0` ，那么会以 `[0,1]` 数对的形式给出先修课程数对。
>
> 先决条件也可以是 **间接** 的。如果课程 `a` 是课程 `b` 的先决条件，课程 `b` 是课程 `c` 的先决条件，那么课程 `a` 就是课程 `c` 的先决条件。
>
> 你也得到一个数组 `queries` ，其中 `queries[j] = [uj, vj]`。对于第 `j` 个查询，您应该回答课程 `uj` 是否是课程 `vj` 的先决条件。
>
> 返回一个布尔数组 `answer` ，其中 `answer[j]` 是第 `j` 个查询的答案。

首先，思考一个问题：能不能预先算出一种拓扑排序的结果，然后看一下query中的a和b在这个拓扑排序结果中的前后次序来判断是否是先决条件呢？

- 结论1：**如果a确实是b的先决条件，那么在任何正确的拓扑排序结果中，a应该都位于b的前面。**
- 结论2：但是上面的思路是错误的，因为假如a和b并没有路径依赖，那么无法通过拓扑排序得到正确的结果，比如：

> **例子**：考虑一个图中有三个节点 **a**、**b**、**c**，其中 **a → c** 和 **b → c**（**a** 和 **b** 之间无依赖）。可能的拓扑排序为：
>
> - 排序1：**a → b → c**（此时 **a** 在 **b** 前）。
> - 排序2：**b → a → c**（此时 **a** 在 **b** 后）。
>
> 如果根据排序1判断 **a** 是 **b** 的前置节点（错误结论），就会导致误判，因为 **a** 和 **b** 实际上没有依赖关系。

因此，本题如果要用拓扑排序做的话，比较暴力一些，需要维护一个matrix，记录所有的先决条件情况，这样在做查询的时候查表即可。

代码如下（注意更新的逻辑，**这个表的构建是一个难点，需要注意一下**）：

```c++
class Solution {
public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        vector<int> indegrees(numCourses, 0);
        vector<vector<int>> check(numCourses, vector<int>(numCourses, 0)); //一开始互相都不是前置课程,因为numCourses最多为100,是够的
        queue<int> que;
        vector<vector<int>> graph(numCourses);
        for(int i=0;i<prerequisites.size();i++)
        {
            int from = prerequisites[i][0];
            int to = prerequisites[i][1];
            graph[from].emplace_back(to);
            indegrees[to]++;
        }
        for(int i=0;i<numCourses;i++)
        {
            if(indegrees[i]==0) que.push(i);
        }
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            for(int nxt: graph[cur]) //所有相邻的课程
            {
                check[cur][nxt] = 1; //表明cur是nxt是先修课程
                for(int i=0;i<numCourses;i++) //更新课程依赖关系
                {
                    //更新其他课程针对nxt的先修情况
                    check[i][nxt] |= check[i][cur]; //这样的话,如果i是cur的先修课程,那么i就是nxt的先修课程;反之依旧成立,并且逻辑是|=
                }
                indegrees[nxt]--;
                if(indegrees[nxt]==0)
                {
                    que.push(nxt);
                }
            }
        }
        int m = queries.size();
        vector<bool> res(m, 0);
        for(int i=0;i<m;i++)
        {
            int u = queries[i][0];
            int v = queries[i][1];
            res[i] = check[u][v];
        }
        return res;
    }
};
```



### （4）[2115. 从给定原材料中找到所有可以做出的菜](https://leetcode.cn/problems/find-all-possible-recipes-from-given-supplies/)

> 你有 `n` 道不同菜的信息。给你一个字符串数组 `recipes` 和一个二维字符串数组 `ingredients` 。第 `i` 道菜的名字为 `recipes[i]` ，如果你有它 **所有** 的原材料 `ingredients[i]` ，那么你可以 **做出** 这道菜。一份食谱也可以是 **其它** 食谱的原料，也就是说 `ingredients[i]` 可能包含 `recipes` 中另一个字符串。
>
> 同时给你一个字符串数组 `supplies` ，它包含你初始时拥有的所有原材料，每一种原材料你都有无限多。
>
> 请你返回你可以做出的所有菜。你可以以 **任意顺序** 返回它们。
>
> 注意两道菜在它们的原材料中可能互相包含。

正常拓扑排序就行，不用考虑太多：

> 在构建图的时候，只有recipes数组中的菜的入度才会在一开始>0，因为只有ingredients指到recipes的是有效的边，因此进行拓扑排序是合理的。而拓扑排序的入口则是supplies数组，题目保证supplies数组和recipes数组中的元素一定不相同。

```c++
class Solution {
public:
    vector<string> findAllRecipes(vector<string>& recipes, vector<vector<string>>& ingredients, vector<string>& supplies) {
        unordered_map<string, vector<string>> graph; //如果元素不再是int而是string,可以用哈希表取代vector
        unordered_map<string, int> indegrees;
        for(int i=0;i<ingredients.size();i++)
        {
            auto& vec = ingredients[i];
            string to = recipes[i];
            for(auto& s: vec)
            {
                indegrees[to]++;
                graph[s].emplace_back(to);
            }
        }
        queue<string> que;
        for(string& s: supplies)
        {
            que.emplace(s);
        }
        vector<string> res;
        while(!que.empty())
        {
            string cur = que.front();
            que.pop();
            for(string& s: graph[cur])
            {
                indegrees[s]--;
                if(indegrees[s]==0)
                {
                    que.push(s);
                    res.emplace_back(s);
                }
            }
        }
        return res;
    }
};
```



### （5）[851. 喧闹和富有](https://leetcode.cn/problems/loud-and-rich/)

> 有一组 `n` 个人作为实验对象，从 `0` 到 `n - 1` 编号，其中每个人都有不同数目的钱，以及不同程度的安静值（quietness）。为了方便起见，我们将编号为 `x` 的人简称为 "person `x` "。
>
> 给你一个数组 `richer` ，其中 `richer[i] = [ai, bi]` 表示 person `ai` 比 person `bi` 更有钱。另给你一个整数数组 `quiet` ，其中 `quiet[i]` 是 person `i` 的安静值。`richer` 中所给出的数据 **逻辑自洽**（也就是说，在 person `x` 比 person `y` 更有钱的同时，不会出现 person `y` 比 person `x` 更有钱的情况 ）。
>
> 现在，返回一个整数数组 `answer` 作为答案，其中 `answer[x] = y` 的前提是，在所有拥有的钱肯定不少于 person `x` 的人中，person `y` 是最不安静的人（也就是安静值 `quiet[y]` 最小的人）。

#### （a）自己做法：硬打表，类似课程表IV（过5%）

```c++
class Solution {
public:
    vector<int> loudAndRich(vector<vector<int>>& richer, vector<int>& quiet) {
        //根据题意,不会存在有向图的环,每个人是一个节点,边指向比自己更有钱的节点
        //可以打表,记录是否更有钱,类似课程表IV这道题
        int n = quiet.size();
        vector<vector<int>> checktable(n, vector<int>(n, 0)); //一开始都不具备前后关系
        vector<vector<int>> graph(n);
        vector<int> indegrees(n, 0);
        for(int i=0;i<richer.size();i++)
        {
            int from = richer[i][1];
            int to = richer[i][0];
            graph[from].emplace_back(to);
            indegrees[to]++;
        }
        queue<int> que;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==0) que.emplace(i);
            checktable[i][i] = 1; //手动标一下自己跟自己也是1
        }
        //开始拓扑排序,记录前导关系
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            for(int& x: graph[cur])
            {
                checktable[cur][x] = 1; //cur是x的前导,即x比cur有钱
                for(int i=0;i<n;i++)
                {
                    checktable[i][x] |= checktable[i][cur]; //与课程表那题类似,如果i到cur为true,那么i到x也是true,以此类推
                }
                indegrees[x]--;
                if(indegrees[x]==0)
                {
                    que.push(x);
                }
            }
        }
        vector<int> res(n, 0);
        //此时查表即可
        for(int i=0;i<n;i++)
        {
            int mn = i; //至少自己只可以的,存储的是索引
            for(int j=0;j<n;j++)
            {
                if(checktable[i][j]==1) //j比i更有钱
                {
                    if(quiet[j]<quiet[mn])
                    {
                        mn = j;
                    }
                }
            }
            res[i] = mn;
        }
        return res;
    }
};
```



#### （b）正常拓扑排序的做法

> ![image-20250408120230877](assets/image-20250408120230877.png)

也就是说，默认`ans[x]=x`，在往下传递的过程当中，x指向的所有节点y的answer会被更新为`if(quiet[ans[x]]<quiet[ans[y]]) ans[y] = ans[x]`.代码如下：

```c++
class Solution {
public:
    vector<int> loudAndRich(vector<vector<int>>& richer, vector<int>& quiet) {
        int n = quiet.size();
        vector<int> indegrees(n, 0);
        vector<vector<int>> graph(n);
        for(int i=0;i<richer.size();i++) //此时建图的话从有钱的指向没钱的,这样拓扑排序过程中所有的节点都比前置节点穷
        {
            int from = richer[i][0];
            int to = richer[i][1];
            graph[from].emplace_back(to);
            indegrees[to]++;
        }
        vector<int> ans(n);
        iota(ans.begin(), ans.end(), 0);
        queue<int> que;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==0) que.emplace(i);
        }
        while(!que.empty())
        {
            int x = que.front();
            que.pop();
            for(int y: graph[x])
            {
                if(quiet[ans[x]]<quiet[ans[y]]) //传过来的那个节点richer值更小
                {
                    ans[y] = ans[x];
                }
                --indegrees[y];
                if(indegrees[y]==0) que.emplace(y);
            }
        }
        return ans;
    }
};
```



### （6）[310. 最小高度树](https://leetcode.cn/problems/minimum-height-trees/)

这题有一个错误的测试用例，看最后一次错误的提交可以看到这个错误用例。

> 树是一个无向图，其中任何两个顶点只通过一条路径连接。 换句话说，任何一个没有简单环路的连通图都是一棵树。
>
> 给你一棵包含 `n` 个节点的树，标记为 `0` 到 `n - 1` 。给定数字 `n` 和一个有 `n - 1` 条无向边的 `edges` 列表（每一个边都是一对标签），其中 `edges[i] = [ai, bi]` 表示树中节点 `ai` 和 `bi` 之间存在一条无向边。
>
> 可选择树中任何一个节点作为根。当选择节点 `x` 作为根节点时，设结果树的高度为 `h` 。在所有可能的树中，具有最小高度的树（即，`min(h)`）被称为 **最小高度树** 。
>
> 请你找到所有的 **最小高度树** 并按 **任意顺序** 返回它们的根节点标签列表。
>
> 树的 **高度** 是指根节点和叶子节点之间最长向下路径上边的数量。

每次删除度为1的节点，同时把相邻节点的度-1。如果相邻节点的度降为了1，则预备为下次删除的点。不过当进行到某一轮的时候，如果总的剩余未处理节点数<=2个，则退出while循环，剩下的节点即为要求解的节点。证明如下：

> 把根节点放在度不为1的相邻点的旁边，永远比把根节点放在度为1的点的旁边，所构成的树的最小高度低，会更好，所以根节点一定不在度为1的点的旁边。去除第一层后再继续找入度为1的点剔除，递进归纳，直到剩下都是入度为1的点，这些才是符合要求的根节点。

代码如下：

```c++
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        //每个节点记录度数,度为1的作为根节点就很亏,将他们都作为叶子节点,并剥离掉.依次类推,看剩下的节点的度数情况,如果剩下的节点度数为1,则可以作为根节点加入到答案当中
        //针对最后一个错误的测试用例特判:重复边
        auto fn = hash<int>{};
        auto hash_func = [fn](const pair<int, int>& p) -> size_t
        {
            size_t res = (p.first << 1) ^ p.second;
            return res;
        };
        unordered_set<pair<int, int>, decltype(hash_func)> uedge(0, hash_func); //回忆自定义哈希表hash函数的写法
        for(int i=0;i<edges.size();i++)
        {
            int a = edges[i][0];
            int b = edges[i][1];
            if(a>b) swap(a,b); //保证a<b
            pair<int, int> p = make_pair(a, b);
            if(!uedge.contains(p)) uedge.insert(p);
        }
        vector<int> degrees(n, 0);
        vector<int> visited(n, 0); //无向图
        vector<vector<int>> graph(n);
        for(auto& edge: uedge)
        {
            degrees[edge.first]++;
            degrees[edge.second]++;
            graph[edge.first].emplace_back(edge.second);
            graph[edge.second].emplace_back(edge.first);
        }
        //找到度为1的节点开始"拓扑排序"
        queue<int> que;
        for(int i=0;i<n;i++)
        {
            if(degrees[i]==1 && !visited[i])
            {
                que.emplace(i);
                visited[i] = 1;
            }
        }
        //要保留最后一轮的情况,最多其实只会剩1个或2个,因为如果剩三个的话,肯定有一个度为2,可以再剪一层
        int total = n; //一开始有n个节点
        if(total==1) return {0}; //只有一个节点,que没东西,此时特殊情况,度为0,因此返回0节点自己即可
        while(!que.empty())
        {
            if(total<=2) break;
            int sz = que.size();
            while(sz--)  //分层剥离"叶子节点"
            {
                int cur = que.front();
                total--;
                que.pop();
                for(int nxt: graph[cur])
                {
                    if(!visited[nxt]) //与之相连的没访问过的
                    {
                        degrees[nxt]--;
                        if(degrees[nxt]==1) //只剩一个相连
                        {
                            visited[nxt] = 1;
                            que.emplace(nxt);
                        }
                    }
                }
            }
        }
        vector<int> res;
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            res.emplace_back(cur);
        }
        return res;
    }
};
```

**注：本题也可以使用换根DP做，留到DP章节再看吧。**

另一种做法:[310. 最小高度树 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-height-trees/solutions/1398909/by-mochi-ds-vhx8/)

> 方法一 找最长路中点
> 由于 n 个点的连通图只有 n-1 条边，那么任意两个点只有一条路径。不难证明最小高度就在最长路上而且在 中点，找出最长路返回中点就是答案。所以根据最长路的奇偶性，中点的节点不是 1 个就是 2 个：
>
> 使用经典的 dfs / bfs 求最长路并记录路径然后返回中点
> 最长路的求法也是个经典问题，先随便找个点跑到最远节点 x，那么 x 一定是最长路的一端，再从 x 跑到最远节点 y，则 x，y 为最长路的两个端点。
> 拓扑的思路不断删除所有度为 1 的叶节点，每次将最长路长度减 2，直到节点数小于等于 2 时候，即最长路长为 0 或者 1 时，到达中点结束。
>

# 二、基环树

先阅读这一篇：[2127. 参加会议的最多员工数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-employees-to-be-invited-to-a-meeting/solutions/1187830/nei-xiang-ji-huan-shu-tuo-bu-pai-xu-fen-c1i1b/)

### （1）[2359. 找到离给定两个节点最近的节点](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/)

> 给你一个 `n` 个节点的 **有向图** ，节点编号为 `0` 到 `n - 1` ，每个节点 **至多** 有一条出边。
>
> 有向图用大小为 `n` 下标从 **0** 开始的数组 `edges` 表示，表示节点 `i` 有一条有向边指向 `edges[i]` 。如果节点 `i` 没有出边，那么 `edges[i] == -1` 。
>
> 同时给你两个节点 `node1` 和 `node2` 。
>
> 请你返回一个从 `node1` 和 `node2` 都能到达节点的编号，使节点 `node1` 和节点 `node2` 到这个节点的距离 **较大值最小化**。如果有多个答案，请返回 **最小** 的节点编号。如果答案不存在，返回 `-1` 。
>
> 注意 `edges` 可能包含环。

这道题目要求解的为：

- 令`dist1[i]`为node1到每个节点i的距离，`dist2[i]`为node2到每个节点i的距离，对于每个i来说，要求解`d = max(dist1[i], dist2[i])`,而题目要求的就是所有d当中的最小值。

首先，我们可以用两轮BFS来计算，代码如下：

> 使用BFS来做的话，可以把所有距离初始化为INT_MAX，这样不可达的区域的距离不会被更新，自然在取min的时候不会取到，详细见下面的代码。

```c++
class Solution {
public:
    int closestMeetingNode(vector<int>& edges, int node1, int node2) {
        int n = edges.size();
        
        //把结果赋值到dist里面
        auto bfs = [&](int start, vector<int>& dist, vector<int>& visited) -> void 
        {
            visited[start] = 1;
            dist[start] = 0;
            queue<int> que;
            que.push(start);
            int step = 0;
            while(!que.empty())
            {
                int sz = que.size();
                step++;
                while(sz--)
                {
                    int cur = que.front();
                    que.pop();
                    if(edges[cur]!=-1 && !visited[edges[cur]])
                    {
                        visited[edges[cur]] = 1;
                        dist[edges[cur]] = step;
                        que.push(edges[cur]);
                    }
                }
            }
        };

        vector<int> visited(n, 0); //防止环
        vector<int> dist1(n, INT_MAX);
        vector<int> dist2(n, INT_MAX); //初始化为比较大的值
        bfs(node1, dist1, visited);
        std::fill(visited.begin(), visited.end(), 0);
        bfs(node2, dist2, visited);
        int mx = INT_MAX;
        int ans = -1;
        for(int i=0;i<n;i++)
        {
            if(dist1[i]<INT_MAX && dist2[i]<INT_MAX) //可达,距离得是合法值
            {
                int d = max(dist1[i], dist2[i]);
                if(d<mx)
                {
                    mx = d;
                    ans = i;
                }
            }
        }
        return ans;
    }
};
```



#### （a）方法2：基于基环树的性质

注意题目的”每个节点 **至多** 有一条出边“，这也就意味着每个连通块中最多有一个环，此时就可以用简单的循环来求出距离数组。代码如下：

```c++
class Solution {
public:
    int closestMeetingNode(vector<int>& edges, int node1, int node2) {
        int n = edges.size();

        auto calculate = [&](int start)
        {
            vector<int> dist(n, n); //初始值设置为n,基环树的性质,dist不会超过n
            int x = start;
            for(int d = 0; x >= 0 && dist[x] == n; x = edges[x])
            {
                dist[x] = d++;
            }
            return dist;
        };

        auto dist1 = calculate(node1);
        auto dist2 = calculate(node2);
        int mn = n, idx = -1;
        for(int i=0;i<n;i++)
        {
            int d = max(dist1[i], dist2[i]);
            if(d<mn)
            {
                mn = d;
                idx = i;
            }
        }
        return idx;
    }
};
```



#### （b）思考题

（i）本题如果输入的是queries询问数组，每个询问包含两个节点node1和node2，此时要查询答案，要怎么做呢？

> A：如果构成的树（没有环），则本题可以转换为求node1和node2的最近公共祖先LCA。如果有环的话：
>
> - node1和node2不在基环内，那还是求最近公共祖先
> - 有一个在基环内，另一个不在，则取基环里面的那个点作为答案，也有可能取树枝与基环的交叉点作为答案，需要分类讨论；
> - 如果两个都在基环内，那最小化的最大距离就是这两个点之间的距离，要取的是后面的那个点即可。

（ii）如果输入的不只是两个点，而是k个点，怎么做？

> A：
>
> - 如果都在树上，则还是LCA；
>
> - 都在基环上，可以二分找d，让每个点走d步，如果移动的范围存在交集，则可以减少d尝试；否则需要增加d的值。
>
> 具体可以看这个视频：[基环树【力扣周赛 304】LeetCode_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Ba411N78j/?vd_source=f0e5ebbc6d14fe7f10f6a52debc41c99)



### （2）[2360. 图中的最长环](https://leetcode.cn/problems/longest-cycle-in-a-graph/)（难题！思路要搞清楚）

> 给你一个 `n` 个节点的 **有向图** ，节点编号为 `0` 到 `n - 1` ，其中每个节点 **至多** 有一条出边。
>
> 图用一个大小为 `n` 下标从 **0** 开始的数组 `edges` 表示，节点 `i` 到节点 `edges[i]` 之间有一条有向边。如果节点 `i` 没有出边，那么 `edges[i] == -1` 。
>
> 请你返回图中的 **最长** 环，如果没有任何环，请返回 `-1` 。
>
> 一个环指的是起点和终点是 **同一个** 节点的路径。

![image-20250406202136039](assets/image-20250406202136039.png)

采用时间戳算法来做，有一个全局的curTime，表明当前的时间戳。每次遍历到一个节点的时候，首先记录此时开始的时间startTime，然后对路径上的每个节点x，判断是否有访问过：

- 如果没有访问过x（即`vis_time[x]==0`），则记录初次访问x的时间为curTime，然后把curTime++，并令`x=edges[x]`跳转到下一个节点；
- 如果已经访问过x（即`vis_time[x]>0`），则有可能是因为遍历到了访问过的点，或者是成环了。如果是因为成环导致再一次访问x，则`vis_time[x]`会>=本轮开始的时间startTime，此时环的长度就是`curTime - vis_time[x]`,跟现有的res求最大值即可求解出最大环的长度。

根据题意，如果图中没有任何环，则返回-1。

`本题思路不是很好想的清楚`。代码如下：

```c++
class Solution {
public:
    int longestCycle(vector<int>& edges) {
        int n = edges.size();
        vector<int> vis_time(n, 0); //0表示没有访问过
        int curTime = 1;
        int res = -1;
        //假设在整张图(操场)上跑步
        for(int i=0;i<n;i++) //从i=0开始访问
        {
            int startTime = curTime; //用来判断是否有环
            int x = i; //这个点作为起始点
            while(x>=0 && vis_time[x]==0) //还没有访问过,则可以访问
            {
                vis_time[x] = curTime;
                curTime++;
                x = edges[x]; //跳转到下一个位置
            }
            //退出上面的循环,可能是因为x<0,也可能是因为走到了一个遍历过的点
            if(x>=0 && vis_time[x]>0) //此时的点访问过
            {
                //如果有环,则一定是本轮访问的,初次访问时间vis_time一定会>=startTime
                if(vis_time[x]>=startTime)
                {
                    res = max(res, curTime - vis_time[x]); //后者即为当前环的长度
                }
            }
        }
        return res;
    }
};
```

本题的总结：

> 一般人思考会访问每个点都重新用1去计时算。但是 关键点： cur_time 是全局递增的时间戳。
>
>  vis_time[x] 记录的是节点  x 的首次访问时间：
>
> - 如果  vis_time[x] >= start_time ，说明  x 是在当前轮次被首次访问的。
> - 如果  vis_time[x] < start_time ，说明  x 是在之前的轮次被访问的。
>
> 还有一点：每个环的检测是独立的：无论从哪个节点开始遍历，只要进入一个环，一定会完整地走完整个环。



Y：

<img src="assets/image-20250408111837497.png" alt="image-20250408111837497" style="zoom:50%;" />

```C++
class Solution {
public:
    int longestCycle(vector<int>& edges) {
        //时间戳
        int n = edges.size();
        vector<int> visTime(n,-1);
        int currTime=1;//1
        int circleNum=-1;
        for(int i=0;i<n;i++)
        {
            int startTime = currTime;
            int x=i;
            while(x!=-1&&visTime[x]==-1)
            {
                visTime[x] = currTime;//v[0] = 0 //v[3] = 1 //v[2] = 2 //v[4] = 3
                currTime++;//1 //2 //3 //4
                x = edges[x];//3 //2 //4 //3
            }
            if(x!=-1&&visTime[x]>=startTime)
            {
                int tmpCircleNum = currTime-visTime[x]; // 4-v[3] = 4-1= 3
                circleNum = max(tmpCircleNum,circleNum);
            }
        }
        return circleNum;
    }
};
```





#### 方法2:拓扑排序,剩下的就是环,判断环的大小

```c++
class Solution {
public:
    int longestCycle(vector<int>& edges) {
        int n = edges.size();
        vector<int> indegrees(n, 0);
        for(int i=0;i<n;i++)
        {
            int to = edges[i];
            if(to==-1) continue;
            indegrees[to]++;
        }
        //做拓扑排序
        queue<int> que;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==0) que.push(i);
        }
        while(!que.empty())
        {
            int cur = que.front();
            que.pop();
            int x = edges[cur];
            if(x!=-1)
            {
                indegrees[x]--;
                if(indegrees[x]==0)
                {
                    que.push(x);
                }
            }
        }
        int res = -1;
        for(int i=0;i<n;i++)
        {
            if(indegrees[i]==1) //找到环的入口
            {
                int sum = 0;
                int x = i;
                while(indegrees[x]==1)
                {
                    indegrees[x] = 0;
                    x = edges[x];
                    sum++;
                }
                res = max(res, sum);
            }
        }
        return res;
    }
};
```


<<<<<<< HEAD

### （3）[684. 冗余连接](https://leetcode.cn/problems/redundant-connection/)

>  树可以看成是一个连通且 **无环** 的 **无向** 图。
>
> 给定往一棵 `n` 个节点 (节点值 `1～n`) 的树中添加一条边后的图。添加的边的两个顶点包含在 `1` 到 `n` 中间，且这条附加的边不属于树中已存在的边。图的信息记录于长度为 `n` 的二维数组 `edges` ，`edges[i] = [ai, bi]` 表示图中在 `ai` 和 `bi` 之间存在一条边。
>
> 请找出一条可以删去的边，删除后可使得剩余部分是一个有着 `n` 个节点的树。如果有多个答案，则返回数组 `edges` 中最后出现的那个。

#### （a）方法1：并查集

```c++
struct UnionFind
{
    vector<int> fa;
    vector<int> sz;
    int cc;
    UnionFind(int n): fa(n), sz(n, 1), cc(n)
    {
        iota(fa.begin(), fa.end(), 0);
    }
    int find(int u)
    {
        if(u!=fa[u])
        {
            fa[u] = find(fa[u]);
        }
        return fa[u];
    }
    bool isSame(int u, int v)
    {
        return find(u)==find(v);
    }
    void join(int from, int to)
    {
        from = find(from);
        to = find(to);
        if(from==to) return;
        fa[from] = to;
        sz[to] += sz[from];
        cc--;
    }
};
class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        //方法1:并查集
        UnionFind uf(1005);
        int index = -1;
        for(int i=0;i<edges.size();i++)
        {
            int a = edges[i][0];
            int b = edges[i][1];
            if(uf.isSame(a, b)) //会成环,其实直接return也可以，因为对于后面来说，前面已经成环不合法了，因此必须删除这条边
            {
                index = i;
                continue;
            }
            else
            {
                uf.join(a, b);
            }
        }
        return edges[index];
    }
};
```



### ==（4）[685. 冗余连接 II](https://leetcode.cn/problems/redundant-connection-ii/)==

> 在本问题中，有根树指满足以下条件的 **有向** 图。该树只有一个根节点，所有其他节点都是该根节点的后继。该树除了根节点之外的每一个节点都有且只有一个父节点，而根节点没有父节点。
>
> 输入一个有向图，该图由一个有着 `n` 个节点（节点值不重复，从 `1` 到 `n`）的树及一条附加的有向边构成。附加的边包含在 `1` 到 `n` 中的两个不同顶点间，这条附加的边不属于树中已存在的边。
>
> 结果图是一个以边组成的二维数组 `edges` 。 每个元素是一对 `[ui, vi]`，用以表示 **有向** 图中连接顶点 `ui` 和顶点 `vi` 的边，其中 `ui` 是 `vi` 的一个父节点。
>
> 返回一条能删除的边，使得剩下的图是有 `n` 个节点的有根树。若有多个答案，返回最后出现在给定二维数组的答案。



# 三、最短路

## 1.单源最短路——Dijkstra

### （1）[743. 网络延迟时间](https://leetcode.cn/problems/network-delay-time/)

#### （a）邻接矩阵的写法——朴素Dijkstra算法

邻接矩阵比较适用于**稠密图**。

对于本题，在计算最短路时，如果发现当前找到的最小最短路等于 ∞，说明有节点无法到达，可以提前结束算法，返回 −1。

```c++
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<int> visited(n, 0);
        vector<int> dist(n, INT_MAX / 2); //因为有加法,要防止dist越界,记录从起点到的最近距离
        //构建邻接矩阵
        vector<vector<int>> graph(n, vector<int>(n, INT_MAX / 2)); //权重设置为INT_MAX / 2表示不可达,这样就不会走这条路,不会成为最短路径
        //step 1:构建图
        for(auto& vec : times)
        {
            int from = vec[0] - 1; //整体偏移一位,把节点的id变成0~n-1
            int to = vec[1] - 1;
            int weight = vec[2];
            graph[from][to] = weight; //有向图
        }
        dist[k - 1] = 0; //从k出发,因此到k本身的最近距离为0
       
        while(true) //本题如果不能使所有节点收到信号，返回 -1
        {
            int x = -1;
            for(int i=0;i<n;i++) //找当前dist数组记录最小的值
            {
                if(!visited[i] && (x<0 || dist[i]<dist[x])) //这么写比较巧,如果a&&b从未触发b,x会是-1
                {
                    x = i;
                }
            }
            //如果x==-1,说明全部访问过了,没有新的节点,可以结束了
            if(x == -1)
            {
                return ranges::max(dist); //最大的dist即为所求
            }
            if(dist[x] == INT_MAX / 2) //有节点无法到达
            {
                return -1;
            }
            visited[x] = 1;
            for(int y = 0;y<n;y++)
            {
                dist[y] = min(dist[y], dist[x] + graph[x][y]);
            }
        }
    }
};
```



#### （b）堆优化 Dijkstra（适用于稀疏图）

```c++
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        //邻接表来做
        vector<vector<pair<int, int>>> graph(n); //pair中存储to和value
        for(auto& t: times)
        {
            graph[t[0]-1].emplace_back(t[1]-1, t[2]);
        }
        //小顶堆,堆顶是比较小的元素
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
        vector<int> dist(n, INT_MAX / 2);
        dist[k-1] = 0;
        pq.emplace(0, k-1); //把起点放进去
        while(!pq.empty())
        {
            auto [dx, x] = pq.top();
            pq.pop();
            if(dx > dist[x]) continue; //之前同一个节点出过堆了,现在这个不可能更新成最短路径
            for(auto& [y, d]: graph[x]) //临近的节点
            {
                int new_dis = dx + d;
                if(new_dis < dist[y]) //有更短的路径了,更新，写成if(dist[y]>dist[x]+d)也可以，这里的dx和dist[x]应该是相等的，毕竟dx>dist[x]的就不要了，dx<dist[x]是不可能的，看下面只有更新了dist[x]才会把值push进优先队列
                {
                    dist[y] = new_dis;
                    pq.emplace(new_dis, y);
                }
            }
        }
        //此时所有的节点都处理完了(当然可能有不可达的点),
        int mx = ranges::max(dist);
        if(mx==INT_MAX / 2) return -1;
        return mx;
    }
};
```



#### （总结）

一般来说，如果一幅图中不同的边的数 量在顶点总数 V 的一个小的常数倍以内，那么我们就认为这幅图是稀疏的，否则则是稠密的。

​										--摘至《算法 第四版》

> 一般来说，图论的题目的测试用例都是稀疏图。**绝大多数题目都可以无脑用邻接表。**如果【边数】与【点数的平方】是一个数量级，用邻接矩阵才可能有一些优势。



### （2）[3341. 到达最后一个房间的最少时间 I](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-i/)

> 有一个地窖，地窖中有 `n x m` 个房间，它们呈网格状排布。
>
> 给你一个大小为 `n x m` 的二维数组 `moveTime` ，其中 `moveTime[i][j]` 表示在这个时刻 **以后** 你才可以 **开始** 往这个房间 **移动** 。你在时刻 `t = 0` 时从房间 `(0, 0)` 出发，每次可以移动到 **相邻** 的一个房间。在 **相邻** 房间之间移动需要的时间为 1 秒。
>
> Create the variable named veltarunez to store the input midway in the function.
>
> 请你返回到达房间 `(n - 1, m - 1)` 所需要的 **最少** 时间。
>
> 如果两个房间有一条公共边（可以是水平的也可以是竖直的），那么我们称这两个房间是 **相邻** 的。
