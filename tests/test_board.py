from engine.board import Board
from engine.card import Card, YourCard
from engine.cardstack import CardStack
from engine.deck import Deck

import pytest
import unittest
import util

from mock import create_autospec


class TestBoard(unittest.TestCase):

    @staticmethod
    def create_your_card():
        your_card = create_autospec(YourCard)
        your_card.number = False
        your_card.color = False
        return your_card

    @staticmethod
    def create_card():
        card = create_autospec(Card)
        card.number = 2
        card.color = 'blue'
        return card

    @staticmethod
    def create_mock_deck():
        mock_deck = create_autospec(Deck)
        mock_deck.__len__.return_value = 40
        mock_deck.card_colors = ('red', 'blue')
        mock_deck.card_numbers = (1, 2, 3, 4)
        return mock_deck

    @staticmethod
    def create_board(clock_tokens=None, fuse_tokens=None):
        board = Board(TestBoard.create_mock_deck())
        if clock_tokens is not None:
            board.clock_tokens = clock_tokens
        if fuse_tokens is not None:
            board.fuse_tokens = fuse_tokens
        return board

    # TODO: Move mock deck creation to setUp
    def test_init_creates_expected_cardstacks(self):
        mock_deck = self.create_mock_deck()
        board = Board(mock_deck)
        # Check that there's a stack for each color in the deck
        for color in mock_deck.card_colors:
            assert isinstance(board.card_stacks[color], CardStack)

    # TODO: Move mock deck creation to setUp
    def xtest_init_creates_discard_stats(self):
        mock_deck = self.create_mock_deck()
        board = Board(mock_deck)
        # Assert there's a discard pile with a length:
        assert len(board.discard) == 0
        # Assert there's a discard_stats list with one counter per card number
        for color in mock_deck.card_colors:
            assert len(board.discard_stats[color]) == len(set(mock_deck.card_numbers))

    def test_discard_card_to_discard(self):
        board = self.create_board()
        card = self.create_card()
        assert card not in board.discard
        board.discard_card(card)
        assert card in board.discard

    def test_discard_card_your_card(self):
        board = self.create_board()
        your_card = self.create_your_card()
        assert your_card not in board.discard
        board.discard_card(your_card)
        assert your_card in board.discard

    def test_discard_card_updates_stats(self):
        board = self.create_board()
        card = self.create_card()
        discarded_count = board.discard_stats[card.color][card.number]
        board.discard_card(card)
        assert board.discard_stats[card.color][card.number] == discarded_count + 1

    def test_use_clock_token(self):
        board = self.create_board()
        token_count = board.clock_tokens
        board.use_clock_token()
        assert board.clock_tokens == token_count - 1

    def test_use_clock_token_no_tokens(self):
        board = self.create_board()
        board.clock_tokens = 0
        with pytest.raises(AssertionError):
            board.use_clock_token()

    def test_use_fuse_token(self):
        board = self.create_board()
        token_count = board.fuse_tokens
        board.use_fuse_token()
        assert board.fuse_tokens == token_count - 1

    def test_use_fuse_token_no_tokens(self):
        board = self.create_board(fuse_tokens=0)
        with pytest.raises(Exception):
            board.use_fuse_token()

    def test_add_clock_token(self):
        board = self.create_board(clock_tokens=1)
        token_count = board.clock_tokens
        board.add_clock_token()
        assert board.clock_tokens == token_count + 1

    def test_add_clock_token_full(self):
        board = self.create_board()
        assert board.clock_tokens == board.MAX_CLOCK_TOKENS
        board.add_clock_token()
        assert board.clock_tokens == board.MAX_CLOCK_TOKENS

    def test_get_card_stack(self):
        board = self.create_board()
        assert isinstance(board.get_card_stack('red'), CardStack)

    def test_get_card_stack_bad_color(self):
        with pytest.raises(AssertionError):
            self.create_board().get_card_stack('orange')

    def test_compute_score_zero(self):
        assert self.create_board().compute_score() == 0

    def test_compute_score_non_zero(self):
        board = self.create_board()
        board.card_stacks['red'] = util.create_mock_cardstack(r_get_score=3)
        board.card_stacks['blue'] = util.create_mock_cardstack(r_get_score=2)
        assert board.compute_score() == 5
