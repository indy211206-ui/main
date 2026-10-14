def parse_time(s):
    """Parse H.MM or HH.MM format. Returns total minutes, or None if invalid."""
    parts = s.strip().split('.')
    if len(parts) != 2:
        return None

    h_str, m_str = parts

    # Minutes must be exactly 2 digits
    if len(m_str) != 2:
        return None

    try:
        h = int(h_str)
        m = int(m_str)
    except ValueError:
        return None

    # Validate ranges
    if h < 0 or h > 23:
        return None
    if m < 0 or m > 59:
        return None

    return h * 60 + m


def solve():
    line1 = input().strip()
    line2 = input().strip()

    i = parse_time(line1)  # entry time in minutes
    o = parse_time(line2)  # exit time in minutes

    # Validate inputs
    if i is None or o is None:
        print("ERROR")
        return

    # Exit must be after entry (same day)
    if o <= i:
        print("ERROR")
        return

    diff = o - i  # difference in minutes

    # Less than 15 minutes: FREE
    if diff < 15:
        print("FREE")
        return

    # Calculate hours (ceiling division)
    hours = (diff + 59) // 60  # rounds up any partial hour

    rates = {1: 25, 2: 50, 3: 80, 4: 110, 5: 145, 6: 180}

    if hours >= 7:
        print(250)
    else:
        print(rates[hours])


solve()
