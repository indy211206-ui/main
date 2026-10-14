def make_readable(s):
    hh, s = divmod(s, 60 ** 2)
    mm, s = divmod(s, 60)
    return f'{hh:02}:{mm:02}:{s:02}'
print(make_readable(3888))
