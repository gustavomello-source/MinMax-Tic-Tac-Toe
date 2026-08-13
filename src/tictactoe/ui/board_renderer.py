"""Pygame rendering for the Tic Tac Toe board."""

import pygame

from tictactoe.game.board import BOARD_SIZE
from tictactoe.ui.board_layout import BoardLayout

GRID_COLOR = (45, 45, 45)
X_COLOR = (50, 100, 200)
O_COLOR = (220, 80, 80)
GRID_WIDTH = 6
MARK_WIDTH = 12


class PygameBoardRenderer:
    """Draw the board grid on a Pygame surface."""

    def __init__(self, board_layout: BoardLayout) -> None:
        """Create a renderer that follows the supplied board layout."""
        self.board_layout = board_layout

    def draw_grid(self, surface: pygame.Surface) -> None:
        """Draw the lines that divide the board cells."""
        for index in range(1, BOARD_SIZE):
            horizontal_offset = index * self.board_layout.cell_width
            vertical_offset = index * self.board_layout.cell_height
            pygame.draw.line(
                surface,
                GRID_COLOR,
                (horizontal_offset, 0),
                (horizontal_offset, self.board_layout.height),
                GRID_WIDTH,
            )
            pygame.draw.line(
                surface,
                GRID_COLOR,
                (0, vertical_offset),
                (self.board_layout.width, vertical_offset),
                GRID_WIDTH,
            )

    def draw_x(self, surface: pygame.Surface, row: int, column: int) -> None:
        """Draw an X in one board cell."""
        horizontal_padding = self.board_layout.cell_width // 4
        vertical_padding = self.board_layout.cell_height // 4
        left = column * self.board_layout.cell_width + horizontal_padding
        right = (column + 1) * self.board_layout.cell_width - horizontal_padding
        top = row * self.board_layout.cell_height + vertical_padding
        bottom = (row + 1) * self.board_layout.cell_height - vertical_padding

        pygame.draw.line(surface, X_COLOR, (left, top), (right, bottom), MARK_WIDTH)
        pygame.draw.line(surface, X_COLOR, (right, top), (left, bottom), MARK_WIDTH)

    def draw_o(self, surface: pygame.Surface, row: int, column: int) -> None:
        """Draw an O in one board cell."""
        center = (
            column * self.board_layout.cell_width
            + self.board_layout.cell_width // 2,
            row * self.board_layout.cell_height
            + self.board_layout.cell_height // 2,
        )
        shortest_cell_side = min(
            self.board_layout.cell_width,
            self.board_layout.cell_height,
        )
        radius = shortest_cell_side // 4
        pygame.draw.circle(surface, O_COLOR, center, radius, MARK_WIDTH)
