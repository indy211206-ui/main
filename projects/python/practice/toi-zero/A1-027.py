a = input().lower()

while len(a) != 5:
    a = input()

def reverse_word(word):
    return word[::-1]

print(reverse_word(a))
