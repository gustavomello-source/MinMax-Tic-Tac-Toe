from enum import StrEnum


class PlayerMark(StrEnum):
    """
    Enumeration for player marks in Tic Tac Toe. Each player can be represented by either 'X' or 'O'.
    """

    X = "X"
    O = "O"  # noqa: E741

    @property
    def opponent(self) -> "PlayerMark":
        """Return the opposing player mark."""
        if self == PlayerMark.X:
            return PlayerMark.O

        return PlayerMark.X
