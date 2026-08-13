from tictactoe.game.game import TicTacToeGame
from tictactoe.ui.board_layout import BoardLayout
from tictactoe.ui.pygame import PyGameBoard


def test_pygame_board_uses_supplied_game() -> None:
    """The Pygame board should render the supplied game instance."""
    game = TicTacToeGame()

    pygame_board = PyGameBoard(game=game)

    assert pygame_board.game is game


def test_pygame_board_uses_supplied_layout() -> None:
    """The Pygame board should use the supplied coordinate layout."""
    board_layout = BoardLayout(width=300, height=300)

    pygame_board = PyGameBoard(board_layout=board_layout)

    assert pygame_board.board_layout is board_layout
