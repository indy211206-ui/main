s = input()
upper = s.upper()

if 'BUU' in upper:
    last_b = upper.rfind('B')
    count_u = 0
    i = last_b + 1
    while i < len(upper) and upper[i] == 'U':
        count_u += 1
        i += 1
    print(f'Yes {count_u}')


else:
    b_index = -1
    for i, c in enumerate(s):
        if c == 'B' or c == 'b':
            b_index = i
            break

    if b_index != -1:
        Us = ""
        for u in s[b_index+2:]:
            Us += 'U'
        result = s[:b_index + 1] + 'U' + Us
        print(result)
    else:
        n = len(s)
        repeated = ('BUU' * ((n // 3) + 1))[:n]
        print(repeated)
