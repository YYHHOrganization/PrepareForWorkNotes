# Leetcode——图论专题

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
        //有向图,没有环的话,可以不用visited数组
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
            int fa = uf.find(i);
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
                minRes = min(minRes, graph[start][index].second);
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
                res.resize(n);
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



### （7）[2192. 有向无环图中一个节点的所有祖先](https://leetcode.cn/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/)

> 给你一个正整数 `n` ，它表示一个 **有向无环图** 中节点的数目，节点编号为 `0` 到 `n - 1` （包括两者）。
>
> 给你一个二维整数数组 `edges` ，其中 `edges[i] = [fromi, toi]` 表示图中一条从 `fromi` 到 `toi` 的单向边。
>
> 请你返回一个数组 `answer`，其中 `answer[i]`是第 `i` 个节点的所有 **祖先** ，这些祖先节点 **升序** 排序。
>
> 如果 `u` 通过一系列边，能够到达 `v` ，那么我们称节点 `u` 是节点 `v` 的 **祖先** 节点。