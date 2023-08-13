# bjcounter

Install python and create a venv:
```$bash
brew install python3
```
From project root run
```$bash
python3 -m venv bjvenv
```
Make sure to activate your `venv` before making changes
```$bash
source bjvenv/bin/activate
```

## To Start APP
After activating the bjvenv run:

```$bash
uvicorn main:app --reload
```

## API curls

### Game state
curl -X 'GET' 'http://localhost:8000/calc/game_state' -H 'accept: application/json'
### Deal player
curl -X 'POST' 'http://localhost:8000/deal/random/deal_player_card' -H 'accept: application/json' -d ''
### Deal dealer
curl -X 'POST' 'http://localhost:8000/deal/random/deal_dealer_card' -H 'accept: application/json' -d ''
### Reset player and dealer hands
curl -X 'PUT' 'http://localhost:8000/reset/player_dealer_hands' -H 'accept: application/json'