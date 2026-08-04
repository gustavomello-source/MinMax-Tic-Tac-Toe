"""
Implement the tic-tac-toe board representation

This module defines the Board class, which represents the state of the Tic Tac Toe board
and provides methods to store current positions, query and update the game state,
such as making moves, checking available positions, and resetting the board.
"""

from .player_mark import PlayerMark

BOARD_SIZE = 3  # The board is always a 3x3 grid


class Board:
    """Represent the state of the Tic Tac Toe board and provide methods
    to store current positions, querying and updating the game state, such as
    making moves, checking available positions and resetting the board.

    The board is always a 3x3 grid, and each position can be either 'X', 'O', or None (empty).
    """

    def __init__(self) -> None:
        """Initialize the board with an empty state."""
        self.board: list[list[PlayerMark | None]] = [
            [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]

    def reset(self) -> None:
        """Reset the board to its initial empty state."""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.board[i][j] = None

    def make_move(self, row: int, col: int, player: PlayerMark) -> bool:
        """Make a move on the board for the given player ('X' or 'O') at the specified position.

        Args:
            row (int): The row index (0-2) where the player wants to place their mark.
            col (int): The column index (0-2) where the player wants to place their mark.
            player (PlayerMark): The player's mark, either 'X' or 'O'.
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and self.board[row][col] is None
        ):
            self.board[row][col] = player
            return True
        return False

    def get_available_positions(self) -> list[tuple[int, int]]:
        """Get a list of available positions on the board.

        Returns:
            list[tuple[int, int]]: A list of tuples representing the available positions (row, col).
        """
        return [
            (i, j)
            for i in range(BOARD_SIZE)
            for j in range(BOARD_SIZE)
            if self.board[i][j] is None
        ]

    def get_current_state(self) -> list[list[PlayerMark | None]]:
        """Get a copy of the current board state.

        Returns:
            list[list[PlayerMark | None]]: A 3x3 list representing the current board state.
        """
        return [row.copy() for row in self.board]




    def get_winner(self) -> PlayerMark | None:
        """Get the winner of the game, if one exists.

        Returns:
        PlayerMark | None: The winning mark, or None if there is no winner.
        """
        for row in self.board:
            if row[0] is not None and row[0] == row[1] == row[2]:
                return row[0]

        for col in range(BOARD_SIZE):
            if (
                self.board[0][col] is not None
                and self.board[0][col]
                == self.board[1][col]
                == self.board[2][col]
            ):
                return self.board[0][col]

        if (
            self.board[0][0] is not None
            and self.board[0][0] == self.board[1][1] == self.board[2][2]
        ):
            return self.board[0][0]

        if (
            self.board[0][2] is not None
            and self.board[0][2] == self.board[1][1] == self.board[2][0]
        ):
            return self.board[0][2]

        return None

    def is_full(self) -> bool:
        """Check whether the board has no available positions.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return len(self.get_available_positions()) == 0


    def is_game_over(self) -> bool:
        """Check whether the game has ended.

        Returns:
            bool: True if there is a winner or the board is full, False otherwise.
        """
        return self.get_winner() is not None or self.is_full()

    