a = input()
count = 0
while len(a) != 3 or not a.islower:
    a = input()
for char in a:
    if char in "aeiou":
        count +=1
print(count)
