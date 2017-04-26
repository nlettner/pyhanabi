from enum import Enum


class MetaHanabiColor(type(Enum)):
    """Metaclass for `HanabiColor`."""

    def __call__(self, value, names=None, a_module=None, a_type=None, start=1):
        if names is None:  # Simple lookup
            if value in self:
                return self._member_map_[value]
            # Otherwise, let parent metaclass handle it.
            return super(MetaHanabiColor, self).__call__(value, names=names, module=a_module, type=a_type, start=start)

    def __contains__(self, item):
        return item in self._member_map_

    def names(self):
        for name in self._member_names_:
            yield name


class HanabiColor(Enum):
    """An enum of Hanabi card colors."""
    __metaclass__ = MetaHanabiColor

    # Unique enum values are assigned in `__new__`
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
