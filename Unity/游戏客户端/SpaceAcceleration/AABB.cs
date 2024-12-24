using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace SpaceAccelerateDemo
{
    public struct AABB
    {
        public Vector3 minCorner; //左下角
        public Vector3 maxCorner;  //右上角

        public AABB(Vector3 min, Vector3 max)
        {
            this.minCorner = min;
            this.maxCorner = max;
        }
        
        public AABB(AABB aabb)
        {
            this.minCorner = new Vector3(aabb.minCorner.x, aabb.minCorner.y, aabb.minCorner.z);
            this.maxCorner = new Vector3(aabb.maxCorner.x, aabb.maxCorner.y, aabb.maxCorner.z);
        }
        
        public Vector3 Size => maxCorner - minCorner;
        public Vector3 Center => (maxCorner + minCorner) * 0.5f;
        
        public static AABB Reset()
        {
            return new AABB(Vector3.one * float.MaxValue, Vector3.one * float.MinValue);
        }
        
        public static AABB Union(AABB aabb1, AABB aabb2)
        {
            Vector3 minCorner = Vector3.Min(aabb1.minCorner, aabb2.minCorner);
            Vector3 maxCorner = Vector3.Max(aabb1.maxCorner, aabb2.maxCorner);
            return new AABB(minCorner, maxCorner);
        }

        public AABB Union(AABB aabb)
        {
            minCorner.x = Mathf.Min(minCorner.x, aabb.minCorner.x);
            minCorner.y = Mathf.Min(minCorner.y, aabb.minCorner.y);
            minCorner.z = Mathf.Min(minCorner.z, aabb.minCorner.z);

            maxCorner.x = Mathf.Max(maxCorner.x, aabb.maxCorner.x);
            maxCorner.y = Mathf.Max(maxCorner.y, aabb.maxCorner.y);
            maxCorner.z = Mathf.Max(maxCorner.z, aabb.maxCorner.z);

            return new AABB(minCorner, maxCorner);
        }
        
        public float surfaceArea => (Size.x * Size.y + Size.x * Size.z + Size.y * Size.z) * 2.0f;
    }
}

