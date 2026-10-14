n = int(input())

base = 0

if n <= 10:
    base = n * 5
elif n <= 50:
    base = 10 * 5 + (n - 10) * 7
elif n <= 100:
    base = 10 * 5 + 40 * 7 + (n - 50) * 10
elif n <= 200:
    base = 10 * 5 + 40 * 7 + 50 * 10 + (n - 100) * 12
else:
    base = 10 * 5 + 40 * 7 + 50 * 10 + 100 * 12 + (n - 200) * 15

ft  = n * 0.50
vat = base * 0.07

total = base + ft + vat
print("%.2f" % total)
