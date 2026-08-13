"""Status values for a Tic Tac Toe game."""

from enum import Enum, auto


class GameStatus(Enum):
    """Represent the current lifecycle state of a game."""

    IN_PROGRESS = auto()
    WON = auto()
    DRAW = auto()
