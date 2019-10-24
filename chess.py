import sys
import traceback
import copy

import board
import history
import players
import pieces


class Chess(object):
  """Represents a game of chess.

  Instance variables:
  b -- the chess board
  white -- the white player object
  black -- the black player object
  current_player -- reference to next player to move

  Public methods:
  play -- start game and enter event loop
    Supported commands:
      exit/quit/q -- exit game
      undo/u -- undo last move
      history/h -- show history of game up until present
      score/s -- show scores
      board/b -- render the board
      moves -- list moves for black, white, or for an occupied square, ex: 'moves white' or 'moves c1'
      attacks -- list attacks for black, white, or for an occupied square, ex: 'attacks white' or 'attacks c1')
      move/m -- move from sqare to square, ex 'm d2 d4'
      debug/d -- enter debug mode (ipdb session)      

  opponent -- takes a player object and returns the other player object
  switch_players -- after a move, this method is called to update the current player
  in_check -- for a given player, determines if the player's king is under attack
  """

  b = None;
  white = None;
  black = None;
  current_player = None;

  def __init__(self, white_name, black_name):

    self.b = board.Board()

    self.white = players.Player(name=white_name, color='white', board=self.b)
    self.black = players.Player(name=black_name, color='black', board=self.b)

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
    king_square = self.b.find_first(player.color, 'king').square.code()
    attacks = self.opponent(player).attacks()
    for attack in attacks:
      # attacks include attacker piece ref and attacked piece ref [attacker, attacked]
      if king_square == attack[1].code():
        return True
    return False

  def play(self):

    # Show board
    self.b.render()

    while True: #(not self.in_check(self.current_player) or len(self.check_breaking_moves(self.current_player)) != 0):  

      # Prompt for command  
      input_data = input("\n{} to move: ".format(self.current_player.color))

      try:

        input_data = input_data.split(" ")

        command = input_data[0]

        if command in [ 'exit', 'quit', 'q']:
          # Handle exit
          print("\nHope you enjoyed the game! Play again soon!\n\n")
          sys.exit()

        elif command in [ 'undo', 'u']:
          # Handle undo
          last_move = self.b.h.pop()
          last_move.player.unmove(last_move.from_square_code, last_move.to_square_code, last_move.piece_taken)
          self.switch_players()
          self.b.render()

        elif command in [ 'history', 'h' ]:
          print(self.b.h)

        elif command in [ 'score', 's' ]:
          white_material, black_material, white_pieces, black_pieces = self.b.score()
          print("white: {material:>6}".format(material=white_material), ", ".join(white_pieces))
          print("black: {material:>6}".format(material=black_material), ", ".join(black_pieces))

        elif command in [ 'board', 'b']:
          self.b.render()

        elif command == 'moves':

          target = input_data[1]

          if len(target) == 2:

            moves = self.b.at(target).piece.moves()

            readable_moves = self.b.to_code(moves)

            print(", ".join(readable_moves))

          elif target in [ "white", "black" ]:

            print("ToDo")

        elif command == "attacks":

          target = input_data[1]

          if target in [ "white", "black" ]:

            for a in self.b.attacks(target):
              print(a[0], "takes", a[1])

          elif len(target) == 2:

            attacks = self.b.at(target).piece.attacks()

            readable_attacks = self.b.to_code(attacks)

            print(", ".join(readable_attacks))

          else:
            raise ValueError("attacks command expects 'white', 'black', or an occupied square, ex 'c1'")

        elif command in [ "move", "m" ]:

          move_from = input_data[1]
          move_to = input_data[2]

          from_check = self.in_check(self.current_player)

          self.current_player.move(move_from, move_to)

          if self.in_check(self.current_player) and from_check:

            last_move = self.b.h.pop()
            self.current_player.unmove(last_move.from_square_code, last_move.to_square_code, last_move.piece_taken)

            print("Illegal move: King remains in check!")

          elif self.in_check(self.current_player):

            last_move = self.b.h.pop()
            self.current_player.unmove(last_move.from_square_code, last_move.to_square_code, last_move.piece_taken)

            print("Illegal move: Cannot put yourself in check!")

          else:

            self.switch_players()
            self.b.render()

            if self.in_check(self.current_player):
              print("\n### CHECK! ###")

        elif command in [ "debug", "d" ]:

          import ipdb; ipdb.set_trace(context=5)

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


    print("CHECK MATE!! {} wins!".format(self.opponent(current_player).color))

    sys.exit()

# Create game
game = Chess('Aron', 'Mous')

game.play()




