"""Maze environment for the A* search.

This module defines the :class:`Maze` class, which represents the grid-based
environment the agent explores. The maze is loaded from a plain-text file
containing a matrix of integers with the following cell conventions:

- ``0``  : wall (not walkable)
- ``1``  : free path (walkable)
- ``-1`` : target cell (must be the bottom-right cell of the matrix)
- ``255``: cell already visited during the search

Also provides the global list of 8-directional moves (row change, column change)
for the agent, since it is used by both A* and BFS.
"""

from __future__ import annotations

# Cell value conventions used throughout the maze, used by both A* and BFS.
WALL: int = 0
FREE: int = 1
TARGET: int = -1
VISITED: int = 255

# Global list of 8-directional moves (row change, column change) for the agent, since it
# is used on both A* and BFS.
MOVES: list[tuple[int, int]] = [
    (-1, 0),  # up
    (1, 0),  # down
    (0, -1),  # left
    (0, 1),  # right
    (-1, -1),  # up-left
    (-1, 1),  # up-right
    (1, -1),  # down-left
    (1, 1),  # down-right
]


class Maze:
    """Grid-based maze environment.

    Responsible for loading the matrix from a file, storing its dimensions,
    validating positions, and marking cells as visited during the search.

    Attributes:
        matrix (Maze): The maze grid as a list of rows, each a list of ``int``.
        target (tuple[int, int] | None): ``(row, column)`` position of the target cell, or ``None``
            while no file has been loaded yet.
        height (int): Number of rows in the matrix.
        width (int): Number of columns in the matrix.
    """

    def __init__(self) -> None:
        """Initialize an empty maze with no matrix loaded."""
        self.matrix: list[list[int]] = []
        self.target: tuple[int, int] | None = None
        self.height: int = 0
        self.width: int = 0

    def __str__(self) -> str:
        """Return a concise human-readable summary of the maze."""
        return f"Maze(height={self.height}, width={self.width}, target={self.target})"

    def load_from_file(self, file_path: str) -> None:
        """Load the maze matrix from a text file.

        Each non-empty line of the file is parsed into a row of integers
        separated by whitespace. The target cell is expected to be the
        bottom-right cell and must hold the value ``-1``.

        Args:
            file_path (str): Path to the text file containing the maze matrix.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or the bottom-right cell is
                not the target (``-1``).
        """
        with open(file_path, "r", encoding="utf-8") as file:
            file_lines: list[str] = file.readlines()

        matrix: list[list[int]] = []

        # Convert each non-empty line into a list of integers.
        for line in file_lines:
            if not line.strip():
                continue

            parsed_row: list[int] = [int(value) for value in line.split()]
            matrix.append(parsed_row)

        if not matrix:
            raise ValueError("File is empty or contains no rows")

        self.matrix = matrix
        self.height = len(matrix)
        self.width = len(matrix[0])

        # The target can be anywhere in the maze
        target_row: int | None = None
        target_column: int | None = None

        for row in range(self.height):
            for column in range(self.width):
                if self.matrix[row][column] == TARGET:
                    target_row = row
                    target_column = column
                    break
        if target_row is None or target_column is None:
            raise ValueError("Maze has no target cell (-1) defined")

        self.target = (target_row, target_column)

    def is_valid_position(self, row: int, column: int) -> bool:
        """Check whether a position can be entered by the agent.

        A position is valid when it lies within the matrix bounds and its
        value is either a free path (``1``) or the target (``-1``).

        Args:
            row: Row index of the position.
            column: Column index of the position.

        Returns:
            ``True`` if the position is inside the maze and walkable,
            ``False`` otherwise.
        """
        if row < 0 or row >= self.height:
            return False

        if column < 0 or column >= self.width:
            return False

        value: int = self.matrix[row][column]

        return value == FREE or value == TARGET

    def mark_visited(self, row: int, column: int) -> None:
        """Mark a free cell as visited.

        Only free cells (``1``) are marked; walls, the target, and cells
        already visited are left unchanged.

        Args:
            row: Row index of the cell to mark.
            column: Column index of the cell to mark.
        """
        if self.matrix[row][column] == FREE:
            self.matrix[row][column] = VISITED
