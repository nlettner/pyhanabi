from engine.board import Board
from engine.card import Card, YourCard
from engine.cardstack import CardStack
from engine.deck import Deck
from engine.gamestate import GameState

from mock import create_autospec


def create_mock_card(number=None, color=None):
    mock_card = create_autospec(Card)
    if color is not None:
        mock_card.color = color
    if number is not None:
        mock_card.number = number
    return mock_card


def create_mock_yourcard(in_your_hand=None, public=False, number=None, color=None, public_number=None, public_color=None):
    mock_yourcard = create_autospec(YourCard)
    if in_your_hand is not None:
        mock_yourcard.in_your_hand = in_your_hand
    if not public:
        if public_number is not None:
            mock_yourcard.public_number = public_number
        if public_color is not None:
            mock_yourcard.public_color = public_color
    if color is not None:
        mock_yourcard.color = color
        if public:
            mock_yourcard.color = color
    if number is not None:
        mock_yourcard.number = number
        if public:
            mock_yourcard.number = number
    return mock_yourcard


def create_mock_cardstack(color=None, return_get_score=None, return_is_legal_play=None, return_is_complete=None):
    mock_cardstack = create_autospec(CardStack)
    if color is not None:
        mock_cardstack.color = color
    if return_get_score is not None:
        mock_cardstack.get_score.return_value = return_get_score
    if return_is_legal_play is not None:
        mock_cardstack.is_legal_play.return_value = return_is_legal_play
    if return_is_complete is not None:
        mock_cardstack.is_complete.return_value = return_is_complete
    return mock_cardstack


def create_mock_deck(card_colors=None, card_numbers=None, return_draw_card=None, return_len=None):
    mock_deck = create_autospec(Deck)
    if card_colors:
        mock_deck.card_colors = card_colors
    if card_numbers:
        mock_deck.card_numbers = card_numbers
    if return_draw_card:
        mock_deck.draw_card.return_value = return_draw_card
    if return_len is not None:
        mock_deck.__len__.return_value = return_len
    return mock_deck


def create_mock_board(clock_tokens=None, fuse_tokens=None, game_almost_over=None,
                      return_get_card_stack=None, return_compute_score=None):
    mock_board = create_autospec(Board)
    if clock_tokens is not None:
        mock_board.clock_tokens = clock_tokens
    if fuse_tokens is not None:
        mock_board.fuse_tokens = fuse_tokens
    if game_almost_over is not None:
        mock_board.game_almost_over = game_almost_over
    if return_get_card_stack is not None:
        mock_board.get_card_stack.return_value = return_get_card_stack
    if return_compute_score is not None:
        mock_board.compute_score.return_value = return_compute_score
    return mock_board

def create_mock_gamestate(hands=None):
    mock_gamestate = create_autospec(GameState)
    if hands is not None:
        mock_gamestate.player_hands = hands
    return mock_gamestate
