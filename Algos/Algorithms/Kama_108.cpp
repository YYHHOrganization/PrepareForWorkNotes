#include<vector>
#include<iostream>
using namespace std;
const int N = 1005;
vector<int> father(N, 0);

void init()
{
    for(int i=0;i<N;i++) father[i]=i;
}

int find(int u)
{
    return u == father[u]? u: father[u] = find(father[u]);
}

bool isSame(int u, int v)
{
    u=find(u);
    v=find(v);
    return u==v;
}

void join(int u, int v)
{
    u=find(u);
    v=find(v);
    if(u==v) return;
    father[v] = u;
}

int main()
{
    init();
    int n;
    cin>>n;
    int s,t;
    while(n--)
    {
        cin>>s>>t;
        if(isSame(s,t)) 
        {
            cout<<s<<" "<<t;
            return;
        } 
        else
        {
            join(s, t);
        }
    }
    return 0;
}