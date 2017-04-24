class Color(object):

    def __init__(self, name, color_matches=None, match_name=True):
        assert isinstance(name, str)
        self.name = name

        matches = set()
        if color_matches is not None:
            for color in color_matches:
                matches.add(color)

        if match_name:
            matches.add(name)

        self.match_set = frozenset(matches)

    def matches(self, colors):
        if isinstance(colors, Color):
            return colors.name in self.match_set
        if isinstance(colors, str):
            return colors in self.match_set
        return not self.match_set.isdisjoint(colors)

    def __eq__(self, other):
        return isinstance(other, Color) and self.name == other.name

    def __repr__(self):
        return self.name
