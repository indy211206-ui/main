#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

string decimalToBase36(long long n) {
    const string digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    if (n == 0)
        return "0";

    string result;

    while (n > 0) {
        int remainder = n % 36;
        result += digits[remainder];
        n /= 36;
    }

    reverse(result.begin(), result.end());

    return result;
}

int main() {
    long long n;
    cin >> n;

    cout << decimalToBase36(n) << endl;

    return 0;
}
