from tictactoe.game.game_status import GameStatus


def test_game_status_defines_game_lifecycle_states() -> None:
    """Game status should distinguish active, won, and drawn games."""
    assert set(GameStatus) == {
        GameStatus.IN_PROGRESS,
        GameStatus.WON,
        GameStatus.DRAW,
    }
