# pieces.py

from abc import abstractmethod

class Piece(object):
  name = None
  code = None
  color = None
  square = None
  def __init__(self, color):
    if color not in [ "white", "black" ]:
      raise ValueError("Color must be white or black")
    self.color = color
  @abstractmethod
  def moves(self):
    pass

  def valid_moves(self, possible_moves, moves_only=False, attacks_only=False):
    b = self.square._board
    valid = []
    for m in possible_moves:
      x1 = m[0]
      y1 = m[1]
      if b.exists(x1, y1):
        target_square = b[x1][y1]
        if not attacks_only:
          if target_square.is_empty() or target_square.piece.color != self.color:
            valid.append(m)
        else:
          if target_square.piece.color != self.color:
            valid.append(m)
    return valid

  def vector(self, move_memo, x, y, func):

    b = self.square._board
    x1, y1 = func(x, y)

    if not b.exists(x1, y1):
      return move_memo
    else:

      current_square = b[x1][y1]

      # if you run into a piece...
      if current_square.is_occupied():

        # ...and the piece is opponent: you can move there, but not beyond
        if current_square.piece.color != self.color:

          move_memo.append([x1, y1])

          return move_memo

        # ...and it's your own piece: you can't move there nor beyond
        else:

          return move_memo
        
      else:

        # if the square is empty: add this square the to moves and continue on
        move_memo.append([x1, y1])
        return self.vector(move_memo, x1, y1, func)
      

class King(Piece):
  name = "king"
  code = "K"
  def moves(self):
    if self.square is None:
      raise ValueError('Piece has not been set on the board.')
    
    print('moves from', self.square._x, self.square._y, self.square.code())
    moves = []
    x = self.square._x
    y = self.square._y
    possible_moves = [ [x, y+1], [x+1, y+1], [x+1, y], [x+1, y-1], [x, y-1], [x-1, y-1], [x-1, y], [x-1, y+1] ]
    moves = self.valid_moves(possible_moves)
    return moves

class Knight(Piece):
  name = "knight"
  code = "k"
  def moves(self):
    moves = []
    x = self.square._x
    y = self.square._y
    possible_moves = [ [x+1, y+2], [x+1, y-2], [x-1, y+2], [x-1, y-2], [x+2, y+1], [x+2, y-1],  [x-2, y+1], [x-2, y-1] ]
    moves = self.valid_moves(possible_moves)
    return moves

class Pawn(Piece):
  name = "pawn"
  code = "p"
  def moves(self):
    moves = []
    b = self.square._board
    x = self.square._x
    y = self.square._y
    if self.color == 'white':
      # normal move
      possible_moves = [ [x, y+1] ]
      # two forward on first move
      if y == 1:
        possible_moves.append( [x, y+2] )
      moves = self.valid_moves(possible_moves, moves_only=True)
      # normal attacks
      # If diagonal forward squares are occupied by opponent, add to moves
      possible_attacks = []
      diagonal = b[x+1][y+1]
      if diagonal.is_occupied() and diagonal.piece.color != 'white':
        possible_attacks.append( [x+1, y+1] )
      diagonal = b[x-1][y+1]
      if  diagonal.is_occupied() and diagonal.piece.color != 'white':
        possible_attacks.append( [x+1, y+1] )
      moves = moves + self.valid_moves(possible_moves=possible_attacks, attacks_only=True)
    else:
      # normal move
      possible_moves = [ [x, y-1] ]
      # two forward on first move
      if y == 6:
        possible_moves.append( [x, y-2] )
      moves = self.valid_moves(possible_moves, moves_only=True)
      # normal attacks
      # If diagonal forward squares are occupied by opponent, add to moves
      possible_attacks = []
      diagonal = b[x+1][y-1]
      if not diagonal.is_empty() and diagonal.piece.color != 'white':
        possible_attacks.append( [x+1, y-1] )
      diagonal = b[x-1][y-1]
      if not diagonal.is_empty() and diagonal.piece.color != 'white':
        possible_attacks.append( [x+1, y-1] )
      moves = moves + self.valid_moves(possible_moves=possible_attacks, attacks_only=True)
    return moves

class Rook(Piece):
  name = "rook"
  code = "r"
  def moves(self):
    moves = []
    funcs = [ 
              lambda x, y: [x+1, y], 
              lambda x, y: [x-1, y], 
              lambda x, y: [x, y+1],
              lambda x, y: [x, y-1] 
            ]
    for func in funcs:
      moves = moves + self.vector([], self.square._x, self.square._y, func)
    return moves

class Bishop(Piece):
  name = "bishop"
  code = "b"
  def moves(self):
    moves = []
    funcs = [ 
              lambda x, y: [x+1, y+1], 
              lambda x, y: [x-1, y+1], 
              lambda x, y: [x-1, y-1],
              lambda x, y: [x+1, y-1] 
            ]
    for func in funcs:
      moves = moves + self.vector([], self.square._x, self.square._y, func)
    return moves

class Queen(Piece):
  name = "queen"
  code = "Q"
  def moves(self):
    moves = []
    funcs = [ 
              lambda x, y: [x+1, y], 
              lambda x, y: [x-1, y], 
              lambda x, y: [x, y+1],
              lambda x, y: [x, y-1],
              lambda x, y: [x+1, y+1], 
              lambda x, y: [x-1, y+1], 
              lambda x, y: [x-1, y-1],
              lambda x, y: [x+1, y-1] 
            ]
    for func in funcs:
      moves = moves + self.vector([], self.square._x, self.square._y, func)
    return moves

