def fmt(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"

def format_duration(ss):
    if ss == 0:
        return 'now'
    y, ss = divmod(ss, 365 * 24 * 60 * 60)
    d, ss = divmod(ss, 24 * 60 * 60)
    h, ss = divmod(ss, 60 * 60)
    m, ss = divmod(ss, 60)
    s = ss % 60
    result = []
    if y:
        result.append(fmt(y, 'year'))
    if d:
        result.append(fmt(d, 'day'))
    if h:
        result.append(fmt(h, 'hour'))
    if m:
        result.append(fmt(m, 'minute'))
    if s:
        result.append(fmt(s, 'second'))
    if len(result) == 1:
        return result[0]

    if len(result) == 2:
        return " and ".join(result)

    return ", ".join(result[:-1]) + " and " + result[-1]
# smarter
times = [("year", 365 * 24 * 60 * 60),
         ("day", 24 * 60 * 60),
         ("hour", 60 * 60),
         ("minute", 60),
         ("second", 1)]

def format_durations(seconds):

    if not seconds:
        return "now"

    chunks = []
    for name, secs in times:
        qty = seconds // secs
        if qty:
            if qty > 1:
                name += "s"
            chunks.append(str(qty) + " " + name)

        seconds = seconds % secs

    return ', '.join(chunks[:-1]) + ' and ' + chunks[-1] if len(chunks) > 1 else chunks[0]
