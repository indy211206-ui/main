a = int(input())

if a >= 1582:
    if a % 400 == 0:
        print("yes")
    elif a % 100 == 0:
        print("no")
    elif a % 4 == 0:
        print("yes")
if a < 1582:
    if a % 4 == 0:
        print("yes")
