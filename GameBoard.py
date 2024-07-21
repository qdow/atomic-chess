"""
Filename: GameBoard.py
Author:
Date updated: 2024-07-09
Description: Contains GameBoard class with methods for playing the "atomic" variety of chess. Uses GamePiece.py.
"""
from GamePiece import *


class GameBoard:
    """
    A class for playing the atomic chess variation.
    Uses GamePieces child classes to play the game.
    After creating a ChessVar object, play the game by
    making moves with the make_moves method.
    The current board can be printed at any time with print_board.
    Get the game state and current player turn with get_game_state
    and player_turn methods.
    """
    def __init__(self):
        self._board = self.initialize_board()
        self._game_state = "UNFINISHED"
        self._player_turn = "WHITE"
        self._king_status = {"WHITE": True,
                             "BLACK": True}

    def initialize_board(self):
        """
        Creates a brand new default chess board as a list of lists
        representing rows and columns
        Each GamePiece type piece is put in their correct default
        spot as the value of the list at its row and column.
        """
        build = [[None for _ in range(8)] for _ in range(8)]

        # black pieces
        build[0][0] = Rook("BLACK")
        build[0][1] = Knight("BLACK")
        build[0][2] = Bishop("BLACK")
        build[0][3] = Queen("BLACK")
        build[0][4] = King("BLACK")
        build[0][5] = Bishop("BLACK")
        build[0][6] = Knight("BLACK")
        build[0][7] = Rook("BLACK")
        for index in range(8):
            build[1][index] = Pawn("BLACK")

        # white pieces
        build[7][0] = Rook("WHITE")
        build[7][1] = Knight("WHITE")
        build[7][2] = Bishop("WHITE")
        build[7][3] = Queen("WHITE")
        build[7][4] = King("WHITE")
        build[7][5] = Bishop("WHITE")
        build[7][6] = Knight("WHITE")
        build[7][7] = Rook("WHITE")
        for index in range(8):
            build[6][index] = Pawn("WHITE")

        return build

    def get_game_state(self):
        """Gets the game's current state ('UNFINISHED', 'WHITE_WON', 'BLACK_WON')"""
        return self._game_state

    def notation_to_board_pos(self, chess_notation):
        """
        Turns algebraic notation board position into row and column numbers.
        Called by make_move.
        The board's indices start at 0, so the row and column numbers range from 0-7
            instead of 1-8 like algebraic notation.
            Algebraic notation numbers the rows starting from the bottom, but the board
            numbers start at the top, so the returned row value will be the opposite of the
            original algebraic notation value.
        :param chess_notation: Algebraic notation symbol as a string representing a square on the board.
            Must be in correct format (columns labeled a-h and rows labeled 1-8, ex: c7)
        :return: A tuple with the converted board row number and column number.
            (Using the c7 example would return 1, 2)
            If invalid notation was given, returns -1, -1.
        """
        # invalid notation length
        if len(chess_notation) < 2 or len(chess_notation) > 2:
            return -1, -1
        # invalid row character type
        if not chess_notation[0].isalpha():
            return -1, -1
        # invalid column character type
        if not chess_notation[1].isnumeric():
            return -1, -1
        # invalid row number
        if int(chess_notation[1]) < 0 or int(chess_notation[1]) > 8:
            return -1, -1

        # notation goes top down from 8-1, board goes from 0-7 so we must convert the row number
        row = abs(int(chess_notation[1]) - 8)

        # to convert the notation's letter to a number, create a dictionary
        letter_to_num = {}
        letter_code = 97    # start at ASCII code for "a"
        for num in range(8):
            letter_to_num[chr(letter_code)] = num
            letter_code += 1

        # now to change column letter to number
        col = chess_notation[0].lower()
        if col not in letter_to_num:
            return -1, -1
        col = letter_to_num[col]

        return row, col

    def make_move(self, sq_from, sq_to):
        """
        Moves a piece on a specified square to a different square.
        If the move is valid, the board is updated.
        If the move captures a piece, any pieces caught in the resulting explosion
        are removed from the board.
        If a king is destroyed, the game_state is set to indicate the winner.
        This method collaborates with the following methods:
            - notation_to_board_pos: turn algebraic notation to board row/col number
            - valid_move: Checks if a move can be made
            - GamePiece.is_valid_move: Piece-specific move validation
            - is_capture: Determine if a move is a capture
            - update_board: Updates the board and game info using the following methods:
            - explosion: Explodes board on capture
            - update_turn: Updates player_turn
            - update_win: Updates game_state
            - move_piece: Moves piece from one place on the board to another
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :return: True if the move was made, False if it was not
        """
        if self._game_state != "UNFINISHED":
            return False

        # convert the notation
        sq_from = self.notation_to_board_pos(sq_from)
        sq_to = self.notation_to_board_pos(sq_to)

        # early validity checks
        if sq_from == (-1, -1) or sq_to == (-1, -1):    # invalid square input
            return False
        if self._board[sq_from[0]][sq_from[1]] is None:  # empty square
            return False
        if sq_from == sq_to:    # going nowhere
            return False

        piece = self._board[sq_from[0]][sq_from[1]]
        if piece.get_color() != self._player_turn:  # wrong color piece
            return False

        # see if the move is valid
        if type(piece) is Knight:
            valid = piece.is_valid_move(sq_from, sq_to)
        else:
            valid = self.valid_move(sq_from, sq_to, piece)

        # now to check if move is a capture
        if valid == "PAWN_CAPTURE":
            return self.update_board(sq_from, sq_to, True)
        elif valid:
            capture = self.is_capture(sq_from, sq_to, piece)
        else:
            return False

        if capture == "KING" or capture == "WRONG_COLOR":
            return False

        return self.update_board(sq_from, sq_to, capture)

    def valid_move(self, sq_from, sq_to, piece):
        """
        Determines if a move is valid or not by taking the direction and distance
        of a move and asking the piece if it is allowed.
        Called by make_move.
        Calls move_direction, piece_move, and pawn capture methods, and the clear_path methods.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :param piece:   The piece that will be moved
        :return: True if the move can be made, False if it cannot.
                 Returns "PAWN_CAPTURE" if the move is a pawn capture.
        """
        direction = self.move_direction(sq_from, sq_to, piece)
        if direction is False:
            return False
        distance = abs(sq_from[0] - sq_to[0])
        # left or right the distance is in the columns
        if direction == "STRAIGHT" and sq_from[0] == sq_to[0]:
            distance = sq_from[1] - sq_to[1]

        piece_move_valid = self.piece_move(direction, distance, piece)
        if piece_move_valid == "PAWN_CAPTURE":
            is_capture = self.pawn_capture(sq_from, sq_to, piece.get_color())
            if is_capture:
                return "PAWN_CAPTURE"
            else:
                return False
        elif piece_move_valid:
            if (type(piece) is Queen or type(piece) is King) and direction == "STRAIGHT":
                return self.clear_path_straight(sq_from, sq_to)
            elif (type(piece) is Queen or type(piece) is King) and direction == "DIAGONAL":
                return self.clear_path_diagonal(sq_from, sq_to)
            elif type(piece) is Rook:
                return self.clear_path_straight(sq_from, sq_to)
            elif type(piece) is Bishop:
                return self.clear_path_diagonal(sq_from, sq_to)
            elif type(piece) is Pawn:
                return self.clear_path_pawn(sq_from, sq_to)
        else:
            return False

    def move_direction(self, sq_from, sq_to, piece):
        """
        Determines in which direction a move is heading.
        Called by valid_move.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :param piece:   The piece that will be moved
        :return: Returns "w_FORWARD" or "b_FORWARD" for forward pawn movement.
                    ("w_FORWARD" for white, "b_FORWARD" for black)
                 Returns "STRAIGHT" for any other straight movement.
                 Returns "w_DIAGONAL" or "b_DIAGONAL" for diagonal pawn movement.
                 Returns "DIAGONAL" for any other diagonal movement.
                 Returns False otherwise.
        """
        if sq_from[0] == sq_to[0] or sq_from[1] == sq_to[1]:  # if rows or columns are the same
            if sq_from[0] - sq_to[0] > 0 and type(piece) is Pawn:
                return "w_FORWARD"
            elif sq_from[0] - sq_to[0] < 0 and type(piece) is Pawn:
                return "b_FORWARD"
            else:
                return "STRAIGHT"
        elif abs(sq_from[0] - sq_to[0]) == abs(sq_from[1] - sq_to[1]):  # if distance to row and column are the same
            if sq_from[0] - 1 == sq_to[0] and sq_from[1] - 1 == sq_to[1] and type(piece) is Pawn:
                return "w_DIAGONAL"
            elif sq_from[0] - 1 == sq_to[0] and sq_from[1] + 1 == sq_to[1] and type(piece) is Pawn:
                return "w_DIAGONAL"
            elif sq_from[0] + 1 == sq_to[0] and sq_from[1] - 1 == sq_to[1] and type(piece) is Pawn:
                return "b_DIAGONAL"
            elif sq_from[0] + 1 == sq_to[0] and sq_from[1] + 1 == sq_to[1] and type(piece) is Pawn:
                return "b_DIAGONAL"
            else:
                return "DIAGONAL"
        else:
            return False

    def piece_move(self, direction, distance, piece):
        """
        Checks if a move is valid for a piece based on its distance and direction.
        Called by valid_move.
        Calls Pawn's is_valid_move method.
        :param direction: Direction of the move
        :param distance: Distance to be moved
        :param piece: Piece being moved
        :return: True if move is possible, False otherwise
        """
        if type(piece) is Queen:
            return True
        elif type(piece) is King:
            if distance == 1:
                return True
        elif type(piece) is Rook:
            if direction == "STRAIGHT":
                return True
        elif type(piece) is Bishop:
            if direction == "DIAGONAL":
                return True
        elif type(piece) is Pawn:
            return piece.is_valid_move(direction, distance)
        else:
            return False
        # Knights were taken care of in make_move

    def clear_path_straight(self, sq_from, sq_to):
        """
        Determines if there is a piece in the way of the straight move being made
        Called by valid_move.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :return: True if the move can be made, False if a piece is in the way
        """
        from_row = sq_from[0]
        from_col = sq_from[1]
        to_row = sq_to[0]
        to_col = sq_to[1]

        if from_row - to_row > 0:    # up
            for row in range(to_row+1, from_row):   # add one to to_row to skip current piece
                if self._board[row][from_col] is not None:
                    return False
            return True
        elif from_row - to_row < 0:  # down
            for row in range(from_row+1, to_row):
                if self._board[row][from_col] is not None:
                    return False
            return True
        elif from_col - to_col > 0:    # left
            for col in range(to_col+1, from_col):
                if self._board[from_row][col] is not None:
                    return False
            return True
        elif from_col - to_col < 0:  # right
            for col in range(from_col+1, to_col):
                if self._board[from_row][col] is not None:
                    return False
            return True
        return False

    def clear_path_diagonal(self, sq_from, sq_to):
        """
        Determines if there is a piece in the way of the diagonal move being made
        Called by valid_move.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :return: True if the move can be made, False if a piece is in the way
        """
        from_row = sq_from[0]
        from_col = sq_from[1]
        to_row = sq_to[0]
        to_col = sq_to[1]

        row_direction = from_row - to_row
        col_direction = from_col - to_col
        distance = abs(from_row - to_row)

        if row_direction > 0 and col_direction > 0:  # up left
            for shift in range(1, distance):   # row and col shift down by same amount
                if self._board[from_row - shift][from_col - shift] is not None:
                    return False
            return True
        elif row_direction > 0 and col_direction < 0:  # up right
            for shift in range(1, distance):
                if self._board[from_row - shift][from_col + shift] is not None:
                    return False
            return True
        elif row_direction < 0 and col_direction > 0:  # down left
            for shift in range(1, distance):
                if self._board[from_row + shift][from_col - shift] is not None:
                    return False
            return True
        elif row_direction < 0 and col_direction < 0:  # down right
            for shift in range(1, distance):
                if self._board[from_row + shift][from_col + shift] is not None:
                    return False
            return True
        else:
            return False

    def clear_path_pawn(self, sq_from, sq_to):
        """
        Determines if there is a piece in the way of a Pawn's move
        Called by valid_move.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :return: True if the move can be made, False if a piece is in the way
        """
        from_row = sq_from[0]
        from_col = sq_from[1]
        to_row = sq_to[0]

        if from_row - to_row > 0:  # up
            for row in range(to_row, from_row):  # different range because pawns don't capture going straight
                if self._board[row][from_col] is not None:
                    return False
            return True
        elif from_row - to_row < 0:  # down
            for row in range(from_row+1, to_row+1):
                if self._board[row][from_col] is not None:
                    return False
            return True

    def pawn_capture(self, sq_from, sq_to, color):
        """
        Determines if a pawn capture is valid or not
        Called by valid_move.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :param color:   Color of the piece being moved
        :return: True if the move is a capture, False if not
        """
        from_row = sq_from[0]
        from_col = sq_from[1]
        to_row = sq_to[0]
        to_col = sq_to[1]
        row_direction = from_row - to_row
        col_direction = from_col - to_col

        if row_direction > 0 and col_direction > 0:  # up left
            if self._board[from_row-1][from_col-1] is not None:
                capture = True
            else:
                capture = False
        elif row_direction > 0 and col_direction < 0:  # up right
            if self._board[from_row-1][from_col+1] is not None:
                capture = True
            else:
                capture = False
        elif row_direction < 0 and col_direction > 0:  # down left
            if self._board[from_row+1][from_col-1] is not None:
                capture = True
            else:
                capture = False
        elif row_direction < 0 and col_direction < 0:  # down right
            if self._board[from_row+1][from_col+1] is not None:
                capture = True
            else:
                capture = False
        else:
            capture = False

        if capture:
            target_square = self._board[sq_to[0]][sq_to[1]]
            # can only capture opponent's piece
            if color == target_square.get_color():
                return False
            else:
                return True
        else:
            return False

    def is_capture(self, sq_from, sq_to, piece):
        """
        Determines whether a move will capture a piece or just move squares.
        Called by make_move.
        :param sq_from: The square containing the piece to move
        :param sq_to:  The square to move the piece to
        :param piece:  Piece doing the capture
        :return: True if a capture will be made, False otherwise
                 Returns "KING" if capture would be made by a King.
                 Returns "WRONG_COLOR" if trying to capture player's own piece.
        """
        row = sq_to[0]
        col = sq_to[1]
        target_square = self._board[row][col]

        # can only capture opponent's piece
        if target_square is not None and piece.get_color() == target_square.get_color():
            return "WRONG_COLOR"

        if target_square is not None:
            if type(piece) is King: # kings are not allowed to capture
                return "KING"
            return True
        else:
            return False

    def update_board(self, sq_from, sq_to, capture):
        """
        Updates the board and game info.
        Called by make_move.
        Calls update_turn, explosion, update_win, and move_piece
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :param capture: True if move is a capture, False if not
        :return:
        """
        self.update_turn()
        if capture:
            explode = self.explosion(sq_to)
            if explode is False:
                return False
            self._board[sq_from[0]][sq_from[1]] = None
            self.update_win()
            return True
        else:
            self.move_piece(sq_from, sq_to)
            return True

    def update_turn(self):
        """
        Updates game player_turn info.
        Called by update_board.
        """
        if self._player_turn == "WHITE":
            self._player_turn = "BLACK"
        else:
            self._player_turn = "WHITE"

    def explosion(self, sq_to):
        """
        When a piece captures another piece, all pieces on the adjacent
        eight squares must be taken off the board (including the piece
        that did the capture)
        Called by update_board.
        :param sq_to: Explosion site square
        """
        row = sq_to[0] - 1   # start at the upper left square
        col = sq_to[1] - 1   # of the 3x3 explosion spot

        # explosion can't happen until it's known that it won't destroy both kings,
        # so store the coordinates of the squares to be exploded in a list
        # to be exploded once king safety is determined
        explode_list = []

        for row_offset in range(3):
            for col_offset in range(3):
                if row+row_offset < 0 or row+row_offset > 7 or col+col_offset < 0 or col+col_offset > 7:
                    continue    # skip when running over the edge of the board
                if self._board[row+row_offset][col+col_offset] is not None:
                    if type(self._board[row+row_offset][col+col_offset]) is King:
                        if self._board[row+row_offset][col+col_offset].get_color() == "WHITE":
                            self._king_status["WHITE"] = False
                        else:
                            self._king_status["BLACK"] = False
                    explode_list.append((row+row_offset, col+col_offset))
        if self._king_status["WHITE"] is False and self._king_status["BLACK"] is False:
            return False    # both kings would be exploded, so move cannot be made

        else:  # safe to explode all squares
            captured_square = self._board[sq_to[0]][sq_to[1]]
            if type(captured_square) is Pawn:   # explode captured pawn
                self._board[sq_to[0]][sq_to[1]] = None
            for item in explode_list:
                row = item[0]
                col = item[1]
                if type(self._board[row][col]) is Pawn:  # other pawns don't explode
                    continue
                else:
                    self._board[row][col] = None
            return True

    def update_win(self):
        """Checks the status of the Kings and updates game_state if necessary"""
        if self._king_status["WHITE"] is False:
            self._game_state = "BLACK_WON"
        elif self._king_status["BLACK"] is False:
            self._game_state = "WHITE_WON"

    def move_piece(self, sq_from, sq_to):
        """
        Moves the piece on the board from one square to another.
        Called by update_board.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        """
        from_row = sq_from[0]
        from_col = sq_from[1]
        to_row = sq_to[0]
        to_col = sq_to[1]
        self._board[to_row][to_col] = self._board[from_row][from_col]
        self._board[from_row][from_col] = None

    def print_board(self):
        """
        Prints out the current state of the board.
        Pieces are represented with unicode characters.
        """
        print("    a   b   c   d   e   f   g   h")
        for row in range(8):
            line = str(abs(row - 8)) + " "  # adds row number
            for col in range(8):
                piece = self._board[row][col]
                if piece is not None and piece.get_color() == "BLACK":
                    if type(piece) is King:
                        square = " ♚ "
                    elif type(piece) is Queen:
                        square = " ♛ "
                    elif type(piece) is Rook:
                        square = " ♜ "
                    elif type(piece) is Bishop:
                        square = " ♝ "
                    elif type(piece) is Knight:
                        square = " ♞ "
                    elif type(piece) is Pawn:
                        square = " ♟︎ "
                elif piece is not None and piece.get_color() == "WHITE":
                    if type(piece) is King:
                        square = " ♔ "
                    elif type(piece) is Queen:
                        square = " ♕ "
                    elif type(piece) is Rook:
                        square = " ♖ "
                    elif type(piece) is Bishop:
                        square = " ♗ "
                    elif type(piece) is Knight:
                        square = " ♘ "
                    elif type(piece) is Pawn:
                        square = " ♙ "
                else:
                    square = "   "
                if row % 2 == 0 and col % 2 == 0:
                    line += "|" + square
                elif row % 2 == 1 and col % 2 == 1:
                    line += "|" + square
                else:
                    line += "|" + square
            line += "| " + str(abs(row - 8))
            print(line)
            print("  —————————————————————————————————")
        print("    a   b   c   d   e   f   g   h")


    def play_game(self):
        """
        Prints out the board and prompts players to input their desired moves
        so game can be played via user input instead of calling the make_move
        method multiple times manually.
        """
        end = False
        self.print_board()
        while not end:
            print(f"{self._player_turn}'s turn")
            sq_from = input("From: ")
            sq_to = input("To: ")
            self.make_move(sq_from, sq_to)
            print()
            self.print_board()
            if self._game_state != "UNFINISHED":
                print("Game over! Result:", self._game_state)
                end = True


    def rapture_pawns(self, color=None):
        """
        Removes all pawns from the board.
        (A method just for fun during testing.)
        :param color: Optional parameter to specify which color pawns to remove.
        """
        if color == "b":
            for row_index, row in enumerate(self._board):
                for col_index, item in enumerate(row):
                    if type(item) is Pawn and item.get_color() == "BLACK":
                        self._board[row_index][col_index] = None
        elif color == "w":
            for row_index, row in enumerate(self._board):
                for col_index, item in enumerate(row):
                    if type(item) is Pawn and item.get_color() == "WHITE":
                        self._board[row_index][col_index] = None
        else:
            for row_index, row in enumerate(self._board):
                for col_index, item in enumerate(row):
                    if type(item) is Pawn:
                        self._board[row_index][col_index] = None
