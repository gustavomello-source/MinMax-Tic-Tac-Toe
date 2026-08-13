"""
Implement the MinMax algorithm for Tic Tac Toe.

This module defines the MinMax class, which evaluates possible moves
and selects the best move for the AI player.
"""

from tictactoe.game.board import Board
from tictactoe.game.player_mark import PlayerMark

WIN_SCORE = 10
LOSS_SCORE = -10
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
        best_score = LOSS_SCORE
        for row, column in board.get_available_positions():
            score = self._evaluate_move(
                board,
                row,
                column,
                self.ai_player,
                depth=0,
            )

            if best_move is None or score > best_score:
                best_score = score
                best_move = (row, column)

        return best_move

    @staticmethod
    def _simulate_move(
        board: Board,
        row: int,
        column: int,
        player: PlayerMark,
    ) -> Board:
        """Return a copied board with one simulated move."""
        simulated_board = board.copy()
        simulated_board.make_move(row, column, player)
        return simulated_board

    def _get_terminal_score(self, board: Board, depth: int) -> int | None:
        """Return a score for a terminal board, or None while play continues."""
        winner = board.get_winner()

        if winner == self.ai_player:
            return WIN_SCORE - depth

        if winner is not None:
            return LOSS_SCORE + depth

        if board.is_draw():
            return DRAW_SCORE

        return None

    def _evaluate_move(
        self,
        board: Board,
        row: int,
        column: int,
        current_player: PlayerMark,
        depth: int,
    ) -> int:
        """Return the MinMax score after one simulated move."""
        simulated_board = self._simulate_move(
            board,
            row,
            column,
            current_player,
        )
        return self._minmax(
            simulated_board,
            current_player.opponent,
            depth + 1,
        )

    def _minmax(
        self,
        board: Board,
        current_player: PlayerMark,
        depth: int,
    ) -> int:
        """Calculate the score of a possible board state.

        Args:
            board (Board): The board state being evaluated.
            current_player (PlayerMark): The player whose turn is being simulated.
        Returns:
            int: The score of the evaluated board state.
        """
        terminal_score = self._get_terminal_score(board, depth)
        if terminal_score is not None:
            return terminal_score

        next_player = current_player.opponent

        if current_player == self.ai_player:
            best_score = LOSS_SCORE

            for row, column in board.get_available_positions():
                score = self._evaluate_move(
                    board,
                    row,
                    column,
                    current_player,
                    depth,
                )
                best_score = max(best_score, score)

            return best_score

        best_score = WIN_SCORE

        for row, column in board.get_available_positions():
            simulated_board = self._simulate_move(
                board,
                row,
                column,
                current_player,
            )

            score = self._minmax(simulated_board, next_player, depth + 1)
            best_score = min(best_score, score)

        return best_score
