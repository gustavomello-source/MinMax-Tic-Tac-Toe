"""A* search strategy for the maze.

This module defines :class:`AStar`, an implementation of the A* pathfinding
algorithm over a :class:`~src.maze.Maze`. The agent starts at the top-left
cell ``(0, 0)`` and searches for the target cell using 8-directional
movement with uniform step cost.
"""

from __future__ import annotations

import heapq

from src.maze import FREE, MOVES, VISITED, Maze
from src.search_node import SearchNode


class AStar:
    """A* pathfinding strategy over a maze.

    Attributes:
        maze (Maze): The :class:`~src.maze.Maze` the strategy searches through.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize the strategy with the maze to search.

        Args:
            maze (Maze): The maze environment to explore.
        """
        self.maze: Maze = maze

    def heuristic(self, position: tuple[int, int]) -> int:
        """Estimate the remaining cost from a position to the target using
        Chebyshev distance.

        Args:
            position (tuple[int, int]): ``(row, column)`` position to estimate from.

        Returns:
            The Chebyshev distance from ``position`` to the target.

        Raises:
            ValueError: If the maze has no target defined.
        """
        if self.maze.target is None:
            raise ValueError("Maze has no target defined")

        current_row, current_column = position
        target_row, target_column = self.maze.target

        row_difference: int = abs(current_row - target_row)
        column_difference: int = abs(current_column - target_column)

        return max(row_difference, column_difference)

    def search(self) -> tuple[int | None, int]:
        """Run the A* search from the start cell to the target.

        The search closes cells only when they are popped from the frontier
        and keeps track of the best-known cost to reach each cell, so the
        returned step count is the shortest possible.

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

        start_steps: int = 0
        start_heuristic: int = self.heuristic(start_position)
        start_total_cost: int = start_steps + start_heuristic

        start_node = SearchNode(
            position=start_position,
            steps=start_steps,
            total_cost=start_total_cost,
        )

        # Priority queue entries: (total_cost, steps, tie_breaker, node).
        frontier: list[tuple[float, int, int, SearchNode]] = []

        # Tie-breaker to keep heap ordering stable when costs match.
        tie_breaker: int = 0

        # Best-known cost (g score) to reach each position.
        best_steps: dict[tuple[int, int], int] = {start_position: start_steps}

        # Positions finalized with their shortest cost.
        closed: set[tuple[int, int]] = set()

        self.maze.mark_visited(row=0, column=0)

        heapq.heappush(
            frontier,
            (start_node.total_cost, start_node.steps, tie_breaker, start_node),
        )

        loops_executed: int = 0

        while frontier:
            _, current_steps, _, current_node = heapq.heappop(frontier)

            loops_executed += 1

            current_position: tuple[int, int] = current_node.position

            # Skip stale entries: a cheaper path to this cell was already
            # popped and finalized.
            if current_position in closed:
                continue

            # Skip entries superseded by a better path found after pushing current_node.
            if current_steps > best_steps.get(current_position, current_steps):
                continue

            # Finalize this cell with its shortest known cost.
            closed.add(current_position)

            if current_position == self.maze.target:
                return current_node.steps, loops_executed

            current_row, current_column = current_position

            for row_offset, column_offset in MOVES:
                next_row: int = current_row + row_offset
                next_column: int = current_column + column_offset
                next_position: tuple[int, int] = (next_row, next_column)

                # Next position is already finalized with its shortest cost, so skip it.
                if next_position in closed:
                    continue

                # Must be inside the maze, walkable, and not a wall.
                if not self.maze.is_valid_position(row=next_row, column=next_column):
                    continue

                next_steps: int = current_node.steps + 1

                # Only proceed if this path to the neighbor is cheaper than
                # any path found so far.
                if next_steps >= best_steps.get(next_position, float("inf")):
                    continue

                best_steps[next_position] = next_steps

                next_heuristic: int = self.heuristic(position=next_position)
                next_total_cost: int = next_steps + next_heuristic

                next_node = SearchNode(
                    position=next_position,
                    steps=next_steps,
                    total_cost=next_total_cost,
                )

                self.maze.mark_visited(row=next_row, column=next_column)

                tie_breaker += 1
                heapq.heappush(
                    frontier,
                    (
                        next_node.total_cost,
                        next_node.steps,
                        tie_breaker,
                        next_node,
                    ),
                )

        # The frontier is empty: no path to the target exists.
        return None, loops_executed
