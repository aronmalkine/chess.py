# history.py

class Event(object):

  player = None
  from_square_code = None
  to_square_code = None
  piece_taken = None

  def __init__(self, player, from_square_code, to_square_code, piece_taken=None):
    if not isinstance(from_square_code, str):
      raise TypeError("Expected square code in string format")
    if not isinstance(to_square_code, str):
      raise TypeError("Expected to code in string format")
    self.player = player
    self.from_square_code = from_square_code
    self.to_square_code = to_square_code
    self.piece_taken = piece_taken

class History(object):

  hist = []

  def push(self, event):
    self.hist.append(event)

  def pop(self):
    return self.hist.pop()

