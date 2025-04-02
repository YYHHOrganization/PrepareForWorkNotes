using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Random = UnityEngine.Random;

namespace SpaceAccelerateDemo
{
    public class BVHTest : MonoBehaviour
    {
        private BVHSpace binarySpace;

        [Range(1, 100)]
        public int generateCount = 10;
        private List<GameObject> seneObjects;

        [Range(0, 10)]
        public int partionDepth = 4;
        [Range(0, 10)]
        public int displayDepth;

        public enum GenerateType
        {
            Ordered,
            Random
        }

        public GenerateType generateType;
        public bool debugTreeNode = true;

        private void Start()
        {
            seneObjects = new List<GameObject>();
            binarySpace = new BVHSpace();

            CreateScene();
            if (debugTreeNode)
            {
                DumpTreeNodeInfos("BVHTree.txt");
            }
        }

        private void DumpTreeNodeInfos(string filename)
        {
            binarySpace.DumpTree(filename);
        }
        
        private void CreateScene()
        {
            var halfCount = generateCount * 0.5f;
            for (int i = 0; i < generateCount; i++)
            {
                var go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                var positionX = i - halfCount;
                var randomPos = Random.insideUnitSphere * 10;
                if (generateType == GenerateType.Ordered)
                {
                    go.transform.position = new Vector3(positionX, randomPos.y, randomPos.z);
                }
                else
                {
                    go.transform.position = randomPos;
                }
                go.name = "Sphere_" + i.ToString();

                seneObjects.Add(go);
            }

            binarySpace.BuildBVH(seneObjects, partionDepth);
        }

        private void OnDrawGizmos()
        {
            binarySpace?.root?.DrawTargetDepth(displayDepth);
        }
    }
}

