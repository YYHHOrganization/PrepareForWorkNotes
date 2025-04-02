#include<iostream>
#include<queue>
#include<vector>
#include<unordered_map>
#include<unordered_set>
using namespace std;

int dirs[4][2] = {0,1,0,-1,1,0,-1,0};
unordered_map<int, int> dict; //存放每个index对应的岛一共有几块
void bfs(vector<vector<int>>& grid, vector<vector<int>>& visited, int x, int y, int label)
{
    queue<pair<int, int>> que;
    visited[x][y] = 1;
    grid[x][y] = label;
    que.push({x,y});
    int cnt = 1;
    while(!que.empty())
    {
        auto front = que.front();
        que.pop();
        for(int i=0;i<4;i++)
        {
            int xnew = front.first + dirs[i][0];
            int ynew = front.second + dirs[i][1];
            if(xnew<0 || xnew>=grid.size() || ynew<0 || ynew>=grid[0].size()) continue; 
            if(!visited[xnew][ynew] && grid[xnew][ynew]!=0)
            {
                visited[xnew][ynew] = 1;
                grid[xnew][ynew] = label;  //将这个岛对应区域标记为同一个label
                cnt+=1;
                que.push({xnew, ynew});
            }
        }
        dict[label] = cnt;
    }
}

int main()
{
    int n,m; //n行m列
    cin>>n>>m;
    vector<vector<int>> grid(n,vector<int>(m, 0)); //这里每一块会存放有多少面积土地
    vector<vector<int>> visited(n,vector<int>(m, 0)); 
    int labelIndex = 1;
    for(int i=0;i<n;i++)
        for(int j=0;j<m;j++) cin>>grid[i][j];
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            if(!visited[i][j] && grid[i][j]!=0)
            {
                bfs(grid, visited, i, j, labelIndex);
                labelIndex++;
            }
        }
    }
    // cout<<"debug"<<endl;
    // for(auto &p: dict)
    // {
    //     cout<<p.first<<" "<<p.second << endl;
    // }
    // cout << "aha"<<endl;
    // for(int i=0;i<n;i++)
    // {
    //     for(int j=0;j<m;j++) cout<<grid[i][j]<<" ";
    //     cout<<endl;
    // }
    // cout<<"enddebug"<<endl;
        
    //经过上述操作之后，每个岛的区域的格子都是该岛的面积数
    int result = 0;
    bool hasZero = false; //是否有空区域，没有的话返回总的格子数
    unordered_set<int> access;
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            if(grid[i][j] == 0) //和上下左右的连起来
            {
                hasZero = true;
                access.clear(); //标记访问过的岛屿，不会再次访问
                int cnt=1;  //连接处得把自己加进去
                for(int d=0;d<4;d++)
                {
                    int xnew = i + dirs[d][0];
                    int ynew = j + dirs[d][1];
                    if(xnew<0 || xnew >= n || ynew<0 || ynew>=m) continue;
                    int index = grid[xnew][ynew]; //当前岛的索引
                    if(access.count(index)) continue; //遍历过了，不再遍历这座岛屿
                    access.insert(index); //已经遍历过了这座岛屿,下次不会遍历
                    cnt+=dict[grid[xnew][ynew]];
                }
                if(cnt>result) result = cnt;
            }
        }
    }
    if(!hasZero) result = m * n;
    cout<<result<<endl;
    return 0;
}