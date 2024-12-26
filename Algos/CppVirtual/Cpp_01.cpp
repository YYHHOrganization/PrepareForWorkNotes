#include <iostream>
using namespace std;

class Hilichurl
{
public:
    int name;
    int age;
    int weight;
    void desc()
    {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "Weight: " << weight << endl;
    }
};

int main()
{
    Hilichurl h;
    h.name = 1;
    h.age = 10;
    h.weight = 100;

    h.desc();
    return 0;
}