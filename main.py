from re import I
import requests
from fastapi import Depends, Body, FastAPI
from pydantic import Field, BaseModel, HttpUrl
from typing import Union

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float = Field(
        gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

class ExchangeObj(BaseModel):
    currency_from: str
    currency_to: str
    amount_from: float = Field(
        gt=0, description="The excahnged amount from must be greater than zero")
    exchange_rate: Union[float, None] = None
    amount_to: Union[float, None, ] = None
    date_of_exchange: Union[str, None] = None


app = FastAPI()


@app.get("/exchange/")
async def exchange(exchange_object: ExchangeObj = Body()):
    pass

