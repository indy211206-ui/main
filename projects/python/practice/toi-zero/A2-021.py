import sys

def can_do_k(N, K, a1, a2, b1, b2, T):
    routes = []
    for i in range(N):
        for j in range(N):
            t1 = a1[i] + b1[j]
            t2 = a2[i] + b2[j]
            if t1 <= T:
                routes.append((t1, i, 1, j))
            if t2 <= T:
                routes.append((t2, i, 2, j))

    routes.sort()

    used_a = [False] * N
    used_b = [False] * N
    count = 0

    for _, i, c, j in routes:
        if not used_a[i] and not used_b[j]:
            used_a[i] = True
            used_b[j] = True
            count += 1
            if count == K:
                return True

    return count >= K

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N, K = int(input_data[idx]), int(input_data[idx+1])
    idx += 2
    a1 = [int(input_data[idx+i]) for i in range(N)]; idx += N
    a2 = [int(input_data[idx+i]) for i in range(N)]; idx += N
    b1 = [int(input_data[idx+i]) for i in range(N)]; idx += N
    b2 = [int(input_data[idx+i]) for i in range(N)]; idx += N

    lo, hi = 2, 2_000_000
    while lo < hi:
        mid = (lo + hi) // 2
        if can_do_k(N, K, a1, a2, b1, b2, mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

solve()
