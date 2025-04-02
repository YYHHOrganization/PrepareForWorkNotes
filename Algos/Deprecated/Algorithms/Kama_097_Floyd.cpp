//floyd算法
#include<iostream>
#include<vector>
using namespace std;

int main()
{
    int n,m;
    cin>>n>>m; //n个顶点，m条边
    vector<vector<int>> dp(n+1, vector<int>(n+1, 10005)); //dp[i][j]表示i到j的最小距离
    int u,v,w;
    while(m--)
    {
        cin>>u>>v>>w;
        dp[u][v] = w;
        dp[v][u] = w; //双向道路
    }
    int q, start, end;
    for(int k=1;k<=n;k++) //本来是三维的dp[i][j][k]表示i到j经过1....k中的点
    {
        for(int i=1;i<=n;i++)
        {
            for(int j=1;j<=n;j++)
            {
                //dp[i][j][k] = min(dp[i][j][k-1], dp[i][k][k-1]+ dp[k][j][k-1])
                dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j]);
            }
        }
    }
    cin>>m;
    while(m--)
    {
        cin>>start>>end;
        if(dp[start][end]==10005) cout<<-1<<endl;
        else cout<<dp[start][end]<<endl;
    }

    return 0;
}