import pandas as pd
from fastapi import HTTPException

from app.calculators import deck_calc
from app.constants.constants import UNITY_NORMALIZED_RANK, PEAKS_FOR_BJ

HARD_TOTALS_MATRIX_OFFSET = 2
SOFT_TOTALS_MATRIX_OFFSET = 12


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

    def show_matrixes(self, dealer_cards):
        self.get_dealer_probs()
        # self.get_stand_probs(dealer_cards)

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

        for j in range(get_idx_from_sum_total_hard(16), -1, -1):
            for i in range(1, 7):
                hard_total = self.get_prob_hard_total(df_t_hard, df_t_soft, j, i)
                df_t_hard.iloc[(i, j)] = hard_total
                if j >= 10:
                    df_t_soft.iloc[(i, j)] = hard_total
                if j <= 4:
                    df_t_soft.iloc[(i, j)] = self.get_prob_soft_total(df_t_soft, j, i)

        if PEAKS_FOR_BJ:
            # American peaking rule on dealer for 10s and Aces
            for j in range(get_idx_from_sum_total_hard(11), get_idx_from_sum_total_hard(9), -1):
                for i in range(1, 7):
                    hard_total = recalculate_for_peak_rule(df_t_hard, df_t_soft, get_idx_from_idx_hard(j), i)
                    df_t_hard.iloc[(i, j)] = hard_total

        print("HARD")
        print(df_t_hard)
        print("SOFT")
        print(df_t_soft)

        # Save the DataFrames to CSV files
        # df_t_hard.to_csv('df_t_hard.csv', index=False)
        # df_t_soft.to_csv('df_t_soft.csv', index=False)

        return df_t_hard


def recalculate_for_peak_rule(df_t_hard, df_t_soft, column_total, i):
    if column_total == 10:
        idx_sum_20 = get_idx_from_sum_total_hard(20)
        line_new_value = 0
        for j in range(get_idx_from_sum_total_hard(12), idx_sum_20):
            line_new_value += df_t_hard[j][i]

        line_new_value += (4 * df_t_hard[idx_sum_20][i])
        return line_new_value / 12
    if column_total == 11:
        line_new_value = 0
        for j in range(get_idx_from_sum_total_soft(12), get_idx_from_sum_total_soft(20) + 1):
            line_new_value += df_t_soft[j][i]
            print(df_t_soft[j][i])
        print("Line value:" + str((line_new_value / 9)) + "Value to replace:" + str(df_t_soft[column_total - 2][i]), "Column total:" + str(column_total))
        return line_new_value / 9

    def get_stand_probs(self, dealer_cards):
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
            probs_for_rank = self.calc_all_probs_dealer(j + 2)
            for i in range(1, 16 - 3):
                get_prob_stand_until_16(probs_for_rank, stand_hard, j, i)

        print("STAND_HARD")
        print(stand_hard)

    # method not used anywhere yet
    def calc_prob_dealer_bust_next_card(self, dealer_cards):
        sum_dealer_cards = deck_calc.calc_sum_hand(dealer_cards)
        if sum_dealer_cards >= 22:
            return 1
        elif 17 <= sum_dealer_cards < 22:
            return 0
        else:
            distance_from_22 = 22 - sum_dealer_cards
            if distance_from_22 > 10:
                return 0
            prob_busting = 0
            for i in range(distance_from_22, 11):
                print("calculating prob of i " + str(i))
                prob_busting += self.get_normalized_prob_rank(str(i))
                print("prob of i:  " + str(prob_busting))
            return prob_busting / 13

    def calc_all_probs_dealer(self, sum_dealer_cards):
        if sum_dealer_cards < 2:
            raise HTTPException(status_code=400, detail=f"Dealer hasn't been dealt any cards.")
        dealer_probs = self.get_dealer_probs()
        prob_bust = dealer_probs.iloc[1, int(sum_dealer_cards - 2)]
        prob_17 = dealer_probs.iloc[2, int(sum_dealer_cards - 2)]
        prob_18 = dealer_probs.iloc[3, int(sum_dealer_cards - 2)]
        prob_19 = dealer_probs.iloc[4, int(sum_dealer_cards - 2)]
        prob_20 = dealer_probs.iloc[5, int(sum_dealer_cards - 2)]
        prob_21 = dealer_probs.iloc[6, int(sum_dealer_cards - 2)]
        return {"bust": prob_bust, "17": prob_17, "18": prob_18, "19": prob_19, "20": prob_20, "21": prob_21}


def get_prob_stand_until_16(probs_for_rank, stand_hard, idx_j, idx_i):
    # Get the probability of the dealer going Bust
    prob_bust = probs_for_rank.get("bust")

    # Get the sum of probabilities for dealer scores 17 through 21
    prob_high_scores = (
            probs_for_rank.get("17")
            + probs_for_rank.get("18")
            + probs_for_rank.get("19")
            + probs_for_rank.get("20")
            + probs_for_rank.get("21")
    )
    # print("probBust" + str(prob_bust))
    # print("prob_high_scores" + str(prob_high_scores))
    stand_hard[idx_j][idx_i] = prob_bust - prob_high_scores


def get_idx_from_idx_hard(sum1):
    return sum1 + HARD_TOTALS_MATRIX_OFFSET


def get_idx_from_sum_total_hard(sum1):
    return sum1 - HARD_TOTALS_MATRIX_OFFSET

def get_idx_from_sum_total_soft(sum1):
    return sum1 - SOFT_TOTALS_MATRIX_OFFSET