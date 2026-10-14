s = input()
u = s.upper()
n = len(u)

if all(c in 'TI' for c in u):
    print('unknown', n)
else:
    error = -1
    for i in range(n):
        c = u[i]
        prev = u[i-1] if i > 0 else None

        if c not in 'RABIT':
            error = i
            break

        if c == 'A' and prev is not None and prev not in 'RA':
            error = i
            break

        if prev == 'R' and c != 'A':
            error = i
            break

        if prev == 'B' and c not in 'IT':
            error = i
            break

    if error == -1 and u[-1] == 'R':
        error = n - 1
    if error == -1 and u[-1] == 'B':
        error = n - 1

    if error != -1:
        print('no', error)
    else:
        max_a = cur = 0
        for c in u:
            if c == 'A':
                cur += 1
                max_a = max(max_a, cur)
            else:
                cur = 0
        print('yes', max_a)
