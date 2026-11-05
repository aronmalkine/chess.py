# Chess

A two-player, command-line game of chess written in Python. Players take turns typing commands at a prompt; the board is rendered in the terminal with Unicode pieces on colored squares.

## Requirements

- Python 3 (standard library only)
- Optional: [`ipdb`](https://pypi.org/project/ipdb/) (`pip install ipdb`), only needed for the `debug` command

## Running

From the project folder:

```sh
python3 chess.py
# or, since the file is executable:
./chess.py
```

On startup you are prompted for the white and black player names (empty names are rejected), then asked `Ready to start? [Y/n]`. Answering anything other than Enter, `y` or `yes` lets you re-enter the names. Ctrl-C or Ctrl-D at any of these prompts exits cleanly. White moves first.

## Reading the board

In a terminal, the board is drawn with filled Unicode chess glyphs on light and dark squares (a1 is dark):

- White pieces are bold white; black pieces are bold black.
- Ranks are numbered down the left and files lettered along the bottom. Use `flip` to view the board from black's side.
- Squares are written file then rank, e.g. `e4`.

If output is not a terminal (e.g. piped) or the `NO_COLOR` environment variable is set, a plain-text board is used instead:

```
8 |  +r +k +b +Q +K +b +k +r |
...
1 |   r  k  b  Q  K  b  k  r |
      a  b  c  d  e  f  g  h
```

- White pieces are shown plain (` p `); black pieces are prefixed with `+` (`+p `).

| Code | Piece  |
|------|--------|
| `K`  | King   |
| `Q`  | Queen  |
| `r`  | Rook   |
| `b`  | Bishop |
| `k`  | Knight |
| `p`  | Pawn   |

The same letter codes appear in the move history and score output.

## Commands

Type a command at the `<color> to move:` prompt.

| Command | Alias | Description |
|---------|-------|-------------|
| `move <from> <to>` | `m` | Move a piece, e.g. `m d2 d4` |
| `undo` | `u` | Undo the last move (including captures) and switch back to the previous player |
| `board` | `b` | Re-render the board |
| `flip` | `f` | Flip the board to view it from the other side (stays flipped until toggled again) |
| `history` | `h` | Show the moves so far, numbered in rounds (white and black side by side) |
| `score` | `s` | Show material captured by each side and the pieces taken |
| `moves <square>` | | List the squares the piece on `<square>` can move to, e.g. `moves g1` |
| `attacks <square>` | | List the opposing pieces the piece on `<square>` can capture, e.g. `attacks c1` |
| `attacks white` / `attacks black` | | List every capture available to that color (`X takes Y`) |
| `debug` | `d` | Drop into an `ipdb` debugger session; resume the game when you exit it |
| `quit` | `exit`, `q` | Exit the game |

## Features

- Standard starting position and white-moves-first turn order
- Movement rules for all six piece types, including blocking by other pieces, pawn double-step from the starting rank, and pawn diagonal captures
- Captures, with taken pieces tracked per player
- Check detection: you are told `### CHECK! ###` when a move puts the opponent in check
- Illegal-move protection: moving into check, or failing to get out of check, is rejected and the move is rolled back
- Unlimited undo
- Move history in a compact notation (piece letter, destination, `x` for captures)
- Material score using standard-ish values (pawn 100, knight/bishop 350, rook 500, queen 1000)
- Move and attack inspection for individual pieces
- Colored Unicode board, with a `flip` command to view it from either side
- Startup prompts for player names with a ready confirmation

## Known limitations

- Not implemented: castling, en passant, pawn promotion
- Checkmate and stalemate are not detected, so the game only ends when you `quit`
- `moves white` / `moves black` prints `ToDo`
- `debug` fails if `ipdb` is not installed
