def balanced_parens(n):
    result = []
    def build(current, open_left, close_left):
        if open_left == 0 and close_left == 0:
            result.append(current)
            return
        if open_left > 0:
            build(current + "(", open_left - 1, close_left)
        if open_left < close_left:
            build(current + ")", open_left, close_left - 1)
    build("", n, n)
    return result
print(balanced_parens(4))
