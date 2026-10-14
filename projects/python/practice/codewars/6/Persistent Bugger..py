def persistence(n):
    count = 0

    while n >= 10:
        result = 1

        for digit in str(n):
            result *= int(digit)

        n = result
        count += 1

    return count
