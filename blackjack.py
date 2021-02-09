import logging
from typing import List, Union, Tuple
import random
from dataclasses import dataclass

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
    'Fiji Hindi': {
        'WELCOME': 'Au Blackjack kehlo!',
        'NUM_PLAYERS': 'Kehtna kehle? ',
        'NUM_DECKS': 'Kehtna deck manta? ',
        'START': 'Ab hum lon kehlega... ',
        'PLAYER_INST': 'Liko h ek aur lo neto s kuch nahi karo.',
        'PLAYER_HIT': 'Ek aur lo aur lelia ek',
        'PLAYER_STAY': 'Kuch nahi karo.',
        'DEALER_HIT': 'Dealer ek aur lais ahbi aur lelise ek',
        'DEALER_STAY': 'Dealer kuch nai kare abhi.',
        'PLAY_AGAIN': 'Liko y ek aur baar kehlo: '
    },
    'Spanish': {
        'WELCOME': 'Bienvenidos a Blackjack!',
        'NUM_PLAYERS': '¿Cuantos jugadores? ',
        'NUM_DECKS': '¿Cuantos barajas de cartes? ',
        'START': 'Comenza... ',
        'PLAYER_INST': 'Escribe hache a golpear o ese a permanecer.',
        'PLAYER_HIT': 'Eligio a golpear y obtene un/una',
        'PLAYER_STAY': 'Eligio a permanecer a.',
        'DEALER_HIT': 'Distribuidor golpea y obtene un/una',
        'DEALER_STAY': 'Distribuidor permanece a',
        'PLAY_AGAIN': 'Escribe i greiga a jugar el juego otra ves: '
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
        for s in self._SUITS:
            for i in range(1, 13):
                self._card_stack.append(Card(s, i))

        random.shuffle(self._card_stack)

        return self._card_stack

    def calculate_optimal_ace_sum(self, number_of_ace_cards: int, current_sum: int,
                                  target_sum: int) -> int:
        """
        Greedy approximation search for optimal sum of Ace cards in a player's stack.

        :param number_of_ace_cards: number of Ace cards in the stack
        :param current_sum: current sum without Ace cards
        :param target_sum: target sum after ace cards
        :return: the optimal Ace-only sum to use
        """
        k = 0
        optimal_ace_sum = 0

        number_of_ace_cards = self._player_stacks.count(1)  # Unsure how correct this is AAAAAAA
        target_sum = 21 - current_sum

        while k <= number_of_ace_cards:
            if target_sum / 11 >= 1:
                optimal_ace_sum += 11
            else:
                optimal_ace_sum += 1
            k += 1

        return optimal_ace_sum

    def _calculate_no_aces(self, stack: List[int]) -> int:
        """
        Calculates sum of a stack without aces

        :param stack: List of all the card numbers without Aces
        :return: Sum of clipped cards (clipped to self._MAX_ROYALTY)
        """
        k = 0
        curr_sum = 0

        while k <= len(stack):
            if stack[k] > self._MAX_ROYALTY:
                curr_sum = curr_sum + self._MAX_ROYALTY
            elif stack[k] > 1:
                curr_sum = curr_sum + stack[k]

        return curr_sum

    def _calculate_stack_sum(self, stack: List[Card]) -> int:
        """
        Calculates the blackjack sum of a stack (list) of Card objects.

        :param stack: List of Card objects to calculate the sum with
        :return: The sum that minimizes the distance to optimal_sum
        """
        no_aces = Blackjack._calculate_no_aces(self, stack)
        only_aces = Blackjack.calculate_optimal_ace_sum(self, stack)

        stack_sum = no_aces + only_aces

        return stack_sum

    def _draw_card(self) -> Card:
        """
        Draw a card from the main stack.
        :return: Card object
        """
        new_card = self._card_stack.pop(0)

        return new_card

    def _dealer_draw(self, silent: bool = False) -> bool:
        """
        Play the dealer, which is forced to stay at 17.
        :param silent: True if this is a silent draw (no logging).
        :return: dealer is done hitting.
        """
        dealer_stack = self.Blackjack._dealer_stack
        dealer_sum = Blackjack._calculate_stack_sum(self, self.Blackjack._dealer_stack)

        if [dealer_sum] < 17:
            draw_card = self._card_stack.pop(0)
            dealer_stack.append(draw_card)

        if not silent:
            print(draw_card)

        return silent

    def _player_draw(self, player_idx: int) -> Card:
        """
        :param player_idx:  The player to which a card should be drawn
        :return: The drawn card (already placed in the player's stack)
        """
        player_stack = self._player_stacks[player_idx]

        draw_card = self._card_stack.pop(0)
        player_stack[player_idx].append(draw_card)

        return draw_card

    def _player_choice(self, player_idx: int) -> bool:
        """
        Ask player for the choice.

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
        m = 0
        player_sum = []

        dealer_sum = self._calculate_stack_sum(self._dealer_stack)

        while m <= self._num_players:
            player_sum[m] = self._calculate_stack_sum(self, self._player_stack)
            m += 1

        return dealer_sum, player_sum

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
        if dealer_sum == 21 and player_sum != 21:
            return 'DEALER'
        elif player_sum > dealer_sum and player_sum <= 21:
            return 'PLAYER'
        elif player_sum == 21 and dealer_sum == 21:
            return 'NONE'
        else:
            return 'ERROR'

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
        print(f"Dealer: {', '.join([str(card) for card in self._dealer_stack])}",
              f" at sum {self._calculate_stack_sum(self._dealer_stack)}")

    def print_player_stack(self, player_idx: int):
        player_stack = self._player_stacks[player_idx]
        player_sum = self._calculate_stack_sum(player_stack)
        print(f"Player {player_idx}: {', '.join([str(card) for card in player_stack])} at sum {player_sum}")

    def _initial_deal(self):
        """
        Does the initial deal, which does:
        1. Public (non-silent) dealer draw.
        2. Silent dealer draw.
        3. Draws twice for each player.
        """
        draw_card_list = self._card_stack
        draw_card = draw_card_list[0]

        if len(self._card_stack) > 1:
            # Add card to dealer stack and announce
            draw_card = self._card_stack.pop(0)
            self._dealer_stack.append(draw_card)
            Blackjack.print_dealer_single(self)

            # Add card to dealer stack silently
            draw_card = self._card_stack.pop(0)
            self._dealer_stack.append(draw_card)

            # Add card to each player stack and announce
            for _ in range(self._num_players):
                draw_card = self._card_stack.pop(0)
                self.player_stack[_].append(draw_card)
                draw_card = self._card_stack.pop(0)
                self.player_stack[_].append(draw_card)
                Blackjack.print_player_stack(self, _)

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
