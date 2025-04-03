using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace SpaceAccelerateDemo
{
    public class BVHNode
    {
        public BVHNode leftNode;
        public BVHNode rightNode;
        public BVHNode parent;

        public AABB aabb { get; private set; }
        public List<GameObject> sceneObjects; //BVH节点包含的物体
        
        #region Debug
        public string Name { get; private set; } //BVH节点的名字
        private Color spaceColor; //BVH节点的颜色
        #endregion
        
        public float surfaceArea => aabb.surfaceArea;
        private void InitializeAABB()
        {
            this.aabb = AABB.Reset();
            if (sceneObjects == null || sceneObjects.Count==0) return;
            //计算AABB,遍历sceneObjects，找到公共包围盒
            foreach (var obj in sceneObjects)
            {
                var aabb = ComputeWorldAABB(obj);
                this.aabb = this.aabb.Union(aabb);
            }
        }
        
        public void DumpSceneObject(System.IO.StreamWriter file)
        {
            if (sceneObjects == null) return;
            foreach (var obj in sceneObjects)
            {
                file.WriteLine("    " + obj.name);
            }
        }
        
        public BVHNode(string name, List<GameObject> objs)
        {
            sceneObjects = objs;
            InitializeAABB();
            Name = name;
            spaceColor = new Color(Random.value, Random.value, Random.value, 0.9f);
        }
        
        public void DrawGizmos()
        {
            Gizmos.color = spaceColor;
            Gizmos.DrawWireCube(this.aabb.Center, this.aabb.Size);
            Gizmos.DrawSphere(this.aabb.minCorner, 0.1f);
            Gizmos.DrawSphere(this.aabb.maxCorner, 0.1f);
        }
        
        public void UnionAABB(AABB other)
        {
            this.aabb = this.aabb.Union(other);
        }
        
        public static AABB ComputeWorldAABB(GameObject obj)
        {
            var mesh = obj.GetComponent<MeshFilter>().sharedMesh;
            var localMin = mesh.bounds.min;
            var localMax = mesh.bounds.max;
            var worldMin = obj.transform.TransformPoint(localMin);
            var worldMax = obj.transform.TransformPoint(localMax);
            return new AABB(worldMin, worldMax);
        }
        
        public void SetLeaf(BVHNode left, BVHNode right)
        {
            leftNode = left;
            rightNode = right;
            if(leftNode!=null) leftNode.parent = this;
            if(rightNode!=null) rightNode.parent = this;
            //if(this.sceneObjects!=null) this.sceneObjects.Clear();  //note：造成bug的一句！原来写了这句，有bug，因为这里的sceneObjects是引用，会导致左右节点的sceneObjects也被清空
            //静态BVH不会报错是因为left和right的sceneObjects是新建的，而不是引用
            this.sceneObjects = null;
        }
        
        public void DrawDepth(int depth)
        {
            if (depth != 0)
            {
                DrawGizmos();
                this.rightNode?.DrawDepth(depth - 1);
                this.leftNode?.DrawDepth(depth - 1);
            }
            // if (this.sceneObjects != null && this.sceneObjects.Count==1)
            // {
            //     DrawGizmos();
            //     return;
            // }
            // this.rightNode?.DrawDepth(depth - 1);
            // this.leftNode?.DrawDepth(depth - 1);
        }
        

        public void DrawTargetDepth(int depth)
        {
            if (depth <= 0)
            {
                DrawGizmos();
            }
            else
            {
                this.rightNode?.DrawTargetDepth(depth - 1);
                this.leftNode?.DrawTargetDepth(depth - 1);
            }
        }
        
        
        #region 与动态BVH相关
        
        public bool isLeaf => this.sceneObjects != null; //判断是否是叶子节点,如果是叶子节点，sceneObjects不为空
        
        //复制一个节点
        public BVHNode(BVHNode source)
        {
            this.aabb = new AABB(source.aabb);
            this.sceneObjects = source.sceneObjects;
            this.leftNode = source.leftNode;
            this.rightNode = source.rightNode;
            //注：这里没有复制parent，因为在动态BVH中，拷贝出来的节点的parent本来就要重新设置
            this.Name = source.Name + "_copy";
            this.spaceColor = new Color(Random.value, Random.value, Random.value, 0.9f);
        }
        
        //获取兄弟节点
        public BVHNode GetSibling()
        {
            return this.parent?.GetTheOtherNode(this);
        }
        
        private BVHNode GetTheOtherNode(BVHNode brother)
        {
            if (this.leftNode == brother) return this.rightNode;
            if (this.rightNode == brother) return this.leftNode;
            return null;
        }
        
        //查找根节点
        public BVHNode FindRoot()
        {
            if (this.parent != null)
            {
                return parent.FindRoot();
            }
            return this;
        }
        
        //合并两个节点,sourcenode的内容会被合并到targetnode中
        public static BVHNode Merge(BVHNode targetNode, BVHNode sourceNode)
        {
            //step1:复制出一个targetNode，取名为copyNode
            BVHNode copyNode = new BVHNode(targetNode);
            //step2:合并source的AABB到targetNode, 并且更新整条树的链的AABB
            targetNode.UnionAABB(sourceNode.aabb);
            targetNode.AABBBroadCast();
            //step3：将targetNode作为copyNode和sourceNode的父节点
            targetNode.SetLeaf(copyNode, sourceNode);
            return copyNode; //返回原来的targetNode
        }
        
        //分离节点,beSeperatedNode是要分离的节点
        public static BVHNode Separate(BVHNode beSeperatedNode)
        {
            //step1:找到父节点和兄弟节点
            BVHNode parent = beSeperatedNode.parent;
            if (parent != null && parent.Contains(beSeperatedNode))
            {
                BVHNode brother = beSeperatedNode.GetSibling();
                //step2:将brother的内容复制到parent中
                var brotherAABB = brother.aabb;
                parent.SetLeaf(brother.leftNode, brother.rightNode);
                parent.aabb = brotherAABB;
                parent.AABBBroadCast();
                parent.sceneObjects = brother.sceneObjects;
                
                //step3:删除beSeperatedNode和brother节点
                //应当会自己GC,毕竟没人引用了
                
                return parent;
            }
            Debug.LogWarning("Separate Warning: beSeperatedNode is not a child of parent");
            return null;
        }
        
        //检查节点是否为子节点
        private bool Contains(BVHNode node)
        {
            return this.leftNode == node || this.rightNode == node;
        }
        
        private void AABBBroadCast()
        {
            if (this.parent != null)
            {
                this.parent.UpdateAABB();
                this.parent.AABBBroadCast();
            }
        }
        
        public void UpdateAABB()
        {
            this.aabb = AABB.Reset(); //重新计算AABB，左右节点的AABB求并
            if (leftNode != null)
            {
                UnionAABB(leftNode.aabb);
            }

            if (rightNode != null)
            {
                UnionAABB(rightNode.aabb);
            }
        }

        #endregion
        
    }

    public class BVHSpace
    {
        public BVHNode root { get; private set; }
        
        public void BuildBVH(List<GameObject> sceneObjects, int depth, int type=1)
        {
            root = new BVHNode("root", null);
            foreach (var obj in sceneObjects)
            {
                var aabb = BVHNode.ComputeWorldAABB(obj);
                root.UnionAABB(aabb);
            }
            if(type==0)
                BinaryPartition(root, sceneObjects, 0, sceneObjects.Count, depth);
            else if(type==1)
                AxisPartition(root, sceneObjects, depth);
        }
        
        //最大方差轴分割
        private void AxisPartition(BVHNode node, List<GameObject> sceneObjects, int depth)
        {
            if ( (node.sceneObjects!=null && node.sceneObjects.Count == 1) || depth <=0) return;
            
            var leftNodeSceneObjects = new List<GameObject>();
            var rightNodeSceneObjects = new List<GameObject>();
            
            int mode = PickVariance(sceneObjects);
            float centerMode = node.aabb.Center[mode]; //对应轴的中心
            foreach (var obj in sceneObjects)
            {
                var objCenter = obj.transform.position[mode];
                if (objCenter < centerMode)
                {
                    leftNodeSceneObjects.Add(obj);
                }
                else
                {
                    rightNodeSceneObjects.Add(obj);
                }
            }
            
            var leftNode = new BVHNode(node.Name + "_leftKid_" + depth.ToString(), leftNodeSceneObjects);
            var rightNode = new BVHNode(node.Name + "_rightKid_" + depth.ToString(), rightNodeSceneObjects);
            node.SetLeaf(leftNode, rightNode);
            //递归
            AxisPartition(leftNode, leftNodeSceneObjects, depth - 1);
            AxisPartition(rightNode, rightNodeSceneObjects, depth - 1);
        }
        
        //选择方差最大的轴
        private int PickVariance(List<GameObject> sceneObjects)
        {
            var maxVariance = float.MinValue;
            var maxIndex = 0;
            for (int i = 0; i < 3; i++)
            {
                var variance = ComputeVariance(sceneObjects, i);
                if (variance > maxVariance)
                {
                    maxVariance = variance;
                    maxIndex = i;
                }
            }
            return maxIndex;
        }
        
        private float ComputeVariance(List<GameObject> sceneObjects, int axis)
        {
            var center = Vector3.zero;
            foreach (var obj in sceneObjects)
            {
                center += obj.transform.position;
            }
            center /= sceneObjects.Count;
            var variance = 0.0f;
            foreach (var obj in sceneObjects)
            {
                variance += Mathf.Pow(obj.transform.position[axis] - center[axis], 2);
            }
            return variance;
        }
        
        //二分递归划分
        private void BinaryPartition(BVHNode node, List<GameObject> objs, int startIndex, int endIndex, int depth)
        {
            if ( (node.sceneObjects!=null && node.sceneObjects.Count == 1) || depth <=0) return;

            //计算二分下标
            var halfIndex = (endIndex + startIndex) / 2;
            //把对应的物体分配到左右子节点
            var leftNode = new BVHNode(node.Name + "_leftKid_" + depth.ToString(), new List<GameObject>(objs.GetRange(startIndex, halfIndex - startIndex)));
            var rightNode = new BVHNode(node.Name + "_rightKid_" + depth.ToString(), new List<GameObject>(objs.GetRange(halfIndex, endIndex - halfIndex)));
            
            node.SetLeaf(leftNode, rightNode);

            //前半部分递归
            BinaryPartition(leftNode, objs, startIndex, halfIndex, depth - 1);
            //后半部分递归
            BinaryPartition(rightNode, objs, halfIndex, endIndex, depth - 1);
        }

        public void DumpTree(string filename = "BVHTree.txt")
        {
            if (root == null) return;
            System.IO.File.WriteAllText(filename, string.Empty);
            DumpNode(root, filename);
        }
        
        private void DumpNode(BVHNode node, string filename)
        {
            if (node == null) return;
            using (System.IO.StreamWriter file = new System.IO.StreamWriter(filename, true))
            {
                //用层序遍历的方法遍历BVH树
                Queue<BVHNode> queue = new Queue<BVHNode>();
                queue.Enqueue(node);
                while (queue.Count > 0)
                {
                    var curNode = queue.Dequeue();
                    file.WriteLine(curNode.Name);
                    curNode.DumpSceneObject(file);
                    if (curNode.leftNode != null)
                    {
                        queue.Enqueue(curNode.leftNode);
                    }
                    if (curNode.rightNode != null)
                    {
                        queue.Enqueue(curNode.rightNode);
                    }
                }
            }
        }
        
    }

    public class DynamicBVHSpace
    {
        public BVHNode root { get; private set; }
        //维护一个当前bvh的所有叶子结点列表
        private List<BVHNode> leafs;
        private int generateCount = 0;
        
        //游戏对象与节点的映射
        public Dictionary<GameObject, BVHNode> gameObjectToNode;
        
        public DynamicBVHSpace()
        {
            leafs = new List<BVHNode>();
            gameObjectToNode = new Dictionary<GameObject, BVHNode>();
        }
        
        //更新、记录游戏对象与节点的映射关系
        private void RecordGameobject(BVHNode node)
        {
            GameObject obj = null;
            if (node!=null && node.sceneObjects != null && node.sceneObjects.Count > 0) obj = node.sceneObjects[0];
            if (obj != null)
            {
                if (gameObjectToNode.ContainsKey(obj))
                {
                    gameObjectToNode[obj] = node;
                }
                else
                {
                    gameObjectToNode.Add(obj, node);
                }
            }
        }


        //添加一个节点
        public BVHNode AddNode(GameObject go)
        {
            BVHNode leaf = new BVHNode("node_" + generateCount.ToString(), new List<GameObject>(){go});
            RecordGameobject(leaf);
            BuildBVH(leaf);
            generateCount++;
            return leaf;
        }

        //删除一个节点,传入的是对应的obj
        public bool RemoveNode(GameObject go)
        {
            if (gameObjectToNode.TryGetValue(go, out var node))
            {
                //step1:在leafs中移除目标节点及其兄弟节点
                leafs.Remove(node);
                leafs.Remove(node.GetSibling()); //如果兄弟节点不是叶子节点，那么不会影响
                //step2:分离节点
                BVHNode subTree = BVHNode.Separate(node); //分离后的子树根节点
                //step3:更新映射,移除后有可能返回的是叶子节点，也有可能不是叶子节点
                if (subTree!=null && subTree.isLeaf)
                {
                    leafs.Add(subTree);
                    RecordGameobject(subTree);
                }

                return true;
            }

            return false;
        }
        
        //找到最佳叶子节点
        private BVHNode findBestLeaf(BVHNode node)
        {
            BVHNode bestLeaf = null;
            float minCost = float.MaxValue;
            foreach (var leaf in leafs)
            {
                var leafAABB = new AABB(leaf.aabb); //复制一个AABB,避免修改原来的AABB,这就是C#引用传递的福报
                var newBranchAABB = AABB.Union(leafAABB, node.aabb);
                //新增的分支节点表面积,新引入的
                float deltaCost = newBranchAABB.surfaceArea;
                float wholeCost = deltaCost;
                var parent = leaf.parent;

                //统计所有祖先节点的表面积差
                while (parent != null)
                {
                    var s2 = parent.surfaceArea;
                    var unionAABB = AABB.Union(parent.aabb, node.aabb);
                    var s3 = unionAABB.surfaceArea;
                    deltaCost = s3 - s2;  //对于父节点链上的节点的AABB的影响
                    wholeCost += deltaCost;
                    parent = parent.parent;
                }

                //返回最小的目标
                if (wholeCost < minCost)
                {
                    bestLeaf = leaf;
                    minCost = wholeCost;
                }
            }
            return bestLeaf;
        }
        
        //构建bvh
        public void BuildBVH(BVHNode leaf)
        {
            if (root == null) //第一次构建
            {
                root = leaf;
                leafs.Add(leaf);
                return;
            }
            //step1:找到最佳叶子节点
            BVHNode bestLeaf = findBestLeaf(leaf);
            if (bestLeaf == null)
            {
                Debug.LogWarning("SAH Can't find best leaf, default to use leaf0");
                bestLeaf = leafs[0];
            }
            //step2:合并节点
            BVHNode newNode = BVHNode.Merge(bestLeaf, leaf);
            //step3:更新叶子节点列表
            leafs.Add(leaf);
            leafs.Add(newNode); //添加了两个新的
            leafs.Remove(bestLeaf); //删除老的
            
            //step4：记录映射并更新根节点
            RecordGameobject(newNode);
            root = newNode.FindRoot(); //记得更新root
        }
        
        public void UpdateNode(GameObject go)
        {
            if (RemoveNode(go))
            {
                AddNode(go);
            }
        }
        
        //for debug
        public void DumpTree(string filename = "BVHTree.txt")
        {
            if (root == null) return;
            System.IO.File.WriteAllText(filename, string.Empty);
            DumpNode(root, filename);
        }
        
        private void DumpNode(BVHNode node, string filename)
        {
            if (node == null) return;
            int level = 0;
            using (System.IO.StreamWriter file = new System.IO.StreamWriter(filename, true))
            {
                //用层序遍历的方法遍历BVH树
                Queue<BVHNode> queue = new Queue<BVHNode>();
                queue.Enqueue(node);
                while (queue.Count > 0)
                {
                    int cnt = queue.Count;
                    file.WriteLine("--------------------Level " + level.ToString() + "--------------------");
                    while (cnt-- > 0)
                    {
                        var curNode = queue.Dequeue();
                        file.WriteLine(curNode.Name);
                        curNode.DumpSceneObject(file);
                        if (curNode.leftNode != null)
                        {
                            queue.Enqueue(curNode.leftNode);
                        }
                        if (curNode.rightNode != null)
                        {
                            queue.Enqueue(curNode.rightNode);
                        }
                    }
                    level++;
                }
                
            }
        }
    }
}

