# board.py

import os
import sys
import pieces
import history

class Square(object):

  _board = None
  _x = 0
  _y = 0
  _horiz = None
  _vert = None
  piece = None
  def __init__(self, board, x, y):
      self._board = board
      self._x = x
      self._y = y
      self._horiz = self._board.x_values[x]
      self._vert = self._board.y_values[y]

  def __repr__(self):
    rep = self.code()
    if self.piece is not None:
      rep = rep + " ({} {})".format(self.piece.color, self.piece.name)
    return rep

  def code(self):
    return self._horiz + self._vert

  def set(self, piece):
    if piece.square is not None:
      piece.square.clear()
    self.piece = piece
    piece.square = self

  def take(self):
    if self.piece is not None:
      piece = self.piece
      self.clear();
      return piece

  def clear(self):
    if not self.is_empty():
      self.piece.square = None
      self.piece = None

  def is_empty(self):
    return self.piece is None

  def is_occupied(self):
    return not self.is_empty()

class Board(object):

  x_values = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  y_values = ['1', '2', '3', '4', '5', '6', '7', '8']

  SIZE = 8
  squares = [] 
  h = None
  flipped = False  # when True, render from black's side of the board

  def __init__(self):
    self.squares = [[ None ] * self.SIZE for i in range(self.SIZE)]
    for x in range(self.SIZE):
      for y in range(self.SIZE):
        self.squares[x][y] = Square(self, x, y)
    self.h = history.History()

  def __getitem__(self, arg):
    return self.squares[arg]

  def at(self, loc):
    if not isinstance(loc, str):
      raise TypeError('Expected string argument.')
    x = self.x_values.index(loc[0])
    y = self.y_values.index(loc[1])
    return self.squares[x][y]

  def exists(self, x, y):
    if x >= self.SIZE or y >= self.SIZE or x < 0 or y < 0:
      return False
    else:
      return True

  def pieces(self, color):
    matches = list()
    for x in range(self.SIZE):
      for y in range(self.SIZE):
        square = self.squares[x][y]
        if square.piece is not None and square.piece.color == color:
          matches.append(square.piece)
    return matches

  def find(self, color, name):
    return list(filter(lambda x: x.name == name, self.pieces(color)))

  def find_first(self, color, name):
    return self.find(color, name)[0]

  def attacks(self, color):
    attacks = []

    for p in self.pieces(color):
      # print(p.square)
      # print(p.attacks())
      for a in p.attacks():
        x, y = a
        attack = self.squares[x][y]
        attacks.append([p.square, attack])
    return attacks

  def to_code(self, coords):
    return list(map(lambda coord: self.x_values[coord[0]] + self.y_values[coord[1]], coords))

  def score(self):
    return self.h.score()

  # Filled glyphs are used for both colors; the foreground color tells them apart.
  # U+FE0E forces text (not emoji) presentation for the pawn.
  GLYPHS = {
    'king': '\u265a', 'queen': '\u265b', 'rook': '\u265c',
    'bishop': '\u265d', 'knight': '\u265e', 'pawn': '\u265f\ufe0e',
  }
  # Outline glyphs for white pieces in the side panel, which has no square background.
  OUTLINE_GLYPHS = {
    'king': '\u2654', 'queen': '\u2655', 'rook': '\u2656',
    'bishop': '\u2657', 'knight': '\u2658', 'pawn': '\u2659',
  }
  LIGHT_BG = '\033[48;5;180m'
  DARK_BG = '\033[48;5;94m'
  LIGHT_MOVE_BG = '\033[48;5;186m'   # last move highlight
  DARK_MOVE_BG = '\033[48;5;136m'
  CHECK_BG = '\033[48;5;160m'        # king in check
  WHITE_FG = '\033[1;38;5;231m'
  BLACK_FG = '\033[1;38;5;16m'
  RESET = '\033[0m'

  def _use_color(self):
    return sys.stdout.isatty() and 'NO_COLOR' not in os.environ

  def symbol(self, piece):
    """Short text for a piece outside the board (e.g. captured pieces)."""
    if not self._use_color():
      return piece.code if piece.color == "white" else "+" + piece.code
    glyphs = self.OUTLINE_GLYPHS if piece.color == "white" else self.GLYPHS
    return glyphs[piece.name]

  def render(self, last_move_squares=(), check_square=None, panel=None):
    """Print the board.

    last_move_squares -- square codes (from, to) to highlight as the last move
    check_square -- square code of a king in check, highlighted in red
    panel -- up to SIZE lines of text shown to the right of the board rows

    Highlights are only drawn on the colored board.
    """
    panel = list(panel or [])
    panel += [""] * (self.SIZE - len(panel))
    if self._use_color():
      self._render_color(last_move_squares, check_square, panel)
    else:
      self._render_plain(panel)

  def _ranks(self):
    return range(self.SIZE) if self.flipped else range(self.SIZE-1, -1, -1)

  def _files(self):
    return range(self.SIZE-1, -1, -1) if self.flipped else range(self.SIZE)

  def _render_color(self, last_move_squares=(), check_square=None, panel=None):
    panel = panel or [""] * self.SIZE
    print()
    for line_no, y in enumerate(self._ranks()):
      row = "{} ".format(y+1)
      for x in self._files():
        square = self.squares[x][y]
        dark = (x + y) % 2 == 0
        if square.code() == check_square:
          bg = self.CHECK_BG
        elif square.code() in last_move_squares:
          bg = self.DARK_MOVE_BG if dark else self.LIGHT_MOVE_BG
        else:
          bg = self.DARK_BG if dark else self.LIGHT_BG
        if square.is_empty():
          row += "{}   {}".format(bg, self.RESET)
        else:
          fg = self.WHITE_FG if square.piece.color == "white" else self.BLACK_FG
          row += "{}{} {} {}".format(bg, fg, self.GLYPHS[square.piece.name], self.RESET)
      print(row + "   " + panel[line_no])
    print("   " + "".join(" {} ".format(self.x_values[x]) for x in self._files()))

  def _render_plain(self, panel=None):
    panel = panel or [""] * self.SIZE
    print()
    print('   ',''.join((["---"] * self.SIZE)))
    for line_no, y in enumerate(self._ranks()):
      row = "{} | ".format(y+1  )
      for x in self._files():
        # print("x", x)
        item = self.squares[x][y]
        if item.is_empty():
          row = row + "   "
        else:
          if item.piece.color == "white":
            row = row + " {} ".format(item.piece.code)
          else:
            row = row + "+{} ".format(item.piece.code)
      print(row, "|", "  " + panel[line_no] if panel[line_no] else "")
    print('   ',''.join((["---"] * self.SIZE)))
    y_labels = '    '
    for x in self._files():
      y_labels += " {} ".format(self.x_values[x])
    print(y_labels)

