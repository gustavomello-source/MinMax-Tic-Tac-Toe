"""Title-formatting abstraction for Tic Tac Toe interfaces."""

from typing import Protocol

from tictactoe.game.game import TicTacToeGame


class TitleFormatter(Protocol):
    """Define an object that formats a title for a game state."""

    def format(self, game: TicTacToeGame) -> str:
        """Return a title describing the supplied game."""
        ...
