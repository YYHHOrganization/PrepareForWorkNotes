#include <iostream>
#include <vector>
using namespace std;

const int N = 1002;
vector<int> father(N, 0); //存储所有的father 

void init()
{
    for(int i=0;i<N;i++)
        father[i] = i;
}

//找到父节点
int find(int u)
{
    return (u == father[u])? u : father[u] = find(father[u]); //路径压缩
}

//判断两个节点是否在一个集合中
bool isSame(int u, int v)
{
    u = find(u);
    v = find(v);
    return u==v;
}

void join(int u, int v) //把v加入到u的集合中
{
    u = find(u);
    v = find(v);
    if(u==v) return;
    father[v] = u;
}

int main()
{
    init();
}