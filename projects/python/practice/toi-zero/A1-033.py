a = int(input())
count = 0
for n in range(a):
    b = input()
    while not b.isupper():
        b = input()
    if b in "AEIOU":
        count += 1

print(count)
