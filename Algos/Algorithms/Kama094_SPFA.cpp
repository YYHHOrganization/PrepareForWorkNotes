#include<queue>
#include<vector>
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
    //SPFA,要存储边的关系了
    int n,m,s,t,v;
    cin>>n>>m;
    vector<list<Edge>> graph(n+1);
    vector<int> minDist(n+1, INT_MAX);
    while(m--)
    {
        cin>>s>>t>>v;
        graph[s].push_back({t,v});
    }
    int start = 1;
    int end = n;
    minDist[start] = 0;// 同样,minDist记录起点到index点的最小距离
    queue<int> que;
    vector<int> isInQue(n+1, 0); //记录是否已经在队列中,在队列中的不需要重复加入
    que.push(start);
    while(!que.empty())
    {
        int front = que.front();
        que.pop();
        isInQue[front] = 0; //被扔出队列的顶点在松弛的时候仍然可以加入队列
        for(Edge& e: graph[front]) //遍历所有相邻的边
        {
            //松弛操作
            int to = e.to;
            int weight = e.weight;
            if(minDist[to]>minDist[front] + weight)
            {
                minDist[to] = minDist[front] + weight;
                if(!isInQue[to])
                {
                    que.push(to);
                    isInQue[to] = 1;
                }
            }
        }
    } 
    if(minDist[end]==INT_MAX) cout<<"unconnected"<<endl;
    else cout<<minDist[end]<<endl;
    return 0;
}