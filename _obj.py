from dataclasses import dataclass
from locale import currency


@dataclass
class ExchangeObj:
    currency_from: str
    currency_to: str
    amount_from:float
    exchange_rate:float
    amount_to:float = amount_from * exchange_rate
    