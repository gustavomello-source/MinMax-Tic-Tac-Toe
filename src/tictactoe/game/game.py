"""Turn-based game flow for Tic Tac Toe."""

from tictactoe.game.board import Board
from tictactoe.game.move_selector import MoveSelector
from tictactoe.game.player_mark import PlayerMark


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
            self.current_player = self.current_player.opponent

        return move_was_played

    def play_selected_move(self, move_selector: MoveSelector) -> bool:
        """Request and play a move from a move selector."""
        selected_move = move_selector.get_best_move(self.board)

        if selected_move is None:
            return False

        row, column = selected_move
        return self.play_move(row, column)

    def reset(self) -> None:
        """Reset the board and restore the starting player."""
        self.board.reset()
        self.current_player = self.starting_player
