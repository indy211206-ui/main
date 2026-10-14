line1 = input().replace(" ","")
size = line1[0].upper()
ramen_type = line1[1].upper()

price = {
    ('S', 'R'): 60, ('S', 'T'): 80,
    ('M', 'R'): 80, ('M', 'T'): 100,
    ('L', 'R'): 100, ('L', 'T'): 120,
}

total = price[(size, ramen_type)]

line2 = input().replace(" ","")
topping = line2[0].upper()

if topping == 'P':
    total += 15 * int(line2[1])
elif topping == 'E':
    total += 10 * int(line2[1])

print(total)
