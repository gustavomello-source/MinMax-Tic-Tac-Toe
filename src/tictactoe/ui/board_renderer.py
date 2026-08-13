"""Pygame rendering for the Tic Tac Toe board."""

import pygame

from tictactoe.game.board import BOARD_SIZE
from tictactoe.ui.board_layout import BoardLayout

GRID_COLOR = (45, 45, 45)
GRID_WIDTH = 6


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
