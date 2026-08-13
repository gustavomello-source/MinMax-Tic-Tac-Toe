from tictactoe.game.game import TicTacToeGame
from tictactoe.ui.game_title_formatter import GameTitleFormatter


def test_formatter_shows_current_player() -> None:
    """An active game title should identify the current player."""
    formatter = GameTitleFormatter(base_title="Tic Tac Toe")

    title = formatter.format(TicTacToeGame())

    assert title == "Tic Tac Toe - X's turn"
