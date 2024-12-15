#include<iostream>
#include<vector>
#include<unordered_map>
#include<queue>
using namespace std;

int main()
{
    int n,m; //n个点，m条边
    cin>>n>>m;
    unordered_map<int, vector<int>> dict;
    vector<int> inDegrees(n);
    int s,t; //t依赖于s,s指到t
    while(m--)
    {
        cin>>s>>t;
        dict[s].push_back(t);
        inDegrees[t]++;
    }
    //找到入度为0的点，放入队列
    queue<int> que;
    vector<int> sequence;
    for(int i=0;i<n;i++)
    {
        if(inDegrees[i]==0) 
        {
            que.push(i);
        }
    }
    while(!que.empty())
    {
        int index = que.front();
        que.pop();
        sequence.push_back(index); //拓扑排序的顺序
        vector<int> edges = dict[index];
        for(int i=0;i<edges.size();i++)
        {
            inDegrees[edges[i]]--;
            if(inDegrees[edges[i]] == 0) 
            {
                que.push(edges[i]);
            }
        }
    }
    //如果sequence.size()!=n,说明有的点无法参与拓扑排序，即相互依赖了
    if(sequence.size()!=n) cout<<-1<<endl;
    else
    {
        for(int i=0;i<sequence.size()-1;i++) cout<<sequence[i]<<" ";
        cout<<sequence[sequence.size()-1];
    }
    return 0;
}