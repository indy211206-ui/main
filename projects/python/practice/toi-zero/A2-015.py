W, L, S = map(int, input().split())
price = int(input())

outline = 2 * W + 2 * L
total_outline = S * outline
total_price = total_outline * price
print(total_outline)
print(total_price)
