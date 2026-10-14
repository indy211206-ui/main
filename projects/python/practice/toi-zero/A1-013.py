a = input()
b = input()

if a == "H" and b == "4567":
    print("safe unlocked")
elif a == "H" and b != "4567":
    print("safe locked - change digit")
elif a != "H" and b == "4567":
    print("safe locked - change char")
else:
    print("safe locked")
