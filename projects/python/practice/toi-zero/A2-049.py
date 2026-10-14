def solve():
    MOD = 2 ** 15 + 9  # = 32777

    # Read matrix A (3x3)
    A = []
    for _ in range(3):
        row = list(map(int, input().split()))
        A.append(row)

    # Read matrix B (3x3)
    B = []
    for _ in range(3):
        row = list(map(int, input().split()))
        B.append(row)

    # Multiply A x B, then mod each element
    C = []
    for i in range(3):
        row = []
        for j in range(3):
            val = 0
            for k in range(3):
                val += A[i][k] * B[k][j]
            # mod must be non-negative
            row.append(val % MOD)
        C.append(row)

    # Print result
    for row in C:
        print(*row)


solve()
