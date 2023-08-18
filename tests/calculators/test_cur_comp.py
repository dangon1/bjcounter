import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(__file__).parents[2]))
import unittest
from app.calculators import deck_calc
from app.constants.constants import NUMBER_OF_DECKS
from app.cur_comp import CurComp

class TestCurComp(unittest.TestCase):

    def test_get_dealer_probs(self):
        global CurComp
        cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))
        dealer_probs = CurComp.get_dealer_probs(cur_comp)

        self.assertEqual(dealer_probs, 1)

if __name__ == '__main__':
    unittest.main()