def snail_length(x, y):
    n = max(abs(x), abs(y))

    if y == n and x != n:
        return 4 * n * n + 3 * n - x

    if x == -n and y != -n:
        return 4 * n * n + n - y

    if y == -n and x != -n:
        return 4 * n * n + 7 * n + x

    return 4 * n * n + 5 * n + y
