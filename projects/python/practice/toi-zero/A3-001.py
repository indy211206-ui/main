def solve():
    n = int(input())

    bars = []
    for i in range(n):
        a, l, b, r = map(int, input().split())
        bars.append((a, l, b, r))

    total = [0.0] * (n + 1)
    added = [0.0] * (n + 1)

    for i in range(n, 0, -1):
        a, l, b, r = bars[i - 1]

        if a == 1:
            left = float(l)
            left_added = 0.0
        else:
            left = total[l]
            left_added = added[l]

        if b == 1:
            right = float(r)
            right_added = 0.0
        else:
            right = total[r]
            right_added = added[r]

        if left < right:
            diff = right - left
            left += diff
            left_added += diff
        elif right < left:
            diff = left - right
            right += diff
            right_added += diff

        total[i] = left + right
        added[i] = left_added + right_added

    print(int(round(added[1])))


solve()
