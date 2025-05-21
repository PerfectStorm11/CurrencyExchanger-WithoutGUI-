import fastapi
from sqlalchemy import select
from fastapi import HTTPException
from typing import List

from sqlalchemy.orm import Session

from src.schemas.currencyschema import CurrencySchema
from src.database.database import SessionDep
from src.database.models.models import CurrenciesModel,ExchangeRatesModel
import http

router = fastapi.APIRouter("/exchanger")

@router.get("/currencies", response_model=List[CurrencySchema])
async def get_all_currencies(session : SessionDep):
    try:
        query = await session.execute(select(CurrenciesModel))
        currencies = query.scalars().all()
        return currencies, http.HTTPStatus.OK
    except:
        raise HTTPException(status_code=404, detail="Currencies not found")

@router.get("/currencies/{code}", response_model=CurrencySchema)
async def get_currency_by_id(code : str, session : SessionDep):
    try:
        query = await session.execute(select(CurrenciesModel).where(CurrenciesModel.Code == code))
        currency = query.scalars().first()
        return currency, http.HTTPStatus.OK
    except:
        raise HTTPException(status_code=404, detail="Currency not found")

@router.post(f"/currencies/add_currency", response_model=CurrencySchema)
async def create_currency_by_id(currency : CurrencySchema, session : SessionDep):
    try:
        exists = await session.execute(select(CurrenciesModel).where(CurrenciesModel.Code == currency.Code))
        if exists:
            raise HTTPException(status_code=409, detail="Currency already exists")
        else:
            new_currency = CurrenciesModel(
            Code=currency.Code,
            FullName=currency.FullName,
            Symbol=currency.Symbol,
            )
            await session.add(new_currency)
            await session.commit()
            return new_currency, http.HTTPStatus.CREATED
    except:
        raise HTTPException(status_code=404, detail="Currency not found")

@router.get("/exchange_rates", response_model = List[CurrencySchema])
async def get_exchange_rates(session : SessionDep):
    try:
        query = await session.execute(select(ExchangeRatesModel)).scalar()
        query = query.one_or_none()
        return query, http.HTTPStatus.OK
    except:
        raise HTTPException(status_code=404, detail="Exchange rates not found")

@router.get("/exchange_rates/{code1}{code2}")
async def get_exchange_rate_by_id(code1 : str, code2 : str, session : SessionDep):
    if len(code1) !=3 or len(code2) !=3:
        raise HTTPException(status_code=400, detail="Invalid or empty currency code")
    else:
        try:
            query = await session.execute(select(ExchangeRatesModel).where(ExchangeRatesModel.BaseCurrencyId == code1 and  ExchangeRatesModel.TargetCurrencyId == code2))
            query = query.scalar().one_or_none()
            return query, http.HTTPStatus.OK
        except:
            raise HTTPException(status_code=404, detail="Exchange rates not found")