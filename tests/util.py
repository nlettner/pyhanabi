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


def create_mock_yourcard(public=False, number=None, color=None, public_number=None, public_color=None):
    mock_yourcard = create_autospec(YourCard)
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


def create_mock_cardstack(r_get_score=None, r_is_legal_play=None, r_is_complete=None):
    mock_cardstack = create_autospec(CardStack)
    if r_get_score is not None:
        mock_cardstack.get_score.return_value = r_get_score
    if r_is_legal_play is not None:
        mock_cardstack.is_legal_play.return_value = r_is_legal_play
    if r_is_complete is not None:
        mock_cardstack.is_complete.return_value = r_is_complete
    return mock_cardstack


def create_mock_deck(card_colors=None, card_numbers=None, r_draw_card=None, r_len=None):
    mock_deck = create_autospec(Deck)
    if card_colors:
        mock_deck.card_colors = card_colors
    if card_numbers:
        mock_deck.card_numbers = card_numbers
    if r_draw_card:
        mock_deck.draw_card.return_value = r_draw_card
    if r_len is not None:
        mock_deck.__len__.return_value = r_len
    return mock_deck


def create_mock_board(clock_tokens=None, fuse_tokens=None, game_almost_over=None, r_get_card_stack=None, r_compute_score=None):
    mock_board = create_autospec(Board)
    if clock_tokens is not None:
        mock_board.clock_tokens = clock_tokens
    if fuse_tokens is not None:
        mock_board.fuse_tokens = fuse_tokens
    if game_almost_over is not None:
        mock_board.game_almost_over = game_almost_over
    if r_get_card_stack is not None:
        mock_board.get_card_stack.return_value = r_get_card_stack
    if r_compute_score is not None:
        mock_board.compute_score.return_value = r_compute_score
    return mock_board


def create_mock_gamestate(hands=None, cards=('card0', 'card1', 'card2', 'card3', 'card4', 'card5', 'card6'), hand_split=3):
    mock_gamestate = create_autospec(GameState)
    if hands is not None:
        mock_gamestate.player_hands = hands
    elif cards is not None and hand_split is not None:
        if hand_split < 0 or hand_split > len(cards):
            hand_split = 3
        mock_gamestate.player_hands = [cards[:hand_split], cards[hand_split:]]
    return mock_gamestate
