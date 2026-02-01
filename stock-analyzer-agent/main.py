from fastapi import FastAPI
from workflow import ask_agent
from pydantic import BaseModel
app = FastAPI()


class StockQuery(BaseModel):
    query: str

@app.get("/")
def pingpong():
    return {"msg": "hello from fastapi server!"}


@app.post("/stock-data")
def getStockInsights(payload: StockQuery):
    answer = ask_agent(payload.query)
    return {"msg": answer}