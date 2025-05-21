from pydantic import BaseModel, Field
from typing import Optional

class Base(BaseModel):
    pass


class CurrencySchema(Base):
    Code : str
    Fullname : str
    Symbol : str

