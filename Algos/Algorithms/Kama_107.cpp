#include<iostream>
#include<vector>
using namespace std;
const int N = 105;
vector<int> father(N, 0);

void init()
{
    for(int i=0;i<N;i++)
    {
        father[i]=i;
    }
}

int find(int u)
{
    return u == father[u] ? u: father[u] = find(father[u]);
}


bool isSame(int u, int v)
{
    u = find(u);
    v = find(v);
    return u==v;
}

void join(int u, int v) //v join 到 u 上
{
    u = find(u);
    v = find(v);
    if(u==v) return;
    father[v] = u;
}

int main()
{
    init();
    int n,m,s,t;//n节点数,m边数
    cin>>n>>m;
    while(m--)
    {
        cin>>s>>t;
        join(s, t);
    }
    int src, dst;
    cin>>src>>dst;
    if(isSame(src, dst)) cout<<1<<endl;
    else cout<<0<<endl;

    return 0;
}