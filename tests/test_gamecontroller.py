from engine.gamecontroller import GameController
from engine.player import Player
import pytest
import util

from mock import create_autospec


@pytest.fixture(scope='module')
def mock_player():
    return create_autospec(Player)


@pytest.fixture(scope="module")
def mock_deck():
    return util.create_mock_deck(return_draw_card='card')


@pytest.fixture(scope='function')
def gamecontroller(mock_player):
    gc = GameController([mock_player, mock_player])
    gc.master_game_state = util.create_mock_gamestate()
    return gc


@pytest.mark.parametrize(argnames='player_count', argvalues=[1, 6])
def test_constructor_fail_invalid_number_of_players(player_count, mock_player):
    with pytest.raises(ValueError) as excinfo:
        GameController(players=[mock_player for _ in range(player_count)])
    assert str(excinfo.value) == 'There must be between 2 and 5 players to play Hanabi.'


@pytest.mark.parametrize(argnames=['player_count', 'expected_hand_size'], argvalues=[[2, 5], [3, 5], [4, 4], [5, 4]])
def test_deal_initial_hand_2p(player_count, expected_hand_size, mock_player, mock_deck):
    gc = GameController([mock_player for _ in range(player_count)])
    gc.deck = mock_deck
    gc.deal_initial_hand()
    assert len(gc.player_hands) == player_count
    assert len(gc.player_hands[0]) == expected_hand_size


# TODO: game_over: every escape case works, returns false when they have expected vals
def test_game_over_no_fuse_tokens(gamecontroller):
    gamecontroller.master_game_state.board = util.create_mock_board(fuse_tokens=0)
    assert gamecontroller.game_over(0, gamecontroller.master_game_state)


def test_game_over_all_stacks_completed(gamecontroller):
    gamecontroller.master_game_state.board = util.create_mock_board(fuse_tokens=1,
                                                                    # Max score for a default game. Need to update when
                                                                    # we add wilds / configurable color counts.
                                                                    return_compute_score=25)
    assert gamecontroller.game_over(0, gamecontroller.master_game_state)


# TODO: There's a more-clear way to manage game state and track final player turn.
# TODO: Finish writing this test, then refactor. Might even need to move game_over to GameState
# Note, this doesn't need to know about the actual deck
@pytest.mark.parametrize(argnames=('deck_length', 'current_turn', 'expected_game_state'),
                         argvalues=((0, 0, True), (1, 0, False), (0, 1, False)))
def test_game_over_last_turn(gamecontroller, deck_length, current_turn, expected_game_state):
    gamecontroller.deck = util.create_mock_deck(return_len=deck_length)
    gamecontroller.master_game_state.board = util.create_mock_board(fuse_tokens=1, game_almost_over=0)
    assert gamecontroller.game_over(current_turn, gamecontroller.master_game_state) is expected_game_state


# TODO: Test play_game fails if player cannot make_move (may belong in make_move?)
def test_play_game_last_move_wins():
    # Because if the final move causes a win we should return true but the game should end with correct points
    pass
