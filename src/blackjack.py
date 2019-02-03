"""
Program: Blackjack

Implement the game of blackjack, using the previously built Card and ChipBank classes,
as well as a new class to represent a game of blackjack. Write additional classes as
needed to support the functionality of the blackjack game.

Author: Michael Boyd
Date: 5/30/18
"""
from casino_night import *


class BlackjackTable:
    def __init__(self):
        self._deck = []
        self._player_cards = []
        self._dealer_cards = []
        self._player_points = 0
        self._dealer_points = 0
        self._wager = 0
        self._winnings = 0
        self._game_status = None

    def game_start(self):
        """Shuffle the deck and deal the first two cards for both the dealer and player.
        Dealer's second card is drawn face down."""
        self._game_status = "Start"
        self._shuffle_deck()

        # Cards are drawn for the player, the hand is shown, and the win condition is
        # checked for getting a blackjack
        self._draw_card("Player")
        self._draw_card("Player")
        self._show_hand("Player")
        if self._check_game_over() == "Blackjack! You win!":
            self._game_status = "Game Over"
            return

        # Cards are drawn for the dealer, the first is set face down, and the hand is shown
        self._draw_card(face="down")
        self._draw_card()
        self._show_hand()

    def _shuffle_deck(self):
        """Create 52 cards representing a full deck of playing cards and place them
        in the deck in random order."""
        for i in range(52):
            card = Card(i)
            self._deck.append(card)
        random.shuffle(self._deck)

    def _draw_card(self, person="", face=None):
        """Draw the top card off the deck and add it to the person's hand"""
        card = self._deck.pop()

        # Show each card as it is drawn if it is not the beginning of the game
        if self._game_status != "Start":
            if person == "Player":
                print("You draw: " + str(card))
            else:
                print("Dealer draws: " + str(card))

        # Add the card to the person's hand and the value to the person's point count
        if person == "Player":
            self._player_cards.append(card)
            self._player_points += card.value
        else:
            if face:
                card.face_down()
            self._dealer_cards.append(card)
            self._dealer_points += card.value

    def _show_hand(self, person=""):
        """Output the person's current hand"""
        hand = ""
        if person == "Player":
            if self._game_status == "Start":
                hand += "Your starting hand: "
            else:
                hand += "Your hand is now: "
            for card in self._player_cards:
                if card != self._player_cards[0]:
                    hand += ", "
                hand += str(card)
        else:
            if self._game_status == "Start":
                hand += "Dealer's starting hand: "
            elif self._game_status == "Dealer's Turn":
                hand += "Dealer's hand is now: "
            else:
                hand += "Dealer stands with: "
            for card in self._dealer_cards:
                if card != self._dealer_cards[0]:
                    hand += ", "
                hand += str(card)
        print(hand)

    def stand_or_hit(self):
        """On a person's turn, they can draw as many cards as they want
        (until they bust) and/or keep their hand for the rest of the current
        game"""
        # Determine who's turn it is
        if self._game_status == "Start":
            self._game_status = "Player's Turn"  # The player's turn follows after the starting phase
        else:
            self._game_status = "Dealer's Turn"  # Dealer goes last
            self._dealer_cards[0].face_up()  # Turn over the dealer's face down card

        stand = False
        while not stand:
            if self._game_status == "Player's Turn":
                player_input = input("STAND or HIT: ")
                if player_input == "HIT":
                    self._draw_card("Player")
                    self._show_hand("Player")
                elif player_input == "STAND":
                    stand = True
            else:
                if self._dealer_points < 17:  # The dealer always hits if under 17 points
                    self._draw_card()
                    self._show_hand()
                else:
                    stand = True
                    self._game_status = "Turns Over"  # Indicates that both the player and dealer now stand
                    self._show_hand()

            result = self._check_game_over()
            if result:
                print(result)
                self._game_status = "Game Over"
                stand = True

    def _check_game_over(self):
        """Determine who wins and who loses based on the game status and
        the number of points the player and dealer have."""
        if self._game_status == "Start" and self._player_points == 21:
            self._winnings = self.wager * 2
            return "Blackjack! You win!"
        elif self._game_status == "Player's Turn" and self._player_points > 21:
            return "You bust!"
        elif self._game_status == "Dealer's Turn" and self._dealer_points > 21:
            self._winnings = self.wager * 2
            return "Dealer busts, you win!"
        elif self._game_status == "Turns Over":
            if self._dealer_points > self._player_points:
                return "The dealer beats your hand!"
            elif self._dealer_points < self._player_points:
                self._winnings = self.wager * 2
                return "You beat the dealer's hand!"
            elif self._player_points == self._dealer_points:
                self._winnings = self.wager
                return "It's a tie!"
        return None

    @property
    def wager(self):
        return self._wager

    @wager.setter
    def wager(self, amount):
        self._wager = amount

    @property
    def winnings(self):
        return self._winnings

    @property
    def game_status(self):
        return self._game_status


def main():
    player_account = ChipBank(250)
    print("Your starting chip balance is: " + str(player_account) + "\n")

    while True:
        table = BlackjackTable()

        # Receive input from the user to wager money or quit the game
        wager = int(input("Enter a wager (whole numbers only) or 0 to quit: "))
        if wager == 0:
            quit()
        else:
            # Wager the desired amount if the player has enough money
            if player_account.balance >= wager:
                player_account.withdraw(wager)
                table.wager = wager
            # Otherwise, wager the rest of the player's balance
            else:
                player_account.withdraw(player_account.balance)
                table.wager = player_account.balance

        table.game_start()
        while table.game_status != "Game Over":
            table.stand_or_hit()

        # Deposit the player's winnings into their account and display the new balance
        player_account.deposit(table.winnings)
        print("Your chip balance is: " + str(player_account) + "\n")
        if player_account.balance == 0:  # If the player is out of money, end the program
            quit()


if __name__ == "__main__":
    main()
