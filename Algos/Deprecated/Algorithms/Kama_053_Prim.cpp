#include<vector>
#include<iostream>
#include<climits>
using namespace std;
const int max_int = 9999999;

int main()
{
    int v,e;
    cin>>v>>e; //顶点数，边数
    vector<vector<int>> graph(v+1,vector<int>(v+1, max_int)); //邻接矩阵,默认填比较大，认为不可达
    vector<int> minDist(v+1, max_int);
    vector<int> parent(v+1, -1); //用于记录联通路径
    vector<int> isInTree(v+1, 0); //是否已经在生成树里
    int v1, v2, val;
    while(e--)
    {
        cin>>v1>>v2>>val;
        graph[v1][v2] = val;
        graph[v2][v1] = val;
    }
    int sum = 0; //最终结果
    for(int i=1;i<v;i++) //一共v-1轮迭代，建立n-1条边
    {
        int tol = INT_MAX;
        int index = 1;
        //遍历minDist,找到最小的作为下一次的点
        for(int j=1;j<=v;j++)
        {
            if(!isInTree[j] && minDist[j]<tol) //注：是找到minDist里面的最小值
            {
                tol = minDist[j];
                index = j;
            }
        }
        //把index放入到生成树里，然后更新所有的dist
        isInTree[index] = 1;
        for(int j=1;j<=v;j++)
        {
            if(!isInTree[j] && graph[index][j]<minDist[j])
            {
                minDist[j] = graph[index][j];
                parent[j] = index;
            }
        }
    }
    for(int i=2;i<=v;i++)  // 不计第一个顶点，因为统计的是边的权值，v个节点有 v-1条边
        sum+=minDist[i];
    cout<<sum<<endl;
    //输出prim算法构建的结果
    for(int i=1;i<=v;i++) cout<< i << "->" <<parent[i]<<endl;
    return 0;
}