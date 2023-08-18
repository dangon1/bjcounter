from fastapi import HTTPException
from app.calculators.deck_calc import Card


def deal_random_player_card(current_deck, player_cards):
    dealt_card = current_deck.pop()
    player_cards.append(dealt_card)
    return dealt_card

def deal_random_dealer_card(current_deck, dealer_cards):
    dealt_card = current_deck.pop()
    dealer_cards.append(dealt_card)
    return dealer_cards

def deal_specific_player_card(current_deck, player_cards, rank, suit):
    card_to_remove = Card(rank, suit)
    try:
        index_to_remove = current_deck.index(card_to_remove)
        dealt_card = current_deck.pop(index_to_remove)
        player_cards.append(dealt_card)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Card {card_to_remove} not found")
    return dealt_card