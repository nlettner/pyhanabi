from engine.board import Board
from engine.cardstack import CardStack

import pytest
import util


@pytest.fixture(scope="module")
def mock_card():
    return util.create_mock_card(number=2, color='blue')


@pytest.fixture(scope="module")
def mock_your_card():
    return util.create_mock_yourcard(public_number=False, public_color=False)


@pytest.fixture(scope='module')
def mock_deck():
    return util.create_mock_deck(card_colors=('red', 'blue'), card_numbers=(1, 2, 2, 3), return_len=40)


@pytest.fixture(scope='function')
def board(mock_deck):
    return Board(mock_deck)


def test_init_creates_expected_cardstacks(board, mock_deck):
    # Ensure that mock_deck requires at least 1 CardStack
    assert len(mock_deck.card_colors) > 0
    # Check that there's a stack for each color in the deck
    for color in mock_deck.card_colors:
        assert isinstance(board.card_stacks[color], CardStack)


def test_init_creates_discard_stats(board, mock_deck):
    # Ensure that mock_deck requires at least 1 CardStack
    assert len(mock_deck.card_colors) > 0
    # Assert there's a discard pile with a length:
    assert len(board.discard) == 0
    # Assert there's a discard_stats list with one counter per card number
    for color in mock_deck.card_colors:
        assert len(board.discard_stats[color]) == len(set(mock_deck.card_numbers))


def test_discard_card_to_discard(board, mock_card):
    assert mock_card not in board.discard
    board.discard_card(mock_card)
    assert mock_card in board.discard


def test_discard_card_your_card(board, mock_your_card):
    assert mock_your_card not in board.discard
    board.discard_card(mock_your_card)
    assert mock_your_card in board.discard


def test_discard_card_updates_stats(board, mock_card):
    discarded_count = board.discard_stats[mock_card.color][mock_card.number]
    board.discard_card(mock_card)
    assert board.discard_stats[mock_card.color][mock_card.number] == discarded_count + 1


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
    board.add_clock_token()
    assert board.clock_tokens == 2


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
    # New boards should have a score of 0
    assert board.compute_score() == 0


def test_compute_score_non_zero(board):
    board.card_stacks['red'] = util.create_mock_cardstack(return_get_score=3)
    board.card_stacks['blue'] = util.create_mock_cardstack(return_get_score=2)
    assert board.compute_score() == 5
