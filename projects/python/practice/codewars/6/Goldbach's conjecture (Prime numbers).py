def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def goldbach(en):
    pnum = []
    for a in range(2, en // 2 + 1):
        b = en - a
        if is_prime(a) and is_prime(b):
            pnum.append([a,b])
    return pnum
