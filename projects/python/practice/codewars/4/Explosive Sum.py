from functools import cache
@cache
def ways(t, l):
    if t == 0:
        return 1
    if l == 0:
        return 0
    if l > t:
        return ways(t, t)

    return ways(t-l, l) + ways(t,l-1)

def exp_sum(n):
    return ways(n, n)
print(exp_sum(-2))
