import sys
import traceback

import board
import history
import players
import pieces

class Chess(object):
  b = None;
  h = None;
  white = None;
  black = None;
  current_player = None;

  def __init__(self):

    self.b = board.Board()

    self.white = players.Player(name='Aron', color='white', board=self.b)
    self.black = players.Player(name='Mous', color='black', board=self.b)

    self.b[0][0].set(pieces.Rook('white'))
    self.b[1][0].set(pieces.Knight('white'))
    self.b[2][0].set(pieces.Bishop('white'))
    self.b[3][0].set(pieces.Queen('white'))
    self.b[4][0].set(pieces.King('white'))
    self.b[5][0].set(pieces.Bishop('white'))
    self.b[6][0].set(pieces.Knight('white'))
    self.b[7][0].set(pieces.Rook('white'))

    self.b[0][1].set(pieces.Pawn('white'))
    self.b[1][1].set(pieces.Pawn('white'))
    self.b[2][1].set(pieces.Pawn('white'))
    self.b[3][1].set(pieces.Pawn('white'))
    self.b[4][1].set(pieces.Pawn('white'))
    self.b[5][1].set(pieces.Pawn('white'))
    self.b[6][1].set(pieces.Pawn('white'))
    self.b[7][1].set(pieces.Pawn('white'))

    self.b[0][6].set(pieces.Pawn('black'))
    self.b[1][6].set(pieces.Pawn('black'))
    self.b[2][6].set(pieces.Pawn('black'))
    self.b[3][6].set(pieces.Pawn('black'))
    self.b[4][6].set(pieces.Pawn('black'))
    self.b[5][6].set(pieces.Pawn('black'))
    self.b[6][6].set(pieces.Pawn('black'))
    self.b[7][6].set(pieces.Pawn('black'))

    self.b[0][7].set(pieces.Rook('black'))
    self.b[1][7].set(pieces.Knight('black'))
    self.b[2][7].set(pieces.Bishop('black'))
    self.b[3][7].set(pieces.Queen('black'))
    self.b[4][7].set(pieces.King('black'))
    self.b[5][7].set(pieces.Bishop('black'))
    self.b[6][7].set(pieces.Knight('black'))
    self.b[7][7].set(pieces.Rook('black'))

    # white to move first
    self.current_player = self.white

  def opponent(self, player):
    if player.color == 'white':
      return self.black
    else:
      return self.white

  def switch_players(self):
    self.current_player = self.opponent(self.current_player)

chess = Chess()

while (not chess.current_player.in_check() or len(chess.current_player.check_breaking_moves()) != 0):
  
  # Show board
  chess.b.dump()

  # Prompt for command  
  command = input("\n{} to move: ".format(chess.current_player.color))

  try:

    if command == 'exit' or command == 'quit':
      # Handle exit
      sys.exit()
    elif command == 'undo':
      # Handle undo
      last_move = chess.b.h.pop()
      last_move.player.unmove(last_move.from_square_code, last_move.to_square_code, last_move.piece_taken)
      chess.switch_players()
    else:
      # Handle move
      c = command.split(" ")  
      if len(c) != 2:
        print("move should be provided in two parts. start square and end square ex: 'd2 d4'")
      else:

        chess.current_player.move(c[0], c[1])

        if chess.current_player.in_check():

          raise ValueError("Cannot put yourself in check!")
          chess.current_player.unmove(chess.h.pop())

        else:

          chess.switch_players()

  except Exception as error:
    print('\n##### ERROR #####\n')
    type_, value_, traceback_ = sys.exc_info()

    trace = traceback.format_tb(traceback_)

    print(*trace, sep = "\n")
    print(type_, '\n')
    print(value_)
    print('\n#####\n')


print("CHECK MATE!! {} wins!".format(chess.opponent(current_player).color))

sys.exit()

# is game over?
# k = b.find('white', 'king')[0]
# print(k)
# if b.in_check('white') and b.check_breaking_moves() == 0:
#   print "Game Over!"
# else:
#   try:
#     white.move('d2', 'd4')
#     if b.in_check('white'):
#       raise ValueError("Cannot put yourself in check!")

# b.dump()




