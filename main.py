
from fastapi import FastAPI
from calculators.best_play_calc import calcBestPlay
app = FastAPI()
@app.get("/calc/best_play")
async def calcBestPlayContract():
     return calcBestPlay(["2","3"],"3")
