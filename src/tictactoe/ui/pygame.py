"""Pygame user interface for Tic Tac Toe."""

import pygame

from game.board import BOARD_SIZE, Board
from game.player_mark import PlayerMark

WINDOW_SIZE = 600
WINDOW_TITLE = "MinMax Tic Tac Toe"
FRAMES_PER_SECOND = 60

BACKGROUND_COLOR = (245, 245, 245)
GRID_COLOR = (45, 45, 45)
X_COLOR = (50, 100, 200)
O_COLOR = (220, 80, 80)

GRID_WIDTH = 6
MARK_WIDTH = 12
CELL_SIZE = WINDOW_SIZE // BOARD_SIZE
MARK_PADDING = CELL_SIZE // 4


class PyGameBoard:
    """Manage the Pygame window and render the current board state."""

    def __init__(self, board: Board | None = None) -> None:
        """Create an application for the supplied board or a new empty board."""
        self.board = board if board is not None else Board()
        self._screen: pygame.Surface | None = None
        self._clock: pygame.time.Clock | None = None
        self._running = False

    def run(self) -> None:
        """Open the window and run the application until it is closed."""
        pygame.init()

        try:
            self._screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption(WINDOW_TITLE)
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
            offset = index * CELL_SIZE
            pygame.draw.line(
                self._screen,
                GRID_COLOR,
                (offset, 0),
                (offset, WINDOW_SIZE),
                GRID_WIDTH,
            )
            pygame.draw.line(
                self._screen,
                GRID_COLOR,
                (0, offset),
                (WINDOW_SIZE, offset),
                GRID_WIDTH,
            )

    def _draw_marks(self) -> None:
        """Draw every mark stored in the board model."""
        for row_index, row in enumerate(self.board.get_current_state()):
            for col_index, mark in enumerate(row):
                if mark == PlayerMark.X:
                    self._draw_x(row_index, col_index)
                elif mark == PlayerMark.O:
                    self._draw_o(row_index, col_index)

    def _draw_x(self, row: int, col: int) -> None:
        """Draw an X in one board cell."""
        if self._screen is None:
            return

        left = col * CELL_SIZE + MARK_PADDING
        right = (col + 1) * CELL_SIZE - MARK_PADDING
        top = row * CELL_SIZE + MARK_PADDING
        bottom = (row + 1) * CELL_SIZE - MARK_PADDING

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
            col * CELL_SIZE + CELL_SIZE // 2,
            row * CELL_SIZE + CELL_SIZE // 2,
        )
        radius = CELL_SIZE // 2 - MARK_PADDING
        pygame.draw.circle(self._screen, O_COLOR, center, radius, MARK_WIDTH)
