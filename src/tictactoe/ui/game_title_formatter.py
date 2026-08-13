"""Window title formatting for Tic Tac Toe game states."""

from dataclasses import dataclass

from tictactoe.game.game import TicTacToeGame
from tictactoe.game.game_status import GameStatus


@dataclass(frozen=True)
class GameTitleFormatter:
    """Format a window title from the current game state."""

    base_title: str

    def format(self, game: TicTacToeGame) -> str:
        """Return a title describing the supplied game state."""
        if game.status == GameStatus.WON:
            winner = game.winner
            assert winner is not None
            return f"{self.base_title} - {winner.value} wins"

        if game.status == GameStatus.DRAW:
            return f"{self.base_title} - Draw"

        return f"{self.base_title} - {game.current_player.value}'s turn"
