from engine.color import Color
from engine.card import Card, YourCard
import pytest

class TestCard:
    def test_init(self):
        color_b = Color('b')
        card_1 = Card(2, color_b)
        assert card_1.color == color_b
        assert card_1.number == 2
        assert card_1.public_number is None
        assert card_1.public_color is None
        assert not card_1.in_your_hand

    def test_eq_true(self):
        y_color = Color('y')
        card_1 = Card(1, y_color)
        card_2 = Card(1, y_color)
        assert card_1 == card_2

    def test_eq_false_number(self):
        y_color = Color('y')
        card_1 = Card(1, y_color)
        card_2 = Card(2, y_color)
        assert card_1 != card_2

    def test_eq_false_color(self):
        card_1 = Card(1, Color('y'))
        card_2 = Card(1, Color('b'))
        assert card_1 != card_2

    def test_eq_true_despite_public(self):
        g_color = Color('g')
        card_1 = Card(1, g_color)
        card_2 = Card(1, g_color)
        card_2.make_public('color')
        assert card_1 == card_2

    def test_make_public_color(self):
        b_color = Color('b')
        card_1 = Card(5, b_color)
        card_1.make_public('color')
        assert card_1.public_color == b_color

    def test_make_public_number(self):
        card_1 = Card(3, Color('y'))
        card_1.make_public('number')
        assert card_1.public_number == 3

    def test_make_public_invalid_input(self):
        card_1 = Card(1, Color('g'))
        with pytest.raises(ValueError):
            card_1.make_public('flavor')


class TestYourCard:
    def test_init(self):
        card_1 = Card(2, Color('b'))
        your_card_1 = YourCard(card_1)
        assert not your_card_1.number
        assert not your_card_1.color
        assert not your_card_1.public_number
        assert not your_card_1.public_color
        assert your_card_1.in_your_hand

    def test_cannot_make_public(self):
        card_1 = Card(2, Color('b'))
        your_card_1 = YourCard(card_1)
        with pytest.raises(Exception):
            your_card_1.make_public("color")

    def test_made_public_number(self):
        card_1 = Card(2, Color('b'))
        card_1.make_public('number')
        your_card_1 = YourCard(card_1)
        assert your_card_1.public_number == 2

    def test_made_public_color(self):
        color_b = Color('b')
        card_1 = Card(2, color_b)
        card_1.make_public('color')
        your_card_1 = YourCard(card_1)
        assert your_card_1.public_color == color_b

    def test_made_public_both(self):
        color_b = Color('b')
        card_1 = Card(2, color_b)
        card_1.make_public('color')
        card_1.make_public('number')
        your_card_1 = YourCard(card_1)
        assert your_card_1.public_color == color_b
        assert your_card_1.public_number == 2
