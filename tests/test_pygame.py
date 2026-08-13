import pygame

from tictactoe.game.game import TicTacToeGame
from tictactoe.game.player_mark import PlayerMark
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


def test_mouse_position_plays_move_in_mapped_cell() -> None:
    """A mouse position should play a move in its mapped board cell."""
    game = TicTacToeGame()
    pygame_board = PyGameBoard(game=game)

    pygame_board._play_move_at(mouse_position=(250, 450))

    assert game.board.get_current_state()[2][1] is not None


def test_r_key_resets_game() -> None:
    """Pressing R should start a new game."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    pygame_board = PyGameBoard(game=game)
    pygame.init()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    pygame_board._handle_events()

    pygame.quit()
    assert game.board.get_current_state()[0][0] is None
    assert game.current_player == PlayerMark.X
