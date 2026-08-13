"""Pygame user interface for Tic Tac Toe."""

import pygame

from tictactoe.game.game import TicTacToeGame
from tictactoe.game.move_selector import MoveSelector
from tictactoe.game.player_mark import PlayerMark
from tictactoe.ui.board_layout import BoardLayout
from tictactoe.ui.board_renderer import PygameBoardRenderer
from tictactoe.ui.board_renderer_protocol import BoardRenderer
from tictactoe.ui.game_title_formatter import GameTitleFormatter

WINDOW_SIZE = 600
WINDOW_TITLE = "MinMax Tic Tac Toe"
FRAMES_PER_SECOND = 60

class PygameApp:
    """Manage the Pygame application lifecycle and user interface."""

    def __init__(
        self,
        game: TicTacToeGame | None = None,
        board_layout: BoardLayout | None = None,
        board_renderer: BoardRenderer | None = None,
        title_formatter: GameTitleFormatter | None = None,
        opponent_move_selector: MoveSelector | None = None,
        human_player: PlayerMark = PlayerMark.X,
    ) -> None:
        """Create a Pygame board for the supplied or a new game."""
        self.game = game if game is not None else TicTacToeGame()
        self.opponent_move_selector = opponent_move_selector
        self.human_player = human_player
        if (
            board_renderer is not None
            and board_layout is not None
            and board_renderer.board_layout != board_layout
        ):
            message = "Board renderer and application must use the same layout"
            raise ValueError(message)

        self.board_layout = (
            board_layout
            or (board_renderer.board_layout if board_renderer is not None else None)
            or BoardLayout(width=WINDOW_SIZE, height=WINDOW_SIZE)
        )
        self.board_renderer = board_renderer or PygameBoardRenderer(self.board_layout)
        self.title_formatter = title_formatter or GameTitleFormatter(WINDOW_TITLE)
        self._screen: pygame.Surface | None = None
        self._clock: pygame.time.Clock | None = None
        self._running = False

    def run(self) -> None:
        """Open the window and run the application until it is closed."""
        pygame.init()

        try:
            window_dimensions = (
                self.board_layout.width,
                self.board_layout.height,
            )
            self._screen = pygame.display.set_mode(window_dimensions)
            self._play_opponent_turn()
            self._update_window_title()
            self._clock = pygame.time.Clock()
            self._running = True

            while self._running:
                self._handle_events()
                self._draw()
                pygame.display.flip()
                self._clock.tick(FRAMES_PER_SECOND)
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Handle application-level Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._play_move_at(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self._reset_game()

    def _reset_game(self) -> None:
        """Reset the game and restore the configured opening turn."""
        self.game.reset()
        self._play_opponent_turn()
        self._update_window_title()

    def _play_move_at(self, mouse_position: tuple[int, int]) -> None:
        """Delegate the board position at a mouse click to the game."""
        if self.game.current_player != self.human_player:
            return

        board_position = self.board_layout.get_board_position(*mouse_position)

        if board_position is not None:
            row, column = board_position
            if self.game.play_move(row, column):
                self._play_opponent_turn()
                self._update_window_title()

    def _play_opponent_turn(self) -> None:
        """Play one move using the configured opponent selector."""
        if (
            self.opponent_move_selector is not None
            and self.game.current_player != self.human_player
        ):
            self.game.play_selected_move(self.opponent_move_selector)

    def _update_window_title(self) -> None:
        """Display the current game state in the window title."""
        pygame.display.set_caption(self._get_window_title())

    def _get_window_title(self) -> str:
        """Return a window title describing the current game state."""
        return self.title_formatter.format(self.game)

    def _draw(self) -> None:
        """Draw the current application state."""
        if self._screen is None:
            return

        self.board_renderer.draw_board(self._screen, self.game.board)
