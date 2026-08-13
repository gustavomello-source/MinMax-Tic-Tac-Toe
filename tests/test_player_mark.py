from tictactoe.game.player_mark import PlayerMark


def test_x_opponent_is_o() -> None:
    """X should identify O as its opponent."""
    assert PlayerMark.X.opponent == PlayerMark.O


def test_o_opponent_is_x() -> None:
    """O should identify X as its opponent."""
    assert PlayerMark.O.opponent == PlayerMark.X
