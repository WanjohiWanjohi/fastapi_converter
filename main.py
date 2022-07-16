from re import A, I
from fastapi import Depends, Body, FastAPI, HTTPException
from pydantic import Field, BaseModel, HttpUrl
from typing import Dict, List, Union
from datetime import date
from converter import Converter
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class ExchangeObj(BaseModel):
    currency_from: str
    currency_to: str = Field( description="The ")
    amount_from: float = Field(
        gt=0, description="The exchanged amount from must be greater than zero")
    exchange_rate: Union[float, None] = None
    amount_to: Union[float, None, ] = None
    date_of_exchange: Union[date, None] = None


# TODO: APi has two working endpoints
    # 1: Lists all available currencies : Done
    # 2: The converter that converts any available currency into other available currencies
# TODO: Add authentication to the api
app = FastAPI()
all_currencies :List=[] 
@app.get("/symbols")
async def get_currencies(converter: Converter = Depends(Converter)):
    """_summary_
    Returns:
        json: with keys `success` and `symbols`, the latter key:value pairs
    """
    if converter:
        try:
            return converter.get_currencies()
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}")

@app.get("/exchange/")
async def exchange(exchange_object: ExchangeObj = Body(), converter: Converter = Depends(Converter)):
    """_summary_
    Returns:
        _type_: _description_
    """
    if converter:
        try:
            if exchange_object.date_of_exchange:
                return converter.get_historical_rate(str(exchange_object.date_of_exchange), exchange_object.currency_from, exchange_object.currency_to.split(","))
            
            conversion :Dict= converter.get_exchanged_value(exchange_object.amount_to, exchange_object.currency_from, exchange_object.amount_from)
            conversion_rate = float(conversion)
            return{}
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}")
