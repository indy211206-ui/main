def flood():
    rows, cols = map(int, input().split())

    # Read grid as 2D list so we can modify it
    grid = []
    for r in range(rows):
        row = input().split()  # split by space: ['*', '-', '*', ...]
        grid.append(row)

    # Make a copy for the next state
    next_grid = []
    for r in range(rows):
        next_row = []
        for c in range(cols):
            next_row.append(grid[r][c])
        next_grid.append(next_row)

    # Water flows DOWN only
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '*':
                # Flood the cell below
                if r + 1 < rows:
                    next_grid[r + 1][c] = '*'

    # Print result
    for r in range(rows):
        print(' '.join(next_grid[r]))


flood()
