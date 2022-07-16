from re import I
import requests
from fastapi import Depends, Body, FastAPI
from pydantic import Field, BaseModel, HttpUrl
from typing import Union
from converter import Converter

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

#TODO: APi has two working endpoints
    # 1: Lists all available currencies
    # 2: The converter
#TODO: Convert any available currency into other available currencies
#TODO: Add authentication to the api 
app = FastAPI()

@app.get("/symbols")
async def get_currencies(converter: Converter = Depends(Converter)):
   #TODO: use proper error handling here
    if converter:
        try:
            return converter.get_currencies()
        except Exception as e:
            return e
@app.get("/exchange/")
async def exchange(exchange_object: ExchangeObj = Body()):
    pass
@app.get("/exchange/{date}")
async def exchange_historical(exchange_object: ExchangeObj = Body()):
    pass

