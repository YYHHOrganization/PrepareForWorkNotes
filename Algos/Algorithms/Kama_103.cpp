#include<iostream>
#include<vector>
using namespace std;

int dirs[4][2] = {1,0,-1,0,0,1,0,-1};
void dfs(const vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y)
{
    if(visited[x][y]) return; //这句判断提前，可以适当加速一点
    visited[x][y] = 1; //当前格可以访问
    for(int i=0;i<4;i++)
    {
        int xnew = x + dirs[i][0];
        int ynew = y + dirs[i][1];
        if(xnew<0 || xnew>=grid.size() || ynew<0 || ynew>=grid[0].size()) continue; //越界了continue即可
        if(grid[xnew][ynew]>=grid[x][y])
        {
            dfs(grid, visited, xnew, ynew);
        }
    }
}

int main()
{
    int n,m; //n行m列
    cin>>n>>m;
    vector<vector<int>> grid(n, vector<int>(m, 0));
    vector<vector<int>> visited1(n, vector<int>(m, 0)); //visited1是左边和上边
    vector<vector<int>> visited2(n, vector<int>(m, 0)); //visited2是右边和下边
    int sizeX = grid.size();
    int sizeY = grid[0].size();
    for(int i=0;i<sizeX;i++)
    {
        for(int j=0;j<sizeY;j++)
            cin>>grid[i][j];
    }
    //left
    for(int j=0;j<sizeX;j++)
    {
        if(!visited1[j][0]) dfs(grid, visited1, j, 0);
    }
    //top
    for(int i=0;i<sizeY;i++)
        if(!visited1[0][i]) dfs(grid, visited1, 0, i);
    //right
    for(int j=0;j<sizeX;j++)
        if(!visited2[j][sizeY-1]) dfs(grid, visited2, j, sizeY-1);
    //down
    for(int i=0;i<sizeY;i++)
        if(!visited2[sizeX-1][i]) dfs(grid, visited2, sizeX-1, i);
    
    //两个visited里都有，打印出来
    for(int i=0;i<sizeX;i++)
    {
        for(int j=0;j<sizeY;j++)
        {
            if(visited1[i][j] && visited2[i][j])
                cout<<i<<" "<<j<<endl;
        }    
    }

    return 0;
}