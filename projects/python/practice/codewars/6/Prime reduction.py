
a,b = map(int ,input().split())
count = 0
string = str(a)
result = a
while result != b:
    num = ()
    for i in range(len(string)):
        num += int(string[i]) ** 2
    result = sum(num)
    count += 1
print(count)
