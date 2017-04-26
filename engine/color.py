from enum import Enum


class MetaHanabiColor(type(Enum)):

    color_count = 6  # Should be equal to the number of colors in the `HanabiColor` enum

    def __init__(self, cls, enum, members):
        super(MetaHanabiColor, self).__init__(cls, enum, members)

    def __contains__(self, item):
        return item in self.__dict__

    def names(self):
        for name in self._member_names_:
            yield name


class HanabiColor(Enum):
    """An enum of Hanabi card colors."""
    __metaclass__ = MetaHanabiColor

    blue, green, red, white, yellow, wild = (None, None, None, None, None, 0)

    def __init__(self, looks_like):
        self.looks_like = looks_like
        if self.name == 'wild':
            self.looks_like = (self.blue | self.green | self.red | self.white | self.yellow)

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        # Assign enum values to unique binary digits (000001, 000010, etc)
        obj._value_ = 1 << len(cls.__members__)
        return obj

    def appears(self, other):
        if self.looks_like is not None:
            return (self.looks_like & other.value) != 0
        else:
            return self == other

    def __or__(self, other):
        return self.value | other.value

    def __ror__(self, other):
        return other | self.value
