# players.py

import history

class Player(object):

  name = None
  color = None
  board = None
  pieces_taken = []

  def __init__(self, name, color, board):
    self.name = name
    self.color = color
    self.board = board

  def move(self, from_square_code, to_square_code):
    if not isinstance(from_square_code, str):
      raise ValueError("Expected string for from_square_code.")
    if not isinstance(to_square_code, str):
      raise ValueError("Expected string for to_square_code.")
    from_square = self.board.at(from_square_code)
    to_square = self.board.at(to_square_code)

    if from_square.piece is None:
      raise ValueError("No piece found on", from_square_code)
    if from_square.piece.color != self.color:
      raise ValueError("Cannot move opponent's piece.")

    if [to_square._x, to_square._y] in from_square.piece.moves():
      taken_piece = None
      if to_square.is_occupied():
        taken_piece = to_square.take()
        self.pieces_taken.append(taken_piece)
      to_square.set(from_square.piece)
      self.board.h.push(history.Event(self, to_square.piece.code, from_square_code, to_square_code, taken_piece))
    else:
      print(from_square.piece.moves())
      raise ValueError("You can't move that piece there!")

  def unmove(self, from_square_code, to_square_code, piece_taken):
    from_square = self.board.at(from_square_code)
    to_square = self.board.at(to_square_code)
    from_square.set(to_square.take())
    if piece_taken is not None:
      self.pieces_taken.remove(piece_taken)
      to_square.set(piece_taken)

  def in_check(self):
    return False

  def check_breaking_moves(self):
    return []
