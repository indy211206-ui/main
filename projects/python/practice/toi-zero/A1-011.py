a = input().upper()
b = ""
result = ""

for i in range(0, len(a)):
    if a[i] in b:continue
    result += str(a.count(a[i])) + a[i]
    b += a[i]

print(result)
