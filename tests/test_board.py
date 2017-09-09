from engine.board import Board
from engine.cardstack import CardStack

import pytest
import unittest
import util


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.mock_deck = util.create_mock_deck(card_colors=('red', 'blue'), card_numbers=(1, 2, 2, 3), r_len=40)
        self.board = Board(self.mock_deck)

    def test_init_creates_expected_cardstacks(self):
        # Check that there's a stack for each color in the deck
        for color in self.mock_deck.card_colors:
            assert isinstance(self.board.card_stacks[color], CardStack)

    def xtest_init_creates_discard_stats(self):
        # Assert there's a discard pile with a length:
        assert len(self.board.discard) == 0
        # Assert there's a discard_stats list with one counter per card number
        for color in self.mock_deck.card_colors:
            assert len(self.board.discard_stats[color]) == len(set(self.mock_deck.card_numbers))

    def test_discard_card_to_discard(self):
        card = util.create_mock_card(number=2, color='blue')
        assert card not in self.board.discard
        self.board.discard_card(card)
        assert card in self.board.discard

    def test_discard_card_your_card(self):
        your_card = util.create_mock_yourcard(public_number=False, public_color=False)
        assert your_card not in self.board.discard
        self.board.discard_card(your_card)
        assert your_card in self.board.discard

    def test_discard_card_updates_stats(self):
        card = util.create_mock_card(number=2, color='blue')
        discarded_count = self.board.discard_stats[card.color][card.number]
        self.board.discard_card(card)
        assert self.board.discard_stats[card.color][card.number] == discarded_count + 1

    def test_use_clock_token(self):
        token_count = self.board.clock_tokens
        self.board.use_clock_token()
        assert self.board.clock_tokens == token_count - 1

    def test_use_clock_token_no_tokens(self):
        self.board.clock_tokens = 0
        with pytest.raises(AssertionError):
            self.board.use_clock_token()

    def test_use_fuse_token(self):
        token_count = self.board.fuse_tokens
        self.board.use_fuse_token()
        assert self.board.fuse_tokens == token_count - 1

    def test_use_fuse_token_no_tokens(self):
        self.board.fuse_tokens = 0
        with pytest.raises(Exception):
            self.board.use_fuse_token()

    def test_add_clock_token(self):
        self.board.clock_tokens = 1
        token_count = self.board.clock_tokens
        self.board.add_clock_token()
        assert self.board.clock_tokens == token_count + 1

    def test_add_clock_token_full(self):
        assert self.board.clock_tokens == self.board.MAX_CLOCK_TOKENS
        self.board.add_clock_token()
        assert self.board.clock_tokens == self.board.MAX_CLOCK_TOKENS

    def test_get_card_stack(self):
        assert isinstance(self.board.get_card_stack('red'), CardStack)

    def test_get_card_stack_bad_color(self):
        with pytest.raises(AssertionError):
            self.board.get_card_stack('orange')

    def test_compute_score_zero(self):
        assert self.board.compute_score() == 0

    def test_compute_score_non_zero(self):
        self.board.card_stacks['red'] = util.create_mock_cardstack(r_get_score=3)
        self.board.card_stacks['blue'] = util.create_mock_cardstack(r_get_score=2)
        assert self.board.compute_score() == 5
