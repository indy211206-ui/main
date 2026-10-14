// Console Chess in pure C++17 (standard library only)
// Build:  g++ -std=c++17 -O2 -o chess chess.cpp
// Run:    ./chess
//
// Features: full legal move generation, check / checkmate / stalemate,
// castling, en passant, promotion, 50-move rule, insufficient material,
// and an optional computer opponent (alpha-beta search).
//
// Input: coordinate notation, e.g.  e2e4   e7e8q (promotion)   O-O not needed,
// just move the king two squares:  e1g1.
// Commands: moves, board, help, quit

#include <algorithm>
#include <array>
#include <cctype>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

using namespace std;

struct Move {
    int from = 0, to = 0;
    char promo = 0;  // 'q','r','b','n' or 0
};

struct State {
    array<char, 64> b;  // index = rank*8 + file, rank 0 = White's back rank
    bool white = true;
    bool wK = true, wQ = true, bK = true, bQ = true;  // castling rights
    int ep = -1;    // en passant target square
    int half = 0;   // half-move clock (50-move rule)
    int full = 1;   // full-move number
};

static inline int fileOf(int sq) { return sq & 7; }
static inline int rankOf(int sq) { return sq >> 3; }
static inline bool isWhitePiece(char c) { return c >= 'A' && c <= 'Z'; }
static inline bool isBlackPiece(char c) { return c >= 'a' && c <= 'z'; }
static inline bool isEnemy(char c, bool white) {
    return white ? isBlackPiece(c) : isWhitePiece(c);
}

State initialState() {
    State s;
    const string back = "RNBQKBNR";
    for (int f = 0; f < 8; f++) {
        s.b[f] = back[f];
        s.b[8 + f] = 'P';
        s.b[48 + f] = 'p';
        s.b[56 + f] = (char)tolower(back[f]);
        for (int r = 2; r < 6; r++) s.b[r * 8 + f] = '.';
    }
    return s;
}

// ---------------------------------------------------------------- attacks
bool isAttacked(const State& s, int sq, bool byWhite) {
    int r = rankOf(sq), f = fileOf(sq);

    // Pawns
    int pr = byWhite ? r - 1 : r + 1;
    if (pr >= 0 && pr < 8) {
        char pawn = byWhite ? 'P' : 'p';
        for (int df = -1; df <= 1; df += 2) {
            int pf = f + df;
            if (pf >= 0 && pf < 8 && s.b[pr * 8 + pf] == pawn) return true;
        }
    }
    // Knights
    static const int kn[8][2] = {{1, 2}, {2, 1}, {-1, 2}, {-2, 1},
                                 {1, -2}, {2, -1}, {-1, -2}, {-2, -1}};
    char knight = byWhite ? 'N' : 'n';
    for (auto& d : kn) {
        int nf = f + d[0], nr = r + d[1];
        if (nf >= 0 && nf < 8 && nr >= 0 && nr < 8 && s.b[nr * 8 + nf] == knight)
            return true;
    }
    // King
    char king = byWhite ? 'K' : 'k';
    for (int dr = -1; dr <= 1; dr++)
        for (int df = -1; df <= 1; df++) {
            if (!dr && !df) continue;
            int nf = f + df, nr = r + dr;
            if (nf >= 0 && nf < 8 && nr >= 0 && nr < 8 && s.b[nr * 8 + nf] == king)
                return true;
        }
    // Sliders
    char rook = byWhite ? 'R' : 'r', bishop = byWhite ? 'B' : 'b',
         queen = byWhite ? 'Q' : 'q';
    static const int dirs[8][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1},
                                   {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    for (int i = 0; i < 8; i++) {
        int nf = f + dirs[i][0], nr = r + dirs[i][1];
        while (nf >= 0 && nf < 8 && nr >= 0 && nr < 8) {
            char c = s.b[nr * 8 + nf];
            if (c != '.') {
                if (c == queen || (i < 4 ? c == rook : c == bishop)) return true;
                break;
            }
            nf += dirs[i][0];
            nr += dirs[i][1];
        }
    }
    return false;
}

int findKing(const State& s, bool white) {
    char k = white ? 'K' : 'k';
    for (int i = 0; i < 64; i++)
        if (s.b[i] == k) return i;
    return -1;
}

bool inCheck(const State& s, bool white) {
    int k = findKing(s, white);
    return k >= 0 && isAttacked(s, k, !white);
}

// ---------------------------------------------------------------- make move
State makeMove(State s, const Move& m) {
    char p = s.b[m.from];
    char cap = s.b[m.to];
    bool pawn = tolower(p) == 'p';
    bool white = s.white;

    // En passant capture
    if (pawn && m.to == s.ep && cap == '.' && fileOf(m.from) != fileOf(m.to)) {
        s.b[m.to + (white ? -8 : 8)] = '.';
        cap = 'x';
    }

    s.b[m.to] = p;
    s.b[m.from] = '.';

    // Promotion
    if (m.promo) s.b[m.to] = white ? (char)toupper(m.promo) : (char)tolower(m.promo);

    // Castling: move the rook too
    if (tolower(p) == 'k' && abs(m.to - m.from) == 2) {
        if (m.to > m.from) { s.b[m.from + 1] = s.b[m.from + 3]; s.b[m.from + 3] = '.'; }
        else               { s.b[m.from - 1] = s.b[m.from - 4]; s.b[m.from - 4] = '.'; }
    }

    // En passant square
    s.ep = (pawn && abs(m.to - m.from) == 16) ? (m.from + m.to) / 2 : -1;

    // Castling rights
    if (p == 'K') s.wK = s.wQ = false;
    if (p == 'k') s.bK = s.bQ = false;
    for (int sq : {m.from, m.to}) {
        if (sq == 0)  s.wQ = false;
        if (sq == 7)  s.wK = false;
        if (sq == 56) s.bQ = false;
        if (sq == 63) s.bK = false;
    }

    s.half = (pawn || cap != '.') ? 0 : s.half + 1;
    if (!white) s.full++;
    s.white = !white;
    return s;
}

// ---------------------------------------------------------------- generation
void addPawnMove(vector<Move>& out, int from, int to, bool white) {
    int promoRank = white ? 7 : 0;
    if (rankOf(to) == promoRank) {
        for (char c : {'q', 'r', 'b', 'n'}) out.push_back({from, to, c});
    } else {
        out.push_back({from, to, 0});
    }
}

vector<Move> pseudoMoves(const State& s) {
    vector<Move> out;
    bool w = s.white;
    static const int kn[8][2] = {{1, 2}, {2, 1}, {-1, 2}, {-2, 1},
                                 {1, -2}, {2, -1}, {-1, -2}, {-2, -1}};
    static const int dirs[8][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1},
                                   {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

    for (int sq = 0; sq < 64; sq++) {
        char c = s.b[sq];
        if (c == '.' || (w ? !isWhitePiece(c) : !isBlackPiece(c))) continue;
        int r = rankOf(sq), f = fileOf(sq);
        char t = (char)tolower(c);

        if (t == 'p') {
            int dir = w ? 1 : -1, startRank = w ? 1 : 6;
            int nr = r + dir;
            if (nr < 0 || nr > 7) continue;
            if (s.b[nr * 8 + f] == '.') {
                addPawnMove(out, sq, nr * 8 + f, w);
                if (r == startRank && s.b[(r + 2 * dir) * 8 + f] == '.')
                    out.push_back({sq, (r + 2 * dir) * 8 + f, 0});
            }
            for (int df = -1; df <= 1; df += 2) {
                int nf = f + df;
                if (nf < 0 || nf > 7) continue;
                int to = nr * 8 + nf;
                if (isEnemy(s.b[to], w) || (to == s.ep && s.b[to] == '.'))
                    addPawnMove(out, sq, to, w);
            }
        } else if (t == 'n') {
            for (auto& d : kn) {
                int nf = f + d[0], nr = r + d[1];
                if (nf < 0 || nf > 7 || nr < 0 || nr > 7) continue;
                char x = s.b[nr * 8 + nf];
                if (x == '.' || isEnemy(x, w)) out.push_back({sq, nr * 8 + nf, 0});
            }
        } else if (t == 'k') {
            for (int dr = -1; dr <= 1; dr++)
                for (int df = -1; df <= 1; df++) {
                    if (!dr && !df) continue;
                    int nf = f + df, nr = r + dr;
                    if (nf < 0 || nf > 7 || nr < 0 || nr > 7) continue;
                    char x = s.b[nr * 8 + nf];
                    if (x == '.' || isEnemy(x, w)) out.push_back({sq, nr * 8 + nf, 0});
                }
            // Castling
            int home = w ? 4 : 60;
            if (sq == home && !isAttacked(s, home, !w)) {
                bool ks = w ? s.wK : s.bK, qs = w ? s.wQ : s.bQ;
                if (ks && s.b[home + 1] == '.' && s.b[home + 2] == '.' &&
                    s.b[home + 3] == (w ? 'R' : 'r') &&
                    !isAttacked(s, home + 1, !w) && !isAttacked(s, home + 2, !w))
                    out.push_back({sq, home + 2, 0});
                if (qs && s.b[home - 1] == '.' && s.b[home - 2] == '.' &&
                    s.b[home - 3] == '.' && s.b[home - 4] == (w ? 'R' : 'r') &&
                    !isAttacked(s, home - 1, !w) && !isAttacked(s, home - 2, !w))
                    out.push_back({sq, home - 2, 0});
            }
        } else {  // sliders
            int lo = (t == 'b') ? 4 : 0, hi = (t == 'r') ? 4 : 8;
            for (int i = lo; i < hi; i++) {
                int nf = f + dirs[i][0], nr = r + dirs[i][1];
                while (nf >= 0 && nf < 8 && nr >= 0 && nr < 8) {
                    char x = s.b[nr * 8 + nf];
                    if (x == '.') out.push_back({sq, nr * 8 + nf, 0});
                    else {
                        if (isEnemy(x, w)) out.push_back({sq, nr * 8 + nf, 0});
                        break;
                    }
                    nf += dirs[i][0];
                    nr += dirs[i][1];
                }
            }
        }
    }
    return out;
}

vector<Move> legalMoves(const State& s) {
    vector<Move> out;
    for (auto& m : pseudoMoves(s)) {
        State n = makeMove(s, m);
        if (!inCheck(n, s.white)) out.push_back(m);
    }
    return out;
}

// ---------------------------------------------------------------- helpers
string sqName(int sq) {
    return string(1, (char)('a' + fileOf(sq))) + string(1, (char)('1' + rankOf(sq)));
}
string moveStr(const Move& m) {
    string s = sqName(m.from) + sqName(m.to);
    if (m.promo) s += m.promo;
    return s;
}

void printBoard(const State& s) {
    cout << "\n    a b c d e f g h\n   +----------------+\n";
    for (int r = 7; r >= 0; r--) {
        cout << " " << r + 1 << " | ";
        for (int f = 0; f < 8; f++) cout << s.b[r * 8 + f] << ' ';
        cout << "| " << r + 1 << "\n";
    }
    cout << "   +----------------+\n    a b c d e f g h\n\n";
}

bool insufficientMaterial(const State& s) {
    int minors = 0;
    for (char c : s.b) {
        char t = (char)tolower(c);
        if (t == 'p' || t == 'r' || t == 'q') return false;
        if (t == 'n' || t == 'b') minors++;
    }
    return minors <= 1;
}

// ---------------------------------------------------------------- AI
int pieceValue(char c) {
    switch (tolower(c)) {
        case 'p': return 100;
        case 'n': return 320;
        case 'b': return 330;
        case 'r': return 500;
        case 'q': return 900;
        default:  return 0;
    }
}

int evaluate(const State& s) {  // from side-to-move's perspective
    int score = 0;
    for (int sq = 0; sq < 64; sq++) {
        char c = s.b[sq];
        if (c == '.') continue;
        int r = rankOf(sq), f = fileOf(sq);
        int v = pieceValue(c);
        char t = (char)tolower(c);
        if (t != 'k' && t != 'r') {  // centralization bonus
            double cd = (3.5 - abs(f - 3.5)) + (3.5 - abs(r - 3.5));
            v += (int)(cd * 4);
        }
        if (t == 'p') v += (isWhitePiece(c) ? r : 7 - r) * 6;  // pawn advancement
        score += isWhitePiece(c) ? v : -v;
    }
    return s.white ? score : -score;
}

const int MATE = 100000;

int negamax(const State& s, int depth, int alpha, int beta, int ply) {
    if (s.half >= 100 || insufficientMaterial(s)) return 0;
    if (depth == 0) return evaluate(s);

    vector<Move> moves = legalMoves(s);
    if (moves.empty()) return inCheck(s, s.white) ? -MATE + ply : 0;

    // Move ordering: captures / promotions first (MVV-LVA-ish)
    auto score = [&](const Move& m) {
        int v = pieceValue(s.b[m.to]) * 10 - pieceValue(s.b[m.from]);
        if (m.promo) v += 800;
        return v;
    };
    sort(moves.begin(), moves.end(),
         [&](const Move& a, const Move& b) { return score(a) > score(b); });

    for (auto& m : moves) {
        int val = -negamax(makeMove(s, m), depth - 1, -beta, -alpha, ply + 1);
        if (val >= beta) return beta;
        if (val > alpha) alpha = val;
    }
    return alpha;
}

Move bestMove(const State& s, int depth) {
    vector<Move> moves = legalMoves(s);
    Move best = moves[0];
    int alpha = -MATE * 2;
    for (auto& m : moves) {
        int val = -negamax(makeMove(s, m), depth - 1, -MATE * 2, -alpha, 1);
        if (val > alpha) { alpha = val; best = m; }
    }
    return best;
}

// ---------------------------------------------------------------- UI
bool parseMove(const string& in, const vector<Move>& legal, Move& out) {
    string t;
    for (char c : in) if (!isspace((unsigned char)c)) t += (char)tolower(c);
    if (t.size() < 4 || t.size() > 5) return false;
    if (t[0] < 'a' || t[0] > 'h' || t[2] < 'a' || t[2] > 'h' ||
        t[1] < '1' || t[1] > '8' || t[3] < '1' || t[3] > '8') return false;
    int from = (t[1] - '1') * 8 + (t[0] - 'a');
    int to = (t[3] - '1') * 8 + (t[2] - 'a');
    char promo = t.size() == 5 ? t[4] : 0;
    for (auto& m : legal) {
        if (m.from == from && m.to == to) {
            if (m.promo) {
                char want = promo ? promo : 'q';  // default to queen
                if (m.promo != want) continue;
            } else if (promo) continue;
            out = m;
            return true;
        }
    }
    return false;
}

void printHelp() {
    cout << "\nEnter moves as <from><to>, e.g. e2e4. Promotion: e7e8q (default queen).\n"
            "Castle by moving the king two squares (e1g1 / e1c1).\n"
            "Commands: moves (list legal moves), board, help, resign, quit\n\n";
}

int main() {
    cout << "=== C++ Chess ===\n"
            "1) Play vs computer\n2) Two players (hot-seat)\nChoose [1/2]: ";
    string choice;
    getline(cin, choice);
    bool vsComputer = (choice != "2");
    bool humanWhite = true;
    int depth = 3;

    if (vsComputer) {
        cout << "Play as White or Black? [w/b]: ";
        string c; getline(cin, c);
        humanWhite = !(c == "b" || c == "B");
        cout << "Difficulty 1-4 (default 3): ";
        string d; getline(cin, d);
        if (!d.empty() && d[0] >= '1' && d[0] <= '4') depth = d[0] - '0';
    }

    State s = initialState();
    printHelp();

    while (true) {
        printBoard(s);
        vector<Move> legal = legalMoves(s);
        bool check = inCheck(s, s.white);

        if (legal.empty()) {
            if (check) cout << "Checkmate! " << (s.white ? "Black" : "White") << " wins.\n";
            else cout << "Stalemate. Draw.\n";
            break;
        }
        if (s.half >= 100) { cout << "Draw by the 50-move rule.\n"; break; }
        if (insufficientMaterial(s)) { cout << "Draw by insufficient material.\n"; break; }
        if (check) cout << "*** Check! ***\n";

        bool computerTurn = vsComputer && (s.white != humanWhite);
        if (computerTurn) {
            cout << "Computer is thinking...\n";
            Move m = bestMove(s, depth);
            cout << "Computer plays: " << moveStr(m) << "\n";
            s = makeMove(s, m);
            continue;
        }

        cout << (s.white ? "White" : "Black") << " to move (" << s.full << "): ";
        string line;
        if (!getline(cin, line)) break;
        string cmd;
        for (char c : line) if (!isspace((unsigned char)c)) cmd += (char)tolower(c);

        if (cmd == "quit" || cmd == "exit") break;
        if (cmd == "resign") {
            cout << (s.white ? "White" : "Black") << " resigns. "
                 << (s.white ? "Black" : "White") << " wins.\n";
            break;
        }
        if (cmd == "help") { printHelp(); continue; }
        if (cmd == "board") continue;
        if (cmd == "moves") {
            for (auto& m : legal) cout << moveStr(m) << ' ';
            cout << "\n";
            continue;
        }

        Move m;
        if (!parseMove(cmd, legal, m)) {
            cout << "Illegal or unrecognized move. Type 'moves' to see legal moves.\n";
            continue;
        }
        s = makeMove(s, m);
    }
    return 0;
}
