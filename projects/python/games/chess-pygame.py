
"""
Pygame Chess - single file, no image or font assets needed.

    pip install pygame
    python chess_pygame.py

Controls: click or drag pieces.  N = new game, U = undo, F = flip board, Esc = cancel.
Features: legal moves only, check / checkmate / stalemate, castling, en passant,
promotion picker, 50-move / repetition / insufficient-material draws,
move list in standard notation, and a computer opponent (levels 1-4).
"""
import math
import random
import sys
import threading
import time

import pygame




FILES = "abcdefgh"


def sq_name(s):
    return FILES[s & 7] + str(1 + (s >> 3))


KN = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

KNIGHT_T = [[] for _ in range(64)]
KING_T = [[] for _ in range(64)]
RAYS = [[[] for _ in range(8)] for _ in range(64)]
PAWN_FROM_W = [[] for _ in range(64)]
PAWN_FROM_B = [[] for _ in range(64)]
for _sq in range(64):
    _f, _r = _sq & 7, _sq >> 3
    for _df, _dr in KN:
        if 0 <= _f + _df < 8 and 0 <= _r + _dr < 8:
            KNIGHT_T[_sq].append((_r + _dr) * 8 + _f + _df)
    for _df in (-1, 0, 1):
        for _dr in (-1, 0, 1):
            if (_df or _dr) and 0 <= _f + _df < 8 and 0 <= _r + _dr < 8:
                KING_T[_sq].append((_r + _dr) * 8 + _f + _df)
    for _i, (_df, _dr) in enumerate(DIRS):
        _nf, _nr = _f + _df, _r + _dr
        while 0 <= _nf < 8 and 0 <= _nr < 8:
            RAYS[_sq][_i].append(_nr * 8 + _nf)
            _nf += _df
            _nr += _dr
    for _df in (-1, 1):
        if 0 <= _f + _df < 8:
            if _r - 1 >= 0:
                PAWN_FROM_W[_sq].append((_r - 1) * 8 + _f + _df)
            if _r + 1 < 8:
                PAWN_FROM_B[_sq].append((_r + 1) * 8 + _f + _df)


def is_white(c):
    return c.isupper()


class State:
    __slots__ = ("b", "white", "wk", "wq", "bk", "bq", "ep", "half", "full")

    def __init__(self):
        self.b = list("RNBQKBNR" + "P" * 8 + "." * 32 + "p" * 8 + "rnbqkbnr")
        self.white = True
        self.wk = self.wq = self.bk = self.bq = True
        self.ep = -1
        self.half = 0
        self.full = 1

    def copy(self):
        n = State.__new__(State)
        n.b = self.b[:]
        n.white, n.wk, n.wq, n.bk, n.bq = self.white, self.wk, self.wq, self.bk, self.bq
        n.ep, n.half, n.full = self.ep, self.half, self.full
        return n

    def key(self):
        return ("".join(self.b), self.white, self.wk, self.wq, self.bk, self.bq, self.ep)


def is_attacked(b, sq, by_white):
    if by_white:
        pawn, knight, king, rook, bishop, queen = "PNKRBQ"
        pf = PAWN_FROM_W[sq]
    else:
        pawn, knight, king, rook, bishop, queen = "pnkrbq"
        pf = PAWN_FROM_B[sq]
    for s in pf:
        if b[s] == pawn:
            return True
    for s in KNIGHT_T[sq]:
        if b[s] == knight:
            return True
    for s in KING_T[sq]:
        if b[s] == king:
            return True
    rays = RAYS[sq]
    for i in range(8):
        for s in rays[i]:
            c = b[s]
            if c != ".":
                if c == queen or c == (rook if i < 4 else bishop):
                    return True
                break
    return False


def find_king(st, white):
    return st.b.index("K" if white else "k")


def in_check(st, white):
    return is_attacked(st.b, find_king(st, white), not white)


def make_move(st, m):
    f, t, promo = m
    s = st.copy()
    b = s.b
    p = b[f]
    cap = b[t]
    pawn = p in "Pp"
    white = st.white
    if pawn and t == st.ep and cap == "." and (f & 7) != (t & 7):
        b[t + (-8 if white else 8)] = "."
        cap = "x"
    b[t] = p
    b[f] = "."
    if promo:
        b[t] = promo.upper() if white else promo
    if p in "Kk" and abs(t - f) == 2:
        if t > f:
            b[f + 1] = b[f + 3]
            b[f + 3] = "."
        else:
            b[f - 1] = b[f - 4]
            b[f - 4] = "."
    s.ep = (f + t) // 2 if pawn and abs(t - f) == 16 else -1
    if p == "K":
        s.wk = s.wq = False
    elif p == "k":
        s.bk = s.bq = False
    for q in (f, t):
        if q == 0:
            s.wq = False
        elif q == 7:
            s.wk = False
        elif q == 56:
            s.bq = False
        elif q == 63:
            s.bk = False
    s.half = 0 if (pawn or cap != ".") else st.half + 1
    if not white:
        s.full += 1
    s.white = not white
    return s


def pseudo_moves(st):
    out = []
    b = st.b
    w = st.white
    for sq in range(64):
        c = b[sq]
        if c == "." or is_white(c) != w:
            continue
        t = c.lower()
        r, f = sq >> 3, sq & 7
        if t == "p":
            d = 1 if w else -1
            nr = r + d
            if not 0 <= nr < 8:
                continue
            promo = nr == (7 if w else 0)
            to = nr * 8 + f
            if b[to] == ".":
                if promo:
                    out += [(sq, to, x) for x in "qrbn"]
                else:
                    out.append((sq, to, ""))
                    if r == (1 if w else 6) and b[to + 8 * d] == ".":
                        out.append((sq, to + 8 * d, ""))
            for df in (-1, 1):
                if not 0 <= f + df < 8:
                    continue
                to = nr * 8 + f + df
                tc = b[to]
                if (tc != "." and is_white(tc) != w) or (to == st.ep and tc == "."):
                    if promo:
                        out += [(sq, to, x) for x in "qrbn"]
                    else:
                        out.append((sq, to, ""))
        elif t == "n":
            for to in KNIGHT_T[sq]:
                tc = b[to]
                if tc == "." or is_white(tc) != w:
                    out.append((sq, to, ""))
        elif t == "k":
            for to in KING_T[sq]:
                tc = b[to]
                if tc == "." or is_white(tc) != w:
                    out.append((sq, to, ""))
            home = 4 if w else 60
            if sq == home and not is_attacked(b, home, not w):
                rook = "R" if w else "r"
                if (st.wk if w else st.bk) and b[home + 1] == b[home + 2] == "." and b[home + 3] == rook \
                        and not is_attacked(b, home + 1, not w) and not is_attacked(b, home + 2, not w):
                    out.append((sq, home + 2, ""))
                if (st.wq if w else st.bq) and b[home - 1] == b[home - 2] == b[home - 3] == "." \
                        and b[home - 4] == rook \
                        and not is_attacked(b, home - 1, not w) and not is_attacked(b, home - 2, not w):
                    out.append((sq, home - 2, ""))
        else:
            lo, hi = (4, 8) if t == "b" else (0, 4) if t == "r" else (0, 8)
            for i in range(lo, hi):
                for to in RAYS[sq][i]:
                    tc = b[to]
                    if tc == ".":
                        out.append((sq, to, ""))
                    else:
                        if is_white(tc) != w:
                            out.append((sq, to, ""))
                        break
    return out


def legal_moves(st):
    w = st.white
    out = []
    for m in pseudo_moves(st):
        n = make_move(st, m)
        if not is_attacked(n.b, n.b.index("K" if w else "k"), not w):
            out.append(m)
    return out


def insufficient_material(st):
    minors = 0
    for c in st.b:
        t = c.lower()
        if t in "prq":
            return False
        if t in "nb":
            minors += 1
    return minors <= 1


def move_str(m):
    return sq_name(m[0]) + sq_name(m[1]) + m[2]


def san(st, m, legal):
    """Standard algebraic notation for move m in position st."""
    f, t, p = m
    piece = st.b[f]
    kind = piece.upper()
    if kind == "K" and abs(t - f) == 2:
        s = "O-O" if t > f else "O-O-O"
    else:
        cap = st.b[t] != "." or (kind == "P" and (f & 7) != (t & 7))
        if kind == "P":
            s = (FILES[f & 7] + "x" if cap else "") + sq_name(t)
            if p:
                s += "=" + p.upper()
        else:
            dis = ""
            others = [o for o in legal if o[1] == t and o != m and st.b[o[0]] == piece]
            if others:
                if all((o[0] & 7) != (f & 7) for o in others):
                    dis = FILES[f & 7]
                elif all((o[0] >> 3) != (f >> 3) for o in others):
                    dis = str(1 + (f >> 3))
                else:
                    dis = sq_name(f)
            s = kind + dis + ("x" if cap else "") + sq_name(t)
    n = make_move(st, m)
    if in_check(n, n.white):
        s += "#" if not legal_moves(n) else "+"
    return s



VALUE = {".": 0, "p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 0}
CENTER = [int(((3.5 - abs((s & 7) - 3.5)) + (3.5 - abs((s >> 3) - 3.5))) * 4) for s in range(64)]
MATE = 100000
INF = 10 ** 9
LEVELS = {1: (1, 0.4), 2: (2, 1.5), 3: (3, 4.0), 4: (4, 9.0)}


class Abort(Exception):
    pass


class Ctx:
    def __init__(self, stop, deadline):
        self.stop, self.deadline, self.nodes = stop, deadline, 0

    def tick(self):
        self.nodes += 1
        if (self.nodes & 255) == 0 and (self.stop.is_set() or time.time() > self.deadline):
            raise Abort


def evaluate(st):
    score = 0
    for sq in range(64):
        c = st.b[sq]
        if c == ".":
            continue
        t = c.lower()
        v = VALUE[t]
        if t not in "kr":
            v += CENTER[sq]
        if t == "p":
            v += ((sq >> 3) if c == "P" else 7 - (sq >> 3)) * 6
        score += v if c.isupper() else -v
    return score if st.white else -score


def qsearch(st, alpha, beta, ctx, qd):
    ctx.tick()
    stand = evaluate(st)
    if stand >= beta:
        return beta
    if stand > alpha:
        alpha = stand
    if qd == 0:
        return alpha
    caps = [m for m in pseudo_moves(st) if st.b[m[1]] != "." or m[2] == "q"]
    caps.sort(key=lambda m: VALUE[st.b[m[1]].lower()] * 10 - VALUE[st.b[m[0]].lower()], reverse=True)
    w = st.white
    for m in caps:
        n = make_move(st, m)
        if is_attacked(n.b, n.b.index("K" if w else "k"), not w):
            continue
        v = -qsearch(n, -beta, -alpha, ctx, qd - 1)
        if v >= beta:
            return beta
        if v > alpha:
            alpha = v
    return alpha


def negamax(st, depth, alpha, beta, ply, ctx):
    ctx.tick()
    if st.half >= 100:
        return 0
    if depth == 0:
        return qsearch(st, alpha, beta, ctx, 4)
    moves = legal_moves(st)
    if not moves:
        return -MATE + ply if in_check(st, st.white) else 0
    moves.sort(key=lambda m: VALUE[st.b[m[1]].lower()] * 10 - VALUE[st.b[m[0]].lower()]
               + (800 if m[2] == "q" else 0), reverse=True)
    for m in moves:
        v = -negamax(make_move(st, m), depth - 1, -beta, -alpha, ply + 1, ctx)
        if v >= beta:
            return beta
        if v > alpha:
            alpha = v
    return alpha


def best_move(st, level, stop):
    """Iterative-deepening alpha-beta search with a time limit."""
    max_depth, seconds = LEVELS[level]
    ctx = Ctx(stop, time.time() + seconds)
    moves = legal_moves(st)
    random.shuffle(moves)
    best = moves[0]
    try:
        for depth in range(1, max_depth + 1):
            alpha, cur_best = -INF, None
            for m in moves:
                v = -negamax(make_move(st, m), depth - 1, -INF, -alpha, 1, ctx)
                if cur_best is None or v > alpha:
                    alpha, cur_best = v, m
            best = cur_best
            moves.remove(best)
            moves.insert(0, best)
            if abs(alpha) > MATE - 100:
                break
    except Abort:
        pass
    return best





W, H = 1000, 720
BX, BY, SQ = 40, 40, 80
PX, PW = 710, 270
C_LIGHT, C_DARK = (240, 217, 181), (181, 136, 99)
C_TEXT, C_DIM = (236, 234, 228), (150, 148, 142)
C_GOLD, C_RED = (255, 214, 90), (240, 100, 90)


def ellipse_poly(cx, cy, rx, ry, n=48):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def circle_poly(cx, cy, r):
    return ellipse_poly(cx, cy, r, r)


def rect_poly(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def shape_for(t):
    """Piece silhouettes as polygons in unit coordinates: (body polys, detail polys)."""
    body, detail = [], []

    def base():
        body.append(rect_poly(0.25, 0.70, 0.75, 0.79))
        body.append(rect_poly(0.20, 0.79, 0.80, 0.88))

    if t == "p":
        body.append(circle_poly(0.5, 0.30, 0.125))
        body.append([(0.41, 0.38), (0.59, 0.38), (0.63, 0.58), (0.72, 0.71), (0.28, 0.71), (0.37, 0.58)])
        body.append(rect_poly(0.36, 0.40, 0.64, 0.46))
    elif t == "r":
        for x in (0.27, 0.45, 0.63):
            body.append(rect_poly(x, 0.16, x + 0.10, 0.33))
        body.append(rect_poly(0.27, 0.30, 0.73, 0.40))
        body.append([(0.34, 0.40), (0.66, 0.40), (0.69, 0.70), (0.31, 0.70)])
    elif t == "n":
        body.append([(0.46, 0.13), (0.55, 0.21), (0.68, 0.33), (0.75, 0.52), (0.75, 0.71), (0.27, 0.71),
                     (0.34, 0.56), (0.45, 0.47), (0.31, 0.49), (0.19, 0.47), (0.23, 0.38), (0.33, 0.26),
                     (0.39, 0.20)])
        detail.append(circle_poly(0.42, 0.31, 0.028))
    elif t == "b":
        body.append(circle_poly(0.5, 0.17, 0.05))
        body.append(ellipse_poly(0.5, 0.36, 0.13, 0.18))
        body.append([(0.42, 0.48), (0.58, 0.48), (0.64, 0.70), (0.36, 0.70)])
        body.append(rect_poly(0.35, 0.52, 0.65, 0.58))
        detail.append([(0.495, 0.26), (0.565, 0.34), (0.545, 0.365), (0.475, 0.285)])
    elif t == "q":
        body.append([(0.24, 0.28), (0.33, 0.52), (0.37, 0.26), (0.43, 0.52), (0.50, 0.22), (0.57, 0.52),
                     (0.63, 0.26), (0.67, 0.52), (0.76, 0.28), (0.70, 0.70), (0.30, 0.70)])
        for x, y in ((0.24, 0.26), (0.37, 0.23), (0.50, 0.19), (0.63, 0.23), (0.76, 0.26)):
            body.append(circle_poly(x, y, 0.045))
    elif t == "k":
        body.append(rect_poly(0.46, 0.08, 0.54, 0.30))
        body.append(rect_poly(0.39, 0.14, 0.61, 0.21))
        body.append([(0.50, 0.28), (0.62, 0.31), (0.74, 0.42), (0.71, 0.55), (0.66, 0.62), (0.69, 0.70),
                     (0.31, 0.70), (0.34, 0.62), (0.29, 0.55), (0.26, 0.42), (0.38, 0.31)])
    base()
    return body, detail


def build_sprite(kind, white, size):
    """Draw a piece at 4x resolution with an outline, then smooth-scale down."""
    ss = 4
    n = size * ss
    body, detail = shape_for(kind)
    fill_c = (250, 249, 243) if white else (66, 66, 74)
    line_c = (34, 32, 30) if white else (12, 12, 14)
    det_c = (34, 32, 30) if white else (232, 232, 236)
    surf = pygame.Surface((n, n), pygame.SRCALPHA)
    r = max(1, round(0.022 * n))
    for poly in body:
        pts = [(x * n, y * n) for x, y in poly]
        pygame.draw.polygon(surf, line_c, pts)
        pygame.draw.polygon(surf, line_c, pts, 2 * r)
        for p in pts:
            pygame.draw.circle(surf, line_c, p, r)
    for poly in body:
        pygame.draw.polygon(surf, fill_c, [(x * n, y * n) for x, y in poly])
    for poly in detail:
        pygame.draw.polygon(surf, det_c, [(x * n, y * n) for x, y in poly])
    return pygame.transform.smoothscale(surf, (size, size))


def aa_disc(radius, color, ring_inner=None):
    """Anti-aliased filled disc (or ring) surface made by supersampling."""
    ss = 4
    d = radius * 2
    surf = pygame.Surface((d * ss, d * ss), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius * ss, radius * ss), radius * ss)
    if ring_inner:
        pygame.draw.circle(surf, (0, 0, 0, 0), (radius * ss, radius * ss), ring_inner * ss)
    return pygame.transform.smoothscale(surf, (d, d))





B_NEW, B_UNDO, B_FLIP, B_MODE, B_SIDE, B_LVL_DN, B_LVL_UP = range(7)


class App:
    def __init__(self):
        self.canvas = pygame.Surface((W, H))
        self.f_title = pygame.font.Font(None, 84)
        self.f_big = pygame.font.Font(None, 40)
        self.f_btn = pygame.font.Font(None, 30)
        self.f_small = pygame.font.Font(None, 26)
        self.sprites = {}
        for t in "pnbrqk":
            self.sprites[t.upper()] = build_sprite(t, True, SQ)
            self.sprites[t] = build_sprite(t, False, SQ)
        self.ov_last = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
        self.ov_last.fill((255, 222, 70, 105))
        self.ov_sel = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
        self.ov_sel.fill((90, 200, 110, 130))
        self.ov_check = aa_disc(SQ // 2 - 2, (235, 60, 50, 160))
        self.dot = aa_disc(12, (40, 40, 40, 85))
        self.ring = aa_disc(SQ // 2 - 2, (40, 40, 40, 95), SQ // 2 - 10)

        self.vs_computer, self.human_white, self.flipped = True, True, False
        self.level = 2
        self.sel = -1
        self.dragging = False
        self.mx = self.my = 0
        self.hx = self.hy = -1
        self.promo_pending = False
        self.promo_base = None
        self.busy = False
        self.ai_result = None
        self.stop_evt = None
        self.thread = None
        self.running = True
        self.new_game()


    def refresh(self):
        self.legal = legal_moves(self.cur)
        self.check = in_check(self.cur, self.cur.white)
        self.over = True
        self.status_sub = ""
        c = self.cur
        if not self.legal:
            if self.check:
                self.status_main, self.status_sub = "CHECKMATE!", ("BLACK WINS" if c.white else "WHITE WINS")
            else:
                self.status_main, self.status_sub = "STALEMATE", "NO LEGAL MOVES"
        elif c.half >= 100:
            self.status_main, self.status_sub = "DRAW", "50 MOVE RULE"
        elif insufficient_material(c):
            self.status_main, self.status_sub = "DRAW", "LOW MATERIAL"
        elif sum(1 for h in self.hist if h.key() == c.key()) + 1 >= 3:
            self.status_main, self.status_sub = "DRAW", "REPETITION"
        else:
            self.over = False
            self.status_main = "WHITE TO MOVE" if c.white else "BLACK TO MOVE"
            if self.check:
                self.status_sub = "CHECK!"

    def new_game(self):
        self.cancel_ai()
        self.cur = State()
        self.hist, self.played, self.sans = [], [], []
        self.sel, self.dragging, self.promo_pending = -1, False, False
        self.flipped = self.vs_computer and not self.human_white
        self.refresh()
        self.maybe_start_ai()

    def apply_move(self, m):
        self.sans.append(san(self.cur, m, self.legal))
        self.hist.append(self.cur)
        self.played.append(m)
        self.cur = make_move(self.cur, m)
        self.sel, self.dragging, self.promo_pending = -1, False, False
        self.refresh()
        self.maybe_start_ai()

    def undo(self):
        self.cancel_ai()
        if not self.hist:
            return

        def pop():
            self.cur = self.hist.pop()
            self.played.pop()
            self.sans.pop()

        pop()
        while self.vs_computer and self.hist and self.cur.white != self.human_white:
            pop()
        self.sel, self.dragging, self.promo_pending = -1, False, False
        self.refresh()
        self.maybe_start_ai()

    def human_turn(self):
        return not self.over and not self.busy and (not self.vs_computer or self.cur.white == self.human_white)


    def maybe_start_ai(self):
        if self.over or not self.vs_computer or self.cur.white == self.human_white or self.busy:
            return
        self.busy = True
        self.ai_result = None
        stop = self.stop_evt = threading.Event()
        state, level = self.cur.copy(), self.level

        def work():
            mv = best_move(state, level, stop)
            if not stop.is_set():
                self.ai_result = mv

        self.thread = threading.Thread(target=work, daemon=True)
        self.thread.start()

    def cancel_ai(self):
        if not self.busy:
            return
        self.stop_evt.set()
        self.thread.join()
        self.busy = False
        self.ai_result = None

    def update(self):
        if self.busy and not self.thread.is_alive():
            self.thread.join()
            self.busy = False
            mv, self.ai_result = self.ai_result, None
            if mv is not None:
                self.apply_move(mv)


    def sq_to_screen(self, sq):
        f, r = sq & 7, sq >> 3
        return BX + (7 - f if self.flipped else f) * SQ, BY + (r if self.flipped else 7 - r) * SQ

    def square_at(self, x, y):
        if not (BX <= x < BX + 8 * SQ and BY <= y < BY + 8 * SQ):
            return -1
        col, row = (x - BX) // SQ, (y - BY) // SQ
        return (row if self.flipped else 7 - row) * 8 + (7 - col if self.flipped else col)

    def own_piece(self, sq):
        p = self.cur.b[sq]
        return p != "." and is_white(p) == self.cur.white

    def buttons(self):
        y, h, step = 178, 38, 46
        return [
            (pygame.Rect(PX, y, PW, h), "NEW GAME", B_NEW, True),
            (pygame.Rect(PX, y + step, PW, h), "UNDO", B_UNDO, bool(self.hist)),
            (pygame.Rect(PX, y + 2 * step, PW, h), "FLIP BOARD", B_FLIP, True),
            (pygame.Rect(PX, y + 3 * step, PW, h), "VS COMPUTER" if self.vs_computer else "2 PLAYERS", B_MODE, True),
            (pygame.Rect(PX, y + 4 * step, PW, h), "PLAY AS: " + ("WHITE" if self.human_white else "BLACK"),
             B_SIDE, self.vs_computer),
            (pygame.Rect(PX, y + 5 * step, 44, h), "-", B_LVL_DN, self.vs_computer and self.level > 1),
            (pygame.Rect(PX + PW - 44, y + 5 * step, 44, h), "+", B_LVL_UP, self.vs_computer and self.level < 4),
        ]

    def click_button(self, bid):
        if bid == B_NEW:
            self.new_game()
        elif bid == B_UNDO:
            self.undo()
        elif bid == B_FLIP:
            self.flipped = not self.flipped
        elif bid == B_MODE:
            self.cancel_ai()
            self.vs_computer = not self.vs_computer
            self.maybe_start_ai()
        elif bid == B_SIDE:
            self.cancel_ai()
            self.human_white = not self.human_white
            self.flipped = not self.human_white
            self.maybe_start_ai()
        elif bid == B_LVL_DN:
            self.level = max(1, self.level - 1)
        elif bid == B_LVL_UP:
            self.level = min(4, self.level + 1)


    def try_move(self, frm, to):
        cands = [m for m in self.legal if m[0] == frm and m[1] == to]
        if not cands:
            return False
        if cands[0][2]:
            self.promo_pending = True
            self.promo_base = (frm, to)
            return True
        self.apply_move(cands[0])
        return True

    def promo_cell(self, i):
        return pygame.Rect(BX + 120 + i * 100, BY + 270, 100, 100)

    def on_down(self, x, y):
        self.mx, self.my = x, y
        if self.promo_pending:
            for i in range(4):
                if self.promo_cell(i).collidepoint(x, y):
                    self.promo_pending = False
                    self.apply_move((self.promo_base[0], self.promo_base[1], "qrbn"[i]))
                    return
            self.promo_pending = False
            self.sel = -1
            return
        for rect, _, bid, enabled in self.buttons():
            if rect.collidepoint(x, y):
                if enabled:
                    self.click_button(bid)
                return
        if not self.human_turn():
            return
        sq = self.square_at(x, y)
        if sq < 0:
            self.sel = -1
            return
        if self.sel >= 0 and self.try_move(self.sel, sq):
            return
        if self.own_piece(sq):
            self.sel, self.dragging = sq, True
        else:
            self.sel = -1

    def on_move(self, x, y):
        self.hx, self.hy = x, y
        if self.dragging:
            self.mx, self.my = x, y

    def on_up(self, x, y):
        if not self.dragging:
            return
        self.dragging = False
        t = self.square_at(x, y)
        if t >= 0 and t != self.sel:
            self.try_move(self.sel, t)

    def on_key(self, key):
        if key == pygame.K_n:
            self.new_game()
        elif key in (pygame.K_u, pygame.K_BACKSPACE):
            self.undo()
        elif key == pygame.K_f:
            self.flipped = not self.flipped
        elif key == pygame.K_ESCAPE:
            self.sel, self.dragging, self.promo_pending = -1, False, False


    def text(self, font, s, pos, color, center_in=None):
        img = font.render(s, True, color)
        if center_in is not None:
            pos = img.get_rect(center=center_in.center).topleft
        self.canvas.blit(img, pos)

    def draw_board(self):
        cv = self.canvas
        pygame.draw.rect(cv, (62, 52, 44), (BX - 6, BY - 6, 8 * SQ + 12, 8 * SQ + 12))
        for sq in range(64):
            x, y = self.sq_to_screen(sq)
            light = ((sq & 7) + (sq >> 3)) % 2 == 1
            pygame.draw.rect(cv, C_LIGHT if light else C_DARK, (x, y, SQ, SQ))
        if self.played:
            for sq in self.played[-1][:2]:
                cv.blit(self.ov_last, self.sq_to_screen(sq))
        if self.sel >= 0:
            cv.blit(self.ov_sel, self.sq_to_screen(self.sel))
        if self.check:
            x, y = self.sq_to_screen(find_king(self.cur, self.cur.white))
            cv.blit(self.ov_check, (x + 2, y + 2))
        for i in range(8):
            f, r = (7 - i if self.flipped else i), (i if self.flipped else 7 - i)
            self.text(self.f_small, FILES[f], (BX + i * SQ + SQ // 2 - 5, BY + 8 * SQ + 12), C_DIM)
            self.text(self.f_small, str(r + 1), (BX - 22, BY + i * SQ + SQ // 2 - 8), C_DIM)
        if self.sel >= 0:
            for f, t, _ in self.legal:
                if f != self.sel:
                    continue
                x, y = self.sq_to_screen(t)
                cap = self.cur.b[t] != "." or (self.cur.b[f] in "Pp" and (f & 7) != (t & 7))
                if cap:
                    cv.blit(self.ring, (x + 2, y + 2))
                else:
                    cv.blit(self.dot, (x + SQ // 2 - 12, y + SQ // 2 - 12))
        for sq in range(64):
            p = self.cur.b[sq]
            if p == "." or (self.dragging and sq == self.sel):
                continue
            cv.blit(self.sprites[p], self.sq_to_screen(sq))
        if self.dragging and self.sel >= 0:
            cv.blit(self.sprites[self.cur.b[self.sel]], (self.mx - SQ // 2, self.my - SQ // 2))

    def draw_promo(self):
        cv = self.canvas
        dim = pygame.Surface((8 * SQ, 8 * SQ), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 150))
        cv.blit(dim, (BX, BY))
        pygame.draw.rect(cv, (245, 240, 228), (BX + 110, BY + 250, 420, 140))
        self.text(self.f_small, "PROMOTE TO", (0, 0), (60, 50, 40), pygame.Rect(BX + 110, BY + 262, 420, 0))
        for i in range(4):
            c = self.promo_cell(i)
            if c.collidepoint(self.hx, self.hy):
                pygame.draw.rect(cv, (210, 190, 150), c)
            t = "QRBN"[i]
            cv.blit(self.sprites[t if self.cur.white else t.lower()], (c.x + 10, c.y + 10))

    def draw_panel(self):
        cv = self.canvas
        self.text(self.f_title, "CHESS", (PX, 30), C_TEXT)
        self.text(self.f_big, self.status_main, (PX, 96), C_GOLD if self.over else C_TEXT)
        if self.busy:
            sub, col = "THINKING" + "." * (int(time.time() * 3.3) % 4), C_DIM
        else:
            sub, col = self.status_sub, (C_RED if self.check else C_DIM)
        self.text(self.f_big, sub, (PX, 128), col)
        for rect, label, bid, enabled in self.buttons():
            hov = rect.collidepoint(self.hx, self.hy)
            bg = (44, 43, 42) if not enabled else (92, 90, 86) if hov else (66, 64, 61)
            pygame.draw.rect(cv, bg, rect, border_radius=4)
            self.text(self.f_btn, label, (0, 0), C_TEXT if enabled else (105, 103, 98), rect)
        lv = pygame.Rect(PX + 44, 178 + 5 * 46, PW - 88, 38)
        self.text(self.f_btn, "LEVEL %d" % self.level, (0, 0), C_TEXT if self.vs_computer else (105, 103, 98), lv)
        self.text(self.f_small, "MOVES", (PX, 472), C_DIM)
        total = (len(self.played) + 1) // 2
        first = max(0, total - 8)
        for n in range(first, total):
            line = "%d. %s" % (n + 1, self.sans[2 * n])
            if 2 * n + 1 < len(self.sans):
                line += "   " + self.sans[2 * n + 1]
            self.text(self.f_small, line, (PX, 498 + (n - first) * 21), C_TEXT)

    def draw(self):
        self.canvas.fill((38, 36, 34))
        self.draw_board()
        self.draw_panel()
        if self.promo_pending:
            self.draw_promo()


    def view_transform(self, screen):
        sw, sh = screen.get_size()
        scale = min(sw / W, sh / H)
        return scale, (sw - W * scale) / 2, (sh - H * scale) / 2

    def present(self, screen):
        scale, ox, oy = self.view_transform(screen)
        screen.fill((20, 19, 18))
        if abs(scale - 1) < 1e-6:
            screen.blit(self.canvas, (int(ox), int(oy)))
        else:
            screen.blit(pygame.transform.smoothscale(self.canvas, (max(1, int(W * scale)), max(1, int(H * scale)))),
                        (int(ox), int(oy)))
        pygame.display.flip()

    def run(self, screen):
        clock = pygame.time.Clock()
        while self.running:
            scale, ox, oy = self.view_transform(screen)

            def logical(pos):
                return int((pos[0] - ox) / scale), int((pos[1] - oy) / scale)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.MOUSEMOTION:
                    self.on_move(*logical(e.pos))
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.on_down(*logical(e.pos))
                elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    self.on_up(*logical(e.pos))
                elif e.type == pygame.KEYDOWN:
                    self.on_key(e.key)
            self.update()
            self.draw()
            self.present(screen)
            clock.tick(60)
        self.cancel_ai()


def main():
    pygame.init()
    sys.setswitchinterval(0.001)
    pygame.display.set_caption("Pygame Chess")
    screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    App().run(screen)
    pygame.quit()


if __name__ == "__main__":
    main()
