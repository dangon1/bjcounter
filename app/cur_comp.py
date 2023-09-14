import pandas as pd

from app.calculators import deck_calc
from app.calculators.deck_calc import get_idx_from_sum_total_hard, recalculate_for_peak_rule, get_idx_from_idx_hard, \
    get_prob_stand_until_16, idx_from_hard_shd, get_prob_stand
from app.constants.constants import UNITY_NORMALIZED_RANK, PEAKS_FOR_BJ


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
                print(str(result) + " i:" + str(idx_row_hard_total) + " j:" + str(idx_column_hard_total))
            elif rank == "A":
                result += normalized_prob_rank * df_t_soft[idx_column_hard_total + 1][idx_row_hard_total]

        return result / 13

    def get_prob_hard_total_hit(self, df_t_hard, df_t_soft, x):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "A"]
        result = 0

        for rank in ranks:
            for i in range(ranks.index(rank) + 1 + x, 10 + ranks.index(rank) + x):
                normalized_prob_rank = self.get_normalized_prob_rank(rank)
                prob_each = normalized_prob_rank * df_t_hard[ranks.index(rank)][i]
                print(str(prob_each) + " i:" + str(i) + " j:" + str(ranks.index(rank)))
                result += prob_each
            
            prob_ace = df_t_soft[ranks.index(rank)][x+4]
            print("prob ace:" +str(prob_ace) + " i:" + str(i) + " j:" + str(ranks.index(rank)))
            result += prob_ace
        return result

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
        self.get_hit_probs()

    def get_dealer_probs(self):
        # Set display options to show all rows and columns
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        dealer_hard = {
            "Outcome": [float(i) for i in range(2, 32)],
            "Bust": [0.0] * 15 + [0] + [0] + [0] + [0] + [0] + [1] * 10,
            "17": [0] * 15 + [1] + [0] + [0] + [0] + [0] + [0] * 10,
            "18": [0] * 15 + [0] + [1] + [0] + [0] + [0] + [0] * 10,
            "19": [0] * 15 + [0] + [0] + [1] + [0] + [0] + [0] * 10,
            "20": [0] * 15 + [0] + [0] + [0] + [1] + [0] + [0] * 10,
            "21": [0] * 15 + [0] + [0] + [0] + [0] + [1] + [0] * 10
        }
        # Therefore df_transposed[3][5] is column 3, line 5
        df_t_hard = pd.DataFrame(dealer_hard).T

        dealer_soft = {
            "Outcome": [float(i) for i in range(12, 32)],
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

        return df_t_hard, df_t_soft

    def get_stand_probs(self):
        stand_hard = {
            "Hard": list(range(2, 11)) + ["Ace"],
            "4": [0] * 10,
            "5": [0] * 10,
            "6": [0] * 10,
            "7": [0] * 10,
            "8": [0] * 10,
            "9": [0] * 10,
            "10": [0] * 10,
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

        # Fill from row 4 through 16
        all_probs_dealer = self.get_dealer_probs()[0]
        for j in range(0, 10):
            probs_for_rank = self.get_prob_per_rank(all_probs_dealer, j)
            for i in range(1, get_idx_from_sum_total_hard(16)):
                get_prob_stand_until_16(probs_for_rank, stand_hard, j, i)

        # Fill for row 17 through 21
        for j in range(0, 10):
            probs_for_rank = self.get_prob_per_rank(all_probs_dealer, j)
            for i in range(17, 22):
                stand_hard[j][idx_from_hard_shd(i) + 1] = get_prob_stand(probs_for_rank, i)

        stand_soft = {
            "Soft": list(range(2, 11)) + ["Ace"],
            "12": stand_hard.iloc[9],
            "13": stand_hard.iloc[10],
            "14": stand_hard.iloc[11],
            "15": stand_hard.iloc[12],
            "16": stand_hard.iloc[13],
            "17": stand_hard.iloc[14],
            "18": stand_hard.iloc[15],
            "19": stand_hard.iloc[16],
            "20": stand_hard.iloc[17],
            "21": stand_hard.iloc[18],
            "22": stand_hard.iloc[9],
            "23": stand_hard.iloc[10],
            "24": stand_hard.iloc[11],
            "25": stand_hard.iloc[12],
            "26": stand_hard.iloc[13],
            "27": stand_hard.iloc[14],
            "28": stand_hard.iloc[15],
            "29": stand_hard.iloc[16],
            "30": stand_hard.iloc[17],
            "31": stand_hard.iloc[18]
        }

        stand_soft = pd.DataFrame(stand_soft).T

        print("STAND_HARD")
        print(stand_hard)
        print("STAND_SOFT")
        print(stand_soft)
        return stand_hard, stand_soft

    def get_hit_probs(self):
        stand_hard, stand_soft = self.get_stand_probs()
        hit_hard, hit_soft = stand_hard, stand_soft
        hs_hard, hs_soft = hit_hard, hit_soft

        for j in range(0, 10):
            for i in range(1, idx_from_hard_shd(31)):
                hs_hard[j][idx_from_hard_shd(i) + 1] = max(stand_hard[j][idx_from_hard_shd(i) + 1],
                                                           hit_hard[j][idx_from_hard_shd(i) + 1])
                if i < 21:
                    hs_soft[j][idx_from_hard_shd(i) + 1] = max(stand_soft[j][idx_from_hard_shd(i) + 1],
                                                               hit_soft[j][idx_from_hard_shd(i) + 1])

        print("HS_HARD")
        print(hs_hard)
        
        print("HS_SOFT")
        print(hs_soft)
        for x in range(0, 17):
            hard_total = self.get_prob_hard_total_hit(hs_hard, hs_soft, x)

        print("HIT_HARD")
        print(hit_hard)

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

    def get_prob_per_rank(self, dealer_probs, idx_sum_dealer):
        prob_bust = dealer_probs.iloc[1, idx_sum_dealer]
        prob_17 = dealer_probs.iloc[2, idx_sum_dealer]
        prob_18 = dealer_probs.iloc[3, idx_sum_dealer]
        prob_19 = dealer_probs.iloc[4, idx_sum_dealer]
        prob_20 = dealer_probs.iloc[5, idx_sum_dealer]
        prob_21 = dealer_probs.iloc[6, idx_sum_dealer]
        return {"bust": prob_bust, "17": prob_17, "18": prob_18, "19": prob_19, "20": prob_20, "21": prob_21}
