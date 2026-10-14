a = input()
b = 'aeiou'
while not a.islower() and a.isalpha():
    a = input()
if a in b:
    print("yes")
else:
    print("no")
