# Technical Development History

This document records the verified technical evolution of the `feature/pygame`
branch. It explains what changed, why each group of changes was necessary, which
commits introduced it, and what remains incomplete. Git history and automated
tests remain the authoritative implementation record.

## Original Baseline

The branch started from `da3b38d feat(ai): implement MinMax algorithm`.

At that point:

- `Board` represented a 3×3 grid and exposed moves, available positions, winner
  detection, fullness, reset, and game-over queries.
- `PlayerMark` represented X and O.
- `MinMax` selected optimal outcome moves using recursive board copies.
- Tests covered common Board and MinMax behavior.
- There was no game controller responsible for turns.
- There was no working application entry point or Pygame interaction loop.
- The README documented `python -m tictactoe`, but the package had no
  `__main__.py`.
- UI, game-flow, and AI integration responsibilities were not yet defined.

## Resulting Architecture

The completed changes established these responsibility boundaries:

```text
tictactoe.__main__
        |
        v
main.py (composition root)
        |
        v
PygameApp -----------------> TitleFormatter
    |  |                       ^
    |  +-------------------- GameTitleFormatter
    |
    +----------------------> BoardRenderer
    |                          ^
    |                          |
    |                    PygameBoardRenderer
    |
    +----------------------> MoveSelector
    |                          ^
    |                          |
    |                        MinMax
    |
    v
TicTacToeGame
    |
    v
Board
```

Responsibilities:

- `Board`: board state, positions, move availability, winner/draw evaluation,
  copying, and board-level queries.
- `TicTacToeGame`: current player, turn progression, reset, lifecycle status,
  winner exposure, and delegated move execution.
- `MinMax`: move selection and recursive scoring only.
- `BoardLayout`: conversion between screen coordinates and board positions.
- `PygameBoardRenderer`: all Pygame board drawing.
- `GameTitleFormatter`: game-state title text.
- `PygameApp`: Pygame lifecycle, input orchestration, and delegation.
- `main.py`: concrete dependency composition.

## Completed Changes

### 1. Runnable Pygame Application

- Added Pygame as a runtime dependency and generated `uv.lock`.
- Added the initial Pygame window, grid, and X/O rendering.
- Added `tictactoe.__main__` so the supported command is:

  ```bash
  uv run python -m tictactoe
  ```

- Centralized execution in `main.py`; direct source-file execution is not the
  supported `src`-layout workflow.
- Restored and standardized absolute package imports after execution failures
  revealed top-level `game` and `ui` imports were incorrect.

Why: package execution must match the documented installation model and must not
depend on the current working directory.

### 2. Turn-Based Game Controller

- Added `TicTacToeGame` between the UI and `Board`.
- Added starting-player and current-player state.
- Added turn alternation after valid moves.
- Preserved the current turn after invalid moves.
- Rejected moves after a win or draw.
- Added reset behavior that restores the configured starting player.
- Added delegated move selection through `MoveSelector`.
- Added early termination so a selector is not asked to search after game over.
- Covered selectors returning no move or an invalid occupied position.

Why: Pygame should translate user input, while the game controller owns game
progression and legality.

### 3. Human and Computer Player Integration

- Added the `MoveSelector` protocol.
- Verified that `MinMax` satisfies it structurally.
- Injected an optional opponent selector into `PygameApp`.
- Triggered one opponent move after a valid human click.
- Configured `MinMax(PlayerMark.O)` at the composition root.
- Added explicit `human_player` configuration.
- Restricted mouse clicks to the human player's turn.
- Added computer-first support when the human controls O.
- Restored the computer opening move after reset in human-O games.

Why: game/UI code depends on a move-selection abstraction, while concrete MinMax
construction remains at the application boundary.

### 4. Board Layout and Input Mapping

- Added immutable `BoardLayout`.
- Added screen-coordinate to `(row, column)` mapping.
- Centralized cell width and height calculations.
- Made window dimensions, grid geometry, mark geometry, and click mapping use the
  same layout.
- Added layout injection.
- Rejected dimensions smaller than the board.
- Required dimensions to divide evenly by the board size.
- Removed a redundant mapped-cell bounds check after those invariants were
  established.

Why: a single geometry owner prevents input and rendering from disagreeing and
supports non-default, including non-square, layouts predictably.

### 5. Rendering SRP

- Renamed `PyGameBoard` to `PygameApp` because it owns the application lifecycle,
  not merely a board.
- Extracted `PygameBoardRenderer`.
- Incrementally moved grid, X, O, mark traversal, background, and full board
  composition into the renderer.
- Made `PygameApp` decide when to draw while the renderer decides how.
- Added renderer injection.
- Added `BoardRenderer` protocol and changed `PygameApp` to depend on it.
- Aligned injected renderer and application layouts.
- Adopted the renderer's layout when no application layout is supplied.
- Rejected conflicting renderer/application layouts.

Why: rendering changes should not modify input, lifecycle, or domain code. The
protocol permits substitution without coupling the app to a concrete renderer.

### 6. Game Feedback and Reset Interaction

- Added R-key reset behavior.
- Added current-player, winner, and draw window-title feedback.
- Extracted reset orchestration into `_reset_game()`.
- Separated pure title construction from the Pygame caption side effect.
- Extracted `GameTitleFormatter` with a configurable base title.
- Delegated title construction from `PygameApp` to the formatter.
- Moved winner/draw formatting tests to the formatter and removed duplicate app
  cases.

Why: game-state text is presentation formatting, while setting the native window
caption is a Pygame side effect.

### 7. Board Encapsulation and Domain Vocabulary

- Renamed public-looking `Board.board` storage to private `_cells`.
- Added `Board.copy()` and migrated MinMax away from generic `deepcopy`.
- Added `get_mark()`, `contains_position()`, and `is_position_available()`.
- Reused these queries in moves, mark lookup, and available-position queries.
- Added `move_count`, `BOARD_AREA`, `BOARD_POSITIONS`, and `WINNING_LINES`.
- Reused `BOARD_POSITIONS` in reset, available-position queries, and rendering.
- Added `BoardPosition` and migrated Board, `MoveSelector`, MinMax, and
  `BoardLayout` annotations.
- Standardized `column` rather than `col`, plus descriptive iteration names.
- Changed `PlayerMark` to Python 3.12 `StrEnum`.
- Added `PlayerMark.opponent` and removed duplicate opponent helpers from the game
  controller and MinMax.

Why: state should remain encapsulated, repeated rules should have one owner, and
domain types/names should communicate intent across layers.

### 8. Winner, Draw, and Lifecycle Modeling

- Defined the eight immutable winning lines.
- Replaced separate row, column, and diagonal branches with line iteration.
- Simplified line equality evaluation without temporary count lists.
- Added `Board.is_draw()` and used it in Board, MinMax, and UI logic.
- Added `GameStatus` with `IN_PROGRESS`, `WON`, and `DRAW`.
- Added `TicTacToeGame.status`, `winner`, and `is_over`.
- Migrated move guards and UI status branching to these controller properties.

Why: named lifecycle concepts prevent each consumer from independently inferring
game state and producing inconsistent rules.

### 9. MinMax Coherence and Search Quality

- Replaced generic deep copies with `Board.copy()`.
- Added depth-aware terminal scores.
- MinMax now prefers quicker forced wins.
- MinMax delays unavoidable losses.
- Extracted move simulation, terminal scoring, move evaluation, and available-move
  scoring helpers.
- Incrementally migrated top-level, maximizing, and minimizing paths to the same
  helpers.
- Simplified maximizing/minimizing reductions to `max()`/`min()` over shared move
  scores.
- Added direct coverage for active, winning, losing, and drawn terminal scores.

Why: all hypothetical-move paths should use identical mechanics, while depth-aware
scores make equally optimal outcomes behave naturally.

### 10. Test Structure and Verification

- Added focused suites for game flow, player marks, layout, renderer, Pygame app,
  composition root, lifecycle status, and title formatting.
- Added integration coverage between `TicTacToeGame` and MinMax.
- Added negative-path coverage for invalid, unavailable, and terminal selected
  moves.
- Added rendering tests using Pygame surfaces rather than visual assumptions.
- Removed duplicate title-format cases after formatter extraction.
- Used SDL dummy drivers for headless Pygame verification.
- Ran focused Pytest and Ruff checks for every atomic increment.

Why: tests should follow responsibility boundaries and verify behavior without
requiring a physical display.

## Important Decisions and Tradeoffs

### `uv run` is the supported local runner

The project uses a `src` layout. Running `python3 src/tictactoe/main.py` bypasses
installed-package resolution and is not supported. `uv run` supplies the project
environment and resolves the `tictactoe` package correctly.

### `Board` remains mutable but encapsulated

The game and MinMax need efficient incremental moves. Rather than replacing Board
with an immutable value object, state is private and copies are explicit through
`Board.copy()`.

### Protocols are introduced only at substitution boundaries

`MoveSelector` and `BoardRenderer` exist because multiple implementations or test
doubles are useful. A title formatter protocol is the current in-progress step for
the same reason. Internal helpers do not receive protocols merely for style.

### Pygame does not own rules

Mouse and keyboard events are translated into controller operations. Turn changes,
terminal rejection, reset state, and selected-move application stay outside raw
Pygame handling.

### MinMax is outcome-optimal and depth-sensitive

Depth changes preference between outcomes of the same category. It does not make a
loss preferable to a draw or a draw preferable to a win.

## Current In-Progress State

At this checkpoint, `HEAD` is:

```text
9c421f7 refactor(ui): depend on board renderer abstraction
```

The worktree contains one uncommitted file:

```text
src/tictactoe/ui/title_formatter.py
```

That file defines the pending `TitleFormatter` protocol. It has passed an import
check and Ruff, but it is not completed or committed work yet.

Expected commit when resumed:

```text
refactor(ui): define title formatter abstraction
```

## Remaining Implementation Work

The following work was identified but had not been completed at this checkpoint:

1. Commit the pending `TitleFormatter` protocol.
2. Change only the injected `PygameApp.title_formatter` annotation from concrete
   `GameTitleFormatter` to `TitleFormatter`; keep `GameTitleFormatter` as default.
3. Run the entire Pytest suite.
4. Run Ruff across `src` and `tests`.
5. Run `git diff --check` and inspect the worktree for untracked or stale files.
6. Perform one bounded architecture review against the responsibility table above.
7. Remove only verified dead code or obsolete placeholders, each atomically.
8. Update README installation, UV execution, controls, architecture, and current
   file structure.
9. Launch the complete app headlessly through:

   ```bash
   uv run python -m tictactoe
   ```

10. Finish when the worktree is clean, all checks pass, documentation matches the
    implementation, and no responsibility boundary above is violated.

Additional changes should be supported by a failing test, verified defect, or new
project requirement.

## Atomic Commit Ledger

The complete branch history remains the authoritative line-by-line record. The
following ledger groups every completed atomic increment by purpose while retaining
the boundary commits that formed each phase.

### Application and initial Pygame slice

- `0a8d8d2` add Pygame board window.
- `b0ae678` add turn-based game controller.
- `01de274` add board coordinate mapping.
- `8613f9e` connect Pygame to the controller.
- `c6f7a29` use absolute UI imports.
- `5af6e4c` add the package module entry point.
- `1ed8cfd` centralize module execution.
- `653fa8a` inject board layout.
- `35ec859` handle board mouse clicks.

### Shared geometry and basic interaction

- `6b0f660` centralize cell dimensions.
- `6e0624f`, `f6ae322`, `3fb5575` migrate grid, X, and O geometry.
- `f8a9b95` remove obsolete geometry constants.
- `2d726c6` derive window size from layout.
- `58290e0` reset with keyboard input.
- `076c492`, `cb04a88`, `98acbec` add current-player, winner, and draw titles.

### Renderer extraction and AI wiring

- `5c72cbb` rename the UI class to `PygameApp`.
- `a0b9ddd`, `f869757`, `c3974f6`, `4f76270`, `abe1e4e` extract and encapsulate
  complete rendering.
- `60fcbd3` add delegated move selection.
- `a5dc29e` verify MinMax integration.
- `2aa82b6`, `72a2c4d`, `8c387f1` inject, execute, and compose the opponent.
- `c86ed3b`, `b0b6b10` configure the human and restrict clicks.
- `6284728`, `910d02c`, `2a79aa3` handle opponent turns, opening moves, and reset.

### Domain and import coherence

- `a3f7f3a`, `3291096`, `45053f9` centralize opponent marks.
- `ce9aab9`, `6b4b3d4`, `cdf660f` standardize absolute imports.
- `fa16c53`, `3919be6`, `3e60c6a`, `925c3fc`, `c2a2874`, `a59474f` simplify
  Board/MinMax implementation and naming.

### Board API and rules

- `a1f5eef`, `28998a2` add and adopt Board copying.
- `7d90665`, `001821f` add direct mark queries and adopt them in rendering.
- `a6edcd0`, `5072e09`, `8bd7178` centralize bounds validation.
- `22b3c1c`, `2e3ae90`, `7ae8677` centralize position availability.
- `e1543f7`, `7324087`, `042ad50` define and evaluate winning lines.
- `9c62b05`, `939f282`, `d907d2f`, `0fe8502` define and adopt draw state.

### Lifecycle controller

- `85cbdeb`, `6e01ffe`, `0c103e0` define and cover lifecycle status.
- `a9853bc`, `b479215` adopt lifecycle status in game and UI.
- `d977366`, `b90288c`, `c5d8e47` expose and adopt winner identity.
- `180f01d`, `dd1f486` expose and adopt terminal state.
- `4a8efe1`, `e9ff248`, `b91a3ba` guard and cover selected-move edge cases.
- `e8460cb`, `660cafc`, `985c30c`, `41b8d41` add progress/capacity vocabulary.

### MinMax scoring and decomposition

- `8425213`, `7f92aae` add and verify depth-aware scoring.
- `d36c2dd`, `ef0c7ee`, `122e5c8`, `04dcd5b` centralize simulation.
- `eaae94b`, `136267c`, `de7a7c5` centralize and cover terminal scoring.
- `2216f08`, `0d21c0b`, `62ae9b6`, `810f58d` centralize move evaluation.
- `dc70182`, `6e92520`, `39b76d2` centralize score lists and reductions.

### Shared positions, layout validation, and presentation boundaries

- `7822a95`, `821220f`, `e9ea73b`, `b642cd0` define and reuse board positions.
- `833e3b7`, `1e74f9b`, `1ec108c`, `95be57e` introduce and adopt
  `BoardPosition`.
- `574a54a`, `c2446c9`, `8c47919` validate and simplify layout mapping.
- `8245a12`, `0325f9a`, `e3368fe` inject renderers and enforce layout consistency.
- `aa700cd`, `8b4b285`, `e861dd4` separate reset and title responsibilities.
- `e1bc1f0`, `0c39739`, `ef279d9`, `c83a937`, `b9816f7` extract, adopt, and
  cover `GameTitleFormatter`.
- `7de2950`, `9c421f7` define and adopt the `BoardRenderer` abstraction.
