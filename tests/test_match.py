from tictactoe.game.match import Match
from tictactoe.game.player_mark import PlayerMark


def test_match_initial_state() -> None:
    """A match should start with the human as X and an empty board."""
    match = Match()

    assert match.human_player == PlayerMark.X
    assert match.ai_player == PlayerMark.O
    assert match.current_player == PlayerMark.X
    assert match.board.get_available_positions() == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ]


def test_human_can_use_o() -> None:
    """The AI should use X when the human chooses O."""
    match = Match(human_player=PlayerMark.O)

    assert match.human_player == PlayerMark.O
    assert match.ai_player == PlayerMark.X
    assert match.current_player == PlayerMark.X


def test_valid_move() -> None:
    """A valid move should be stored and switch the current player."""
    match = Match()

    success: bool = match.play_move(row=0, col=0)

    assert success is True
    assert match.board.get_current_state()[0][0] == PlayerMark.X
    assert match.current_player == PlayerMark.O


def test_invalid_move() -> None:
    """An invalid move should not switch the current player."""
    match = Match()

    match.play_move(row=0, col=0)
    success: bool = match.play_move(row=0, col=0)

    assert success is False
    assert match.current_player == PlayerMark.O


def test_move_after_game_over() -> None:
    """A move should not be accepted after the game has ended."""
    match = Match()

    match.play_move(0, 0)
    match.play_move(1, 0)
    match.play_move(0, 1)
    match.play_move(1, 1)
    match.play_move(0, 2)

    success: bool = match.play_move(2, 2)

    assert match.board.is_game_over() is True
    assert success is False
    assert match.board.get_current_state()[2][2] is None


def test_ai_waits_for_its_turn() -> None:
    """The AI should not play during the human turn."""
    match = Match()

    move: tuple[int, int] | None = match.play_ai_move()

    assert move is None
    assert len(match.board.get_available_positions()) == 9


def test_ai_plays() -> None:
    """The AI should play a valid move during its turn."""
    match = Match()

    match.play_move(row=1, col=1)
    move: tuple[int, int] | None = match.play_ai_move()

    assert move is not None

    row, col = move

    assert match.board.get_current_state()[row][col] == PlayerMark.O
    assert match.current_player == PlayerMark.X


def test_reset() -> None:
    """Reset should clear the board and return the turn to X."""
    match = Match()

    match.play_move(row=0, col=0)
    match.play_ai_move()
    match.reset()

    state: list[list[PlayerMark | None]] = (
        match.board.get_current_state()
    )

    assert all(cell is None for row in state for cell in row)
    assert match.current_player == PlayerMark.X
    assert match.human_player == PlayerMark.X
    assert match.ai_player == PlayerMark.O