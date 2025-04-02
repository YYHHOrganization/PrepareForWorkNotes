#include <iostream>
#include <cstring>
using namespace std;

template<unsigned N, unsigned M>
int compare(const char (&p1)[N], const char (&p2)[M])
{
    return strcmp(p1, p2);
}
int main()
{
    //c++ primer p580
    int res = compare("hi", "mom");
    cout << res << endl; //-1
}