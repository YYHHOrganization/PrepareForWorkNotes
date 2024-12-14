#include<vector>
#include<list>
#include<iostream>
#include<vector>
#include<queue>
#include<unordered_set>
using namespace std;

int main()
{
    int n,k,s,t;
    cin>>n>>k; //n节点，k边
    vector<list<int>> graph(n+1); //边索引从1开始，所以n+1
    //构建图
    while(k--)
    {
        cin>>s>>t;
        graph[s].push_back(t);
    }
    //开始bfs
    queue<int> que;
    vector<int> visited(n+1); //这个点是否被访问过
    que.push(1);
    visited[1]=1;
    while(!que.empty())
    {
        int index = que.front();
        que.pop();
        for(int g:graph[index])
        {
            if(!visited[g])
            {
                que.push(g);
                visited[g] = 1;
            }
        }
    }
    bool canReach = true;
    for(int i=1;i<=n;i++)
    {
        if(visited[i]==0) canReach = false;
    }
    cout<<(canReach?1:-1)<<endl;
}