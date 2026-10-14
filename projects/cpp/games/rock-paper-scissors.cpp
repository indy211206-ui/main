#include <iostream>
#include <cstdlib>
#include <ctime>

char uc();
char cc();
void showChoice(char choice);
void chooseWinner(char player, char computer);

int main() {
    char player;
    char computer;

    player = uc();

    std::cout << "You choose: ";
    showChoice(player);

    computer = cc();

    std::cout << "Computer choose: ";
    showChoice(computer);

    chooseWinner(player, computer);

    return 0;
}

char uc() {
    char player;

    do {
        std::cout << "Choose one of following\n";
        std::cout << "**************************\n";
        std::cout << "r for Rock\n";
        std::cout << "p for Paper\n";
        std::cout << "s for Scissor\n";
        std::cout << "Choose your weapon: ";

        std::cin >> player;

        if (player != 'r' && player != 'p' && player != 's') {
            std::cout << "Invalid choice\n";
        }

    } while (player != 'r' && player != 'p' && player != 's');

    return player;
}

char cc() {
    srand(time(NULL));

    int num = rand() % 3 + 1;

    switch (num) {
        case 1: return 'r';
        case 2: return 'p';
        case 3: return 's';
    }

    return 'r';
}

void showChoice(char choice) {
    switch (choice) {
        case 'r':
            std::cout << "Rock\n";
            break;

        case 'p':
            std::cout << "Paper\n";
            break;

        case 's':
            std::cout << "Scissor\n";
            break;
    }
}

void chooseWinner(char player, char computer) {
    switch (player) {

        case 'r':
            if (computer == 'r') {
                std::cout << "It's a tie\n";
            }
            else if (computer == 's') {
                std::cout << "You've won\n";
            }
            else {
                std::cout << "You lost\n";
            }
            break;

        case 'p':
            if (computer == 'p') {
                std::cout << "It's a tie\n";
            }
            else if (computer == 'r') {
                std::cout << "You've won\n";
            }
            else {
                std::cout << "You lost\n";
            }
            break;

        case 's':
            if (computer == 's') {
                std::cout << "It's a tie\n";
            }
            else if (computer == 'p') {
                std::cout << "You've won\n";
            }
            else {
                std::cout << "You lost\n";
            }
            break;
    }
}
