#include<iostream>
#include<vector>
#include<list>
#include<queue>
#include<climits>
using namespace std;

struct Edge
{
    int end;
    int weight;
    Edge(int end, int weight): end(end), weight(weight){}
};

class MyCompare
{
public:
    bool operator()(const pair<int, int>& lhs, const pair<int, int>& rhs)
    {
        //注意这个判断语句，是大于！此时是小顶堆,这个容器比较特殊
        return lhs.second > rhs.second; //When true is returned, it means the order is NOT correct and swapping of elements takes place.
    } 
};

int main()
{
    int n,m,s,e,v;
    cin>>n>>m;
    vector<list<Edge>> graph(n+1); //索引从0开始
    while(m--)
    {
        cin>>s>>e>>v;
        graph[s].push_back(Edge(e, v));
    }
    priority_queue<pair<int, int>, vector<pair<int, int>>, MyCompare> pq;
    vector<int> visited(n+1, 0);
    vector<int> minDist(n+1, INT_MAX);
    int start = 1;
    int end = n;
    pq.push({start, 0}); //一开始把start，0 push进来，这里存储minDist
    minDist[start] = 0;
    while(!pq.empty())
    {
        //从优先队列中弹出最小的minDist
        pair<int, int> cur = pq.top();
        pq.pop();
        //cout<<"cur "<< cur.first <<endl;
        //此时top.first就存储当前节点，top.second存储minDist[当前节点]
        if(visited[cur.first]) continue;
        visited[cur.first] = 1; //标记已访问
        list<Edge>& edges = graph[cur.first]; //与其相连的所有边
        for(Edge& e: edges)
        {
            if(e.weight!=INT_MAX && !visited[e.end] && cur.second + e.weight < minDist[e.end]) //与朴素版Dijkstra是类似的
            {
                minDist[e.end] = cur.second + e.weight;
                pq.push({e.end, minDist[e.end]}); //都是e.end，别把错的搞进来
            }
        }
    }
    if(!visited[end]) cout<<-1<<endl;
    else cout<<minDist[end]<<endl;
    return 0;
}