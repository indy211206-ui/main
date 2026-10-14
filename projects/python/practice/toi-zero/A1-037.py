a = int(input())
while not a >= 1 or not a <= 3999:
    a = int(input())
def to_roman(num):
    values = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'),  (90, 'XC'), (50, 'L'),  (40, 'XL'),
        (10, 'X'),   (9, 'IX'),  (5, 'V'),   (4, 'IV'), (1, 'I')
    ]
    result = ""
    for value, symbol in values:
        while num >= value:
            result += symbol
            num -= value
    return result
print(to_roman(a))
