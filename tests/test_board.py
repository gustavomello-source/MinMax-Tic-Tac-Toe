from src.tictactoe.game.board import BOARD_SIZE, Board
from src.tictactoe.game.player_mark import PlayerMark


def test_board_is_initialized_empty() -> None:
    """The board should start with all positions empty."""
    board = Board()

    state: list[list[PlayerMark | None]] = board.get_current_state()

    assert len(state) == BOARD_SIZE
    assert all(len(row) == BOARD_SIZE for row in state)
    assert all(cell is None for row in state for cell in row)


def test_make_move_places_player_mark() -> None:
    """A valid move should place the player's mark on the board."""
    board = Board()

    success: bool = board.make_move(row=1, col=2, player=PlayerMark.X)

    assert success is True
    assert board.get_current_state()[1][2] == PlayerMark.X


def test_make_move_returns_false_if_position_is_occupied() -> None:
    """A move cannot overwrite an occupied position."""
    board = Board()

    board.make_move(row=0, col=0, player=PlayerMark.X)

    success: bool = board.make_move(row=0, col=0, player=PlayerMark.O)

    assert success is False
    assert board.get_current_state()[0][0] == PlayerMark.X


def test_make_move_returns_false_for_negative_row() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=-1, col=0, player=PlayerMark.X) is False


def test_make_move_returns_false_for_negative_column() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=0, col=-1, player=PlayerMark.X) is False


def test_make_move_returns_false_for_row_out_of_bounds() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=BOARD_SIZE, col=0, player=PlayerMark.X) is False


def test_make_move_returns_false_for_column_out_of_bounds() -> None:
    """A move outside the board should fail."""
    board = Board()

    assert board.make_move(row=0, col=BOARD_SIZE, player=PlayerMark.X) is False


def test_reset_clears_the_board() -> None:
    """Reset should remove all player marks."""
    board = Board()

    board.make_move(row=0, col=0, player=PlayerMark.X)
    board.make_move(row=2, col=2, player=PlayerMark.O)

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

    board.make_move(row=0, col=0, player=PlayerMark.X)
    board.make_move(row=2, col=1, player=PlayerMark.O)

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
