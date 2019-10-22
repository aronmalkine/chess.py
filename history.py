# history.py

class Event(object):

  player = None
  piece_moved = None
  from_square_code = None
  to_square_code = None
  piece_taken = None

  def __init__(self, player, piece_moved, from_square_code, to_square_code, piece_taken=None):
    if not isinstance(from_square_code, str):
      raise TypeError("Expected square code in string format")
    if not isinstance(to_square_code, str):
      raise TypeError("Expected to code in string format")
    self.player = player
    self.piece_moved = piece_moved
    self.from_square_code = from_square_code
    self.to_square_code = to_square_code
    self.piece_taken = piece_taken

  def __str__(self):
    move = ""
    if self.piece_moved != 'p':
      move = self.piece_moved
    move += self.to_square_code
    if self.piece_taken:
      move = move + "x" + self.piece_taken.code
    return move

class History(object):

  hist = []

  def push(self, event):
    self.hist.append(event)

  def pop(self):
    return self.hist.pop()

  def output(self):
    round = []
    index = 1
    
    for h in self.hist:
      round.append(h)
      if len(round) == 2:
        print("{:3}. {:8} {:8}".format(index, str(round[0]), str(round[1])))
        round = []
        index += 1
    if len(round) == 1:
      print("{:3}. {:8}".format(index, str(round[0])))
