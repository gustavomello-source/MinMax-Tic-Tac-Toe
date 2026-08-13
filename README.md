# MinMax Tic Tac Toe

A Tic Tac Toe game built with Python and Pygame. The human player uses `X`, and
a depth-aware MinMax opponent uses `O` to choose outcome-optimal moves.

## Requirements

- Python 3.12 or later
- [UV](https://docs.astral.sh/uv/)

## Installation

Clone the repository, enter its directory, and synchronize the project and
development dependencies:

```bash
git clone <REPOSITORY_URL>
cd MinMax-Tic-Tac-Toe
uv sync --extra dev
```

## Running the game

Start the installed package through its module entry point:

```bash
uv run python -m tictactoe
```

Controls:

- Left-click an empty cell to play as `X`.
- Press `R` to reset the game.
- Close the window to exit.

The window title reports whose turn it is and the final result. After a human
move, the MinMax opponent plays automatically.

## Development checks

Run the complete test suite:

```bash
uv run pytest
```

Run the configured Ruff checks:

```bash
uv run ruff check src tests
```

Generate a coverage report:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

## Architecture

The code separates game rules from decision-making and presentation:

- `Board` owns cell state, legal positions, winning lines, and terminal-state
  queries.
- `TicTacToeGame` coordinates turns, accepted moves, resets, and game status.
- `MoveSelector` defines the opponent-selection boundary; `MinMax` implements it.
- `BoardLayout` maps window coordinates to board positions.
- `BoardRenderer` defines the drawing boundary; `PygameBoardRenderer` implements
  it.
- `TitleFormatter` defines the status-title boundary; `GameTitleFormatter`
  implements it.
- `PygameApp` owns the Pygame lifecycle and translates input events into game
  operations.
- `main.create_app` is the composition root that connects the Pygame application
  to the MinMax opponent.

This division keeps domain rules independent of Pygame and allows UI and opponent
implementations to be injected without changing the game model.

## Project structure

```text
src/tictactoe/
├── __main__.py
├── main.py
├── ai/
│   └── minmax.py
├── game/
│   ├── board.py
│   ├── game.py
│   ├── game_status.py
│   ├── move_selector.py
│   └── player_mark.py
└── ui/
    ├── board_layout.py
    ├── board_renderer.py
    ├── board_renderer_protocol.py
    ├── game_title_formatter.py
    ├── pygame.py
    └── title_formatter.py

tests/
├── test_board.py
├── test_board_layout.py
├── test_board_renderer.py
├── test_game.py
├── test_game_status.py
├── test_game_title_formatter.py
├── test_main.py
├── test_minmax.py
├── test_player_mark.py
└── test_pygame.py
```

The detailed rationale and incremental change record are maintained in
[`TECHNICAL_HISTORY.md`](TECHNICAL_HISTORY.md).

## License

This project is distributed under the terms in [`LICENSE`](LICENSE).
