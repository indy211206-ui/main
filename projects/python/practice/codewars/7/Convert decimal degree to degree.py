def convert(n):
    m_float = (n - int(n)) * 60
    m = int(m_float)
    s = round((m_float - m) * 60)
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        n += 1
    result = [int(n)]
    if m != 0 or s != 0:
        result.append(m)
    if s != 0:
        result.append(s)
    return result
