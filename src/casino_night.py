"""
Assignment 4: Casino Night

Components:
    - A card class that represents a standard playing card from a 52 card deck
    - A chip bank class that acts as a bank for casino chips

Author: Adam Zimmer and Michael Boyd
Date: 5/16/18
"""
import random


class Card:
    def __init__(self, card_num):
        self._suit = None
        self._rank = None
        self._value = None
        self._face_up = True
        self._create_card(card_num)

    def __str__(self):
        """Return a string with the rank and suit of a card.
        If the card is facedown, returns <facedown>"""
        if self._face_up is True:
            if self._rank:
                return str(self._rank + " of " + self._suit)
            else:
                return str(self._value) + " of " + self._suit
        else:
            return "<facedown>"

    def _create_card(self, card_num):
        """Method takes in a card number value, and uses that number
        to assign the passed in card a suit, rank and value.
        # suit_index = parameter value // num_cards_per_suit (13)
        # parameter_value -= suit_index * num_cards_per_suit (13)
        # Switch statement for any value >= 9 (Jack, King, Queen, Ace), manually set Rank and Value
        # Default - Rank = None, Value = parameter_value += 2"""
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        ranks = ['Jack', 'Queen', 'King', 'Ace']
        values = [10, 10, 10, 11]
        suit_index = card_num // 13  # Number of cards per suit
        self._suit = suits[suit_index]
        card_index = card_num - (suit_index * 13)  # Strip away the suit information, now have index between 0 and 12
        if card_index == 9:
            self._value = values[0]
            self._rank = ranks[0]
        elif card_index == 10:
            self._value = values[1]
            self._rank = ranks[1]
        elif card_index == 11:
            self._value = values[2]
            self._rank = ranks[2]
        elif card_index == 12:
            self._value = values[3]
            self._rank = ranks[3]
        else:
            self._value = card_index + 2
            self._rank = None

    def face_up(self):
        """Turns a card face up"""
        self._face_up = True

    def face_down(self):
        """Turns a card face down"""
        self._face_up = False

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return self._value


class ChipBank:
    chip_types = \
        [
            ["blacks", "greens", "reds", "blues"],
            [100, 25, 5, 1]
        ]

    def __init__(self, balance):
        self._balance = int(balance)

    def __str__(self):
        return self.calc_chips()

    def calc_chips(self):
        """Returns a string with the fewest number of chipsto represent the
        monetary balance"""
        to_return = ""
        counts = [0, 0, 0, 0]
        balance_inflated = int(self.balance * 100)

        for i in range(0, len(counts)):
            counts[i] = balance_inflated // int(self.chip_types[1][i] * 100)
            balance_inflated -= counts[i] * int(self.chip_types[1][i] * 100)
            to_return += str(counts[i]) + " " + self.chip_types[0][i]
            if i != len(counts)-1:
                to_return += ", "
        to_return += " - totaling $" + str(self.balance)

        return to_return

    def deposit(self, amount):
        """Add an amount to the balance"""
        self._balance += amount

    def withdraw(self, amount):
        """Subtract and amount from the balance"""
        if amount <= self.balance:
            self._balance -= amount

    @property
    def balance(self):
        return self._balance


if __name__ == "__main__":
    print("--Test card initialization and deck creation--")
    deck = []
    for i in range(52):
        my_card = Card(i)
        deck.append(my_card)
        my_card.face_up()
        print(my_card)
    print("")

    print("--Test card randomizer--")
    print(str(random.choice(deck)) + "\n")

    print("--Test card operations--")
    card = Card(37)
    card.face_up()
    print("Card: " + str(card))  # Queen of Clubs
    print("Value: " + str(card.value))  # 10
    print("Suit: " + card.suit)  # Clubs
    print("Rank: " + card.rank)  # Queen
    card.face_down()
    print("Turn it face down: " + str(card))  # <facedown>
    card.face_up()
    print("Turn it face up: " + str(card) + "\n")  # Queen of Clubs

    print("--Test ChipBank operations--")
    cs = ChipBank(149)
    print("Balance set at $149: " + str(cs.balance))  # 149
    print("Chip bank: " + str(cs))  # 1 blacks, 1 greens, 4 reds, 4 blues - totaling $149
    cs.deposit(7)
    print("Deposit $7: " + str(cs.balance))  # 156
    print("Chip bank: " + str(cs))  # 1 blacks, 2 greens, 1 reds, 1 blues - totaling $156
    cs.withdraw(84)
    print("Withdraw $84: " + str(cs.balance))  # 72
    print("Chip bank: " + str(cs))  # 0 blacks, 2 greens, 4 reds, 2 blues - totaling $72
    cs.deposit(120)
    print("Deposit $120: " + str(cs.balance))  # 192
    print("Chip bank: " + str(cs))  # 1 blacks, 3 greens, 3 reds, 2 blues - totaling $192
    cs.withdraw(300)
    print("Withdraw $300: " + str(cs.balance))  # 192
