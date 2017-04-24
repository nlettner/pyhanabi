from engine.move import Move
from engine.player import Player


class BasicMCSPlayer(Player):
    """An AI that uses monte carlo search techniques to choose moves."""

    def __str__(self):
        return "BasicMCSPlayer"

    def make_move(self, game_state):
        raise NotImplementedError
