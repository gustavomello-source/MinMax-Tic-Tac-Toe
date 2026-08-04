"""
Implement the console interface for Tic Tac Toe.

This module defines the ConsoleUI class, which displays the board,
reads human moves, and runs the match loop.
"""

from ..game.match import Match
from ..game.player_mark import PlayerMark


class ConsoleUI:
    """Control the console interface of a Tic Tac Toe match."""

    def __init__(self) -> None:
        """Initialize the console interface."""
        self.match: Match = Match(human_player=PlayerMark.X)

    def _display_board(self) -> None:
        """Display the current board state in the console."""
        state: list[list[PlayerMark | None]] = (
            self.match.board.get_current_state()
        )

        print("\n  1   2   3")

        for row_index, row in enumerate(state):
            symbols: list[str] = [
                cell.value if cell is not None else " "
                for cell in row
            ]

            print(f"{row_index + 1} " + " | ".join(symbols))

            if row_index < 2:
                print("  ---------")

        print()

    def _read_move(self) -> tuple[int, int]:
        """Read a valid row and column from the user.

        Returns:
            tuple[int, int]: The selected board position.
        """
        while True:
            try:
                value: str = input(
                    "Enter row and column (1-3), separated by space: "
                )

                row, col = map(int, value.split())

                if 1 <= row <= 3 and 1 <= col <= 3:
                    return row - 1, col - 1

                print("Row and column must be between 1 and 3.")

            except ValueError:
                print("Enter two numbers separated by space.")


    def _display_result(self) -> None:
        """Display the final result of the match."""
        winner: PlayerMark | None = self.match.board.get_winner()

        if winner is not None:
            print(f"Player {winner.value} wins!")
        else:
            print("The match ended in a draw.")


    def run(self) -> None:
        """Run the console match loop."""
        print("Tic Tac Toe")

        while not self.match.board.is_game_over():
            self._display_board()

            if self.match.current_player == self.match.human_player:
                row, col = self._read_move()
                success: bool = self.match.play_move(row, col)

                if not success:
                    print("This position is not available.")
            else:
                print("The AI is thinking...")

                move: tuple[int, int] | None = (
                    self.match.play_ai_move()
                )

                if move is None:
                    print("The AI could not make a move.")
                    return

                row, col = move
                print(f"The AI played at row {row + 1}, column {col + 1}.")

        self._display_board()
        self._display_result()

if __name__ == "__main__":
    ConsoleUI().run()