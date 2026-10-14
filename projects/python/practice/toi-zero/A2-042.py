stock = {}
output = []

while True:
    command = input()

    if 'ADD' in command:
        parts = command.split(' ')
        name, qty = parts[1], int(parts[2])
        if name in stock:
            stock[name] += qty       # add, not overwrite
        else:
            stock[name] = qty

    elif 'REMOVE' in command:
        parts = command.split(' ')
        name, qty = parts[1], int(parts[2])
        current = stock[name] if name in stock else 0
        if qty > current:
            output.append('Not enough stock for ' + name)
            if name in stock:
                del stock[name]      # remove item
        else:
            stock[name] -= qty
            if stock[name] == 0:
                del stock[name]      # remove if zero

    elif command == 'CHECK':
        low = []
        for k in stock:
            if stock[k] < 5:
                low.append(k)
        # manual sort
        for i in range(len(low)):
            for j in range(i+1, len(low)):
                if low[i] > low[j]:
                    low[i], low[j] = low[j], low[i]
        if len(low) == 0:
            output.append('All stocks are sufficient')
        else:
            for name in low:
                output.append(name)

    elif command == 'REPORT':
        items = []
        for k in stock:
            items.append((k, stock[k]))
        # manual sort by name
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                if items[i][0] > items[j][0]:
                    items[i], items[j] = items[j], items[i]
        for name, qty in items:
            output.append(name + ': ' + str(qty))

    elif command == 'END':
        break

for line in output:
    print(line)
