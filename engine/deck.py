from engine.card import Card
from random import shuffle, Random


class Deck(object):

    def __init__(self,
                 colors=('red', 'yellow', 'green', 'white', 'blue'),
                 numbers=(1, 1, 1, 2, 2, 3, 3, 4, 4, 5),
                 has_wild=False,
                 seed=None):
        self.card_colors = colors
        self.card_numbers = numbers
        self.has_wild = has_wild

        self.card_list = []
        for color in self.card_colors:
            for number in self.card_numbers:
                self.card_list.append(Card(number, color))

        if self.has_wild:
            for number in self.card_numbers:
                self.card_list.append(Card(number, 'wild'))

        self.shuffle(seed=seed)

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
