import json
from re import A, I
import re
from fastapi import Depends, Body, FastAPI, HTTPException, status
from pydantic import Field, BaseModel, HttpUrl
from typing import Dict, List, Union
from datetime import date
from converter import Converter
from auth import UserInDB, User, fake_users_db, fake_hash_password, get_current_active_user,oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
all_currencies: List = []
class ExchangeObj(BaseModel):
    currency_from: str
    currency_to: str = Field(description="The ")
    amount_from: float = Field(
        gt=0, description="The exchanged amount from must be greater than zero")
    exchange_rate: Union[float, None] = None
    amount_to: Union[float, None, ] = None
    date_of_exchange: Union[date, None] = None

# TODO: Use proper db for authentication (stretch goal)
app = FastAPI()

@app.post("/token",  include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/symbols/")
async def get_currencies(current_user: User = Depends(get_current_active_user), converter: Converter = Depends(Converter)):
    """_summary_
    Returns:
        json: with keys `success` and `symbols`, the latter key:value pairs of currencies available for conversion
    """
    if converter:
        try:
            return converter.get_currencies()
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}")


@app.post("/exchange/")
async def exchange(exchange_object: ExchangeObj = Body(), converter: Converter = Depends(Converter), token: str = Depends(oauth2_scheme)):
    """_summary_
    Returns:
        _type_: _description_
    """
    if converter:
        try:
            if exchange_object.date_of_exchange:
                result = converter.get_historical_rate(str(exchange_object.date_of_exchange), str(exchange_object.currency_from), exchange_object.currency_to.split(","))
                print(result)
                return result
            else:
              result = converter.get_exchanged_value(exchange_object.currency_to, exchange_object.currency_from, str(exchange_object.amount_from))
              json_result = json.loads(result)
              exchange_object.exchange_rate = json_result["info"]["rate"]
              exchange_object.amount_to = json_result["result"]
              exchange_object.date_of_exchange = json_result["date"]              
              return exchange_object
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}")
