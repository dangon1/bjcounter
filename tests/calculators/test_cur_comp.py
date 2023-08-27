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
                if j >= 10:
                    df_t_soft.iloc[(i, j)] = round(df_t_soft.iloc[(i, j)], 10)
                if j <= 4:
                    df_t_soft.iloc[(i, j)] = round(df_t_soft.iloc[(i, j)], 10)

        # Save the DataFrames to CSV files
        df_t_hard.to_csv('df_t_hard.csv', index=False)
        df_t_soft.to_csv('df_t_soft.csv', index=False)

        self.assert_csv_files_equal('df_t_hard.csv', 'expected_df_t_hard.csv')
        self.assert_csv_files_equal('df_t_soft.csv', 'expected_df_t_soft.csv')

    def assert_csv_files_equal(self, expected_filename, actual_filename):
        # round_csv(expected_filename, 'expected_df_t_hard_2', 10)
        with open(expected_filename, newline='') as expected_file, open(actual_filename, newline='') as actual_file:
            expected_rows = list(csv.reader(expected_file))
            actual_rows = list(csv.reader(actual_file))

            self.assertEqual(expected_rows, actual_rows)

if __name__ == '__main__':
    unittest.main()
