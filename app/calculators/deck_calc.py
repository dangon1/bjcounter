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

def buildDeck(num_decks: int) -> List[Card]:
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'D', 'C', 'S'] # Hearts, Diamonds, Clubs, Spades
    
    deck = [Card(rank, suit) for _ in range(num_decks) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def getGameState(current_deck, player_cards, dealer_cards):
    player_cards_str = [str(card) for card in player_cards]
    dealer_cards_str = [str(card) for card in dealer_cards]

    return {
        "player_cards":{", ".join(player_cards_str)},
        "dealer_cards":{", ".join(dealer_cards_str)},
        "deck_size": len(current_deck)
    }
