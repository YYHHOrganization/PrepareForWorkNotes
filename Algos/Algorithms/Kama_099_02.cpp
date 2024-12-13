#include<iostream>
#include<vector>
#include<queue>
using namespace std;

int dirs[4][2] = {0,1,0,-1,1,0,-1,0};
void bfs(const vector<vector<int>>& grids, vector<vector<int>>& visited, int x, int y)
{
    queue<pair<int, int>> que; //用于BFS的队列
    que.push({x, y}); //先把当前的push进来
    while(!que.empty()) //队列不为空
    {
        pair<int, int> front = que.front();
        que.pop(); //弹出队首
        for(int i=0;i<4;i++)
        {
            int xnew = front.first + dirs[i][0];
            int ynew = front.second + dirs[i][1];
            if(xnew<0 || xnew >= grids.size() || ynew < 0 || ynew>=grids[0].size()) continue;
            if(!visited[xnew][ynew] && grids[xnew][ynew]==1)
            {
                visited[xnew][ynew] = 1;
                que.push({xnew, ynew});
            }
        }
    }
    
}

int main()
{
    int n, m;
    cin>>n>>m; //n:行数，m：列数
    vector<vector<int>> grids(n, vector<int>(m, 0));
    vector<vector<int>> visited(n, vector<int>(m, 0));
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            cin>>grids[i][j];
        }
    }
    int res = 0;
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            if(grids[i][j]==1 && !visited[i][j])
            {
                res++;
                visited[i][j]=1;
                bfs(grids, visited, i, j);
            }
        }
    }
    cout<< res<< endl;
    return 0;
}