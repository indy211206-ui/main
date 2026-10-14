def solve():
    MOD = 2 ** 15 + 9


    A = []
    for _ in range(3):
        row = list(map(int, input().split()))
        A.append(row)


    B = []
    for _ in range(3):
        row = list(map(int, input().split()))
        B.append(row)


    C = []
    for i in range(3):
        row = []
        for j in range(3):
            val = 0
            for k in range(3):
                val += A[i][k] * B[k][j]

            row.append(val % MOD)
        C.append(row)


    for row in C:
        print(*row)


solve()
