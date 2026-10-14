def flood():
    rows, cols = map(int, input().split())


    grid = []
    for r in range(rows):
        row = input().split()
        grid.append(row)


    next_grid = []
    for r in range(rows):
        next_row = []
        for c in range(cols):
            next_row.append(grid[r][c])
        next_grid.append(next_row)


    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '*':

                if r + 1 < rows:
                    next_grid[r + 1][c] = '*'


    for r in range(rows):
        print(' '.join(next_grid[r]))


flood()
