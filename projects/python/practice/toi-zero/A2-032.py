def solve():
    n, m = map(int, input().split())
    k = int(input())

    grid = [[0] * m for _ in range(n)]

    for _ in range(k):
        r, c = map(int, input().split())
        grid[r][c] += 1

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    best = 0

    for r in range(n):
        for c in range(m):
            if grid[r][c] > 0:
                continue

            total = 0
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    total += grid[nr][nc]

            best = max(best, total)

    print(best)


solve()
