
def minesweeper():
    rows, cols = map(int, input().split())
    n_bombs = int(input())

    bombs = {}
    for _ in range(n_bombs):
        r, c = map(int, input().split())
        bombs.add((r, c))

    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if (r, c) in bombs:
                row.append('x')
            else:
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if (dr, dc) != (0, 0) and (r + dr, c + dc) in bombs:
                            count += 1
                row.append(str(count))
        grid.append(row)

    for row in grid:
        print(' '.join(row))


minesweeper()
