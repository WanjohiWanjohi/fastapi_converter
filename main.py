from re import A, I
from fastapi import Depends, Body, FastAPI, HTTPException, status
from pydantic import Field, BaseModel, HttpUrl
from typing import Dict, List, Union
from datetime import date
from converter import Converter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class ExchangeObj(BaseModel):
    currency_from: str
    currency_to: str = Field(description="The ")
    amount_from: float = Field(
        gt=0, description="The exchanged amount from must be greater than zero")
    exchange_rate: Union[float, None] = None
    amount_to: Union[float, None, ] = None
    date_of_exchange: Union[date, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_hash_password(password: str):
    # TODO: implement password hashing
    return "fakehashed" + password


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
# TODO: APi has two working endpoints
    # 2: The converter that converts any available currency into other available currencies
# TODO: Use proper db for authentication (stretch goal)
#TODO: Refactor security & API into different files
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


all_currencies: List = []


@app.get("/symbols/")
async def get_currencies(current_user: User = Depends(get_current_active_user), converter: Converter = Depends(Converter)):
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
async def exchange(exchange_object: ExchangeObj = Body(), converter: Converter = Depends(Converter), token: str = Depends(oauth2_scheme)):
    """_summary_
    Returns:
        _type_: _description_
    """
    if converter:
        try:
            if exchange_object.date_of_exchange:
                return converter.get_historical_rate(str(exchange_object.date_of_exchange), exchange_object.currency_from, exchange_object.currency_to.split(","))

            conversion: Dict = converter.get_exchanged_value(
                exchange_object.amount_to, exchange_object.currency_from, exchange_object.amount_from)
            conversion_rate = float(conversion)
            return{}
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}")
