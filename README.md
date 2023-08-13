# bjcounter

### Install python
```$bash
brew install python3
```

### Create a virtual environment and activate it:
From project root run
```$bash
python3 -m venv bjvenv
```
Make sure to activate your `venv` before making changes
```$bash
source bjvenv/bin/activate
```

### Install the requirements
pip3 install -r requirements.txt

### To Start APP
After activating the bjvenv run:

```$bash
uvicorn app.main:app --reload
```


## Development

### Adding dependencies

```
# Install the dependency using pip
pip3 install <dependency_name>

# Update the requirements.txt with the dependencies
pip3 freeze > requirements.txt

```

### Verify if pytest is on your path
if using zsh, check if on ~/.zshrc there is the line:
export PATH=$PATH:/home/ddeaguiargoncalves/.local/bin

### API curls

#### Game state
curl -X 'GET' 'http://localhost:8000/calc/game_state' -H 'accept: application/json'
#### Deal player
curl -X 'POST' 'http://localhost:8000/deal/random/deal_player_card' -H 'accept: application/json' -d ''
#### Deal dealer
curl -X 'POST' 'http://localhost:8000/deal/random/deal_dealer_card' -H 'accept: application/json' -d ''
#### Reset player and dealer hands
curl -X 'PUT' 'http://localhost:8000/reset/player_dealer_hands' -H 'accept: application/json'