from tictactoe.game.game import TicTacToeGame
from tictactoe.ui.game_title_formatter import GameTitleFormatter


def test_formatter_shows_current_player() -> None:
    """An active game title should identify the current player."""
    formatter = GameTitleFormatter(base_title="Tic Tac Toe")

    title = formatter.format(TicTacToeGame())

    assert title == "Tic Tac Toe - X's turn"


def test_formatter_shows_winner() -> None:
    """A won game title should identify the winning player."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    game.play_move(row=1, column=0)
    game.play_move(row=0, column=1)
    game.play_move(row=1, column=1)
    game.play_move(row=0, column=2)
    formatter = GameTitleFormatter(base_title="Tic Tac Toe")

    title = formatter.format(game)

    assert title == "Tic Tac Toe - X wins"


def test_formatter_shows_draw() -> None:
    """A drawn game title should identify the draw."""
    game = TicTacToeGame()
    moves = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
        (2, 2),
    ]
    for row, column in moves:
        game.play_move(row, column)
    formatter = GameTitleFormatter(base_title="Tic Tac Toe")

    title = formatter.format(game)

    assert title == "Tic Tac Toe - Draw"
