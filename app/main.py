from fastapi import FastAPI

from app.admin import admin
from app.calculators import deck_calc
from app.constants.constants import NUMBER_OF_DECKS
from app.calculators import best_play_calc
from app.calculators import dealer
from app.cur_comp import CurComp

app = FastAPI()

player_cards = []
dealer_cards = []
cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))

def on_startup():
     global cur_comp
     cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))

@app.on_event("startup")
async def startup_event():
    on_startup()

@app.get("/admin/show_matrixes")
async def show_matrixes():
     global cur_comp
     return admin.show_matrixes(cur_comp)

@app.get("/admin/prob_bust")
async def prob_bust():
     global cur_comp
     sum_dealer_cards = deck_calc.calc_sum_hand(dealer_cards)
     return cur_comp.calc_all_probs_dealer(sum_dealer_cards)

@app.get("/calc/best_play")
async def calc_best_play_contract():
     global cur_comp
     return best_play_calc.calc_best_play(cur_comp, player_cards, dealer_cards)

@app.get("/calc/game_state")
async def get_game_state():
     return deck_calc.get_game_state(cur_comp, player_cards, dealer_cards)

@app.post("/deal/random/deal_player_card")
async def deal_random_player_card():
     return dealer.deal_random_player_card(cur_comp.cur_deck, player_cards)

@app.post("/deal/random/deal_dealer_card")
async def deal_random_dealer_card():
     return dealer.deal_random_dealer_card(cur_comp.cur_deck, dealer_cards)

@app.post("/deal/specific/deal_player_card")
async def deal_specific_player_card(rank:str, suit: str | None = None):
     return dealer.deal_specific_player_card(cur_comp, player_cards, rank, suit)

@app.post("/deal/specific/deal_dealer_card")
async def deal_specific_dealer_card(rank:str, suit: str | None = None):
     return dealer.deal_specific_player_card(cur_comp, dealer_cards, rank, suit)

@app.put("/reset/player_dealer_hands")
async def reset_player_dealer_hands():
     global player_cards, dealer_cards
     player_cards = []
     dealer_cards = []
     return "OK"

@app.put("/reset/shoe")
async def reset_shoe():
     global player_cards, dealer_cards, cur_comp
     player_cards = []
     dealer_cards = []
     cur_comp = CurComp(deck_calc.build_deck(NUMBER_OF_DECKS))
     return "OK"