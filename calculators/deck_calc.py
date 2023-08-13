from typing import List
import logging
import random

class Card:
    def __init__(self, value: str, suit: str):
        self.value = value
        self.suit = suit
    def __str__(self):
        return f"{self.value}{self.suit}"
    def __repr__(self):
        return f"{self.value}{self.suit}"

def deck_builder(num_decks: int) -> List[Card]:
    logging.error("chamou aqui")
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'D', 'C', 'S'] # Hearts, Diamonds, Clubs, Spades
    
    deck = [Card(value, suit) for _ in range(num_decks) for value in values for suit in suits]
    random.shuffle(deck)
    return deck
