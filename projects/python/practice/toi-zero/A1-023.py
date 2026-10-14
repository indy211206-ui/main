a = int(input())
b = input().lower()

if b == "c":
    if a <= 0:
        print("solid")
    elif a > 0 and a < 100:
        print("liquid")
    elif a >= 100:
        print("gas")
elif b == "f":
    if a <= 32:
        print("solid")
    elif a > 32 and a < 212:
        print("liquid")
    elif a >= 212:
        print("gas")
