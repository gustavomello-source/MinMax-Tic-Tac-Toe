"""Entry point for the maze solver.

Loads a maze from a text file, runs the chosen search algorithm from the
top-left cell to the target, and prints the resulting shortest path length and
the number of main-loop iterations performed.

Usage:
    python -m src.main [file] [-a {astar,bfs}]

If ``file`` is not found as given, the solver looks for a file with the same
base name inside the package ``data`` directory. If no path is provided, the
default ``data/input_lab256.txt`` is used. When no maze file can be resolved,
the program prints an error and exits with a non-zero status.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.agent import RobotAgent
from src.maze import Maze

# Directory bundled with the package holding the data
DATA_DIR: Path = Path(__file__).resolve().parent / "data"

# Default maze file used when no path is given on the command line.
DEFAULT_MAZE_PATH: Path = DATA_DIR / "input_lab256.txt"


def resolve_maze_path(file_arg: str | None) -> Path:
    """Resolve the maze file path, falling back to the data directory.

    Args:
        file_arg (str | None): Path passed on the command line, or ``None`` if omitted.

    Returns:
        The resolved path to an existing maze file.

    Raises:
        FileNotFoundError: If no maze file can be found through any of the
            resolution steps.
    """
    if file_arg is None:
        if DEFAULT_MAZE_PATH.is_file():
            return DEFAULT_MAZE_PATH
        raise FileNotFoundError(f"Default maze file not found: {DEFAULT_MAZE_PATH}")

    given_path = Path(file_arg)
    if given_path.is_file():
        return given_path

    # Fall back to a file with the same given name inside the data directory.
    fallback_path: Path = DATA_DIR / given_path.name
    if fallback_path.is_file():
        return fallback_path

    raise FileNotFoundError(
        f"Maze file not found: {file_arg} (also looked for "
        f"{given_path.name!r} in {DATA_DIR})"
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        The parsed arguments namespace with ``file`` (optional path) and
        ``algorithm`` (``"astar"`` or ``"bfs"``).
    """
    parser = argparse.ArgumentParser(
        description="Solve a given maze with A* or BFS search."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help=(
            "Path to the maze .txt file. If not found, the solver looks for the file"
            "inside the data directory or fallback to the default."
        ),
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        choices=["astar", "bfs"],
        default="astar",
        help="Search algorithm to use between astar and bfs (default: astar).",
    )
    return parser.parse_args()


def main() -> None:
    """Parse arguments, load the maze, run the search, and print results."""
    args = parse_arguments()

    try:
        maze_path: Path = resolve_maze_path(file_arg=args.file)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        sys.exit(1)

    print(f"Starting maze solver ({args.algorithm})")

    try:
        maze = Maze()
        maze.load_from_file(file_path=str(object=maze_path))

        print(maze)

        agent = RobotAgent(maze, algorithm=args.algorithm)
        steps: int | None = agent.run()

        if steps is not None:
            print("Target found.")
            print(f"Steps: {steps}.")
            print(f"Loops executed: {agent.loops_executed}")
        else:
            print("No path found.")
            print(f"Loops executed: {agent.loops_executed}")

    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
