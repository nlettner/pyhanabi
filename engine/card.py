from .color import Color


class Card(object):
    def __init__(self, number, color):
        assert isinstance(number, int)
        self.number = number
        assert isinstance(color, Color)
        self.color = color
        self.public_color = None
        self.public_number = None
        self.in_your_hand = False

    def __eq__(self, other):
        if type(other) != Card:
            return False
        return self.number == other.number and self.color == other.color

    def __str__(self):
        return "Card({number}:{color}, Public:{public_number}:{public_color})".format(number=self.number,
                                                                                      color=self.color,
                                                                                      public_number=self.public_number,
                                                                                      public_color=self.public_color)

    def __repr__(self):
        return str(self)

    def matches(self, valid_colors=None, valid_numbers=None):
        return self.does_color_match(valid_colors) and self.does_number_match(valid_numbers)

    def does_color_match(self, valid_colors=None):
        if isinstance(valid_colors, Card):
            valid_colors = valid_colors.color
        return not valid_colors or self.color.matches(valid_colors)

    def does_number_match(self, valid_numbers=None):
        if isinstance(valid_numbers, int):
            valid_numbers = [valid_numbers]
        return not valid_numbers or self.number in valid_numbers

    def make_public(self, information_type, information=None):
        if information_type == 'color':
            # No color information suggested or the `information` color does not match the `public_color`.
            if (not information or
                    # Ensure public color is not `None` or `False` before checking if it matches `information`.
                    (self.public_color and not self.public_color.matches(information))):
                # This card's private color is being exposed to the holder (or there's a bug somewhere).
                self.public_color = self.color
            else:
                assert isinstance(information, Color)
                # Ensure `Card`s do not advertise public colors that are inconsistent with the private color
                assert self.color.matches(information)
                # Set the public color of this card from the `information`
                self.public_color = information
        elif information_type == 'number':
            self.public_number = self.number
        else:
            raise ValueError("type must be either 'color' or 'number'")


class YourCard(Card):
    def __init__(self, card):
        assert isinstance(card, Card)
        self.number = False
        self.color = False
        self.public_number = card.public_number
        self.public_color = card.public_color
        self.in_your_hand = True

    def __str__(self):
        return "Card(?:?,Public:{public_number}:{public_color})".format(public_number=self.public_number,
                                                                        public_color=self.public_color)

    def __repr__(self):
        return str(self)

    def matches(self, valid_colors=None, valid_numbers=None):
        return self.does_color_match(valid_colors) and self.does_number_match(valid_numbers)

    def does_color_match(self, valid_colors=None):
        return not valid_colors or self.public_color.matches(valid_colors)

    def does_number_match(self, valid_numbers=None):
        if isinstance(valid_numbers, int):
            valid_numbers = tuple(valid_numbers)
        return not valid_numbers or self.public_number in valid_numbers

    # Todo: Figure out if this is unneeded. Players shouldn't run it on other cards, but it doesn't hurt anything
    def make_public(self, information_type):
        raise Exception("Cannot make YourCards public because actual attributes are hidden.")

