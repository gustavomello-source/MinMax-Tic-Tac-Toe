from tictactoe.game.board import (
    BOARD_AREA,
    BOARD_POSITIONS,
    BOARD_SIZE,
    WINNING_LINES,
    Board,
)
from tictactoe.game.player_mark import PlayerMark


def test_board_is_initialized_empty() -> None:
    """The board should start with all positions empty."""
    board = Board()

    state: list[list[PlayerMark | None]] = board.get_current_state()

    assert len(state) == BOARD_SIZE
    assert all(len(row) == BOARD_SIZE for row in state)
    assert all(cell is None for row in state for cell in row)


def test_board_defines_all_winning_lines() -> None:
    """A 3x3 board should define rows, columns, and diagonals as winning lines."""
    assert len(WINNING_LINES) == 8


def test_board_defines_every_position() -> None:
    """Board positions should contain each row and column coordinate once."""
    assert len(BOARD_POSITIONS) == BOARD_AREA
    assert len(set(BOARD_POSITIONS)) == BOARD_AREA


def test_make_move_places_player_mark() -> None:
    """A valid move should place the player's mark on the board."""
    board = Board()

    success: bool = board.make_move(row=1, column=2, player=PlayerMark.X)

    assert success is True
    assert board.get_current_state()[1][2] == PlayerMark.X


def test_make_move_returns_false_if_position_is_occupied() -> None:
    """A move cannot overwrite an occupied position."""
    board = Board()

    board.make_move(row=0, column=0, player=PlayerMark.X)

    success: bool = board.make_move(row=0, column=0, player=PlayerMark.O)

    assert success is False
    assert board.get_current_state()[0][0] == PlayerMark.X


def test_make_move_returns_false_for_negative_row() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=-1, column=0, player=PlayerMark.X) is False


def test_make_move_returns_false_for_negative_column() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=0, column=-1, player=PlayerMark.X) is False


def test_make_move_returns_false_for_row_out_of_bounds() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=BOARD_SIZE, column=0, player=PlayerMark.X) is False


def test_make_move_returns_false_for_column_out_of_bounds() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=0, column=BOARD_SIZE, player=PlayerMark.X) is False


def test_reset_clears_the_board() -> None:
    """Reset should remove all player marks."""
    board = Board()

    board.make_move(row=0, column=0, player=PlayerMark.X)
    board.make_move(row=2, column=2, player=PlayerMark.O)

    board.reset()

    state: list[list[PlayerMark | None]] = board.get_current_state()

    assert all(cell is None for row in state for cell in row)


def test_get_available_positions_returns_all_positions_on_empty_board() -> None:
    """An empty board should report every position as available."""
    board = Board()

    positions: list[tuple[int, int]] = board.get_available_positions()

    expected: list[tuple[int, int]] = [
        (row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)
    ]

    assert sorted(positions) == expected


def test_get_available_positions_excludes_occupied_positions() -> None:
    """Occupied positions should not be reported as available."""
    board = Board()

    board.make_move(row=0, column=0, player=PlayerMark.X)
    board.make_move(row=2, column=1, player=PlayerMark.O)

    positions: list[tuple[int, int]] = board.get_available_positions()

    assert (0, 0) not in positions
    assert (2, 1) not in positions
    assert len(positions) == BOARD_SIZE * BOARD_SIZE - 2


def test_get_current_state_returns_copy() -> None:
    """The returned board state should not expose the internal board."""
    board = Board()

    state: list[list[PlayerMark | None]] = board.get_current_state()
    state[0][0] = PlayerMark.X

    assert board.get_current_state()[0][0] is None


def test_get_mark_returns_mark_at_position() -> None:
    """A board position should expose its stored mark."""
    board = Board()
    board.make_move(row=1, column=2, player=PlayerMark.O)

    assert board.get_mark(row=1, column=2) == PlayerMark.O


def test_get_mark_returns_none_outside_board() -> None:
    """A position outside the board should not contain a mark."""
    board = Board()

    assert board.get_mark(row=BOARD_SIZE, column=0) is None


def test_contains_position_accepts_position_inside_board() -> None:
    """A valid row and column should be contained by the board."""
    board = Board()

    assert board.contains_position(row=2, column=2) is True


def test_contains_position_rejects_position_outside_board() -> None:
    """An invalid row or column should be outside the board."""
    board = Board()

    assert board.contains_position(row=-1, column=0) is False


def test_empty_position_is_available() -> None:
    """An empty position inside the board should be available."""
    board = Board()

    assert board.is_position_available(row=1, column=1) is True


def test_occupied_position_is_not_available() -> None:
    """A position containing a mark should not be available."""
    board = Board()
    board.make_move(row=1, column=1, player=PlayerMark.X)

    assert board.is_position_available(row=1, column=1) is False


def test_move_count_reports_placed_marks() -> None:
    """Move count should report how many positions contain marks."""
    board = Board()
    board.make_move(row=0, column=0, player=PlayerMark.X)
    board.make_move(row=1, column=1, player=PlayerMark.O)

    assert board.move_count == 2


def test_copy_returns_independent_board() -> None:
    """Changing a copied board should not change the original board."""
    board = Board()
    board.make_move(row=0, column=0, player=PlayerMark.X)

    copied_board = board.copy()
    copied_board.make_move(row=1, column=1, player=PlayerMark.O)

    assert copied_board.get_current_state()[0][0] == PlayerMark.X
    assert board.get_current_state()[1][1] is None


def test_get_winner() -> None:
    """Should detect winners in rows, columns and diagonals."""

    row_board = Board()
    row_board.make_move(0, 0, PlayerMark.X)
    row_board.make_move(0, 1, PlayerMark.X)
    row_board.make_move(0, 2, PlayerMark.X)

    assert row_board.get_winner() == PlayerMark.X

def test_get_winner_in_column() -> None:
    """Three equal marks in a column should produce a winner."""
    board = Board()

    board.make_move(0, 1, PlayerMark.O)
    board.make_move(1, 1, PlayerMark.O)
    board.make_move(2, 1, PlayerMark.O)

    assert board.get_winner() == PlayerMark.O


def test_get_winner_in_main_diagonal() -> None:
    """Three equal marks in the main diagonal should produce a winner."""
    board = Board()

    board.make_move(0, 0, PlayerMark.X)
    board.make_move(1, 1, PlayerMark.X)
    board.make_move(2, 2, PlayerMark.X)

    assert board.get_winner() == PlayerMark.X


def test_get_winner_in_secondary_diagonal() -> None:
    """Three equal marks in the secondary diagonal should produce a winner."""
    board = Board()

    board.make_move(0, 2, PlayerMark.O)
    board.make_move(1, 1, PlayerMark.O)
    board.make_move(2, 0, PlayerMark.O)

    assert board.get_winner() == PlayerMark.O


def test_get_winner_returns_none() -> None:
    """An empty board should not have a winner."""
    board = Board()

    assert board.get_winner() is None


def test_is_full_returns_false_for_empty_board() -> None:
    """An empty board should not be considered full."""
    board = Board()

    assert board.is_full() is False


def test_is_full_returns_true_for_full_board() -> None:
    """A board without available positions should be considered full."""
    board = Board()

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            board.make_move(row, col, PlayerMark.X)

    assert board.is_full() is True


def test_is_draw_returns_true_for_full_board_without_winner() -> None:
    """A full board without a winner should be a draw."""
    board = Board()
    moves = [
        (0, 0, PlayerMark.X),
        (0, 1, PlayerMark.O),
        (0, 2, PlayerMark.X),
        (1, 0, PlayerMark.X),
        (1, 1, PlayerMark.O),
        (1, 2, PlayerMark.O),
        (2, 0, PlayerMark.O),
        (2, 1, PlayerMark.X),
        (2, 2, PlayerMark.X),
    ]
    for row, column, player in moves:
        board.make_move(row, column, player)

    assert board.is_draw() is True


def test_is_draw_returns_false_for_winning_board() -> None:
    """A board with a winner should not be a draw."""
    board = Board()
    board.make_move(0, 0, PlayerMark.X)
    board.make_move(0, 1, PlayerMark.X)
    board.make_move(0, 2, PlayerMark.X)

    assert board.is_draw() is False


def test_game_continues() -> None:
    """A game without a winner or full board should continue."""
    board = Board()

    board.make_move(0, 0, PlayerMark.X)

    assert board.is_game_over() is False


def test_game_over_with_winner() -> None:
    """A game should end when a player wins."""
    board = Board()

    board.make_move(0, 0, PlayerMark.X)
    board.make_move(0, 1, PlayerMark.X)
    board.make_move(0, 2, PlayerMark.X)

    assert board.is_game_over() is True


def test_game_over_with_draw() -> None:
    """A game should end when the board is full without a winner."""
    board = Board()

    moves = [
        (0, 0, PlayerMark.X),
        (0, 1, PlayerMark.O),
        (0, 2, PlayerMark.X),
        (1, 0, PlayerMark.X),
        (1, 1, PlayerMark.O),
        (1, 2, PlayerMark.O),
        (2, 0, PlayerMark.O),
        (2, 1, PlayerMark.X),
        (2, 2, PlayerMark.X),
    ]

    for row, col, player in moves:
        board.make_move(row, col, player)

    assert board.get_winner() is None
    assert board.is_game_over() is True
