#include<iostream>
#include<string>
using namespace std;

class Monster
{
public:
    Monster(string name, int id, int hp) : name(name), id(id), hp(hp) {}
    virtual void desc()
    {
        cout << "Name: " << name << endl;
        cout << "ID: " << id << endl;
        cout << "HP: " << hp << endl;
    }

    virtual void attack()
    {
        cout<<"Monster attack!"<<endl;
    }
    string name;
    int id;
    int hp;
};

class Hilichurl : public Monster
{
public:
    Hilichurl(string name, int id, int hp, int atk) : Monster(name, id, hp), atk(atk) {}
    void desc()
    {
        cout << "Name: " << name << endl;
        cout << "ID: " << id << endl;
        cout << "HP: " << hp << endl;
        cout << "ATK: " << atk << endl;
    }

    void attack()
    {
        cout<<"Hilichurl attack!"<<endl;
    }

    int atk;
};

int main()
{
    Hilichurl h("Hilichurl1", 1, 100, 10);
    h.desc();
    Monster* m = &h; //父类指针指向子类对象
    m->desc(); //调用子类的desc

    Monster& m2 = h; //父类引用指向子类对象
    m2.desc(); //调用子类的desc
    m2.attack();
    return 0;
}