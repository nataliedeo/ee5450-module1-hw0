import logging
from typing import List, Union, Tuple
import random
from dataclasses import dataclass
import numpy as np

#################################################################################
# EE 5450 Module 1 Homework 0
#
# This is a blackjack game stub.  Unit tests are in test_blackjack.py.
#
# TODO: Complete the functions and docstrings below so that the unit tests pass.
#################################################################################


BLACKJACK_INSTRUCTIONS = {
    'English': {
        'WELCOME': 'Welcome to Blackjack!',
        'NUM_PLAYERS': 'How many players? ',
        'NUM_DECKS': 'How many decks? ',
        'START': 'Starting game... ',
        'PLAYER_INST': 'Type h to hit or s to stay.',
        'PLAYER_HIT': 'Chose to hit and drew',
        'PLAYER_STAY': 'Chose to Stay.',
        'DEALER_HIT': 'Dealer hit and drew a',
        'DEALER_STAY': 'Dealer stays at',
        'PLAY_AGAIN': 'Type y to play another game: '
    },
    # TODO: add another language here for fun! Feel free to use Google Translate.
}


@dataclass
class Card(object):
    suit: str
    number: int

    @staticmethod
    def _convert_card_num_to_str(num) -> str:
        if num == 1:
            return 'Ace'
        elif num == 11:
            return 'Jack'
        elif num == 12:
            return 'Queen'
        elif num == 13:
            return 'King'
        else:
            return str(num)

    def __str__(self):
        return f'{self._convert_card_num_to_str(self.number)} of {self.suit}'


class Blackjack(object):
    """ Blackjack game object.
    """
    def __init__(self, num_decks: int = 1, num_players: int = 1):
        """
        Constructor for the Blackjack game object.

        :param num_decks: number of decks in this game; defaults to 1 deck
        :param num_players: number of players in this game; defaults to 1 player
        """
        self._SUITS = ("Spades", "Hearts", "Clubs", "Diamonds")
        self._ACE_LOW = 1
        self._ACE_HIGH = 11
        self._LOWEST_CARD = 1
        self._HIGHEST_CARD = 13
        self._WINNING_SUM = 21
        self._MAX_ROYALTY = 10
        self._num_decks = num_decks
        self._num_players = num_players
        self._card_stack = self._create_stack(num_decks)
        self._dealer_stack = []
        self._player_stacks = [[] for _ in range(self._num_players)]
        self._player_dones = [False for _ in range(self._num_players)]
        self._current_turn = 0

    def _create_stack(self, num_decks: int) -> List[Card]:
        """
        Creates the stack of the cards (52 * num_decks), shuffled.

        :param num_decks: number of decks to use
        :return: stack of all card objects, shuffled.
        """
        pass

    def calculate_optimal_ace_sum(self, number_of_ace_cards: int, current_sum: int,
                                  target_sum: int) -> int:
        """
        Greedy approximation search for optimal sum of Ace cards in a player's stack.

        :param number_of_ace_cards: number of Ace cards in the stack
        :param current_sum: current sum without Ace cards
        :param target_sum: target sum after ace cards
        :return: the optimal Ace-only sum to use
        """
        pass

    def _calculate_no_aces(self, stack: List[int]) -> int:
        """
        Calculates sum of a stack without aces

        :param stack: List of all the card numbers without Aces
        :return: Sum of clipped cards (clipped to self._MAX_ROYALTY)
        """
        pass

    def _calculate_stack_sum(self, stack: List[Card]) -> int:
        """
        Calculates the blackjack sum of a stack (list) of Card objects.

        :param stack: List of Card objects to calculate the sum with
        :return: The sum that minimizes the distance to optimal_sum
        """
        pass

    def _draw_card(self) -> Card:
        """
        Draw a card from the main stack.

        :return: Card object
        """
        pass

    def _dealer_draw(self, silent: bool = False) -> bool:
        """
        Play the dealer, which is forced to stay at 17.

        :param silent: True if this is a silent draw (no logging).
        :return: dealer is done hitting.
        """
        pass

    def _player_draw(self, player_idx: int) -> Card:
        """
        Draw a card for the player.

        :param player_idx:  The player to which a card should be drawn
        :return: The drawn card (already placed in the player's stack)
        """
        pass

    def _player_choice(self, player_idx: int) -> bool:
        """
        Ask player for the choice.

        :param player_idx:
        :return: player is done hitting
        """
        player_input = 'g'
        while player_input not in ('h', 's'):
            player_input = input(f"Player {player_idx}: {BLACKJACK_INSTRUCTIONS['English']['PLAYER_INST']} ")
            if player_input == 'h':
                drawn_card = self._player_draw(player_idx)
                print(f"Player {player_idx}: {BLACKJACK_INSTRUCTIONS['English']['PLAYER_HIT']} {drawn_card}")
                return self._calculate_stack_sum(self._player_stacks[player_idx]) > 21
            elif player_input == 's':
                print(f"Player {player_idx}: {BLACKJACK_INSTRUCTIONS['English']['PLAYER_STAY']}")
                return True

    def _get_sums(self) -> Tuple[int, List[int]]:
        """
        Computes the dealer and player sums using self._calculate_stack_sum()

        :return: (dealer_sum, [player_sum])
        """
        pass

    def _compute_winner(self, dealer_sum: int, player_sum: int) -> str:
        """
        Computes the winner, between the dealer and player.

        Dealer wins if:
        - Dealer's sum is 21 and the player's sum is not
        - Player has busted (greater than 21)

        Player wins if:
        - Player has a higher sum than the dealer but is <= 21

        No one wins if both player and dealer have 21.

        :param dealer_sum: optimal sum of the dealer's stack
        :param player_sum: optimal sum of the player's stack
        :return: the winner: 'NONE', 'DEALER', or 'PLAYER'
        """
        pass

    def _compute_winners(self) -> List[str]:
        """
        Computes the winners of the current game.

        :return: List of the winner between each player and the dealer.
        """
        dealer_sum, player_sums = self._get_sums()
        return [self._compute_winner(dealer_sum, player_sum) for player_sum in player_sums]

    def print_dealer_single(self):
        print(f"Dealer: {self._dealer_stack[0]}")

    def print_dealer_full(self):
        print(f"Dealer: {''.join([str(card) for card in self._dealer_stack])}"
              f" at sum {self._calculate_stack_sum(self._dealer_stack)}")

    def print_player_stack(self, player_idx: int):
        player_stack = self._player_stacks[player_idx]
        player_sum = self._calculate_stack_sum(player_stack)
        print(f"Player {player_idx}: {''.join([str(card) for card in player_stack])} at sum {player_sum}")

    def _initial_deal(self):
        """
        Does the initial deal, which does:
        1. Public (non-silent) dealer draw.
        2. Silent dealer draw.
        3. Draws twice for each player.
        """
        pass

    def run(self):
        print(BLACKJACK_INSTRUCTIONS['English']['START'])
        self._initial_deal()
        self.print_dealer_single()
        while not all(self._player_dones):
            for player_idx in range(self._num_players):
                if self._current_turn < 1:
                    self.print_player_stack(player_idx)
                self._player_dones[player_idx] = self._player_choice(player_idx)
                self.print_player_stack(player_idx)
            self._current_turn += 1
        while not self._dealer_draw():
            self.print_dealer_full()
        print(f"Final winners: {self._compute_winners()}")
        return


def main():
    play_another = True
    while play_another:
        print(f"{BLACKJACK_INSTRUCTIONS['English']['WELCOME']}")
        num_players_input = int(input(f"{BLACKJACK_INSTRUCTIONS['English']['NUM_PLAYERS']}"))
        num_decks_input = int(input(f"{BLACKJACK_INSTRUCTIONS['English']['NUM_DECKS']}"))
        the_game = Blackjack(num_decks=num_decks_input, num_players=num_players_input)
        the_game.run()
        play_another_input = input(f"{BLACKJACK_INSTRUCTIONS['English']['PLAY_AGAIN']}")
        if play_another_input != 'y':
            play_another = False
    return False


if __name__ == '__main__':
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=print)
    main()
