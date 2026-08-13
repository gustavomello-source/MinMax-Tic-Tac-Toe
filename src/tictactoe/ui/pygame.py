"""Pygame user interface for Tic Tac Toe."""

import pygame

from tictactoe.game.board import BOARD_SIZE
from tictactoe.game.game import TicTacToeGame
from tictactoe.game.player_mark import PlayerMark
from tictactoe.ui.board_layout import BoardLayout

WINDOW_SIZE = 600
WINDOW_TITLE = "MinMax Tic Tac Toe"
FRAMES_PER_SECOND = 60

BACKGROUND_COLOR = (245, 245, 245)
GRID_COLOR = (45, 45, 45)
X_COLOR = (50, 100, 200)
O_COLOR = (220, 80, 80)

GRID_WIDTH = 6
MARK_WIDTH = 12


class PyGameBoard:
    """Manage the Pygame window and render the current board state."""

    def __init__(
        self,
        game: TicTacToeGame | None = None,
        board_layout: BoardLayout | None = None,
    ) -> None:
        """Create a Pygame board for the supplied or a new game."""
        self.game = game if game is not None else TicTacToeGame()
        self.board_layout = board_layout or BoardLayout(
            width=WINDOW_SIZE,
            height=WINDOW_SIZE,
        )
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
                self._update_window_title()

    def _update_window_title(self) -> None:
        """Display the current player in the window title."""
        current_mark = self.game.current_player.value
        pygame.display.set_caption(f"{WINDOW_TITLE} - {current_mark}'s turn")

    def _draw(self) -> None:
        """Draw the current application state."""
        if self._screen is None:
            return

        self._screen.fill(BACKGROUND_COLOR)
        self._draw_grid()
        self._draw_marks()

    def _draw_grid(self) -> None:
        """Draw the lines that divide the board cells."""
        if self._screen is None:
            return

        for index in range(1, BOARD_SIZE):
            horizontal_offset = index * self.board_layout.cell_width
            vertical_offset = index * self.board_layout.cell_height
            pygame.draw.line(
                self._screen,
                GRID_COLOR,
                (horizontal_offset, 0),
                (horizontal_offset, self.board_layout.height),
                GRID_WIDTH,
            )
            pygame.draw.line(
                self._screen,
                GRID_COLOR,
                (0, vertical_offset),
                (self.board_layout.width, vertical_offset),
                GRID_WIDTH,
            )

    def _draw_marks(self) -> None:
        """Draw every mark stored in the board model."""
        for row_index, row in enumerate(self.game.board.get_current_state()):
            for col_index, mark in enumerate(row):
                if mark == PlayerMark.X:
                    self._draw_x(row_index, col_index)
                elif mark == PlayerMark.O:
                    self._draw_o(row_index, col_index)

    def _draw_x(self, row: int, col: int) -> None:
        """Draw an X in one board cell."""
        if self._screen is None:
            return

        horizontal_padding = self.board_layout.cell_width // 4
        vertical_padding = self.board_layout.cell_height // 4
        left = col * self.board_layout.cell_width + horizontal_padding
        right = (col + 1) * self.board_layout.cell_width - horizontal_padding
        top = row * self.board_layout.cell_height + vertical_padding
        bottom = (row + 1) * self.board_layout.cell_height - vertical_padding

        pygame.draw.line(
            self._screen, X_COLOR, (left, top), (right, bottom), MARK_WIDTH
        )
        pygame.draw.line(
            self._screen, X_COLOR, (right, top), (left, bottom), MARK_WIDTH
        )

    def _draw_o(self, row: int, col: int) -> None:
        """Draw an O in one board cell."""
        if self._screen is None:
            return

        center = (
            col * self.board_layout.cell_width
            + self.board_layout.cell_width // 2,
            row * self.board_layout.cell_height
            + self.board_layout.cell_height // 2,
        )
        shortest_cell_side = min(
            self.board_layout.cell_width,
            self.board_layout.cell_height,
        )
        radius = shortest_cell_side // 4
        pygame.draw.circle(self._screen, O_COLOR, center, radius, MARK_WIDTH)
