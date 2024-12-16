#include<iostream>
#include<vector>
#include<climits>
using namespace std;

int main()
{
    int n,m,s,e,v; //n个节点，m条边，索引从1开始
    cin>>n>>m;
    vector<vector<int>> graph(n+1, vector<int>(n+1, INT_MAX)); //初始化为最大权重
    vector<int> minDist(n+1, INT_MAX); //初始化minDist数组，默认是最大值
    vector<int> visited(n+1, 0);
    vector<int> parent(n+1, -1); //不是必须的，存储路径
    while(m--)
    {
        cin>>s>>e>>v;
        graph[s][e] = v; //设置权重
    }
    int start = 1;
    int end = n;
    minDist[start] = 0; //更新距离初始点的距离为0
    for(int i=1;i<=n;i++) //开始Dijkstra算法,n轮迭代
    {
        int minDistance = INT_MAX;
        int cur = 1; //注意！这里不能是-1，因为如果第一个节点的出度是0，cur不会被更新，就会出错
        //总：遍历所有节点，找到与“源”节点最近的，minDist此时存储的是与start最近的
        //step1：找到距离源点最近的
        for(int j=1;j<=n;j++)
        {
            if(!visited[j] && minDist[j]<minDistance)
            {
                minDistance = minDist[j];
                cur = j;
            }
        }
        //step2:设置为已访问
        visited[cur] = 1;
        //step3:更新所有节点“距离源节点”的距离
        for(int j=1;j<=n;j++)
        {
            if(!visited[j] && graph[cur][j] != INT_MAX && minDist[j] > minDist[cur] + graph[cur][j]) //注意第二个&&，不然容易越界
            {
                minDist[j] = minDist[cur] + graph[cur][j];
                parent[j] = cur; //从cur过去
            }
        }
        //step4(可选)：debug
        // cout<<"cur: "<< cur<< endl;
        // for(int j=1;j<=n;j++) cout<<j<<" : "<< minDist[j]<< "\\";
        // cout<<endl<<endl;
    }

    //如果结尾节点没被访问，说明不可达
    if(!visited[end]) cout<<-1<<endl;
    else
    {
        cout<<minDist[end]<<endl;
    }
    
    return 0;
}