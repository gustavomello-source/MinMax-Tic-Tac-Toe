from tictactoe.ai.minmax import MinMax
from tictactoe.game.game import TicTacToeGame
from tictactoe.game.game_status import GameStatus
from tictactoe.game.player_mark import PlayerMark


class FirstCellSelector:
    """Select the first cell for game-controller tests."""

    def get_best_move(self, _board: object) -> tuple[int, int]:
        """Return a fixed board position."""
        return 0, 0


def test_game_starts_with_x_by_default() -> None:
    """X should play first unless another starting player is selected."""
    game = TicTacToeGame()

    assert game.current_player == PlayerMark.X


def test_new_game_is_in_progress() -> None:
    """A new game should report an active lifecycle status."""
    game = TicTacToeGame()

    assert game.status == GameStatus.IN_PROGRESS


def test_winning_game_reports_won_status() -> None:
    """A game with a winner should report a won lifecycle status."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    game.play_move(row=1, column=0)
    game.play_move(row=0, column=1)
    game.play_move(row=1, column=1)
    game.play_move(row=0, column=2)

    assert game.status == GameStatus.WON


def test_drawn_game_reports_draw_status() -> None:
    """A full game without a winner should report a draw status."""
    game = TicTacToeGame()
    moves = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 0),
        (1, 2),
        (2, 1),
        (2, 0),
        (2, 2),
    ]
    for row, column in moves:
        game.play_move(row, column)

    assert game.status == GameStatus.DRAW


def test_game_accepts_a_custom_starting_player() -> None:
    """The selected starting player should take the first turn."""
    game = TicTacToeGame(starting_player=PlayerMark.O)

    assert game.current_player == PlayerMark.O


def test_play_move_uses_the_current_player() -> None:
    """A legal move should place the current player's mark on the board."""
    game = TicTacToeGame()

    move_was_played = game.play_move(row=1, column=2)

    assert move_was_played is True
    assert game.board.get_current_state()[1][2] == PlayerMark.X


def test_successful_move_changes_the_current_player() -> None:
    """Players should alternate after each legal move."""
    game = TicTacToeGame()

    game.play_move(row=0, column=0)

    assert game.current_player == PlayerMark.O


def test_invalid_move_does_not_change_the_current_player() -> None:
    """The same player should retry after an illegal move."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)

    move_was_played = game.play_move(row=0, column=0)

    assert move_was_played is False
    assert game.current_player == PlayerMark.O


def test_move_is_rejected_after_the_game_ends() -> None:
    """No marks should be added after a player has won."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    game.play_move(row=1, column=0)
    game.play_move(row=0, column=1)
    game.play_move(row=1, column=1)
    game.play_move(row=0, column=2)

    move_was_played = game.play_move(row=2, column=2)

    assert move_was_played is False
    assert game.board.get_current_state()[2][2] is None


def test_reset_starts_a_new_game() -> None:
    """Reset should clear the board and restore the configured first player."""
    game = TicTacToeGame(starting_player=PlayerMark.O)
    game.play_move(row=0, column=0)

    game.reset()

    assert game.current_player == PlayerMark.O
    assert all(
        mark is None
        for row in game.board.get_current_state()
        for mark in row
    )


def test_play_selected_move_delegates_move_selection() -> None:
    """A selected move should use the game's normal turn handling."""
    game = TicTacToeGame()

    move_was_played = game.play_selected_move(FirstCellSelector())

    assert move_was_played is True
    assert game.board.get_current_state()[0][0] == PlayerMark.X
    assert game.current_player == PlayerMark.O


def test_game_accepts_minmax_as_move_selector() -> None:
    """MinMax should select a move through the game abstraction."""
    game = TicTacToeGame()
    game.play_move(row=0, column=0)
    game.play_move(row=1, column=0)
    game.play_move(row=0, column=1)
    game.play_move(row=1, column=1)

    move_was_played = game.play_selected_move(MinMax(PlayerMark.X))

    assert move_was_played is True
    assert game.board.get_winner() == PlayerMark.X
