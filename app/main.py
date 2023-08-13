from fastapi import FastAPI
from app.calculators import deck_calc
from app.constants.constants import NUMBER_OF_DECKS
from app.calculators import best_play_calc
from app.calculators import dealer
import logging

app = FastAPI()

current_deck = []
player_cards = []
dealer_cards = []

def on_startup():
    global current_deck
    current_deck = deck_calc.buildDeck(NUMBER_OF_DECKS)

@app.on_event("startup")
async def startup_event():
    on_startup()

@app.get("/calc/best_play")
async def calcBestPlayContract():
     return best_play_calc.calcBestPlay(current_deck, player_cards, dealer_cards)

@app.get("/calc/game_state")
async def getGameState():
     return deck_calc.getGameState(current_deck, player_cards, dealer_cards)

@app.post("/deal/random/deal_player_card")
async def dealRandomPlayerCard():
     return dealer.dealRandomPlayerCard(current_deck, player_cards)

@app.post("/deal/random/deal_dealer_card")
async def dealRandomDealerCard():
     return dealer.dealRandomDealerCard(current_deck, dealer_cards)

@app.put("/reset/player_dealer_hands")
async def resetPlayerDealerhands():
     global player_cards, dealer_cards
     player_cards = []
     dealer_cards = []
     return "OK"

@app.put("/reset/shoe")
async def resetPlayerDealerhands():
     global player_cards, dealer_cards, current_deck
     player_cards = []
     dealer_cards = []
     current_deck = deck_calc.buildDeck(NUMBER_OF_DECKS)
     return "OK"