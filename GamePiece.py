"""
Filename: GamePiece.py
Author:
Date updated: 2024-07-09
Description: Contains GamePiece class which has subclasses for each type of chess piece
"""


class GamePiece:
    """
    Represents a chess piece and its color (black or white).
    Each type of piece is represented by a child class King, Queen, Rook, Bishop, Knight, and Pawn.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        self._color = color

    def get_color(self):
        """Gets the piece's color (black or white)"""
        return self._color


class King(GamePiece):
    """
    Represents a king chess piece. Inherits from the GamePiece class.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        super().__init__(color)


class Queen(GamePiece):
    """
    Represents a queen chess piece. Inherits from the GamePiece class.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        super().__init__(color)


class Rook(GamePiece):
    """
    Represents a rook chess piece. Inherits from the GamePiece class.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        super().__init__(color)


class Bishop(GamePiece):
    """
    Represents a bishop chess piece. Inherits from the GamePiece class.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        super().__init__(color)


class Knight(GamePiece):
    """
    Represents a knight chess piece. Inherits from the GamePiece class.
    Has method is_valid_move to handle Knight's unique movement.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, sq_from, sq_to):
        """
        Determines if proposed move is valid for Knight's special movement.
        :param sq_from: The square containing the piece to move
        :param sq_to:   The square to move the piece to
        :return: True if the move is valid, False if it is not
        """
        # distance between rows and distance between columns
        #   Knights first move two squares up, down, left, or right,
        #   then one square in the perpendicular direction, therefore
        #   row distance needs to be 2 AND col distance needs to be 1
        #   OR col distance needs to be 2 AND row distance needs to be 1
        row_distance = abs(sq_from[0] - sq_to[0])
        col_distance = abs(sq_from[1] - sq_to[1])
        if row_distance == 2 and col_distance == 1:
            return True
        elif row_distance == 1 and col_distance == 2:
            return True
        else:
            return False


class Pawn(GamePiece):
    """
    Represents a pawn chess piece. Inherits from the GamePiece class.
    Has extra private data member "is_first_turn" to help in determining
    what type of movement is valid.
    Has method is_valid_move to handle Pawn's various movement scenarios.
    Used in the ChessVar class.
    """
    def __init__(self, color):
        super().__init__(color)
        self._is_first_turn = True

    def is_valid_move(self, direction, distance):
        """
        Takes the direction and distance of a proposed move and determines
        if it is a valid move the piece can do
        :param direction: Direction the move would take the piece
        :param distance: How many squares the move would take the piece
        :return: True if the move is valid, False if it is not.
                 Returns "PAWN_CAPTURE" if the move is a potential pawn capture.
        """
        if direction == "b_DIAGONAL" and self._color == "BLACK" and distance == 1:
            return "PAWN_CAPTURE"
        elif direction == "w_DIAGONAL" and self._color == "WHITE" and distance == 1:
            return "PAWN_CAPTURE"

        if direction != "b_FORWARD" and direction != "w_FORWARD":
            return False

        black_valid = self._color == "BLACK" and direction == "b_FORWARD"
        white_valid = self._color == "WHITE" and direction == "w_FORWARD"

        if black_valid or white_valid:
            if distance == 2 and self._is_first_turn:   # on first turn, pawns can move 2
                self._is_first_turn = False
                return True
            elif distance == 1:
                return True
        return False
