"""Search node used by the A* algorithm.

This module defines :class:`SearchNode`, which describes a
single position reached during the A* search along with its cost information.
"""

from __future__ import annotations


class SearchNode:
    """A single node explored during the search.

    Each node stores the cost accumulated to reach it (``g``) and the total
    estimated cost through it (``f = g + h``), where ``h`` is the heuristic
    estimate to the target.

    Attributes:
        position (tuple[int, int]): ``(row, column)`` position represented by this node.
        steps (int): Number of steps taken from the start to this node. This is
            the ``g(n)`` value of the A* algorithm.
        total_cost (float): Total estimated cost ``f(n) = g(n) + h(n)`` used to
            prioritize the node in the search frontier.
    """

    def __init__(
        self, position: tuple[int, int], steps: int, total_cost: float
    ) -> None:
        """Initialize a search node.

        Args:
            position (tuple[int, int]): ``(row, column)`` position of the node.
            steps (int): Cost to reach the node from the start (``g(n)``).
            total_cost (float): Estimated total cost through the node (``f(n)``).
        """
        self.position: tuple[int, int] = position
        self.steps: int = steps
        self.total_cost: float = total_cost

    def __str__(self) -> str:
        """Return a concise human-readable representation of the node."""
        return (
            f"SearchNode("
            f"position={self.position}, "
            f"steps={self.steps}, "
            f"total_cost={self.total_cost:.2f}"
            f")"
        )
