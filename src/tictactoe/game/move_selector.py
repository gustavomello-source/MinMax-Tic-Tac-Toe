"""Move-selection abstraction for Tic Tac Toe players."""

from typing import Protocol

from tictactoe.game.board import Board, BoardPosition


class MoveSelector(Protocol):
    """Define an object that selects a move for a board state."""

    def get_best_move(self, board: Board) -> BoardPosition | None:
        """Return a selected board position, or no move when unavailable."""
        ...
