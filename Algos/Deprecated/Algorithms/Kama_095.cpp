#include<iostream>
#include<queue>
#include<vector>
#include<climits>
#include<list>
using namespace std;

struct Edge
{
    int end;
    int weight;
    Edge(int end, int weight): end(end), weight(weight){}
};

int main()
{
    int n,m,s,t,v;
    cin>>n>>m;
    vector<list<Edge>> graph(n+1); //邻接表
    while(m--)
    {
        cin>>s>>t>>v;
        graph[s].push_back(Edge(t,v));
    }
    int start = 1;
    int end = n; 
    vector<int> minDist(n+1, INT_MAX);
    vector<int> isInQueue(n+1, 0);
    vector<int> cnt(n+1, 0); //记录每个节点入队了多少次,超过n-1次说明有负环回路
    queue<int> que;
    minDist[start] = 0;
    que.push(start);
    cnt[start] = 1; //进入队列一次
    //开始SPFA松弛操作
    bool flag = false; //是否出现了负权环
    while(!que.empty())
    {
        int cur = que.front();
        que.pop();
        isInQueue[cur] = 0; //拿出来,松弛相邻边
        for(Edge& e: graph[cur])
        {
            //松弛的原则：如果到当前的更小，就更新
            int to = e.end;
            int weight = e.weight;
            if(minDist[to]>minDist[cur] + weight)
            {
                minDist[to] = minDist[cur] + weight;
                //push进来
                que.push(to);
                isInQueue[to] = 1;
                cnt[to]++;
                //如果出现了cnt==n的情况，说明出现了负权回路
                if(cnt[to]==n)
                {
                    flag = true;
                    //把队列全pop出来
                    while(!que.empty()) que.pop();
                    break;
                }
            }
        }
    }
    if(flag) cout<<"circle"<<endl;
    else if(minDist[end]==INT_MAX) cout<<"unconnected"<<endl;
    else cout<<minDist[end]<<endl;
    return 0;
}