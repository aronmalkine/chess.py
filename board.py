# board.py

import curses
import pieces
import history

class Square(object):

  x_values = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  y_values = ['1', '2', '3', '4', '5', '6', '7', '8']

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
      self._horiz = self.x_values[x]
      self._vert = self.y_values[y]

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

  SIZE = 8
  squares = [] 
  h = None

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
    x = Square.x_values.index(loc[0])
    y = Square.y_values.index(loc[1])
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
    return filter(lambda x: x.name == pieces. King.name, self.pieces(color))

  def dump(self):
    print(''.join(([" - "] * self.SIZE)))
    for y in range(self.SIZE-1,-1,-1):
      # print("y", y)
      row = ""
      for x in range(self.SIZE):
        # print("x", x)
        item = self.squares[x][y]
        if item.is_empty():
          row = row + "   "
        else:
          if item.piece.color is "white":
            row = row + " {} ".format(item.piece.code)
          else:
            row = row + "+{} ".format(item.piece.code)
      print(row)
    print(''.join(([" - "] * self.SIZE)))


