"""Run the Tic Tac Toe application."""

from tictactoe.ai.minmax import MinMax
from tictactoe.game.player_mark import PlayerMark
from tictactoe.ui.pygame import PygameApp


def create_app() -> PygameApp:
    """Create the Pygame application with a MinMax opponent."""
    return PygameApp(opponent_move_selector=MinMax(PlayerMark.O))


def main() -> None:
    """Start the Pygame application."""
    create_app().run()
