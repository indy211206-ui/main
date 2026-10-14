student = input().upper()
lines = int(input())
discount = 0
while lines < 0 or lines > 100:
    print("invalid")
    lines = int(input())
total = sum(float(input()) for price in range(lines))
for line in range(0, lines):
    if student == "Y":
        discount = total * 0.05
    if student == "N":
        if total >= 500:
            discount = total * 0.03
        else:
            discount = 0
result = (total - discount)
print(f"{round(result + 0.001, 2):.2f}")
