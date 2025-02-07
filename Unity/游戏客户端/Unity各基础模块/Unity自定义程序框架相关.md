# Unity自定义程序框架相关



# 一、缓存池的概念

前置知识：

- 【1】Unity是如何进行GC的？[Unity GC 学习总结 - 知乎](https://zhuanlan.zhihu.com/p/265217138)。更为具体的算法细节在面经相关的笔记中会进行整理。



# 二、一个缓存池的demo

最核心的部分其实就是下面这些（其中ab包管理器需要自己定义）：

```c#
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PoolMgr : BaseManager<PoolMgr>
{
    private Dictionary<string, List<GameObject>> poolDic = new Dictionary<string, List<GameObject>>();
    
    //从ab包中加载,一般都是GameObject
    public GameObject GetObj(string abName, string resName, Transform parent = null)
    {
        GameObject go = null;
        if(poolDic.ContainsKey(resName) && poolDic[resName].Count > 0)
        {
            go = poolDic[resName][0];
            poolDic[resName].RemoveAt(0);
        }
        else
        {
            go = ABMgr.GetInstance().LoadRes<GameObject>(abName, resName);
            go.name = resName; //让物品名和池子名保持一致
            go.transform.SetParent(parent);
        }
        go.SetActive(true);
        return go;
    }
    
    
    public void PushObj(string name, GameObject obj) //把用完的放进来
    {
        obj.SetActive(false);
        if(!poolDic.ContainsKey(name))
        {
            poolDic.Add(name, new List<GameObject>(){obj});
        }
        else
        {
            poolDic[name].Add(obj);
        }
    }
}

```

其他的需求比如清空对象池之类的就不放进来了，并不是非常核心的部分。