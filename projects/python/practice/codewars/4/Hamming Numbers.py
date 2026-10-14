def hamming(n):
    h = [1]
    i2 = i3 = i5 = 0
    while len(h) < n:
        n2 = 2 * h[i2]
        n3 = 3 * h[i3]
        n5 = 5 * h[i5]
        nxt = min(n2, n3, n5)
        h.append(nxt)
        if nxt == n2:
            i2 += 1
        if nxt == n3:
            i3 += 1
        if nxt == n5:
            i5 += 1
    return h[-1]
print(hamming(925))
