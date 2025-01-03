#pragma once

#include "Vector.hpp"

class Light
{
public:
    Light(const Vector3f &p, const Vector3f &i) : position(p), intensity(i) {}
    virtual ~Light() = default;
    Vector3f position; //这里指的是光源的左下角
    Vector3f intensity;
};