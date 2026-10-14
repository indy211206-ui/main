a = int(input())
b = int(input())
while a > 50 or b > 50 or a < 0 or b < 0:
    a = int(input())
    b = int(input())
print(a + b)
if a + b >= 50:
    print("pass")
else:
    print("fail")
