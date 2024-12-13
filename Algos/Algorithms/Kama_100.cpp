#include<iostream>
#include<vector>
using namespace std;

int dirs[4][2] = {0,1,0,-1,1,0,-1,0};
void dfs(const vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y, int& cnt)
{
    for(int i=0;i<4;i++)
    {
        int xnew = x + dirs[i][0];
        int ynew = y + dirs[i][1];
        if(xnew<0 || xnew >= grid.size() || ynew<0 || ynew>=grid[0].size()) continue;
        if(!visited[xnew][ynew] && grid[xnew][ynew]==1)
        {
            cnt++;
            visited[xnew][ynew] = 1;
            dfs(grid, visited, xnew, ynew, cnt);
        }
    }
}

void bfs(const vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y, int& cnt)
{
    
}

int main()
{
    int n, m; //n是行数，m是列数
    cin>>n>>m;
    vector<vector<int>> grids(n, vector<int>(m, 0));
    vector<vector<int>> visited(n, vector<int>(m, 0));
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
            cin>>grids[i][j];
    }
    int res = 0; //最终结果
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            if(!visited[i][j]&&grids[i][j]==1)
            {
                int cnt = 1; //先把自己算上
                visited[i][j] = 1; //总是忘了写这句
                dfs(grids, visited, i,j,cnt); 
                if(cnt>res) res = cnt;
            }
        }
    }
    cout<<res<<endl;
    return 0;
}