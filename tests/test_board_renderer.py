import pygame

from tictactoe.ui.board_layout import BoardLayout
from tictactoe.ui.board_renderer import GRID_COLOR, PygameBoardRenderer


def test_draw_grid_draws_cell_divider() -> None:
    """Grid rendering should draw a divider at each cell boundary."""
    board_layout = BoardLayout(width=300, height=300)
    renderer = PygameBoardRenderer(board_layout)
    surface = pygame.Surface((300, 300))

    renderer.draw_grid(surface)

    assert surface.get_at((100, 50))[:3] == GRID_COLOR
