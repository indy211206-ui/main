rows, cols = map(int, input().split())
rabbit_r, rabbit_c = map(int, input().split())
n = int(input())

grid = [[0] * cols for _ in range(rows)]
for _ in range(n):
    ir, ic = map(int, input().split())

    for r in range(rows):
        for c in range(cols):
            dist = max(abs(r - ir), abs(c - ic))

            if dist == 0:
                risk = 100
            elif dist == 1:
                risk = 60
            elif dist == 2:
                risk = 20
            else:
                risk = 0

            grid[r][c] = max(grid[r][c], risk)

safe = sum(1 for r in range(rows) for c in range(cols) if grid[r][c] == 0)

rabbit_risk = grid[rabbit_r][rabbit_c]

print(safe)
print(f"{rabbit_risk}%")
