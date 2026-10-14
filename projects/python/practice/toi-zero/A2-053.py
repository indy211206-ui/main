
def solve():
    name = input().strip()
    n = len(name)
    first = ord(name[0].upper())
    last = ord(name[-1].upper())

    digits = []
    for i in range(1, 11):
        v = i - 1
        if i % 2 == 1:
            val = first + v
        else:
            val = last - v
        val = val % n
        if val > 9:
            val = val % 10
        digits.append(val)

    print(*digits[2:8])


solve()
