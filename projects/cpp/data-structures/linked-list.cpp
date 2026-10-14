#include <bits/stdc++.h>

using namespace std;

class Node{
    public:
        int value;
        Node* next;

        Node(int val){
            value = val;
            this->next = nullptr;
        }
};
class linkedList{
    private:
        Node* head;
        Node* tail;
        int len;
    public:

        linkedList(int value){
            Node* newNode = new Node(value);
            head = newNode;
            tail = newNode;
            len = 1;
        }
        ~linkedList(){
            Node* temp = head;
            while(head){
                head = head->next;
                delete temp;
                temp = head;
            }
        }
        void printList() {
            Node* temp = head;
            while (temp){
                cout << temp->value << endl;
                temp = temp->next;
            }
        }
        void getHead(){
            cout << "Head: " << head->value << endl;
        }
        void getTail(){
            cout << "Tail: " << tail->value << endl;
        }
        void getLength(){
            cout << "length: " << len << endl;
        }
        void append(int v){
            Node* newNode = new Node(v);
            if(!head){
                head = newNode;
                tail = newNode;
            }
            else{
                tail->next = newNode;
                tail = newNode;
            }
            len++;
        }
        void deleteLast(){
            if(len == 0)return;

            Node* temp = head;
            if(len == 0){
                head = nullptr;
                tail = nullptr;
            }else {
            Node* pre = head;

            while(temp->next){
                pre = temp;
                temp = temp->next;
            }
            tail = pre;
            tail->next = nullptr;
        }
            delete temp;
            len--;
        }
        void prepend(int v){
            Node* newNode = new Node(v);

            if(head){
                head = newNode;
                tail = newNode;
            } else{
                newNode->next = head;
                head = newNode;
            }
            len++;
        }
        void deleteFirst(){
            if(len == 0)return;
            Node* temp = head;
            if(len == 1){
                head = nullptr;
                tail = nullptr;

            }else {
                head = head->next;
            }
            delete temp;
            len--;
        }
        Node* get(int index){
            if(index < 0 || index >= len){
                return nullptr;
            }
            Node* temp = head;
            for(int i = 0; i < index;i++){
                temp = temp->next;
            }
            return temp;
        }
        bool set(int ind,int val){
            Node* temp = get(ind);

            if (temp){
                temp->value = val;
                return true;
            }
            return false;
        }
        bool insert(int ind, int val){
            if(ind < 0 || ind > len)return false;
            if(ind == 0){
                prepend(val);
                return true;
            }
            if(ind == len){
                append(val);
                return true;
            }
            Node* newNode = new Node(val);
            Node* temp = get(ind -1);

            newNode->next = temp->next;
            temp->next = newNode;
            len++;
            delete temp;
            return true;
        }

};
int main(){
    linkedList* list = new linkedList(4);

    list->append(5);
    list->append(6);
    list->append(7);
    list->append(8);

    list->insert(2, 888);
    list->printList();
}
