from engine.color import HanabiColor
import pytest


class TestHanabiColor(object):

    def test_constructor_element(self):
        assert HanabiColor(HanabiColor.red) == HanabiColor.red

    def test_purple_element(self):
        with pytest.raises(AttributeError):
            _ = HanabiColor.purple

    def test_getitem_purple(self):
        with pytest.raises(KeyError):
            _ = HanabiColor['purple']

    @pytest.mark.parametrize('expected_element',
                             ['blue',
                              'green',
                              'red',
                              'white',
                              'yellow',
                              'wild'])
    def test__names_gen(self, expected_element):
        assert expected_element in HanabiColor.names()

    @pytest.mark.parametrize('name,expected_item',
                             [('blue', HanabiColor.blue),
                              ('green', HanabiColor.green),
                              ('red', HanabiColor.red),
                              ('white', HanabiColor.white),
                              ('yellow', HanabiColor.yellow),
                              ('wild', HanabiColor.wild)])
    def test_constructor_string(self, name, expected_item):
        assert HanabiColor(name) == expected_item

    @pytest.mark.parametrize('name,expected_item',
                             [('blue', HanabiColor.blue),
                              ('green', HanabiColor.green),
                              ('red', HanabiColor.red),
                              ('white', HanabiColor.white),
                              ('yellow', HanabiColor.yellow),
                              ('wild', HanabiColor.wild)])
    def test__getitem(self, name, expected_item):
        assert HanabiColor[name] == expected_item

    def test__names(self):
        name_list = list(HanabiColor.names())
        assert len(name_list) == 6
        for name in name_list:
            assert isinstance(name, str)

    def test__correct_length(self):
        assert len(HanabiColor) == 6

    @pytest.mark.parametrize('name',
                             ['blue',
                              'green',
                              'red',
                              'white',
                              'yellow',
                              'wild'])
    def test__contains_str_name(self, name):
        assert name in HanabiColor

    @pytest.mark.parametrize('name',
                             [('purple',),
                              ('orange',),
                              ('turquoise',),
                              ('magenta',),
                              ('cyan',)])
    def test__not_contains_str_name(self, name):
        assert name not in HanabiColor

    @pytest.mark.parametrize('element,expected_name',
                             [(HanabiColor.blue, 'blue'),
                              (HanabiColor.green, 'green'),
                              (HanabiColor.red, 'red'),
                              (HanabiColor.white, 'white'),
                              (HanabiColor.yellow, 'yellow'),
                              (HanabiColor.wild, 'wild')])
    def test__name(self, element, expected_name):
        assert element.name == expected_name

    @pytest.mark.parametrize('element,expected_str',
                             [(HanabiColor.blue, 'HanabiColor.blue'),
                              (HanabiColor.green, 'HanabiColor.green'),
                              (HanabiColor.red, 'HanabiColor.red'),
                              (HanabiColor.white, 'HanabiColor.white'),
                              (HanabiColor.yellow, 'HanabiColor.yellow'),
                              (HanabiColor.wild, 'HanabiColor.wild')])
    def test__str(self, element, expected_str):
        assert str(element) == expected_str

    @pytest.mark.parametrize('a,b',
                             [(HanabiColor.blue, HanabiColor.green),
                              (HanabiColor.green, HanabiColor.red),
                              (HanabiColor.red, HanabiColor.white),
                              (HanabiColor.white, HanabiColor.yellow),
                              (HanabiColor.yellow, HanabiColor.blue),
                              (HanabiColor.wild, HanabiColor.blue),
                              (HanabiColor.wild, HanabiColor.green),
                              (HanabiColor.wild, HanabiColor.red),
                              (HanabiColor.wild, HanabiColor.white),
                              (HanabiColor.wild, HanabiColor.yellow)])
    def test__not_equal(self, a, b):
        assert not a == b

    @pytest.mark.parametrize('color,expected_appearance',
                             [(HanabiColor.blue, HanabiColor.blue),
                              (HanabiColor.green, HanabiColor.green),
                              (HanabiColor.red, HanabiColor.red),
                              (HanabiColor.white, HanabiColor.white),
                              (HanabiColor.yellow, HanabiColor.yellow),
                              (HanabiColor.wild, HanabiColor.blue),
                              (HanabiColor.wild, HanabiColor.green),
                              (HanabiColor.wild, HanabiColor.red),
                              (HanabiColor.wild, HanabiColor.white),
                              (HanabiColor.wild, HanabiColor.yellow)])
    def test__appears(self, color, expected_appearance):
        assert color.appears(expected_appearance)

    @pytest.mark.parametrize('color,unexpected_appearance',
                             [(HanabiColor.blue, HanabiColor.green),
                              (HanabiColor.green, HanabiColor.red),
                              (HanabiColor.red, HanabiColor.white),
                              (HanabiColor.white, HanabiColor.yellow),
                              (HanabiColor.yellow, HanabiColor.blue),
                              (HanabiColor.wild, HanabiColor.wild)])
    def test__not_appears(self, color, unexpected_appearance):
        assert not color.appears(unexpected_appearance)
