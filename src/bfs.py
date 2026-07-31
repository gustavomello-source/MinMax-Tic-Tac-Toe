"""Breadth-first search strategy for the maze.

This module defines :class:`BFS`, a breadth-first search over a
:class:`~src.maze.Maze`. The agent starts at the top-left cell ``(0, 0)`` and
searches for the target using 8-directional movement with uniform step cost.
"""

from __future__ import annotations

from collections import deque

from src.maze import FREE, MOVES, VISITED, Maze
from src.search_node import SearchNode


class BFS:
    """Breadth-first search strategy over a maze.

    Provides the same interface as :class:`~src.astar.AStar` so the two can
    be used interchangeably by the agent.

    Attributes:
        maze (Maze): The :class:`~src.maze.Maze` the strategy searches through.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize the strategy with the maze to search.

        Args:
            maze: The maze environment to explore.
        """
        self.maze: Maze = maze

    def search(self) -> tuple[int | None, int]:
        """Run the breadth-first search from the start cell to the target.

        Returns:
            A tuple ``(steps, loops_executed)`` where ``steps`` is the length
            of the shortest path to the target (or ``None`` if no path
            exists), and ``loops_executed`` is the number of main-loop
            iterations performed.
        """
        start_position: tuple[int, int] = (0, 0)

        start_value: int = self.maze.matrix[0][0]
        if start_value not in (FREE, VISITED):
            return None, 0

        start_node = SearchNode(position=start_position, steps=0, total_cost=0)

        # FIFO queue of nodes to explore, in discovery order.
        frontier: deque[SearchNode] = deque([start_node])

        # Cells already discovered, to avoid enqueuing them twice.
        discovered: set[tuple[int, int]] = {start_position}

        self.maze.mark_visited(row=0, column=0)

        loops_executed: int = 0

        while frontier:
            current_node: SearchNode = frontier.popleft()

            loops_executed += 1

            current_position: tuple[int, int] = current_node.position

            if current_position == self.maze.target:
                return current_node.steps, loops_executed

            current_row, current_column = current_position

            for row_offset, column_offset in MOVES:
                next_row: int = current_row + row_offset
                next_column: int = current_column + column_offset
                next_position: tuple[int, int] = (next_row, next_column)

                # Skip cells already discovered.
                if next_position in discovered:
                    continue

                # Must be inside the maze, walkable, and not a wall.
                if not self.maze.is_valid_position(row=next_row, column=next_column):
                    continue

                discovered.add(next_position)
                self.maze.mark_visited(row=next_row, column=next_column)

                next_node = SearchNode(
                    position=next_position,
                    steps=current_node.steps + 1,
                    total_cost=0,
                )
                frontier.append(next_node)

        # The frontier is empty: no path to the target exists.
        return None, loops_executed
