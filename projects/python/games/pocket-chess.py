"""
Pocket Chess — a small desktop chess app built with Python + Tkinter.

Setup:
    py -m pip install python-chess
Run:
    py pocket_chess.py

Features:
- Click a piece, then click a highlighted legal destination.
- Play White vs Black locally, or toggle the computer opponent.
- Undo, reset, flip board, move list, check/checkmate/draw status.
"""

import random
import tkinter as tk
from tkinter import messagebox

try:
    import chess
except ImportError:
    raise SystemExit(
        "Missing dependency: python-chess\n"
        "Install it with: py -m pip install python-chess"
    )

SQUARE_SIZE = 76
BOARD_SIZE = SQUARE_SIZE * 8
LIGHT = "#EEEED2"
DARK = "#769656"
SELECTED = "#F6F669"
LAST_MOVE = "#CDD26A"
LEGAL_DOT = "#3F6B3A"
PANEL = "#202522"
PANEL_TEXT = "#F1F4ED"
ACCENT = "#A8C686"

PIECE_GLYPHS = {
    chess.Piece.from_symbol("K"): "♔",
    chess.Piece.from_symbol("Q"): "♕",
    chess.Piece.from_symbol("R"): "♖",
    chess.Piece.from_symbol("B"): "♗",
    chess.Piece.from_symbol("N"): "♘",
    chess.Piece.from_symbol("P"): "♙",
    chess.Piece.from_symbol("k"): "♚",
    chess.Piece.from_symbol("q"): "♛",
    chess.Piece.from_symbol("r"): "♜",
    chess.Piece.from_symbol("b"): "♝",
    chess.Piece.from_symbol("n"): "♞",
    chess.Piece.from_symbol("p"): "♟",
}

VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 335,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}


class PocketChess:
    def __init__(self, root):
        self.root = root
        self.root.title("Pocket Chess")
        self.root.configure(bg=PANEL)
        self.root.resizable(False, False)

        self.board = chess.Board()
        self.selected = None
        self.legal_targets = []
        self.flipped = False
        self.vs_computer = tk.BooleanVar(value=False)
        self.computer_color = chess.BLACK
        self.last_move = None

        outer = tk.Frame(root, bg=PANEL, padx=18, pady=18)
        outer.pack()

        left = tk.Frame(outer, bg=PANEL)
        left.grid(row=0, column=0, sticky="n")

        tk.Label(
            left, text="POCKET CHESS", bg=PANEL, fg=PANEL_TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.status = tk.Label(
            left, text="", bg=PANEL, fg=ACCENT,
            font=("Segoe UI", 11, "bold"), width=34, anchor="w"
        )
        self.status.pack(fill="x", pady=(0, 8))

        self.canvas = tk.Canvas(
            left, width=BOARD_SIZE, height=BOARD_SIZE,
            bg=LIGHT, highlightthickness=0, cursor="hand2"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        controls = tk.Frame(left, bg=PANEL)
        controls.pack(fill="x", pady=(12, 0))

        self.make_button(controls, "New game", self.new_game).pack(side="left", padx=(0, 6))
        self.make_button(controls, "Undo", self.undo).pack(side="left", padx=6)
        self.make_button(controls, "Flip board", self.flip_board).pack(side="left", padx=6)

        options = tk.Frame(left, bg=PANEL)
        options.pack(fill="x", pady=(10, 0))
        tk.Checkbutton(
            options, text="Play against computer (you are White)",
            variable=self.vs_computer, command=self.on_mode_change,
            bg=PANEL, fg=PANEL_TEXT, selectcolor="#39433B",
            activebackground=PANEL, activeforeground=PANEL_TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        right = tk.Frame(outer, bg="#2B332D", padx=14, pady=14)
        right.grid(row=0, column=1, padx=(18, 0), sticky="n")
        tk.Label(
            right, text="MOVE HISTORY", bg="#2B332D", fg=PANEL_TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.move_list = tk.Listbox(
            right, width=23, height=27, bg="#171C19", fg=PANEL_TEXT,
            selectbackground="#536B4C", borderwidth=0,
            font=("Consolas", 10), activestyle="none"
        )
        self.move_list.pack()

        tk.Label(
            right, text="Click a piece, then its destination.",
            bg="#2B332D", fg="#C4CEC3", wraplength=185,
            justify="left", font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(12, 0))

        self.draw()

    def make_button(self, parent, label, command):
        return tk.Button(
            parent, text=label, command=command,
            bg="#39483A", fg=PANEL_TEXT, activebackground="#526B4D",
            activeforeground="white", relief="flat", padx=10, pady=7,
            font=("Segoe UI", 9, "bold"), cursor="hand2"
        )

    def square_to_xy(self, square):
        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)
        if self.flipped:
            col = 7 - file_index
            row = rank_index
        else:
            col = file_index
            row = 7 - rank_index
        return col * SQUARE_SIZE, row * SQUARE_SIZE

    def xy_to_square(self, x, y):
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        if not (0 <= col < 8 and 0 <= row < 8):
            return None
        if self.flipped:
            file_index = 7 - col
            rank_index = row
        else:
            file_index = col
            rank_index = 7 - row
        return chess.square(file_index, rank_index)

    def draw(self):
        self.canvas.delete("all")
        legal_set = set(self.legal_targets)

        for row in range(8):
            for col in range(8):
                square = self.xy_to_square(col * SQUARE_SIZE + 1, row * SQUARE_SIZE + 1)
                x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
                x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE
                color = LIGHT if (chess.square_file(square) + chess.square_rank(square)) % 2 == 0 else DARK

                if self.last_move and square in (self.last_move.from_square, self.last_move.to_square):
                    color = LAST_MOVE
                if square == self.selected:
                    color = SELECTED

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

                piece = self.board.piece_at(square)
                if piece:
                    glyph = PIECE_GLYPHS[piece]
                    # A subtle contrasting outline makes the Unicode pieces easier to read.
                    fg = "#FAFAF5" if piece.color == chess.WHITE else "#171A17"
                    outline = "#343B32" if piece.color == chess.WHITE else "#D7DED2"
                    self.canvas.create_text(
                        x1 + SQUARE_SIZE / 2 + 1, y1 + SQUARE_SIZE / 2 + 2,
                        text=glyph, font=("DejaVu Sans", 43), fill=outline
                    )
                    self.canvas.create_text(
                        x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2,
                        text=glyph, font=("DejaVu Sans", 43), fill=fg
                    )

                if square in legal_set and not piece:
                    cx, cy = x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2
                    self.canvas.create_oval(cx - 8, cy - 8, cx + 8, cy + 8,
                                            fill=LEGAL_DOT, outline="")
                elif square in legal_set and piece:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5,
                                            outline=LEGAL_DOT, width=4)

        # Coordinates
        for i in range(8):
            file_label = "abcdefgh"[7 - i if self.flipped else i]
            rank_label = str(i + 1 if self.flipped else 8 - i)
            self.canvas.create_text(
                i * SQUARE_SIZE + 7, BOARD_SIZE - 8, text=file_label,
                fill="#465641", font=("Segoe UI", 8, "bold"), anchor="w"
            )
            self.canvas.create_text(
                5, i * SQUARE_SIZE + 8, text=rank_label,
                fill="#465641", font=("Segoe UI", 8, "bold"), anchor="nw"
            )

        self.update_status()
        self.update_move_list()

    def update_status(self):
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            msg = f"Checkmate — {winner} wins!"
        elif self.board.is_stalemate():
            msg = "Draw — stalemate"
        elif self.board.is_insufficient_material():
            msg = "Draw — insufficient material"
        elif self.board.can_claim_fifty_moves() or self.board.is_seventyfive_moves():
            msg = "Draw available — 50-move rule"
        elif self.board.is_check():
            msg = ("White" if self.board.turn else "Black") + " is in check!"
        else:
            msg = ("White" if self.board.turn else "Black") + " to move"
        if self.vs_computer.get() and not self.board.is_game_over():
            msg += "  ·  vs computer"
        self.status.config(text=msg)

    def update_move_list(self):
        self.move_list.delete(0, tk.END)
        temp = chess.Board()
        moves = list(self.board.move_stack)
        for i in range(0, len(moves), 2):
            white_move = moves[i]
            san_white = temp.san(white_move)
            temp.push(white_move)
            line = f"{i // 2 + 1:>2}. {san_white:<7}"
            if i + 1 < len(moves):
                san_black = temp.san(moves[i + 1])
                temp.push(moves[i + 1])
                line += san_black
            self.move_list.insert(tk.END, line)
        if self.move_list.size():
            self.move_list.see(tk.END)

    def on_click(self, event):
        if self.board.is_game_over():
            return
        if self.vs_computer.get() and self.board.turn == self.computer_color:
            return

        square = self.xy_to_square(event.x, event.y)
        if square is None:
            return

        if self.selected is not None:
            matching = [m for m in self.board.legal_moves
                        if m.from_square == self.selected and m.to_square == square]
            if matching:
                move = matching[0]
                if move.promotion:
                    move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                self.play_move(move)
                return

        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            self.selected = square
            self.legal_targets = [m.to_square for m in self.board.legal_moves
                                  if m.from_square == square]
        else:
            self.selected = None
            self.legal_targets = []
        self.draw()

    def play_move(self, move):
        if move not in self.board.legal_moves:
            return
        self.board.push(move)
        self.last_move = move
        self.selected = None
        self.legal_targets = []
        self.draw()
        if self.vs_computer.get() and not self.board.is_game_over() and self.board.turn == self.computer_color:
            self.root.after(250, self.computer_move)

    def computer_move(self):
        if self.board.is_game_over() or self.board.turn != self.computer_color:
            return
        move = self.choose_computer_move()
        if move:
            self.play_move(move)

    def evaluate(self, board):
        if board.is_checkmate():
            return -100000 if board.turn == chess.WHITE else 100000
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        score = 0
        for square, piece in board.piece_map().items():
            value = VALUES[piece.piece_type]
            # Mild center preference for pawns and minor pieces.
            file_c = abs(3.5 - chess.square_file(square))
            rank_c = abs(3.5 - chess.square_rank(square))
            center_bonus = int(12 - 3 * (file_c + rank_c))
            if piece.piece_type in (chess.PAWN, chess.KNIGHT, chess.BISHOP):
                value += center_bonus
            score += value if piece.color == chess.WHITE else -value
        return score

    def minimax(self, depth, alpha, beta):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate(self.board), None

        best_move = None
        maximizing = self.board.turn == chess.WHITE
        moves = list(self.board.legal_moves)
        random.shuffle(moves)
        # Try captures first to help the simple search find tactical moves.
        moves.sort(key=lambda m: self.board.is_capture(m), reverse=True)

        if maximizing:
            best_score = -float("inf")
            for move in moves:
                self.board.push(move)
                score, _ = self.minimax(depth - 1, alpha, beta)
                self.board.pop()
                if score > best_score:
                    best_score, best_move = score, move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        else:
            best_score = float("inf")
            for move in moves:
                self.board.push(move)
                score, _ = self.minimax(depth - 1, alpha, beta)
                self.board.pop()
                if score < best_score:
                    best_score, best_move = score, move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score, best_move

    def choose_computer_move(self):
        # Search a little deeper in quieter positions; keep the app responsive.
        _, move = self.minimax(2, -float("inf"), float("inf"))
        if move is None:
            legal = list(self.board.legal_moves)
            return random.choice(legal) if legal else None
        return move

    def undo(self):
        if not self.board.move_stack:
            return
        self.board.pop()
        if self.vs_computer.get() and self.board.move_stack and self.board.turn == self.computer_color:
            self.board.pop()
        self.last_move = self.board.peek() if self.board.move_stack else None
        self.selected = None
        self.legal_targets = []
        self.draw()

    def new_game(self):
        if self.board.move_stack and not messagebox.askyesno("New game", "Start a new game? Current progress will be lost."):
            return
        self.board.reset()
        self.selected = None
        self.legal_targets = []
        self.last_move = None
        self.draw()

    def flip_board(self):
        self.flipped = not self.flipped
        self.draw()

    def on_mode_change(self):
        self.selected = None
        self.legal_targets = []
        self.draw()
        if self.vs_computer.get() and self.board.turn == self.computer_color and not self.board.is_game_over():
            self.root.after(250, self.computer_move)


if __name__ == "__main__":
    root = tk.Tk()
    app = PocketChess(root)
    root.mainloop()
