#include<vector>
#include<queue>
#include<list>
#include<iostream>
#include<climits>
using namespace std;

struct Edge
{
    int to;
    int weight;
    Edge(int to, int weight): to(to), weight(weight){}
};

int main()
{
    int n,m,s,t,v;
    cin>>n>>m;
    vector<list<Edge>> graph(n+1);
    while(m--)
    {
        cin>>s>>t>>v;
        graph[s].push_back(Edge(t, v));
    }
    vector<int> minDist(n+1, INT_MAX);
    vector<int> oldMinDist(n+1, INT_MAX);
    queue<int> que;
    int start, end, k;
    cin>>start>>end>>k;
    minDist[start]=0;
    que.push(start);
    k++;
    int queSize = 0; //记录每轮que.size() 
    while(!que.empty() && k--) //一共k+1轮
    {
        vector<int> visited(n+1, 0); //记录是否这轮已经访问过了
        oldMinDist = minDist; //old是上一轮的
        queSize = que.size();
        while(queSize--)  //只能pop出来queSize的东西
        {
            int cur = que.front();
            que.pop();
            for(Edge& e: graph[cur])  //遍历所有的相邻边，然后松弛，被更新的加入队列，但注意比较的是上一次的
            {
                if(minDist[e.to] > oldMinDist[cur] + e.weight)
                {
                    minDist[e.to] = oldMinDist[cur] + e.weight;
                    if(!visited[e.to])
                    {
                        que.push(e.to);
                        visited[e.to] = 1;
                    }
                    
                }
            }
        }
    }
    if(minDist[end]==INT_MAX) cout<<"unreachable"<<endl;
    else cout<<minDist[end]<<endl;

    return 0;
}