from engine.gamecontroller import GameController
from engine.player import Player
from engine.gamestate import GameState
import pytest
import unittest
import util

from mock import create_autospec


class TestGameController(unittest.TestCase):

    def setUp(self):
        self.player = create_autospec(Player)

    def test_constructor_fail_not_enough_players(self):
        with pytest.raises(ValueError) as excinfo:
            GameController(players=[self.player])
        assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'

    def test_constructor_fail_too_many_players(self):
        with pytest.raises(ValueError) as excinfo:
            GameController(players=[self.player, self.player, self.player,
                                    self.player, self.player, self.player])
        assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'

    def test_deal_initial_hand_2p(self):
        gc = GameController([self.player, self.player])
        gc.deck = util.create_mock_deck(r_draw_card="card")
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 2
        assert len(gc.player_hands[0]) == 5

    def test_deal_initial_hand_3p(self):
        gc = GameController([self.player, self.player, self.player])
        gc.deck = util.create_mock_deck(r_draw_card="card")
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 3
        assert len(gc.player_hands[0]) == 5

    def test_deal_initial_hand_4p(self):
        gc = GameController([self.player, self.player, self.player, self.player])
        gc.deck = util.create_mock_deck(r_draw_card="card")
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 4
        assert len(gc.player_hands[0]) == 4

    def test_deal_initial_hand_5p(self):
        gc = GameController([self.player, self.player, self.player, self.player, self.player])
        gc.deck = util.create_mock_deck(r_draw_card="card")
        gc.deal_initial_hand()
        assert len(gc.player_hands) == 5
        assert len(gc.player_hands[0]) == 4

    # TODO: game_over: every escape case works, returns false when they have expected vals
    def test_game_over_no_fuse_tokens(self):
        gc = GameController([self.player, self.player])
        gc.master_game_state.board.fuse_tokens = 0
        self.assertIs(gc.game_over(0, gc.master_game_state), True)

    def test_game_over_all_stacks_completed(self):
        gc = GameController([self.player, self.player])
        gc.master_game_state.board = util.create_mock_board(fuse_tokens=1,
                                                            # Max score for a default game. Need to update when we add
                                                            # wilds / configurable color counts.
                                                            r_compute_score=25)
        self.assertIs(gc.game_over(0, gc.master_game_state), True)

    def test_game_over_last_turn(self):
        # TODO: There's a more-clear way to manage game state and track final player turn.
        # TODO: Finish writing this test, then refactor. Might even need to move game_over to GameState
        # Note, this doesn't need to know about the actual deck
        gc = GameController([self.player, self.player])
        gc.deck = util.create_mock_deck(r_len=0)
        gc.master_game_state.board = util.create_mock_board(fuse_tokens=1, game_almost_over=0)
        self.assertIs(gc.game_over(0, gc.master_game_state), True)

    def test_game_over_not_over_deck_not_empty(self):
        gc = GameController([self.player, self.player])
        gc.deck = util.create_mock_deck(r_len=1)
        gc.master_game_state.board = util.create_mock_board(fuse_tokens=1, game_almost_over=0)
        self.assertIs(gc.game_over(0, gc.master_game_state), False)

    def test_game_over_not_over_deck_empty(self):
        gc = GameController([self.player, self.player])
        gc.deck = util.create_mock_deck(r_len=0)
        gc.master_game_state.board = util.create_mock_board(fuse_tokens=1, game_almost_over=0)
        self.assertIs(gc.game_over(1, gc.master_game_state), False)


    # TODO: Test play_game fails if player cannot make_move (may belong in make_move?)
    def test_play_game_last_move_wins(self):
        # Because if the final move causes a win we should return true but the game should end with correct points
        pass
