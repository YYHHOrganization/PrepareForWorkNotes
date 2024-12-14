#include<iostream>
#include<vector>
#include<queue>
using namespace std;

int dirs[4][2] = {1,0,-1,0,0,1,0,-1};
int bfs(const vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y) //返回值表示是否是孤岛
{
    int cnt = 0;
    queue<pair<int, int>> que;
    que.push({x, y});
    visited[x][y] = 1;
    cnt = 1;
    bool isDead = false;
    while(!que.empty())
    {
        pair<int, int> front = que.front();
        que.pop();
        for(int i=0;i<4;i++)
        {
            int xnew = front.first + dirs[i][0];
            int ynew = front.second + dirs[i][1];
            if(xnew<0 || xnew>=grid.size() || ynew<0 || ynew>=grid[0].size()) continue;
            if(!visited[xnew][ynew] && grid[xnew][ynew] == 1) //说明是当前岛屿的一部分
            {
                if(xnew == 0 || xnew == grid.size() - 1|| ynew == 0 || ynew == grid[0].size() - 1)
                {
                    isDead = true;
                }
                //即使不是孤岛，也要遍历完，不然有的可能没遍历到
                visited[xnew][ynew] = 1;
                //cout<<xnew<<"  "<<ynew<<endl;
                que.push({xnew, ynew});
                cnt++;
            }
        }
    }
    return isDead?0:cnt;
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
    int cnt = 0; //孤岛的总数
    for(int i=1;i<n-1;i++)
    {
        for(int j=1;j<m-1;j++) //周围的肯定不是，遍历中间的看看就行
        {
            if(!visited[i][j] && grids[i][j] == 1)
            {
                cnt+=bfs(grids, visited, i, j);
            }
        }
    }
    cout<< cnt<< endl;
    return 0;

}