from engine.move import Move
from engine.player import Player


class HeuristicPlayer(Player):
    """An AI that uses heuristic techniques to choose moves."""

    def __str__(self):
        return "HeuristicPlayer"

    def make_move(self, game_state):
        raise NotImplementedError
