import pygame
import pytest

from tictactoe.game.game import TicTacToeGame
from tictactoe.game.player_mark import PlayerMark
from tictactoe.ui.board_layout import BoardLayout
from tictactoe.ui.board_renderer import PygameBoardRenderer
from tictactoe.ui.game_title_formatter import GameTitleFormatter
from tictactoe.ui.pygame import PygameApp


class FixedMoveSelector:
    """Select a fixed move for Pygame application tests."""

    def get_best_move(self, _board: object) -> tuple[int, int]:
        """Return a fixed board position."""
        return 0, 0


def test_pygame_board_uses_supplied_game() -> None:
    """The Pygame board should render the supplied game instance."""
    game = TicTacToeGame()

    pygame_board = PygameApp(game=game)

    assert pygame_board.game is game


def test_pygame_board_uses_supplied_layout() -> None:
    """The Pygame board should use the supplied coordinate layout."""
    board_layout = BoardLayout(width=300, height=300)

    pygame_board = PygameApp(board_layout=board_layout)

    assert pygame_board.board_layout is board_layout


def test_pygame_app_uses_supplied_board_renderer() -> None:
    """The Pygame app should retain its configured board renderer."""
    board_layout = BoardLayout(width=300, height=300)
    board_renderer = PygameBoardRenderer(board_layout)

    pygame_app = PygameApp(
        board_layout=board_layout,
        board_renderer=board_renderer,
    )

    assert pygame_app.board_renderer is board_renderer


def test_pygame_app_uses_supplied_renderer_layout() -> None:
    """An injected renderer should provide the application board layout."""
    board_renderer = PygameBoardRenderer(BoardLayout(width=300, height=300))

    pygame_app = PygameApp(board_renderer=board_renderer)

    assert pygame_app.board_layout is board_renderer.board_layout


def test_pygame_app_rejects_conflicting_renderer_layout() -> None:
    """The renderer and application should not use different layouts."""
    board_renderer = PygameBoardRenderer(BoardLayout(width=300, height=300))

    with pytest.raises(ValueError):
        PygameApp(
            board_layout=BoardLayout(width=600, height=600),
            board_renderer=board_renderer,
        )


def test_pygame_app_uses_supplied_opponent_move_selector() -> None:
    """The Pygame app should retain its configured opponent selector."""
    move_selector = FixedMoveSelector()

    pygame_app = PygameApp(opponent_move_selector=move_selector)

    assert pygame_app.opponent_move_selector is move_selector


def test_pygame_app_uses_supplied_human_player() -> None:
    """The Pygame app should retain the configured human player."""
    pygame_app = PygameApp(human_player=PlayerMark.O)

    assert pygame_app.human_player == PlayerMark.O


def test_pygame_app_uses_supplied_title_formatter() -> None:
    """The Pygame app should retain its configured title formatter."""
    title_formatter = GameTitleFormatter(base_title="Custom Game")

    pygame_app = PygameApp(title_formatter=title_formatter)

    assert pygame_app.title_formatter is title_formatter


def test_valid_click_plays_opponent_selected_move() -> None:
    """A valid human move should be followed by the selected opponent move."""
    game = TicTacToeGame()
    pygame_app = PygameApp(
        game=game,
        opponent_move_selector=FixedMoveSelector(),
    )

    pygame_app._play_move_at(mouse_position=(250, 250))

    assert game.board.get_current_state()[1][1] == PlayerMark.X
    assert game.board.get_current_state()[0][0] == PlayerMark.O


def test_click_is_ignored_outside_human_turn() -> None:
    """Mouse input should not place a mark during the opponent's turn."""
    game = TicTacToeGame(starting_player=PlayerMark.O)
    pygame_app = PygameApp(game=game, human_player=PlayerMark.X)

    pygame_app._play_move_at(mouse_position=(250, 250))

    assert game.board.get_current_state()[1][1] is None


def test_opponent_plays_opening_move_when_human_is_second() -> None:
    """The opponent should play first when the human controls O."""
    game = TicTacToeGame()
    pygame_app = PygameApp(
        game=game,
        opponent_move_selector=FixedMoveSelector(),
        human_player=PlayerMark.O,
    )

    pygame_app._play_opponent_turn()

    assert game.board.get_current_state()[0][0] == PlayerMark.X
    assert game.current_player == PlayerMark.O


def test_reset_replays_opponent_opening_move() -> None:
    """Reset should restore the opponent opening move for a human O player."""
    game = TicTacToeGame()
    pygame_app = PygameApp(
        game=game,
        opponent_move_selector=FixedMoveSelector(),
        human_player=PlayerMark.O,
    )
    game.play_move(row=1, column=1)
    pygame.init()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    pygame_app._handle_events()

    pygame.quit()
    assert game.board.get_current_state()[0][0] == PlayerMark.X
    assert game.board.get_current_state()[1][1] is None
    assert game.current_player == PlayerMark.O


def test_mouse_position_plays_move_in_mapped_cell() -> None:
    """A mouse position should play a move in its mapped board cell."""
    game = TicTacToeGame()
    pygame_board = PygameApp(game=game)

    pygame_board._play_move_at(mouse_position=(250, 450))

    assert game.board.get_current_state()[2][1] is not None


def test_r_key_resets_game() -> None:
    """Pressing R should start a new game."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    pygame_board = PygameApp(game=game)
    pygame.init()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))

    pygame_board._handle_events()

    pygame.quit()
    assert game.board.get_current_state()[0][0] is None
    assert game.current_player == PlayerMark.X


def test_window_title_shows_current_player() -> None:
    """The window title should identify whose turn it is."""
    game = TicTacToeGame()
    pygame_app = PygameApp(game=game)

    window_title = pygame_app._get_window_title()

    assert window_title == "MinMax Tic Tac Toe - X's turn"
