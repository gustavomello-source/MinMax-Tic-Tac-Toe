"""Screen layout calculations for the Tic Tac Toe board."""

from dataclasses import dataclass

from tictactoe.game.board import BOARD_SIZE, BoardPosition


@dataclass(frozen=True)
class BoardLayout:
    """Translate screen coordinates into board positions."""

    width: int
    height: int

    def __post_init__(self) -> None:
        """Reject dimensions that cannot contain every board cell."""
        if self.width < BOARD_SIZE or self.height < BOARD_SIZE:
            message = "Board layout dimensions must be at least the board size"
            raise ValueError(message)

        if self.width % BOARD_SIZE != 0 or self.height % BOARD_SIZE != 0:
            message = "Board layout dimensions must be divisible by the board size"
            raise ValueError(message)

    @property
    def cell_width(self) -> int:
        """Return the width of one board cell."""
        return self.width // BOARD_SIZE

    @property
    def cell_height(self) -> int:
        """Return the height of one board cell."""
        return self.height // BOARD_SIZE

    def get_board_position(self, x: int, y: int) -> BoardPosition | None:
        """Return the board row and column at the screen coordinates."""
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return None

        row = y // self.cell_height
        column = x // self.cell_width

        if row >= BOARD_SIZE or column >= BOARD_SIZE:
            return None

        return row, column
