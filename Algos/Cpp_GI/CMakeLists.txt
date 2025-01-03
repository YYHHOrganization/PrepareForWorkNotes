cmake_minimum_required(VERSION 3.10) # 指定CMake的最低版本
project(PathTracingDemo) 
add_executable(BeautifulCpp main.cpp Object.hpp Vector.cpp Vector.hpp Sphere.hpp global.hpp Triangle.hpp Scene.cpp
        Scene.hpp Light.hpp AreaLight.hpp BVH.cpp BVH.hpp Bounds3.hpp Ray.hpp Material.hpp Intersection.hpp
        Renderer.cpp Renderer.hpp)
set_target_properties(BeautifulCpp PROPERTIES CXX_STANDARD 17)