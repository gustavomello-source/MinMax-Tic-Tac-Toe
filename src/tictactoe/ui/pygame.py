"""Pygame user interface for Tic Tac Toe."""

import pygame

from tictactoe.game.game import TicTacToeGame
from tictactoe.game.move_selector import MoveSelector
from tictactoe.ui.board_layout import BoardLayout
from tictactoe.ui.board_renderer import PygameBoardRenderer

WINDOW_SIZE = 600
WINDOW_TITLE = "MinMax Tic Tac Toe"
FRAMES_PER_SECOND = 60

class PygameApp:
    """Manage the Pygame application lifecycle and user interface."""

    def __init__(
        self,
        game: TicTacToeGame | None = None,
        board_layout: BoardLayout | None = None,
        opponent_move_selector: MoveSelector | None = None,
    ) -> None:
        """Create a Pygame board for the supplied or a new game."""
        self.game = game if game is not None else TicTacToeGame()
        self.opponent_move_selector = opponent_move_selector
        self.board_layout = board_layout or BoardLayout(
            width=WINDOW_SIZE,
            height=WINDOW_SIZE,
        )
        self.board_renderer = PygameBoardRenderer(self.board_layout)
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
                self.game.reset()
                self._update_window_title()

    def _play_move_at(self, mouse_position: tuple[int, int]) -> None:
        """Delegate the board position at a mouse click to the game."""
        board_position = self.board_layout.get_board_position(*mouse_position)

        if board_position is not None:
            row, column = board_position
            if self.game.play_move(row, column):
                if self.opponent_move_selector is not None:
                    self.game.play_selected_move(self.opponent_move_selector)
                self._update_window_title()

    def _update_window_title(self) -> None:
        """Display the winner or current player in the window title."""
        winner = self.game.board.get_winner()

        if winner is not None:
            pygame.display.set_caption(f"{WINDOW_TITLE} - {winner.value} wins")
            return

        if self.game.board.is_full():
            pygame.display.set_caption(f"{WINDOW_TITLE} - Draw")
            return

        current_mark = self.game.current_player.value
        pygame.display.set_caption(f"{WINDOW_TITLE} - {current_mark}'s turn")

    def _draw(self) -> None:
        """Draw the current application state."""
        if self._screen is None:
            return

        self.board_renderer.draw_board(self._screen, self.game.board)
