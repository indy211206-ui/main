
import sys
import pygame
from collections import Counter

pygame.init()


SQ = 80
BOARD = SQ * 8
TOP = 48
FOOT = 32
WIDTH, HEIGHT = BOARD, TOP + BOARD + FOOT

LIGHT = (238, 216, 192)
DARK = (112, 145, 112)
BG = (30, 33, 36)
PANEL = (43, 47, 51)
WHITE = (250, 250, 245)
BLACK = (28, 30, 31)
TEXT = (245, 245, 245)
YELLOW = (246, 225, 90)
GREEN = (50, 180, 90)
RED = (220, 65, 65)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess - Two Players")
clock = pygame.time.Clock()

piece_font_path = (
    pygame.font.match_font("segoeuisymbol")
    or pygame.font.match_font("dejavusans")
    or pygame.font.match_font("arial")
)

piece_font = pygame.font.Font(piece_font_path, 64)
small_font = pygame.font.SysFont("arial", 18)
tiny_font = pygame.font.SysFont("arial", 13)

GLYPHS = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟",
}

START = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("........"),
    list("........"),
    list("........"),
    list("........"),
    list("PPPPPPPP"),
    list("RNBQKBNR"),
]


def inside(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def side_name(white):
    return "White" if white else "Black"


class ChessGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.b = [row[:] for row in START]
        self.white_turn = True
        self.castle = {"K": True, "Q": True, "k": True, "q": True}
        self.ep = None
        self.halfmove = 0
        self.last_move = None
        self.draw_claimed = False
        self.positions = Counter([self.position_key()])

    def position_key(self):
        rows = "/".join("".join(row) for row in self.b)
        rights = "".join(k for k in "KQkq" if self.castle[k]) or "-"
        ep = "-"
        if self.ep is not None:
            er, ec = self.ep
            pr = er + 1 if self.white_turn else er - 1
            pawn = "P" if self.white_turn else "p"
            if any(
                inside(pr, ec + dc) and self.b[pr][ec + dc] == pawn
                for dc in (-1, 1)
            ):
                ep = f"{er},{ec}"
        return rows, self.white_turn, rights, ep

    def king_pos(self, white):
        king = "K" if white else "k"
        for r in range(8):
            for c in range(8):
                if self.b[r][c] == king:
                    return r, c
        return None

    def attacked(self, r, c, by_white):

        pr = r + 1 if by_white else r - 1
        pawn = "P" if by_white else "p"

        for dc in (-1, 1):
            pc = c + dc
            if inside(pr, pc) and self.b[pr][pc] == pawn:
                return True


        knight = "N" if by_white else "n"
        for dr, dc in (
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ):
            nr, nc = r + dr, c + dc
            if inside(nr, nc) and self.b[nr][nc] == knight:
                return True


        king = "K" if by_white else "k"
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if inside(nr, nc) and self.b[nr][nc] == king:
                    return True


        groups = [
            (
                ((-1, -1), (-1, 1), (1, -1), (1, 1)),
                ("B", "Q") if by_white else ("b", "q")
            ),
            (
                ((-1, 0), (1, 0), (0, -1), (0, 1)),
                ("R", "Q") if by_white else ("r", "q")
            )
        ]

        for directions, attackers in groups:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while inside(nr, nc):
                    p = self.b[nr][nc]
                    if p != ".":
                        if p in attackers:
                            return True
                        break
                    nr += dr
                    nc += dc

        return False

    def in_check(self, white):
        king = self.king_pos(white)
        return king is None or self.attacked(
            king[0], king[1], not white
        )

    def pseudo_moves(self, r, c):
        p = self.b[r][c]
        if p == ".":
            return []

        white = p.isupper()
        kind = p.upper()
        moves = []


        def add(nr, nc):
            if not inside(nr, nc):
                return False

            target = self.b[nr][nc]

            if target == ".":
                moves.append((r, c, nr, nc, None))
                return True

            if target.isupper() != white and target.upper() != "K":
                moves.append((r, c, nr, nc, None))

            return False

        if kind == "P":
            direction = -1 if white else 1
            start = 6 if white else 1
            nr = r + direction

            if inside(nr, c) and self.b[nr][c] == ".":
                moves.append((r, c, nr, c, None))

                nr2 = r + 2 * direction
                if r == start and self.b[nr2][c] == ".":
                    moves.append((r, c, nr2, c, "double"))

            for dc in (-1, 1):
                nr, nc = r + direction, c + dc

                if not inside(nr, nc):
                    continue

                target = self.b[nr][nc]

                if (
                    target != "."
                    and target.isupper() != white
                    and target.upper() != "K"
                ):
                    moves.append((r, c, nr, nc, None))
                elif self.ep == (nr, nc):
                    moves.append((r, c, nr, nc, "ep"))

        elif kind == "N":
            for dr, dc in (
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1)
            ):
                add(r + dr, c + dc)

        elif kind == "K":
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        add(r + dr, c + dc)


            if white and (r, c) == (7, 4) and not self.in_check(True):
                if (
                    self.castle["K"]
                    and self.b[7][5] == self.b[7][6] == "."
                    and self.b[7][7] == "R"
                    and not self.attacked(7, 5, False)
                    and not self.attacked(7, 6, False)
                ):
                    moves.append((7, 4, 7, 6, "castleK"))

                if (
                    self.castle["Q"]
                    and self.b[7][1] == self.b[7][2] == self.b[7][3] == "."
                    and self.b[7][0] == "R"
                    and not self.attacked(7, 3, False)
                    and not self.attacked(7, 2, False)
                ):
                    moves.append((7, 4, 7, 2, "castleQ"))

            elif not white and (r, c) == (0, 4) and not self.in_check(False):
                if (
                    self.castle["k"]
                    and self.b[0][5] == self.b[0][6] == "."
                    and self.b[0][7] == "r"
                    and not self.attacked(0, 5, True)
                    and not self.attacked(0, 6, True)
                ):
                    moves.append((0, 4, 0, 6, "castlek"))

                if (
                    self.castle["q"]
                    and self.b[0][1] == self.b[0][2] == self.b[0][3] == "."
                    and self.b[0][0] == "r"
                    and not self.attacked(0, 3, True)
                    and not self.attacked(0, 2, True)
                ):
                    moves.append((0, 4, 0, 2, "castleq"))

        else:
            if kind == "B":
                directions = (
                    (-1, -1), (-1, 1), (1, -1), (1, 1)
                )
            elif kind == "R":
                directions = (
                    (-1, 0), (1, 0), (0, -1), (0, 1)
                )
            else:
                directions = (
                    (-1, -1), (-1, 1), (1, -1), (1, 1),
                    (-1, 0), (1, 0), (0, -1), (0, 1)
                )

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while inside(nr, nc):
                    if add(nr, nc):
                        nr += dr
                        nc += dc
                    else:
                        break

        return moves

    def apply(self, move, promotion="Q"):
        r, c, nr, nc, special = move
        p = self.b[r][c]
        captured = self.b[nr][nc]

        snapshot = (
            [row[:] for row in self.b],
            self.white_turn,
            self.castle.copy(),
            self.ep,
            self.halfmove,
            self.last_move
        )

        self.b[r][c] = "."

        if special == "ep":
            captured_row = nr + 1 if p.isupper() else nr - 1
            captured = self.b[captured_row][nc]
            self.b[captured_row][nc] = "."

        if special in ("castleK", "castlek"):
            self.b[nr][5] = self.b[nr][7]
            self.b[nr][7] = "."
        elif special in ("castleQ", "castleq"):
            self.b[nr][3] = self.b[nr][0]
            self.b[nr][0] = "."

        if p.upper() == "P" and nr in (0, 7):
            promotion = promotion if promotion in "QRBN" else "Q"
            self.b[nr][nc] = (
                promotion if p.isupper() else promotion.lower()
            )
        else:
            self.b[nr][nc] = p


        if p == "K":
            self.castle["K"] = self.castle["Q"] = False
        elif p == "k":
            self.castle["k"] = self.castle["q"] = False

        if (r, c) == (7, 0) or (captured == "R" and (nr, nc) == (7, 0)):
            self.castle["Q"] = False
        if (r, c) == (7, 7) or (captured == "R" and (nr, nc) == (7, 7)):
            self.castle["K"] = False
        if (r, c) == (0, 0) or (captured == "r" and (nr, nc) == (0, 0)):
            self.castle["q"] = False
        if (r, c) == (0, 7) or (captured == "r" and (nr, nc) == (0, 7)):
            self.castle["k"] = False

        self.ep = (
            ((r + nr) // 2, c) if special == "double" else None
        )

        self.halfmove = (
            0 if p.upper() == "P" or captured != "."
            else self.halfmove + 1
        )

        self.white_turn = not self.white_turn
        self.last_move = (r, c, nr, nc)

        return snapshot

    def restore(self, snapshot):
        (
            self.b, self.white_turn, self.castle,
            self.ep, self.halfmove, self.last_move
        ) = snapshot

    def legal_moves_from(self, r, c):
        p = self.b[r][c]

        if p == "." or p.isupper() != self.white_turn:
            return []

        legal = []

        for move in self.pseudo_moves(r, c):
            snapshot = self.apply(move, "Q")
            safe = not self.in_check(not self.white_turn)
            self.restore(snapshot)

            if safe:
                legal.append(move)

        return legal

    def all_legal_moves(self):
        result = []

        for r in range(8):
            for c in range(8):
                p = self.b[r][c]
                if p != "." and p.isupper() == self.white_turn:
                    result.extend(self.legal_moves_from(r, c))

        return result

    def make_move(self, move, promotion=None):
        if move not in self.legal_moves_from(move[0], move[1]):
            return False

        self.apply(move, promotion or "Q")
        self.positions[self.position_key()] += 1
        return True

    def status(self):
        if self.draw_claimed:
            return "Draw claimed"

        moves = self.all_legal_moves()
        check = self.in_check(self.white_turn)

        if not moves:
            if check:
                return f"Checkmate! {side_name(not self.white_turn)} wins"
            return "Draw by stalemate"

        if self.halfmove >= 150:
            return "Draw by 75-move rule"

        if self.positions[self.position_key()] >= 5:
            return "Draw by fivefold repetition"

        if self.halfmove >= 100:
            return f"{side_name(self.white_turn)} to move — D: claim draw"

        if self.positions[self.position_key()] >= 3:
            return f"{side_name(self.white_turn)} to move — D: claim draw"

        return side_name(self.white_turn) + " to move" + (
            " — CHECK!" if check else ""
        )

    def game_over(self):
        return (
            self.draw_claimed
            or self.halfmove >= 150
            or self.positions[self.position_key()] >= 5
            or not self.all_legal_moves()
        )


def promote_dialog(white):
    options = [("Q", "Queen"), ("R", "Rook"),
               ("B", "Bishop"), ("N", "Knight")]

    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((0, 0, 0, 175))
    screen.blit(shade, (0, 0))

    title = small_font.render("Promote pawn to:", True, TEXT)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 65)))

    buttons = []

    for i, (letter, name) in enumerate(options):
        rect = pygame.Rect(45 + i * 130, HEIGHT // 2 - 35, 120, 100)
        pygame.draw.rect(screen, PANEL, rect, border_radius=8)

        piece = letter if white else letter.lower()
        ink = WHITE if white else BLACK
        image = piece_font.render(GLYPHS[piece], True, ink)
        screen.blit(image, image.get_rect(center=(rect.centerx, rect.centery - 10)))

        label = tiny_font.render(name, True, TEXT)
        screen.blit(label, label.get_rect(center=(rect.centerx, rect.bottom - 13)))
        buttons.append((rect, letter))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Q"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, letter in buttons:
                    if rect.collidepoint(event.pos):
                        return letter

        clock.tick(60)


def draw_game(game, selected, legal_moves, dragging):
    screen.fill(BG)
    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, TOP))

    label = small_font.render(game.status(), True, TEXT)
    screen.blit(label, (10, 14))

    for r in range(8):
        for c in range(8):
            rect = pygame.Rect(c * SQ, TOP + r * SQ, SQ, SQ)
            pygame.draw.rect(
                screen, LIGHT if (r + c) % 2 else DARK, rect
            )

            if game.last_move and (r, c) in (
                game.last_move[:2], game.last_move[2:]
            ):
                tint = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
                tint.fill((255, 215, 0, 75))
                screen.blit(tint, rect.topleft)

    if selected:
        rect = pygame.Rect(
            selected[1] * SQ, TOP + selected[0] * SQ, SQ, SQ
        )
        pygame.draw.rect(screen, YELLOW, rect, 4)

    for move in legal_moves:
        _, _, r, c, special = move
        rect = pygame.Rect(c * SQ, TOP + r * SQ, SQ, SQ)

        if game.b[r][c] != "." or special == "ep":
            pygame.draw.rect(screen, RED, rect, 4)
        else:
            pygame.draw.circle(screen, GREEN, rect.center, 9)

    if game.in_check(game.white_turn):
        king = game.king_pos(game.white_turn)
        if king:
            rect = pygame.Rect(
                king[1] * SQ, TOP + king[0] * SQ, SQ, SQ
            )
            pygame.draw.rect(screen, RED, rect, 5)

    for r in range(8):
        for c in range(8):
            p = game.b[r][c]

            if p == "." or (dragging and selected == (r, c)):
                continue

            ink = WHITE if p.isupper() else BLACK
            rect = pygame.Rect(c * SQ, TOP + r * SQ, SQ, SQ)

            shadow = piece_font.render(GLYPHS[p], True, (120, 120, 120))
            screen.blit(
                shadow,
                shadow.get_rect(center=(rect.centerx + 2, rect.centery + 2))
            )

            image = piece_font.render(GLYPHS[p], True, ink)
            screen.blit(image, image.get_rect(center=rect.center))

    if dragging and selected:
        p = game.b[selected[0]][selected[1]]
        if p != ".":
            ink = WHITE if p.isupper() else BLACK
            image = piece_font.render(GLYPHS[p], True, ink)
            screen.blit(image, image.get_rect(center=pygame.mouse.get_pos()))

    for r in range(8):
        label = tiny_font.render(str(8 - r), True, (50, 50, 50))
        screen.blit(label, (3, TOP + r * SQ + 2))

    for c in range(8):
        label = tiny_font.render(chr(ord("a") + c), True, (50, 50, 50))
        screen.blit(label, (c * SQ + SQ - 13, TOP + BOARD - 15))

    pygame.draw.rect(screen, PANEL, (0, TOP + BOARD, WIDTH, FOOT))
    footer = tiny_font.render(
        "Drag and drop | R: restart | D: claim eligible draw | Esc: quit",
        True, TEXT
    )
    screen.blit(
        footer, footer.get_rect(center=(WIDTH // 2, TOP + BOARD + FOOT // 2))
    )
    pygame.display.flip()


def main():
    game = ChessGame()
    selected = None
    legal_moves = []
    dragging = False
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    game.reset()
                    selected, legal_moves, dragging = None, [], False

                elif event.key == pygame.K_d and not game.game_over():
                    if game.halfmove >= 100:
                        game.draw_claimed = True
                    elif game.positions[game.position_key()] >= 3:
                        game.draw_claimed = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                if (
                    0 <= x < BOARD
                    and TOP <= y < TOP + BOARD
                    and not game.game_over()
                ):
                    r, c = (y - TOP) // SQ, x // SQ
                    p = game.b[r][c]

                    if p != "." and p.isupper() == game.white_turn:
                        selected = (r, c)
                        legal_moves = game.legal_moves_from(r, c)
                        dragging = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging and selected:
                    x, y = event.pos

                    if (
                        0 <= x < BOARD
                        and TOP <= y < TOP + BOARD
                        and not game.game_over()
                    ):
                        r, c = (y - TOP) // SQ, x // SQ
                        matches = [
                            m for m in legal_moves
                            if m[2] == r and m[3] == c
                        ]

                        if matches:
                            move = matches[0]
                            p = game.b[selected[0]][selected[1]]
                            promotion = None

                            if p.upper() == "P" and r in (0, 7):
                                promotion = promote_dialog(game.white_turn)

                            game.make_move(move, promotion)

                selected, legal_moves, dragging = None, [], False

        draw_game(game, selected, legal_moves, dragging)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
