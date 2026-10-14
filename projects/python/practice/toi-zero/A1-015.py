a = input()
b = input()
c = input()

while not a.isalpha() or not b.isalpha() or not c.isdigit():
    a = input()
    b = input()
    c = input()

if len(a) > 5:
    print(a[0] + a[1] + b[len(b) - 1] + c[len(c) - 1])
else:
    print(a[0] + c + b[len(b) - 1])
