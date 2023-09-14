import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(__file__).parents[2]))
import unittest
from app.calculators import dealer

class TestCardDealing(unittest.TestCase):

    def test_dealRandomPlayerCard(self):
        current_deck = ["A-S", "K-H", "Q-D", "J-C"]
        player_cards = []
        dealt_card = dealer.deal_random_player_card(current_deck, player_cards)

        self.assertEqual(len(player_cards), 1)
        self.assertEqual(player_cards[0], dealt_card)
        self.assertNotIn(dealt_card, current_deck)

    def test_dealRandomDealerCard(self):
        current_deck = ["A-S", "K-H", "Q-D", "J-C"]
        dealer_cards = []
        dealt_cards = dealer.deal_random_dealer_card(current_deck, dealer_cards)

        self.assertEqual(dealer_cards, dealt_cards)
        self.assertEqual(len(dealer_cards), len(dealt_cards))
        self.assertNotIn(dealt_cards[-1], current_deck)

if __name__ == '__main__':
    unittest.main()