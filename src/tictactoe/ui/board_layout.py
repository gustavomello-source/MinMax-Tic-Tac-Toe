"""Screen layout calculations for the Tic Tac Toe board."""

from dataclasses import dataclass

from ..game.board import BOARD_SIZE


@dataclass(frozen=True)
class BoardLayout:
    """Translate screen coordinates into board positions."""

    width: int
    height: int

    def get_board_position(self, x: int, y: int) -> tuple[int, int] | None:
        """Return the board row and column at the screen coordinates."""
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return None

        cell_width = self.width // BOARD_SIZE
        cell_height = self.height // BOARD_SIZE
        row = y // cell_height
        column = x // cell_width

        if row >= BOARD_SIZE or column >= BOARD_SIZE:
            return None

        return row, column
