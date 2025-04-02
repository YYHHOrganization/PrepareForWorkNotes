#include<vector>
#include<iostream>
using namespace std;
const int N = 1002;
vector<int> father(N, 0); //用于并查集查询

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

void findCycleEdge(vector<vector<int>>& edges) //和108题一样
{
    init(); //用并查集来做
    for(vector<int>& e: edges)
    {
        int start = e[0];
        int end = e[1];
        if(isSame(start, end))
        {
            cout<<start<<" "<<end;
            return;
        }
        join(start, end);
    }
}

bool isTreeAfterDeleteEdge(vector<vector<int>> edges, int deleteIndex)
{
    //检测删完边之后是否还有环,用并查集
    init();
    for(int i=0;i<edges.size();i++)
    {
        if(i == deleteIndex) continue; //模拟删掉这条边的操作,不加入并查集
        int start = edges[i][0];
        int end = edges[i][1];
        if(isSame(start, end)) return false;
        join(start, end);
    }
    return true;
}

int main()
{
    int n;
    cin>>n;
    int s,t;
    //存储所有的边
    vector<vector<int>> edges; //每条边存起点和终点,注意存储边的数据结构
    vector<int> degrees(n+1, 0); //存储每个顶点的入度
    while(n--)
    {
        cin>>s>>t;
        edges.push_back({s, t});
        degrees[t]++;
    }
    //遍历所有边,找到入度为2的边的索引,加入到vector中
    vector<int> degree2Indexes;
    for(int i=edges.size()-1;i>=0;i--)  //从后往前遍历,因为要找到最后的符合要求的边
    {
        if(degrees[edges[i][1]] == 2) degree2Indexes.push_back(i); //把入度为2的边索引存起来
    }
    //看是否有入度为2的点
    if(degree2Indexes.size()>0)
    {
        //此时肯定有两个,因为a->b和c->b会记录b两次
        //先试试删除第一个
        if(isTreeAfterDeleteEdge(edges, degree2Indexes[0]))
        {
            //删完是树,就删这个,否则其实删完是有环的
            cout << edges[degree2Indexes[0]][0]<< " "<< edges[degree2Indexes[0]][1];
        }
        else
        {
            //不能删第一个,删第二个
            cout << edges[degree2Indexes[1]][0]<< " "<< edges[degree2Indexes[1]][1];
        }
    }
    else //没有入度为2的点,说明有环,找到最后一个成环的地方,输出,与108题类似
    {
        findCycleEdge(edges);
    }

    return 0;
}