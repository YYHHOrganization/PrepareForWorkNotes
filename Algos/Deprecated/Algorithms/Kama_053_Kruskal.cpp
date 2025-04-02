#include<vector>
#include<algorithm>
#include<iostream>
using namespace std;

struct Edge
{
    int l,r,val;
    Edge(int l, int r, int val):l(l),r(r),val(val){}
};

const int N=10005;
vector<int> father(N,-1);
vector<Edge> result;
void init()
{
    for(int i=0;i<N;i++) father[i]=i;
}

int find(int u)
{
    return u==father[u]?u:father[u]=find(father[u]);
}

bool isSame(int u,int v)
{
    u = find(u);
    v = find(v);
    return u==v;
}

void join(int u, int v)
{
    u=find(u);
    v=find(v);
    if(u==v) return;
    father[v]=u;
}

int main()
{
    int v,e,v1,v2,val;
    cin>>v>>e;
    vector<Edge> edges; //存放所有边的信息
    while(e--)
    {
        cin>>v1>>v2>>val;
        edges.emplace_back(Edge(v1,v2,val)); //v1指到v2，题目里有说
    }
    sort(edges.begin(), edges.end(), [](const Edge& l, const Edge& r){
        return l.val<r.val;
    }); //按照边的权重进行排序
    init();//用并查集来构建最小生成树
    int res = 0;
    for(Edge& e:edges)
    {
        int start = e.l;
        int end = e.r;
        if(isSame(start, end)) continue; //成环了，不做处理
        
        join(start, end); //加入到同一个集合当中
        result.emplace_back(e); //加入到最小生成树的结果里
        res += e.val;
    }
    cout<<res<<endl;
}