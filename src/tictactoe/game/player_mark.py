from enum import Enum


class PlayerMark(str, Enum):
    """
    Enumeration for player marks in Tic Tac Toe. Each player can be represented by either 'X' or 'O'.
    """

    X = "X"
    O = "O"
