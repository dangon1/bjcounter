
from fastapi import FastAPI
from calculators.deck_calc import deck_builder
from constants.constants import NUMBER_OF_DECKS
from calculators import best_play_calc
from calculators import dealer
import logging

app = FastAPI()

current_deck = {}

def on_startup():
    logging.error("called here")
    global current_deck
    current_deck = deck_builder(NUMBER_OF_DECKS)
    logging.error(current_deck)

@app.on_event("startup")
async def startup_event():
    on_startup()

@app.get("/calc/best_play")
async def calcBestPlayContract():
     return best_play_calc.calcBestPlay(current_deck, ["2","3"],"3")

@app.get("/calc/current_deck")
async def getCurrentDeck():
     return { "size": len(current_deck), "deck": tuple(current_deck) }

@app.get("/calc/deal_player_card")
async def dealPlayerCard():
     return dealer.dealPlayerCard(current_deck)
