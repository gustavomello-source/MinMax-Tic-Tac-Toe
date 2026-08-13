"""Rendering abstraction for Tic Tac Toe boards."""

from typing import Protocol

import pygame

from tictactoe.game.board import Board
from tictactoe.ui.board_layout import BoardLayout


class BoardRenderer(Protocol):
    """Define an object that renders a board on a Pygame surface."""

    board_layout: BoardLayout

    def draw_board(self, surface: pygame.Surface, board: Board) -> None:
        """Draw the supplied board on a surface."""
        ...
