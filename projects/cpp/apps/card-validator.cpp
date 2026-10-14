#include <iostream>
#include <string>

int getDigit(const int n);
int sumOddDigits(const std::string cardn);
int sumEvenDigits(const std::string cardn);

int main()
{
    std::string cardnum;
    int result = 0;

    std::cout << "Enter a credit card #: ";
    std::cin >> cardnum;

    result = sumEvenDigits(cardnum) + sumOddDigits(cardnum);

    if(result %10 == 0){
        std::cout << cardnum << "is valid";
    }
    else{
        std::cout << cardnum << "is not valid";
    }


    return 0;
};

int getDigit(const int n){
    return n % 10 + (n/10 % 10);
}
int sumOddDigits(const std::string cardn){
    int sum = 0;

    for(int i = cardn.size()-2;i>=0;i-=2){
        sum += cardn[i]-'0';
    }
}
int sumEvenDigits(const std::string cardn){
    int sum = 0;

    for(int i = cardn.size()-2;i>=0;i-=2){
        sum += getDigit((cardn[i]-'0')*2);
    }
}
