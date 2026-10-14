def bird_choice(n, h):
    count = 0
    for i in range(n):
        left_ok = (i == 0) or (h[i] > h[i-1])
        right_ok = (i == n-1) or (h[i] > h[i+1])
        if left_ok and right_ok:
            count += 1
    print(count)
bird_choice(int(input()), list(map(int, input().split())))
