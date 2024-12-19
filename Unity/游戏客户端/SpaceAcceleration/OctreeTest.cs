using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.TextCore.Text;
using Random = UnityEngine.Random;

namespace SpaceAccelerateDemo
{
    public enum OctreeDebugMode
    {
        AllDepth,
        TargetDepth
    }
    public class OctreeTest : MonoBehaviour
    {
        //生成物体数量
        [Range(0, 500)]
        public int genCount = 100;

        //Octree 构建最大深度
        [Range(1, 8)]
        public int buildDepth = 3;
        public OctreeNode root;

        //物体生成范围
        [Range(1, 300)]
        public float range = 100;
        
        public bool debugDraw = true; //是否绘制八叉树
        public OctreeDebugMode octreeDebugMode;
        [Range(1,3)]
        public int targetDisplayDepth = 1;

        public bool doQueryTest = false;
        public Transform queryTransform;
        private List<GameObject> queryObjects; //临近物体的列表，用于找到最近的物体
        private OctreeNode queryNode; //查询到的最终节点，会递归找到叶子节点，将其可视化为绿色

        private void Update()
        {
            if (doQueryTest)
            {
                if(queryObjects != null)
                    queryObjects.Clear();
                queryObjects = new List<GameObject>();
                queryNode = null;
                QueryNearestObject(root, queryTransform.position);
            }
        }
        
        private void QueryNearestObject(OctreeNode node, Vector3 position)
        {
            if (node.isLeaf)
            {
                queryNode = node;
                queryObjects.AddRange(node.areaObjects);
                return;
            }
            for (int i = 0; i < 8; i++)
            {
                if (node.Kids[i].Contains(position))
                {
                    QueryNearestObject(node.Kids[i], position);
                }
            }
        }

        //记录生成的场景物体
        private List<GameObject> sceneObjects;
        private void Start()
        {
            GenSceneObjects();
            OctreePartion();
        }
        
        private void GenSceneObjects()
        {
            float genRange = range * 0.5f;
            sceneObjects = new List<GameObject>();
            for (int i = 0; i < genCount; i++)
            {
                var obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
                obj.transform.position = new Vector3(Random.Range(-genRange, genRange), 0, Random.Range(-genRange, genRange));
                obj.hideFlags = HideFlags.HideInHierarchy; //隐藏在Hierarchy面板
                sceneObjects.Add(obj);
            }
        }
        
        private void OctreePartion()
        {
            root = new OctreeNode(Vector3.zero, range);
            root.areaObjects.AddRange(sceneObjects);
            BuildOctree(root, 0);
        }
        
        private void DrawOctree(OctreeNode node, int depth)
        {
            //AllDepth:绘制所有深度的八叉树
            if (octreeDebugMode == OctreeDebugMode.AllDepth)
            {
                node.DrawGizmos();
                if (node.isLeaf)
                {
                    return; 
                }
                for (int i = 0; i < 8; i++)
                {
                    DrawOctree(node.Kids[i], depth + 1);
                }
            }
            //TargetDepth:绘制目标深度的八叉树
            else if (octreeDebugMode == OctreeDebugMode.TargetDepth)
            {
                if (depth == targetDisplayDepth)
                {
                    Gizmos.color = Color.yellow;
                    node.DrawGizmos();
                }
                if (node.isLeaf)
                {
                    return;
                }
                for (int i = 0; i < 8; i++)
                {
                    DrawOctree(node.Kids[i], depth + 1);
                }
            }
        }
        
        private void OnDrawGizmos()
        {
            if (root == null || !debugDraw)
            {
                return;
            }
            DrawOctree(root,0);
            if (queryNode != null)  //gizmos相关调用只能在OnDrawGizmos中调用
            {
                Gizmos.color = Color.green;
                queryNode.DrawGizmos();
                //找到最近的物体，绘制一条红色的线连过去
                GameObject nearestObj = null;
                float minDistance = float.MaxValue;
                foreach (var obj in queryObjects)
                {
                    var distance = Vector3.Distance(obj.transform.position, queryTransform.position);
                    if (distance < minDistance)
                    {
                        minDistance = distance;
                        nearestObj = obj;
                    }
                }
                if (nearestObj != null)
                {
                    Gizmos.color = Color.red;
                    Gizmos.DrawLine(nearestObj.transform.position, queryTransform.position);
                }
            }
        }
        
        private void BuildOctree(OctreeNode node, int depth)
        {
            if (depth >= buildDepth)
            {
                return;
            }
            if (node.objectCount <= 1)
            {
                return;
            }
            var halfSize = node.size * 0.5f;
            for (int i = 0; i < 8; i++)
            {
                var center = node.center;
                //根据i的二进制位来判断是在左还是右,前还是后,上还是下,i=0~7分别是000，001，010，011，100，101，110，111
                center.x += (i & 1) == 0 ? halfSize * 0.5f : -halfSize * 0.5f;
                center.y += (i & 2) == 0 ? halfSize * 0.5f : -halfSize * 0.5f;
                center.z += (i & 4) == 0 ? halfSize * 0.5f : -halfSize * 0.5f;
                var newNode = new OctreeNode(center, halfSize);
                node.Kids[i] = newNode;
                newNode.areaObjects = node.areaObjects.FindAll(obj => newNode.Contains(obj.transform.position));
                BuildOctree(newNode, depth + 1);
            }
        }
    }
}

