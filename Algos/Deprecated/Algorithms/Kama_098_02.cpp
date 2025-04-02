#include <iostream>
#include <vector>
#include <list>
using namespace std;

vector<vector<int>> results;
vector<int> path;

void dfs(const vector<list<int>>& graph, int x, int n) //x为当前的，n为终点
{
    if(x==n)
    {
        results.push_back(path);
        return;
    }
    for(int i:graph[x])
    {
        path.push_back(i);
        dfs(graph, i, n);
        path.pop_back();
    }
}

int main()
{
    int n,m,s,t; //n个节点，m条边
    cin>>n>>m;
    vector<list<int>> graph(n+1); //注意邻接表的写法
    while(m--)
    {
        cin>>s>>t;
        graph[s].push_back(t); //邻接表的读入
    }
    path.push_back(1);
    dfs(graph, 1, n);
    //输出结果
    if (results.size() == 0) cout << -1 << endl;
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