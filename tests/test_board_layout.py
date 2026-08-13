from tictactoe.ui.board_layout import BoardLayout


def test_get_board_position_returns_cell_at_coordinates() -> None:
    """Coordinates inside the layout should map to a board position."""
    layout = BoardLayout(width=600, height=600)

    assert layout.get_board_position(x=250, y=450) == (2, 1)


def test_get_board_position_rejects_coordinates_outside_layout() -> None:
    """Coordinates outside the layout should not map to the board."""
    layout = BoardLayout(width=600, height=600)

    assert layout.get_board_position(x=600, y=200) is None
