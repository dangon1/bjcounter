import random
from fastapi import HTTPException
from typing import List

ACE_VALUE_11 = 11

ACE_VALUE_1 = 1


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


def calc_prob_dealer_bust_next_card(cur_comp, dealer_cards):
    sum_dealer_cards = calc_sum_hand(dealer_cards)
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
            prob_busting += cur_comp.get_normalized_prob_rank(str(i))
            print("prob of i:  " + str(prob_busting))
        return prob_busting / 13


def calc_all_probs_dealer(cur_comp, dealer_cards):
    sum_dealer_cards = calc_sum_hand(dealer_cards)
    if sum_dealer_cards < 2:
        raise HTTPException(status_code=400, detail=f"Dealer hasn't been dealt any cards.")
    prob_bust = cur_comp.get_dealer_probs().iloc[1, int(sum_dealer_cards - 2)]
    prob_17 = cur_comp.get_dealer_probs().iloc[2, int(sum_dealer_cards - 2)]
    prob_18 = cur_comp.get_dealer_probs().iloc[3, int(sum_dealer_cards - 2)]
    prob_19 = cur_comp.get_dealer_probs().iloc[4, int(sum_dealer_cards - 2)]
    prob_20 = cur_comp.get_dealer_probs().iloc[5, int(sum_dealer_cards - 2)]
    prob_21 = cur_comp.get_dealer_probs().iloc[6, int(sum_dealer_cards - 2)]
    return { "Bust:": prob_bust, "17": prob_17, "18": prob_18, "19": prob_19, "20": prob_20, "21": prob_21 }
