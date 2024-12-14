#include<iostream>
#include<queue>
#include<vector>
using namespace std;

int dirs[4][2] = {1,0,-1,0,0,1,0,-1};
void bfs(vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y)
{
    queue<pair<int, int>> que;
    grid[x][y] = 2;
    que.push({x, y});
    visited[x][y] = 1;
    while(!que.empty())
    {
        pair<int, int> front = que.front();
        que.pop();
        for(int i=0;i<4;i++)
        {
            int xnew = front.first + dirs[i][0];
            int ynew = front.second + dirs[i][1];
            if(xnew<0 || xnew>=grid.size() || ynew<0 || ynew>=grid[0].size()) continue;
            if(!visited[xnew][ynew] && grid[xnew][ynew] == 1)
            {
                grid[xnew][ynew] = 2;
                visited[xnew][ynew] =1;
                que.push({xnew, ynew});
            }
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
    //从四个边缘开始遍历，把所有的1都变成2，然后再整体遍历一次，把所有的2变成1，1变成0
    int sizeX = grids.size();
    int sizeY = grids[0].size();
    for(int i=0;i<sizeX;i++)
    {
        if(!visited[i][0] && grids[i][0]==1) bfs(grids, visited, i, 0);
        if(!visited[i][sizeY-1] && grids[i][sizeY-1]==1) bfs(grids, visited, i, sizeY-1);
    }
    for(int j=0;j<sizeY;j++)
    {
        if(!visited[0][j] && grids[0][j]==1) bfs(grids, visited, 0, j);
        if(!visited[sizeX-1][j] && grids[sizeX-1][j]==1) bfs(grids, visited, sizeX-1, j);
    }
    for(int i=0;i<sizeX;i++)
    {
        for(int j=0;j<sizeY;j++)
        {
            if(grids[i][j] == 1 ) grids[i][j] =0;
            else if(grids[i][j] == 2) grids[i][j] =1;
            cout<<grids[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}