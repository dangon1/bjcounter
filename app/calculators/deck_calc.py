import random
from typing import List

ACE_VALUE_11 = 11
ACE_VALUE_1 = 1
HARD_TOTALS_MATRIX_OFFSET = 2
SOFT_TOTALS_MATRIX_OFFSET = 12
HARD_TOTALS_MATRIX_STAND_OFFSET = 4

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}-{self.suit}"

    def __repr__(self):
        return f"{self.rank}-{self.suit}"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False


def build_deck(num_decks: int) -> List[Card]:
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades

    deck = [Card(rank, suit) for _ in range(num_decks) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck


def get_game_state(cur_comp, player_cards, dealer_cards):
    player_cards_str = [str(card) for card in player_cards]
    dealer_cards_str = [str(card) for card in dealer_cards]

    return {
        "player_cards": {", ".join(player_cards_str)},
        "dealer_cards": {", ".join(dealer_cards_str)},
        "deck_size": len(cur_comp.cur_deck),
        "cur_2_size:": cur_comp.get_qty_rank("2"),
        "cur_3_size:": cur_comp.get_qty_rank("3"),
        "cur_4_size:": cur_comp.get_qty_rank("4"),
        "cur_5_size:": cur_comp.get_qty_rank("5"),
        "cur_6_size:": cur_comp.get_qty_rank("6"),
        "cur_7_size:": cur_comp.get_qty_rank("7"),
        "cur_8_size:": cur_comp.get_qty_rank("8"),
        "cur_9_size:": cur_comp.get_qty_rank("9"),
        "cur_T_size:": cur_comp.get_qty_rank(["10", "J", "Q", "K"]),
        "cur_A_size:": cur_comp.get_qty_rank("A")
    }


def calc_card_value(card, ace_value):
    if card.rank == "A":
        rank_value = ace_value
    elif card.rank in ["10", "J", "Q", "K"]:
        rank_value = 10
    else:
        rank_value = int(card.rank)
    return rank_value


def get_cards_ranks(cards):
    return [card.rank for card in cards]


def calc_sum_hand(cards):
    sum_cards = calc_sum_hand_ace_(cards, ACE_VALUE_11)
    if "A" in get_cards_ranks(cards) and sum_cards >= 22:
        sum_cards = calc_sum_hand_ace_(cards, ACE_VALUE_1)
    return sum_cards


def calc_sum_hand_ace_(cards, ace_value):
    sum_cards = 0
    for card in cards:
        rank_value = calc_card_value(card, ace_value)
        sum_cards += rank_value
    return sum_cards

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
        return line_new_value / 9


def get_idx_from_idx_hard(sum1):
    return sum1 + HARD_TOTALS_MATRIX_OFFSET

def get_idx_from_sum_total_hard(sum1):
    return sum1 - HARD_TOTALS_MATRIX_OFFSET

def get_idx_from_sum_total_soft(sum1):
    return sum1 - SOFT_TOTALS_MATRIX_OFFSET

def idx_from_hard_shd(sum1):
    return sum1 - HARD_TOTALS_MATRIX_STAND_OFFSET

def get_prob_stand_until_16(probs_for_rank, stand_hard, idx_j, idx_i):
    # Get the probability of the dealer losing
    prob_player_win = probs_for_rank.get("bust")

    prob_player_lose = (
            probs_for_rank.get("17")
            + probs_for_rank.get("18")
            + probs_for_rank.get("19")
            + probs_for_rank.get("20")
            + probs_for_rank.get("21")
    )

    # print("probBust" + str(prob_player_win))
    # print("prob_against" + str(prob_against))
    stand_hard[idx_j][idx_i] = prob_player_win - prob_player_lose

def get_prob_stand(probs_for_rank, player_rank):
    # Get the probability of the dealer losing
    prob_player_win = (
            probs_for_rank.get("bust")
            + sum(probs_for_rank.get(str(rank)) for rank in range(17, player_rank + 1))
    )

    prob_player_lose = sum(probs_for_rank.get(str(rank)) for rank in range(player_rank, 22))

    return prob_player_win - prob_player_lose