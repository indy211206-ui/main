def spiralize(n):
    grid = [[0] * n for _ in range(n)]

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d = 0

    r = c = 0

    for _ in range(n * n):
        grid[r][c] = 1


        nr = r + dirs[d][0]
        nc = c + dirs[d][1]

        def can_move(x, y):
            if not (0 <= x < n and 0 <= y < n):
                return False
            if grid[x][y] == 1:
                return False


            for dx, dy in dirs:
                ax, ay = x + dx, y + dy
                if (0 <= ax < n and 0 <= ay < n):
                    if (ax, ay) != (r, c) and grid[ax][ay] == 1:
                        return False

            return True

        if can_move(nr, nc):
            r, c = nr, nc
        else:
            d = (d + 1) % 4

            nr = r + dirs[d][0]
            nc = c + dirs[d][1]

            if not can_move(nr, nc):
                break

            r, c = nr, nc
    return grid
for line in spiralize(5):
    print(line)
