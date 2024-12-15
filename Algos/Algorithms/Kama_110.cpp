#include<iostream>
#include<unordered_set>
#include<unordered_map>
#include<queue>
using namespace std;

int main()
{
    int n;
    cin>>n;
    unordered_set<string> words;  //存储所有的单词
    string beginStr, endStr;
    cin>>beginStr>>endStr;
    words.insert(beginStr);
    words.insert(endStr); //放入单词列表中

    while(n--)
    {
        string word;
        cin>>word;
        words.insert(word);
    }
    //至此,所有的词汇都被放入了词汇表中
    unordered_map<string, int> dict; //key是单词,value是到达的最短路径
    queue<string> que; //用于BFS
    que.push(beginStr);
    dict.insert({beginStr, 1}); 
    while(!que.empty())
    {
        string front = que.front();
        que.pop();
        int dist = dict[front];
        //找到与之"相连"的单词,如果在fict中说明已经访问完了
        //暴力找
        for(char &s: front) //替换front单词中的每个字母
        {
            char tmp = s;
            for(int i=0;i<26;i++)
            {
                s = 'a'+ i; //进行替换
                //查看是否到了终点
                if(front == endStr)
                {
                    cout<<dist+1<<endl;
                    return 0;
                }
                //查看单词表里是否有替换字母后的单词,并且没有访问过
                if(words.count(front)>0 && dict.count(front)==0)
                {
                    dict[front] = dist + 1;
                    que.push(front);
                }
            }
            s = tmp;
        }

    }

    cout<<0<<endl; //没找到,输出0
    return 0;
}