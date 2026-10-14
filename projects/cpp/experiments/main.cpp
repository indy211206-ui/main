#include <bits/stdc++.h>

using namespace std;

class me{
    private:
        string color;
    public:
        me(string color){
            this->color = color;
        }
        string get_color(){
            return color;
        }
        void set_color(string color){
            this->color = color;
        }
};


int main(){

    me* me1 = new me("black");
    me1->set_color("green");
    cout << me1->get_color() << '\n';

    return 0;
}
