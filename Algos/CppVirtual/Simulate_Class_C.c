#include<stdio.h>
typedef struct Hilichurl
{
    int name;
    int age;
    int weight;
} Hilichurl;

//obj中各个字段的值不一定被初始化过，通常还会在类内定义一个类似构造函数的函数指针，这里简化
void desc(Hilichurl* obj)
{
    printf("Name: %d\n", obj->name);
    printf("Age: %d\n", obj->age);
    printf("Weight: %d\n", obj->weight);
}

int main()
{
    Hilichurl h;
    h.name = "Hilichurl1";
    h.age = 10;
    h.weight = 100;

    desc(&h); //直接调用函数指针
    return 0;
}