#include<vector>
#include<iostream>
#include<climits>
using namespace std;

int main()
{
    int n,m,s,t,v;
    cin>>n>>m; //n个节点,m条边,index从1开始
    vector<vector<int>> graph;
    vector<int> minDist(n+1, INT_MAX); //minDist存储从start到这个点的最小距离
    while(m--)
    {
        cin>>s>>t>>v;
        graph.push_back({s,t,v}); //因为BellmanFord算法并不需要知道边的相邻情况,所以直接存进去所有边就行
    }
    int start = 1;
    int end = n;
    minDist[start] = 0;
    for(int i=1;i<n;i++) //遍历n-1次,因为n个顶点,起点到终点最多有n-1条边,松弛n-1次即可
    {
        //遍历所有的边,进行松弛操作
        for(vector<int>& e:graph)
        {
            int from = e[0];
            int to = e[1];
            int weight = e[2]; //可能存在负权重
            //这条边的起点不能是没遍历过的
            if(minDist[from]!=INT_MAX && minDist[to]>minDist[from] + weight)
            {
                //更新
                minDist[to] = minDist[from] + weight; 
            }
        }
    }
    if(minDist[end]==INT_MAX) cout<<"unconnected"<<endl;
    else cout<<minDist[end]<<endl;
    return 0;
    
}