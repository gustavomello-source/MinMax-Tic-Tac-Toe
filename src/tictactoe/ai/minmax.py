"""
Implement the MinMax algorithm for Tic Tac Toe.

This module defines the MinMax class, which evaluates possible moves
and selects the best move for the AI player.
"""

from copy import deepcopy

from tictactoe.game.board import Board
from tictactoe.game.player_mark import PlayerMark

WIN_SCORE = 1
LOSS_SCORE = -1
DRAW_SCORE = 0


class MinMax:
    """Evaluate possible board states and select the best move for the AI."""

    def __init__(self, ai_player: PlayerMark) -> None:
        """Initialize the MinMax algorithm.

        Args:
            ai_player (PlayerMark): The mark controlled by the AI.
        """
        self.ai_player = ai_player

    def get_best_move(self, board: Board) -> tuple[int, int] | None:
        """Get the best available move for the AI.

        Args:
            board (Board): The current game board.
        Returns:
            tuple[int, int] | None: The best position, or None if the game is over.
        """
        if board.is_game_over():
            return None

        best_move: tuple[int, int] | None = None
        best_score: int = LOSS_SCORE   
        opponent: PlayerMark = self.ai_player.opponent

        for row, column in board.get_available_positions():
            simulated_board: Board = deepcopy(board)
            simulated_board.make_move(row, column, self.ai_player)

            score: int = self._minmax(simulated_board, opponent)

            if best_move is None or score > best_score:
                best_score = score
                best_move = (row, column)

        return best_move
    def _minmax(self, board: Board, current_player: PlayerMark) -> int:
        """Calculate the score of a possible board state.

        Args:
            board (Board): The board state being evaluated.
            current_player (PlayerMark): The player whose turn is being simulated.
        Returns:
            int: The score of the evaluated board state.
        """
        winner: PlayerMark | None = board.get_winner()

        if winner == self.ai_player:
            return WIN_SCORE

        if winner is not None:
            return LOSS_SCORE

        if board.is_full():
            return DRAW_SCORE

        next_player: PlayerMark = current_player.opponent

        if current_player == self.ai_player:
            best_score: int = LOSS_SCORE

            for row, column in board.get_available_positions():
                simulated_board: Board = deepcopy(board)
                simulated_board.make_move(row, column, current_player)

                score: int = self._minmax(simulated_board, next_player)
                best_score = max(best_score, score)

            return best_score

        best_score = WIN_SCORE

        for row, column in board.get_available_positions():
            simulated_board = deepcopy(board)
            simulated_board.make_move(row, column, current_player)

            score = self._minmax(simulated_board, next_player)
            best_score = min(best_score, score)

        return best_score
