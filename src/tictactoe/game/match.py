"""
Implement the Tic Tac Toe match controller.

This module defines the Match class, which controls the board,
players, turns, and moves during a match.
"""

from ..ai.minmax import MinMax
from .board import Board
from .player_mark import PlayerMark

class Match:
    """Control the board, players and turns of a Tic Tac Toe match.""" 


    def __init__(self, human_player: PlayerMark = PlayerMark.X) -> None:
        """Initialize a new match.

        Args:
            human_player (PlayerMark): The mark controlled by the human.
        """
        self.board: Board = Board()
        self.human_player: PlayerMark = human_player
        self.ai_player: PlayerMark = (
            PlayerMark.O
            if human_player == PlayerMark.X
            else PlayerMark.X
        )
        self.current_player: PlayerMark = PlayerMark.X
        self.ai: MinMax = MinMax(self.ai_player)


    def _switch_player(self) -> None:
        """Switch the current player between X and O."""
        if self.current_player == PlayerMark.X:
            self.current_player = PlayerMark.O
        else:
            self.current_player = PlayerMark.X


    def play_move(self, row: int, col: int) -> bool:
        """Play a move for the current player.

        Args:
            row (int): The row index of the move.
            col (int): The column index of the move.
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.board.is_game_over():
            return False

        success: bool = self.board.make_move(row, col, self.current_player)

        if not success:
            return False

        if not self.board.is_game_over():
            self._switch_player()

        return True


    def play_ai_move(self) -> tuple[int, int] | None:
        """Calculate and play the AI move.

        Returns:
            tuple[int, int] | None: The AI position, or None if it cannot play.
        """
        if self.current_player != self.ai_player:
            return None

        if self.board.is_game_over():
            return None

        move: tuple[int, int] | None = self.ai.get_best_move(self.board)

        if move is None:
            return None

        row, col = move
        success: bool = self.play_move(row, col)

        if not success:
            return None

        return move

    def reset(self) -> None:
        """Reset the board and return the turn to player X."""
        self.board.reset()
        self.current_player = PlayerMark.X
    