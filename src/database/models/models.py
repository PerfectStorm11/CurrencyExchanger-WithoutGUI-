import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass

class CurrenciesModel(Base):
    __tablename__ = "Currencies"

    ID : Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    Code : Mapped[str] = Column(String, unique=True)
    FullName : Mapped[str] = Column(String)
    Symbol : Mapped[str] = Column(String)

class ExchangeRatesModel(Base):
    __tablename__ = "Exchange_Rates"

    ID : Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    BaseCurrencyId : Mapped[int] = Column(Integer, ForeignKey("Currencies.ID"))
    TargetCurrencyId : Mapped[int] = Column(Integer, ForeignKey("Currencies.ID"))
    Rate : Mapped[float] = Column(DECIMAL(6))
