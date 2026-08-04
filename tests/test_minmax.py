from tictactoe.ai.minmax import MinMax
from tictactoe.game.board import Board
from tictactoe.game.player_mark import PlayerMark


def test_ai_wins() -> None:
    """The AI should choose a move that wins the game."""
    board = Board()
    ai = MinMax(PlayerMark.O)

    board.make_move(0, 0, PlayerMark.O)
    board.make_move(0, 1, PlayerMark.O)
    board.make_move(1, 0, PlayerMark.X)
    board.make_move(1, 1, PlayerMark.X)

    move: tuple[int, int] | None = ai.get_best_move(board)

    assert move == (0, 2)


def test_ai_blocks() -> None:
    """The AI should block an immediate opponent victory."""
    board = Board()
    ai = MinMax(PlayerMark.O)

    board.make_move(0, 0, PlayerMark.X)
    board.make_move(0, 1, PlayerMark.X)
    board.make_move(1, 0, PlayerMark.O)

    move: tuple[int, int] | None = ai.get_best_move(board)

    assert move == (0, 2)


def test_ai_chooses_available_position() -> None:
    """The AI should choose an available board position."""
    board = Board()
    ai = MinMax(PlayerMark.O)

    board.make_move(0, 0, PlayerMark.X)
    board.make_move(0, 2, PlayerMark.X)
    board.make_move(1, 1, PlayerMark.O)

    available_positions: list[tuple[int, int]] = (
        board.get_available_positions()
    )

    move: tuple[int, int] | None = ai.get_best_move(board)

    assert move in available_positions


def test_no_move_when_game_over() -> None:
    """The AI should return None when the game has ended."""
    board = Board()
    ai = MinMax(PlayerMark.O)

    board.make_move(0, 0, PlayerMark.X)
    board.make_move(0, 1, PlayerMark.X)
    board.make_move(0, 2, PlayerMark.X)

    move: tuple[int, int] | None = ai.get_best_move(board)

    assert move is None


def test_board_is_not_changed() -> None:
    """Calculating a move should not change the original board."""
    board = Board()
    ai = MinMax(PlayerMark.O)

    board.make_move(0, 0, PlayerMark.X)
    board.make_move(1, 1, PlayerMark.O)

    state_before: list[list[PlayerMark | None]] = (
        board.get_current_state()
    )

    ai.get_best_move(board)

    assert board.get_current_state() == state_before


def test_ai_uses_last_position() -> None:
    """The AI should choose the final available position."""
    board = Board()
    ai = MinMax(PlayerMark.X)

    moves: list[tuple[int, int, PlayerMark]] = [
        (0, 0, PlayerMark.X),
        (0, 1, PlayerMark.O),
        (0, 2, PlayerMark.X),
        (1, 0, PlayerMark.X),
        (1, 1, PlayerMark.O),
        (1, 2, PlayerMark.O),
        (2, 0, PlayerMark.O),
        (2, 1, PlayerMark.X),
    ]

    for row, col, player in moves:
        board.make_move(row, col, player)

    move: tuple[int, int] | None = ai.get_best_move(board)

    assert move == (2, 2)