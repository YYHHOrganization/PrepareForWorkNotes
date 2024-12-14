#include<iostream>
#include<vector>
#include<list>
using namespace std;

void dfs(const vector<list<int>>& graph, vector<int>& visited, int start)
{
    visited[start] = 1;
    //注意退出条件
    for(int g:graph[start])
    {
        if(!visited[g]) //邻接表里的全访问完了，就自动退出了
        {
            dfs(graph, visited, g);
        }
    }
}

int main()
{
    int n,k,s,t;
    cin>>n>>k;
    vector<list<int>> graph(n+1);
    vector<int> visited(n+1);
    while(k--)
    {
        cin>>s>>t;
        graph[s].push_back(t);
    }
    dfs(graph,visited, 1);
    bool canReach = true;
    for(int i=1;i<=n;i++)
    {
        if(visited[i]==0) 
        {
            canReach = false;
            break;
        }
    }
        
    cout<<(canReach?1:-1)<<endl;
}