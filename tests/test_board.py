from engine.board import Board
from engine.cardstack import CardStack

import pytest
import util


@pytest.fixture(scope="module")
def card():
    return util.create_mock_card(number=2, color='blue')


@pytest.fixture(scope="module")
def your_card():
    return util.create_mock_yourcard(public_number=False, public_color=False)


@pytest.fixture(scope='module')
def mock_deck():
    return util.create_mock_deck(card_colors=('red', 'blue'), card_numbers=(1, 2, 2, 3), r_len=40)


@pytest.fixture(scope='function')
def board(mock_deck):
    return Board(mock_deck)


def test_init_creates_expected_cardstacks(board, mock_deck):
    # Check that there's a stack for each color in the deck
    for color in mock_deck.card_colors:
        assert isinstance(board.card_stacks[color], CardStack)


def xtest_init_creates_discard_stats(board, mock_deck):
    # Assert there's a discard pile with a length:
    assert len(board.discard) == 0
    # Assert there's a discard_stats list with one counter per card number
    for color in mock_deck.card_colors:
        assert len(board.discard_stats[color]) == len(set(mock_deck.card_numbers))


def test_discard_card_to_discard(board, card):
    assert card not in board.discard
    board.discard_card(card)
    assert card in board.discard


def test_discard_card_your_card(board, your_card):
    assert your_card not in board.discard
    board.discard_card(your_card)
    assert your_card in board.discard


def test_discard_card_updates_stats(board, card):
    discarded_count = board.discard_stats[card.color][card.number]
    board.discard_card(card)
    assert board.discard_stats[card.color][card.number] == discarded_count + 1


def test_use_clock_token(board):
    token_count = board.clock_tokens
    board.use_clock_token()
    assert board.clock_tokens == token_count - 1


def test_use_clock_token_no_tokens(board):
    board.clock_tokens = 0
    with pytest.raises(AssertionError):
        board.use_clock_token()


def test_use_fuse_token(board):
    token_count = board.fuse_tokens
    board.use_fuse_token()
    assert board.fuse_tokens == token_count - 1


def test_use_fuse_token_no_tokens(board):
    board.fuse_tokens = 0
    with pytest.raises(Exception):
        board.use_fuse_token()


def test_add_clock_token(board):
    board.clock_tokens = 1
    token_count = board.clock_tokens
    board.add_clock_token()
    assert board.clock_tokens == token_count + 1


def test_add_clock_token_full(board):
    assert board.clock_tokens == board.MAX_CLOCK_TOKENS
    board.add_clock_token()
    assert board.clock_tokens == board.MAX_CLOCK_TOKENS


def test_get_card_stack(board):
    assert isinstance(board.get_card_stack('red'), CardStack)


def test_get_card_stack_bad_color(board):
    with pytest.raises(AssertionError):
        board.get_card_stack('orange')


def test_compute_score_zero(board):
    assert board.compute_score() == 0


def test_compute_score_non_zero(board):
    board.card_stacks['red'] = util.create_mock_cardstack(r_get_score=3)
    board.card_stacks['blue'] = util.create_mock_cardstack(r_get_score=2)
    assert board.compute_score() == 5
