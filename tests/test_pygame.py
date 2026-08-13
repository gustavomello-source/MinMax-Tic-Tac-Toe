from tictactoe.game.game import TicTacToeGame
from tictactoe.ui.pygame import PyGameBoard


def test_pygame_board_uses_supplied_game() -> None:
    """The Pygame board should render the supplied game instance."""
    game = TicTacToeGame()

    pygame_board = PyGameBoard(game=game)

    assert pygame_board.game is game
