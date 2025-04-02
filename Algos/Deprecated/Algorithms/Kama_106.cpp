#include<iostream>
#include<vector>
using namespace std;
int dirs[4][2] = {1,0,-1,0,0,1,0,-1};
int main()
{
    int n, m; //n行m列
    cin>>n>>m;
    int total = 0;
    vector<vector<int>> grid(n, vector<int>(m, 0));
    for(int i=0;i<n;i++)
        for(int j=0;j<m;j++) cin>>grid[i][j];
    for(int i=0;i<n;i++)
    {
        for(int j=0;j<m;j++)
        {
            if(grid[i][j]==0) continue;
            int cnt = 0;
            for(int d=0;d<4;d++)
            {
                int xnew = i + dirs[d][0];
                int ynew = j + dirs[d][1];
                if(xnew<0 || xnew >=n || ynew<0 || ynew>=m) continue;
                if(grid[xnew][ynew]==1)
                    cnt++;
            }
            total += (4-cnt);
        }
    }
    cout<<total<<endl;
}