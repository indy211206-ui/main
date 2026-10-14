#include <bits/stdc++.h>

using namespace std;

class Node {
    public:
        int value;
        Node* next;
        Node* prev;

        Node(int value){
            this->value = value;
            next = nullptr;
            prev = nullptr;
        }
};

class DoublyLinkedList{
    private:
        Node* head;
        Node* tail;
        int len;

    public:
        DoublyLinkedList(int value){
            Node* newNode = new Node(value);
            head = newNode;
            tail = newNode;
            len = 1;
        }

        void printl(){
            Node* temp= head;
            while(temp){
                cout << temp->value << " ";
                temp = temp->next;
            }
            cout << endl;
        }
        void append(int val){
            Node* newNode = new Node(val);
            if(!head){
                head = newNode;
                tail = newNode;
            }else{
                tail->next = newNode;
                newNode->prev = tail;
                tail = newNode;
            }
            len++;
        }
        void deleteLast(){
            if(!head)return;
            Node* temp = tail;
            if(!head->next){
                head = nullptr;
                tail = nullptr;
            }else{
                tail = tail->prev;
                tail->next = nullptr;
            }
            delete temp;
            len--;
        }
        void prepend(int val){
            Node* newNode = new Node(val);
            if(!head){
                head = newNode;
                tail = newNode;
            }else{
                newNode->next = head;
                head->prev = newNode;
                head = newNode;
            }
            len++;
        }
        void deleteFirst(){
            if(!head)return;
            Node* temp = head;
            if(!head->next){
                head = nullptr;
                tail = nullptr;
            }else{
                head = head->next;
                head->prev = nullptr;
            }
            delete temp;
            len--;
        }
        Node* get(int index){
            if(index < 0 || index >= len)return nullptr;
            Node* temp = head;
            if(index < len/2){
                for(int i=0;i<index;i++){
                    temp = temp->next;
                }
            }else{
                temp = tail;
                for(int i = len-1;i>index;i--){
                    temp = temp->prev;
                }
            }
            return temp;
        }
        bool set(int index, int val){
            Node* temp = get(index);
            if(temp){
                temp->value = val;
                return true;
            }
            return false;
        }
        bool insert(int index,int val){
            if(index < 0 || index > len)return false;
            if(index == 0){
                prepend(val);
                return true;
            }
            if(index == len){
                append(val);
                return true;
            }
            Node* newNode = new Node(val);
            Node* before = get(index-1);
            Node* after = before->next;

            newNode->prev = before;
            newNode->next = after;
            before->next = newNode;
            after->prev = newNode;
            len++;
            return true;
        }
        void deleteNode(int index){
            if(index < 0 || index >= len)return;
            if(index==0){
                deleteFirst();
                return;
            }
            if(index==len-1){
                deleteLast();
                return;
            }
            Node* temp = get(index);
            temp->next->prev = temp->prev;
            temp->prev->next = temp->next;

            delete temp;
            len--;
        }
};

int main(){
    DoublyLinkedList* dll = new DoublyLinkedList(7);

    dll->append(10);
    dll->append(1);
    dll->deleteFirst();

    dll->prepend(67);
    dll->insert(1,69);
    dll->printl();
    dll->deleteNode(1);
    dll->printl();
}
