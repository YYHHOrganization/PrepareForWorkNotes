#include<iostream>
#include<vector>
using namespace std;

const int dirs[4][2] = {0, 1, 0, -1, 1, 0, -1, 0}; 
void dfs(const vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y) //x和y指的是起点
{
    for(int i=0;i<4;i++) //遍历四个方向
    {
        int deltaX = dirs[i][0];
        int deltaY = dirs[i][1];
        int xnew = x + deltaX;
        int ynew = y + deltaY;
        if(xnew>=0 && xnew<grid.size() && ynew >=0 && ynew<grid[0].size() && grid[xnew][ynew] == 1 && !visited[xnew][ynew])
        {
            visited[xnew][ynew] = 1; //只是标记上即可，不需要回退回来
            dfs(grid, visited, xnew, ynew);
        }
    }
}

void print(const vector<vector<int>>& visited)
{
    cout<<"print!!"<<endl;
    for(const vector<int>& vec: visited)
    {
        for(int i=0;i<vec.size();i++)
        {
            cout<<vec[i]<<" ";
        }
        cout<<endl;
    }
}

int main()
{
    int n, m;
    cin>>n>>m;
    vector<vector<int>> grid(n, vector<int>(m, 0)); //n行，m列
    vector<vector<int>> visited(n, vector<int>(m, 0));//一开始都没访问过
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
            cin>>grid[i][j];
    }
    int res = 0;
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            if(grid[i][j] == 1 && !visited[i][j]) //新的还没访问过的地带
            {
                res++;
                visited[i][j] = 1;
                dfs(grid, visited, i, j);
                //print(visited);
            }
        }
    }
    cout<<res<<endl;
    return 0;
}