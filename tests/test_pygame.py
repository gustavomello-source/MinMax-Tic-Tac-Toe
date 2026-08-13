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


def test_window_title_shows_current_player() -> None:
    """The window title should identify whose turn it is."""
    game = TicTacToeGame()
    pygame_board = PyGameBoard(game=game)
    pygame.init()

    pygame_board._update_window_title()

    window_title, _ = pygame.display.get_caption()
    pygame.quit()
    assert window_title == "MinMax Tic Tac Toe - X's turn"


def test_window_title_shows_winner() -> None:
    """The window title should identify the winner."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    game.play_move(row=1, column=0)
    game.play_move(row=0, column=1)
    game.play_move(row=1, column=1)
    game.play_move(row=0, column=2)
    pygame_board = PyGameBoard(game=game)
    pygame.init()

    pygame_board._update_window_title()

    window_title, _ = pygame.display.get_caption()
    pygame.quit()
    assert window_title == "MinMax Tic Tac Toe - X wins"
