#include <iostream>
#include <iomanip>

void showBalance();
double deposit();
double withdraw();

double balance = 0;
int choice;
int main(){

    do{
        std::cout << "******************\n";
        std::cout << "Enter your choice\n";
        std::cout << "******************\n";

        std::cout << "1. Show Balnace\n";
        std::cout << "2. Deposit Money\n";
        std::cout << "3. Withdraw Money\n";
        std::cout << "4. Exit\n";

        std:: cin >> choice;

        switch(choice){
            case 1: showBalance();
                    break;
            case 2: balance += deposit();
                    break;
            case 3: balance -= withdraw();
                    break;
            case 4: std::cout << "Bye.";
            default: std::cout << "invalid output";
        }
}while(choice != 4);
    return 0;

}

void showBalance(){
    std::cout << "Your Balance is: $"
              << std::fixed << std::setprecision(2)
              << balance << std::endl;
}

double deposit(){
    double amount = 0;
    do{
        std::cout << "Deposit Amount: ";
        std::cin >> amount;

        if(amount < 0){
            std::cout << "that's not a valid amount"
                      << std::endl;
        }
    }while(amount < 0);
    return amount;
}

double withdraw(){
    double amount = 0;
    do{
        std::cout << "Withdraw Amount: ";
        std::cin >> amount;

        if(amount < 0){
            std::cout << "that's not a valid amount"
                      << std::endl;
        }
        else if(amount > balance){
            std::cout << "You're too poor for that"
                      << std::endl;
        }
    }while(amount < 0 or amount > balance);
    return amount;
}
