def Overlay_pic():
    rows, cols = map(int, input().split())

    grid1 = []
    grid2 = []


    for r in range(rows):
        row = []
        line = input()
        for c in line:
            row.append(c)
        grid1.append(row)

    for r in range(rows):
        row = []
        line = input()
        for c in line:
            row.append(c)
        grid2.append(row)


    result = []
    for r in range(rows):
        row = []
        for c in range(cols):
            a = grid1[r][c]
            b = grid2[r][c]
            if a == '-' and b == '-':
                row.append('-')
            elif a == '-' and b == '+':
                row.append('+')
            elif a == '-' and b == 'x':
                row.append('x')
            elif a == '+' and b == 'x':
                row.append('*')
            elif a == 'x' and b == '+':
                row.append('*')
            else:
                row.append(a)
        result.append(row)

    for r in range(rows):
        line = ''
        for c in result[r]:
            line += c
        print(line)

Overlay_pic()
