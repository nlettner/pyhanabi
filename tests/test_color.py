from engine.color import Color
import pytest


@pytest.mark.parametrize("name,matches",
                         [('red', None),
                          ('green', None),
                          ('wild', ('red', 'green'))])
def test_init__name_set(name, matches):
    """Test `Color` object `__init__`."""

    color = Color(name, color_matches=matches)
    assert color.name == name


@pytest.mark.parametrize("name,matches",
                         [('red', None),
                          ('green', None),
                          ('wild', ('red', 'green'))])
def test_color_matches_self(name, matches):
    """Test that a `Color` `matches` itself."""

    color = Color(name, color_matches=matches)
    assert color.matches(color)


@pytest.mark.parametrize("name,matches",
                         [('red', None),
                          ('green', None),
                          ('wild', ('red', 'green'))])
def test_color_matches_str(name, matches):
    """Test that a `Color` `matches` its own name."""

    color = Color(name, color_matches=matches)
    assert color.matches(color.name)


@pytest.mark.parametrize("name,matches",
                         [('red', None),
                          ('green', None),
                          ('wild', ('red', 'green'))])
def test_color_match_name_false(name, matches):
    """Test that a `Color` with `match_name=False` does matches neither `Color`s with the same name nor its own name."""

    color = Color(name, color_matches=matches, match_name=False)
    assert not color.matches(color.name)
    assert not color.matches(color)


@pytest.mark.parametrize("color, not_expected",
                         [(Color('red'), (Color('yellow'), 'white', Color('wild', ('red', 'green')))),
                          (Color('blue'), (Color('red'), 'green', Color('wild', ('red', 'green')))),
                          (Color('wild', ('red', 'blue')), ('yellow', Color('green'), 'white'))])
def test_color_does_not_match(color, not_expected):
    """Test that a `Color` does not match unexpected colors."""
    assert isinstance(color, Color)
    assert not_expected
    for not_match in not_expected:
        assert not color.matches(not_match)


@pytest.mark.parametrize("color,expected_matches",
                         [(Color('wild', ('red', 'green')), ('red', 'green', 'wild'))])
def test_wild_matches_all(color, expected_matches):
    """Test that a `Color` with many color matches correctly matches them."""
    assert isinstance(color, Color)
    assert expected_matches
    for expected_match in expected_matches:
        assert color.matches(expected_match)


@pytest.mark.parametrize("color,expected_matches",
                         [(Color('wild', ('red', 'green')), ('yellow', Color('white'), 'blue'))])
def test_wild_not_match(color, expected_matches):
    """Test that a `Color` with many color matches does not match other colors."""
    assert isinstance(color, Color)
    assert expected_matches
    for expected_match in expected_matches:
        assert not color.matches(expected_match)


@pytest.mark.parametrize("color,match_any",
                         [(Color('red'), (('red',), ('green', 'red'))),
                          (Color('wild', ('red', 'green')),
                           (('red',), ('blue', 'green'), ('wild', 'white'), ('red', 'green')))])
def test_color_matches_any(color, match_any):
    """Test that a `Color` matches a set of `str` that has color at least one names that matches."""
    assert isinstance(color, Color)
    assert match_any
    for color_set in match_any:
        assert color.matches(color_set)


@pytest.mark.parametrize("color,match_none",
                         [(Color('red'), (("blue",), ('wild',), ('yellow', 'green'))),
                          (Color('wild', ('red', 'green')), (('yellow',), ('purple', 'blue'), ('blue', 'white')))])
def test_color_matches_none(color, match_none):
    """Test that a `Color` does not match a set of `str` that has no color names that match it."""
    assert isinstance(color, Color)
    assert match_none
    for color_set in match_none:
        assert not color.matches(color_set)


@pytest.mark.parametrize("color_a,color_b",
                         [(Color('red'), Color('green')),
                          (Color('white'), Color('blue')),
                          (Color('wild', ('red', 'blue')), Color('red')),
                          (Color('wild', ('red', 'blue')), Color('blue'))])
def test_not_eq(color_a, color_b):
    """Test that `not color_a == color_b`."""
    assert isinstance(color_a, Color)
    assert isinstance(color_b, Color)
    assert not color_a == color_b


@pytest.mark.parametrize("color_a,color_b",
                         [(Color('red'), Color('red')),
                          (Color('wild', ('red', 'blue')), Color('wild')),
                          (Color('wild', ('red', 'blue')), Color('wild', ('red', 'green'))),
                          (Color('wild', ('red', 'blue')), Color('wild', ('red', 'blue')))])
def test_eq(color_a, color_b):
    """Test that 'color_a == color_b`."""
    assert isinstance(color_a, Color)
    assert isinstance(color_b, Color)
    assert color_a == color_b
