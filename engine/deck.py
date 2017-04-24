from engine.card import Card
from engine.color import Color
from random import shuffle, Random


class Deck(object):

    def __init__(self,
                 colors=(Color('red'), Color('yellow'), Color('green'), Color('white'), Color('blue')),
                 numbers=(1, 1, 1, 2, 2, 3, 3, 4, 4, 5),
                 seed=None,
                 do_shuffle=True):
        self.card_colors = colors
        self.card_numbers = numbers

        self.card_list = []
        for color in self.card_colors:
            for number in self.card_numbers:
                self.card_list.append(Card(number, color))

        if do_shuffle:
            self.shuffle(seed)

    def shuffle(self, seed=None):
        if seed:
            Random(seed).shuffle(self.card_list)
        else:
            shuffle(self.card_list)

    def __len__(self):
        return len(self.card_list)

    def __str__(self):
        return "Deck: {card_list}".format(card_list=self.card_list)

    def __repr__(self):
        return str(self)

    def draw_card(self):
        if len(self.card_list) > 0:
            return self.card_list.pop()
        return False


class WildDeck(Deck):

    def __init__(self,
                 colors=(Color('red'), Color('yellow'), Color('green'), Color('white'), Color('green')),
                 has_wild=True,
                 numbers=(1, 1, 1, 2, 2, 3, 3, 4, 4, 5),
                 seed=None,
                 do_shuffle=True):
        super(WildDeck, self).__init__(colors=list(colors), numbers=numbers, seed=seed, do_shuffle=False)

        self.has_wild = has_wild
        if self.has_wild:
            wild_color = Color('wild', color_matches=self.card_colors, match_name=False)
            self.card_colors.append(wild_color)
            for number in self.card_numbers:
                self.card_list.append(Card(number, wild_color))

        if do_shuffle:
            self.shuffle(seed)
