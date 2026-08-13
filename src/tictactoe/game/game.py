"""Turn-based game flow for Tic Tac Toe."""

from .board import Board
from .player_mark import PlayerMark


class TicTacToeGame:
    """Coordinate turns and moves for one Tic Tac Toe game."""

    def __init__(self, starting_player: PlayerMark = PlayerMark.X) -> None:
        """Create an empty game with the selected starting player."""
        self.board = Board()
        self.starting_player = starting_player
        self.current_player = starting_player

    def play_move(self, row: int, column: int) -> bool:
        """Play a move for the current player when the move is legal."""
        if self.board.is_game_over():
            return False

        move_was_played = self.board.make_move(row, column, self.current_player)

        if move_was_played:
            self.current_player = self._get_opponent(self.current_player)

        return move_was_played

    def reset(self) -> None:
        """Reset the board and restore the starting player."""
        self.board.reset()
        self.current_player = self.starting_player

    @staticmethod
    def _get_opponent(player: PlayerMark) -> PlayerMark:
        """Return the mark that plays after the supplied player."""
        if player == PlayerMark.X:
            return PlayerMark.O

        return PlayerMark.X
