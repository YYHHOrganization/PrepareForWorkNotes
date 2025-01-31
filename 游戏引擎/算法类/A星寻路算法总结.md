# A*寻路算法总结

对于寻路算法，Games104有系统的讲过，对应的笔记中也有整理。A*算法是一个非常常考的题目，因此单独做一篇笔记复习时使用。主要参考对象：

> [A-Star（A*）寻路算法原理与实现 - 知乎](https://zhuanlan.zhihu.com/p/385733813)

这里由于之前已经学过了，因此精简地把重点内容说明一下，并会结合项目demo中的代码。



# 一、基础原理

`A*`算法基于Grid来完成。也就是说会把我们的地图看作是由 `w*h` 个格子组成的，因此寻得的路径也就是由一连串相邻的格子所组成的路径。

> 注：非基于格子的寻路可以使用**基于采样**（Sampling Based）的算法，例如**RRT-Connect**。

对于`A*`算法来说，需要一个估价函数，来判断应该先往哪个格子走。对于任意一个格子`n`，其估价函数为：
$$
f(n) = g(n) + h(n)
$$
其中 **$g(n)$ 指的是从起始格子到格子n的实际代价，而 $h(n)$ 指的是从格子n到终点格子的估计代价。**比如说来看下面这个例子：

![img](A%E6%98%9F%E5%AF%BB%E8%B7%AF%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93.assets/v2-7188b33ac2451d594d794da573bb9f06_r.jpg)

绿色点是出发点，红色点为终点，深灰色点为中间障碍物。来计算一下（考虑$g(n)$和$h(n)$直接算直线过去的距离）：

- （1）格子1：$g(n)=1, h(n)=6$;
- （2）格子2：$g(n)=1,h(n)=4$;
- （3）格子3：$g(n)=\sqrt2,h(n)=\sqrt{17}$;

而计算$f(n)$的时候就是把$g(n)$和$h(n)$加到一起。使用上述的欧几里得距离，有两个弊端：

- 计算过程中伴随着平方与开根号运算，并且需要使用浮点数，性能差。
- 实际上，我们不能直接平滑的移动到红色格子，而需要水平+对角移动结合。此时若没有障碍物的话，实际的$h(n)$应该是$\sqrt2+3$。咋如果$h(n)$采用欧氏距离，那么**$h(n)$ 的值永远小于或等于格子n到终点的最短实际距离。**



因此在实际使用时，我们更常用**曼哈顿距离**或者**对角线+直线**的距离。

![image-20250131101019016](A%E6%98%9F%E5%AF%BB%E8%B7%AF%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93.assets/image-20250131101019016.png)

- 对于曼哈顿距离来说，只需要计算加减法，并且连浮点数都不需要。但是由于我们的格子可以对角线移动，因此不考虑障碍物的话，或者障碍物在两个格子形成的包围盒内，**曼哈顿距离肯定大于或等于格子n到终点的最短实际距离。**
- 对角线+直线距离：既然我们可以对角线移动，那么我们就可以根据水平方向的差值与竖直方向的差值中较小的那个值，计算出对角线，然后再平移。这样不考虑障碍物的情况下，肯定**等于格子n到终点的最短实际距离。但是由于计算对角线同样需要开根号以及浮点数。为了加快计算，我们可以**假设两个格子间的距离为10，然后直接认为对角线距离为14，这样就可以避免浮点数和根号运算了。

> 个人理解，还是取决于游戏内的移动策略。以上的情况是基于移动时不能朝着终点直接撞过来移动，所以不用欧几里得距离。在之前学习`A*`的时候，看到用曼哈顿距离的也很多。



## 1.$h(n)$的影响

来看下面这个例子：

![img](A%E6%98%9F%E5%AF%BB%E8%B7%AF%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93.assets/v2-8caa5c655eb6417494d1e36091a691e4_r.jpg)

图中$g(1)=g(2)=20$，若$h(n)$使用曼哈顿距离，则$h(1)=h(2)=60$，即$f(1)=f(2)$，导致我们无法判断出走1和走2哪个更好。但是若使用对角线距离，则$h(1)=54，h(2)=42$，$f(1)>f(2)$，因此我们下一步要走2。

实际上走2才是最短的路径，但是由于有障碍物，格子2到红格子的实际距离为10+14+14+10=48（右->右下->右下->下），可以发现这种情况下：曼哈顿距离>实际距离>对角线距离。



再看下面这个例子：

![img](A%E6%98%9F%E5%AF%BB%E8%B7%AF%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93.assets/v2-f34196f91853315065d003111d4e1d06_r.jpg)

若使用曼哈顿距离，$f(1)=g(1)+h(1)=14+190=204,f(2)=g(2)+h(2)=74+90=184$，就是说我宁可考虑格子2也不会去考虑格子1。

但是使用对角线距离，$f(1)=g(1)+h(1)=14+136=150，f(2)=g(2)+h(2)=74+78=152$，那就变得格子1要优先考虑。

两种$h(n)$得到的路径如下：

1. 曼哈顿距离

![img](A%E6%98%9F%E5%AF%BB%E8%B7%AF%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93.assets/v2-4a3010191cf96bde40881ae7c598ef89_r.jpg)

2. 对角线距离

![img](A%E6%98%9F%E5%AF%BB%E8%B7%AF%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93.assets/v2-141d37a4d64adbef8f5bf7a2dde385b5_r.jpg)

可以发现，对角线距离的结果才是最短的路径，但是它会计算更多的格子（图中两种蓝色的格子就是要计算的格子）。

总结来说：

- 如果 h(n) <= `n到终点的实际距离`，A*算法可以找到最短路径，但是搜索的点数多，搜索范围大，效率低。
- 如果 h(n) > `n到终点的实际距离`，搜索的点数少，搜索范围小，效率高，但是得到的路径并不一定是最短的。
- h(n) 越接近` n到终点的实际距离`，那么A*算法越完美。（个人理解是如果用曼哈顿距离，那么只需要找到一条长度小于等于该距离的路径就算完成任务了。而使用对角线距离就要找到一条长度大于等于对角线距离且最短的路径才行。）
- 若 h(n)=0，即 f(n)=g(n)，A*算法就变为了Dijkstra算法（Dijstra算法会毫无方向的向四周搜索）。
- 若 h(n) 远远大于 g(n) ，那么 f(n) 的值就主要取决于 h(n)，A*算法就演变成了BFS算法（这里的BFS指的是(最佳优先搜索)Best-First Search）。

**因此在[启发式搜索](https://zhida.zhihu.com/search?content_id=173849187&content_type=Article&match_order=1&q=启发式搜索&zhida_source=entity)中，估价函数是十分重要的，采用了不同的估价可以有不同的效果。**



## 2.具体寻路过程

这里原理看知乎链接：[A-Star（A*）寻路算法原理与实现 - 知乎](https://zhuanlan.zhihu.com/p/385733813)。后文直接给出关键的代码。



# 二、代码说明

这部分是`A*`寻路demo的代码说明。

## 1.Node类

```c#
public class Node
{
    Int2 m_position;//下标
    public Int2 position => m_position;
    public Node parent;//上一个node
    
    //角色到该节点的实际距离
    int m_g;
    public int g {
        get => m_g;
        set {
            m_g = value;
            m_f = m_g + m_h;
        }
    }

    //该节点到目的地的估价距离
    int m_h;
    public int h {
        get => m_h;
        set {
            m_h = value;
            m_f = m_g + m_h;
        }
    }

    int m_f;
    public int f => m_f;

    public Node(Int2 pos, Node parent, int g, int h) {
        m_position = pos;
        this.parent = parent;
        m_g = g;
        m_h = h;
        m_f = m_g + m_h;
    }
}
```



## 2.`Open`列表和`Close`列表

我们需要两个数据结构**open**和**close**来存储格子，在之前的过程中，将要被计算周边格子的格子都存储在open当中，当周边格子计算完后，就可以把这个格子存储到close中，然后把它周边的格子再放入到open中。

例如一开始我们把起始格子放入open中，然后从open中取出f(n)值最小的一个格子（**这里使用C#的Linq排序**）去计算它周边的格子。因为此时open中只有一个元素，因此就是计算起始格子周边的格子。接着把起始格子周边8个格子加入到open中，把起始格子从open中删除加入到close中。

然后再从open中找出f(n)最小的格子，将它周边的格子加入到open中，并将自己从open中删除加入到close中，如此循环。

> 如果在C++中，以上步骤应当可以通过`priority_queue`优先队列来实现。

每次计算周边格子的时候，需要判断这些格子是否超出边界，是否是障碍物，是否在close中，这三种情况不需要再处理该格子了。如果格子已经在open中。**若新的g值小于老的g值，就要更新g、f 以及parent的值。**直观理解，`close`列表其实就相当于`visited`数组。

最后如果周边某个格子是终点（代表寻路完成）或者open列表为空（代表可用格子全部计算完，但却没找到终点，死路一条！），则结束寻路过程。

可以发现整个过程都要频繁的用到了增删以及查询，因此open和close使用了Dictionary。

此时核心的AStar类如下：

```c#
public class AStar 
{
    static int FACTOR = 10;//水平竖直相邻格子的距离
    static int FACTOR_DIAGONAL = 14;//对角线相邻格子的距离

    bool m_isInit = false;
    public bool isInit => m_isInit;

    UIGridController[,] m_map;//地图数据
    Int2 m_mapSize;
    Int2 m_player, m_destination;//起始点和结束点坐标
    EvaluationFunctionType m_evaluationFunctionType;//估价方式

    Dictionary<Int2, Node> m_openDic = new Dictionary<Int2, Node>();//准备处理的网格
    Dictionary<Int2, Node> m_closeDic = new Dictionary<Int2, Node>();//完成处理的网格

    Node m_destinationNode;

    public void Init(UIGridController[,] map, Int2 mapSize, Int2 player, Int2 destination, EvaluationFunctionType type = EvaluationFunctionType.Diagonal) {
        m_map = map;
        m_mapSize = mapSize;
        m_player = player;
        m_destination = destination;
        m_evaluationFunctionType = type;

        m_openDic.Clear();
        m_closeDic.Clear();

        m_destinationNode = null;

        //将起始点加入open中
        AddNodeInOpenQueue(new Node(m_player, null, 0, 0));
        m_isInit = true;
    }
}

void AddNodeInOpenQueue(Node node) {
    m_openDic[node.position] = node;
    ShowOrUpdateAStarHint(node);
}
```



## 3.A*寻路的过程

每次按下下一步的时候会调用的函数如下：

```c#
void OnAStarButtonClicked() {
    if(!m_aStar.isInit) {
        m_aStar.Init(m_map, m_mapSize, m_player.position, m_destination.position, evaluationFunctionType);
        m_aStarProcess = m_aStar.Start();
    }
    if(isStepOneByOne) {
        if(!m_aStarProcess.MoveNext()) { //注意这里
            SetHint("寻路完成");
        }
    }
    else {
        while(m_aStarProcess.MoveNext())
            ;
        SetHint("寻路完成");
    }
}
```

在C#中，`IEnumerator`修饰的函数可以通过`MoveNext`迭代到下一轮循环的位置，` m_aStar.Start()`函数如下：

```c#
public IEnumerator Start() {
    while(m_openDic.Count > 0 && m_destinationNode == null) {
        //先按照f的值升序排列，当f值相等时再按照h的值升序排列
        m_openDic = m_openDic.OrderBy(kv => kv.Value.f).ThenBy(kv => kv.Value.h).ToDictionary(p => p.Key, o => o.Value);  //具体细节可以参考这篇：https://zhuanlan.zhihu.com/p/385733813的最下面“补充”部分
        //提取排序后的第一个节点
        Node node = m_openDic.First().Value;
        //因为使用的不是Queue，因此要从open中手动删除该节点
        m_openDic.Remove(node.position);
        //处理该节点相邻的节点
        OperateNeighborNode(node);
        //处理完后将该节点加入close中
        AddNodeInCloseDic(node);
        yield return null;
    }
    if(m_destinationNode == null)
        Debug.LogError("找不到可用路径");
    else
        ShowPath(m_destinationNode);
}

void OperateNeighborNode(Node node) {
    for(int i = -1; i < 2; i++) {
        for(int j = -1; j < 2; j++) {
            
            if(i == 0 && j == 0)
                continue;
            Int2 pos = new Int2(node.position.x + i, node.position.y + j);
            //超出地图范围
            if(pos.x < 0 || pos.x >= m_mapSize.x || pos.y < 0 || pos.y >= m_mapSize.y)
                continue;
            //已经处理过的节点
            if(m_closeDic.ContainsKey(pos))
                continue;
            //障碍物节点
            if(m_map[pos.x, pos.y].state == GridState.Obstacle)
                continue;
            //将相邻节点加入open中
            if(i == 0 || j == 0)
                AddNeighborNodeInQueue(node, pos, FACTOR);
            else
                AddNeighborNodeInQueue(node, pos, FACTOR_DIAGONAL);
        }
    }
}

//将节点加入到open中
void AddNeighborNodeInQueue(Node parentNode, Int2 position, int g) {
    //当前节点的实际距离g等于上个节点的实际距离加上自己到上个节点的实际距离
    int nodeG = parentNode.g + g;
    //如果该位置的节点已经在open中
    if(m_openDic.ContainsKey(position)) {
        //比较实际距离g的值，用更小的值替换
        if(nodeG < m_openDic[position].g) {
            m_openDic[position].g = nodeG;
            m_openDic[position].parent = parentNode;
            ShowOrUpdateAStarHint(m_openDic[position]);
        }
    }
    else {
        //生成新的节点并加入到open中
        Node node = new Node(position, parentNode, nodeG, GetH(position));
        //如果周边有一个是终点，那么说明已经找到了。
        if(position == m_destination)
            m_destinationNode = node;
        else
            AddNodeInOpenQueue(node);
    }
}

//加入open中，并更新网格状态
void AddNodeInOpenQueue(Node node) {
    m_openDic[node.position] = node;
    ShowOrUpdateAStarHint(node);
}

int GetH(Int2 position) {
    if(m_evaluationFunctionType == EvaluationFunctionType.Manhattan)
        return GetManhattanDistance(position);
    else if(m_evaluationFunctionType == EvaluationFunctionType.Diagonal)
        return GetDiagonalDistance(position);
    else
        return Mathf.CeilToInt(GetEuclideanDistance(position));
}

 //寻路完成，显示路径（主要就是修改颜色而已）
void ShowPath(Node node) {
    while(node != null) {
        m_map[node.position.x, node.position.y].ChangeToPathState();
        node = node.parent;
    }
}
```

**通过这样写，就可以实现每按下一次A*寻路的代码就会迭代一步。**