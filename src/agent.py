"""Agent that executes a search strategy over the maze.

This module defines :class:`RobotAgent`, which selects a search strategy
(A* or BFS), runs it, and records how many main-loop iterations were needed to
reach the target.
"""

from __future__ import annotations

from src.astar import AStar
from src.bfs import BFS
from src.maze import Maze

# Map to each available search strategy class by its name.
STRATEGIES: dict[str, type] = {
    "astar": AStar,
    "bfs": BFS,
}


class RobotAgent:
    """Agent that runs a search strategy over a maze.

    The agent always starts at the top-left cell ``(0, 0)`` and delegates the
    pathfinding to the selected strategy (A* or BFS).

    Attributes:
        maze (Maze): The maze the agent explores.
        algorithm (str): Name of the selected search algorithm.
        start_position (tuple[int, int]): The agent's starting cell, always ``(0, 0)``.
        loops_executed (int): Number of main-loop iterations performed by the last
            search run.
    """

    def __init__(self, maze: Maze, algorithm: str = "astar") -> None:
        """Initialize the agent with the maze and the algorithm to use.

        Args:
            maze (Maze): The maze environment the agent will search.
            algorithm (str): Name of the search algorithm to use, either
                ``"astar"`` or ``"bfs"``.

        Raises:
            ValueError: If ``algorithm`` is not a known strategy.
        """
        if algorithm not in STRATEGIES:
            known: str = ", ".join(sorted(STRATEGIES))
            raise ValueError(f"Unknown algorithm {algorithm!r}. Choose one of: {known}")

        self.maze: Maze = maze
        self.algorithm: str = algorithm
        self.start_position: tuple[int, int] = (0, 0)
        self.loops_executed: int = 0

    def run(self) -> int | None:
        """Execute the selected search and record the loop count.

        Returns:
            The length of the shortest path to the target, or ``None`` if no
            path exists.
        """
        strategy = STRATEGIES[self.algorithm](self.maze)

        steps, loops = strategy.search()

        self.loops_executed = loops

        return steps
