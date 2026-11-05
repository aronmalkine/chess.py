# notation.py
#
# Parses move text typed by a player into a (from_square, to_square) pair.
#
# Accepted forms (spaces are ignored):
#   e4, d5            pawn move
#   exd5              pawn capture (file of the capturing pawn is required)
#   Nf3, Bxc6, Qd1    piece move (K, Q, R, B, N), 'x' optional
#   Nbd7, R1e2, Qh4e1 disambiguation by file, rank, or both
#   e2e4, e2-e4, e2xd3 coordinate form (from-square then to-square)
# A trailing check/mate marker (+ or #) is allowed and ignored.

import re

PIECE_NAMES = {
  'K': 'king',
  'Q': 'queen',
  'R': 'rook',
  'B': 'bishop',
  'N': 'knight',
}

MOVE_PATTERN = re.compile(
  r'^(?P<piece>[KQRBN])?'
  r'(?P<from_file>[a-h])?'
  r'(?P<from_rank>[1-8])?'
  r'(?P<capture>[x:-])?'
  r'(?P<dest>[a-h][1-8])'
  r'[+#]?$'
)


def parse_move(text, board, player):
  """Return (from_code, to_code) for the move described by text.

  Raises ValueError if the text is not valid move notation, or if it matches
  no piece (or more than one piece) belonging to the player.

  Only piece movement rules are used to find the piece; leaving your own king
  in check is still rejected by the game when the move is made.
  """
  cleaned = re.sub(r'\s+', '', text)

  if re.match(r'^[O0](-[O0]){1,2}[+#]?$', cleaned):
    raise ValueError("Castling is not implemented.")
  if '=' in cleaned:
    raise ValueError("Pawn promotion is not implemented.")

  match = MOVE_PATTERN.match(cleaned)
  if match is None:
    raise ValueError("Unrecognized command or move: {}".format(text))

  piece_letter = match.group('piece')
  from_file = match.group('from_file')
  from_rank = match.group('from_rank')
  is_capture = match.group('capture') == 'x'
  dest = match.group('dest')

  # Coordinate form such as e2e4: the from-square is fully given.
  if piece_letter is None and from_file and from_rank:
    return from_file + from_rank, dest

  dest_square = board.at(dest)
  dest_xy = [dest_square._x, dest_square._y]

  if is_capture and dest_square.is_empty():
    raise ValueError("Illegal move: nothing to capture on {}.".format(dest))

  name = PIECE_NAMES[piece_letter] if piece_letter else 'pawn'

  if name == 'pawn' and is_capture and from_file is None:
    raise ValueError("Pawn captures need the pawn's file, ex: 'exd5'.")

  candidates = []
  for piece in board.find(player.color, name):
    code = piece.square.code()
    if from_file and code[0] != from_file:
      continue
    if from_rank and code[1] != from_rank:
      continue
    # A pawn that isn't capturing stays on its file.
    if name == 'pawn' and not is_capture and not from_file and code[0] != dest[0]:
      continue
    if dest_xy in piece.moves():
      candidates.append(piece)

  if not candidates:
    raise ValueError("Illegal move: no {} {} can move to {}.".format(player.color, name, dest))

  if len(candidates) > 1:
    options = ", ".join(sorted(p.square.code() for p in candidates))
    raise ValueError("Ambiguous move: {} can come from {}. Add the file or rank, ex: 'N{}{}'.".format(
      name, options, sorted(p.square.code() for p in candidates)[0][0], dest))

  return candidates[0].square.code(), dest
