import pandas as pd

from app.constants.constants import UNITY_NORMALIZED_RANK

class CurComp:
    def __init__(self, cur_deck):
        self.cur_deck = cur_deck

    def get_qty_rank(self, rank):
        rank_qty = len([card.rank for card in self.cur_deck if card.rank in rank])
        return rank_qty

    def get_next_card_of_rank(self, rank):
        for card in self.cur_deck:
            if card.rank is rank:
                return card
        return None

    def get_normalized_prob_rank(self, rank):
        return self.get_prob_rank(rank) / UNITY_NORMALIZED_RANK

    def get_prob_rank(self, rank):
        if rank == "T" or rank == "10":
            rank_qty = self.get_qty_rank("10") \
                       + self.get_qty_rank("J") \
                       + self.get_qty_rank("Q") \
                       + self.get_qty_rank("K")
        else:
            rank_qty = self.get_qty_rank(rank)
        prob_rank = (rank_qty / len(self.cur_deck))
        return prob_rank

    def get_prob_hard_total(self, df_t_hard, df_t_soft, idx_column_hard_total, idx_row_hard_total):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "A"]
        result = 0

        for rank in ranks:
            normalized_prob_rank = self.get_normalized_prob_rank(rank)
            if rank in ["2", "3", "4", "5", "6", "7", "8", "9", "T"]:
                result += normalized_prob_rank * df_t_hard[idx_column_hard_total + ranks.index(rank) + 2][
                    idx_row_hard_total]
            elif rank == "A":
                result += normalized_prob_rank * df_t_soft[idx_column_hard_total + 1][idx_row_hard_total]

        return result / 13

    def get_prob_soft_total(self, df_t_soft, idx_column_soft_total, idx_row_soft_total):
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T"]
        result = 0

        for rank in ranks:
            normalized_prob_rank = self.get_normalized_prob_rank(rank)
            result += normalized_prob_rank * df_t_soft[idx_column_soft_total + ranks.index(rank) + 1][
                idx_row_soft_total]

        return result / 13

    def show_matrixes(self):
        self.get_dealer_probs()
        self.get_stand_probs()

    def get_dealer_probs(self):
        # Set display options to show all rows and columns
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        dealer_hard = {
            "Outcome": list(range(2, 32)),
            "Bust": [0] * 15 + [0] + [0] + [0] + [0] + [0] + [1] * 10,
            "17": [0] * 15 + [1] + [0] + [0] + [0] + [0] + [0] * 10,
            "18": [0] * 15 + [0] + [1] + [0] + [0] + [0] + [0] * 10,
            "19": [0] * 15 + [0] + [0] + [1] + [0] + [0] + [0] * 10,
            "20": [0] * 15 + [0] + [0] + [0] + [1] + [0] + [0] * 10,
            "21": [0] * 15 + [0] + [0] + [0] + [0] + [1] + [0] * 10
        }
        # Therefore df_transposed[3][5] is column 3, line 5
        df_t_hard = pd.DataFrame(dealer_hard).T

        dealer_soft = {
            "Outcome": list(range(12, 32)),
            "Bust": [0] * 5 + [0] + [0] + [0] + [0] + [0] + [0] * 5 + [0] + [0] + [0] + [0] + [0],
            "17": [0] * 5 + [1] + [0] + [0] + [0] + [0] + [0] * 5 + [1] + [0] + [0] + [0] + [0],
            "18": [0] * 5 + [0] + [1] + [0] + [0] + [0] + [0] * 5 + [0] + [1] + [0] + [0] + [0],
            "19": [0] * 5 + [0] + [0] + [1] + [0] + [0] + [0] * 5 + [0] + [0] + [1] + [0] + [0],
            "20": [0] * 5 + [0] + [0] + [0] + [1] + [0] + [0] * 5 + [0] + [0] + [0] + [1] + [0],
            "21": [0] * 5 + [0] + [0] + [0] + [0] + [1] + [0] * 5 + [0] + [0] + [0] + [0] + [1],
        }

        # Therefore df_transposed[3][5] is column 3, line 5
        df_t_soft = pd.DataFrame(dealer_soft).T

        for j in range(14, -1, -1):
            for i in range(1, 7):
                hard_total = self.get_prob_hard_total(df_t_hard, df_t_soft, j, i)
                df_t_hard.iloc[(i, j)] = hard_total
                if j >= 10:
                    df_t_soft.iloc[(i, j)] = hard_total
                if j <= 4:
                    df_t_soft.iloc[(i, j)] = self.get_prob_soft_total(df_t_soft, j, i)
        print("HARD")
        print(df_t_hard)
        print("SOFT")
        print(df_t_soft)

        # Save the DataFrames to CSV files
        # df_t_hard.to_csv('df_t_hard.csv', index=False)
        # df_t_soft.to_csv('df_t_soft.csv', index=False)
        return df_t_hard

    def get_stand_probs(self):
        stand_hard = {
            "Hard": list(range(2, 11)) + ["Ace"],
            "4": [0] * 10,
            "5": [0] * 10,
            "6": [0] * 10,
            "7": [0] * 10,
            "8": [0] * 10,
            "9": [0] * 10,
            "11": [0] * 10,
            "12": [0] * 10,
            "13": [0] * 10,
            "14": [0] * 10,
            "15": [0] * 10,
            "16": [0] * 10,
            "17": [0] * 10,
            "18": [0] * 10,
            "19": [0] * 10,
            "20": [0] * 10,
            "21": [0] * 10,
            "22": [-1] * 10,
            "23": [-1] * 10,
            "24": [-1] * 10,
            "25": [-1] * 10,
            "26": [-1] * 10,
            "27": [-1] * 10,
            "28": [-1] * 10,
            "29": [-1] * 10,
            "30": [-1] * 10,
            "31": [-1] * 10
        }

        stand_hard = pd.DataFrame(stand_hard).T

        for j in range(0, 10, 1):
            for i in range(1, 23):
                self.get_prob_stand_hard(stand_hard, j, i)

        print("STAND_HARD")
        print(stand_hard)

    def get_prob_stand_hard(self, stand_hard, idx_j, idx_i):
        # TODO do the calculation here. On spreadsheet is using american dealer odds, may need to redo dealer matrix
        stand_hard[idx_j][idx_i] = "X"