#include<iostream>
#include<queue>
#include<cstring>
using namespace std;

int chess_jump_cnt[1001][1001];
int dirs[8][2] = {-1,2, 1,2, 1,-2, -1,-2, -2,1 ,-2,-1 ,2,1 ,2,-1};
struct Knight //骑士的数据结构
{
    int f,g,h; //用于A*寻路的启发式算法
    int x,y; //所处的坐标
    bool operator < (const Knight & k) const // 重载运算符， 从小到大排序
    {  
        return k.f < f;
    }
};
priority_queue<Knight> que;

int Heuristic(const Knight& node, int& endX, int& endY)
{
    //计算距离终点的启发式距离,这里直接用欧拉距离了
    int x = node.x;
    int y = node.y;
    return (endX - x) * (endX - x) + (endY - y) * (endY - y); //统一不开根号，这样算的快
}


void AStar(int& endX, int& endY)
{
    while(!que.empty())
    {
        //拿出队首
        Knight cur = que.top();
        que.pop();
        if(cur.x == endX && cur.y == endY) break; //BFS最终找到了目标
        for(int i=0;i<8;i++)
        {
            int nextX = cur.x + dirs[i][0];
            int nextY = cur.y + dirs[i][1];
            if(nextX<=0 || nextX>1000 || nextY<=0 || nextY>1000) continue;
            if(!chess_jump_cnt[nextX][nextY]) //还没有访问过的地方
            {
                chess_jump_cnt[nextX][nextY] = chess_jump_cnt[cur.x][cur.y] + 1;
                Knight next;
                next.x = nextX;
                next.y = nextY;
                next.g = cur.g + 5; //每次跳的移动距离+5,取平方
                next.h = Heuristic(next, endX, endY);
                next.f = next.g + next.h;
                que.push(next);
            }
            
        }
    }
}

int main()
{
    int n;
    cin>>n;
    int a1,a2,b1,b2;
    while(n--)
    {
        cin>>a1>>a2>>b1>>b2;
        memset(chess_jump_cnt, 0, sizeof(chess_jump_cnt));
        while(!que.empty()) que.pop();
        Knight start;
        start.x = a1;
        start.y = a2; //设置起点
        start.g = 0;
        start.h = Heuristic(start, b1, b2);
        start.f = start.g + start.h;
        que.push(start);
        AStar(b1, b2); //传入的是终点坐标
        cout<< chess_jump_cnt[b1][b2] << endl; //输出最小的步数 
    }
    return 0;
}