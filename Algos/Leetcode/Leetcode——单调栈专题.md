# Leetcode——单调栈专题

# 一、基础

## 1.[739. 每日温度](https://leetcode.cn/problems/daily-temperatures/)

第一种写法，是从右往左写，维护“可能的最大值”：

```c++
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        //1.从右到左遍历,维护"可能的最近最大值",一定不会是该条件的就会被pop出去
        int n = temperatures.size();
        vector<int> res(n);
        stack<int> stk; //单调栈,里面保存的是索引值
        for(int i=n-1;i>=0;i--){
            int temperature = temperatures[i];
            while(!stk.empty() && temperature>=temperatures[stk.top()]){ //相等的情况也要pop,只保留最前面的相等值
                stk.pop();
            }
            if(!stk.empty()){
                //单调栈里还有东西,更新索引
                res[i] = stk.top()-i;
            }
            stk.push(i); //pop掉应该弹栈的元素后,入栈
        }
        return res;
    }
};
```



第二种写法，是从左往右写，维护“还没有找到答案的值”：

```c++
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> res(n);
        //从左往右写,维护还没有找到答案的值(依旧存储索引)
        stack<int> stk;
        for(int i=0;i<n;i++){
            //小于当前值的全部弹栈(注意!等于当前值的还没有找到更高的温度,根据题意需要更高的而不是相等的,因此还要在栈里等着),并且更新结果
            int temperature = temperatures[i];
            while(!stk.empty() && temperatures[stk.top()]<temperature){
                int index = stk.top();
                stk.pop();
                res[index] = i - index;
            }
            stk.push(i);
        }
        return res;
    }
};
```

