using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace SpaceAccelerateDemo
{
    public class OctreeNode
    {
        public List<GameObject> areaObjects;
        public Vector3 center;
        public float size;  //为了节省空间，这里定义每个node都是正方体，因此用一个float值即可存储size
        
        private const int kidCount = 8; //八叉树，每个节点有8个子节点
        private OctreeNode[] kids;
        public OctreeNode[] Kids => kids;
        public OctreeNode(Vector3 center, float size)
        {
            this.center = center;
            this.size = size;
            areaObjects = new List<GameObject>();
            kids = new OctreeNode[kidCount];
        }
        
        //一些基本的逻辑函数
        public int objectCount => areaObjects.Count;
        public bool isLeaf => kids[0] == null;
        
        public bool Contains(Vector3 position)
        {
            var halfSize = size * 0.5f;
            return Mathf.Abs(position.x - center.x) <= halfSize &&
                   Mathf.Abs(position.y - center.y) <= halfSize &&
                   Mathf.Abs(position.z - center.z) <= halfSize;
        }
        
        public void ClearArea()
        {
            areaObjects.Clear();
        }
        
        public void AddObject(GameObject obj)
        {
            areaObjects.Add(obj);
        }
        
        public void DrawGizmos()
        {
            Gizmos.DrawWireCube(center, Vector3.one * size);
        }
    }
}


