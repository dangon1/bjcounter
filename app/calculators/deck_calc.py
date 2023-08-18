from typing import List
import logging
import random

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
    suits = ['H', 'D', 'C', 'S'] # Hearts, Diamonds, Clubs, Spades
    
    deck = [Card(rank, suit) for _ in range(num_decks) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def get_game_state(cur_comp, player_cards, dealer_cards):
    player_cards_str = [str(card) for card in player_cards]
    dealer_cards_str = [str(card) for card in dealer_cards]

    return {
        "player_cards":{", ".join(player_cards_str)},
        "dealer_cards":{", ".join(dealer_cards_str)},
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
