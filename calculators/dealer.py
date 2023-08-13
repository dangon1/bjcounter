def dealRandomPlayerCard(current_deck, player_cards):
    dealt_card = current_deck.pop()
    player_cards.append(dealt_card)
    return dealt_card

def dealRandomDealerCard(current_deck, dealer_cards):
    dealt_card = current_deck.pop()
    dealer_cards.append(dealt_card)
    return dealer_cards