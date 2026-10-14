def knight_vs_rook(knight, rook):
    kx, ky = knight
    rx, ry = rook

    if kx == rx or ky == ry:
        return "Rook"

    dx = abs(kx - rx)
    dy = abs(ky - ry)

    if (dx, dy) in [(1, 2), (2, 1)]:
        return "Knight"

    return "None"
