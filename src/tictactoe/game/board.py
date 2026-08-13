"""
Implement the tic-tac-toe board representation

This module defines the Board class, which represents the state of the Tic Tac Toe board
and provides methods to store current positions, query and update the game state,
such as making moves, checking available positions, and resetting the board.
"""

from tictactoe.game.player_mark import PlayerMark

BOARD_SIZE = 3  # The board is always a 3x3 grid
BOARD_AREA = BOARD_SIZE * BOARD_SIZE
BOARD_POSITIONS = tuple(
    (row, column)
    for row in range(BOARD_SIZE)
    for column in range(BOARD_SIZE)
)
WINNING_LINES = (
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
)


class Board:
    """Represent the state of the Tic Tac Toe board and provide methods
    to store current positions, querying and updating the game state, such as
    making moves, checking available positions and resetting the board.

    The board is always a 3x3 grid, and each position can be either 'X', 'O', or None (empty).
    """

    def __init__(self) -> None:
        """Initialize the board with an empty state."""
        self._cells: list[list[PlayerMark | None]] = [
            [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]

    def reset(self) -> None:
        """Reset the board to its initial empty state."""
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                self._cells[row][column] = None

    def make_move(self, row: int, column: int, player: PlayerMark) -> bool:
        """Make a move on the board for the given player ('X' or 'O') at the specified position.

        Args:
            row (int): The row index (0-2) where the player wants to place their mark.
            column (int): The column index (0-2) where the player wants to place their mark.
            player (PlayerMark): The player's mark, either 'X' or 'O'.
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.is_position_available(row, column):
            self._cells[row][column] = player
            return True
        return False

    def get_available_positions(self) -> list[tuple[int, int]]:
        """Get a list of available positions on the board.

        Returns:
            list[tuple[int, int]]: A list of tuples representing the available positions (row, col).
        """
        return [
            (row, column)
            for row, column in BOARD_POSITIONS
            if self.is_position_available(row, column)
        ]

    def get_current_state(self) -> list[list[PlayerMark | None]]:
        """Get a copy of the current board state.

        Returns:
            list[list[PlayerMark | None]]: A 3x3 list representing the current board state.
        """
        return [row.copy() for row in self._cells]

    def get_mark(self, row: int, column: int) -> PlayerMark | None:
        """Return the mark stored at one board position."""
        if not self.contains_position(row, column):
            return None

        return self._cells[row][column]

    def contains_position(self, row: int, column: int) -> bool:
        """Return whether a row and column are inside the board."""
        return 0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE

    def is_position_available(self, row: int, column: int) -> bool:
        """Return whether a board position exists and is empty."""
        return (
            self.contains_position(row, column)
            and self._cells[row][column] is None
        )

    @property
    def move_count(self) -> int:
        """Return the number of marks placed on the board."""
        return sum(cell is not None for row in self._cells for cell in row)

    def copy(self) -> "Board":
        """Return an independent copy of the board."""
        copied_board = Board()
        copied_board._cells = self.get_current_state()
        return copied_board




    def get_winner(self) -> PlayerMark | None:
        """Get the winner of the game, if one exists.

        Returns:
        PlayerMark | None: The winning mark, or None if there is no winner.
        """
        for line in WINNING_LINES:
            first_row, first_column = line[0]
            first_mark = self._cells[first_row][first_column]
            if first_mark is not None and all(
                self._cells[row][column] == first_mark for row, column in line[1:]
            ):
                return first_mark

        return None

    def is_full(self) -> bool:
        """Check whether the board has no available positions.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        return self.move_count == BOARD_AREA

    def is_draw(self) -> bool:
        """Return whether the board is full without a winner."""
        return self.is_full() and self.get_winner() is None


    def is_game_over(self) -> bool:
        """Check whether the game has ended.

        Returns:
            bool: True if there is a winner or the board is full, False otherwise.
        """
        return self.get_winner() is not None or self.is_draw()
