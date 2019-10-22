import sys
import traceback

import board
import history
import players
import pieces

class Chess(object):
  b = None;
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

  def in_check(self, player):
    return False
    # return board.find(player.color, 'king').square.code() in board.to_code(self.player.opponent().attacks())

chess = Chess()

# Show board
chess.b.render()

while True: #(not chess.in_check(chess.current_player) or len(chess.check_breaking_moves(chess.current_player)) != 0):  

  # Prompt for command  
  input_data = input("\n{} to move: ".format(chess.current_player.color))

  try:

    input_data = input_data.split(" ")

    command = input_data[0]

    if command in [ 'exit', 'quit', 'q']:
      # Handle exit
      print("\nHope you enjoyed the game! Play again soon!\n\n")
      sys.exit()

    elif command in [ 'undo', 'u']:
      # Handle undo
      last_move = chess.b.h.pop()
      last_move.player.unmove(last_move.from_square_code, last_move.to_square_code, last_move.piece_taken)
      chess.switch_players()
      chess.b.render()

    elif command in [ 'history', 'h' ]:
      chess.b.h.output()

    elif command in [ 'score', 's' ]:
      white_material, black_material, white_pieces, black_pieces = chess.b.score()
      print("white: {material:>6}".format(material=white_material), ", ".join(white_pieces))
      print("black: {material:>6}".format(material=black_material), ", ".join(black_pieces))

    elif command in [ 'board', 'b']:
      chess.b.render()

    elif command == 'moves':

      if len(input_data[1]) == 2:

        target = input_data[1]

        print(", ".join(chess.b.to_code(chess.b.at(target).piece.moves())))

      elif input_data[1] == 'all':

        print("ToDo")

    elif command == "attacks":

      target = input_data[1]

      if target in [ "white", "black" ]:

        for a in chess.b.attacks(target):
          print(a[0], "takes", a[1])

      elif len(target) == 2:

        attacks = chess.b.at(target).piece.attacks()

        readable_attacks = chess.b.to_code(attacks)

        print(", ".join(readable_attacks))

      else:
        raise ValueError("attacks command expects 'white', 'black', or an occupied square.")

    elif command in [ "move", "m" ]:

      move_from = input_data[1]
      move_to = input_data[2]

      chess.current_player.move(move_from, move_to)

      if chess.in_check(chess.current_player):

        raise ValueError("Cannot put yourself in check!")
        last_move = chess.b.h.pop()
        chess.current_player.unmove(last_move.from_square_code, last_move.to_square_code, last_move.piece_taken)

      else:

        chess.switch_players()
        chess.b.render()

    elif command in [ "debug", "d" ]:

      import pdb; pdb.set_trace()

      print("\nResuming game\n\n")

    else:
      print("Unrecognized command:", input_data)


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



