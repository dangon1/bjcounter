import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(Path(__file__).parents[2]))
import unittest
from app.calculators import deck_calc
from app.constants.constants import NUMBER_OF_DECKS
import csv
from app.cur_comp import CurComp


class TestCurComp(unittest.TestCase):

    def test_get_dealer_probs(self):
        global CurComp
        cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))
        df_t_hard, df_t_soft = CurComp.get_dealer_probs(cur_comp)

        for j in range(14, -1, -1):
            for i in range(1, 7):
                df_t_hard.iloc[(i, j)] = round(df_t_hard.iloc[(i, j)], 10)
                if j >= 10 or j <= 4:
                    df_t_soft.iloc[(i, j)] = round(df_t_soft.iloc[(i, j)], 10)

        # Save the DataFrames to CSV files
        df_t_hard.to_csv('df_t_hard.csv', index=False)
        df_t_soft.to_csv('df_t_soft.csv', index=False)

        self.assert_csv_files_equal('df_t_hard.csv', 'expected_df_t_hard.csv')
        self.assert_csv_files_equal('df_t_soft.csv', 'expected_df_t_soft.csv')

    def test_get_stand_probs(self):
        global CurComp
        cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))
        stand_hard, stand_soft = CurComp.get_stand_probs(cur_comp)

        for j in range(0, 10):
            for i in range(1, 26):
                stand_hard.iloc[(i, j)] = round(stand_hard.iloc[(i, j)], 10)

        for j in range(0, 10):
            for i in range(1, 21):
                stand_soft.iloc[(i, j)] = round(stand_soft.iloc[(i, j)], 10)

        # Save the DataFrames to CSV files
        stand_hard.to_csv('stand_hard.csv', index=False)
        stand_soft.to_csv('stand_soft.csv', index=False)

        self.assert_csv_files_equal('stand_hard.csv', 'expected_hard_stand.csv')
        self.assert_csv_files_equal('stand_soft.csv', 'expected_soft_stand.csv')

    def test_get_hit_probs(self):
        # def get_prob_hard_total_hit(self, df_t_hard, df_t_soft, x):
        global CurComp
        cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))
        stand_hard, stand_soft = CurComp.get_stand_probs(cur_comp)
        # hit_hard look at formula in table not copy from stand
        hit_hard, hit_soft = stand_hard, stand_soft
        hs_hard, hs_soft = hit_hard, hit_soft

        for j in range(0, 10):
            for i in range(1, deck_calc.idx_from_hard_shd(31)):
                
                hs_hard[j][deck_calc.idx_from_hard_shd(i) + 1] = max(stand_hard[j][deck_calc.idx_from_hard_shd(i) + 1],
                                                           hit_hard[j][deck_calc.idx_from_hard_shd(i) + 1])
                if i < 21:
                    hs_soft[j][deck_calc.idx_from_hard_shd(i) + 1] = max(stand_soft[j][deck_calc.idx_from_hard_shd(i) + 1],
                                                               hit_soft[j][deck_calc.idx_from_hard_shd(i) + 1])
        print("HS_HARD")
        print(hs_hard)
        #
        print("HS_SOFT")
        print(hs_soft)
        # TODO fazer de tras pra frente para ter valores
        for x in range(18, 1, -1):
            hard_total = cur_comp.get_prob_hard_total_hit(hs_hard, hs_soft, x)
            print(hard_total)
            #TODO until '2': -0.2533899859666381, is correct. Then '2': 0.031780496555725304 should be 0.2383507495

       

    def assert_csv_files_equal(self, expected_filename, actual_filename):
        # round_csv(expected_filename, 'expected_df_t_hard_2', 10)
        with open(expected_filename, newline='') as expected_file, open(actual_filename, newline='') as actual_file:
            expected_rows = list(csv.reader(expected_file))
            actual_rows = list(csv.reader(actual_file))

            self.assertEqual(expected_rows, actual_rows)

if __name__ == '__main__':
    unittest.main()
