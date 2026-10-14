def order_weight(x):
    w = x.split(' ')
    sum_w = []
    for a in w:
        r = 0
        for char in a:
            r += int(char)
        sum_w.append(r)
    pair = sorted(zip(sum_w,w))
    sum_w, w = zip(*pair)
    return ' '.join(map(str,sum_w))
