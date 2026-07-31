# Maze Solver (A* / BFS)

## Table of Contents
- [Maze Solver (A\* / BFS)](#maze-solver-a--bfs)
  - [Table of Contents](#table-of-contents)
  - [About the project](#about-the-project)
  - [Getting started](#getting-started)
  - [Requirements](#requirements)
    - [Maze file format](#maze-file-format)
  - [How to run](#how-to-run)
    - [Windows](#windows)
    - [Linux / macOS](#linux--macos)
  - [Arguments](#arguments)
  - [File structure](#file-structure)
  - [Edits](#edits)

## About the project

An object-oriented maze solver that finds the shortest path from the top-left
cell `(0, 0)` to the target using either A* or Breadth-First Search, with
8-directional movement and uniform step cost.

## Getting started
To get started, install Python 3.10 or newer.

## Requirements

- Python 3.10 or newer (uses modern type-hint syntax).
- A .txt file containing a maze in the format specified at [Maze file format](#maze-file-format).

### Maze file format

The maze is a text file containing a matrix of integers separated by
whitespace, one row per line:

- `0`  — wall/obstacle (not walkable)
- `1`  — free path (walkable)
- `-1` — target cell

The agent always starts at the top-left cell `(0, 0)`.

## How to run

Run the program as a module from the project root (the directory that
contains the `src/` folder).

### Windows

```bat
:: Default maze (data\input_lab256.txt) with A*
python -m main

:: Choose the algorithm: astar (default) or bfs
python -m main -a bfs

:: Pass a specific maze file
python -m main path\to\maze.txt

:: File + algorithm
python -m main path\to\maze.txt -a bfs
```

### Linux / macOS

```bash
# Default maze (data/input_lab256.txt) with A*
python3 -m main

# Choose the algorithm: astar (default) or bfs
python3 -m main -a bfs

# Pass a specific maze file
python3 -m main path/to/maze.txt

# File + algorithm
python3 -m main path/to/maze.txt -a bfs
```

If no text file is provided, the program will look for the default maze file
`data/input_lab256.txt`. If a file is provided but not found, the program will look for a file with the same name inside the `data/` directory.

## Arguments

| Argument            | Description                                                        | Default              |
| ------------------- | ------------------------------------------------------------------ | -------------------- |
| `file` (positional) | Path to the maze `.txt` file. Optional.                            | `data/input_lab256.txt` |
| `-a`, `--algorithm` | Search algorithm to use: `astar` or `bfs`.                         | `astar`              |

## File structure

```
project
├── data/
│   └── input_lab256.txt   # Sample maze file
├── src/
│   ├── __init__.py       # Package definition
│   ├── main.py           # Entry point: CLI arguments and program execution
│   ├── maze.py           # Maze environment (grid, cell rules, shared moves)
│   ├── search_node.py    # SearchNode: a single position in the search
│   ├── astar.py          # AStar search strategy (Chebyshev heuristic)
│   ├── bfs.py            # BFS search strategy
│   └── agent.py          # RobotAgent: picks and runs a strategy
├── .gitignore
├── LICENSE
├── main.py # Entry point for running the program as a script
└── README.md
```

## Edits
This section describes briefly what each directory and file is responsible for:

- `src/__init__.py`: defines the package and its modules.
- `main.py`: entry point of the program, handles CLI arguments and runs the agent.
- `src/maze.py`: defines the `Maze` class, which represents the maze environment, including the grid, cell rules, and shared moves.
- `src/search_node.py`: defines the `SearchNode` class, which represents a single position in the search process.
- `src/astar.py`: implements the A* search strategy, using the Chebyshev heuristic for 8-directional movement.
- `src/bfs.py`: implements the Breadth-First Search (BFS) strategy.
- `src/agent.py`: defines the `RobotAgent` class, which selects and runs a search strategy (A* or BFS) over the maze.
- `data/input_lab256.txt`: a sample maze file used for testing and demonstration purposes.
