#include <iostream>
#include <vector>
using namespace std;

vector<vector<int> > results;
vector<int> path;

void dfs(const vector<vector<int>>& graph, int x, int n) //x是当前节点，n是终点
{
    //先记得写退出条件,找到终点了
    if(x == n)
    {
        results.emplace_back(path);
        return;
    }
    for(int i=1;i<=n;i++) //遍历所有与x相邻的边
    {
        if(graph[x][i] == 1)
        {
            //回溯dfs的经典写法
            path.push_back(i);
            dfs(graph, i, n);
            path.pop_back();
        }
    }
}

int main()
{
    int n,m,s,t;
    cin>>n>>m; //n个节点，m条边
    vector<vector<int> > graph(n+1, vector<int>(n+1, 0)); //临界矩阵,注意写法
    while(m--)
    {
        cin>>s>>t;
        graph[s][t] = 1; //有向图
    }
    path.push_back(1); //从1节点出发
    dfs(graph, 1, n);

    if(results.size()==0) cout<<"-1"<<endl;
    //开始打印结果
    for(const vector<int>& res: results)
    {
        for(int i=0;i<res.size()-1;i++)
        {
            cout<<res[i]<<" ";
        }
        cout<<res[res.size()-1]<<endl;
    }

    return 0;
}