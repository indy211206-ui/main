#include <iostream>
#include <ctime>

int main() {
    srand(time(0));
    int n = rand() % 10 + 1;
    int guess;
    int attempts = 0;
    std::cout << "********NUMBER GUESSING GAME********" << std::endl;
    do{
        std::cout << "Guess the number from 1 to 10:" << std::endl;
        std::cin >> guess;
        if (guess == n) {
            std::cout << "Congratulations! You guessed the number in " << attempts + 1 << " attempts." << std::endl;
            break;
        } else {
            std::cout << "Wrong guess! Try again." << std::endl;
            attempts++;
        }
    }
    while(guess != n);
    std::cout << "The number was: " << n << std::endl;
    std::cout << "****************************************" << std::endl;
}
