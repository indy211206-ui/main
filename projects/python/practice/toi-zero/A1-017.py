y1 = input()
m1 = input()
d1 = input()
y2 = input()
m2 = input()
d2 = input()

if y1 == y2 and m1 == m2 and d1 == d2:
    print("0")
elif y1 > y2:
    print("2")
elif y1 < y2:
    print("1")
elif y1 == y2:
    if m1 > m2:
        print("2")
    elif m1 < m2:
        print("1")
    else:
        if d1 > d2:
            print("2")
        elif d1 < d2:
            print("1")
