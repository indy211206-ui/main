
a = input().upper()
kinds = {"A": "ace",
         "J": "jack",
         "K": "king",
         "Q": "queen",}
groups = {"D": "diamonds",
         "H": "hearts",
         "S": "spades",
         "C": "clubs"}
num = a[0]
suit = a[-1]

if num in kinds:
    kind = kinds[num]
else:
    kind = num
group = groups[suit]

print(f"{kind} of {group}")
