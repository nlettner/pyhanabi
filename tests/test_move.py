from engine.move import Move

import pytest
import util


# TODO: Are some of these integration tests?

@pytest.fixture(scope='function')
def card():
    return util.create_mock_card()


@pytest.fixture(scope='module')
def wild_card():
    return util.create_mock_card(color='wild')


@pytest.fixture(scope='function')
def blue_card():
    return util.create_mock_card(color='blue')


@pytest.fixture(scope='function')
def red_card():
    return util.create_mock_card(color='red')


@pytest.fixture(scope='function')
def two_card():
    return util.create_mock_card(number=2)


@pytest.fixture(scope='function')
def four_card():
    return util.create_mock_card(number=4)


@pytest.fixture(scope='module')
def your_card():
    return util.create_mock_yourcard(public=True, number=2, color='blue')


@pytest.fixture(scope='module')
def default_hands_3_4():
    return [['card0', 'card1', 'card2'], ['card3', 'card4', 'card5', 'card6']]


@pytest.fixture(scope='module')
def default_hands_4_3():
    return [['card0', 'card1', 'card2', 'card3'], ['card4', 'card5', 'card6']]


@pytest.fixture(scope='module')
def mock_hand():
    return ['is_playable should not', 'look at players own hand']


def create_mock_gamestate(hands, clock_tokens=1):
    mock_gamestate = util.create_mock_gamestate(hands=hands)
    mock_gamestate.board = util.create_mock_board(clock_tokens=clock_tokens)
    return mock_gamestate


def test_create_bad_move_type():
    with pytest.raises(ValueError) as exinfo:
        Move(move_type='cheat', player_index=0)
    assert str(exinfo.value) == 'Moves must either play, discard, or share information.'


def test_create_bad_move_info():
    with pytest.raises(AssertionError):
        info_dict = {'has_no_useful_keys': 'or values!'}
        Move(move_type='give_information', player_index=0, information=info_dict)


@pytest.mark.parametrize(argnames='move', argvalues=('play', 'discard'))
def test_is_playable_play(move, default_hands_4_3):
    """move.is_playable returns true so long as there's a card in that player's hand at that index."""
    mock_gamestate = util.create_mock_gamestate(hands=default_hands_4_3)
    move = Move(move_type=move, player_index=0, card_index=3)
    assert move.is_playable(mock_gamestate) is True


@pytest.mark.parametrize(argnames='move', argvalues=('play', 'discard'))
@pytest.mark.parametrize(argnames='card_index', argvalues=(-1, 3))
def test_is_playable_invalid_card_index(move, card_index, default_hands_3_4):
    """move.is_playable returns false when there's no card in that player's hand at that index."""
    mock_gamestate = util.create_mock_gamestate(hands=default_hands_3_4)
    move = Move(move_type=move, player_index=0, card_index=card_index)
    assert move.is_playable(mock_gamestate) is False


def test_is_playable_information_color(mock_hand, blue_card):
    mock_gamestate = create_mock_gamestate(hands=[[blue_card, blue_card], mock_hand])
    info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'blue'}
    move = Move(move_type='give_information', player_index=1, information=info_dict)
    assert move.is_playable(mock_gamestate)


@pytest.mark.parametrize(argnames=['info_type', 'info'], argvalues=(('color', 'blue'), ('number', 2)))
def test_is_playable_information_known(info_type, info, your_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[[your_card, your_card], mock_hand])
    info_dict = {'player_id': 0, 'information_type': info_type, 'information': info}
    move = Move(move_type='give_information', player_index=1, information=info_dict)
    assert move.is_playable(mock_gamestate)


def test_is_playable_information_color_subset_of_cards(red_card, blue_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[[blue_card, red_card, red_card, red_card], mock_hand])
    info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'blue'}
    move = Move(move_type='give_information', player_index=1, information=info_dict)
    assert move.is_playable(mock_gamestate)


def test_is_playable_information_number(two_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[mock_hand, [two_card, two_card, two_card]])
    info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    assert move.is_playable(mock_gamestate)


def test_is_playable_information_number_subset_of_cards(two_card, four_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[mock_hand, [four_card, two_card, four_card, two_card]])
    info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    assert move.is_playable(mock_gamestate)


def test_is_playable_information_give__information_fails(two_card):
    mock_gamestate = create_mock_gamestate(hands=[[two_card, two_card, two_card], [two_card, two_card, two_card]])
    info_dict = {'player_id': 0, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


def test_is_playable_information_no_clock_tokens(two_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[mock_hand, [two_card, two_card, two_card]], clock_tokens=0)
    info_dict = {'player_id': 0, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=1, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


def test_is_playable_information_no_colors_fails(blue_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[[blue_card, blue_card], mock_hand])
    info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'red'}
    move = Move(move_type='give_information', player_index=1, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


def test_is_playable_information_no_numbers_fails(four_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[mock_hand, [four_card, four_card, four_card]])
    info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


def test_is_playable_information_invalid_player_fails(two_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[mock_hand, [two_card, two_card, two_card]])
    info_dict = {'player_id': 3, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


# Todo: Rebuild this when wilds are properly implemented.
def test_is_playable_information_color_is_wild_fail(wild_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[[wild_card, wild_card], mock_hand])
    info_dict = {'player_id': 0, 'information_type': 'color', 'information': 'wild'}
    move = Move(move_type='give_information', player_index=1, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


def test_is_playable_information_bad_information_type_fails(two_card, mock_hand):
    mock_gamestate = create_mock_gamestate(hands=[mock_hand, [two_card, two_card, two_card]])
    info_dict = {'player_id': 1, 'information_type': 'board talk is for cheaters', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    assert move.is_playable(mock_gamestate) is False


def test_apply_bad_move_fails(default_hands_3_4):
    mock_gamestate = util.create_mock_gamestate(hands=default_hands_3_4)
    move = Move(move_type='discard', player_index=0, card_index=-1)
    with pytest.raises(AssertionError) as excinfo:
        move.apply(mock_gamestate)
    assert str(excinfo.value) == 'Cannot apply move discard card index -1 in their hand, not playable.'


def test_apply_discard(card):
    """Discard should remove a card from the player's hand, add it to the discard pile and add back a clock token.
    """
    to_discard = util.create_mock_card()
    mock_gamestate = create_mock_gamestate(hands=[[card], [card, to_discard]], clock_tokens=None)
    move = Move(move_type='discard', player_index=1, card_index=1)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    assert len(mock_gamestate.player_hands[1]) == 1
    mock_gamestate.board.discard_card.assert_called_with(to_discard)
    mock_gamestate.board.add_clock_token.assert_called_once()


def test_apply_play_blow_fuse(card):
    """Play (blow fuse) should discard the card marked for play and call board.use_fuse_token"""
    to_play = util.create_mock_card(color='red')
    mock_gamestate = util.create_mock_gamestate(hands=[[card], [to_play, card]])
    mock_stack = util.create_mock_cardstack(r_is_legal_play=False)
    mock_gamestate.board = util.create_mock_board(r_get_card_stack=mock_stack)
    move = Move(move_type='play', player_index=1, card_index=0)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    mock_gamestate.board.get_card_stack.assert_called_with('red')
    assert len(mock_gamestate.player_hands[1]) == 1
    mock_gamestate.board.use_fuse_token.assert_called_once()
    mock_gamestate.board.discard_card.assert_called_with(to_play)


def test_apply_play_successful_play_incomplete_stack(card):
    """Play (successful) should 
            remove the card from hand, 
            add it to the stack of the right color, 
            not call board.add_clock_token
    """
    to_play = util.create_mock_card(color='green')
    mock_gamestate = util.create_mock_gamestate(hands=[[card], [to_play, card]])
    mock_stack = util.create_mock_cardstack(r_is_legal_play=True, r_is_complete=False)
    mock_gamestate.board = util.create_mock_board(r_get_card_stack=mock_stack)
    move = Move(move_type='play', player_index=1, card_index=0)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    mock_gamestate.board.get_card_stack.assert_called_with('green')
    mock_stack.play.assert_called_with(to_play)
    assert len(mock_gamestate.player_hands[1]) == 1
    mock_gamestate.board.add_clock_token.assert_not_called()


def test_apply_play_successful_play_complete_stack(card):
    """Play (successful) should 
              remove the card from hand, 
              add it to the stack of the right color, 
              call board.add_clock_token
    """
    to_play = util.create_mock_card(color='green')
    mock_gamestate = util.create_mock_gamestate(hands=[[card], [to_play, card]])
    mock_stack = util.create_mock_cardstack(r_is_legal_play=True, r_is_complete=True)
    mock_gamestate.board = util.create_mock_board(r_get_card_stack=mock_stack)
    move = Move(move_type='play', player_index=1, card_index=0)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    mock_gamestate.board.get_card_stack.assert_called_with('green')
    mock_stack.play.assert_called_with(to_play)
    assert len(mock_gamestate.player_hands[1]) == 1
    mock_gamestate.board.add_clock_token.assert_called_once()


def test_apply_give_information_color_once(blue_card, red_card):
    """Give information (color) should:
        call make_public('color') on all cards with that color in a hand
        call board.use_clock_token()
    """
    mock_gamestate = create_mock_gamestate(hands=[[red_card, red_card, blue_card, blue_card], [blue_card, red_card]],
                                           clock_tokens=2)
    info_dict = {'player_id': 1, 'information_type': 'color', 'information': 'blue'}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    blue_card.make_public.assert_called_once_with('color')
    mock_gamestate.board.use_clock_token.assert_called_once()


def test_apply_give_information_color_multiple_cards(blue_card, red_card):
    """Give information (color) should:
        call make_public('color') on all cards with that color in a hand
        call board.use_clock_token()
    """
    mock_gamestate = create_mock_gamestate(hands=[[red_card, red_card, blue_card], [blue_card, red_card, blue_card]],
                                           clock_tokens=2)
    info_dict = {'player_id': 1, 'information_type': 'color', 'information': 'blue'}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    blue_card.make_public.assert_called_with('color')
    assert blue_card.make_public.call_count == 2
    mock_gamestate.board.use_clock_token.assert_called_once()


def test_apply_give_information_number(two_card, four_card):
    """Give information (number) should:
        call make_public('number') on all cards with that number in a hand
        call board.use_clock_token()
    """
    mock_gamestate = create_mock_gamestate(hands=[[four_card, two_card, two_card],
                                                  [two_card, four_card, four_card]])
    info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    two_card.make_public.assert_called_once_with('number')
    mock_gamestate.board.use_clock_token.assert_called_once()


def test_apply_give_information_number_multiple_cards(two_card, four_card):
    """Give information (number) should:
        call make_public('number') on all cards with that number in a hand
        call board.use_clock_token()
    """
    mock_gamestate = create_mock_gamestate(hands=[[four_card, two_card, four_card], [two_card, four_card, two_card]])
    info_dict = {'player_id': 1, 'information_type': 'number', 'information': 2}
    move = Move(move_type='give_information', player_index=0, information=info_dict)
    mock_gamestate = move.apply(game_state=mock_gamestate)
    two_card.make_public.assert_called_with('number')
    assert two_card.make_public.call_count == 2
    mock_gamestate.board.use_clock_token.assert_called_once()
