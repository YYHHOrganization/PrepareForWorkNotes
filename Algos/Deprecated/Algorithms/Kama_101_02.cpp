#include<iostream>
#include<vector>
#include<queue>
using namespace std;

int dirs[4][2] = {1,0,-1,0,0,1,0,-1};
void dfs(vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y)
{
    visited[x][y] = 1;
    grid[x][y] = 0; //变成海洋
    for(int i=0;i<4;i++)
    {
        int xnew = x + dirs[i][0];
        int ynew = y + dirs[i][1];
        if(xnew<0 || xnew>=grid.size() || ynew<0 || ynew>=grid[0].size()) continue;
        if(!visited[xnew][ynew] && grid[xnew][ynew] == 1)
        {
            grid[xnew][ynew] = 0; //沉没下去！
            dfs(grid, visited, xnew, ynew);
        }
    }
}


int main()
{
    int n, m;
    cin>>n>>m; //n行，m列
    vector<vector<int>> grids(n, vector<int>(m, 0));
    vector<vector<int>> visited(n, vector<int>(m, 0));
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
            cin>>grids[i][j];
    }
    int sizeY = grids[0].size();
    int sizeX = grids.size();
    //另一种比较巧妙的做法，这里用dfs做示例，遍历地图的边缘四周，然后把所有与边缘相连的岛屿都“变为”海洋，剩下的grid还是1的就是孤岛
    for(int i=0;i<grids.size();i++)
    {
        if(!visited[i][0] && grids[i][0] == 1) dfs(grids, visited, i, 0);
        if(!visited[i][sizeY-1] && grids[i][sizeY-1] == 1) dfs(grids, visited, i, sizeY-1);
    }

    for(int j=0;j<sizeY;j++)
    {
        if(!visited[0][j] && grids[0][j] == 1) dfs(grids, visited, 0, j);
        if(!visited[sizeX-1][j] && grids[sizeX-1][j] == 1) dfs(grids, visited, sizeX-1, j);
    }

    int cnt = 0;
    for(int i=0;i<sizeX;i++)
    {
        for(int j=0;j<sizeY;j++)
            if(grids[i][j]==1) cnt++;
    }
    cout<<cnt<<endl;
    return 0;
}