using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace SpaceAccelerateDemo
{
    public class DynamicBVHTest : MonoBehaviour
    {
        private DynamicBVHSpace sahSpace;
        private List<GameObject> seneObjects;
        [Range(0, 10)]
        public int displayDepth;

        public GameObject removeObj;
        public bool dumpTree = false;

        void Start()
        {
            seneObjects = new List<GameObject>();
            sahSpace = new DynamicBVHSpace();
        }

        private int globalIndex = 0;

        private void Update()
        {
            if (Input.GetKeyDown(KeyCode.A)) //A添加物体
            {
                var go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                go.name = "Sphere" + globalIndex++;
                var randomPos = Random.insideUnitSphere * 10;
                go.transform.position = randomPos;
                sahSpace.AddNode(go);
                seneObjects.Add(go);
            }
            if (Input.GetKeyDown(KeyCode.S)) //S删除物体
            {
                if (removeObj != null)
                {
                    sahSpace.RemoveNode(removeObj);
                    Destroy(removeObj);
                    seneObjects.Remove(removeObj);
                }
                else
                {
                    //随机删除一个物体
                    if (seneObjects.Count > 0)
                    {
                        var index = Random.Range(0, seneObjects.Count);
                        var obj = seneObjects[index];
                        sahSpace.RemoveNode(obj);
                        seneObjects.RemoveAt(index);
                        Destroy(obj);
                    }
                }
            }
            
            if(removeObj != null) //用removeObj来表示要移动的物体
            {
                if(removeObj.transform.hasChanged)
                {
                    sahSpace.UpdateNode(removeObj);
                    removeObj.transform.hasChanged = false;
                }
            }

            if (dumpTree)
            {
                sahSpace.DumpTree("DynamicBVHTree.txt");
                dumpTree = false;
            }
        }

        private void OnDrawGizmos()
        {
            //sahSpace?.root?.DrawTargetDepth(displayDepth);
            sahSpace?.root?.DrawDepth(displayDepth);
        }
    }
}

