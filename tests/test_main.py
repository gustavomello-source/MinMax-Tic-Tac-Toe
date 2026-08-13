from tictactoe.ai.minmax import MinMax
from tictactoe.game.player_mark import PlayerMark
from tictactoe.main import create_app


def test_create_app_configures_minmax_as_o_player() -> None:
    """The application should use MinMax as the O opponent."""
    app = create_app()

    assert isinstance(app.opponent_move_selector, MinMax)
    assert app.opponent_move_selector.ai_player == PlayerMark.O
