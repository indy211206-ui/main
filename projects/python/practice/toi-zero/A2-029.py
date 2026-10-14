num = int(input())
count = 0
for row in range(num):
    count += 1
    line = []
    for col in range(count):
        if col == 0 or col == row or row == num - 1:
            line.append(0)
        else:
            line.append(1)
    print(' '.join(map(str, line)))
