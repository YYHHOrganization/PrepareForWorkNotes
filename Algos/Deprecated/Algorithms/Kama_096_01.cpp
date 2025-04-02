#include<vector>
#include<iostream>
#include<climits>
using namespace std;

int main()
{
    int n,m,s,t,v;
    cin>>n>>m;
    //存所有的边即可
    vector<vector<int>> edges;
    while(m--)
    {
        cin>>s>>t>>v;
        edges.push_back({s,t,v});
    }
    //开始松弛，但是每次松弛都是基于上次的minDist，而不是基于本次的
    vector<int> minDist(n+1, INT_MAX); //minDist里面存储的是距离起点的最小距离
    vector<int> lastMinDist(n+1, INT_MAX);
    int start, end, k;
    cin>>start>>end>>k; //k是最多可以走几个点
    //松弛k-1次，但每次都是基于上次的minDist
    minDist[start] = 0;
    for(int i=1;i<=k+1;i++)  //起点最多经过k + 1 条边到达终点的最短距离,原来的Bellman Ford算法起点到终点最多经过n-1条边，所以松弛n-1次，这里最多经过k+1条边，因此松弛k+1次
    {
        lastMinDist = minDist;
        for(vector<int>& e: edges)
        {
            int from = e[0];
            int to = e[1];
            int weight = e[2];
            //松弛,基于上次的,容易写错
            if(lastMinDist[from]!=INT_MAX && lastMinDist[from]+weight<minDist[to])
            {
                minDist[to] = lastMinDist[from] + weight;
            }
        }
    }
    if(minDist[end] == INT_MAX) cout<<"unreachable"<<endl;
    else cout<<minDist[end]<<endl;

    return 0;
}